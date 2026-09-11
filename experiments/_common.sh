#!/usr/bin/env bash
# Shared settings for every experiment. Sourced, never run directly.
#
# Required in your environment (or edit here once):
#   PARTITION      slurm partition with a GPU          e.g. PARTITION=gpu
# Optional:
#   ACCOUNT        slurm account                       (adds -A)
#   GRES           gres string                         (default gpu:1)
#   STUDENT_MODEL  HF id of the student                (default granite-4.2-3b)
#   TEACHER        provider-prefixed teacher id
#   JUDGE          provider-prefixed judge id (chain allowed)
#   DRY_RUN=1      print what would be submitted, submit nothing
set -uo pipefail

KIT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export KIT
cd "$KIT" || exit 1

PARTITION="${PARTITION:-}"
ACCOUNT="${ACCOUNT:-}"
GRES="${GRES:-gpu:1}"
STUDENT_MODEL="${STUDENT_MODEL:-ibm-granite/granite-4.2-3b}"
TEACHER="${TEACHER:-oai-teacher/deepseek-ai/DeepSeek-V4-Flash-0731}"
JUDGE="${JUDGE:-oai-judge/moonshotai/Kimi-K2.6}"
DRY_RUN="${DRY_RUN:-0}"
PY="${PY:-$KIT/.venv/bin/python}"
PY_TRAIN="${PY_TRAIN:-$KIT/.venv_train/bin/python}"
[ -x "$PY_TRAIN" ] || PY_TRAIN="$PY"

# sbatch options assembled once
SB_OPTS=()
[ -n "$PARTITION" ] && SB_OPTS+=(-p "$PARTITION")
[ -n "$ACCOUNT" ]   && SB_OPTS+=(-A "$ACCOUNT")
[ -n "$GRES" ]      && SB_OPTS+=(--gres="$GRES")

# submit <sbatch-script> [args...]   -- honours DRY_RUN
submit() {
  if [ "$DRY_RUN" = "1" ]; then
    echo "    [dry-run] sbatch ${SB_OPTS[*]-} $*"
  else
    [ -n "$PARTITION" ] || { echo "!! set PARTITION (see experiments/README.md)" >&2; return 2; }
    sbatch ${SB_OPTS[@]+"${SB_OPTS[@]}"} "$@"
  fi
}

# submit_cpu <sbatch-script> [args...]  -- same, but never asks for a GPU
submit_cpu() {
  local opts=()
  [ -n "$PARTITION" ] && opts+=(-p "${CPU_PARTITION:-$PARTITION}")
  [ -n "$ACCOUNT" ]   && opts+=(-A "$ACCOUNT")
  if [ "$DRY_RUN" = "1" ]; then
    echo "    [dry-run] sbatch ${opts[*]-} $*"
  else
    [ -n "$PARTITION" ] || { echo "!! set PARTITION (see experiments/README.md)" >&2; return 2; }
    sbatch ${opts[@]+"${opts[@]}"} "$@"
  fi
}

# local <cmd...>  -- run a CPU-only kit script here, or print it under DRY_RUN
run_local() {
  if [ "$DRY_RUN" = "1" ]; then echo "    [dry-run] $*"; else "$@"; fi
}

banner() { echo; echo "=== $*"; }

need_file() {
  [ -e "$1" ] && return 0
  echo "!! missing: $1" >&2; [ $# -gt 1 ] && echo "   $2" >&2
  return 1
}
