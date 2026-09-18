# E10 — Stopping behaviour

**Question.** How much accuracy does late stopping cost?

**Answer.** A lot for the untrained student, little for the others. Episodes the agent ends
itself are far more often correct than episodes the budget ends, but only a minority end that
way. Judge-correct by stop reason on the 747 held-out questions (Gemma-4-31B-it):

| Arm | voluntary finish | correct when voluntary | correct when budget-forced, answer given | correct when budget-forced, no answer |
|---|---|---|---|---|
| base student | 2.4 % (18) | 83.3 % | 74.1 % (174) | 10.6 % (555) |
| guided student | 4.6 % (34, teacher accepted) | 100 % | 54.1 % (713) | — |
| trained student | 11.0 % (82) | 81.7 % | 62.4 % (630) | 37.1 % (35) |
| teacher alone | 24.0 % (179) | 94.4 % | 63.7 % (568) | — |

The base student's failure is mostly not stopping at all: 74 % of its episodes run out of budget
without a `finish` action, and those are right 10.6 % of the time. Training removes most of
that (4.7 % left). The remaining gap to the teacher is not in forced answers (62.4 vs 63.7 %
correct) but in voluntary stops: the teacher ends 24 % of its episodes itself and is then right
94 % of the time, the trained student 11 % at 82 %. Output: `kit/stopping_e00.txt`.

**Protocol.** `experiments/exp10_stopping_behavior/analyze_stopping.py` on the E00 episodes
(`runs/e00/eval`) with the Gemma verdicts (`runs/judge/e00`). Voluntary = the episode ended
before the budget did (`finish`; for the guided arm and the teacher-alone records,
`teacher_accept`, the harness's name for an accepted finish). Pool task `e10_stopping`.

**Caveats.** Stop reasons are the harness's labels. The teacher arm was collected as
teacher-guidance records with no teacher in the loop, where an agent's own finish is recorded
as `teacher_accept`. Step 2 of the plan (closing the gap by decoding or targeted supervision)
was not run.

## History

- **2026-09-18:** first run. The script had three bugs, fixed first: it read the list of step
  records as the step count and crashed; it would have matched no verdict, silently falling back
  to cover-match; and it counted budget-forced finishes as voluntary. Earlier docs gave the
  teacher's voluntary-finish rate as 100 %. On the same episodes, the kit's metric
  (`tgd/metrics.py`) and this script both give 24.0 %.
