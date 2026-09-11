#!/usr/bin/env bash
# Evaluate every arm on an external dataset you added under data/questions/<name>/.
#
# prepare_external.py writes the questions gzipped, but slurm/eval_student.sbatch reads
# data/splits/test/<test-set>_questions.jsonl uncompressed, so this stages a plain copy.
# The corpus stays gzipped: that path is passed through as-is.
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$HERE/../_common.sh"
DS="${EXTERNAL_DS:-}"
[ -n "$DS" ] || { echo "set EXTERNAL_DS=<name>  (build it with prepare_external.py)"; exit 2; }

Q_GZ="data/questions/$DS/${DS}_questions.jsonl.gz"
Q_PLAIN="data/questions/$DS/${DS}_questions.jsonl"
need_file "data/questions/$DS/${DS}_corpus.jsonl.gz" "run prepare_external.py first" || exit 1

banner "exp07: evaluate on external set '$DS'"
TEST="data/splits/test/full_${DS}_questions.jsonl"
if [ "$DRY_RUN" = "1" ]; then
  echo "    [dry-run] stage $DS questions -> $TEST"
else
  mkdir -p data/splits/test
  if [ -e "$Q_GZ" ]; then gzip -dc "$Q_GZ" > "$TEST"
  elif [ -e "$Q_PLAIN" ]; then cp "$Q_PLAIN" "$TEST"
  else echo "!! no $Q_GZ or $Q_PLAIN"; exit 1; fi
  echo "  staged $(wc -l < "$TEST") questions -> $TEST"
fi

ADAPTER="${ADAPTER:-runs/train/uniform/adapter}"
submit "$KIT/slurm/eval_student.sbatch" "base=student trained=trained:$ADAPTER" \
    "full_$DS" --model "$STUDENT_MODEL"
submit_cpu "$KIT/slurm/eval_teacher.sbatch" teacher "$TEACHER" "full_$DS"
echo
echo "then judge and compare:"
echo "  bash $HERE/../exp01_supervision_ablation/04_judge_and_compare.sh"
