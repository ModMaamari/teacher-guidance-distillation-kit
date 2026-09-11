#!/usr/bin/env bash
# Train / evaluate every candidate student on the same split. Stages: train | eval | judge
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$HERE/../_common.sh"
SPLIT="${SIZE_SPLIT:-data/splits/uniform}"
TESTS="${TESTS:-heldout_hotpotqa heldout_2wikimultihopqa heldout_musique heldout_strategyqa}"
LIST="${STUDENT_LIST:-$HERE/students.txt}"
STAGE="${1:-train}"

models() { grep -vE '^\s*(#|$)' "$LIST"; }
slug()   { echo "$1" | tr '/' '_' | tr '[:upper:]' '[:lower:]'; }

case "$STAGE" in
  train)
    banner "exp05: train each student on $SPLIT"
    need_file "$SPLIT/train.jsonl" "run exp04 or 'make data'" || exit 1
    while read -r m; do
      s=$(slug "$m")
      submit "$KIT/slurm/train.sbatch" "$SPLIT" "runs/train/stu_$s" \
          --model "$m" --health-every 200
    done < <(models)
    ;;
  eval)
    banner "exp05: evaluate each student (one vLLM server per model)"
    while read -r m; do
      s=$(slug "$m")
      a="runs/train/stu_$s/adapter"
      if [ ! -e "$a/.done" ] && [ "$DRY_RUN" != "1" ]; then
        echo "  !! $a unfinished; skipping $m"; continue
      fi
      # base and trained for this model share a server, so lift is measured like-for-like
      submit "$KIT/slurm/eval_student.sbatch" \
          "base_$s=base_$s stu_$s=stu_$s:$a" "$TESTS" --model "$m"
    done < <(models)
    ;;
  judge)
    banner "exp05: judge + collect"
    submit_cpu "$KIT/slurm/judge.sbatch" "$JUDGE"
    echo "  report absolute accuracy AND lift over each model's own base arm"
    ;;
  *) echo "usage: bash run.sh [train|eval|judge]"; exit 2 ;;
esac
