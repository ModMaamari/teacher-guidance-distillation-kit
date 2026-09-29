# exp32 — Outcome-reward RL (GRPO) at Self-Guidance's compute

**Why.** Reinforcement learning with a verifiable reward is the other standard way to learn from
gold answers: sample episodes, reward the correct ones, and push the policy toward them. It needs
no critic and no hint. If it matches Self-Guidance at equal compute, the critique is not needed;
if it trails, Self-Guidance is the more sample-efficient use of the same answers.

**Design.** GRPO from the base student (`rl_grpo.py`), on the same harness, questions (the 7,252
trainable ones), step budget and LoRA configuration (rank 32, alpha 64) as every SFT route:

- Each round: 32 questions × 8 episodes sampled from the current policy at temperature 1.0,
  through `collect_episodes.py --no-teacher` with the policy served by vLLM as a LoRA adapter.
- Reward: token F1 of the final answer against the gold answer. Advantage
  `(r - group mean) / (group std + eps)`; groups with no variance are skipped.
- One on-policy gradient step per round on every student call of every episode (plan, steps,
  repairs), on the exact prompt the policy saw and the text it sampled; calls cut off at the
  token limit are left out; token-level loss normalisation, no KL term, AdamW lr 2e-5, gradient
  clipping 1.0.
- Compute counted as in E23: collection 2 × 3.4B × tokens, training 6 × 3.4B × trained tokens.
  The adapter is published at **1,474 PFLOPs** (`rl2_c1`, Self-Guidance's whole build) and at
  **2,948** (`rl2_c2`, twice that), so RL is compared at equal compute and given a second chance
  at double.

Three seeds (13, 17, 23). Compared with the six self-guided and six unguided students of E25;
primary contrasts `rl2_c1 -> self-guided` and `unguided -> rl2_c1`, Holm over the two.

**What each outcome means, written before the runs.**
- *Self-guided > RL at equal compute:* critique-guided data is the more compute-efficient use of
  gold answers than outcome reward, for this student and budget. If RL at double compute also
  trails, the claim is strong.
- *RL ≈ or > self-guided:* outcome-reward RL is at least as good a use of the answers, and the
  paper must say so; Self-Guidance's case then rests on needing no RL infrastructure.

**First version: rewarded by the cover match, and reward-hacked (2026-09-28/29).** The first
runs (`rl_s*`, now `runs/rl/rlcover_s*`) used the cover match -- the lenient string test every SFT
route filters on -- as the reward, with lr 5e-5. The policy learned to answer at length until some
phrase contained the gold string: on seed 13, exact match on the sampled episodes rose from 0.08
to 0.24 by round 10 and then fell to 0.00 by round 50 while the cover reward stayed at 0.5-0.7 and
the median answer grew from 10 to about 30 words. All three seeds then collapsed (gradient norms
of 70-200, rewards near 0, degenerate multi-thousand-token outputs). The checkpoints published at
1,474 PFLOPs score 0.0, 0.0 and 9.1 % judge-correct, below the untrained student's 27.3 %. Filtering
a fixed sample on a lenient test is harmless; optimising against it is not. The runs were stopped
and the design changed to the F1 reward above (verbosity lowers F1), with overlong filtering and a
lower learning rate. Every round now logs cover, exact match, F1 and answer length, so hacking would
show immediately. The collapsed checkpoints are reported as a secondary arm (`rlcover`).

**Limits, stated up front.** One configuration (batch, group size, learning rate) was chosen from
common practice, not tuned; RL typically needs more updates than SFT, which the 2× checkpoint
partly addresses. Training starts from the base student, not from an SFT model.

**Run.** Pool tasks `e32b_smoke` (two tiny rounds end to end), `rl2_s{13,17,23}` (resumable by
round), `eval_rl2_c{1,2}_s*`, `judge_*`, `results_E32`. Curves: `runs/rl/rl2_s*/rl_log.jsonl`.
First version: `e32_smoke`, `rl_s*` (cover reward), `eval_rl_c1_s*`.
