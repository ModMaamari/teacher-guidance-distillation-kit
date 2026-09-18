#!/usr/bin/env bash
#SBATCH --job-name=tgd-worker
#SBATCH --cpus-per-task=16
#SBATCH --mem=128G
#SBATCH --signal=B:USR1@600
#SBATCH --output=runs/pool/logs/%x_%j.log
# One pool worker (experiments/pool/README.md). Partition, GPU, walltime and kind come from the
# command line; keeper.py submits these, and so can you, from the kit root:
#   sbatch -p <gpu-partition> --gres=gpu:1 -t 12:00:00 -J tgd-gpu --export=ALL,WORKER_WALL_H=12 experiments/pool/worker.sbatch
#   sbatch -p <cpu-partition> -c 8 --mem 32G -t 1-00:00:00 -J tgd-cpu \
#          --export=ALL,WORKER_KIND=cpu,WORKER_WALL_H=24,WORKER_THREADS=1 experiments/pool/worker.sbatch
# WORKER_WALL_H must match -t: the worker only starts what fits in the time left.
ROOT=${SLURM_SUBMIT_DIR:?submit from the kit root}
. "$ROOT/slurm/common.sh"
exec "$PY_BASE" -u experiments/pool/worker.py
