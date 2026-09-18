# E02 — Seed variance

**Question.** Do the gains survive other training seeds?

**Answer.** Yes, and seed noise is small. Three students trained on the uniform split with seeds
13, 17 and 23 score 62.1 %, 61.6 % and 62.0 % judge-correct on the 747 held-out questions: 61.9 ±
0.3 % (mean ± SD, n = 3). Base 27.3 %. Every seed beats the base by +34.3 to +34.8 points (each
CI at least 30.4 points above zero). No two seeds differ significantly (largest gap 0.5 points,
McNemar p ≥ 0.78). A difference between two trained arms much larger than about 1 point is
therefore not seed noise.

| Arm | HotpotQA | 2Wiki | MuSiQue | StrategyQA | All | Δ vs base [95 % CI] |
|---|---|---|---|---|---|---|
| Base student | 42.9 | 35.3 | 17.2 | 15.1 | 27.3 | — |
| Seed 13 | 63.5 | 76.5 | 38.9 | 73.0 | 62.1 | +34.8 [+30.8, +38.7] |
| Seed 17 | 63.0 | 78.2 | 36.9 | 71.9 | 61.6 | +34.3 [+30.4, +38.1] |
| Seed 23 | 63.0 | 76.5 | 36.9 | 75.1 | 62.0 | +34.7 [+30.8, +38.6] |

Per-dataset numbers for every seed: `kit/RESULTS.md`; summary: `kit/seeds.txt`; LaTeX: `kit/table.tex`.

**Protocol.** Student `ibm-granite/granite-4.1-3b`, LoRA rank 32, α 64, lr 1e-4, 2 epochs,
effective batch 16, max length 8,192. Trained by the kit's own `scripts/train_sft.py` (loss path
fixed, E14) on `data/splits/uniform` (14,458 examples). Evaluated with vLLM, greedy, budget 3,
hidden, and judged by Gemma-4-31B-it. Pool tasks `train_seed*`, `eval_seed*`, `judge_seed*`,
`results_E02`.

**Consistency with E00.** The kit-trained seed-13 student (62.1 %) and the research workspace's
trained student (63.3 %, E00) differ by 1.2 points. The kit's base arm reproduces the research
base arm: 27.3 % vs 27.2 %, with 88 % per-question agreement.

## History

- **2026-09-18:** first run (pool).
