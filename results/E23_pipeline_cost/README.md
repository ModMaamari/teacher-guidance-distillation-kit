# E23 — What each route costs end to end

**Question.** Accuracy tables hide that the routes consume very different amounts of compute: a
teacher-guided collection runs a 284B-parameter critic on every step, plain distillation runs the
teacher as the agent, and Self-Guidance runs only the student. What does each route cost from
collection through filtering and training?

**Answer.** Self-guided collection costs about a third of teacher-guided collection per episode and
about three times a plain unguided student rollout. Compute in PFLOPs (collection and filter:
2 × active parameters × tokens, counted call by call; training: the trainer's own counter):

| Route | Collection PF/episode | Build as run: collect + train = total PF |
|---|---|---|
| Student's own rollouts, unguided | 0.032 | 258 + 602 = 859 |
| **Self-guided (ours)** | **0.099** | **790 + 684 = 1,474** |
| Teacher-guided (DeepSeek critic) | 0.284 | 2,271 + 720 = 2,991 |
| Teacher-guided (GLM critic) | 0.270 | 2,157 + 660 = 2,817 |
| Teacher's own rollouts, all 7,999 questions | 0.187 | 1,509 + 724 = 2,233 |

Normalised to the same 3,818 usable episodes, self-guidance totals 1,395 PF against 2,661 (DeepSeek
critic), 2,454 (GLM critic), 1,602 (teacher rollouts) and 921 (unguided self-rollouts). An LLM-judge
filter would add about 0.0155 PF per episode judged; the cover-match filter costs nothing.

**Protocol.** `experiments/exp23_pipeline_cost/pipeline_cost.py` walks every model call in every
collected episode, including critic and plan-review calls, and prices tokens with each model's
active parameter count. `actual_build.py` prices each trained student as it was actually built
(episodes collected, including the 747 held-out questions that are priced but never trained on;
training FLOPs from the trainer). Pool task `e23_pipeline_cost` (CPU).

**Files.** `kit/pipeline_cost.txt`/`.json` (collection, filter, normalised build),
`kit/actual_build.txt`/`.json` (build as run, with the seeds behind each route).

**Caveats.** FLOP counts are the 2·N·tokens approximation and ignore attention and prefix-cache
reuse; wall-clock and energy depend on the serving stack and are not reported. The route costs do
not include inference, which is in the paper's efficiency table.

**History.** The first version missed the plan-review calls and undercounted collection (fixed
2026-09-20, commit 4b9c6a0). The build-as-run table was added on 2026-09-25.
