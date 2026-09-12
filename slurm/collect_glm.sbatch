#!/usr/bin/env bash
# Collect teacher-guided episodes with a GLM teacher on OpenRouter and a local granite
# student. Resumable and monitorable: re-submitting continues where it stopped.
#
#   sbatch -p <gpu-partition> slurm/collect_glm.sbatch [--num-samples N] [--datasets ...]
#
# Env it needs (put in .env):
#   CUSTOM_LLM_ENDPOINT=https://openrouter.ai/api
#   CUSTOM_LLM_API_KEY=sk-or-...
# Routing is pinned below so the run cannot silently change backend or start paying for
# reasoning tokens halfway through.
#SBATCH --job-name=tgd_collect_glm
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=16
#SBATCH --mem=96G
#SBATCH --time=24:00:00
#SBATCH --output=runs/slurm/collect_glm_%j.log
set -uo pipefail
cd "${SLURM_SUBMIT_DIR:-$PWD}"
source slurm/common.sh

STUDENT_MODEL="${STUDENT_MODEL:-ibm-granite/granite-4.2-3b}"
TEACHER="${TEACHER:-custom/z-ai/glm-5.3-flash}"
OUT="${OUT:-runs/collect_glm}"
# 16 is the measured ceiling before the endpoint starts returning 429: at 16
# concurrent teacher calls nothing was rate-limited (3,145 calls/h); at 24 and 32
# a third of requests were rejected. ~43k teacher calls -> about 14 h.
SHARDS="${SHARDS:-16}"
PORT="${PORT:-8310}"

# Pin the upstream provider and switch reasoning off. allow_fallbacks=False is applied by
# the client, so a routing failure stops the run rather than quietly moving to a provider
# with different pricing and different sampling.
export OPENROUTER_PROVIDER_ONLY="${OPENROUTER_PROVIDER_ONLY:-DeepInfra}"
# glm-5.3-flash refuses reasoning:{enabled:false} on every provider ("Reasoning is
# mandatory for this endpoint"), so low effort is the cheapest setting available.
export OPENROUTER_REASONING="${OPENROUTER_REASONING:-low}"

echo "== $(date -u +%FT%TZ) node=$(hostname) job=${SLURM_JOB_ID:-local}"
nvidia-smi --query-gpu=name,memory.total --format=csv,noheader
echo "== student  $STUDENT_MODEL   (served locally as vllm/student)"
echo "== teacher  $TEACHER  provider=$OPENROUTER_PROVIDER_ONLY reasoning=$OPENROUTER_REASONING"
echo "== out      $OUT   shards=$SHARDS"
echo "== student thinking: ${VLLM_CHAT_TEMPLATE_KWARGS:-on (default)}"

# the collector addresses the student as vllm/student; point the client at this port
export VLLM_ENDPOINT="http://127.0.0.1:$PORT"
MODEL=$STUDENT_MODEL start_server "$PORT" || exit 1
trap stop_server EXIT

$PY_TRAIN scripts/collect_episodes.py \
    --student "vllm/student" \
    --teacher "$TEACHER" \
    --shards "$SHARDS" \
    --out "$OUT" \
    --student-max-tokens "${STUDENT_MAX_TOKENS:-3000}" \
    "$@"
rc=$?
echo "== done $(date -u +%FT%TZ) rc=$rc"
[ $rc -ne 0 ] && echo "!! incomplete - resubmit the same command to resume"
exit $rc
