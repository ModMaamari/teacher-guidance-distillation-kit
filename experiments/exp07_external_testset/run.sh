#!/usr/bin/env bash
# Evaluate every arm on an external dataset you added under data/questions/<name>/.
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$HERE/../_common.sh"
DS="${EXTERNAL_DS:-}"
[ -n "$DS" ] || { echo "set EXTERNAL_DS=<name> (data/questions/<name>/ must exist)"; exit 2; }
need_file "data/questions/$DS/${DS}_questions.jsonl" "see docs/DATA.md section 4" || exit 1
need_file "data/questions/$DS/${DS}_corpus.jsonl.gz" || exit 1
banner "exp07: evaluate on external set '$DS'"
mkdir -p data/splits/test
cp -n "data/questions/$DS/${DS}_questions.jsonl" "data/splits/test/full_${DS}_questions.jsonl" 2>/dev/null || true
ADAPTER="${ADAPTER:-runs/train/pipetest/adapter}"
submit "$KIT/slurm/eval_student.sbatch" "base=base trained=trained:$ADAPTER" "full_$DS" --model "$STUDENT_MODEL"
submit_cpu "$KIT/slurm/eval_teacher.sbatch" teacher "$TEACHER" "full_$DS"
echo "  then: bash ../exp01_supervision_ablation/04_judge_and_compare.sh"
