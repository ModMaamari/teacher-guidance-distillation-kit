# Research workflow — experiments, results, paper

How experiments are run, recorded and cited, so that every number in the paper traces back to one
folder. Kept short on purpose.

## Four places, four jobs

| Where | Holds | In git |
|---|---|---|
| `experiments/expNN_<name>/` | how to run it: `README.md` (question, design, commands) and scripts | yes |
| `runs/` | raw outputs: adapters, episodes, verdicts, logs | no |
| `results/ENN_<name>/` | what we cite: final numbers, tables and figures, plus a provenance `README.md` | yes |
| `experiments/registry.yaml` | the status of every experiment; `experiments/REGISTRY.md` is generated from it | yes |

Running them: `experiments/pool/` executes every experiment's tasks as Slurm jobs and publishes
into `results/` through a scrubber. Each experiment's scripts still work by hand.

## IDs

Every experiment has one ID, `E00`–`E16` today. The ID names its folder
(`experiments/exp04_data_scaling`), its results (`results/E04_data_scaling`) and its paper labels
(`tab:E04-scaling`, `fig:E04-curve`). IDs are never reused or renumbered; a new experiment takes
the next free number.

## Status

`planned → running → done`, or `partial` (some of it done), `superseded` (replaced by a rerun;
the README says by what) and `dropped` (with the reason). Status lives only in `registry.yaml`.
After editing it:

```bash
python experiments/status.py          # regenerates experiments/REGISTRY.md
python experiments/status.py --check  # also fails if a done/partial entry has no results README
```

## Definition of done

An experiment is `done` when `results/ENN_<name>/` holds:

1. `README.md` — the question, the answer in one sentence with its key numbers, the protocol
   (student, teacher, judge, budget, seeds, n), where the raw runs are (paths, job ids, commit),
   and caveats.
2. The numbers as produced by a script (`results.json`, `summary.json`, `comparison.json`),
   never typed by hand.
3. Any table or figure the paper uses, generated from (2).

Nothing in `results/` may contain keys, endpoint URLs, host names or personal paths.

## Rules that protect the paper

* **One judge per comparison.** Every number in one table comes from the same judge, named in the
  README. The current judge is Gemma-4-31B-it (see `results/E16_judge_selection`).
* **Uncertainty is part of the number.** Report the paired 95 % CI and the McNemar p-value;
  E12 corrects the p-values across the paper.
* **Seeds are recorded.** A single-seed result says so in its README.
* **The paper never cites `runs/`.** Copy the final artifact into `results/` first.
* **Reruns keep history.** When a result is redone (another judge, a fixed bug), update its folder
  and add a dated line under `## History` in its README saying what changed and why.

## Adding an experiment

Take the next free ID, create `experiments/expNN_<name>/README.md` (question, design, commands),
add the registry entry as `planned`, and dry-run before submitting (`DRY_RUN=1`, see
`experiments/README.md`).

## Writing the paper

Tables and figures come only from `results/`. The paper's appendix lists the experiments by ID —
`experiments/REGISTRY.md` is that list — so a reviewer's question about any number maps to one
folder.
