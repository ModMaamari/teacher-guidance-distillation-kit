# E11 — LoRA rank

**Question.** Does adapter capacity limit the gain?

**Answer.** No. From rank 8 to rank 64 (8× the trainable parameters), judge-correct on the 747
held-out questions moves 2.1 points, and no two ranks differ significantly. The largest pair,
rank 64 vs rank 8, is +2.1 (CI −0.7 to +5.0, p 0.17). The default rank 32 is not a ceiling.

| LoRA rank (α = 2 × rank) | Judge-correct | Δ vs base [95 % CI] | Train loss | Dev loss |
|---|---|---|---|---|
| — (base student) | 27.3 % | — | — | — |
| 8 | 61.2 % | +33.9 [+30.0, +37.8] | 0.283 | 0.252 |
| 16 | 61.7 % | +34.4 [+30.5, +38.3] | 0.273 | 0.248 |
| 32 (default; E02 seed 13) | 62.1 % | +34.8 [+30.8, +38.7] | 0.264 | 0.247 |
| 64 | 63.3 % | +36.0 [+32.1, +39.9] | 0.257 | 0.249 |

Table: `kit/RESULTS.md`, `kit/table.tex`.

**Protocol.** Same split, seed (13), learning rate (1e-4), epochs (2) and evaluation as E02; only
`--lora-r` and `--lora-alpha` change. Judge Gemma-4-31B-it. Pool tasks `train_r*`, `eval_r*`,
`judge_r*`, `results_E11`.

**Caveats.** One seed per rank; E02's seed SD is 0.3 points. The second half of the plan
(learning rate and epochs) and a full fine-tune were not run.

## History

- **2026-09-18:** rank sweep (pool).
