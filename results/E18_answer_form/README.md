# E18 — Does answer form move the ranking?

**Question.** Students trained on the student's own trajectories answer in about 20 words (median),
DeepSeek-guided ones in 2. Does that verbosity inflate the primary judge, or do the comparisons
hold under a strict rubric and other judges?

**Answer.** The main result holds. Every arm of E01, E06 and E17 was re-graded four ways:
- **primary:** Gemma-4-31B-it, the standard prompt
- **strict:** the same judge with a rubric that rejects hedged or multi-candidate answers
- **kimi, qwen:** Kimi-K2.6 and Qwen3.6-35B with the standard prompt

The strict rubric moves every arm by at most 1.4 points (self-guided 66.7 → 66.0 %, DeepSeek-guided
62.1 → 62.0 %), so verbosity is not buying accuracy.

| Comparison (seed 13) | primary | strict | kimi | qwen |
|---|---|---|---|---|
| self-guided vs DeepSeek-guided, all data | +4.5 (p 0.010) | +4.0 (p 0.022) | +3.9 (p 0.033) | +4.6 (p 0.010) |
| self-guided vs unguided, all data | +4.4 (p 0.003) | +4.7 (p 0.001) | +3.4 (p 0.031) | +4.3 (p 0.005) |
| self-guided vs unguided, matched | +3.2 (p 0.031) | +2.7 (p 0.072) | +2.3 (p 0.13) | +2.8 (p 0.062) |
| DeepSeek-guided vs unguided, matched | +0.8 (p 0.67) | +0.7 (p 0.74) | −0.1 (p 1.0) | +0.3 (p 0.93) |
| teacher rollouts vs self-guided, matched | +3.1 (p 0.073) | +3.8 (p 0.026) | +3.5 (p 0.042) | +3.4 (p 0.046) |

**Reading.** At full size, self-guided beats DeepSeek-guided and unguided trajectories under every
grader. At matched size the self-guided advantage over unguided keeps its sign under every grader
but is significant only under the primary one, so it should be reported as consistent but modest.
The teacher's own rollouts beat self-guided ones under three of four graders. Full report with
accuracies, CIs and median answer lengths: `kit/report.md` (`kit/report.json`).

**Protocol.** `experiments/exp18_answer_form/report.py` over the verdicts of the four graders.
Paired differences use a bootstrap 95 % CI and an exact McNemar test over the 747 held-out
questions. Qwen left one or two answers per arm unresolved (746 judged). Pool tasks
`judge_e18_strict`, `judge_e18_kimi`, `judge_e18_qwen`, `e18_report`.

**Caveats.** One training seed per arm; self-guided seed SD is 1.7 points (E19).

## History

- **2026-09-19:** first run (pool).
