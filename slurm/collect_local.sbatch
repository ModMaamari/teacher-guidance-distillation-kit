#!/usr/bin/env bash
# Collect teacher-guided episodes with the student served on this job's GPU by vLLM. The
# teacher defaults to that same served model, which is self-teaching: the model reviews its
# own plan and steps with the gold answer in view, and the leakage sanitiser keeps the answer
# out of the guidance it then reads as the student (docs/EXPERIMENTS.md, experiment 5). Set
# TEACHER to any provider-prefixed id to pair the local student with a different teacher.
#
#   MODEL=<hf model id> OUT=runs/collect_self \
#     sbatch -p <partition> --gres=gpu:<type>:1 slurm/collect_local.sbatch [collect_episodes.py args]
#
# Ask for a GPU type that fits the model: an untyped --gres=gpu:1 can land on a card too
# small to serve it. All datasets run at once, SHARDS workers each, against one server that
# batches their requests. Resumable: resubmit, or chain chunks with
# --dependency=afterany:<previous id>, to continue past the time limit.
#SBATCH --job-name=tgd_collect_local
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=32
#SBATCH --mem=128G
#SBATCH --time=04:00:00
#SBATCH --output=runs/slurm/collect_local_%j.log
set -uo pipefail
cd "${SLURM_SUBMIT_DIR:-$PWD}"
source slurm/common.sh

MODEL="${MODEL:-ibm-granite/granite-4.1-3b}"
TEACHER="${TEACHER:-vllm/student}"
OUT="${OUT:?set OUT to a run directory no other job uses}"
TAG="${TAG:-collect_local}"
SHARDS="${SHARDS:-8}"   # workers per dataset
N="${N:-2000}"
PORT="${PORT:-8310}"
DATASETS="${DATASETS:-2wikimultihopqa hotpotqa musique strategyqa}"
# Teacher prompts carry the whole trajectory, and a repair retry doubles the output budget.
export MAX_LEN="${MAX_LEN:-32768}"
export VLLM_ENDPOINT="http://127.0.0.1:$PORT"

echo "== served model $MODEL (as vllm/student)"
echo "== teacher $TEACHER"
echo "== datasets $DATASETS, $SHARDS workers each, out $OUT"

$PY_BASE scripts/verify_collection.py --runs "$OUT" --prune --repair-checkpoints --yes || true

MODEL=$MODEL start_server "$PORT" || { echo "!! the model failed to serve"; exit 1; }
trap stop_server EXIT

# One question end to end before the chunk, so a serving, template or parsing problem costs
# a minute instead of a chunk of errored episodes. It writes outside OUT, where consolidation
# never looks.
PRE="runs/preflight_${SLURM_JOB_ID:-local}"
rm -rf "$PRE"
$PY_TRAIN scripts/collect_episodes.py --datasets hotpotqa --num-samples 1 --smoke \
    --student vllm/student --teacher "$TEACHER" --out "$PRE" --tag "${TAG}_preflight" \
    --student-max-tokens "${STUDENT_MAX_TOKENS:-3000}" > "$PRE.log" 2>&1
if ! $PY_BASE scripts/consolidate_episodes.py --runs "$PRE" --out "$PRE/check" --strict \
    --expect hotpotqa=1 >> "$PRE.log" 2>&1; then
  echo "!! preflight episode missing or errored, see $PRE.log"; tail -20 "$PRE.log"; exit 1
fi
echo "== preflight passed"

# shellcheck disable=SC2086  # DATASETS is a word list
$PY_TRAIN scripts/collect_episodes.py --datasets $DATASETS --num-samples "$N" \
    --student vllm/student --teacher "$TEACHER" --shards "$SHARDS" --out "$OUT" --tag "$TAG" \
    --student-max-tokens "${STUDENT_MAX_TOKENS:-3000}" "$@"
rc=$?

echo; echo "== verification"
$PY_BASE scripts/verify_collection.py --runs "$OUT" || true
echo "== done $(date -u +%FT%TZ) rc=$rc"
exit $rc
