# Handoff — running the experiments

For whoever picks up `experiments/`. It says what state the repository is in, what to set up
before submitting anything, what has changed since the experiment folders were written, and in
which order to run them. Each experiment's own `README.md` is still the authority on *why* it
exists and how to read its result; this page is the operational layer around them.

Written 2026-09-18 against commit `6ae1340`.

## 1. State of the repository

**Present and finished:**

| | |
|---|---|
| Questions and corpora | `data/questions/<ds>/` — 2,000 each for HotpotQA, 2WikiMultihopQA, MuSiQue, 1,999 for StrategyQA |
| Teacher-guided episodes | three sets of 7,999 on the same questions: `data/episodes/` (teacher DeepSeek-V4-Flash), `data/episodes_glm/` (teacher GLM-5.3-flash, student granite-4.2-3b), `data/episodes_self/` (granite-4.1-3b as both student and teacher) |
| SFT splits | `data/splits/{uniform,lodo,test}` — already built here by `make data` |
| Judge verdicts | `runs/judge_shipped/`, `runs/judge_glm/`, `runs/judge_self/` — one verdict per episode for each of the three sets |
| Collection-side comparison | `runs/compare_teachers/`, documented in `docs/TG_DATASETS.md` |

**Finished results** live in `results/`, one folder per experiment ID, and
`experiments/REGISTRY.md` shows the status of all of them (`docs/RESEARCH_WORKFLOW.md`). The
reference (E00), transfer (E13) and stability (E14) results were produced in the research
workspace and imported; their raw runs (adapters, episodes, verdicts) are not in this checkout, so
`runs/train/`, `runs/eval/` and `runs/results/` are empty here. Experiments that need a trained
adapter should point `ADAPTER` at the corrected-loss adapter described in E14.

**Health check as of this writing:** `bash experiments/run_smoke_tests.sh` passes 67 of 67 offline
checks against the current code. `make test` passes 55 unit tests.

## 2. Set up once

1. **Environments.** `bash setup_env.sh` builds three virtualenvs: `.venv` (CPU: data, judging,
   the teacher arm, results), `.venv_train` (training and in-process evaluation), `.venv_vllm`
   (serving, pinned to vLLM 0.28.0). Build it on a machine that sees the GPU driver, or
   `ONLY=serve bash setup_env.sh` for the serving one alone.
   *In this checkout `.venv_vllm` does not exist:* the local `.env` sets `PY_VLLM` to a vLLM
   environment outside the repository, and `slurm/common.sh` honours that. On a fresh machine,
   either create `.venv_vllm` or set `PY_VLLM` yourself, then check it:
   `$PY_VLLM -c "import vllm, sys; print(vllm.__version__)"`.
2. **Credentials.** `cp .env.example .env` and fill in the teacher and judge endpoints
   (`docs/PROVIDERS.md` explains the provider prefixes). `.env` is gitignored — keep every
   machine-specific value there, never in a tracked file.
3. **Data.** `make data` builds `data/splits/` from the episodes and audits it for leakage. It is
   already built here; re-run it after changing the episode set you train from.
4. **Sanity checks**, in increasing cost: `make test`, `make smoke` (whole pipeline on mock
   models, no GPU or API), `bash experiments/run_smoke_tests.sh` (every experiment script parses,
   dry-runs and passes its fixtures), `ONLINE=1 bash experiments/run_smoke_tests.sh` (adds live
   student and teacher probes). Run the last one after editing anything under `experiments/`.
5. **GPU smoke** before a real training run: `sbatch -p <gpu-partition> tests/smoke_gpu.sbatch`
   (~25 min, real student, tiny run).

### Environment variables the scripts read

| Variable | Meaning |
|---|---|
| `PARTITION` | **required to submit anything**; the GPU partition |
| `ACCOUNT` | Slurm account, if your cluster needs one |
| `GRES` | default `gpu:1`; use `gpu:<type>:1` to pick a card. An untyped request can land on a card too small to serve the student |
| `CPU_PARTITION` | partition for CPU-only jobs (judging, the teacher arm); falls back to `PARTITION` |
| `STUDENT_MODEL` | default `ibm-granite/granite-4.2-3b` |
| `TEACHER`, `JUDGE` | provider-prefixed ids; a comma-separated chain is a fallback list |
| `DRY_RUN=1` | print what would be submitted and submit nothing |
| `PY`, `PY_TRAIN`, `PY_VLLM` | interpreters, if not the defaults in the checkout |
| per experiment | `SEEDS`, `SIZES`, `BUDGETS`, `ARMS`, `TESTS`, `SEED`, `SPLIT`, `SIZE_SPLIT`, `STUDENT_LIST`, `TEACHER_ARMS`, `EXTERNAL_DS`, `ADAPTER`, `SWAP_A`, `SWAP_B`, `MODELS` |

**Use `DRY_RUN=1` first, every time.** Every script is idempotent: finished work is skipped, so
resubmitting after a time-limit kill continues where it stopped.

## 3. Pick the judge deliberately

`experiments/_common.sh` still defaults `JUDGE` to Kimi-K2.6, which is what `docs/RESULTS.md`
used. A later benchmark of 14 candidate judges on 145 labelled question–answer pairs (86
correct, 59 incorrect; labels assigned by the AI assistant, not a human — see E16) ranked
Gemma-4-31B-it first:

| Judge | Accuracy | Cohen's κ | Incorrect answers accepted |
|---|---|---|---|
| Gemma-4-31B-it | 98.6 % | 0.97 | 3.4 % |
| Kimi-K2.6 | 94.5 % | 0.88 | 11.9 % |

So: `export JUDGE=oai-<name>/RedHatAI/gemma-4-31B-it-FP8-block,oai-<name2>/<same model>` — two
endpoints of the same model, so one stalling endpoint cannot stall a run. Since commit `2396c65`
the router trips its circuit breaker per endpoint rather than per provider type, which is what
makes that fallback effective.

Three rules that cost real results when broken:

* **One judge across everything you compare.** `docs/RESULTS.md` (Kimi) and `docs/TG_DATASETS.md`
  (Gemma) are not directly comparable.
* **The judge is never the teacher**, or the teacher grades its own student (exp03, exp06).
* **Re-judging is cheap; re-running arms is not.** `scripts/judge.py` resumes, so judging a new
  arm costs only the new episodes.

## 4. What changed since the experiment folders were written (2026-09-11)

* **Collecting episodes now happens in this kit.** `experiments/README.md`, exp01 and exp06 say
  new episode sets must be collected in a separate repository. That is out of date:
  * `slurm/collect_api.sbatch` — student and teacher both behind APIs, no GPU.
  * `slurm/collect_local.sbatch` — student served by vLLM on the job's GPU; the teacher defaults
    to that same served model (self-teaching), or set `TEACHER` to any provider-prefixed id.
  * Both wrap `scripts/collect_episodes.py`, are resumable, and run a one-question check before
    the full chunk. Consolidate with `scripts/consolidate_episodes.py --strict`.
* **Two more episode sets ship** (see the table in §1 and `docs/TG_DATASETS.md`), which gives
  exp06 two of its teacher arms for free — with the caveat that the GLM set used a different
  student, so it mixes the teacher's effect with the student's.
* **`scripts/compare_teachers.py`** compares collections *before* training — outcome, training
  yield, teacher behaviour, leak control — with paired bootstrap CIs and McNemar tests. It
  complements `scripts/collect_results.py`, which compares trained arms.
* **Fixes that matter for long runs:** the simulate loop no longer keeps every episode in memory
  (`d3464b1`; workers used to grow ~75 MB per episode until the job's memory limit killed them),
  vLLM calls default to a 300 s timeout (`8215f5f`), the judge reads the last verdict object in a
  reply (`ad1ff62`), and the circuit breaker is per endpoint (`2396c65`).

## 5. Suggested order

**Step 0 — the reference results.** They exist (`results/E00_reference`). Run the headline
pipeline only to reproduce them in this checkout (`docs/REPRODUCE.md` §2):

```bash
export PARTITION=<gpu-partition>
TEACHER=<teacher-id> JUDGE=<judge-chain> bash slurm/run_pipeline.sh -p "$PARTITION"
```

It submits, with dependencies: train the uniform student → evaluate base and trained on the four
held-out sets → the guided arm → the teacher arm (CPU) → judge → `runs/results/`. Expect about
4 GPU-hours for the training plus evaluation time.

Then, cheapest-first:

| Order | Experiment | Needs | Cost |
|---|---|---|---|
| 1 | **12** multiple comparisons | `runs/results/results.json` | seconds, CPU |
| 2 | **09** forgetting | a trained adapter | cheap, one job per arm |
| 3 | **08** step budget | a trained adapter | evaluation only, no training |
| 4 | **03** judge validity | judged episodes + a person to label ~150–200 rows | API only |
| 5 | **02** seed variance | the uniform split | 3 trainings + evaluations |
| 6 | **01** supervision ablation | two control episode sets (see below) | 3 trainings + evaluations |
| 7 | **04**, **05**, **06**, **07**, **10**, **11** | see each README | the expensive half |

Experiments 01, 02 and 03 are the ones the project's own README marks Tier 1: they are what a
reviewer uses to attack the central claim.

## 6. Notes per experiment

* **01 supervision ablation.** Needs `data/episodes_selfdist/` (student rollouts, no teacher) and
  `data/episodes_teachdist/` (teacher's own rollouts). Before budgeting GPU time, settle how to
  produce them: `scripts/collect_episodes.py` always builds its template with the teacher in the
  loop (`skip_teacher: False`), so either expose that flag or use `scripts/eval.py --arm student`
  / `--arm teacher`, whose episode files follow the same schema. Verify that
  `scripts/build_splits.py` yields SFT examples from whichever you choose *before* collecting
  8,000 of them. `00_check_inputs.sh` tells you what is missing.
* **02 seed variance.** `SEEDS="13 17 23" bash run.sh`, then `bash run.sh judge`, then
  `python summarize_seeds.py`. Three seeds is the minimum for a "± sd"; five is better.
* **03 judge validity.** With Gemma as the primary judge, pick two *different* swap judges — for
  example Qwen3.6-35B-A3B-FP8 (97.9 % on the same benchmark) and Mistral-Medium-3.5-128B — via
  `SWAP_A` and `SWAP_B`. The human sample is blind by construction; label at least 150 rows.
* **04 data scaling.** The shipped trainable pool is 7,252 episodes (about 54.6 % correct →
  3,959 usable → 14,458 SFT examples). The default ladder 500 → 7,252 spans 14×; anything above
  needs a fresh collection round, which this kit can now do itself.
* **05 student family.** Run `00_probe_students.sh` first (tokenizer only, no GPU). The Liquid
  model opens a reasoning block unconditionally — read that README before interpreting its
  diagnostics. Pin `SIZE_SPLIT` to one split so data is not a confound.
* **06 teacher strength.** Two of the three arms already exist: `data/episodes_glm/` (a different
  teacher *and* a different student) and `data/episodes_self/` (the student teaching itself, which
  is the weakest possible teacher and therefore a useful low anchor). For a clean scale axis,
  collect the two Mistral arms named in its README with `slurm/collect_api.sbatch`. Match
  supervision across teachers before training — yields differ by teacher.
* **07 external test set.** Needs a dataset the students cannot have memorised, in the kit's
  format; `prepare_external.py` converts and validates it. `contamination_check.py` runs today
  against the shipped split.
* **08 step budget.** Evaluation only. Report cost alongside accuracy: the efficiency claim is
  stated at budget 3.
* **09 forgetting.** One job measures base and adapter on the same server, so do not submit a
  base-only run. Also worth running `slurm/eval_stability.sbatch` per arm.
* **10 stopping behaviour.** `analyze_stopping.py` needs `runs/eval/`. Measure the ceiling before
  spending a GPU hour trying to close the gap.
* **11 training knobs.** About ten short trainings. Watch the loss-path guard (`docs/STABILITY.md`)
  in every run; a knob sweep is where an unusual configuration trips it.
* **12 multiple comparisons.** Run it the moment `runs/results/results.json` exists, and keep
  re-running it as experiments add comparisons.

## 7. Operational notes from recent runs

* **Serving takes time.** A 3B student behind vLLM took 10–13 minutes from job start to first
  answer. Size job time limits accordingly; a 45-minute job spends a quarter of itself starting.
* **Memory.** After `d3464b1` a collection worker holds ~0.8 GB steady. Before it, workers grew
  until the job's limit killed them — if you see `exited -9`, that is an out-of-memory kill, not a
  crash.
* **One output directory per concurrent job.** Every collection job repairs bookkeeping in its
  `OUT` at startup, so two jobs sharing one `OUT` will disturb each other.
* **Resume is the normal path.** Re-run the same command; finished questions, finished evaluations
  and existing verdicts are skipped.
* **Watch:** `squeue -u $USER`, `runs/slurm/*.log`, and the `status.json` each long-running stage
  writes.

## 8. Where results land, and how to report them

```
runs/train/<name>/adapter          trained adapter (.done marks a finished run)
runs/eval/<arm>/<test-set>/        episodes.jsonl + status.json per arm and test set
runs/judge/verdicts.jsonl          one verdict per (episode file, question)
runs/results/results.{json,md}     per-arm table + every paired comparison
runs/compare_teachers/             collection-side comparison (REPORT.md, comparison.json)
```

Every judged comparison already carries a paired bootstrap 95 % CI and an exact McNemar test.
Report the interval, not just the point estimate, and run exp12 before quoting p-values.

## 9. Open items

* The raw runs behind E00, E13 and E14 are outside this checkout; set `ADAPTER` to the corrected
  adapter for experiments that need a trained student.
* `_common.sh` still defaults to the older judge — override `JUDGE`, or change the default once
  the team agrees.
* `docs/RESULTS.md` numbers come from the older judge; if you re-judge those arms with the current
  one, update that page and say which judge produced which table.
* exp01's two control episode sets do not exist yet, and how to produce them is the open design
  question in §6.
* The three episode sets are tracked in git (~140 MB of compressed data), so clones are large.
  If that becomes a problem, moving them to Git LFS is a history rewrite — decide before the
  repository is shared more widely.
