#!/usr/bin/env bash
# Cheap pre-flight: tokenizer + chat template for every candidate student. No GPU, no weights.
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$HERE/../_common.sh"
banner "exp05: probe candidate students"
$PY_TRAIN "$HERE/probe_students.py" "$@"
