# E19 — Robustness of the self-guided student

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

**Done: transfer.** Four leave-one-dataset-out students trained on the self-guided episodes
(`data/splits_self/lodo/fold_*`), each evaluated on every question of the dataset it never saw,
against the base student re-run on the same questions:

| Unseen dataset | n | Base | Self-guided fold | Δ (95 % CI) | Teacher-guided fold (E13) |
|---|---|---|---|---|---|
| HotpotQA | 2,000 | 46.9 % | 72.5 % | +25.7 (+23.4 to +27.8) | 69.0 % |
| 2WikiMultihopQA | 2,000 | 38.6 % | 73.3 % | +34.6 (+32.3 to +37.0) | 71.3 % |
| MuSiQue | 2,000 | 12.2 % | 40.6 % | +28.4 (+26.2 to +30.6) | 32.8 % |
| StrategyQA | 1,999 | 16.9 % | 64.8 % | +47.9 (+45.6 to +50.3) | 65.3 % |

Self-guided folds transfer at least as well as teacher-guided ones: higher on three unseen
datasets and within 0.5 points on StrategyQA. The teacher-guided folds come from E13 and were
compared there with an earlier base run (47.1 / 38.9 / 11.7 / 15.9 %). Numbers:
`lodo/results.json`, table `lodo/RESULTS.md`.

**Caveats.** One seed per fold.

## History

- **2026-09-18:** forgetting check (pool task `forget_selftaught`).
- **2026-09-19:** seeds 17 and 23, paired with the teacher-guided seeds (`results_E19`); the four
  transfer folds (`results_E19lodo`).
