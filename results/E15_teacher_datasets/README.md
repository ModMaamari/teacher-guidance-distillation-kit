# E15 — Teacher-guided datasets: DeepSeek, GLM and self-teaching

**Question.** How do episodes collected on the same 7,999 questions compare when the teacher is
DeepSeek-V4-Flash, GLM-5.3-flash, or the student itself?

**Answer.** With the student fixed (`granite-4.1-3b`), self-teaching and the DeepSeek teacher are
statistically tied on judge-correct overall (61.5 % vs 62.3 %, DeepSeek − Self +0.8 points, 95 % CI
−0.2 to +1.8); only StrategyQA differs (+5.3 for DeepSeek). The self-teacher is a poor grader of
final answers and states the answer more often (every such statement was redacted). GLM scores
highest (65.6 %) but used a different student. Full write-up: `docs/TG_DATASETS.md`.

**Files.** `REPORT.md` and `comparison.json` from `scripts/compare_teachers.py`;
`per_question.jsonl` has every question's judge and rule-based outcome in each dataset.

**Protocol.** Judge Gemma-4-31B-it (all 7,999 × 3 episodes); datasets in `data/episodes*/`.

**Source.** `runs/compare_teachers/` in this repository, regenerated 2026-09-15.
