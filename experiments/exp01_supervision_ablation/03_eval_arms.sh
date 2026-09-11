#!/usr/bin/env bash
# Evaluate the three trained arms plus the untrained base on the four held-out sets.
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$HERE/../_common.sh"
TESTS="${TESTS:-heldout_hotpotqa heldout_2wikimultihopqa heldout_musique heldout_strategyqa}"
banner "exp01: evaluate"
ARMS=""
for arm in selfdist teachdist guided; do
  a="runs/train/sup_$arm/adapter"
  if [ -e "$a/.done" ] || [ "$DRY_RUN" = "1" ]; then ARMS="$ARMS sup_$arm=sup_$arm:$a"
  else echo "  !! $a not finished; skipping"; fi
done
[ -z "$ARMS" ] && { echo "nothing to evaluate"; exit 1; }
echo "  arms:$ARMS"
submit "$KIT/slurm/eval_student.sbatch" "$ARMS" "$TESTS" --model "$STUDENT_MODEL"
echo "  (base arm, for reference -- skip if runs/eval/base already exists)"
submit "$KIT/slurm/eval_student.sbatch" "base=student" "$TESTS" --model "$STUDENT_MODEL"
