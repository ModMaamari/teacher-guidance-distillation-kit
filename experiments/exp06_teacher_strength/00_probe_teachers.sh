#!/usr/bin/env bash
# Confirm each candidate teacher answers before committing to a collection run.
# Reads OAI_TEACHER_BASE_URL / OAI_TEACHER_API_KEY from .env, like the kit does.
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$HERE/../_common.sh"
[ -f "$KIT/.env" ] && { set -a; . "$KIT/.env"; set +a; }
BASE="${OAI_TEACHER_BASE_URL:-${OAI_BASE_URL:-}}"
KEY="${OAI_TEACHER_API_KEY:-${OAI_API_KEY:-}}"
MODELS="${MODELS:-mistralai/Mistral-Medium-3.5-128B RedHatAI/Mistral-Small-3.2-24B-Instruct-2506-FP8 deepseek-ai/DeepSeek-V4-Flash-0731}"

banner "exp06: probe teachers at ${BASE:-<unset>}"
[ -n "$BASE" ] || { echo "!! set OAI_TEACHER_BASE_URL in $KIT/.env"; exit 1; }
$PY "$HERE/probe_teachers.py" $MODELS
echo
echo "reasoning=yes means give that teacher a large --teacher-max-tokens,"
echo "or the critique budget is spent on chain-of-thought and content comes back empty."
