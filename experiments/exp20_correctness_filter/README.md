# exp20 — Does the correctness filter matter?

**Why.** Every training split keeps only the episodes whose final answer was correct (rejection
sampling, as in STaR and RFT). Collecting the self-guided data yields about as many incorrect
episodes as correct ones, and the filter discards them. Would the student be as good, or better,
trained on all of them, correct and incorrect? A reviewer will ask, and E01/E17 never isolate the
filter.

## Design

Data: the self-guided episodes (`data/episodes_self`, the paper's method). All arms go through the
same hygiene filters (held-out duplicates, leakage gate, ungrounded gold, placeholders, malformed
targets); only the correctness filter changes. "Correct" is the collection-time cover match, as in
every other split. Same LoRA recipe, budget 3, the 747 held-out questions, primary judge.

| Arm | Training episodes | Seeds |
|---|---|---|
| `correct` | correct only (the method; `selftaught`, E19 `selftaught_s17/_s23`) | 13, 17, 23 (exist) |
| `mixall` | correct and incorrect: every trainable episode, about twice the data | 13, 17, 23 |
| `mixmatch` | correct and incorrect, whole episodes sampled until the example count equals `correct`'s | 13, 17, 23 |
| `wrongonly` | incorrect only (diagnostic: what the failures alone teach) | 13 |

Contrasts, stated before the results:
1. **`correct` vs `mixall`**: what the filter buys at a fixed collection budget (the filter throws
   data away, so this is the practical choice).
2. **`correct` vs `mixmatch`**: the filter at equal training-set size (content, not amount).
3. `mixall` vs `mixmatch`: does more unfiltered data help?
4. `wrongonly` vs base and vs `correct`: how much of the gain comes from format and tool use
   alone.

Statistics: per seed, the paired bootstrap CI and exact McNemar of the results table; across
seeds, mean and SD, and a seed-averaged paired test (each question's accuracy averaged over the
three seeds of each arm, bootstrap CI and sign-flip permutation p over the 747 questions), with
Holm over contrasts 1 and 2. Also reported: steps, tokens per question and median answer length.

## Run

```bash
bash experiments/pool/run_task.sh prep_e20      # splits: data/splits_self_{all,wrong,mixmatch}
```

Pool tasks: `prep_e20`, `train_mixall_s{13,17,23}`, `train_mixmatch_s{13,17,23}`,
`train_wrongonly`, `eval_*`, `judge_*`, `results_E20` (which also runs `summarize.py` and
refreshes E12). `make_matched.py` builds the size-matched split; `summarize.py` prints the
seed-level table.
