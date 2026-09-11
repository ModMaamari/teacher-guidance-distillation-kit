# exp12 — Correct the p-values

**Tier 3, five minutes.** `docs/RESULTS.md` reports six pairwise McNemar tests from four
arms. Every experiment here adds more. Uncorrected, the family-wise error rate across six
tests at alpha 0.05 is about 26 %, and the smallest reported effect (trained vs guided,
p = 0.0052) is exactly the kind that does not survive correction cleanly.

Reviewers of empirical ML papers ask for this routinely, and its absence is free ammunition.

```bash
python correct_pvalues.py --results runs/results/results.json
```

Applies Holm-Bonferroni (family-wise, conservative) and Benjamini-Hochberg (false discovery
rate, standard for many comparisons) to every pair `collect_results.py` produced, and
prints which conclusions change.

## Reporting

Add a corrected-p column to the paired-differences table and say which correction you used.
If a result survives Holm, state that explicitly; it is a strong sentence and costs nothing.
