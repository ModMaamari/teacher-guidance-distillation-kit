# exp02 — Seed variance

**Tier 1. Cheap, and the paper is not publishable without it.**

`docs/RESULTS.md` says "One seed." The confidence intervals there are a bootstrap over
*questions*, which says nothing about training randomness. Two of the reported effects are
small enough that a reviewer will not accept them from a single run:

- trained student vs guided student: **-5.0 points**, CI [-8.3, -1.6]
- trained student vs teacher alone: **+6.8 points**, CI [+3.4, +10.3]

The headline +35.6 will survive anything. These two might not.

## Design

Retrain the uniform split with `--seed 13 17 23` (nothing else changes), evaluate and judge
each, then report mean ± sd across seeds alongside the within-seed bootstrap CI. Three seeds
is the minimum that lets you write "± sd"; five is better if GPUs allow.

## Run

```bash
export PARTITION=<gpu-partition>
bash run.sh                 # trains + evaluates every seed (idempotent, resumable)
bash run.sh judge           # judge once all evals are done
python summarize_seeds.py   # mean, sd, and a per-seed table
```

`SEEDS="13 17 23 31 37" bash run.sh` for five.

## Reporting

Put the seed spread in the main table, not an appendix. If the -5.0 point gap flips sign on
any seed, the honest sentence is that the two arms are indistinguishable, and that is fine:
the method still matches live guidance at 0.43x the tokens, which is the real claim.
