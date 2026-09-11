#!/usr/bin/env bash
# Forgetting check on MMLU / GSM8K / HellaSwag.
#
# slurm/eval_forgetting.sbatch serves ONE vLLM instance and answers every benchmark twice,
# once through the base weights and once through the adapter, so the base arm is measured
# automatically in the same job. Do not try to submit a base-only run: the wrapper requires
# a real adapter directory and exits if it is missing.
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$HERE/../_common.sh"
ARMS="${ARMS:-uniform}"
export STUDENT_MODEL

if [ "${1:-}" = "report" ]; then
  banner "exp09: forgetting report"
  for arm in $ARMS; do
    run_local $PY scripts/forgetting_report.py --runs runs/benchmarks \
        --out "runs/forgetting/$arm" --base-arm base --trained-arm "$arm"
  done
  exit 0
fi

banner "exp09: benchmarks for $ARMS (each job also measures the base arm)"
for arm in $ARMS; do
  a="runs/train/$arm/adapter"
  if [ ! -e "$a/adapter_config.json" ] && [ "$DRY_RUN" != "1" ]; then
    echo "  !! no adapter at $a -- train it first, or set ARMS=..."; continue
  fi
  submit "$KIT/slurm/eval_forgetting.sbatch" "$a" "$arm"
done
echo
echo "RUNS=5 repeats each (arm, benchmark) with distinct seeds so the spread can be tested."
echo "Also worth running per arm:  sbatch ... $KIT/slurm/eval_stability.sbatch <adapter> <arm>"
echo "Forgetting asks whether the model still knows things; stability asks whether it can"
echo "still be sampled at all. They catch different failures."
