# E17 — Is self-guidance better than no guidance?

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

**Answer (full size): yes.** Each source with all its training episodes, seed 13:

| Trajectories (correct ones kept) | Usable episodes | Judge-correct |
|---|---|---|
| Student alone, no teacher (all) | 3,753 | 62.3 % |
| Student guided by DeepSeek-V4-Flash (all; E06) | 3,959 | 62.1 % |
| **Student guided by itself (all; E06)** | 3,818 | **66.7 %** |

Paired differences:
- self-guided vs unguided: +4.4 (95 % CI +1.7 to +7.2, McNemar p 0.003)
- self-guided vs DeepSeek-guided: +4.5 (CI +1.2 to +7.9, p 0.010)
- DeepSeek-guided vs unguided: −0.1 (CI −3.2 to +2.9, p 1.0)

At both sizes a strong teacher's critique adds nothing to the student's own filtered rollouts,
while self-critique with the answer key adds 3 to 4 points. Table: `full/RESULTS.md`.

**Sensitivity.** E18 re-grades every arm with a strict single-answer rubric and two other judges:
- **Full size (+4.4):** significant under all four.
- **Matched size (+3.2):** positive under all four (+2.3 to +3.2) but significant only under the
  primary judge (p 0.03; others p 0.06 to 0.13).

E19 finds a self-guided seed SD of 1.7 points, larger than the teacher-guided 0.3 (E02), so these
single-seed comparisons carry more seed noise than E02 suggested.

**Protocol.** The self-taught episodes (E15) were cut to E01's matched usable count with the same
nested cutter (`prep_e17`). Training, evaluation and judge are identical to E01. Pool tasks
`prep_e17`, `train_sup_selftaught`, `eval_sup_selftaught`, `judge_sup_selftaught`, `results_E17`.

**Caveats.** One seed per arm. Self-guided seeds vary by SD 1.7 points (E19). The matched +3.2 is
significant only under the primary judge.

## History

- **2026-09-18:** matched-size arm (pool).
- **2026-09-19:** full-size unguided arm (`selfdist_full`); sensitivity from E18 and E19 added.
