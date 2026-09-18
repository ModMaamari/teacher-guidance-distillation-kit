# E04 — Data scaling

**Question.** How much teacher-guided data does the student need?

**Answer.** Very little: the curve is nearly flat after 1,000 episodes. Judge-correct on the 747
held-out questions:

| Episodes collected | Usable (correct) | Training examples | Judge-correct | 95 % CI (Wilson) |
|---|---|---|---|---|
| 0 (base) | — | — | 27.3 % | 24.2–30.6 |
| 500 | 274 | 1,029 | 57.6 % | 54.0–61.1 |
| 1,000 | 542 | 2,021 | 60.2 % | 56.7–63.7 |
| 2,000 | 1,076 | 4,020 | 60.0 % | 56.4–63.4 |
| 4,000 | 2,188 | 8,186 | 61.3 % | 57.8–64.7 |
| 7,252 (all) | 3,959 | 14,458 | 62.1 % | 58.6–65.5 |

Half of the full gain appears with 500 episodes. Of all the pairwise differences between sizes,
only 500 vs all (+4.5 points, p 0.008) and 500 vs 4,000 (+3.8, p 0.02) are significant. Seed
noise is about 0.3 points (E02). Figure data: `kit/figure_scaling.csv`; table: `kit/RESULTS.md`,
`kit/table.tex`.

**Protocol.** Nested cuts of the uniform split: one seeded order per dataset, and each size is a
prefix of the next (`scripts/make_size_splits.py`), all against the same dev set. Every size was
trained, evaluated and judged exactly like E02's seed 13, which is the 7,252-episode point. Pool
tasks `prep_sizes`, `train_ep*`, `eval_ep*`, `judge_ep*`, `results_E04`.

**Caveats.** One seed per size.

## History

- **2026-09-18:** first run (pool). A 500-episode point was added to the planned 1k/2k/4k ladder.
