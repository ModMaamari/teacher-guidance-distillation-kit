# exp08 — Does the result depend on the step budget?

**Tier 2.** Every reported number uses budget 3, hidden. That is one arbitrary point, and
it interacts directly with the paper's own diagnosis: the students' remaining gap to the
teacher is *stopping behaviour*, not retrieval (2-11 % voluntary finishes against 100 %,
doc recall 0.79 against 0.84). Budget is exactly the knob that governs stopping, so a
reviewer will ask what happens when you move it.

## Design

Evaluate the base and trained students, and the teacher, at budgets 1, 3, 5 and 8, on the
same held-out questions. Nothing is retrained; this is evaluation only.

## Run

```bash
export PARTITION=<gpu-partition>
BUDGETS="1 3 5 8" bash run.sh
bash run.sh judge
python summarize_budget.py --results runs/results/results.json
```

## What each shape means

- **Trained student gains with budget, teacher flat.** The student is using extra steps
  productively and the gap is a stopping problem, which supports your existing analysis.
- **Trained student flat, teacher gains.** The student cannot exploit more steps; the gap
  is planning, not stopping, and the paper's diagnosis needs revising.
- **Everything flat.** Budget 3 was already saturating. Say so; it retires the question in
  one sentence and justifies the original choice.

Report cost too. If accuracy rises with budget, the token count rises with it, and the
efficiency claim (0.43x the guided arm's tokens) is stated at budget 3.
