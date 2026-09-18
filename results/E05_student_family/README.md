# E05 — A second student family

**Question.** Does the method work for a small student from another model family?

**Answer.** Yes. `openbmb/MiniCPM5-2B` (Llama architecture, 2B), trained on the same episodes,
reaches 64.7 % judge-correct on the 747 held-out questions. That is on par with the Granite-4.1-3B
reference (62.1 %; difference +2.5 points, CI −0.8 to +5.9, p 0.17).

| Student | Base | Trained | Δ [95 % CI] |
|---|---|---|---|
| Granite-4.1-3B (reference, E02 seed 13) | 27.3 % | 62.1 % | +34.8 [+30.8, +38.7] |
| MiniCPM5-2B | 2.4 % | 64.7 % | +62.3 [+58.8, +65.7] |

**Read the MiniCPM lift with care.** The untrained MiniCPM plans and searches, but it never ends an
episode with the finish action in 728 of 747 episodes and answers "unknown". Its 2.4 % therefore
measures the agent protocol more than its knowledge, and most of its +62.3 is the protocol being
learned. The informative comparison is trained vs trained, where the smaller model from another
family matches the reference. Table: `kit/RESULTS.md`, `kit/table.tex`.

**Protocol.**
- **Training.** Same split (`data/splits/uniform`, 14,458 examples, collected with the Granite
  student and the DeepSeek teacher) and the same recipe as E02, with `--health-every 200`.
- **Evaluation.** The base and trained MiniCPM arms were served by one vLLM server, so the adapter
  is the only difference. Greedy, budget 3, judge Gemma-4-31B-it.
- **Pool tasks.** `train_e05`, `eval_e05`, `judge_e05`, `results_E05`.
- **Scope.** One extra student only, by the plan's scope. The other five probed candidates were
  not run.

**Caveats.** One seed. The training episodes were written by a different student (Granite), so
MiniCPM learns from another model's trajectories.

## History

- **2026-09-18:** first run (pool).
