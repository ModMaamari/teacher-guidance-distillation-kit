# E08 — Does the conclusion depend on the 3-step budget?

**Question.** Every other table evaluates at a budget of 3 tool steps. Would more steps close the
gap between the base and the trained student, and how does the teacher scale?

**Answer.** No, and the base student is the reason: it does not use extra steps. Judge-correct
accuracy (Gemma-4-31B-it) on the 747 held-out questions, with steps used and total tokens per
question:

| agent | B=1 | B=3 | B=5 | B=8 |
|---|---|---|---|---|
| base Granite-4.1-3B | 0.5 % (1.00 / 1,419) | 27.3 % (2.97 / 5,067) | 28.1 % (4.89 / 8,939) | 26.2 % (7.74 / 14,923) |
| trained (DeepSeek-guided, seed 13) | 10.3 % (1.00 / 1,729) | 62.1 % (2.92 / 5,334) | 66.8 % (4.44 / 9,027) | 67.3 % (6.51 / 13,922) |
| teacher alone (DeepSeek-V4-Flash) | 60.0 % (1.00 / 4,766) | 82.7 % (2.89 / 7,231) | 85.0 % (4.21 / 10,055) | 85.8 % (5.64 / 13,358) |

**Reading.**
- The base student gains nothing past three steps: it spends the extra steps without committing to
  an answer (E10).
- The trained student gains +4.7 from three to five steps (Holm-corrected p 0.010, E12). No later
  step is significant for any agent.
- The teacher's +2.3 from three to five steps survives BH only.
- At one step the teacher still answers 60 % correctly while retrieving no documents (doc recall
  0 in `kit/RESULTS.md`). That is the knowledge a 284B-parameter model brings, not search behaviour.
- Tokens per question grow roughly linearly with steps for every agent.

`teacher_b3` (82.7 %) is the teacher-alone reference in the paper. It supersedes the 71.1 % of E00,
which ran with a 1,200-token output cap through another provider (see the E00 History).

**Protocol.** The same harness, test set and judge as E00, at budgets 1, 3, 5 and 8. The base and
trained students use greedy vLLM decoding. The teacher uses the same endpoint and 6,000-token
output limit as the teacher's own rollouts (E01, E17). Budget 3 reuses the E02 seed-13 and base
evaluations; the other budgets are pool tasks `eval_budget{1,5,8}` and `eval_teacher_b{1,3,5,8}`.
Summary: `experiments/exp08_step_budget/summarize_budget.py` (pool task `results_E08`).

**Files.** `kit/budget.txt` (the table above), `kit/figure_budget.csv` (Wilson 95 % intervals, the
paper's Figure 2 right), `kit/results.json` and `kit/RESULTS.md` (per test set, with EM, F1, doc
recall and latency).

**Caveats.** One training seed for the trained student. Teacher latency reflects a shared API
endpoint and is not comparable with local GPU latency.

## History

- **2026-09-19:** complete. The teacher arms were revived twice after endpoint outages
  (HTTP 500), then finished with the probe-and-wait added to `teacher_eval`.
