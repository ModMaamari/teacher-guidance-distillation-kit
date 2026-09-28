# exp31 — STaR: the student's correct attempts plus answer-hinted rationalizations

**Why.** Self-Guidance uses the gold answer to *critique* the student's steps. The best-known way
to use gold answers for self-training is STaR (Zelikman et al., 2022): keep the model's own correct
attempts, and for the questions it got wrong, show it the answer as a hint and keep the hinted
attempts that end correct, with the hint removed from the training input ("rationalization").
Reviewers will ask for it: it uses exactly the same privileged information, with no critic.

**Design.** Everything as in the self-guided and unguided routes (same 7,999 questions, same
harness, three-step budget, same LoRA recipe, correctness by cover match):

- *Attempt.* One unguided episode per question (iteration 1 reuses E25's `data/episodes_selfdist`).
- *Rationalize.* For every trainable question the attempt failed, one more episode in which the
  student's step prompts carry `Answer hint (the known correct answer): "<gold>"`
  (`collect_episodes.py --answer-hint`). The plan prompt is not hinted.
- *Train.* Correct attempts + correct rationalizations, the hint stripped from every input
  (`tgd.episode_lib`). A hinted step is kept only if nothing it wrote -- thought, query, extracted
  facts, final answer -- names the answer before retrieved documents do; the student's own earlier
  outputs do not count as evidence. This is stricter than STaR, which keeps any rationale that
  reaches the answer.
- *Iterate.* STaR repeats with the newest model and retrains from the base model each time.
  Iteration 2 collects attempts and rationalizations with iteration 1's seed-13 model (merged).

| Arm | Data from | Seeds |
|---|---|---|
| `star1` (STaR, 1 iteration) | base model's attempts + its rationalizations | 13, 17, 23 |
| `star2` (STaR, 2 iterations) | `star1_s13`'s attempts + its rationalizations | 13, 17, 23, 29, 31, 37 |

Compared with the six self-guided and six unguided students of E25; primary contrasts
`star2 -> self-guided` and `unguided -> star2`, Holm over the two; compute measured as in E23/E30.

**What each outcome means, written before the runs.**
- *Self-guided > STaR:* critiquing with the answer is a better use of it than hinting it; the paper
  can say so against the standard baseline.
- *STaR ≈ self-guided:* the gold answer helps, and how it is delivered does not matter much; the
  paper must present Self-Guidance as one of several equivalent ways, and compare cost.
- *STaR > self-guided:* the simpler method wins, and the paper's contribution narrows to the
  analysis.

**Run.** Pool tasks `e31_smoke` (a few hinted episodes checked end to end), `collect_star1_rat`,
`prep_star1`, `train_star1_s*`, `merge_star1`, `collect_star2_att`, `prep_star2q`,
`collect_star2_rat`, `prep_star2`, `train_star2_s*`, `eval_*`, `judge_*`, `results_E31`.
