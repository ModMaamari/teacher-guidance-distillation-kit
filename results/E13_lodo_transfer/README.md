# E13 — Leave-one-dataset-out transfer

**Question.** Does guidance internalised on three datasets transfer to a fourth the student never
trained on?

**Answer.** Yes. Judge-correct on the whole unseen dataset (fold student vs base student):
HotpotQA 70.6 % vs 49.2 %, 2WikiMultihopQA 73.8 % vs 44.4 %, MuSiQue 36.8 % vs 13.8 %,
StrategyQA 66.9 % vs 18.9 %. On the held-out questions of its training datasets each fold scores
within 0.5–6 points of the student trained on all four. Numbers: `results.json`; write-up:
`docs/RESULTS.md` (group A).

**Protocol.** Four LoRA students (`ibm-granite/granite-4.1-3b`), each trained on three datasets;
evaluated on the full unseen dataset (2,000 questions, three shards) and on the held-out 10 % of
its training datasets; base-student baselines on the same questions; budget 3, hidden; greedy.
Judge Kimi-K2.6 (18,956 verdicts; 28 from a fallback judge). Teacher-alone reference on seeded
samples of each full set.

**Source.** Research workspace, `training_methods/m1_lodo/runs/lodo` (2026-09-01).

**Caveats.** One seed; judged by Kimi-K2.6, not the current judge.
