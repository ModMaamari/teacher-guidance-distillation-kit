# When something goes wrong

Ordered by how hard the failure is to notice, not by how common it is. Everything in the
first section produces *no error at all* — the run completes, the numbers look plausible, and
the result is wrong. Those are the ones that cost real time here.

## Failures that look like success

### The student answers nothing, and retrieval looks fine

**Symptom.** EM, F1 and cover are all exactly 0.000 across every test set. `mean_steps` sits at
the budget, `voluntary_finish` is 0.00, and `stop_reasons` is entirely
`budget_forced_finish_no_finish` — yet `doc_recall` is healthy, so the agent is finding the
right documents and then never reporting an answer.

**Diagnose.** Look at a raw step, not the metrics:

```bash
python - <<'PY'
import json
ep = json.loads(open("runs/eval/<arm>/<set>/episodes.jsonl", encoding="utf-8").readline())
print(ep["steps"][0]["student_raw"][:400])
PY
```

Prose where a JSON object should be — and often prose all the way to the token budget — means
the model is writing in a reasoning channel it was never asked to leave.

**Most likely cause.** A reasoning student whose chat template opens a thinking block in the
generation prompt while training rendered a closed one. `docs/MODELS.md` § *Reasoning
("thinking") students* has the mechanism; `train_sft.py` and `eval.py` now detect and reconcile
it, and the training log says which keyword it used. An untrained granite-4.2-3b scored 0.000
on 100 episodes for exactly this reason.

### The GPU is five to ten times slower than it should be

**Symptom.** No error. Training crawls, memory sits just under the card's capacity, and
`nvidia-smi` reports 100% utilisation the whole time. Peak memory grows faster than linearly
with sequence length — a clue, if you are logging it.

**Diagnose.** Ask PyTorch whether it has a fused kernel for grouped-query attention:

```bash
python -c "
import torch
from torch.nn.attention import SDPBackend, sdpa_kernel
q = torch.zeros(1, 4, 8, 16, device='cuda', dtype=torch.bfloat16)
kv = torch.zeros(1, 2, 8, 16, device='cuda', dtype=torch.bfloat16)
with sdpa_kernel([SDPBackend.EFFICIENT_ATTENTION, SDPBackend.FLASH_ATTENTION]):
    torch.nn.functional.scaled_dot_product_attention(q, kv, kv, is_causal=True, enable_gqa=True)
print('fused GQA kernel available')"
```

**Most likely cause.** Transformers asks PyTorch to handle grouped-query attention itself
whenever there is no attention mask. A build without that kernel — the Windows CUDA wheels, for
one — falls back to the *math* backend, which materialises the full `[batch, heads, seq, seq]`
score matrix. There is no warning. Measured on one attention op at 40 heads and 2,560 tokens in
bf16: **0.13 GiB on the memory-efficient kernel against 4.03 GiB on math**, and end to end 466
against 48 tokens/second. `tgd/sdpa_compat.py` probes for the kernel on every model load and
repeats the key/value heads instead when it is missing; the log line says so when it engages.

### The model is excellent at greedy and useless when sampled

**Symptom.** Greedy evaluation looks right. At temperature 0.3 or above the agent task collapses
— near-zero cover, almost every action unparseable. On single-token benchmarks it degrades
gently instead, which makes it easy to dismiss.

**Diagnose.**

```bash
python scripts/diag_distributions.py --models "base=<base>" "trained=<merged dir>" \
    --n 150 --out runs/diag
```

Healthy: entropy well under 1 nat, top-1 above 0.8, valid-token mass 100 %. Broken looks like
entropy near `ln(vocab_size)` (about 11.5 for a 100k vocabulary), top-1 near zero, and almost no
mass on legal tokens. The ranking stays correct throughout, which is exactly why greedy hides it.

**Most likely cause.** The loss the trainer optimised was computed at a different logit scale
than the model produces. `scripts/train_sft.py` now checks this before training and refuses to
start, so a fresh run should not reach here. A checkpoint trained before that guard existed can
be repaired without retraining — `scripts/repair_logit_scale.py`, and `docs/STABILITY.md` for
the whole story.

**Other causes with the same signature.** A merge that dropped a config field, a quantisation
step, or genuine over-training. The diagnostic above does not care which; it tells you the
distribution is broken, and the position profile
(`scripts/diag_position_profile.py`) tells you whether it is broken everywhere or only at the
start.

### Training loss is exactly 0.0

Every completion was truncated away, so there is nothing to compute a loss on. Raise
`--max-length`, or shorten prompts. The trainer checks a few real batches at startup and
refuses to run when this would happen, so you should only see it on an older checkpoint's logs.

### `valid-token mass 0.000` but entropy and top-1 look healthy

Not a broken model. The chat template almost certainly opens a reasoning (`<think>`) block, so
the first generated token — the one the diagnostic inspects — is the start of the model's
reasoning rather than its answer. Two of the six students listed in `docs/MODELS.md` behave this
way.

The diagnostics close the block automatically and print a warning when a template will not let
them. If you see that warning, entropy and top-1 are still meaningful; the answer-token metrics
are not.

### Two arms were evaluated under different settings

Every stage skips work when it finds a `.done` marker. If you change temperature, decoding, or
the model and re-run into the *same* output directory, finished arms are skipped and you end up
comparing yesterday's settings against today's. Use a fresh `--out` per configuration, or delete
the specific `.done` files you intend to redo. `runs/.../metrics.json` records the settings that
produced it — check them before believing a comparison.

### The adapter was merged onto the wrong base

Produces a broken model rather than an error. `scripts/merge_adapter.py` now takes the base from
the adapter's own record and refuses a contradicting `--base`, so this needs `--force-base` to
happen at all.

### Everything looks fine because you only measured greedy

Greedy decoding cannot see a damaged output distribution: a broken model and a correct one score
*identically* on it. If a model will ever be sampled, run
`slurm/eval_stability.sbatch` before trusting it, and train with `--health-every 200` so the
problem shows up during training rather than a week later.

## Failures that stop the run

| Symptom | Cause and fix |
|---|---|
| `torch.OutOfMemoryError` partway through an epoch, not at step 0 | The non-chunked loss materialises a `[batch, seq, vocab]` tensor — 12 GB at micro-batch 4 with an 8k sequence and a 100k vocabulary — and it only fails when the first full-length batch arrives. The trainer trades micro-batch for accumulation automatically; if you overrode it, lower `--batch-size` and raise `--grad-accum` by the same factor. Resuming across that change is safe |
| `AutoModelForCausalLM` raises on a model that clearly is a language model | It ships as a conditional-generation or vision-language architecture and is not in the causal-LM mapping. The kit tries the other auto classes and logs which one loaded (`docs/MODELS.md`); if you load models yourself, use `tgd.models.load_lm` |
| `PermissionError: ... /home/...` on a compute node | Home is read-only there. The Slurm templates already redirect `HOME`, `HF_HOME`, `XDG_CACHE_HOME`, `VLLM_CACHE_ROOT`, `TRITON_CACHE_DIR` and `TORCHINDUCTOR_CACHE_DIR` into the project; do the same in an interactive shell |
| `vLLM server failed to start` | Read `runs/vllm_<port>_*.log`. Usually: the port is taken (`PORT=`), not enough GPU memory (`GPU_MEM=0.7`), or a LoRA rank above `--max-lora-rank` |
| The server takes 8–10 minutes to come up | Normal on a cold cache — it compiles kernels. The wait is in the start-up loop; do not shorten it |
| `ModuleNotFoundError` in the training env | Re-run `setup_env.sh`, or install `requirements/train.txt` into `.venv_train` |
| Trainer errors about `SFTConfig` arguments | TRL version mismatch. Install the pinned `requirements/train.txt` |
| `no OpenAI-compatible endpoint configured for '...'` | Set the provider's base URL and key in `.env` (`docs/PROVIDERS.md`) |
| `eval.py` exits with code 3 | Some questions failed after retries. Re-run the same command; it retries only those |
| A model has no chat template | The kit needs one to build prompts. Supply one, or pick a model that ships it |

## Slurm

| Symptom | Cause and fix |
|---|---|
| Job pending for hours, reason `Priority` | Fair-share throttling from recent usage. It decays; waiting also raises the age factor. Shorter walltime requests backfill sooner |
| Job pending, reason `Resources` | Nothing outranks you; the hardware is busy. Check with `sinfo`/`squeue` |
| Job pending with a start time days away after you added `--nodelist` | Pinning to one node makes you wait for *that* node. Remove it unless you truly need it |
| A job died and you lost hours of training | Training checkpoints every `--save-steps` and resumes automatically from `--out`. Re-submit the same command; it continues rather than restarting |
| GPUs are idle but nothing schedules onto them | The node is likely out of CPUs or memory, which blocks GPU allocation too |

## The diagnostic ladder

When something is wrong and you do not know what, in this order:

1. **`<out>/status.json`** — step, epoch, loss and ETA. Rewritten every
   logging step, so it is current even mid-run.
2. **`<out>/train.log`** — UTC-stamped. The startup lines record the logit rescaling, the loss
   path, the micro-batch, the supervision check and the loss-path check.
3. **Health-check lines** — `HEALTH step N: k/8 parseable at T=0.7`. A number that starts low or
   falls means the model is losing its ability to be sampled while training.
4. **`scripts/diag_distributions.py`** — the instrument. Entropy, top-1 and valid-token mass, in
   and out of distribution.
5. **`scripts/diag_position_profile.py`** — where along a completion the distribution degrades.
   Front-loaded means a decoding fix may be enough; uniform means the objective is wrong.
6. **`scripts/sweep_decoding.py`** — task metrics across temperature and truncation, to find a
   working operating point.

## Two habits

Both come from failures on this project, not from theory.

**Never evaluate only at greedy.** It cannot distinguish a healthy model from one whose output
distribution is destroyed.

**Train with `--health-every 200`.** Eight sampled prompts every couple of hundred steps would
have caught the worst bug here within the first hour instead of a week later.

## `UnicodeEncodeError` from a script that was working a moment ago

**Symptom.** `make data`, `collect_results.py` or `agentsim` dies with
`'charmap' codec can't encode character '∩'` (or `✗`, `Δ`). The traceback points
at a `print`, and whatever the script was reporting is lost.

**Cause.** The scripts print set notation and typographic marks (`qid∩=0`, `Δ pts`, `✓`); a
console whose encoding cannot represent them raises. It bites hardest where the crashing line is
itself an error reporter, because the crash then replaces the message it was about to show —
that is what made `tests/smoke_offline.sh` fail at step 1 on Windows with no usable diagnosis.

**Fix.** Importing `tgd` now switches the streams to UTF-8, or to `errors="replace"` if it
cannot, so output degrades instead of aborting. If you hit this in your own code, call
`tgd.console.enable()`. Setting `PYTHONUTF8=1` works too.
