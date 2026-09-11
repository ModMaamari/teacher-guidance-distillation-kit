#!/usr/bin/env bash
# Forgetting check on MMLU / GSM8K / HellaSwag for the base and every trained arm.
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$HERE/../_common.sh"
ARMS="${ARMS:-uniform}"

if [ "${1:-}" = "report" ]; then
  banner "exp09: forgetting report"
  for arm in $ARMS; do
    run_local $PY scripts/forgetting_report.py --runs runs/benchmarks \
        --out "runs/forgetting/$arm" --base-arm base --trained-arm "$arm"
  done
  exit 0
fi

banner "exp09: benchmarks for base + $ARMS"
for arm in $ARMS; do
  a="runs/train/$arm/adapter"
  need_file "$a" "train it first, or set ARMS=..." || continue
  STUDENT_MODEL="$STUDENT_MODEL" submit "$KIT/slurm/eval_forgetting.sbatch" "$a" "$arm"
done
echo
echo "the base arm must be measured the same way or the deltas mean nothing:"
echo "  sbatch ... $KIT/slurm/eval_forgetting.sbatch '' base"
echo
echo "also worth running per arm:  sbatch ... $KIT/slurm/eval_stability.sbatch <adapter> <arm>"
