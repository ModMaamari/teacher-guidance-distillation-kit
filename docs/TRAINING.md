# Training

`scripts/train_sft.py` fine-tunes a student with LoRA on the "guidance as internal
thought" examples (see `docs/DATA.md` §3 for the format). Loss is computed on completion
tokens only (TRL `completion_only_loss`), using the model's own chat template.

## Command

```bash
# group B: train on all four datasets
.venv_train/bin/python scripts/train_sft.py \
    --train-file data/splits/uniform/train.jsonl --dev-file data/splits/uniform/dev.jsonl \
    --out runs/train/uniform

# group A: one fold
.venv_train/bin/python scripts/train_sft.py \
    --train-file data/splits/lodo/fold_musique/train.jsonl --dev-file data/splits/lodo/fold_musique/dev.jsonl \
    --out runs/train/fold_musique
```

| Option | Default | Notes |
|---|---|---|
| `--model` | `ibm-granite/granite-4.1-3b` | any HF causal LM with a chat template |
| `--epochs` | 2 | |
| `--lr` | 1e-4 | cosine schedule, warm-up 3 % |
| `--batch-size` × `--grad-accum` | 4 × 4 = 16 sequences per optimizer step | per GPU |
| `--max-length` | 8192 tokens | prompts contain retrieved documents; 8k covers >99 % of examples |
| `--lora-r` / `--lora-alpha` / `--lora-dropout` | 32 / 64 / 0.05 | all linear layers |
| `--eval-steps` / `--save-steps` | 200 / 200 | dev loss and checkpoint cadence |
| `--seed` | 13 | |
| `--limit` | — | cap training examples. A **seeded sample**, not the first N rows — `build_splits.py` also shuffles what it writes, so a prefix of the file is representative too. Both matter: written dataset-by-dataset, `--limit 1000` on the uniform split used to be 100% HotpotQA and `--limit 5000` contained no MuSiQue at all |
| `--load-4bit` | off | load the base weights as NF4 (QLoRA) and train the adapter on top: a 3B student drops from 7.3 GB to ~2.3 GB and fits an 8 GB card. Evaluate the adapter with the same flag |
| `--smoke` | — | 64 examples, 8 steps: validates the pipeline in ~2 min |
| `--loss-type` | `auto` | `auto` picks `nll` when the model rescales logits, else TRL's chunked default. Leave it alone unless you know why. See `docs/STABILITY.md` |
| `--health-every` | 0 (off) | sample held-out prompts at temperature 0.7 every N steps and log how many parse |

bf16 + gradient checkpointing; the 3B student peaks at ~26 GB GPU memory and trains the
uniform split in ~4 GPU-hours on a 80 GB-class GPU (1,810 optimizer steps, ~8 s/step).

`train.log` records GPU memory (allocated, reserved and peak) at each phase — after the
model loads, after the dataloader probe, after the loss-path check and at the end. On a
card with headroom that is a footnote. On a small one it is the whole story: the loss-path
check allocates the largest tensor of the run, and a caching allocator that keeps the
reserve can push the process into paging host memory, which looks exactly like a GPU that
is five times slower than it should be and produces no error at all.

## Resumability and monitoring

`--out` is a fixed directory:

* `checkpoints/checkpoint-<step>/` every `--save-steps` steps (last two kept). Re-running
  the same command resumes from the latest checkpoint with optimizer state.
* `adapter/.done` marks a finished run; the script then exits immediately (`--force` to
  retrain).
* `status.json` — step, epoch, last loss, elapsed, ETA (rewritten at every logging step).
* `train.log` — UTC-timestamped log; `trainer_state.json` — full loss history;
  `final_metrics.json` — train loss, dev loss, runtime.

```bash
watch -n 30 cat runs/train/uniform/status.json
```

## Output

`runs/train/<name>/adapter/` is a PEFT adapter (plus tokenizer). Serve it next to the
base model with `scripts/serve_vllm.sh --lora <name>=runs/train/<name>/adapter` and
evaluate it with `--served-model <name>`; or evaluate in-process with
`scripts/eval.py --student hf --adapter runs/train/<name>/adapter`.

When a run fails or finishes wrong, `docs/TROUBLESHOOTING.md` is organised by symptom.

**Using a different student.** Every check here is architecture-agnostic: before training,
the trainer compares the loss it is about to optimise against the model's own forward pass on a
real batch, and refuses to start if they disagree. You do not need to know anything about how
your model handles logits. See `docs/STABILITY.md`.

**One thing to check on a new model.** TRL's default memory-chunked loss reads logit rescaling
from `config.logit_scale`. Architectures that use a different field name (Granite's is
`logits_scaling`) would train at the wrong scale — greedy fine, sampling broken. The trainer
detects this and switches loss paths, logging a warning; if you see that warning, it is working
as intended.

**Budget memory for it.** The chunked path exists to avoid materialising the full
`[batch, sequence, vocab]` logit tensor, so switching away from it costs exactly that memory:

| Micro-batch | Sequence | Vocab | Logit tensor (fp32) |
|---|---|---|---|
| 4 | 8192 | 100k | 12.3 GB, plus a same-size softmax buffer |
| 2 | 8192 | 100k | 6.1 GB |
| 1 | 8192 | 100k | 3.1 GB |

A run that fits comfortably with `chunked_nll` can fail with `nll` partway through the first
epoch, when it first meets a batch of full-length sequences. Keep the *effective* batch by
trading micro-batch for accumulation — `--batch-size 1 --grad-accum 16` is the same optimiser
step as `--batch-size 4 --grad-accum 4`, and resuming from a checkpoint across that change is
safe because the sample count the trainer skips is identical. Expect roughly 25 % more wall
time per step.

`--smoke` runs on CPU as well (64 examples, 8 steps, fp32) if no GPU is visible, which makes it
a usable pre-flight check on a laptop before queueing a real job. Keep `--max-length` at its
default when you do: a prompt longer than the limit truncates the completion away, and a run
that trains on no completion tokens reports a loss of exactly 0. The trainer now checks a few
real batches at startup and refuses to run when that happens.

## On a Slurm cluster

```bash
sbatch -p <gpu-partition> [-A <account>] slurm/train.sbatch data/splits/uniform runs/train/uniform
sbatch -p <gpu-partition> slurm/train.sbatch data/splits/lodo/fold_musique runs/train/fold_musique
```

`slurm/common.sh` redirects every cache (`HF_HOME`, vLLM, Triton, Inductor, and `HOME`
itself) into the project directory, because compute nodes frequently mount the home
directory read-only. Set `HF_HOME` yourself if you keep model weights elsewhere.
Resubmitting a job after a time-limit kill resumes from the last checkpoint.

## Multi-GPU

The trainer is a standard TRL `SFTTrainer`; `torchrun --nproc_per_node N
scripts/train_sft.py ...` data-parallelises it (effective batch scales with N; reduce
`--grad-accum` accordingly). Only rank 0 writes artifacts.

## Reference training run

Uniform split, defaults above, one GPU: 2 epochs = 1,810 steps in 4.0 h; train loss
0.348 (mean), final dev loss 0.269 (0.349 → 0.303 → 0.279 → 0.269 at steps 400/800/1400/1810).
