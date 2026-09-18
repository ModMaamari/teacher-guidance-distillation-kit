# E07 — Contamination

**Question.** Is the result driven by overlap between the test questions and the training data?

**Answer.** No. 14 of the 747 held-out questions (1.9 %) share a rare 8-gram with the training
examples fed to the optimiser: HotpotQA 8/189, MuSiQue 4/203, 2WikiMultihopQA 1/170, StrategyQA
1/185. Dropping them leaves every arm within 0.3 points, and base → trained moves from +36.1 to
+36.2 points (733 paired questions). The flagged questions are easier for every arm, including
the untrained base student (35.7 % vs 27.0 %). That points to shared Wikipedia source text
rather than leaked answers. Numbers: `kit/contamination.txt`, `kit/exclude_flagged_e00.txt`,
flagged ids: `kit/flagged.json`.

**Protocol.** `experiments/exp07_external_testset/contamination_check.py`: 8-grams of each test
question against every prompt and completion in `data/splits/uniform/train.jsonl` (14,458
rows), counting only n-grams that occur in at most 3 training rows. `exclude_flagged.py`
re-scores the E00 arms with the Gemma-4-31B-it verdicts. The qid-level audit
(`scripts/check_leakage.py`) already guarantees no test question is a training question. Pool
task `e07_contamination`.

**Caveats.** n-gram overlap misses paraphrase. The second half of the plan, an external test set
the student cannot have seen, was not run: none was chosen.
