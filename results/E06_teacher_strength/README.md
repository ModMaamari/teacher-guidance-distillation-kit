# E06 — Teacher strength

**Question.** Does the student need a strong teacher? Train the same student on episodes collected
with a strong teacher, a different teacher, and itself as teacher.

**Answer.** No. The self-taught student is the best of the three. Judge-correct on the 747
held-out questions, student `granite-4.1-3b`:

| Training episodes collected with | Training examples | Judge-correct | Δ vs base [95 % CI] |
|---|---|---|---|
| — (base student) | — | 27.3 % | — |
| DeepSeek-V4-Flash as teacher (E02 seed 13) | 14,458 | 62.1 % | +34.8 [+30.8, +38.7] |
| GLM-5.3-flash as teacher (student granite-4.2-3b) | 13,556 | 64.3 % | +37.0 [+33.1, +40.8] |
| The student itself as teacher | 13,825 | 66.7 % | +39.4 [+35.5, +43.4] |

Self-taught vs DeepSeek-taught: +4.5 points (CI +1.2 to +7.9, McNemar p 0.010), about 16 times
E02's seed SD. GLM-taught sits between them and differs from neither significantly (+2.1 vs
DeepSeek, p 0.24; −2.4 vs self, p 0.17). The three training sets are within 7 % of each other in
size, so size does not explain the order. Table: `kit/RESULTS.md`, `kit/table.tex`.

**What this means for the paper.**
- A stronger teacher does not give a better student here, which fits E15: at collection time the
  self-taught and DeepSeek-taught episodes were equally often correct.
- Whether guidance matters at all, or only the correct trajectories, is E01's question. Read the
  two together.

**Protocol.**
- **Episodes.** From E15: the same 7,999 questions under three teachers. The GLM set was collected
  with a different student (granite-4.2-3b); the other two with granite-4.1-3b.
- **Splits.** Built with `scripts/build_splits.py`.
- **Training and evaluation.** Same recipe, evaluation and judge as E02.
- **Pool tasks.** `prep_self`, `prep_glm`, `train_selftaught`, `train_glmtaught`, `eval_*`,
  `judge_*`, `results_E06`.

**Caveats.**
- One seed per arm.
- The GLM arm changes two things at once (teacher and collecting student).
- The planned Mistral-family teachers were not run.

## History

- **2026-09-18:** students trained and evaluated (pool). Before this, only the collection-side
  comparison (E15) existed.
