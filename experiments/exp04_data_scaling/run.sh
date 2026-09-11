#!/usr/bin/env bash
# Training-set-size ablation. Stages: splits | train | eval | judge
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$HERE/../_common.sh"
SIZES="${SIZES:-500 1000 2000 4000 7252}"
TESTS="${TESTS:-heldout_hotpotqa heldout_2wikimultihopqa heldout_musique heldout_strategyqa}"
STAGE="${1:-splits}"

case "$STAGE" in
  splits)
    banner "exp04: build nested size splits ($SIZES)"
    need_file data/episodes/index.jsonl || exit 1
    need_file data/splits/uniform/train.jsonl "run 'make data' first" || exit 1
    run_local $PY scripts/make_size_splits.py --sizes $SIZES
    echo "  sizes above the 7,252 trainable pool are skipped by the script, with a message"
    ;;
  train)
    banner "exp04: train one student per size"
    for n in $SIZES; do
      d="data/splits/uniform_ep$n"
      [ -d "$d" ] || { echo "  skip $n (no $d)"; continue; }
      submit "$KIT/slurm/train.sbatch" "$d" "runs/train/ep$n" \
          --model "$STUDENT_MODEL" --health-every 200
    done
    ;;
  eval)
    banner "exp04: evaluate each size"
    ARMS=""
    for n in $SIZES; do
      [ -d "data/splits/uniform_ep$n" ] || continue
      ARMS="$ARMS ep$n=ep$n:runs/train/ep$n/adapter"
    done
    [ -z "$ARMS" ] && { echo "nothing to evaluate"; exit 1; }
    submit "$KIT/slurm/eval_student.sbatch" "$ARMS" "$TESTS" --model "$STUDENT_MODEL"
    ;;
  judge)
    banner "exp04: judge, collect, plot"
    submit_cpu "$KIT/slurm/judge.sbatch" "$JUDGE"
    echo "  after it lands:"
    echo "    $PY scripts/collect_results.py --runs runs/eval --judge runs/judge/verdicts.jsonl --out runs/results"
    echo "    $PY scripts/plot_size_curve.py --results runs/results/results.json --out runs/results"
    ;;
  *) echo "usage: bash run.sh [splits|train|eval|judge]"; exit 2 ;;
esac
