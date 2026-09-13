#!/usr/bin/env bash
# Collect one dataset at a time, so concurrency stays at the measured safe level.
#
# collect_episodes.py's --shards is PER DATASET. Passing four datasets with --shards 16
# ran 64 workers: 8,260 rate-limit responses, 96 GB peak RSS (killed OOM), and 5.1% of
# questions produced no episode at all because every model call had exhausted its retries.
# Running datasets sequentially keeps 16 workers -- the level that drew no 429s when
# measured -- without renaming the per-shard output directories, so episodes already
# collected are still recognised and skipped.
#SBATCH --job-name=tgd_collect_seq
#SBATCH --cpus-per-task=16
#SBATCH --mem=256G
#SBATCH --time=24:00:00
#SBATCH --output=runs/slurm/collect_seq_%j.log
set -uo pipefail
cd "${SLURM_SUBMIT_DIR:-$PWD}"
source slurm/common.sh

STUDENT_MODEL="${STUDENT_MODEL:-ibm-granite/granite-4.2-3b}"
TEACHER="${TEACHER:-custom/z-ai/glm-5.3-flash}"
OUT="${OUT:-runs/collect_glm}"
SHARDS="${SHARDS:-16}"
PORT="${PORT:-8310}"
N="${N:-2000}"
DATASETS="${DATASETS:-2wikimultihopqa hotpotqa strategyqa musique}"
# No default provider. `:-DeepInfra` pinned every job to DeepInfra whenever .env left this
# empty to enable the self-reordering ladder, so the ladder never ran and ~98% of episode
# errors were DeepInfra 429s that should have stepped down to Relace or Morph.
export OPENROUTER_PROVIDER_ONLY="${OPENROUTER_PROVIDER_ONLY-}"
export OPENROUTER_REASONING="${OPENROUTER_REASONING:-low}"
export VLLM_ENDPOINT="http://127.0.0.1:$PORT"

echo "== $(date -u +%FT%TZ) node=$(hostname) job=${SLURM_JOB_ID:-local}"
echo "== teacher $TEACHER  provider=$OPENROUTER_PROVIDER_ONLY reasoning=$OPENROUTER_REASONING"
echo "== student $STUDENT_MODEL  thinking=${VLLM_CHAT_TEMPLATE_KWARGS:-on}"
echo "== $SHARDS workers per dataset, datasets run one at a time"

$PY_BASE scripts/check_teacher_openrouter.py || { echo "!! teacher not ready"; exit 1; }
MODEL=$STUDENT_MODEL start_server "$PORT" || { echo "!! student failed to serve"; exit 1; }
trap stop_server EXIT

rc=0
for ds in $DATASETS; do
  echo; echo "######## $ds  $(date -u +%FT%TZ)"
  $PY_TRAIN scripts/collect_episodes.py --datasets "$ds" --num-samples "$N" \
      --student vllm/student --teacher "$TEACHER" --shards "$SHARDS" \
      --out "$OUT" --tag collect --student-max-tokens "${STUDENT_MAX_TOKENS:-3000}" || rc=$?
  $PY_BASE scripts/verify_collection.py --runs "$OUT" 2>&1 | head -8
done

echo; echo "== final verification"
$PY_BASE scripts/verify_collection.py --runs "$OUT" || true
echo "== done $(date -u +%FT%TZ) rc=$rc"
echo "   orphans left? re-run this script; it prunes nothing automatically"
exit $rc
