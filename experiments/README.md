# Experiments

One folder per experiment. Each has a `README.md` saying what it answers and how to read
the result, and scripts numbered in the order you run them. Everything here drives the
kit's existing stage scripts; nothing re-implements training or evaluation.

## Set this up once

```bash
export PARTITION=<your gpu partition>     # required to submit anything
export ACCOUNT=<slurm account>            # only if your cluster needs one
export GRES=gpu:1                         # or gpu:<type>:1 to pick a card
export STUDENT_MODEL=ibm-granite/granite-4.2-3b
cp .env.example .env                      # teacher + judge endpoints, see docs/PROVIDERS.md
make data                                 # builds the SFT train/dev files (~2 min, required)
```

**`DRY_RUN=1` on any script prints what it would submit and submits nothing.** Use it first,
every time. All scripts are idempotent: finished work is skipped, so resubmitting after a
time-limit kill continues where it stopped.

## Check everything still works

```bash
bash experiments/run_smoke_tests.sh            # offline: syntax, dry-runs, fixtures
ONLINE=1 bash experiments/run_smoke_tests.sh   # also probes students and teachers live
```

67 checks offline, 69 with the live probes. It submits nothing, needs no GPU, and calls no
model unless `ONLINE=1`. Run it after changing any script here.

## Order

Tier 1 first. These are the ones a reviewer can sink the paper with.

| # | Experiment | Answers | Cost |
|---|---|---|---|
| **01** | `exp01_supervision_ablation` | is *guidance* the active ingredient, or just filtered SFT? | 3 trainings + evals |
| **02** | `exp02_seed_variance` | do the small effects survive a different seed? | 3 trainings + evals |
| **03** | `exp03_judge_validity` | does a human agree, and does the ranking survive another judge? | API only + human labelling |
| 04 | `exp04_data_scaling` | how much guidance do you need? | 5 trainings + evals |
| 05 | `exp05_student_family` | does it work for other students? | 6 trainings + evals |
| 06 | `exp06_teacher_strength` | is the effect specific to one teacher? | 2 collections + 2 trainings |
| 07 | `exp07_external_testset` | is the result contamination-driven? | 1 eval sweep + a new dataset |
| 08 | `exp08_step_budget` | does budget 3 drive the conclusion? | evals only, no training |
| 09 | `exp09_forgetting` | what did training cost in general ability? | cheap, scripts already exist |
| 10 | `exp10_stopping_behavior` | the diagnosed gap, measured then closed | analysis, then 1 training |
| 11 | `exp11_training_knobs` | is LoRA capacity the ceiling? | ~10 short trainings |
| 12 | `exp12_multiple_comparisons` | do the p-values survive correction? | seconds, CPU |

**12 needs nothing but existing results — run it today.** 09 is nearly free. 08 needs no
training at all. If GPU time is short, those three plus 03 buy the most credibility per hour.

## Two things that are not in this kit

**Collecting new episodes** happens in the `teacher-guidence` repo, not here. Experiments 01
and 06 need episode sets this kit does not ship; their READMEs give the exact commands and
where to copy the output.

**The size ceiling.** The shipped trainable pool is 7,252 episodes, of which 54.6 % are
correct, giving 3,959 usable training episodes and 14,458 SFT examples. Any experiment
asking for more than 7,252 collected episodes needs a fresh collection round first. See
`exp04_data_scaling/README.md`.

## Conventions

- Arms are named so `scripts/collect_results.py` keeps them apart: `sup_<source>`,
  `seed<N>`, `ep<N>`, `stu_<model>`, `teach_<teacher>`, `<arm>_b<budget>`, `knob_<setting>`.
- Trained adapters land in `runs/train/<name>/adapter`, evaluations in
  `runs/eval/<arm>/<test-set>/`, verdicts in `runs/judge/`, tables in `runs/results/`.
- Every judged comparison already carries a paired bootstrap CI and an exact McNemar test.
  Report the CI, not just the point estimate.
