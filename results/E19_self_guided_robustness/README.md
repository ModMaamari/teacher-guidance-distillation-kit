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

**Done: seeds.** The self-guided student retrained with seeds 17 and 23, paired with the
teacher-guided seeds of E02 (same seeds, same recipe):

| Seed | Teacher-guided | Self-guided | Δ (95 % CI), McNemar p |
|---|---|---|---|
| 13 | 62.1 % | 66.7 % | +4.5 (+1.2 to +7.9), 0.010 |
| 17 | 61.6 % | 64.9 % | +3.4 (+0.3 to +6.6), 0.046 |
| 23 | 62.0 % | 63.2 % | +1.2 (−1.9 to +4.4), 0.51 |
| mean ± SD | 61.9 ± 0.3 % | 64.9 ± 1.7 % | +3.0 |

Self-guided training is less stable across seeds (SD 1.7 vs 0.3), but its lowest seed beats the
highest teacher-guided one. Numbers: `kit/results.json`, `kit/seeds.txt`.

**Still running.** The four leave-one-dataset-out self-guided folds against the base student on
the full unseen sets (`results_E19lodo`); the 2WikiMultihopQA fold's evaluation is the last piece.

## History

- **2026-09-18:** forgetting check (pool task `forget_selftaught`).
- **2026-09-19:** seeds 17 and 23, paired with the teacher-guided seeds (`results_E19`).
