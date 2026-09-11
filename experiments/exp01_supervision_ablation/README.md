# exp01 — What supervision actually causes the gain?

**Tier 1. Run this one first. The paper's central claim rests on it.**

## The question

The headline result compares an untrained student against one trained on teacher-guided
episodes that were *filtered to the correct ones*. Two confounds are baked into that
comparison, and a reviewer will find both:

1. **The correctness filter.** Training on any set of *successful* trajectories helps.
   That is rejection sampling (STaR), and it needs no teacher at all.
2. **Trajectory distillation.** Training on a strong model's own rollouts is standard
   distillation. It also needs no *guidance*, just a good teacher.

Unless both are ruled out, "teacher guidance" is not shown to be the active ingredient.

## The design

Three training sets, **matched on episode count**, everything else identical:

| Arm | Trajectory source | Teacher in the loop | What it controls for |
|---|---|---|---|
| `selfdist` | the student's own rollouts, correct ones kept | no | the correctness filter alone |
| `teachdist` | the teacher's own rollouts, correct ones kept | no (teacher *is* the agent) | plain trajectory distillation |
| `guided` | the student's rollouts with the teacher critiquing each step (the shipped data) | yes | the method |

Matching on episode count matters: yields differ (guided episodes are correct ~54 % of the
time, an unguided student far less), so equal *collected* episodes means unequal training
examples. `01_build_matched_splits.sh` matches on **usable training episodes**, the quantity
that actually reaches the optimiser, and reports both numbers so you can state either.

## What you must generate first

The two control episode sets are **not** in this kit — they are collected in the
`teacher-guidence` repo, which already has the machinery:

```bash
# in teacher-guidence/ -- skip_teacher=True makes the agent act with no critic
python scripts/run_teacher_only_traces.py --agent <student-id> --out runs/selfdist   ...
python scripts/run_teacher_only_traces.py --agent <teacher-id> --out runs/teachdist  ...
```

Copy the resulting episode files here as:

```
data/episodes_selfdist/episodes.jsonl.gz
data/episodes_teachdist/episodes.jsonl.gz
```

`00_check_inputs.sh` tells you exactly what is missing.

## Run

```bash
export PARTITION=<gpu-partition>
bash 00_check_inputs.sh          # verify the two control sets are present
bash 01_build_matched_splits.sh  # -> data/splits/sup_{selfdist,teachdist,guided}_epN
bash 02_train_arms.sh            # 3 LoRA runs
bash 03_eval_arms.sh             # 3 x 4 held-out sets
bash 04_judge_and_compare.sh     # judge + paired tests
```

`DRY_RUN=1` on any of them prints the commands without submitting.

## Reading the result

- `guided` > `teachdist` and `guided` > `selfdist` at matched size: guidance is the
  active ingredient, and the paper's title is earned.
- `guided` ≈ `teachdist`: the gain is distillation from a strong model. Reframe the
  contribution as a cheaper way to get distillation data, not as guidance.
- `guided` ≈ `selfdist`: the gain is the correctness filter. That is a much weaker paper,
  and better to discover now than in review.

Report all three with the paired bootstrap CI and McNemar test that
`scripts/collect_results.py` already computes.
