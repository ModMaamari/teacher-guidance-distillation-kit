# E00 — Reference: four arms on the held-out questions

**Question.** Does training a small student on teacher-guided episodes lift it, and how does it
compare with the same student guided live and with the teacher alone?

**Answer.** Yes. Judge-correct on the 747 held-out questions, judged by Gemma-4-31B-it: base
student 27.2 %, guided student 56.2 %, trained student 63.3 %, teacher alone 71.1 %. Base → trained
is +36.1 points (95 % CI +32.3 to +39.9, McNemar p < 1e-6). The trained student beats live
guidance by 7.1 points (CI +3.8 to +10.4, p = 6e-5) and trails the teacher by 7.8 (CI 4.3 to
11.2). Numbers: `gemma/results.json`, table: `gemma/RESULTS.md`.

**Protocol.** Student `ibm-granite/granite-4.1-3b` (LoRA on the uniform split, one seed); teacher
DeepSeek-V4-Flash-0731 for the guided and teacher arms; budget 3, hidden; greedy student decoding;
judge Gemma-4-31B-it (FP8) with the same model on a second endpoint as fallback; the judge sees
only question, gold answer and final answer. Test set: the 747
held-out questions (HotpotQA 189, 2WikiMultihopQA 170, MuSiQue 203, StrategyQA 185).

**Source.** Produced in the research workspace (`training_methods/m1_lodo/runs/uniform`, trained
and guided arms 2026-09-02; base and teacher arms from the `lodo` run, E13). Raw episodes, verdicts
and the adapter stay there; this folder holds the final numbers with provider prefixes removed.

**Caveats.** One seed (E02). The adapter was trained through the loss path later fixed (E14);
greedy results are unchanged by that fix. Voluntary finishes, by the kit's definition (`finish`
or `teacher_accept`): base 2.4 %, guided 4.6 %, trained 11.0 %, teacher 24.0 % (E10).

## History

- **2026-09-19: teacher arm superseded as the reference.** This teacher arm ran through another
  provider with the harness default of 1,200 output tokens per call (3,889 tokens per question,
  71.1 %). The kit's teacher-alone run under the protocol of the teacher's own rollouts (E08,
  budget 3, 6,000-token limit) scores 82.7 % at 7,231 tokens per question; 16 % of its step calls
  exceed 1,190 tokens. The paper uses 82.7 % as the teacher-alone reference. The comparisons in
  this folder are unchanged.
- **2026-09-18: re-judged with Gemma-4-31B-it**, the judge of every other table (E16 picked it).
  Episodes were imported unchanged from the research workspace
  (`experiments/exp00_reference/import_runs.py`) and judged by the pool task `judge_e00`. The
  arm ranking is unchanged, and the three pooled comparisons keep their sign and significance:
  base → trained +36.1 (Kimi +35.6), guided → trained +7.1 (+5.0), trained vs teacher −7.8
  (−6.8). Accuracy is 1–4 points lower in every arm: base 27.2 vs 29.8 %, guided 56.2 vs 60.5 %,
  trained 63.3 vs 65.5 %, teacher 71.1 vs 72.3 %.
- **2026-09-02: first judged with Kimi-K2.6**, 28 base-arm verdicts from a fallback judge. Kept as
  `results.json` and `report.md` in this folder, superseded by `gemma/`.
