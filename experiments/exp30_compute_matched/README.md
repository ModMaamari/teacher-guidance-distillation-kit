# exp30 — Self-guidance against the same compute spent on more unguided attempts

**Why.** Self-guided collection costs about three times a plain unguided rollout per episode
(0.099 vs 0.032 PFLOPs, E23) and yields a similar number of usable episodes (3,818 vs 3,753). The
obvious question, and the one a reviewer asks first, is what the same compute buys if it is spent
on more unguided attempts per question instead — rejection-sampling self-training, ReST-EM style.

**Design.** Two further unguided attempts per question over the same 7,999 questions, sampled at
temperature 0.7 so they are not near-duplicates of the temperature-0.2 first attempt, which is
reused. Three attempts at 0.032 PFLOPs each is 0.096, against 0.099 for self-guidance: the
collection compute is matched to within 3 %.

| Variant | Training data | Controls for |
|---|---|---|
| `all` | every attempt that passes the filter | more data at equal collection compute |
| `first` | the first correct attempt per question | question coverage, no duplicate questions |
| `match` | a random subset of `first` with 3,818 correct episodes | coverage *and* training-set size |

Seeds: six for `first` (it pairs with the six self-guided and six unguided seeds of E25), three for
`all` and `match`. `pick_attempts.py` also reports **pass@k**: how many trainable questions are
solved at least once by k = 1, 2, 3 unguided attempts and by self-guidance, and how many each
solves that the other never does.

**What each outcome means, written before the runs.**
- *Self-guided > `first`:* the stronger claim the paper currently cannot make — better than the
  same compute spent on more self-samples.
- *Self-guided ≈ `first`:* say so plainly. Self-guidance is then a different use of the same
  compute whose case rests on coverage (which questions get solved at all) and on cost at
  inference, not on accuracy.

**Run.** Pool tasks `collect_selfdist_a{2,3}`, `prep_e30`, `train_k3_{first,all,match}_s*`,
`eval_*`, `judge_*`, `results_E30`.
