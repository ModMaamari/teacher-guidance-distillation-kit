# exp09 — What did the training cost in general ability?

**Tier 2, and nearly free.** The kit already ships the benchmarks and both scripts; the gap
is that the result is not reported per trained student. A method that buys +35.6 points on
multi-hop QA by wrecking MMLU is a different paper, and a reviewer will ask.

## Run

```bash
export PARTITION=<gpu-partition>
bash run.sh                # MMLU / GSM8K / HellaSwag for base + every trained arm
bash run.sh report         # deltas + box plots
```

`ARMS="uniform seed13 ep4000"` selects which trained runs to measure.

**You do not submit a base run.** `slurm/eval_forgetting.sbatch` serves one vLLM instance
and answers every benchmark twice, once through the base weights and once through the
adapter, so the base arm is measured in the same job and on the same server. That is what
makes the delta trustworthy: the adapter is the only difference. The wrapper requires a
real adapter directory and exits if it is missing.

## Reporting

One table: benchmark by arm, with the base row first and deltas in brackets. Put it in the
main paper, not an appendix. Small negative deltas are expected and fine to show; hiding
them is what looks bad.

Also run `slurm/eval_stability.sbatch` for each arm. Forgetting asks whether the model
still knows things; stability asks whether it can still be sampled at all. Both are cheap
and both catch failures the headline evaluation cannot see.
