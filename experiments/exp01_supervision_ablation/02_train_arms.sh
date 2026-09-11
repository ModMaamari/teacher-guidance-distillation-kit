#!/usr/bin/env bash
# Train one LoRA student per supervision source. Same hyper-parameters, same seed,
# same dev set -- only the training file differs.
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$HERE/../_common.sh"
SEED="${SEED:-13}"
banner "exp01: train 3 arms (student=$STUDENT_MODEL seed=$SEED)"
for arm in selfdist teachdist guided; do
  root=data/splits_$arm; [ "$arm" = guided ] && root=data/splits
  split=$(ls -d $root/uniform_ep* 2>/dev/null | head -1)
  if [ -z "$split" ]; then
    echo "  !! no $root/uniform_ep* -- run 01_build_matched_splits.sh first"; continue
  fi
  echo "  $arm  <- $split"
  submit "$KIT/slurm/train.sbatch" "$split" "runs/train/sup_$arm" \
      --model "$STUDENT_MODEL" --seed "$SEED" --health-every 200
done
echo
echo "watch: squeue -u \$USER   |   tail -f runs/train/sup_*/train.log"
