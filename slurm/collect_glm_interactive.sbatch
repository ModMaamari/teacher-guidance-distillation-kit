#!/usr/bin/env bash
# Collect on the interactive partition, in 4-hour chunks.
#
# The gpu partition estimated a 9-day wait after a day of heavy use dropped our fair-share
# there to 0.016. Interactive sits at 0.061 because we have barely touched it, and offers a
# slot within hours -- at the price of a 4-hour cap. The collector is resumable, so the run
# is simply split across chunks; each one skips what is already on disk.
#
# Target the GPU type explicitly: an untyped request on this partition schedules onto a
# 2014 Titan Black with 6 GB, which cannot serve the student.
#
# Collect one dataset at a time, so concurrency stays at the measured safe level.
#
# collect_episodes.py's --shards is PER DATASET. Passing four datasets with --shards 16
# ran 64 workers: 8,260 rate-limit responses, 96 GB peak RSS (killed OOM), and 5.1% of
# questions produced no episode at all because every model call had exhausted its retries.
# Running datasets sequentially keeps 16 workers -- the level that drew no 429s when
# measured -- without renaming the per-shard output directories, so episodes already
# collected are still recognised and skipped.
#SBATCH --job-name=tgd_collect_int
#SBATCH --cpus-per-task=16
#SBATCH --mem=256G
#SBATCH --time=04:00:00
#SBATCH --output=runs/slurm/collect_int_%j.log
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
export OPENROUTER_PROVIDER_ONLY="${OPENROUTER_PROVIDER_ONLY:-DeepInfra}"
export OPENROUTER_REASONING="${OPENROUTER_REASONING:-low}"
export VLLM_ENDPOINT="http://127.0.0.1:$PORT"

echo "== $(date -u +%FT%TZ) node=$(hostname) job=${SLURM_JOB_ID:-local}"
echo "== teacher $TEACHER  provider=$OPENROUTER_PROVIDER_ONLY reasoning=$OPENROUTER_REASONING"
echo "== student $STUDENT_MODEL  thinking=${VLLM_CHAT_TEMPLATE_KWARGS:-on}"
echo "== $SHARDS workers per dataset, datasets run one at a time"

# Repair bookkeeping before collecting. A worker records a sample as completed once it
# has finished attempting it and marks the shard status=completed at the end of its list,
# so questions that produced no episode are skipped by every later resume. Without this
# the run converges to whatever the first pass happened to get, not to the full dataset.
echo "== repairing markers and checkpoints before this chunk"
$PY_BASE scripts/verify_collection.py --runs "$OUT" --prune --repair-checkpoints --yes || true

# Refuse to start a chunk on a nearly empty account. The budget is small and this run has
# already met several bugs that spend money without producing new questions; a floor makes
# the worst case a stopped chunk rather than an exhausted key.
CREDIT_FLOOR="${CREDIT_FLOOR:-1.00}"
left=$($PY_BASE - <<'PY'
import json, os, urllib.request
req = urllib.request.Request("https://openrouter.ai/api/v1/credits",
    headers={"Authorization": "Bearer " + os.environ.get("CUSTOM_LLM_API_KEY", "")})
try:
    d = json.loads(urllib.request.urlopen(req, timeout=60).read())["data"]
    print(f"{d['total_credits'] - d['total_usage']:.2f}")
except Exception:
    print("unknown")
PY
)
echo "== OpenRouter credit remaining: \$$left (floor \$$CREDIT_FLOOR)"
if [ "$left" != "unknown" ] && awk "BEGIN{exit !($left < $CREDIT_FLOOR)}"; then
  echo "!! credit below floor -- not starting this chunk"; exit 1
fi

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
