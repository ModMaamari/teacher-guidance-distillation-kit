# Running your own experiments

This kit is a harness, not a single result. Everything is parameterised: the student, the
teacher, the judge, the datasets, the training objective and the decoder. This page is the map
of what to change and where.

## The shortest path to your own run

```bash
bash setup_env.sh                  # three virtualenvs
make data                          # build the SFT train/dev files (~2 min, required)
make smoke                         # whole pipeline with mock models, no GPU or API key
cp .env.example .env               # add a teacher/judge endpoint if you want those arms
```

Then train and evaluate with your own student:

```bash
sbatch -p <partition> slurm/train.sbatch data/splits/uniform runs/train/mine \
    --model Qwen/Qwen2.5-3B-Instruct --kl-coef 0.03 --health-every 200
sbatch -p <partition> slurm/eval_student.sbatch \
    "mine=mine:runs/train/mine/adapter" "heldout_hotpotqa heldout_musique" \
    --model Qwen/Qwen2.5-3B-Instruct
sbatch -p <partition> slurm/eval_stability.sbatch runs/train/mine/adapter mine
STUDENT_MODEL=Qwen/Qwen2.5-3B-Instruct sbatch -p <partition> \
    slurm/eval_forgetting.sbatch runs/train/mine/adapter mine
```

## What you can change

| Knob | Where | Notes |
|---|---|---|
| **student** | `--model <hf id>` on `train_sft.py`, `eval.py`; `MODEL=` for `serve_vllm.sh`; `STUDENT_MODEL=` for the sbatch wrappers | any HF causal LM with a chat template. Memory scales with size; the 3B reference peaks near 26 GB with LoRA at 8k context |
| **teacher** | `--teacher <id>` (guided arm), `--agent-model <id>` (teacher-alone arm) | any provider-prefixed id, comma-separated for a fallback chain — `docs/PROVIDERS.md` |
| **judge** | `judge.py --judge <id>`, `--prompt-file` for a custom rubric | the judge never sees the trajectory or which arm produced an answer |
| **datasets** | `--datasets` on `build_splits.py` and `collect_episodes.py` | add `data/questions/<name>/<name>_{questions,corpus}.jsonl[.gz]` in the documented format — `docs/DATA.md` §4 |
| **split design** | `--heldout-fraction`, `--salt`, `--dev-fraction` | a different salt gives a different, equally valid held-out set; always re-run `check_leakage.py` |
| **training objective** | `--kl-coef`, `--kl-direction`, `--kl-mask-target`, `--lr`, `--epochs`, `--lora-r` | `docs/STABILITY.md` has the measured trade-off curve, and why training length matters more |
| **decoder** | `--student-temperature`, `--top-p`, `--min-p`, `--top-k` on `eval.py` | relative truncation matters for fine-tuned students — `docs/STABILITY.md` |
| **budget / prompts** | `--budget`, `--hidden-budget`, `--no-plan` | the agent's step budget and whether it is told what it is |

## Three experiments worth running first

**1. Does it work at all with your student?** Train on `data/splits/uniform`, evaluate the base
and trained arms on the four held-out sets, and judge. That reproduces the headline comparison
with your model in place of ours. Roughly 4 GPU-hours plus evaluation.

**2. Does it transfer?** Train the four `data/splits/lodo/fold_*` students and evaluate each on
its unseen dataset. That answers whether guidance internalised on three datasets carries to a
fourth. Four times the training cost, and the most interesting result in `docs/RESULTS.md`.

**3. What did it cost?** `slurm/eval_forgetting.sbatch` for general ability, and
`slurm/eval_stability.sbatch` for whether the model can still be sampled. Both are cheap and
both catch failures that the headline evaluation cannot see.

## Choosing a KL coefficient

First check whether you need one at all. The failure this guards against tracked training
length, not the objective: a short no-KL run was healthy where a long one was not
(`docs/STABILITY.md`). Run `scripts/diag_distributions.py` on an early checkpoint before
spending anything here.

If you do need one, the regulariser trades task performance for calibration. Measured on this
project's student the coefficient mattered far more than the direction, and the useful range sat
at or below 0.03, so sweep downward from there:

```bash
for coef in 0 0.003 0.01 0.03; do
  sbatch -p <partition> slurm/train.sbatch data/splits/uniform runs/train/kl$coef \
      --limit 6000 --epochs 1 --kl-coef $coef --health-every 100
done
# then, per run: agent cover and exact match at greedy, and OOD top-1
sbatch -p <partition> slurm/eval_stability.sbatch runs/train/kl0.03/adapter kl003
```

Keep every point at the same `--limit` and `--epochs`. Comparing a KL run against a baseline
trained on more data confounds the constraint's cost with the budget difference, which is worth
about 9 points of cover here — roughly the size of the effect being measured.

A healthy point keeps agent cover near the `--kl-coef 0` run while pulling out-of-distribution
top-1 back toward the base model's. If cover falls toward the *untrained* baseline, the
coefficient is too high. **Watch exact match separately**: it fell by roughly three quarters at
every coefficient tested here, including ones where cover looked acceptable.

## Costs to plan around, measured on this hardware

| Stage | Scale | Time |
|---|---|---|
| build splits + leakage audit | full | ~2 min CPU |
| train, uniform split | 14.5k examples, 2 epochs | ~4 GPU-hours |
| train with `--kl-coef` | same | ~5.5 GPU-hours (extra base forward pass) |
| evaluate one student arm | 747 questions | ~15 GPU-minutes |
| guided arm (teacher in the loop) | 747 questions | ~45 min + teacher API |
| general benchmarks | 4,529 items | ~10 GPU-minutes |
| stability check | full | ~40 GPU-minutes |

## Conventions worth knowing

* Every long-running script takes a fixed `--out`, appends results as they land, writes
  `status.json`, and marks completion with `.done`. Re-running is always safe and resumes.
* Slurm wrappers redirect every cache and `HOME` into the project directory, because compute
  nodes often mount home read-only.
* `mock/<anything>` as a model id runs the whole pipeline offline with canned responses. That
  is what `make smoke` uses, and it is the fastest way to check a change end to end.
* Nothing under `runs/` is needed to rebuild anything else.

## If something looks wrong

`docs/REPRODUCE.md` has a troubleshooting table covering read-only home directories, vLLM
startup failures, unconfigured providers and partial evaluations. The two failures most likely
to mislead you are documented in `docs/STABILITY.md`: a model that collapses only when sampled,
and an inference server whose default truncation differs from another's.
