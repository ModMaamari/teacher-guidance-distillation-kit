#!/usr/bin/env bash
# Verify the two control episode sets exist before anything expensive starts.
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$HERE/../_common.sh"
banner "exp01 inputs"
ok=0
for arm in selfdist teachdist; do
  f="data/episodes_$arm/episodes.jsonl.gz"
  if [ -e "$f" ]; then
    n=$($PY - "$f" <<'PY'
import gzip,sys
print(sum(1 for _ in gzip.open(sys.argv[1],'rt')))
PY
)
    echo "  ok      $f  ($n episodes)"
  else
    echo "  MISSING $f"
    echo "          generate in teacher-guidence/ with run_teacher_only_traces.py (skip_teacher=True)"
    echo "          agent = the student for selfdist, the teacher for teachdist"
    ok=1
  fi
done
f="data/episodes/episodes.jsonl.gz"
[ -e "$f" ] && echo "  ok      $f  (guided, shipped)" || { echo "  MISSING $f"; ok=1; }
echo
[ $ok = 0 ] && echo "all inputs present -> run 01_build_matched_splits.sh" \
            || echo "generate the missing sets first (see README.md)"
exit $ok
