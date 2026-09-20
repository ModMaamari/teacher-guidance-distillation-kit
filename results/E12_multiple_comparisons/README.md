# E12 — Do the p-values survive multiple-comparison correction?

**Question.** Each results table runs several paired McNemar tests, so some uncorrected p < 0.05
are expected by chance. Which claims survive Holm (family-wise error) and Benjamini-Hochberg
(false discovery rate)?

**Answer.** Every headline claim survives at least BH, and most survive Holm. One family is one
results table: all pairs of its arms, pooled over the 747 held-out questions, judge-correct
accuracy (Gemma-4-31B-it).

| family | tests | survive Holm | the claims that matter |
|---|---|---|---|
| E00 reference | 6 | 6 | every pair, including trained vs guided (+7.1) and teacher vs trained (+7.8) |
| E01 supervision (matched) | 6 | 5 | teacher rollouts > unguided (+6.3) and > teacher-guided (+5.5), Holm ≤ 0.002; teacher-guided vs unguided n.s. |
| E02 seeds | 6 | 3 | base gains only; seeds do not differ (p ≥ 0.78) |
| E04 data scaling | 15 | 5 | base gains; 500 episodes vs all data survives BH only |
| E05 students | 6 | 5 | both students gain; Granite vs MiniCPM trained n.s. |
| E06 teacher strength | 6 | 4 | self-guided > DeepSeek-guided +4.5 (Holm 0.029); self vs GLM n.s. |
| E08 step budget | 66 | 59 | trained B3 → B5 +4.7 (Holm 0.010); teacher B3 → B5 +2.3 BH only |
| E11 LoRA rank | 10 | 4 | base gains only; ranks do not differ |
| E13 transfer (DeepSeek-guided folds) | 21 | 12 | every fold vs base (+25.1 to +43.7) and the teacher vs every student; among folds only HotpotQA vs StrategyQA reaches BH |
| E17 self-guidance, matched | 10 | 6 | self-guided > unguided +3.2 BH only (Holm 0.12, BH 0.044); teacher rollouts vs self-guided n.s. (raw 0.073) |
| E17 self-guidance, all data | 6 | 5 | self-guided > unguided +4.4 (Holm 0.008) and > DeepSeek-guided +4.5 (Holm 0.020) |
| E19 seeds (self vs DeepSeek-guided, 3 seeds each) | 21 | 7 | seed 13: +4.5 BH only (Holm 0.12, BH 0.021); seeds 17 and 23 n.s. |
| E19 transfer (self-guided folds) | 4 | 4 | every fold vs its base (+25.7 to +47.9) |
| E20 correctness filter (10 arms) | 55 | 15 | every arm vs base; correct-only > incorrect-only (-7.8, -6.0); seed-13 correct vs size-matched mix survives Holm, the seed-13/17 all-episode gaps BH only |
| E20 matched (early publication) | 28 | 12 | the same arms without the all-episode ones |
| E20 seed 13 | 10 | 6 | seed 13 of every arm |

**Reading.** The gains of training over the base student survive every correction. E20's planned
contrasts are corrected in its own summary over the two contrasts stated in advance (Holm 0.006
and 0.002); the 55-pair family here is far stricter and is reported for completeness. Two
claims are strong: that self-guided beats unguided and teacher-guided rollouts with all data, and
that the teacher's own rollouts beat both at matched size. Two claims are consistent but modest:
the matched-size self-guided advantage and the per-seed self-vs-teacher-guided differences. The
paper states which correction each claim survives.

**Protocol.** `experiments/exp12_multiple_comparisons/correct_pvalues.py` over the paired tests in
each `results/E*/*/results.json` (pool task `e12_pvalues`, `tools.py pvalues`). Raw p is exact
McNemar; differences are in accuracy points.

**Caveats.** A family is one table, as the paper reports it. Correcting across all tables at once
would be stricter still, and the E08 family of 66 pairs is inflated by uninteresting cross-budget
pairs.

## History

- **2026-09-19:** first run (pool); the diff column was then reprinted in points instead of
  fractions (the p-values are unchanged).
