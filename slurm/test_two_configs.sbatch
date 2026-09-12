#!/usr/bin/env bash
# Two candidate fixes for the step-0 truncation, one server, back to back:
#   A  bigger budget, reasoning left on   (8000 tokens)
#   B  thinking switched off              (3000 tokens)
# B was never fairly tested: the run that appeared to show it failing was measuring a
# broken client. The isolated 2x2 had it producing compact valid JSON.
#SBATCH --job-name=tgd_two_cfg
#SBATCH --cpus-per-task=16
#SBATCH --mem=96G
#SBATCH --time=02:00:00
#SBATCH --output=runs/slurm/two_cfg_%j.log
set -uo pipefail
cd "${SLURM_SUBMIT_DIR:-$PWD}"
source slurm/common.sh
PORT=8321
export VLLM_ENDPOINT="http://127.0.0.1:$PORT"
echo "== $(date -u +%FT%TZ) node=$(hostname) job=${SLURM_JOB_ID:-local}"

MODEL=ibm-granite/granite-4.2-3b start_server "$PORT" || { echo "!! serve failed"; exit 1; }
trap stop_server EXIT

run_cfg() {   # run_cfg <name> <max_tokens> <thinking:on|off>
  local name=$1 tok=$2 think=$3 out="runs/collect_cfg_$1"
  echo; echo "######## config $name: max_tokens=$tok thinking=$think"
  rm -rf "$out"
  if [ "$think" = off ]; then export VLLM_CHAT_TEMPLATE_KWARGS='{"enable_thinking": false}'
  else unset VLLM_CHAT_TEMPLATE_KWARGS; fi
  $PY_TRAIN scripts/collect_episodes.py --datasets hotpotqa 2wikimultihopqa \
      --num-samples 3 --student vllm/student --teacher custom/z-ai/glm-5.3-flash \
      --shards 2 --out "$out" --tag "cfg$name" --student-max-tokens "$tok"
  echo "-- config $name result:"
  $PY_BASE scripts/check_student_actions.py --runs "$out" || true
}

run_cfg A 8000 on
run_cfg B 3000 off
echo "== done $(date -u +%FT%TZ)"
