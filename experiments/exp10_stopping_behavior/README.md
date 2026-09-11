# exp10 — The stopping gap, measured and then closed

**Tier 3, but the highest-value one here.** `docs/RESULTS.md` already contains the
diagnosis: the students' remaining gap to the teacher is *when they stop*, not what they
retrieve. Voluntary finishes are 2.4 % (base) and 11.0 % (trained) against 100 % for the
teacher, while doc recall is 0.79 against 0.84.

That is a limitation section today. Measured properly and then fixed, it is a contribution.

## Step 1 — measure

```bash
python analyze_stopping.py --runs runs/eval
```

Reports, per arm: stop-reason distribution, voluntary-finish rate, steps used against
budget, and **accuracy split by stop reason**. The last one is the number that matters. If
episodes that stop voluntarily are much more often correct, then teaching the model to stop
is worth real points, and you can estimate how many before spending a GPU hour.

## Step 2 — close it

Two cheap interventions, in increasing order of effort:

1. **Decoding.** The stop decision is a token like any other. Check whether the trained
   student's stop token is merely ranked second at the point it should fire; if so, this is
   a decoding fix, not a training one.
2. **Targeted supervision.** Up-weight the final step of each training episode, or filter
   training episodes to those that ended voluntarily, and retrain. `scripts/train_sft.py`
   takes any `train.jsonl`, so this is a data-shaping change, not a code change.

Report the estimated ceiling from step 1 next to what step 2 actually recovered. An honest
"we predicted +6, we recovered +4" is a stronger result than an unexplained gain.
