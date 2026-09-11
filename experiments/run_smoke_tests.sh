#!/usr/bin/env bash
# Smoke-test every experiment without submitting a job, touching a GPU, or calling a model.
#
#   bash experiments/run_smoke_tests.sh            # offline: syntax, dry-runs, fixtures
#   ONLINE=1 bash experiments/run_smoke_tests.sh   # also probe students and teachers live
#
# Exits non-zero if anything fails. Run this after changing any experiment script.
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$HERE/_common.sh"
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
PASS=0; FAIL=0
ok()   { printf "  \033[32mok\033[0m   %s\n" "$1"; PASS=$((PASS+1)); }
bad()  { printf "  \033[31mFAIL\033[0m %s\n" "$1"; [ -n "${2:-}" ] && echo "$2" | head -4 | sed 's/^/         /'; FAIL=$((FAIL+1)); }
check(){ if out=$("${@:2}" 2>&1); then ok "$1"; else bad "$1" "$out"; fi; }

banner "1. shell syntax"
for f in "$HERE"/_common.sh "$HERE"/exp*/*.sh; do
  if bash -n "$f" 2>/dev/null; then PASS=$((PASS+1)); else bad "syntax $(basename "$(dirname "$f")")/$(basename "$f")"; fi
done
[ $FAIL = 0 ] && ok "$(ls "$HERE"/exp*/*.sh | wc -l) scripts + _common.sh parse"

banner "2. python helpers expose a working CLI"
for f in "$HERE"/exp*/*.py; do
  rel="$(basename "$(dirname "$f")")/$(basename "$f")"
  if timeout 120 "$PY" "$f" --help >/dev/null 2>&1; then ok "$rel"; else bad "$rel"; fi
done

banner "3. every stage dry-runs (submits nothing)"
while read -r f st; do
  rel="$(basename "$(dirname "$f")")/$(basename "$f")${st:+ $st}"
  out=$(cd "$KIT" && DRY_RUN=1 PARTITION=_smoke_ ARMS=uniform EXTERNAL_DS=_x_ bash "$f" $st 2>&1)
  if echo "$out" | grep -qiE "unbound variable|command not found|syntax error"; then bad "$rel" "$out"
  else ok "$rel"; fi
done <<'STAGES'
exp01_supervision_ablation/00_check_inputs.sh 
exp01_supervision_ablation/01_build_matched_splits.sh 
exp01_supervision_ablation/02_train_arms.sh 
exp01_supervision_ablation/03_eval_arms.sh 
exp01_supervision_ablation/04_judge_and_compare.sh 
exp02_seed_variance/run.sh 
exp02_seed_variance/run.sh judge
exp04_data_scaling/run.sh splits
exp04_data_scaling/run.sh train
exp04_data_scaling/run.sh eval
exp04_data_scaling/run.sh judge
exp05_student_family/run.sh train
exp05_student_family/run.sh eval
exp05_student_family/run.sh judge
exp06_teacher_strength/run.sh splits
exp06_teacher_strength/run.sh train
exp06_teacher_strength/run.sh eval
exp06_teacher_strength/run.sh judge
exp07_external_testset/run.sh 
exp08_step_budget/run.sh 
exp08_step_budget/run.sh judge
exp09_forgetting/run.sh 
exp09_forgetting/run.sh report
exp11_training_knobs/run.sh rank
exp11_training_knobs/run.sh lr
exp11_training_knobs/run.sh epochs
exp11_training_knobs/run.sh eval
exp11_training_knobs/run.sh judge
STAGES

banner "4. analysis helpers on fixtures"
if fx=$("$PY" "$HERE/_fixtures.py" "$TMP" 2>&1); then
  ok "fixtures built"
else
  bad "fixture generation" "$fx"
  echo "  everything below depends on the fixtures; fix that first."
  echo
  echo "================  $PASS passed, $FAIL failed  ================"
  exit 1
fi
check "exp01 match_sizes"        "$PY" "$HERE/exp01_supervision_ablation/match_sizes.py" --root a="$TMP/split_a" --root b="$TMP/split_b"
check "exp02 summarize_seeds"    "$PY" "$HERE/exp02_seed_variance/summarize_seeds.py" --results "$TMP/results_seeds.json"
check "exp03 sample_for_human"   "$PY" "$HERE/exp03_judge_validity/01_sample_for_human.py" --verdicts "$TMP/verdicts.jsonl" --n 40 --out "$TMP/human.csv"
check "exp03 agreement"          "$PY" "$HERE/exp03_judge_validity/03_agreement.py" --primary "$TMP/verdicts.jsonl" --swap "$TMP/verdicts_swap.jsonl"
check "exp07 prepare_external"   "$PY" "$HERE/exp07_external_testset/prepare_external.py" --input "$TMP/ext.jsonl" --name smoke --out-root "$TMP/q"
check "exp08 summarize_budget"   "$PY" "$HERE/exp08_step_budget/summarize_budget.py" --results "$TMP/results_budget.json"
check "exp10 analyze_stopping"   "$PY" "$HERE/exp10_stopping_behavior/analyze_stopping.py" --runs "$TMP/eval" --judge "$TMP/none.jsonl"
check "exp12 correct_pvalues"    "$PY" "$HERE/exp12_multiple_comparisons/correct_pvalues.py" --results "$TMP/results_paired.json"

banner "5. contamination check against the shipped split"
if [ -e "$KIT/data/splits/uniform/train.jsonl" ]; then
  check "exp07 contamination_check" "$PY" "$HERE/exp07_external_testset/contamination_check.py" --n 10
else
  echo "  skip  exp07 contamination_check (run 'make data' first)"
fi

if [ "${ONLINE:-0}" = "1" ]; then
  banner "6. live probes (network)"
  check "exp05 probe_students" "$PY_TRAIN" "$HERE/exp05_student_family/probe_students.py"
  if [ -f "$KIT/.env" ]; then
    check "exp06 probe_teachers" bash "$HERE/exp06_teacher_strength/00_probe_teachers.sh"
  else
    echo "  skip  exp06 probe_teachers (no .env)"
  fi
else
  banner "6. live probes"
  echo "  skip  (set ONLINE=1 to probe students and teacher endpoints)"
fi

echo
echo "================  $PASS passed, $FAIL failed  ================"
exit $(( FAIL > 0 ))
