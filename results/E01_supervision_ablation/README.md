# E01 — What supervision causes the gain?

**Question.** Is teacher guidance the active ingredient? The alternatives are the correctness
filter (training on any successful trajectories) and plain distillation of the teacher's own
trajectories.

**Answer.** Not guidance, under this protocol.
- **Filter alone matches guidance.** At matched size, the student trained on its own unguided
  rollouts, keeping only the correct ones, is as good as the student trained on teacher-guided
  rollouts: −0.8 points, n.s.
- **Teacher rollouts do best.** Training on the teacher's own correct rollouts beats both, by
  +5.5 and +6.3 points.

Judge-correct on the 747 held-out questions:

| Training trajectories (correct ones kept) | Usable episodes | Training examples | HotpotQA | 2Wiki | MuSiQue | StrategyQA | All | Δ vs base [95 % CI] |
|---|---|---|---|---|---|---|---|---|
| — (base student) | — | — | — | — | — | — | 27.3 % | — |
| Student alone, no teacher (`selfdist`) | 1,429 | 5,291 | 64.5 | 75.9 | 39.9 | 68.6 | 61.5 % | +34.1 [+30.4, +38.0] |
| Student guided by the teacher (`guided`, the method) | 1,401 | 5,236 | 64.0 | 78.8 | 39.9 | 69.7 | 62.3 % | +34.9 [+31.1, +38.8] |
| Teacher alone as the agent (`teachdist`) | 1,412 | 4,189 | 68.2 | 85.9 | 49.7 | 70.3 | 67.7 % | +40.4 [+36.4, +44.3] |

Paired differences (McNemar p):
- guided − selfdist: +0.8 [−2.4, +3.9], p 0.67
- teachdist − guided: +5.5 [+2.3, +8.8], p 0.001
- teachdist − selfdist: +6.3 [+2.9, +9.6], p 0.0004

Seed noise is about 0.3 points (E02), so the teacher-rollout advantage is well beyond it and the
guided/self difference is not. Table: `kit/RESULTS.md`, `kit/table.tex`.

**How this reads with the other results.** The method's reading guide
(`experiments/exp01_supervision_ablation/README.md`) says guided ≈ student-alone means "the gain is
the correctness filter", and this is that case. The other results point the same way:
- **E06:** the self-taught student beat the DeepSeek-taught one.
- **E15:** at collection time, guided and self-taught episodes were equally often correct.
- **E04:** 500–1,000 episodes already give most of the gain.

What does carry signal is whose actions the student imitates. Correct trajectories written by the
strong model are worth about 6 points more than equally many correct trajectories written by the
student, with or without a teacher's critique.

**Protocol.**
- **Collection.** Three sets of rollouts on the same question files, same harness (plan + 3
  steps, hidden budget, plan review off when no teacher):
  - `selfdist`: `granite-4.1-3b` alone, 2,000 questions per dataset, `scripts/collect_episodes.py
    --no-teacher`.
  - `teachdist`: DeepSeek-V4-Flash-0731 alone as the agent, 500 questions per dataset.
  - `guided`: the shipped teacher-guided episodes (student `granite-4.1-3b`, teacher
    DeepSeek-V4-Flash).
- **Matching.** Matched on usable training episodes, the ones that reach the optimiser, with
  `match_sizes.py` and nested cuts. The teacher-alone arm was the limiting one and uses its whole
  split.
- **Training and evaluation.** Identical: E02's recipe (seed 13), greedy, budget 3, judge
  Gemma-4-31B-it.
- **Pool tasks.** `collect_*dist`, `prep_*dist`, `prep_e01_match`, `train_sup_*`, `eval_sup_*`,
  `judge_sup_*`, `results_E01`.

**Caveats.**
- **One seed per arm.**
- **Teacher version.** The guided set's teacher was DeepSeek-V4-Flash; the teacher-alone agent
  was the 0731 revision, since the original was retired from the endpoint.
- **Question pool.** The teacher-alone arm covers fewer distinct questions (the first 500 per
  dataset vs up to 2,000). Its advantage comes with fewer training examples (4,189 vs about
  5,250), because teacher episodes are shorter.
- **Scope.** The result is for this student (3B), these four datasets and a 3-step budget. It
  does not say guidance never helps. It says the gain measured here does not need it.

## History

- **2026-09-18:** first run (pool). The teacher-alone collection was cut from 1,000 to 500
  questions per dataset to fit the endpoint's throughput. 500 already made it the limiting arm
  at ≈1,400 usable episodes.
