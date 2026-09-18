# E03 — Judge validity

**Question.** Does a human agree with the judge, and does the ranking of arms survive another
judge?

**Answer.** Yes on both counts. The primary judge (Gemma-4-31B-it) agrees with a human on 94.9 %
of 196 blind answers (Cohen's κ 0.898). Two other judges re-grading all 2,988 E00 answers agree
with it on 96.9 % (Kimi-K2.6, κ 0.937) and 98.4 % (Qwen3.6-35B, κ 0.968), and both give the same
ranking: teacher > trained > guided > base.

| Judge | Base | Guided | Trained | Teacher | Agreement with Gemma | κ |
|---|---|---|---|---|---|---|
| Gemma-4-31B-it (primary) | 27.2 % | 56.2 % | 63.3 % | 71.1 % | — | — |
| Kimi-K2.6 | 30.1 % | 60.9 % | 65.2 % | 73.0 % | 96.9 % (n = 2,988) | 0.937 |
| Qwen3.6-35B-A3B | 27.3 % | 56.8 % | 64.1 % | 71.4 % | 98.4 % (n = 2,987) | 0.968 |
| Human, blind sample | | | | | 94.9 % (n = 196) | 0.898 |

**Where the human and the judge disagree** (10 of 196): in 8 the judge accepted an answer the
human rejected, and 5 of those 8 are base-student answers. The judge is slightly lenient, and
most of that leniency lifts the base arm, so the reported gains over the base student are, if
anything, understated. Per-arm agreement: base 89.8 %, guided 96.0 %, teacher 95.7 %,
trained 98.0 %.

**Length.** Answers judged correct are 2.9 words longer on average (12.9 vs 10.0 words). Mean
answer length per arm: base 6.3, trained 7.0, guided 9.1, teacher 23.9 words. The trained student
beats the guided one with shorter answers, so a length preference cannot explain its lead.

Files: `agreement/agreement.txt` (the full report), `agreement/human_labels.csv` (the human
verdicts; `human_correct` is blank for "can't tell"), `agreement/human_labels.key.json` (which arm
and judge verdict each sample came from), `kit/swaps.txt` (the judge-swap report).

**Protocol.**
- **Sample.** `01_sample_for_human.py` drew 200 answers from the four E00 arms, stratified by
  (arm, primary verdict): 25 per cell, seed 7, shuffled.
- **Labelling.** Labelled blind in `label_app.html` (question, gold answer and model answer only;
  no arm, no verdict) against the judge's own rubric. 4 rows were marked "can't tell" and are left
  out.
- **Swap judges.** They saw the same prompt as the primary judge. Qwen left 2 answers unresolved
  after retries, so its agreement is on 2,987.
- **Analysis.** `03_agreement.py`; pool tasks `judge_e00_kimi`, `judge_e00_qwen`, `e03_swaps`,
  `e03_agreement`.

**Caveats.**
- One annotator.
- The human sample is balanced 50/50 on the judge's verdict by design, which is not the
  population rate, so its κ describes agreement on a deliberately hard-to-guess mix.
- The rough 95 % band on the human κ is ±0.14.

## History

- **2026-09-18:** human labels (one annotator, 200 answers) and two swap judges. Before this, only
  E16's 145 items existed, and those labels were assigned by the AI assistant, not a human.
