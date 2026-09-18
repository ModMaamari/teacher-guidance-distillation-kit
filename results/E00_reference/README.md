# E00 — Reference: four arms on the held-out questions

**Question.** Does training a small student on teacher-guided episodes lift it, and how does it
compare with the same student guided live and with the teacher alone?

**Answer.** Yes. Judge-correct on 747 held-out questions: base student 29.8 %, guided student
60.5 %, trained student 65.5 %, teacher alone 72.3 %. Base → trained is +35.6 points
(95 % CI +31.7 to +39.4); the trained student beats live guidance by 5.0 points (CI 1.6 to 8.3)
and trails the teacher by 6.8 (CI 3.4 to 10.3). Numbers: `results.json`; readable report:
`report.md`; kit write-up: `docs/RESULTS.md` (group B).

**Protocol.** Student `ibm-granite/granite-4.1-3b` (LoRA on the uniform split, one seed); teacher
DeepSeek-V4-Flash-0731 for the guided and teacher arms; budget 3, hidden; greedy student decoding;
judge Kimi-K2.6 (28 of the base arm's verdicts came from a fallback judge). Test set: the 747
held-out questions (HotpotQA 189, 2WikiMultihopQA 170, MuSiQue 203, StrategyQA 185).

**Source.** Produced in the research workspace (`training_methods/m1_lodo/runs/uniform`, trained
and guided arms 2026-09-02; base and teacher arms from the `lodo` run, E13). Raw episodes, verdicts
and the adapter stay there; this folder holds the final numbers with provider prefixes removed.

**Caveats.** One seed (E02). A different judge from E15/E16 (re-judging with Gemma-4-31B-it is
the registry's next step). The adapter was trained through the loss path later fixed (E14); greedy
results are unchanged by that fix.
