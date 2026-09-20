# E20 — Does the correctness filter earn its place?

**Question.** Every training split keeps only the episodes whose final answer was correct, which
discards 47 % of the self-guided collection. Is the filter worth the data it throws away, and how
much of the gain comes from the answers being right rather than from learning the agent loop?

**Answer.** The filter earns its place, and failed episodes are still worth a lot. Judge-correct
accuracy (Gemma-4-31B-it) on the 747 held-out questions, three training seeds unless noted:

| Training episodes | Episodes | Correct | Examples | Train PFLOPs | Judge-correct | vs correct only |
|---|---|---|---|---|---|---|
| None (base student) | — | — | — | — | 27.3 | — |
| **Correct only (the method)** | 3,818 | 100 % | 13,825 | 684 | **64.9 ± 1.7** | — |
| Correct and incorrect, all | 7,208 | 53 % | 26,610 | 1,312 | 62.6 ± 0.8 | **−2.3** [−3.9, −0.7], p 0.006 |
| Correct and incorrect, size-matched | 3,642 | 53 % | 13,828 | 682 | 61.9 ± 0.8 | **−3.0** [−4.7, −1.2], p 0.0008 |
| Incorrect only (one seed) | 3,390 | 0 % | 12,785 | 628 | 58.9 | −6.0 [−8.3, −3.7] |

Differences are seed-averaged (each question averaged over the seeds of each arm; bootstrap 95 %
CI, sign-flip permutation p). Both survive Holm correction over the two planned contrasts
(0.006 and 0.002). Per seed the picture is consistent in sign: all episodes −3.6 (p 0.012),
−3.2 (p 0.012), −0.1 (p 1.0); size-matched −5.6 (p 0.0001), −2.5 (p 0.076), −0.8 (p 0.61).

**Reading.**
- **Dropping the filter costs accuracy and doubles the training bill.** Training on everything
  loses 2.3 points while spending 1,312 instead of 684 PFLOPs (26,610 instead of 13,825 examples).
- **It is not dilution, it is what the failures teach.** At equal training-set size the loss is
  the same or larger (−3.0), and doubling the unfiltered data recovers only 0.7 points (p 0.44).
- **Failed episodes still teach the agent loop.** Trained on wrong-answer episodes alone, the
  student reaches 58.9 %, +31.6 over the base student, which is 84 % of the gain of correct-only
  training, while staying 6.0 points behind it. Most of what self-guided data teaches a small
  agent is to search, extract and commit to an answer; correctness adds the last few points.
- **Cost of the filter is zero, its saving is real.** The discarded episodes are collected either
  way, so the filter saves only training: half the compute and half the time, at the same peak
  memory (18.1 GiB, LoRA on a 3.4B student). Inference is unchanged: every trained arm uses 2.89
  steps and 5.1–5.2k tokens per question, and answers in about 20 words.

**Protocol.** Self-guided episodes (`data/episodes_self`), the paper's method. Only the
correctness filter changes; the leakage gate, held-out duplicate guard, ungrounded-gold and
malformed-target filters are identical (`scripts/build_splits.py --keep correct|all|incorrect`).
The size-matched split takes whole episodes from the unfiltered pool in one seeded order until it
has as many examples as the filtered split (`make_matched.py`). Same LoRA recipe, budget 3 and
judge as everywhere else. Pool tasks `prep_e20`, `train_mix*`, `train_wrongonly`, `eval_*`,
`judge_*`, `results_E20mm` (early: matched arms), `results_E20`.

**Files.** `kit/` (all arms, three seeds): `summary.txt`/`.json` (seed means and the paired
tests), `train_cost.txt`/`.json` (examples, tokens, PFLOPs, GPU-hours, peak memory),
`results.json`/`RESULTS.md` (per test set), `split_*.json` (what each split contains),
`filter_vs_judge.txt`. `matched/` and `seed13/` are the earlier partial publications.

**Caveats.**
- The filter is a string match (cover match), not the judge: of the episodes it drops, 22.9 % are
  judged correct (right answer, different wording), and 4.4 % of those it keeps are judged wrong
  (`kit/filter_vs_judge.txt`). A judge-based filter might do better than either arm here.
- Filtering also changes the dataset mix, because MuSiQue episodes succeed least often: MuSiQue is
  14 % of correct-only examples and 26 % of unfiltered ones.
- One seed for the incorrect-only arm; three for every other arm.
- E12 corrects this table over all 55 pairs of its 10 arms, which is far stricter than the two
  planned contrasts; there only `correct13 -> mixmatch13` survives Holm, and the two seed-13/17
  all-episode gaps survive BH.

## History

- **2026-09-20:** first run (pool). Trainings ran on shared GPUs and some resumed from
  checkpoints, so `train_cost` GPU-hours are not comparable between arms; PFLOPs, examples and
  peak memory are. The clean single-GPU reference is 2.90 h for a correct-only arm on one L40S.
