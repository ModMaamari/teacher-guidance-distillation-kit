#!/usr/bin/env bash
# Train + evaluate the uniform split under several seeds. `bash run.sh judge` to judge.
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$HERE/../_common.sh"
SEEDS="${SEEDS:-13 17 23}"
TESTS="${TESTS:-heldout_hotpotqa heldout_2wikimultihopqa heldout_musique heldout_strategyqa}"

if [ "${1:-}" = "judge" ]; then
  banner "exp02: judge every seed"
  submit_cpu "$KIT/slurm/judge.sbatch" "$JUDGE"; exit 0
fi

banner "exp02: seeds = $SEEDS"
need_file data/splits/uniform/train.jsonl "run 'make data' first" || exit 1
for s in $SEEDS; do
  if [ -e "runs/train/seed$s/adapter/.done" ]; then
    echo "  seed $s: trained already"
  else
    submit "$KIT/slurm/train.sbatch" data/splits/uniform "runs/train/seed$s" \
        --model "$STUDENT_MODEL" --seed "$s" --health-every 200
  fi
done
echo
banner "evaluate (submit after training finishes, or use --dependency)"
ARMS=""; for s in $SEEDS; do ARMS="$ARMS seed$s=seed$s:runs/train/seed$s/adapter"; done
submit "$KIT/slurm/eval_student.sbatch" "$ARMS" "$TESTS" --model "$STUDENT_MODEL"
