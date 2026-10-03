# E32 — Outcome-reward RL (GRPO) at self-guidance's compute

**Question.** Reinforcement learning with a verifiable reward is the other standard way to learn
from gold answers: sample episodes, reward the correct ones, push the policy toward them. No critic,
no hint, no teacher. At the compute Self-Guidance spends on its whole build, does it match it?

**Answer.** It beats it. Judge-correct accuracy (Gemma-4-31B-it) on the 747 held-out questions:

| Training | Build PFLOPs | Seeds | Per seed | Mean |
|---|---|---|---|---|
| **RL (GRPO, F1 reward), equal compute** | 1,474 | 3 | 71.0 / 67.7 / 68.9 | **69.2 ± 1.6** |
| **RL, twice the compute** | 2,948 | 3 | 72.0 / 70.3 / 70.2 | **70.8 ± 1.0** |
| Self-guided (E25) | 1,474 | 6 | 66.7 / 64.9 / 63.2 / 63.6 / 64.9 / 65.2 | 64.8 ± 1.2 |
| Unguided self-rollouts (E25) | 859 | 6 | 62.3 / 64.8 / 62.6 / 62.0 / 60.6 / 62.4 | 62.5 ± 1.4 |
| *Teacher's own rollouts (E24), for reference* | 2,233 | 3 | 71.8 / 72.3 / 69.2 | 71.1 ± 1.6 |
| Base student | — | — | 27.3 | 27.3 |

Seed-averaged paired test, bootstrap 95 % CI, sign-flip p; Holm over the two primary contrasts:

| Contrast | Δ | 95 % CI | p | Holm |
|---|---|---|---|---|
| self-guided → RL, equal compute (primary) | **+4.5** | +2.1 to +6.8 | 0.0002 | 0.0002 |
| unguided → RL, equal compute (primary) | **+6.8** | +4.2 to +9.4 | 0.0001 | 0.0002 |
| self-guided → RL, twice the compute | +6.1 | +3.6 to +8.5 | 0.0001 | — |
| RL equal → RL twice the compute | +1.6 | −0.1 to +3.3 | 0.072 | — |

RL is ahead of self-guided data at every seed (+4.3, +2.8, +5.8 at equal compute) and on every
dataset. At twice the compute it reaches the level of the 284B teacher's own rollouts (70.8 vs
71.1, E24) with no teacher at all. This is the second pre-stated outcome in
`experiments/exp32_rl/README.md`: *outcome-reward RL is at least as good a use of the answers, and
the paper must say so; Self-Guidance's case then rests on needing no RL infrastructure.*

**Not an artefact of the judge or the answer form.** The RL student answers in one word (median),
the self-guided student in about twenty, so string metrics that reward brevity (exact match, F1)
are not comparable. The lenient string test, which does not penalise length, agrees with the
judge: cover match 63.6–67.2 % for the RL seeds against 60.6–63.2 % for the self-guided ones. The
judge accepts answers the string test rejects about equally often for both (35–38 vs 38–42 per
seed) and rejects string-test passes less often for RL (5–7 vs 16–19). Per dataset, RL at equal
compute (mean of seeds) against self-guided (seeds 13/17/23): 2WikiMultihopQA 85.9 vs 76.6,
HotpotQA 70.2 vs 67.4, MuSiQue 48.8 vs 46.5, StrategyQA 75.3 vs 71.9.

**Cheaper at inference too.** 3,774 tokens and 2.81 steps per question against 5,176 and 2.89; it
ends 18.9 % of episodes itself, against 10.8 %.

**How the run went.** Each round samples 32 questions × 8 episodes from the current policy under
the evaluation protocol and takes one GRPO step (F1 reward, group-normalised advantage, no KL). The
dev questions (held back from training, evaluated greedily under the evaluation protocol) went
from F1 0.13–0.14 for the base student to 0.53–0.58 at the round-15 gate and 0.65–0.68 by the end;
every seed passed the gate. Equal compute was reached after 81–104 rounds (6.3–6.9 hours of
rounds on one L40/A100 GPU, the vLLM server and the trainer sharing it), twice the compute after
164–229 rounds (11.5–13.0 hours). Self-Guidance's collection took 12.5 hours on one 48 GB GPU plus
2.9 GPU-hours of training.

**What it took.** Two earlier versions failed, and both are documented in
`experiments/exp32_rl/README.md` and kept as arms here:
- *v1, cover-match reward (`rlcover`):* reward-hacked -- verbose answers that contain the gold
  string -- then collapsed: 0.0 / 0.0 / 9.1 % judge-correct at equal compute.
- *v2, F1 reward, rollouts in the collection harness (`rlharness`):* learned under the harness's
  finish-only final-step grammar and never learned to finish on its own: 0.4 / 5.5 %.
v3 samples under the evaluation protocol, keeps truncated calls in the loss, and gates on a dev
evaluation at round 15. Self-Guidance needed none of this: it is supervised fine-tuning with the
same recipe as every other route.

**Protocol.** `experiments/exp32_rl/rl_grpo.py --rollout eval --reward f1` (lr 2e-5, LoRA rank 32,
32 × 8 episodes per round, temperature 1.0, 700-token cap, 3 steps); prompts checked token for
token against vLLM's counts; the loss-path check compares selected-position log-probabilities with
a full forward pass (difference 0 to 6e-8). Compute counted as in E23 (collection 2 × 3.4B ×
tokens, training 6 × 3.4B × tokens); dev evaluations are not counted. Pool tasks `e32c_smoke`,
`rl3_s{13,17,23}`, `eval_rl3_c{1,2}_s*`, `judge_*`, `results_E32`.

**Files.** `kit/summary.txt`/`.json` (all arms and tests), `kit/results.json`/`RESULTS.md`,
`kit/rl_curves.txt`/`.json`, `kit/rl_log_*.jsonl` (every round of every run, v1-v3),
`kit/dev_log_rl3_s*.jsonl` (the dev evaluations).

**Caveats.** Three seeds per RL arm. In domain; the external benchmarks are queued
(`evalnew_*_rl3`, `results_E32new`). One RL configuration, not tuned; a stronger one could only
widen the gap. RL starts from the base student; starting it from a self-guided student was not
tried.
