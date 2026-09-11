#!/usr/bin/env bash
# One student per teacher, everything else held fixed. Stages: splits | train | eval | judge
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$HERE/../_common.sh"
ARMS="${TEACHER_ARMS:-tstrong tweak ref}"
TESTS="${TESTS:-heldout_hotpotqa heldout_2wikimultihopqa heldout_musique heldout_strategyqa}"
STAGE="${1:-splits}"

ep_dir()   { [ "$1" = ref ] && echo data/episodes || echo "data/episodes_$1"; }
root_dir() { [ "$1" = ref ] && echo data/splits   || echo "data/splits_$1"; }

case "$STAGE" in
  splits)
    banner "exp06: build a split per teacher"
    for arm in $ARMS; do
      epdir=$(ep_dir "$arm"); root=$(root_dir "$arm")
      need_file "$epdir/episodes.jsonl.gz" "collect it in teacher-guidence (see README)" || continue
      [ -e "$epdir/index.jsonl" ] || \
        run_local $PY scripts/consolidate_episodes.py --runs "$epdir" --out "$epdir" --gzip
      [ -e "$root/stats.json" ] && echo "    have $root/stats.json" || \
        run_local $PY scripts/build_splits.py --episodes "$epdir/episodes.jsonl.gz" --out "$root"
    done
    echo
    echo "match supervision across teachers before training -- yields differ by teacher:"
    echo "  $PY ../exp01_supervision_ablation/match_sizes.py \\"
    for arm in $ARMS; do echo "      --root $arm=$(root_dir "$arm") \\"; done
    echo "  then scripts/make_size_splits.py --split <root>/uniform --out-root <root> --sizes <n>"
    ;;
  train)
    banner "exp06: train one student per teacher"
    for arm in $ARMS; do
      root=$(root_dir "$arm")
      split=$(ls -d "$root"/uniform_ep* 2>/dev/null | head -1); : "${split:=$root/uniform}"
      [ -e "$split/train.jsonl" ] || { echo "  skip $arm (no $split/train.jsonl)"; continue; }
      echo "  $arm <- $split"
      submit "$KIT/slurm/train.sbatch" "$split" "runs/train/teach_$arm" \
          --model "$STUDENT_MODEL" --health-every 200
    done
    ;;
  eval)
    banner "exp06: evaluate"
    A=""
    for arm in $ARMS; do
      a="runs/train/teach_$arm/adapter"
      if [ -e "$a/.done" ] || [ "$DRY_RUN" = "1" ]; then A="$A teach_$arm=teach_$arm:$a"
      else echo "  !! $a unfinished; skipping"; fi
    done
    [ -z "$A" ] && { echo "nothing to evaluate"; exit 1; }
    submit "$KIT/slurm/eval_student.sbatch" "$A" "$TESTS" --model "$STUDENT_MODEL"
    ;;
  judge)
    banner "exp06: judge + collect"
    submit_cpu "$KIT/slurm/judge.sbatch" "$JUDGE"
    echo "  also report guidance yield per teacher (correct/collected) from each stats.json:"
    for arm in $ARMS; do echo "    jq '[.per_dataset[]|.correct]|add' $(root_dir "$arm")/stats.json"; done
    ;;
  *) echo "usage: bash run.sh [splits|train|eval|judge]"; exit 2 ;;
esac
