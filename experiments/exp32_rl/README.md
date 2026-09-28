# exp32 — Outcome-reward RL (GRPO) at Self-Guidance's compute

**Why.** Reinforcement learning with a verifiable reward is the other standard way to learn from
gold answers: sample episodes, reward the correct ones, and push the policy toward them. It needs
no critic and no hint. If it matches Self-Guidance at equal compute, the critique is not needed;
if it trails, Self-Guidance is the more sample-efficient use of the same answers.

**Design.** GRPO from the base student (`rl_grpo.py`), on the same harness, questions (the 7,252
trainable ones), step budget and LoRA configuration (rank 32, alpha 64) as every SFT route:

- Each round: 32 questions × 8 episodes sampled from the current policy at temperature 1.0,
  through `collect_episodes.py --no-teacher` with the policy served by vLLM as a LoRA adapter.
- Reward 1 if the final answer passes the cover match (the test every SFT route filters on), else 0.
  Advantage `(r - group mean) / (group std + eps)`; groups with no variance are skipped.
- One on-policy gradient step per round on every student call of every episode (plan, steps,
  repairs), on the exact prompt the policy saw and the text it sampled; token-level loss
  normalisation, no KL term, AdamW lr 5e-5, gradient clipping 1.0.
- Compute counted as in E23: collection 2 × 3.4B × tokens, training 6 × 3.4B × trained tokens.
  The adapter is published at **1,474 PFLOPs** (`rl_c1`, Self-Guidance's whole build) and at
  **2,948** (`rl_c2`, twice that), so RL is compared at equal compute and given a second chance
  at double.

Three seeds (13, 17, 23). Compared with the six self-guided and six unguided students of E25;
primary contrasts `rl_c1 -> self-guided` and `unguided -> rl_c1`, Holm over the two.

**What each outcome means, written before the runs.**
- *Self-guided > RL at equal compute:* critique-guided data is the more compute-efficient use of
  gold answers than outcome reward, for this student and budget. If RL at double compute also
  trails, the claim is strong.
- *RL ≈ or > self-guided:* outcome-reward RL is at least as good a use of the answers, and the
  paper must say so; Self-Guidance's case then rests on needing no RL infrastructure.

**Limits, stated up front.** One configuration (batch, group size, learning rate) was chosen from
common practice, not tuned; RL typically needs more updates than SFT, which the 2× checkpoint
partly addresses. Training starts from the base student, not from an SFT model.

**Run.** Pool tasks `e32_smoke` (two tiny rounds end to end), `rl_s{13,17,23}` (resumable by
round), `eval_rl_c{1,2}_s*`, `judge_*`, `results_E32`. Curves: `runs/rl/rl_s*/rl_log.jsonl`.
