# E25 — Does self-guidance beat plain self-distillation? Six seeds

**Question.** E21 took this comparison to three seeds and left it undecided: self-guided
trajectories beat the student's own unguided, correctness-filtered rollouts by +1.7 points with all
data, with a 95 % CI of −0.2 to +3.6 (p 0.089). Since self-guided collection costs about three
times what plain self-rollouts cost (0.099 vs 0.032 PFLOPs per episode, E23), the question decides
whether the method earns its collection budget. Three more seeds per arm halve the standard error.

**Answer.** Yes. With six seeds per arm the difference is **+2.3 points** and significant.
Judge-correct accuracy (Gemma-4-31B-it) on the 747 held-out questions:

| Arm | 13 | 17 | 23 | 29 | 31 | 37 | Mean |
|---|---|---|---|---|---|---|---|
| **Self-guided** | 66.7 | 64.9 | 63.2 | 63.6 | 64.9 | 65.2 | **64.8 ± 1.2** |
| Unguided self-rollouts | 62.3 | 64.8 | 62.6 | 62.0 | 60.6 | 62.4 | **62.5 ± 1.4** |

Seed-averaged (each question averaged over an arm's six seeds): **+2.3 points**, bootstrap 95 % CI
**+0.7 to +4.0**, sign-flip permutation **p 0.0079**. Per seed: +4.4 (p 0.003), +0.1 (p 1.0),
+0.5 (p 0.78), +1.6 (p 0.32), +4.3 (p 0.002), +2.8 (p 0.076) — positive in all six pairs, two of
them significant on their own.

**Reading.**
- **The effect is real but small**, about a third of the way from plain self-distillation to the
  teacher's own rollouts (+6.2 at matched size, E21). Anyone reading a single seed would have got
  anything from +0.1 to +4.4.
- **Three seeds were not enough** for an effect this size against this noise. The same data that
  looked inconclusive at three seeds (+1.7, p 0.089) is significant at six (+2.3, p 0.008), and the
  estimate barely moved: the interval shrank.
- **It costs three times the collection compute** of plain self-rollouts for those 2.3 points
  (1,395 vs 921 PFLOPs to build a student, E23), which is the trade-off to state rather than hide.
- The self-guided arm is also the more consistent of the two here (SD 1.2 vs 1.4).

**Protocol.** No new data and no method change: the same two full-size splits, the kit's LoRA
recipe, budget 3, primary judge, seeds 29, 31 and 37 added to the existing 13, 17 and 23. The
decision rule (the seed-averaged paired test) was written down before the runs, in
`experiments/exp25_seed_power/README.md`.

**Files.** `kit/summary.txt`/`.json` (seed table, per-seed and seed-averaged tests),
`kit/results.json`/`RESULTS.md`.

**Caveats.** Six seeds still estimate an SD from few samples. This is the full-size comparison; at
matched supervision (~1,400 episodes) the three-seed estimate is +1.5 (p 0.13, E21) and has not
been extended. One judge, one student, four datasets.

## History

- **2026-09-20:** first run (pool). It resolved the comparison E21 left open, in the method's
  favour, and shows that the earlier three-seed "not established" was a power problem rather than
  an absent effect.
