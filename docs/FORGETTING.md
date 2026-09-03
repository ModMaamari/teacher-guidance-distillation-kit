# Forgetting check — does the student keep its general abilities?

Fine-tuning a small model on agent trajectories teaches it one narrow behaviour: emit a
JSON action, ground every claim in a retrieved document, stop when the evidence is in.
The obvious risk is that it forgets everything else, or that it can no longer answer an
ordinary question because it now answers everything in the agent format.

This check measures that directly. The base weights and the trained adapter answer the
**same** items through **one** vLLM server, so the adapter is the only difference. The
prompts are each benchmark's ordinary chat format, deliberately *not* the agent format
the adapter was trained on.

## Benchmarks

Three standard held-out sets, chosen because the guidance data touches none of them:

| Benchmark | Split | Items shipped | Capability |
|---|---|---|---|
| MMLU | test, stratified over all 57 subjects | 1,710 | broad factual knowledge |
| GSM8K | test, complete | 1,319 | multi-step arithmetic reasoning |
| HellaSwag | validation (test labels are not public) | 1,500 | commonsense completion |

`data/benchmarks/*.jsonl.gz` ship with the repository (gzipped, ~0.7 MB total; all three
are MIT-licensed, and `manifest.json` records source, split, license, homepage and a
checksum of the uncompressed content). Rebuild or resize them with:

```bash
.venv_train/bin/python scripts/prepare_benchmarks.py --out data/benchmarks
# --mmlu 1710 --gsm8k 0 (0 = the whole test split) --hellaswag 1500 --seed 13
```

Selection is seeded and stratified, so a rebuild reproduces the shipped files and both
arms always see identical items.

## Scoring

Every item is answered by generation, then parsed two ways:

* **strict** — the reply has exactly the requested shape: a bare letter for multiple
  choice, a final `#### <number>` line for GSM8K.
* **lenient** — the answer is recovered from a messier reply (a standalone letter, a
  letter inside JSON or prose, the last number in the text).

Both are reported, along with how often the reply had the requested shape and how often
nothing could be parsed at all. That separation is the point: a model that has
over-fitted to the agent format keeps its knowledge but loses the ability to answer in
the asked form, and strict-only scoring would misread that as knowledge loss.

## Running it

```bash
# one GPU; base + adapter served together, both arms, all three benchmarks
sbatch -p <gpu-partition> slurm/eval_forgetting.sbatch runs/train/uniform/adapter trained_uniform

# or by hand against a server you already have up
scripts/serve_vllm.sh --lora trained=runs/train/uniform/adapter &
.venv_train/bin/python scripts/eval_benchmarks.py --benchmarks data/benchmarks/mmlu.jsonl.gz \
    --served-model student --arm base --out runs/forgetting/base/mmlu
.venv_train/bin/python scripts/eval_benchmarks.py --benchmarks data/benchmarks/mmlu.jsonl.gz \
    --served-model trained --arm trained --out runs/forgetting/trained/mmlu
.venv/bin/python scripts/forgetting_report.py --runs runs/forgetting --out runs/forgetting/report
```

### Repeated runs

A single greedy pass gives no measure of its own noise. `RUNS=5` repeats every
(arm, benchmark) five times with distinct sampling seeds at `TEMPERATURE` (0.3 by
default when `RUNS>1`), so the spread across replicates *is* the decoding noise:

```bash
RUNS=5 sbatch -p <gpu-partition> slurm/eval_forgetting.sbatch runs/train/uniform/adapter trained_uniform
```

`scripts/forgetting_report.py` then reports, per benchmark and pooled, each arm's mean,
variance, standard deviation and 95 % t-interval over the runs, the paired difference
tested with a paired t-test and an exact Wilcoxon signed-rank test on the R paired run
accuracies, an item-level exact McNemar test over all R x N decisions, and box plots of
the per-run distributions (`boxplot.svg`, inline SVG, no plotting dependency).

`BENCHMARKS="mmlu gsm8k"` limits the set; `CONCURRENCY=` tunes throughput; `SEEDS=` sets
the seed list.

### Sampling robustness — read this before raising the temperature

A student fine-tuned hard on one narrow format can be perfectly well behaved at its
argmax and fall apart when sampled. SFT drives output entropy down, and on prompts
unlike the training data the model is left poorly calibrated: greedy decoding still
picks a sensible token, but sampling reaches into a tail that has become garbage.

Measured on this project's own student, on MMLU items:

| Decoding | Base model | Trained student |
|---|---|---|
| greedy (T=0) | replies in format | replies in format |
| T=0.3 | replies in format | replies in format |
| T=0.7 | replies in format | **collapses into token salad** |

The collapse is identical at concurrency 1 and 16, so it is temperature-driven, not a
batching or serving artefact. Two consequences:

* Replicates default to T=0.3, where both arms are stable. If a run collapses, the
  canary in the job script fails it loudly rather than letting a serving or decoding
  problem be written up as catastrophic forgetting.
* The collapse is itself a finding worth measuring, not just avoiding. `SWEEP=` runs the
  same benchmark subset across temperatures for both arms, which turns brittleness into
  a curve you can report:

```bash
SWEEP="0.0 0.3 0.5 0.7 1.0" SWEEP_N=400 sbatch slurm/eval_forgetting.sbatch <adapter> <arm>
```

Report the greedy numbers as the point estimate and the sweep as the robustness result;
a model that is only usable greedily is a materially different product from one that
tolerates sampling, even when their greedy accuracies match. Each
`(arm, benchmark)` writes `predictions.jsonl` (one row per item, with the raw reply),
`metrics.json`, `status.json` and a `.done` marker, and is skipped on resubmission — so
an interrupted run continues where it stopped.

The report gives per-benchmark and pooled accuracy for both arms plus the paired
difference on identical items, with a 95% bootstrap confidence interval and an exact
McNemar test.

## Reference result

Measured for the student in `docs/RESULTS.md` (granite-4.1-3b, LoRA on 14,458
guidance-as-thought examples), 4,529 items per arm, greedy decoding:

| Benchmark | Base | Trained | Δ | McNemar p |
|---|---|---|---|---|
| MMLU | 64.1 % | 63.2 % | −0.9 | 0.18 |
| GSM8K | 89.3 % | 87.1 % | −2.2 | 0.007 |
| HellaSwag | 75.3 % | 74.2 % | −1.1 | 0.14 |
| **pooled** | **76.9 %** | **75.5 %** | **−1.4** (CI −2.1 … −0.5) | 0.001 |

Format compliance survived intact: 100 % of multiple-choice replies and 99.3 % of GSM8K
replies had the requested shape (base: 100 % / 99.9 %), and nothing was unparseable in
either arm. On GSM8K the trained model lost 65 items and gained 40; only 4 of the losses
were format problems, the rest genuine arithmetic errors.

So the cost of internalising the teacher's guidance is about **1.4 points of general
ability**, against **+35.6 points** of judge-correct accuracy on the agent task. Two
caveats: a single decoding seed at temperature 0, and zero-shot chat prompting rather
than the log-likelihood scoring used by public leaderboards, so absolute numbers are not
comparable to published ones. The comparison between arms is unaffected, since the arms
differ only by the adapter.
