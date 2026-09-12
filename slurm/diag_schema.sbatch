#!/usr/bin/env bash
#SBATCH --job-name=tgd_diag_schema
#SBATCH --cpus-per-task=8
#SBATCH --mem=64G
#SBATCH --time=00:50:00
#SBATCH --output=runs/slurm/diag_schema_%j.log
set -uo pipefail
cd "${SLURM_SUBMIT_DIR:-$PWD}"
source slurm/common.sh
PORT="${PORT:-8314}"
for M in "${MODELS:-ibm-granite/granite-4.2-3b ibm-granite/granite-4.1-3b}"; do :; done
echo "== $(date -u +%FT%TZ) node=$(hostname)"
for M in ${MODELS:-ibm-granite/granite-4.2-3b ibm-granite/granite-4.1-3b}; do
  echo; echo "######## $M"
  MODEL=$M start_server "$PORT" || { echo "!! failed to serve $M"; continue; }
  $PY_BASE scripts/diag_student_schema.py --server-url "http://127.0.0.1:$PORT"
  stop_server; sleep 20
  PORT=$((PORT+1))
done
echo "== done $(date -u +%FT%TZ)"
