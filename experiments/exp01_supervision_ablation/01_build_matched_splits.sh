#!/usr/bin/env bash
# Consolidate each arm's episodes, build a split, then cut all three to the SAME number of
# USABLE training episodes, so supervision source is the only variable.
#
# Layout per arm:  data/splits_<arm>/{stats.json,uniform/train.jsonl,uniform_ep<N>/}
# The shipped guided data already lives in data/splits, so that arm reuses it.
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$HERE/../_common.sh"
ARMS="selfdist teachdist guided"

ep_dir()   { [ "$1" = guided ] && echo data/episodes      || echo "data/episodes_$1"; }
root_dir() { [ "$1" = guided ] && echo data/splits        || echo "data/splits_$1"; }

banner "1/3  build a full split per arm"
for arm in $ARMS; do
  epdir=$(ep_dir "$arm"); root=$(root_dir "$arm")
  need_file "$epdir/episodes.jsonl.gz" "run 00_check_inputs.sh" || exit 1
  [ -e "$epdir/index.jsonl" ] || \
    run_local $PY scripts/consolidate_episodes.py --runs "$epdir" --out "$epdir" --gzip
  if [ -e "$root/stats.json" ]; then
    echo "    have $root/stats.json"
  else
    run_local $PY scripts/build_splits.py --episodes "$epdir/episodes.jsonl.gz" --out "$root"
  fi
done

banner "2/3  matched sizes (equal USABLE episodes, not equal collected)"
ROOTS=(); for arm in $ARMS; do ROOTS+=(--root "$arm=$(root_dir "$arm")"); done
if [ "$DRY_RUN" = "1" ]; then
  echo "    [dry-run] $PY $HERE/match_sizes.py ${ROOTS[*]}"; PLAN=""
else
  PLAN=$($PY "$HERE/match_sizes.py" "${ROOTS[@]}") || exit 1
fi

banner "3/3  cut each arm (own --out-root: the script always names the dir uniform_ep<N>)"
printf '%s\n' "$PLAN" | while read -r arm n; do
  [ -z "${arm:-}" ] && continue
  epdir=$(ep_dir "$arm"); root=$(root_dir "$arm")
  run_local $PY scripts/make_size_splits.py \
      --index "$epdir/index.jsonl" --split "$root/uniform" \
      --out-root "$root" --sizes "$n"
  echo "    -> $root/uniform_ep$n"
done
echo
echo "check the arms really matched:"
echo "  for a in $ARMS; do r=data/splits_\$a; [ \$a = guided ] && r=data/splits; \\"
echo "    jq -r --arg a \$a '\"\\(\$a): \\(.target) collected -> \\(.episodes_with_examples) usable -> \\(.train_examples) examples\"' \$r/uniform_ep*/manifest.json; done"
