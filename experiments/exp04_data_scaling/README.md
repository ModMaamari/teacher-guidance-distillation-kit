# exp04 — How much guidance do you actually need?

**Tier 2.** Your experiment 1, with one correction.

## The ceiling you cannot exceed with the shipped data

`make_size_splits.py --sizes N` counts **episodes collected**, not training examples. The
trainable pool is **7,252 episodes** (1,830 / 1,811 / 1,797 / 1,814 across the four
datasets). About 54.6 % are correct and become supervision, giving 3,959 usable episodes
and 14,458 SFT examples.

So the requested ladder cannot run as written:

| Requested | Feasible on shipped data |
|---|---|
| 1k, 2k, 4k | yes |
| 8k | no -- above the 7,252 pool |
| 12k | no -- needs a fresh collection round |

The default ladder here is **500, 1000, 2000, 4000, 7252**, which still spans 14x and is
enough to show whether the curve has flattened. To go beyond it you need new questions;
the upstream datasets have plenty (HotpotQA alone ships ~90k train questions), so this is
a collection cost, not a hard limit. Collect in `teacher-guidence`, then rebuild.

## Plot against both axes

Yield varies sharply by dataset -- MuSiQue 30 %, 2Wiki 69 % -- so "episodes collected" and
"training examples" are not interchangeable. `plot_size_curve.py` draws accuracy against
episode count; also report examples, because that is what the optimiser saw. Both numbers
are in each `manifest.json`.

## Run

```bash
export PARTITION=<gpu-partition>
bash run.sh splits     # build the nested size splits
bash run.sh train      # one LoRA run per size
bash run.sh eval       # evaluate each as arm ep<N>
bash run.sh judge      # judge + collect + plot
```

Sizes are nested from one seeded shuffle: the 500 sample is a subset of the 1000, and so
on, so a larger run never loses an episode a smaller one had and size is the only variable.

## Reading it

The question is whether the curve has flattened by 7,252. If it has, say so and the data
story is finished. If it is still climbing, that is the argument for a bigger collection
round, and you can quote the marginal points-per-thousand-episodes from the last segment.
