# E24 — Plain teacher distillation at the same scale as Self-Guidance

**Question.** At matched supervision (~1,400 episodes) the teacher's own rollouts train the best
student by a wide margin (E01, E21). Does that hold when both routes collect over **the same 7,999
questions**, where the teacher's higher success rate also gives it more usable episodes?

**Answer.** Yes, and by the same margin. Judge-correct accuracy (Gemma-4-31B-it) on the 747
held-out questions, three seeds each:

| Training trajectories | Episodes kept | Examples | Train PFLOPs | Seeds 13 / 17 / 23 | Mean |
|---|---|---|---|---|---|
| Self-guided (ours) | 3,818 | 13,825 | 684 | 66.7 / 64.9 / 63.2 | **64.9 ± 1.7** |
| **Teacher's own rollouts** | 5,533 | 15,805 | 724 | 71.8 / 72.3 / 69.2 | **71.1 ± 1.6** |

Seed-averaged **+6.2 points** for the teacher's rollouts (bootstrap 95 % CI +3.6 to +8.8,
permutation p 0.0001); per seed +5.1 (p 0.004), +7.4 (p < 0.001), +6.0 (p 0.0004). The matched-size
comparison of E21 gave the same +6.2, so the advantage is about whose actions are imitated, not
about the extra episodes.

**Reading.**
- **Imitating a capable model's own trajectories is the strongest lever in this project**, at both
  ~1,400 and ~5,500 episodes, on every seed.
- **It also wastes less collection.** On the same questions the teacher's episodes pass the
  correctness filter 76.4 % of the time against 53.0 % for self-guided ones, so one pass over the
  question set yields 5,533 usable episodes instead of 3,818.
- **What it costs** is a 284B-parameter model served for the whole collection, which must be able
  to solve the training questions; E23 prices the two routes end to end.
- The teacher-trained students also answer more briefly (median 14 words against 20) and finish
  voluntarily about as often.

**Protocol.** The teacher (DeepSeek-V4-Flash-0731) answers the same 7,999 questions with no critic,
budget 3, 6,000-token output limit; correct episodes become training data under the kit's usual
filters; three seeds of the same LoRA recipe; primary judge. Pool tasks `collect_teachdist_or`,
`prep_e24`, `train_teachdist_full_s{13,17,23}`, `eval_*`, `judge_*`, `results_E24`.

**One gateway.** The collection ran entirely through a single gateway
(`kit/provider_split.txt`: 7,999 episodes, one provider), after an earlier attempt through a
second gateway was discarded rather than mixed: two deployments of the same model id are not
interchangeable, as the appendix's teacher-reference note shows.

**Files.** `kit/summary.txt`/`.json`, `kit/train_cost.txt`/`.json`, `kit/results.json`/`RESULTS.md`,
`kit/split_teachdist.json`, `kit/provider_split.txt`.

**Caveats.** Three seeds per arm. The two arms differ in episode count by construction, which is
what collecting the same questions produces; E01 and E21 hold size constant and find the same gap.

## History

- **2026-09-21:** first run (pool). An earlier publication of this table pooled the held-out
  questions with a new benchmark, because views linked whole evaluation directories; views now
  select test sets explicitly and the numbers above come from the corrected run.
