# E22 — Should the correctness filter be a string match or an LLM judge?

**Question.** Every training split keeps episodes whose final answer *covers* the gold answer, a
string test with no LLM. E20 showed that filter is worth 2.3 points, and that it drops 22.9 % of
episodes an LLM judge would accept (the right answer, worded differently) while keeping 4.4 % the
judge rejects. Does filtering with the judge instead train a better student?

**Answer.** No. The judge keeps 598 more episodes and trains a slightly *worse* student, at 15 %
more training compute. Judge-correct accuracy (Gemma-4-31B-it) on the 747 held-out questions, three
seeds per arm:

| Filter | Episodes kept | Examples | Train PFLOPs | Seeds 13 / 17 / 23 | Mean |
|---|---|---|---|---|---|
| **cover match (the kit's filter, free)** | 3,818 | 13,825 | 684 | 66.7 / 64.9 / 63.2 | **64.9 ± 1.7** |
| LLM judge (Gemma-4-31B-it) | 4,416 | 15,960 | 790 | 64.8 / 64.0 / 62.4 | **63.7 ± 1.2** |

Seed-averaged difference **−1.2 points** (bootstrap 95 % CI −2.7 to +0.3, sign-flip permutation
p 0.126). Every seed is negative (−1.9, −0.9, −0.8), none significantly so.

**Reading.**
- **The cheap filter is not leaving value on the table.** The 598 extra episodes the judge admits
  are exactly the ones whose final answer does not contain the gold string — right in substance,
  loose in form. Training on them does not help, and the point estimate says it mildly hurts.
- **Filtering by the judge is not free.** It costs an LLM call on every episode *collected*, not
  only on those kept, plus 15 % more training compute for the larger set (790 vs 684 PFLOPs).
- **Together with E20:** the filter matters (dropping it costs 2.3 points), but which correctness
  test it uses does not, as long as it is a correctness test. A string match is enough here.

**Protocol.** The same self-guided episodes, the same LoRA recipe, budget 3 and primary judge; only
the filter changes (`build_splits.py --keep judge --judge-verdicts`). The judge verdicts already
existed from judging the collection, so the only new cost was training. Pool tasks `prep_e22`,
`train_judgefilt_s{13,17,23}`, `eval_*`, `judge_*`, `results_E22`.

**Files.** `kit/summary.txt`/`.json` (seed table, per-seed and seed-averaged tests),
`kit/train_cost.txt`/`.json`, `kit/results.json`/`RESULTS.md`, `kit/split_cover.json` and
`kit/split_judge.json`.

**Caveats.** One judge (the paper's primary) defines the alternative filter; a stricter or
differently-prompted judge might select differently. Three seeds per arm. The two arms differ in
training-set size by design, because that is what changing the filter does.

## History

- **2026-09-20:** first run (pool).
