# Decoding stability — can the trained student be sampled?

A model can be excellent at greedy decoding and unusable when sampled. Greedy needs only the
*ranking* of the top token; sampling needs its *probability* to be right. Supervised fine-tuning
can preserve the first while destroying the second, and no greedy evaluation will ever show it.

This happened to the student shipped with this kit, and it is worth knowing about before you
train your own.

## What it looked like

Measured on 300 held-out teacher-guidance questions, budget 3:

| Temperature | Base cover | Trained cover | Trained invalid steps |
|---|---|---|---|
| 0 (greedy) | 23.3 % | **61.0 %** | 36 / 862 |
| 0.3 | 25.7 % | **0.0 %** | 899 / 900 |
| 0.7 | 24.7 % | 0.0 % | 900 / 900 |
| 1.0 | 26.7 % | 0.0 % | 900 / 900 |

The base model is indifferent to temperature. The trained student is excellent at greedy and
produces nothing usable at 0.3. On single-token multiple choice the cliff sits higher — fine at
0.3, half its accuracy gone by 0.5 — because an agent action is several hundred JSON tokens that
must *all* be right, and a per-token error rate that barely dents one token is fatal across
three hundred.

## Why

The next-token distribution at the position where the answer must start, measured on 200
out-of-distribution prompts and 200 in-distribution agent prompts:

| Model | OOD entropy | OOD top-1 | OOD mass on valid tokens |
|---|---|---|---|
| base | 0.09 | 0.96 | 100 % |
| trained (plain SFT) | **10.91** | **0.006** | **1.2 %** |
| trained with `--kl-coef` | 0.17 | 0.93 | 100 % |

The vocabulary is 100,352 tokens, so 10.9 nats is nearly uniform. The trained model still ranks
the correct token first — greedy works — but holds 0.6 % of the probability on it. Everything
else is spread across junk, and sampling draws from that.

The account is quantitative: the chance of sampling a valid answer, computed from the model's
own logits under the exact filtering the sampler applies, matches what generation actually does
to within a few points. It also explains why two inference stacks disagreed on identical
weights — `transformers` applies `top_k=50` by default and held 69 % format compliance, while
vLLM truncates nothing by default and held 7.5 %.

## Two things to do about it

### At inference: use relative truncation

Nucleus sampling keeps a fixed share of probability *mass*, which on a flat distribution admits
tens of thousands of tokens. Min-p sets its threshold relative to the top token, so it adapts.
On the agent task, at the same temperature:

| Decoding | Cover | Invalid steps |
|---|---|---|
| greedy | 61.0 % | 36 / 862 |
| T 0.3, **min-p 0.1** | **49.7 %** | **9 / 854** |
| T 0.3, nucleus 0.95 | 0.0 % | 899 / 900 |
| T 0.7, min-p 0.1 | 0.0 % | 900 / 900 |

`--min-p 0.1` is plumbed through `scripts/eval.py`. Two variables govern whether a damaged
checkpoint works: **the temperature must be low and the truncation must be relative**. Above
0.5 nothing helps.

### At training: regularise toward the base

`scripts/train_sft.py --kl-coef 0.05` pulls every completion token toward the frozen base
model's own distribution. The base distribution comes from the same weights with the adapter
switched off, so it costs one extra forward pass and no extra parameters.

`--kl-direction` decides what is penalised, and the choice matters more than the coefficient:

* **`reverse`** (default) — KL(student ‖ base), *mode-seeking*: penalises probability mass where
  the base has none, which is exactly the junk tail, while leaving the student free to sharpen
  on the correct token. This is the direction [MiniLLM](https://arxiv.org/abs/2306.08543) uses
  for LLM distillation and that RLHF/DPO use for their reference constraint.
* **`forward`** — KL(base ‖ student), *mass-covering*: penalises the student for withdrawing
  mass from anything the base found plausible. That fights the cross-entropy directly. Measured
  here at coefficient 0.1 it fixed the calibration completely (OOD top-1 0.006 → 0.934, stable
  at every temperature, and it forgot *less*: pooled general-benchmark gap 1.4 → 0.6 points) and
  cost most of the task: agent cover fell from 61 % to 29 %, barely above the untrained base.

So: forward KL is a documented way to trade the task away for calibration. Reverse KL is the
direction to start from. `--kl-mask-target` excludes the target token from the divergence
entirely, so only the shape of the alternatives is constrained.

Pick a coefficient by sweeping — 0.03 and 0.1 bracket the useful range — and read the trade-off
off the two numbers that matter: agent cover at greedy, and OOD top-1.

**What is measured and what is not.** The cliff itself, its mechanism, the decoder mitigations
and the forward-KL result above are all measured on this project's student. The reverse-KL
setting is argued from the objective and from the distillation literature, not yet measured
here — it is the obvious first experiment to run, and `docs/EXPERIMENTS.md` sets it up.

### And measure it during training

`--health-every 200 --health-temperature 0.7` samples a few held-out prompts during training and
logs how many parse. Its absence is why this failure reached evaluation unnoticed.

Be aware of its limits: on eight prompts it could not distinguish a healthy model from a
damaged one after 375 steps, while the distribution measurement separated them easily. Treat the
health check as a smoke alarm and `scripts/diag_distributions.py` as the instrument.

## Running the check

```bash
# everything below, on one GPU, for an adapter you have trained
sbatch -p <gpu-partition> slurm/eval_stability.sbatch runs/train/uniform/adapter trained
```

That merges the adapter, measures the distributions in and out of distribution, sweeps
temperature and truncation on MMLU, and runs the agent task under greedy, nucleus and min-p.
Individually:

```bash
.venv_train/bin/python scripts/merge_adapter.py --base <hf id> \
    --adapter runs/train/uniform/adapter --out runs/train/uniform/merged
.venv_train/bin/python scripts/diag_distributions.py \
    --models base=<hf id> trained=runs/train/uniform/merged --n 200 --out runs/diag
.venv_train/bin/python scripts/sweep_decoding.py \
    --models trained=runs/train/uniform/merged --n 100 --out runs/diag
.venv_train/bin/python scripts/diag_consistency.py \
    --model runs/train/uniform/merged --top-k 50    # predicted vs observed, validates the above
```

## What to check before trusting any fine-tune

1. **Never accept a model on greedy evaluation alone.** Greedy is the one setting that hides
   this failure completely.
2. **Look at the distribution, not only the loss.** Top-1 probability and entropy on
   out-of-distribution prompts are the sensitive instrument.
3. **If output collapses, lower the temperature before blaming the model.** And check whether
   your server truncates: vLLM applies no `top_k` by default, `transformers` applies 50.
4. **Sampling-based workflows are the ones at risk** — self-consistency, rejection sampling, RL
   rollouts. All of them would fail silently on a checkpoint like this.
