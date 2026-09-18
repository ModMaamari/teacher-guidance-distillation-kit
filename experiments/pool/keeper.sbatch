#!/usr/bin/env bash
#SBATCH --job-name=tgd-keeper
#SBATCH --cpus-per-task=1
#SBATCH --mem=1G
#SBATCH --time=2-00:00:00
#SBATCH --output=runs/pool/logs/%x_%j.log
# Keeps the pool staffed without anything running on a login node: every 10 minutes keeper.py
# submits the workers the remaining tasks need. Submit once, from the kit root, on a CPU partition:
#   sbatch -p <cpu-partition> experiments/pool/keeper.sbatch
# It queues its own successor (afterany), so the chain outlives the partition's time limit, and
# ends once every task is done or dead. Stop it: touch runs/pool/STOP; scancel -n tgd-keeper
ROOT=${SLURM_SUBMIT_DIR:?submit from the kit root}
. "$ROOT/slurm/common.sh"
[ -e runs/pool/STOP ] && { echo "runs/pool/STOP present; exiting"; exit 0; }
"$PY_BASE" experiments/pool/keeper.py --finished && { echo "all tasks finished; chain ends"; exit 0; }
sbatch -p "$SLURM_JOB_PARTITION" --dependency=afterany:"$SLURM_JOB_ID" experiments/pool/keeper.sbatch
while [ ! -e runs/pool/STOP ]; do
  "$PY_BASE" experiments/pool/keeper.py || echo "$(date -u +%FT%TZ) keeper.py rc=$?"
  "$PY_BASE" experiments/pool/keeper.py --finished && { echo "all tasks finished"; break; }
  sleep 600
done
