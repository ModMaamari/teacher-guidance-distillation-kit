#!/usr/bin/env bash
#SBATCH --job-name=tgd_forgetting
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=16
#SBATCH --mem=96G
#SBATCH --time=04:00:00
#SBATCH --output=runs/slurm/forgetting_%j.log
# Forgetting check: does the student keep its general abilities after training on
# teacher-guidance trajectories? The base weights and the trained adapter answer the
# same standard benchmarks through ONE vLLM server, so the adapter is the only
# difference between the arms.
#
#   sbatch [-p <gpu-partition> -A <account>] slurm/eval_forgetting.sbatch <adapter-dir> [arm-name]
#   sbatch slurm/eval_forgetting.sbatch runs/train/uniform/adapter trained_uniform
#
# RUNS=5 repeats every (arm, benchmark) five times with distinct sampling seeds at
# TEMPERATURE (default 0.7 when RUNS>1), so the spread across replicates measures
# decoding noise and the comparison can be tested for significance. RUNS=1 (default)
# runs once, greedy and deterministic.
#
# Resumable: a finished (arm, benchmark, run) triple is skipped on resubmission.
set -uo pipefail
mkdir -p runs/slurm
ROOT=${SLURM_SUBMIT_DIR:-$(cd "$(dirname "$0")/.." && pwd)}   # submit from the project root
. "$ROOT/slurm/common.sh"
ADAPTER=${1:?adapter dir, e.g. runs/train/uniform/adapter}
ARM=${2:-trained}
OUT=runs/forgetting
PORT=${PORT:-8300}
BENCHMARKS=${BENCHMARKS:-"mmlu gsm8k hellaswag"}
STUDENT_MODEL=${STUDENT_MODEL:-ibm-granite/granite-4.1-3b}
RUNS=${RUNS:-1}
if [ "$RUNS" -gt 1 ]; then TEMPERATURE=${TEMPERATURE:-0.7}; else TEMPERATURE=${TEMPERATURE:-0.0}; fi
SEEDS=${SEEDS:-"13 17 23 29 31 37 41 43 47 53"}

[ -f "$ADAPTER/adapter_config.json" ] || { echo "no adapter at $ADAPTER"; exit 1; }
for b in $BENCHMARKS; do
  [ -f "data/benchmarks/$b.jsonl.gz" ] || { echo "missing data/benchmarks/$b.jsonl.gz (see scripts/prepare_benchmarks.py)"; exit 1; }
done

MODEL=$STUDENT_MODEL start_server "$PORT" --lora "$ARM=$ADAPTER"
trap stop_server EXIT

RC=0
r=0
for seed in $SEEDS; do
  r=$((r+1)); [ "$r" -gt "$RUNS" ] && break
  run=$([ "$RUNS" -gt 1 ] && echo "run$r" || echo "greedy")
  for spec in "base=student" "$ARM=$ARM"; do
    arm=${spec%%=*}; served=${spec#*=}
    for b in $BENCHMARKS; do
      d="$OUT/$run/$arm/$b"
      mkdir -p "$d"
      [ -f "$d/.done" ] && { echo "skip $run/$arm/$b (done)"; continue; }
      echo "=== $(date -u +%T) $run $arm on $b (served=$served, T=$TEMPERATURE, seed=$seed)"
      $PY_TRAIN scripts/eval_benchmarks.py --benchmarks "data/benchmarks/$b.jsonl.gz" \
          --server-url "http://127.0.0.1:$PORT" --served-model "$served" --arm "$arm" \
          --run "$run" --temperature "$TEMPERATURE" --seed "$seed" \
          --out "$d" --concurrency "${CONCURRENCY:-48}" > "$d.stdout" 2>&1 \
        || { rc=$?; echo "  !! $run/$arm/$b incomplete (rc=$rc); last lines:"; tail -15 "$d.stdout"; RC=3; }
    done
  done
done
$PY_BASE scripts/forgetting_report.py --runs "$OUT" --out "$OUT/report"
echo "=== done $(date -u +%FT%TZ) rc=$RC -> $OUT/report/REPORT.md"
exit $RC
