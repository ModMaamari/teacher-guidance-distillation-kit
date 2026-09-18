# E13 — Leave-one-dataset-out transfer

**Question.** Does guidance internalised on three datasets transfer to a fourth the student never
trained on?

**Answer.** Yes. Judge-correct on the whole unseen dataset, fold student vs base student
(Gemma-4-31B-it), with the paired difference and its 95 % CI:

| Unseen dataset | n | Fold student | Base student | Δ points | 95 % CI |
|---|---|---|---|---|---|
| HotpotQA | 2,000 | 69.0 % | 47.1 % | +21.9 | +19.7 to +24.1 |
| 2WikiMultihopQA | 2,000 | 71.3 % | 38.9 % | +32.4 | +30.1 to +34.8 |
| MuSiQue | 2,000 | 32.8 % | 11.7 % | +21.1 | +19.1 to +23.2 |
| StrategyQA | 1,999 | 65.3 % | 15.9 % | +49.4 | +47.0 to +51.8 |

On the held-out questions of its three training datasets, each fold trails the student trained on
all four by 1.3–5.5 points. Only the StrategyQA fold's gap is significant (−5.5, CI −8.9 to −2.0).
Numbers: `gemma/results.json`, table: `gemma/RESULTS.md`.

**Protocol.** Four LoRA students (`ibm-granite/granite-4.1-3b`), each trained on three datasets;
evaluated on the full unseen dataset (2,000 questions, three shards) and on the held-out 10 % of
its training datasets; base-student baselines on the same questions; budget 3, hidden; greedy.
Judge Gemma-4-31B-it (19,982 verdicts, with the same model on a second endpoint as fallback). Teacher-alone reference on seeded
samples of each full set.

**Source.** Research workspace, `training_methods/m1_lodo/runs/lodo` (2026-09-01).

**Caveats.** One seed. The teacher-alone reference covers a seeded sample of 229–273 questions per unseen set.

## History

- **2026-09-18: re-judged with Gemma-4-31B-it.** Episodes were imported unchanged
  (`experiments/exp00_reference/import_runs.py`, pool tasks `judge_e13` and `results_e13`). Every
  transfer gain stays large and significant. Accuracy is lower under Gemma for both arms: fold
  students 69.0/71.3/32.8/65.3 % vs Kimi's 70.6/73.8/36.8/66.9 %, base 47.1/38.9/11.7/15.9 % vs
  49.2/44.4/13.8/18.9 % (HotpotQA/2Wiki/MuSiQue/StrategyQA).
- **2026-09-01: first judged with Kimi-K2.6.** Kept as `results.json`, superseded by `gemma/`.
