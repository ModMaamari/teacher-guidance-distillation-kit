#!/usr/bin/env bash
# Evaluate fixed checkpoints at several step budgets. No retraining.
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$HERE/../_common.sh"
BUDGETS="${BUDGETS:-1 3 5 8}"
TESTS="${TESTS:-heldout_hotpotqa heldout_2wikimultihopqa heldout_musique heldout_strategyqa}"
ADAPTER="${ADAPTER:-runs/train/uniform/adapter}"

if [ "${1:-}" = "judge" ]; then
  banner "exp08: judge every budget"; submit_cpu "$KIT/slurm/judge.sbatch" "$JUDGE"; exit 0
fi

banner "exp08: budgets = $BUDGETS"
for b in $BUDGETS; do
  echo "  budget $b"
  submit "$KIT/slurm/eval_student.sbatch" \
      "base_b$b=student trained_b$b=trained_b$b:$ADAPTER" "$TESTS" \
      --model "$STUDENT_MODEL" --budget "$b"
  submit_cpu "$KIT/slurm/eval_teacher.sbatch" "teacher_b$b" "$TEACHER" "$TESTS" --budget "$b"
done
echo
echo "arms are named <arm>_b<budget> so collect_results.py keeps them apart"
