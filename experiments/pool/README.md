# Experiment pool: run every remaining experiment unattended on Slurm

One task table, self-scheduling worker jobs, and a keeper job that staffs them. Nothing runs
on a login node. Once submitted, the pool trains, evaluates, judges and tabulates
every experiment in `registry.yaml` that is not yet done. It stops by itself when the table
is finished.

| File | Role |
|---|---|
| `tasks.tsv` | every task, **highest priority first**: `name  vram_gb  ram_gb  est_h  resumable  deps` |
| `run_task.sh` | what each task does (one `case` branch per task family) |
| `worker.py` / `worker.sbatch` | one Slurm job = one worker; claims tasks and packs them onto its GPU |
| `keeper.py` / `keeper.sbatch` | every 10 min, submits the workers that runnable tasks need |
| `tools.py` | coverage check for verdicts, per-experiment views, publishing into `results/` |
| `status.sh` | one-screen status |
| `local.env.example` | site settings (judge, teacher, research checkout); copy to `local.env` (gitignored) |

## Run

```bash
cp experiments/pool/local.env.example experiments/pool/local.env   # fill in the model ids
python experiments/pool/worker.py --dry                            # what a worker would start
sbatch -p <cpu-partition> experiments/pool/keeper.sbatch           # from the kit root; that is all
bash experiments/pool/status.sh [task]                             # progress, anytime
```

The keeper submits up to `GPU_WORKERS` (4) GPU workers (12 h) for runnable GPU tasks. It adds
one 1-hour worker on the `short` partition for evaluations, which start at once, and one CPU
worker (24 h) for API and CPU tasks. It re-queues itself, so the chain outlives the
partition limit. Partitions and GPU type are set by env: `GPU_PARTITION`, `SHORT_PARTITION`,
`SHORT_GRES`, `CPU_PARTITION`.

Stop everything: `touch runs/pool/STOP; scancel -n tgd-keeper,tgd-gpu,tgd-short,tgd-cpu`. Running
tasks lose at most their last checkpoint. Delete `runs/pool/STOP` and resubmit the keeper to go on.

## How it behaves

- **Dependencies:**
  - `done:<task>` means the task is finished.
  - `file:<path>` means the file exists and has not changed for 2 minutes. E03's agreement
    task, for example, waits for `runs/e03/human_labels.csv`.
- **Packing:** a GPU worker starts tasks while their summed VRAM fits the card. Measured
  peaks in `runs/pool/queue/peaks.tsv` replace the table's guesses. Each vLLM server gets
  24 GB of its GPU (`GPU_MEM` is computed per card), so evaluations share a card with training.
- **Strict priority:** a worker never lets a lower task overtake a higher one that only
  waits for room.
- **Resumable:**
  - Every task skips finished work: `adapter/.done`, `runs/eval/<arm>/<set>/.done`, and
    verdicts already on disk. Training resumes from its last checkpoint.
  - A task exits non-zero while anything is missing. It is retried, at least 2 minutes after
    each failure, until it has failed 5 times (`MAX_FAIL`), then marked dead. Shared
    filesystems stall now and then (CephFS was seen returning EAGAIN on writes); the retry
    absorbs that.
  - On the walltime signal a worker stops its tasks and releases their claims for the next
    worker.
- **Editable while running:** workers re-read `tasks.tsv` every 30 s, and each task runs from
  a snapshot of `run_task.sh` (`runs/pool/snap/`). You can add tasks or fix a branch at any
  time. To rerun a dead task, remove `runs/pool/queue/dead/<task>` and its
  `runs/pool/queue/fail/<task>.*` files.
- **Publishing:** `tools.py publish` is the only route into `results/`. It strips provider
  prefixes and refuses a file that still names a gateway, cluster, host or absolute path.

## Layout it produces

```
runs/pool/{queue/{claim,done,fail,dead},logs,snap}   state, worker and task logs
runs/train/<run>/adapter                             LoRA adapters (seed13, ep1000, sup_guided, ...)
runs/eval/<arm>/<test-set>/                          episodes, metrics, .done
runs/judge/<name>/verdicts.jsonl                     primary judge; runs/judge_swap/ for E03
runs/views/<EID>/                                    symlinked arms + merged verdicts per table
runs/results/<EID>/                                  collect_results output
results/<EID>_*/{kit,gemma}/                         published tables (committed)
```

## Which task serves which experiment

| Experiment | Tasks |
|---|---|
| E00 reference, E13 LODO (re-judged) | `import_research`, `judge_e00`, `judge_e13`, `results_e00`, `results_e13` |
| E01 supervision ablation | `collect_selfdist` (GPU), `collect_teachdist` (API), `prep_*dist`, `prep_e01_match`, `train_sup_*`, `eval_sup_*`, `judge_sup_*`, `results_E01` |
| E02 seed variance | `train_seed{13,17,23}`, `eval_seed*`, `eval_base`, `judge_*`, `results_E02` |
| E03 judge validity | `judge_e00_kimi`, `judge_e00_qwen`, `e03_sample`, `e03_agreement` (waits for the human labels) |
| E04 data scaling | `prep_sizes`, `train_ep{1000,2000,4000}`, `eval_ep*`, `results_E04` |
| E06 teacher strength | `prep_self`, `prep_glm`, `train_selftaught`, `train_glmtaught`, `results_E06` |
| E07 contamination | `e07_contamination` |
| E08 step budget | `eval_budget{1,5,8}`, `teacher_b{1,3,5,8}`, `results_E08` |
| E09 forgetting | `forget_seed13` |
| E10 stopping | `e10_stopping` |
| E11 LoRA rank | `train_r{8,16,64}`, `eval_r*`, `results_E11` (lowest priority) |
| E12 corrected p-values | `e12_pvalues` (after the result tables) |
