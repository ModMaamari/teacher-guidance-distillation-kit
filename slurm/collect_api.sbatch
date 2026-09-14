#!/usr/bin/env bash
# Collect teacher-guided episodes when the student and the teacher are both API models: no
# GPU and no vLLM server, so any CPU partition will do. The typical use is self-teaching,
# where one model plays both roles (docs/EXPERIMENTS.md, experiment 5).
#
#   STUDENT=oai-x/org/model TEACHER=oai-x/org/model OUT=runs/collect_self/hotpotqa \
#     DATASETS=hotpotqa sbatch -p <partition> slurm/collect_api.sbatch [collect_episodes.py args]
#
# Give every concurrent job its own OUT. The job prunes orphaned sample directories before it
# starts, and in a shared OUT it would delete the questions another job is still collecting.
#
# Resumable: a resubmitted job skips finished questions and retries errored ones, so a run
# longer than the time limit is a chain of jobs (sbatch --dependency=afterany:<previous id>).
#SBATCH --job-name=tgd_collect_api
#SBATCH --cpus-per-task=8
#SBATCH --mem=32G
#SBATCH --time=04:00:00
#SBATCH --output=runs/slurm/collect_api_%j.log
set -uo pipefail
cd "${SLURM_SUBMIT_DIR:-$PWD}"
source slurm/common.sh

STUDENT="${STUDENT:?set STUDENT to a provider-prefixed model id}"
TEACHER="${TEACHER:?set TEACHER to a provider-prefixed model id}"
OUT="${OUT:?set OUT to a run directory no other job uses}"
TAG="${TAG:-collect_api}"
SHARDS="${SHARDS:-8}"   # workers per dataset
N="${N:-2000}"
DATASETS="${DATASETS:-2wikimultihopqa hotpotqa musique strategyqa}"

echo "== student $STUDENT"
echo "== teacher $TEACHER"
echo "== datasets $DATASETS, $SHARDS workers each, out $OUT"

$PY_BASE scripts/verify_collection.py --runs "$OUT" --prune --repair-checkpoints --yes || true

# Both endpoints must answer before any worker starts: a wrong key or model id would
# otherwise turn every question of the chunk into an errored episode.
for model in "$STUDENT" "$TEACHER"; do
  $PY_BASE - "$model" <<'PY' || { echo "!! $model did not answer"; exit 1; }
import asyncio
import sys

import tgd  # noqa: F401
from agentsim.clients.llm_client import LLMClient


async def main():
    r = await LLMClient().get_completion(prompt="Reply with OK.", model=sys.argv[1], temperature=0.0, max_tokens=8)
    print("== ready:", sys.argv[1], repr((r.get("text") if isinstance(r, dict) else r)[:20]))

asyncio.run(main())
PY
done

# shellcheck disable=SC2086  # DATASETS is a word list
$PY_TRAIN scripts/collect_episodes.py --datasets $DATASETS --num-samples "$N" \
    --student "$STUDENT" --teacher "$TEACHER" --shards "$SHARDS" --out "$OUT" --tag "$TAG" \
    --student-max-tokens "${STUDENT_MAX_TOKENS:-3000}" "$@"
rc=$?

echo; echo "== verification"
$PY_BASE scripts/verify_collection.py --runs "$OUT" || true
echo "== done $(date -u +%FT%TZ) rc=$rc"
exit $rc
