# exp25 — Is self-guidance better than plain self-distillation? Six seeds

**Why.** E21 took the supervision ablation to three seeds and left the paper's central mechanism
claim undecided: self-guided trajectories beat the student's own unguided, correctness-filtered
rollouts by +1.7 points with all data (95 % CI −0.2 to +3.6, p 0.089) and +1.5 at matched size
(p 0.13). The sign is positive in five of six seed pairs, so the question is power, not direction.
Collecting self-guided data costs about three times what plain self-rollouts cost (0.099 vs 0.032
PFLOPs per episode, E23), so whether that increment is real decides whether the method earns its
collection budget.

**Design.** No new data and no new method: the two full-size splits are retrained with three more
seeds each (29, 31, 37), giving six seeds per arm.

| Arm | Trajectories | Split | Seeds |
|---|---|---|---|
| `unguided` | the student's own rollouts, correct ones kept | `splits_selfdist/uniform` | 13, 17, 23 + 29, 31, 37 |
| `selfguided` | the same rollouts critiqued by the student with the gold answer | `splits_self/uniform` | 13, 17, 23 + 29, 31, 37 |

**Power.** With a seed SD of about 1.5 points, three seeds give a standard error of ~0.9 on each
arm's mean; six give ~0.6. A true difference of 1.7 points is then about three standard errors, so
six seeds should separate it from zero if it is real, and bound it tightly if it is not. The
decision rule is stated before the runs: the seed-averaged paired test over the 747 questions
(bootstrap CI, sign-flip permutation p), reported whichever way it comes out.

**Run.** Pool tasks `train_selfdist_full_s{29,31,37}`, `train_selftaught_s{29,31,37}`, `eval_*`,
`judge_*`, `results_E25`.
