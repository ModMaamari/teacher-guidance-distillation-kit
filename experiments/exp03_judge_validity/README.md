# exp03 — Is the judge measuring what you say it is?

**Tier 1.** A single LLM judge carries every headline number in the paper. Three things a
reviewer will want, in order of how badly their absence hurts:

1. **Human agreement.** Does the judge agree with a person on a sample you can show?
2. **Judge swap.** Does the *ranking of arms* survive a different judge? Accuracy may move;
   the ordering must not.
3. **Length confound.** Judges reward longer, hedged answers. Your arms differ in verbosity
   (the base student rarely finishes voluntarily, the teacher always does), so this is a
   live risk, not a formality.

## Run

```bash
# 1. draw a blind, stratified sample for a human to label
python 01_sample_for_human.py --verdicts runs/judge/verdicts.jsonl --n 200 \
       --out runs/judge/human_sample.csv
#    fill in the 'human_correct' column by hand: 1, 0, or leave blank to skip

# 2. re-judge everything with two other judges
export PARTITION=<partition>
bash 02_judge_swap.sh

# 3. agreement, ranking stability, length confound
python 03_agreement.py --primary runs/judge/verdicts.jsonl \
       --swap runs/judge_swapA/verdicts.jsonl runs/judge_swapB/verdicts.jsonl \
       --human runs/judge/human_sample.csv
```

## The sample is blind by construction

`01_sample_for_human.py` writes the question, the gold answer and the model's answer, and
nothing else. No arm name, no judge verdict, no model identity, and the rows are shuffled.
That is what makes the resulting agreement number worth printing.

Stratification is by (arm, judge verdict) so both agreeing and disagreeing regions are
covered; with `--n 200` over four arms you get 25 per cell. Label at least 150 or the
kappa confidence interval will be too wide to mean anything.

## What to report

- Cohen's kappa, human vs primary judge, with n. Above 0.6 is defensible, above 0.8 strong.
- The arm ranking under each judge, side by side. Say plainly if it moves.
- Mean answer length by verdict. If correct answers are systematically longer, report it
  and note that the trained arm is not the most verbose, which defuses the objection.
