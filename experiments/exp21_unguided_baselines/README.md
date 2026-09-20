# exp21 — Guidance vs no guidance, at three seeds

**Why.** E01 and E17 already compare four sources of trajectories at matched size: the student's own
unguided rollouts, teacher-guided rollouts, self-guided rollouts, and the teacher's own unguided
rollouts (plain distillation). Each was one training seed, and self-guided seeds vary by 1.7
points, so the differences deserve the same three-seed treatment as the main result.

**Design.** No new data: the same splits, retrained with seeds 17 and 23 beside the existing 13.

| Arm | Trajectories | Guidance | Split |
|---|---|---|---|
| `unguided` | the student's own rollouts, correct ones kept | none | `splits_sup_selfdist/matched` |
| `teacherguided` | the student's rollouts critiqued by DeepSeek-V4-Flash | teacher | `splits_sup_guided/matched` |
| `selfguided` | the student's rollouts critiqued by itself with the answer | self | `splits_sup_selftaught/matched` |
| `teacherrollouts` | the teacher's own rollouts (plain distillation) | none | `splits_sup_teachdist/matched` |

`results_E21full` repeats the comparison with every episode each route collected, where the
unguided arm gets seeds 17 and 23 as well (`selfdist_full`).

**Run.** Pool tasks `train_sup_{selfdist,guided,selftaught,teachdist}_s{17,23}`,
`train_selfdist_full_s{17,23}`, `eval_*`, `judge_*`, `results_E21`, `results_E21full`.
Statistics as in E20: per-seed paired tests plus a seed-averaged test with Holm over the two
planned contrasts (unguided vs self-guided, unguided vs teacher-guided).
