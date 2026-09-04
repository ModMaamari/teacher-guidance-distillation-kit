#!/usr/bin/env bash
#SBATCH --job-name=tgd_stability
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=8
#SBATCH --mem=64G
#SBATCH --time=03:00:00
#SBATCH --output=runs/slurm/stability_%j.log
# Decoding-stability check: does the trained student still work when it is SAMPLED?
#
#   sbatch [-p <partition>] slurm/eval_stability.sbatch <adapter-dir> [arm-name]
#   sbatch slurm/eval_stability.sbatch runs/train/uniform/adapter trained
#
# A model can be excellent at greedy decoding and unusable at temperature 0.3 -- greedy
# needs only the ranking of the top token, sampling needs its probability to be right.
# This measures both, and the distribution that explains the difference:
#
#   1. merge the adapter, so the runtime LoRA path is not a variable
#   2. next-token distributions in and out of distribution (the diagnostic)
#   3. accuracy and format compliance across temperature and truncation (MMLU)
#   4. the agent task at greedy, 0.3-nucleus and 0.3-min-p (where compounding bites)
#
# Env: STUDENT_MODEL (base id), TEST_SET (default heldout_musique), SWEEP_N, CONCURRENCY.
set -uo pipefail
mkdir -p runs/slurm
ROOT=${SLURM_SUBMIT_DIR:-$(cd "$(dirname "$0")/.." && pwd)}   # submit from the project root
. "$ROOT/slurm/common.sh"
ADAPTER=${1:?adapter dir, e.g. runs/train/uniform/adapter}
ARM=${2:-trained}
BASE=${STUDENT_MODEL:-ibm-granite/granite-4.1-3b}
TEST=${TEST_SET:-heldout_musique}
DS=${TEST#*_}
OUT=runs/stability/$ARM
PORT=${PORT:-8300}
MERGED=$OUT/merged
mkdir -p "$OUT"
[ -f "$ADAPTER/adapter_config.json" ] || { echo "no adapter at $ADAPTER"; exit 1; }

echo "=== 1/5 merge the adapter into the base weights"
$PY_TRAIN scripts/merge_adapter.py --base "$BASE" --adapter "$ADAPTER" --out "$MERGED" || exit 1

echo "=== 2/5 next-token distributions (the calibration diagnostic)"
$PY_TRAIN scripts/diag_distributions.py --models "base=$BASE" "$ARM=$MERGED" \
    --n 200 --out "$OUT/diag" || echo "!! distributions failed"

echo "=== 3/5 decoding sweep on MMLU"
$PY_TRAIN scripts/sweep_decoding.py --models "$ARM=$MERGED" --n 100 --out "$OUT/diag" \
    || echo "!! decoding sweep failed"

echo "=== 4/5 where along the completion the distribution goes flat"
$PY_TRAIN scripts/diag_position_profile.py --models "base=$BASE" "$ARM=$MERGED" \
    --data data/splits/uniform/dev.jsonl --n 48 --out "$OUT/diag_positions" \
    || echo "!! position profile failed"

echo "=== 5/5 the agent task under three decoders"
MODEL=$MERGED start_server "$PORT" || exit 1
trap stop_server EXIT
run () {  # run <label> <temperature> [extra eval args]
  local label=$1 T=$2; shift 2
  local d=$OUT/agent/$label; mkdir -p "$d"
  [ -f "$d/.done" ] && { echo "  skip $label"; return; }
  $PY_TRAIN scripts/eval.py --arm student --student vllm --server-url "http://127.0.0.1:$PORT" \
      --served-model student --questions "data/splits/test/${TEST}_questions.jsonl" \
      --corpus "data/questions/$DS/${DS}_corpus.jsonl.gz" --out "$d" \
      --student-temperature "$T" "$@" > "$d/stdout.log" 2>&1 \
    || echo "  !! $label incomplete"
  [ -f "$d/metrics.json" ] && $PY_BASE -c "
import json; m=json.load(open('$d/metrics.json'))
print(f\"  $label: cover {m['cover_match']:.3f} | em {m['em']:.3f} | invalid {m['invalid_action_steps']}/{m['total_steps']}\")"
}
run greedy      0.0
run T0.3_nucleus 0.3
run T0.3_minp    0.3 --min-p 0.1
echo "=== done $(date -u +%FT%TZ) -> $OUT"
