#!/usr/bin/env bash
# Hyper-parameter sensitivity. Stages: rank | lr | epochs | eval | judge
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$HERE/../_common.sh"
SPLIT="${SPLIT:-data/splits/uniform}"
TESTS="${TESTS:-heldout_hotpotqa heldout_2wikimultihopqa heldout_musique heldout_strategyqa}"
SEED="${SEED:-13}"
STAGE="${1:-rank}"

train_one() {  # train_one <tag> <extra args...>
  local tag="$1"; shift
  submit "$KIT/slurm/train.sbatch" "$SPLIT" "runs/train/knob_$tag" \
      --model "$STUDENT_MODEL" --seed "$SEED" --health-every 200 "$@"
}

case "$STAGE" in
  rank)
    banner "exp11: LoRA rank sweep"
    for r in 8 16 32 64; do train_one "r$r" --lora-r "$r" --lora-alpha "$((r * 2))"; done ;;
  lr)
    banner "exp11: learning-rate sweep"
    for lr in 1e-4 2e-4 5e-4; do train_one "lr$lr" --lr "$lr"; done ;;
  epochs)
    banner "exp11: epoch sweep"
    for e in 1 2 3; do train_one "ep$e" --epochs "$e"; done ;;
  eval)
    banner "exp11: evaluate every knob variant"
    A=""
    for d in runs/train/knob_*/adapter; do
      [ -e "$d/.done" ] || { [ "$DRY_RUN" = "1" ] || continue; }
      t=$(basename "$(dirname "$d")"); A="$A $t=$t:$d"
    done
    [ -z "$A" ] && { echo "  nothing trained yet"; exit 1; }
    submit "$KIT/slurm/eval_student.sbatch" "$A" "$TESTS" --model "$STUDENT_MODEL" ;;
  judge)
    banner "exp11: judge + collect"
    submit_cpu "$KIT/slurm/judge.sbatch" "$JUDGE" ;;
  *) echo "usage: bash run.sh [rank|lr|epochs|eval|judge]"; exit 2 ;;
esac
