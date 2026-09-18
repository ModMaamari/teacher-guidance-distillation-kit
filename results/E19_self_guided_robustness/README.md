# E19 — Robustness of the self-guided student (partial)

**Question.** Do the seed, transfer and forgetting results hold for the self-guided student?

**Done so far: forgetting.** The self-guided student (E06 `selftaught`) against the base weights,
same items and server, greedy:

| Benchmark | Items | Base | Self-guided | Δ points | McNemar p |
|---|---|---|---|---|---|
| MMLU | 1,710 | 63.51 % | 63.04 % | −0.47 | 0.45 |
| GSM8K | 1,319 | 89.16 % | 86.35 % | −2.81 | 0.0003 |
| HellaSwag | 1,500 | 75.27 % | 74.80 % | −0.47 | 0.53 |
| Pooled | 4,529 | 74.87 % | 73.72 % | −1.15 | 0.002 |

That is slightly more than the teacher-guided student (pooled −0.84, p 0.04; E09), and the loss
is concentrated on GSM8K rather than HellaSwag. Report: `forgetting/REPORT.md`, numbers:
`forgetting/stats.json`.

**Still running.** Seeds 17 and 23 of the self-guided student, the four leave-one-dataset-out
self-guided folds, and the base student on the full unseen sets (pool tasks `train_selftaught_s*`,
`train_selflodo_*`, `eval_basefull_*`, `results_E19`).

## History

- **2026-09-18:** forgetting check (pool task `forget_selftaught`).
