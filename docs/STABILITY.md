# Decoding stability — can the trained student be sampled?

A model can be excellent at greedy decoding and unusable when sampled. Greedy needs only the
*ranking* of the top token; sampling needs its *probability* to be right. A training/inference
mismatch can preserve the first while destroying the second, and no greedy evaluation will ever
show it.

This happened to a student trained with this kit. **The cause was a two-line configuration bug,
diagnosed only after a week of work that assumed it was a property of the objective.** The bug
is now guarded against in `scripts/train_sft.py`; this page documents the failure, the guard,
and — because the same signature can have other causes — how to measure it on your own model.

## The bug, first

Some architectures divide their logits by a constant before the softmax. Granite does, via
`config.logits_scaling` (10.0). TRL's memory-chunked cross-entropy (`loss_type="chunked_nll"`,
its default) bypasses the model's forward pass and applies its own scaling read from
`config.logit_scale` — a field Granite does not define, so it silently defaults to 1.0.

The result: training optimises logits **ten times larger** than the ones inference produces.
Dividing logits by a constant is monotonic, so the token *ranking* is untouched and greedy
decoding looks perfect. The *calibration* is destroyed, and sampling collapses.

Verified directly. Scoring one saved checkpoint two ways on the file its trainer evaluated:

| View of the same weights | Loss | Entropy |
|---|---|---|
| as inference produces them | 6.568 | 11.071 |
| logits multiplied back by 10 | **0.263** | **0.218** |
| what the training log recorded | **0.269** | **0.229** |

The training log is reproduced to within 0.007. A model trained identically but with
`loss_type="nll"` matches its own log with no adjustment (0.282 measured, 0.297 logged) — same
architecture, same config, opposite verdict. That control rules out the measurement itself.

**The guard.** `scripts/train_sft.py` now inspects the model config before training. If the
architecture rescales logits under a field TRL's chunked path does not read, it switches to
`loss_type="nll"` and says so; `--loss-type chunked_nll` on such a model is refused rather than
run. `--loss-type` overrides the choice if you need to. The chunked path is a memory optimisation, so the safe
path needs a smaller micro-batch and more accumulation — `docs/TRAINING.md` has the numbers.

## Using this with any student model

The bug was found on Granite, but nothing about it is Granite-specific: it happens whenever the
loss a trainer optimises is computed differently from the logits the model emits. Other
architectures rescale logits too (Gemma softcaps, Cohere scales), and the next one may use a
field name nobody has written down yet.

So the kit does not rely on recognising field names. Before training starts, it **measures the
invariant directly** on a real batch: compute the completion-token cross-entropy from the
model's own forward pass, compute the loss the trainer is about to optimise, and compare. If a
loss path reconstructs logits differently — for any reason, on any architecture — the two
numbers disagree and the run stops before spending a GPU-hour.

```
loss-path check: training loss 0.4131 matches the model's own forward pass 0.4129
                 -- training and inference agree
```

On the student here the mismatch showed as **1.47 against 13.06**, a 790 % disagreement against
a 2 % tolerance. The field-name check below still runs first, because it can name the cause and
fix it automatically; the measurement is what actually decides.

One limitation, worth knowing before you test it: the check compares losses, so it only sees a
transform that changes them. A *randomly initialised* model has near-uniform logits and scaling
them barely moves the cross-entropy, so the check reads clean on one. Fine-tuning always starts
from pretrained weights, so this matters only if you point it at noise.

## What is guarded, and where

You should not be able to hit this again by following the kit. `tgd/logit_scale.py` holds the
one implementation; these use it:

| Script | Guard |
|---|---|
| `train_sft.py` | **measures that the training loss matches the model's own forward pass, and refuses to start if not** — architecture-agnostic; also picks the safe loss path, refuses the unsafe one, rescales the micro-batch to fit, and logs the model's scaling |
| `merge_adapter.py` | verifies the merged config kept the base's scaling; **deletes the merged model and fails** if not, rather than leaving a silently-wrong checkpoint on disk |
| `diag_distributions.py`, `diag_position_profile.py`, `sweep_decoding.py`, `diag_consistency.py` | print the model's scaling next to every measurement |
| `eval.py` | prints it whenever it is about to sample a local checkpoint |

The diagnostics and the KL term all read `model(...).logits`, which is *post*-scaling — what
inference actually produces — so they measure the right thing by construction. vLLM applies the
scaling from the config too; that was confirmed here, since the broken model failed identically
under vLLM and under transformers.

Two habits matter more than any of the above. **Never evaluate only at greedy** — it cannot see
this class of bug. And run `--health-every 200` during training: sampling eight held-out prompts
would have caught this on the first run, hours in rather than a week later.

## What the fix bought

The same training run, same data, same hyperparameters and seed, with only the loss path
corrected. 300 held-out questions, budget 3:

| Decoding | Broken cover | Fixed cover | Fixed EM |
|---|---|---|---|
| greedy | 61.0 % | 61.0 % | 0.340 |
| T 0.7, nucleus | **0.0 %** | **59.7 %** | 0.333 |
| T 0.3, min-p 0.1 | 0.0 % | **61.7 %** | 0.330 |

**Greedy is unchanged to within a rounding error** — 61.0 % against 61.0 %, EM 0.340 against
0.343. That is the signature of the bug confirming itself: dividing logits by a constant cannot
reorder them, so greedy, which reads only the ranking, never noticed. Everything that samples
was destroyed, and is now fine. The next-token distribution went from entropy 10.9 with 1.2 % of
its mass on valid tokens to entropy 0.22 with 100 %.

The practical lesson is the uncomfortable one: **a greedy evaluation cannot detect this class of
bug at all.** Both models score identically on it. If the only number you look at is greedy
accuracy, a model with a badly broken output distribution is indistinguishable from a correct
one.

## What it looked like before the cause was known

Everything below was measured on the miscalibrated checkpoint. It is kept because the
*symptoms* are what you will see first, whatever the underlying cause — a genuinely
over-trained model, a bad merge, or a quantisation step can all present this way.

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

`scripts/train_sft.py --kl-coef 0.03` pulls every completion token toward the frozen base
model's own distribution. The base distribution comes from the same weights with the adapter
switched off, so it costs one extra forward pass and no extra parameters.

`--kl-direction` decides what is penalised:

* **`reverse`** (default) — KL(student ‖ base), *mode-seeking*: penalises probability mass where
  the base has none, which is exactly the junk tail, while leaving the student free to sharpen
  on the correct token. This is the direction [MiniLLM](https://arxiv.org/abs/2306.08543) uses
  for LLM distillation and that RLHF/DPO use for their reference constraint.
* **`forward`** — KL(base ‖ student), *mass-covering*: penalises the student for withdrawing
  mass from anything the base found plausible, which fights the cross-entropy directly.

The theory says the direction should matter a great deal. **Measured, it barely does.** A sweep
on this project's student, every point trained identically on 6,000 examples for 375 steps:

| Variant | Exact match | Greedy cover | Nucleus 0.7 | min-p 0.3 |
|---|---|---|---|---|
| no KL | **0.287** | **51.7 %** | not measured | not measured |
| reverse, coef 0.03 | 0.073 | 42.3 % | 42.3 % | 43.3 % |
| reverse, coef 0.1 | 0.077 | 30.7 % | 32.0 % | 35.3 % |
| forward, coef 0.1 | 0.060 | 29.0 % | not measured | not measured |
| reverse 0.1, `--kl-mask-target` | 0.080 | 28.3 % | 30.7 % | 23.3 % |
| untrained base | — | 23.3 % | — | — |

Read three things off that table.

**The coefficient dominates the direction.** Reverse and forward at the same 0.1 differ by 1.7
points; reverse at 0.03 versus 0.1 differ by 11.6. Pick the coefficient carefully and the
direction second.

**Every KL setting removes the cliff.** Cover varies by a few points across three decoders
instead of collapsing to zero. That part works exactly as advertised, at every coefficient tested.

**The constraint is not free, and exact match pays most.** Cover falls 9.4 points at the cheapest
setting that was tried; exact match falls by roughly three quarters at *every* setting, including
that one. If exact match is what you care about, none of these points is good enough yet — sweep
below 0.03.

`--kl-mask-target` excludes the target token from the divergence, so only the shape of the
alternatives is constrained. It produced the best calibration measured here (better than base,
in distribution) and the worst task score. It is the wrong end of the curve.

### Before you reach for any of this: check for the scaling bug

The two runs that looked like "healthy short training vs damaged long training" differed in
their **loss path**, not only their length:

| Plain SFT run | Loss path | In-distribution entropy | Top-1 |
|---|---|---|---|
| 2 epochs, full data | `chunked_nll` | 11.076 | 0.001 |
| 1 epoch, 6,000 examples | `nll` | 0.000 | 1.000 |
| untrained base | — | 0.048 | 0.992 |

It is tempting to read that as over-training. It is not: the confound is the loss path, and the
verification above settles it. With the guard in place this specific failure cannot recur
silently, so **check the loss path before reaching for any training-side mitigation.**

**What is measured and what is not.** Every number on this page comes from one student and one
seed. The KL sweep above was run *before* the scaling bug was found, so it measures what the KL
term does to an already-healthy short run — its conclusions about the cost of the constraint
stand, but "the KL term fixes the cliff" does not: the cliff was a bug, and the fix is the
guard. **With the loss path corrected, the KL term buys nothing here**: the corrected student is
stable at every temperature with `--kl-coef 0`, and every non-zero coefficient measured cost
task accuracy. Leave it off unless a diagnostic on your own model says otherwise.

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
