#!/usr/bin/env bash
# Validate the student half of collection without spending teacher credit: serve the
# student and run a few episodes with a mock teacher. Exercises the chat template, the
# action schema, the tools and the on-disk layout -- everything except the real teacher.
#
#   sbatch -p <gpu-partition> slurm/test_student_collect.sbatch
#   STUDENT_MODEL=ibm-granite/granite-4.1-3b PORT=8312 OUT=runs/t41 sbatch ... # A/B
#
# Check the result with:
#   python scripts/check_student_actions.py --runs <OUT>
#SBATCH --job-name=tgd_test_student
#SBATCH --cpus-per-task=8
#SBATCH --mem=64G
#SBATCH --time=01:30:00
#SBATCH --output=runs/slurm/test_student_%j.log
set -uo pipefail
cd "${SLURM_SUBMIT_DIR:-$PWD}"
source slurm/common.sh
STUDENT_MODEL="${STUDENT_MODEL:-ibm-granite/granite-4.2-3b}"
PORT="${PORT:-8311}"
OUT="${OUT:-runs/collect_studenttest}"
N="${N:-4}"
DATASET="${DATASET:-hotpotqa}"

echo "== $(date -u +%FT%TZ) node=$(hostname) job=${SLURM_JOB_ID:-local}"
echo "== student $STUDENT_MODEL  port $PORT  out $OUT"
echo "== chat_template_kwargs: ${VLLM_CHAT_TEMPLATE_KWARGS:-<unset>}"
export VLLM_ENDPOINT="http://127.0.0.1:$PORT"

MODEL=$STUDENT_MODEL start_server "$PORT" || { echo "!! student failed to serve"; exit 1; }
trap stop_server EXIT
curl -sf "http://127.0.0.1:$PORT/v1/chat/completions" -H 'Content-Type: application/json' \
  -d '{"model":"student","messages":[{"role":"user","content":"Reply with the single word OK."}],"max_tokens":300}' \
  | $PY_BASE -c "import json,sys;m=json.load(sys.stdin)['choices'][0]['message'];print('student says:',repr((m.get('content') or '')[:90]))"

echo "== $N episodes with a MOCK teacher (no API spend)"
$PY_TRAIN scripts/collect_episodes.py --datasets "$DATASET" --num-samples "$N" \
    --student vllm/student --teacher mock/teacher --shards 1 \
    --out "$OUT" --tag "$(basename "$OUT")"
rc=$?
echo "== collector rc=$rc  episodes: $(find "$OUT" -name _SUCCESS 2>/dev/null | wc -l)"
$PY_BASE scripts/check_student_actions.py --runs "$OUT" || true
echo "== done $(date -u +%FT%TZ)"
exit $rc
