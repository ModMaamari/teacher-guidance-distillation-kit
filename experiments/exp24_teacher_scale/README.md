# exp24 — Plain teacher distillation at the self-guided scale

**Why.** The teacher's own rollouts train the best student per episode (E01: 67.7 % at ~1,400
usable episodes), but only 2,000 were collected because they run a 284B-parameter model as the
agent. Self-Guidance trains on 3,818. A reviewer will ask what plain distillation does with the
same number of usable episodes, which is the fair "normal distillation" baseline.

**Design.** Collect the teacher's own rollouts over **the same 7,999 questions as every other
collection** (2,000 per dataset), so the routes differ only in who produced the trajectories. At the
observed 78 % keep rate that yields about 6,200 usable episodes, against 3,818 for self-guided,
because the teacher fails far less often on the same questions. Then train three seeds and compare
with the self-guided students in accuracy and in end-to-end cost (E23): the teacher writes more
output tokens per episode and needs its 284B weights hosted, but wastes far fewer episodes.

Two comparisons follow, and they answer different questions. **Same questions collected** (this
experiment) is the practical one: given one pass over the question set, which route gives the
better student? **Same number of usable episodes** (E01/E21, ~1,400 each) controls for training-set
size and already shows the teacher's rollouts ahead by +6.2 points. Reporting only the first would
confound source with data volume, so the write-up gives both.

**One gateway, collected from scratch.** The first attempt extended the existing 2,000-episode
collection, but its gateway's DeepSeek deployment started returning HTTP 500 mid-run (the other
models it serves were unaffected), and finishing on a second gateway would have mixed two
deployments of the same model id inside one training set. The paper already documents a teacher
run whose accuracy moved when the provider and the token cap changed, so E24 instead collects all
1,250 questions per dataset fresh through the second gateway, in its own run directory
(`runs/collect_teachdist_or` -> `data/episodes_teachdist_or`). The original 2,000 episodes stay
untouched and remain the basis of E01's matched-size arm; the partial mixed episodes were moved out
of the way. `provider_split.py` runs over the new collection and is published with the results, so
the single-provider claim is checked rather than asserted.

**Run.** `collect_teachdist_or` (API, resumable), `prep_e24` (consolidate + build
`data/splits_teachdist_or`), `train_teachdist_full_s{13,17,23}`, `eval_*`, `judge_*`,
`results_E24`.
