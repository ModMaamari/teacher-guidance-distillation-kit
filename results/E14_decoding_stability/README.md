# E14 — Decoding stability and the loss-path fix

**Question.** Can the trained student be sampled, and did fixing the training loss path change the
greedy results?

**Answer.** The first trained adapter optimised logits at 10x the scale inference uses (TRL's
chunked loss read the wrong config field for this architecture), so it decoded greedily but
produced nothing usable when sampled. Retrained with the corrected loss path (same data,
hyper-parameters and seed), on 300 held-out questions at budget 3: greedy cover 61.0 % both
before and after the fix; temperature 0.7 with nucleus sampling went from 0.0 % to 59.7 %;
temperature 0.3 with min-p 0.1 from 0.0 % to 61.7 %. The next-token distribution went from
entropy 10.9 with 1.2 % of its mass on valid tokens to entropy 0.22 with 100 %. Details:
`docs/STABILITY.md`.

**Files.** `distribution_stats.json` (entropy, valid-token mass in and out of distribution),
`hf_sampling_check.json` (sampling check), `train_final_metrics.json` (the corrected run's final
training metrics).

**Source.** Research workspace, `training_methods/m1_calibrated/runs/all4_nll` (2026-09-04). This
corrected adapter is the one new experiments should build on.
