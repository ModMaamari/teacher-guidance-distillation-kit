#!/usr/bin/env bash
# Run one pool task by name. worker.py starts a snapshot copy of this file per task, from the
# kit root, with POOL_KIT set, so editing it never disturbs a running task:
#   bash experiments/pool/run_task.sh <task>          # also fine by hand, inside srun/sbatch
#
# Every task is idempotent: finished work is recognised on disk (adapter/.done, eval .done
# markers, verdicts already written) and skipped, and a task exits non-zero while anything it
# owns is still missing, so the worker's retry resumes it. Settings: experiments/pool/local.env
# (copy local.env.example). Task list and priorities: experiments/pool/tasks.tsv.
set -uo pipefail
TASK=${1:?task name}
KIT=${POOL_KIT:-$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)}
export SLURM_SUBMIT_DIR=$KIT            # the slurm/*.sbatch scripts locate the kit from it
ROOT=$KIT . "$KIT/slurm/common.sh"       # cd kit, caches, .env, PY_BASE/PY_TRAIN/PY_VLLM, start_server
[ -f experiments/pool/local.env ] || { echo "!! experiments/pool/local.env missing (see local.env.example)"; exit 2; }
set -a; . experiments/pool/local.env; set +a
: "${JUDGE:?}" "${TEACHER:?}" "${STUDENT_MODEL:?}"
HELDOUT="heldout_hotpotqa heldout_2wikimultihopqa heldout_musique heldout_strategyqa"
TOOLS="$PY_BASE experiments/pool/tools.py"
echo "== task $TASK  $(date -u +%FT%TZ)"

free_port() { $PY_BASE -c 'import socket; s = socket.socket(); s.bind(("127.0.0.1", 0)); print(s.getsockname()[1])'; }
# vLLM memory fraction that gives this server $1 GB of the GPU it shares with other tasks
gpu_frac() {
  local total; total=$(nvidia-smi --query-gpu=memory.total --format=csv,noheader,nounits | head -1)
  $PY_BASE -c "print(round(min(0.9, $1 * 1024 / $total), 3))"
}

train() {   # train <run-name> <split-dir> [train_sft.py args]
  local name=$1 split=$2; shift 2
  [ -f "runs/train/$name/adapter/.done" ] && { echo "have runs/train/$name"; return 0; }
  local dev=$split/dev.jsonl   # size cuts (make_size_splits.py) keep the full split's dev set
  [ -s "$dev" ] || dev=$($PY_BASE -c 'import json,sys; print(json.load(open(sys.argv[1]))["dev_file"])' "$split/manifest.json" 2>/dev/null)
  for f in "$split/train.jsonl" "$dev"; do [ -s "$f" ] || { echo "!! missing ${f:-dev set of $split}"; return 1; }; done
  $PY_TRAIN scripts/train_sft.py --model "$STUDENT_MODEL" --train-file "$split/train.jsonl" \
      --dev-file "$dev" --out "runs/train/$name" "$@" || return 1
  [ -f "runs/train/$name/adapter/.done" ]
}

all_done() {  # all_done "<arm ...>" "<test ...>": every runs/eval/<arm>/<test>/.done exists
  local a t rc=0
  for a in $1; do for t in $2; do
    [ -f "runs/eval/$a/$t/.done" ] || { echo "   missing runs/eval/$a/$t"; rc=1; }
  done; done
  return $rc
}

evals() {   # evals "<arm=served[:adapter]> ..." "<test ...>" [eval.py args]
  local specs=$1 tests=$2 arms="" s; shift 2
  for s in $specs; do arms="$arms ${s%%=*}"; done
  all_done "$arms" "$tests" >/dev/null && { echo "all evaluated:$arms"; return 0; }
  PORT=$(free_port) GPU_MEM=${EVAL_GPU_MEM:-$(gpu_frac 24)} MODEL=$STUDENT_MODEL \
    bash slurm/eval_student.sbatch "$specs" "$tests" --model "$STUDENT_MODEL" "$@"
  all_done "$arms" "$tests"
}

teacher_eval() {  # teacher_eval <arm> <budget>: the teacher alone is the agent (API)
  CONCURRENCY=${TEACHER_CONCURRENCY:-6} bash slurm/eval_teacher.sbatch "$1" "$TEACHER" "$HELDOUT" \
    --budget "$2" --student-max-tokens "${TEACHER_AGENT_MAX_TOKENS:-6000}"
  all_done "$1" "$HELDOUT"
}

judge() {   # judge <out-dir> "<episodes glob>" <judge chain> [judge.py args]
  local out=$1 glob=$2 chain=$3; shift 3
  $PY_BASE scripts/judge.py --judge "$chain" --episodes "$glob" --out "$out" \
      --concurrency "${JUDGE_CONCURRENCY:-8}" "$@"
  $TOOLS judged --episodes "$glob" --verdicts "$out/verdicts.jsonl"
}

results() {  # results <view-name> <results-dir> <arm=runs/eval-dir> ...: table + publish
  local name=$1 dest=$2; shift 2
  $TOOLS view --name "$name" "$@" || return 1
  $PY_BASE scripts/collect_results.py --runs "runs/views/$name" --judge "runs/views/$name/verdicts.jsonl" \
      --out "runs/results/$name" || return 1
  $TOOLS publish "runs/results/$name" "$dest"
}

split_of() {  # split_of <episodes-dir> <split-root>: build a training split from consolidated episodes
  [ -f "$2/stats.json" ] && [ -s "$2/uniform/train.jsonl" ] && { echo "have $2"; return 0; }
  $PY_BASE scripts/build_splits.py --episodes "$1/episodes.jsonl.gz" --out "$2"
}

case "$TASK" in
  # ---------- E00 / E13: research runs, re-judged with the paper's judge ----------
  import_research) $PY_BASE experiments/exp00_reference/import_runs.py --research-root "${RESEARCH_ROOT:?}" ;;
  judge_e00)       judge runs/judge/e00 'runs/e00/eval/*/*/episodes.jsonl' "$JUDGE" ;;
  judge_e13)       judge runs/judge/e13 'runs/e13/eval/*/*/episodes.jsonl' "$JUDGE" ;;
  results_e00)
    $PY_BASE scripts/collect_results.py --runs runs/e00/eval --judge runs/judge/e00/verdicts.jsonl \
        --out runs/results/e00 && $TOOLS publish runs/results/e00 results/E00_reference/gemma ;;
  results_e13)
    $PY_BASE scripts/collect_results.py --runs runs/e13/eval --judge runs/judge/e13/verdicts.jsonl \
        --out runs/results/e13 && $TOOLS publish runs/results/e13 results/E13_lodo_transfer/gemma ;;

  # ---------- E03: judge validity (swap judges on the same E00 answers; human sample) ----------
  judge_e00_kimi)  judge runs/judge_swap/kimi 'runs/e00/eval/*/*/episodes.jsonl' "$JUDGE_SWAP_A" ;;
  judge_e00_qwen)  judge runs/judge_swap/qwen 'runs/e00/eval/*/*/episodes.jsonl' "$JUDGE_SWAP_B" --max-tokens 4000 ;;
  e03_sample)
    mkdir -p runs/e03
    [ -s runs/e03/human_sample.csv ] && { echo "have runs/e03/human_sample.csv"; exit 0; }
    $PY_BASE experiments/exp03_judge_validity/01_sample_for_human.py --verdicts runs/judge/e00/verdicts.jsonl \
        --out runs/e03/human_sample.csv --n 200 --seed 7 ;;
  e03_agreement)
    mkdir -p results/E03_judge_validity
    cp -n runs/e03/human_sample.key.json runs/e03/human_labels.key.json   # 03_agreement pairs <csv> with <csv stem>.key.json
    $PY_BASE experiments/exp03_judge_validity/03_agreement.py --primary runs/judge/e00/verdicts.jsonl \
        --swap runs/judge_swap/kimi/verdicts.jsonl runs/judge_swap/qwen/verdicts.jsonl \
        --human runs/e03/human_labels.csv | tee runs/e03/agreement.txt &&
      $TOOLS publish runs/e03 results/E03_judge_validity/agreement --only agreement.txt human_labels.csv human_labels.key.json ;;

  # ---------- data preparation ----------
  prep_sizes)
    for n in 1000 2000 4000; do [ -s "data/splits/uniform_ep$n/train.jsonl" ] || need=1; done
    [ -z "${need:-}" ] && { echo "have size splits"; exit 0; }
    $PY_BASE scripts/make_size_splits.py --sizes 1000 2000 4000 ;;
  prep_self)       split_of data/episodes_self data/splits_self ;;
  prep_glm)        split_of data/episodes_glm data/splits_glm ;;
  prep_selfdist|prep_teachdist)
    arm=${TASK#prep_}
    [ -s "data/episodes_$arm/episodes.jsonl.gz" ] ||
      $PY_BASE scripts/consolidate_episodes.py --runs "runs/collect_$arm" --out "data/episodes_$arm" --gzip || exit 1
    split_of "data/episodes_$arm" "data/splits_$arm" ;;
  prep_e01_match)
    plan=$($PY_BASE experiments/exp01_supervision_ablation/match_sizes.py --root selfdist=data/splits_selfdist \
             --root teachdist=data/splits_teachdist --root guided=data/splits) || exit 1
    echo "$plan"
    while read -r arm n; do
      [ -z "${arm:-}" ] && continue
      ep=data/episodes_$arm; root=data/splits_$arm
      [ "$arm" = guided ] && { ep=data/episodes; root=data/splits; }
      [ -s "data/splits_sup_$arm/uniform_ep$n/train.jsonl" ] ||
        $PY_BASE scripts/make_size_splits.py --index "$ep/index.jsonl" --split "$root/uniform" \
            --out-root "data/splits_sup_$arm" --sizes "$n" || exit 1
      ln -sfn "uniform_ep$n" "data/splits_sup_$arm/matched"
    done <<< "$plan" ;;

  # ---------- E01: control collections (no teacher in the loop) ----------
  collect_selfdist)   # the student alone, served on this GPU
    MODEL=$STUDENT_MODEL OUT=runs/collect_selfdist TAG=selfdist SHARDS=${SELFDIST_SHARDS:-8} N=2000 \
      PORT=$(free_port) GPU_MEM=$(gpu_frac 30) TEACHER=vllm/student \
      bash slurm/collect_local.sbatch --no-teacher ;;
  collect_teachdist)  # the teacher alone, through its API
    $PY_TRAIN scripts/collect_episodes.py --no-teacher --student "$TEACHER" --num-samples "${TEACHDIST_N:-1000}" \
        --shards "${TEACHDIST_SHARDS:-4}" --out runs/collect_teachdist --tag teachdist \
        --student-max-tokens "${TEACHER_AGENT_MAX_TOKENS:-6000}" ;;

  # ---------- training (LoRA on the student) ----------
  train_seed*)      s=${TASK#train_seed}; train "seed$s" data/splits/uniform --seed "$s" ;;
  train_ep*)        n=${TASK#train_ep}; train "ep$n" "data/splits/uniform_ep$n" ;;
  train_selftaught) train selftaught data/splits_self/uniform ;;
  train_glmtaught)  train glmtaught data/splits_glm/uniform ;;
  train_sup_*)      arm=${TASK#train_sup_}; train "sup_$arm" "data/splits_sup_$arm/matched" ;;
  train_r*)         r=${TASK#train_r}; train "r$r" data/splits/uniform --lora-r "$r" --lora-alpha $((2 * r)) ;;

  # ---------- evaluation on the 747 held-out questions (vLLM on this GPU) ----------
  eval_base)        evals "base=student" "$HELDOUT" ;;
  eval_budget*)     b=${TASK#eval_budget}   # E08: base and seed-13 student at another step budget
                    evals "base_b$b=student seed13_b$b=seed13:runs/train/seed13/adapter" "$HELDOUT" --budget "$b" ;;
  eval_*)           arm=${TASK#eval_}; evals "$arm=$arm:runs/train/$arm/adapter" "$HELDOUT" ;;
  teacher_b*)       b=${TASK#teacher_b}; teacher_eval "teacher_b$b" "$b" ;;
  forget_seed13)    # E09: MMLU, GSM8K, HellaSwag, base and trained through one server
    PORT=$(free_port) GPU_MEM=$(gpu_frac 24) bash slurm/eval_forgetting.sbatch runs/train/seed13/adapter seed13 &&
      $TOOLS publish runs/forgetting/report results/E09_forgetting/kit ;;

  # ---------- judging (primary judge) ----------
  judge_budget*)    b=${TASK#judge_budget}; judge "runs/judge/budget$b" "runs/eval/*_b$b/*/episodes.jsonl" "$JUDGE" ;;
  judge_*)          arm=${TASK#judge_}; judge "runs/judge/$arm" "runs/eval/$arm/*/episodes.jsonl" "$JUDGE" ;;

  # ---------- per-experiment tables, published to results/ ----------
  results_E01)
    results E01 results/E01_supervision_ablation/kit base=runs/eval/base guided=runs/eval/sup_guided \
        selfdist=runs/eval/sup_selfdist teachdist=runs/eval/sup_teachdist ;;
  results_E02)
    results E02 results/E02_seed_variance/kit base=runs/eval/base seed13=runs/eval/seed13 \
        seed17=runs/eval/seed17 seed23=runs/eval/seed23 &&
      $PY_BASE experiments/exp02_seed_variance/summarize_seeds.py --results runs/results/E02/results.json \
        | tee runs/results/E02/seeds.txt && $TOOLS publish runs/results/E02 results/E02_seed_variance/kit --only seeds.txt ;;
  results_E04)
    results E04 results/E04_data_scaling/kit base=runs/eval/base ep1000=runs/eval/ep1000 ep2000=runs/eval/ep2000 \
        ep4000=runs/eval/ep4000 full=runs/eval/seed13 ;;
  results_E06)
    results E06 results/E06_teacher_strength/kit base=runs/eval/base deepseek_taught=runs/eval/seed13 \
        self_taught=runs/eval/selftaught glm_taught=runs/eval/glmtaught ;;
  results_E08)
    views=""
    for b in 1 5 8; do views="$views base_b$b=runs/eval/base_b$b trained_b$b=runs/eval/seed13_b$b teacher_b$b=runs/eval/teacher_b$b"; done
    # shellcheck disable=SC2086
    results E08 results/E08_step_budget/kit $views base_b3=runs/eval/base trained_b3=runs/eval/seed13 \
        teacher_b3=runs/eval/teacher_b3 &&
      $PY_BASE experiments/exp08_step_budget/summarize_budget.py --results runs/results/E08/results.json \
        | tee runs/results/E08/budget.txt && $TOOLS publish runs/results/E08 results/E08_step_budget/kit --only budget.txt ;;
  results_E11)
    results E11 results/E11_training_knobs/kit base=runs/eval/base r8=runs/eval/r8 r16=runs/eval/r16 \
        r32=runs/eval/seed13 r64=runs/eval/r64 ;;

  # ---------- CPU analyses ----------
  e07_contamination)
    mkdir -p runs/results/E07
    $PY_BASE experiments/exp07_external_testset/contamination_check.py | tee runs/results/E07/contamination.txt &&
      $TOOLS publish runs/results/E07 results/E07_external_testset/kit --only contamination.txt ;;
  e10_stopping)
    mkdir -p runs/results/E10
    $PY_BASE experiments/exp10_stopping_behavior/analyze_stopping.py --runs runs/e00/eval \
        --judge runs/judge/e00/verdicts.jsonl | tee runs/results/E10/stopping_e00.txt &&
      $TOOLS publish runs/results/E10 results/E10_stopping_behavior/kit --only stopping_e00.txt ;;
  e12_pvalues)      $TOOLS pvalues --out results/E12_multiple_comparisons/kit ;;

  *) echo "!! unknown task $TASK"; exit 2 ;;
esac
rc=$?
echo "== task $TASK rc=$rc  $(date -u +%FT%TZ)"
exit $rc
