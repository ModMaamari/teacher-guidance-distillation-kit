#!/usr/bin/env bash
# A small REAL collection batch: local student + GLM teacher on OpenRouter + judge.
# Everything the full run does, at 12 questions, so the episodes can be inspected first.
#SBATCH --job-name=tgd_real_batch
#SBATCH --cpus-per-task=16
#SBATCH --mem=96G
#SBATCH --time=02:00:00
#SBATCH --output=runs/slurm/real_batch_%j.log
set -uo pipefail
cd "${SLURM_SUBMIT_DIR:-$PWD}"
source slurm/common.sh
STUDENT_MODEL="${STUDENT_MODEL:-ibm-granite/granite-4.2-3b}"
TEACHER="${TEACHER:-custom/z-ai/glm-5.3-flash}"
OUT="${OUT:-runs/collect_realtest}"
PORT="${PORT:-8320}"
N="${N:-3}"                      # per dataset
SHARDS="${SHARDS:-3}"
STUDENT_MAX_TOKENS="${STUDENT_MAX_TOKENS:-3000}"

echo "== $(date -u +%FT%TZ) node=$(hostname) job=${SLURM_JOB_ID:-local}"
echo "== student $STUDENT_MODEL (max_tokens=$STUDENT_MAX_TOKENS)"
echo "== teacher $TEACHER provider=${OPENROUTER_PROVIDER_ONLY:-any} reasoning=${OPENROUTER_REASONING:-default}"
export VLLM_ENDPOINT="http://127.0.0.1:$PORT"

echo "== teacher readiness"
$PY_BASE scripts/check_teacher_openrouter.py || { echo "!! teacher not ready"; exit 1; }

MODEL=$STUDENT_MODEL start_server "$PORT" || { echo "!! student failed to serve"; exit 1; }
trap stop_server EXIT

echo "== collecting $((N*4)) episodes across all four datasets"
$PY_TRAIN scripts/collect_episodes.py \
    --datasets hotpotqa 2wikimultihopqa musique strategyqa \
    --num-samples "$N" --student vllm/student --teacher "$TEACHER" \
    --shards "$SHARDS" --out "$OUT" --tag realtest \
    --student-max-tokens "$STUDENT_MAX_TOKENS"
rc=$?
echo "== collector rc=$rc  episodes: $(find "$OUT" -name _SUCCESS 2>/dev/null | wc -l)"
echo; echo "== did the student's steps parse?"
$PY_BASE scripts/check_student_actions.py --runs "$OUT" || true
echo; echo "== spend + progress"
$PY_BASE scripts/watch_collection.py --out "$OUT" || true
echo "== done $(date -u +%FT%TZ)"
exit $rc
