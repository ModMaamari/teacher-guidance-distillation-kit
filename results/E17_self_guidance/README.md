# E17 — Is self-guidance better than no guidance? (partial)

**Question.** At matched size, do self-guided trajectories (the student critiques itself with the
gold answer in view) train a better student than the student's own unguided rollouts?

**Answer (matched size): yes, modestly.** With about 1,400 usable (correct) training episodes per
arm, judge-correct on the 747 held-out questions:

| Trajectories (correct ones kept) | Usable episodes | Examples | Judge-correct |
|---|---|---|---|
| — (base student) | — | — | 27.3 % |
| Student alone, no teacher (E01) | 1,429 | 5,291 | 61.5 % |
| Student guided by DeepSeek-V4-Flash (E01) | 1,401 | 5,236 | 62.3 % |
| **Student guided by itself, with the gold answer** | 1,417 | 5,265 | **64.7 %** |
| Teacher alone as the agent (E01) | 1,412 | 4,189 | 67.7 % |

Paired differences against the self-guided arm:
- vs unguided: +3.2 (95 % CI +0.4 to +6.0, McNemar p 0.031)
- vs DeepSeek-guided: +2.4 (CI −0.8 to +5.5, p 0.15)
- vs teacher rollouts: −3.1 (CI −6.3 to +0.1, p 0.07)

So self-critique with the answer key adds to the correctness filter, while a strong teacher's
critique does not (E01). Table: `kit/RESULTS.md`, `kit/table.tex`.

**Still running.** The student trained on all unguided self-rollouts (`selfdist_full`), which
compares with the self-guided student trained on all its data (66.7 %, E06) at full size.

**Protocol.** The self-taught episodes (E15) were cut to E01's matched usable count with the same
nested cutter (`prep_e17`). Training, evaluation and judge are identical to E01. Pool tasks
`prep_e17`, `train_sup_selftaught`, `eval_sup_selftaught`, `judge_sup_selftaught`, `results_E17`.

**Caveats.** One seed per arm (seed SD 0.3 points, E02). The +3.2 is significant at p < 0.05, but
its CI lower bound is +0.4.

## History

- **2026-09-18:** matched-size arm (pool).
