# E30 — Self-guidance against the same compute spent on more unguided attempts

**Question.** Self-guided collection costs about three plain unguided rollouts per episode (E23).
What does the same compute buy if it is spent on three unguided attempts per question instead
(rejection-sampling self-training), and does self-guidance still train the better student?

**Answer.** Yes. Self-guided data beats three unguided attempts per question at the same compute,
by 2.0 points over six seeds. Judge-correct accuracy (Gemma-4-31B-it) on the 747 held-out
questions:

| Training data (correct episodes only) | Questions | Examples | Seeds | Per seed | Mean |
|---|---|---|---|---|---|
| **Self-guided (E25)** | 3,818 | 13,825 | 6 | 66.7 / 64.9 / 63.2 / 63.6 / 64.9 / 65.2 | **64.8 ± 1.2** |
| First correct of three unguided attempts (`first`) | 4,440 | 15,966 | 6 | 62.4 / 62.9 / 62.5 / 63.7 / 62.3 / 62.8 | 62.8 ± 0.5 |
| `first` cut to 3,818 episodes (`match`) | 3,818 | 13,708 | 3 | 62.8 / 63.9 / 63.2 | 63.3 ± 0.6 |
| Every correct attempt (`all`) | 4,440 | 39,796 | 3 | 64.5 / 63.0 / 62.6 | 63.4 ± 1.0 |
| One unguided attempt (E25) | 3,753 | 13,510 | 6 | 62.3 / 64.8 / 62.6 / 62.0 / 60.6 / 62.4 | 62.5 ± 1.4 |

Seed-averaged paired test (each question averaged over a family's seeds), bootstrap 95 % CI,
sign-flip p; Holm over the two planned primary contrasts:

| Contrast | Δ | 95 % CI | p | Holm |
|---|---|---|---|---|
| **`first` → self-guided** | **+2.0** | +0.4 to +3.6 | **0.017** | **0.017** |
| one attempt → self-guided | +2.3 | +0.7 to +4.0 | 0.008 | 0.016 |
| `match` → self-guided | +1.5 | −0.3 to +3.3 | 0.12 | — |
| `all` → self-guided | +1.3 | −0.5 to +3.1 | 0.15 | — |
| one attempt → `first` | +0.3 | −0.8 to +1.4 | 0.61 | — |

Over seeds, a Welch test on the twelve per-seed accuracies of self-guided and `first` gives
p 0.010. Self-guided leads `first` at five of six seeds (+4.3, +2.0, +0.7, −0.1, +2.7, +2.4).
This is the first pre-stated outcome in `experiments/exp30_compute_matched/README.md`: *better
than the same compute spent on more self-samples.*

**Compute is matched, measured rather than assumed.** Collection, 2 × 3.4B × tokens over every
recorded call (`kit/collection_cost.txt`): self-guided 790 PFLOPs; three unguided attempts 258 +
256 + 255 = 768 (97 %). Training (the trainer's counter, `kit/train_cost.txt`): self-guided 684,
`first` 710, `match` 610, `all` 1,767. Whole build: **self-guided 1,474, `first` 1,478**, `match`
1,378, `all` 2,535. Peak training memory is 17–18 GiB for every arm.

**Coverage is not what matters.** Three attempts solve more of the 7,252 trainable questions at
least once than one self-guided episode does (`kit/attempts.txt`):

| Attempts | Solved at least once |
|---|---|
| 1 unguided | 3,753 (51.8 %) |
| 2 unguided | 4,212 (58.1 %) |
| 3 unguided | 4,440 (61.2 %) |
| 1 self-guided | 3,841 (53.0 %) |

264 questions are solved only by self-guidance and 863 only by the attempts. Yet 687 more solved
questions (`first` over one attempt) buy +0.3 points (p 0.61), and three times the training data
(`all`) no significant gain either. What self-guidance adds is not more solved questions but
different trajectories for them.

**Protocol.** Attempts 2 and 3 are fresh unguided collections over the same 7,999 questions with
the student at temperature 0.7 (`collect_selfdist_a{2,3}`); attempt 1 is E25's temperature-0.2
collection, reused. `pick_attempts.py` builds the three variants (`match` samples with seed 30).
Same LoRA recipe as every other student. Pool tasks `collect_selfdist_a{2,3}`, `prep_e30`,
`train_k3_{first,all,match}_s*`, `eval_*`, `judge_*`, `results_E30`.

**Files.** `kit/summary.txt`/`.json` (accuracy, steps, tokens, voluntary finish, every test),
`kit/results.json`/`RESULTS.md`, `kit/attempts.txt` (coverage), `kit/collection_cost.txt`/`.json`,
`kit/train_cost.txt`/`.json`.

**Caveats.** In domain only; the external benchmarks (E27) were not rerun for these students.
`match` and `all` have three seeds each, so their contrasts are underpowered. Attempts 2 and 3 are
sampled hotter than attempt 1, by design, so the three are not identically distributed. GPU-hours
in `train_cost.txt` are unreliable for resumed runs (only the last chunk's clock was recorded for
some of them); PFLOPs are the trainer's own count and are reliable.
