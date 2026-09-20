# exp23 — What each route costs end to end

**Why.** Accuracy comparisons hide that the routes differ in what they consume: a teacher-guided
collection runs a 284B-parameter critic on every step, plain distillation runs the teacher as the
agent, and Self-Guidance runs only the student. The paper's cost table covers inference and
collection per episode; this makes the whole pipeline explicit and general, so the numbers
transfer to other hardware and other models.

**What it reports** (`pipeline_cost.py`):
- **Collection:** episodes, input and output tokens per episode, separately for the actor and the
  critic, and PFLOPs per episode ($\approx 2 \times$ active parameters $\times$ tokens).
- **Filter:** what each filter keeps, and what the filter itself costs (a string match is free; an
  LLM judge costs tokens on every episode collected).
- **Build:** what it costs to reach the same number of usable training episodes, which is where a
  low keep rate hurts: collection + filter + training compute.
- **Models:** total and active parameters, so memory and compute can be re-derived elsewhere.

Inference cost per question and accuracy come from the evaluation tables (Table 7 of the paper).

**Run.** Pool task `e23_pipeline_cost` (CPU).
