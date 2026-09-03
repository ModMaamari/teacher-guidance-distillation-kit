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
| `--smoke` | — | 64 examples, 8 steps: validates the pipeline in ~2 min |
| `--kl-coef` | 0 (off) | KL toward the frozen base on completion tokens; keeps the student samplable. See `docs/STABILITY.md` |
| `--kl-direction` | `reverse` | `reverse` = mode-seeking (recommended); `forward` = mass-covering, fights the task objective |
| `--health-every` | 0 (off) | sample held-out prompts at temperature 0.7 every N steps and log how many parse |

bf16 + gradient checkpointing; the 3B student peaks at ~26 GB GPU memory and trains the
uniform split in ~4 GPU-hours on a 80 GB-class GPU (1,810 optimizer steps, ~8 s/step).

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

`--smoke` runs on CPU as well (64 examples, 8 steps, fp32) if no GPU is visible, which makes it
a usable pre-flight check on a laptop before queueing a real job. Keep `--max-length` at its
default when you do: a prompt longer than the limit truncates the completion away, and a run
that trains on no completion tokens reports a loss of exactly 0. The trainer now checks a few
real batches at startup and refuses to run when that happens.

With `--kl-coef > 0` the trainer needs real logits, so it switches off TRL's memory-chunked
cross-entropy and runs a micro-batch of 1 at four times the gradient accumulation. Expect about
40 % more wall time for the extra base-model forward pass.

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
