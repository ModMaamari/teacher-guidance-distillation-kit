# E21 — Guidance vs no guidance, at three seeds

**Question.** E01 and E17 compared four sources of trajectories at one training seed each. Since
self-guided training varies by 1.7 points across seeds, do those comparisons hold at three?

**Answer.** Two of them change. Judge-correct accuracy (Gemma-4-31B-it) on the 747 held-out
questions, mean ± SD over seeds 13, 17 and 23; Δ is seed-averaged (each question averaged over an
arm's seeds) with a bootstrap 95 % CI and a sign-flip permutation p.

### Matched supervision (~1,400 correct episodes per arm)

| Training trajectories | Seeds 13 / 17 / 23 | Mean | Δ vs unguided |
|---|---|---|---|
| Student's own rollouts, unguided | 61.5 / 61.7 / 62.9 | 62.0 ± 0.8 | — |
| Critiqued by DeepSeek (teacher-guided) | 62.3 / 58.4 / 60.0 | 60.2 ± 1.9 | **−1.8** [−4.1, +0.5], p 0.13 |
| **Critiqued by itself (self-guided)** | 64.7 / 63.6 / 62.3 | **63.5 ± 1.2** | **+1.5** [−0.4, +3.4], p 0.13 |
| Teacher's own rollouts (plain distillation) | 67.7 / 66.9 / 70.0 | **68.2 ± 1.6** | **+6.2** [+3.6, +8.9], p 0.0001 |

### All episodes each route collected

| Training trajectories | Seeds 13 / 17 / 23 | Mean | Δ vs unguided |
|---|---|---|---|
| Student's own rollouts, unguided | 62.3 / 64.8 / 62.6 | 63.2 ± 1.4 | — |
| Teacher-guided | 62.1 / 61.6 / 62.0 | 61.9 ± 0.3 | −1.3 [−3.6, +0.9], p 0.25 |
| **Self-guided** | 66.7 / 64.9 / 63.2 | **64.9 ± 1.7** | **+1.7** [−0.2, +3.6], p 0.089 |

**Reading.**
- **Self-guidance vs the student's own unguided rollouts is smaller than one seed suggested and is
  not significant at three.** Seed 13 gave +3.2 (matched) and +4.4 (all data); across three seeds
  the differences are +1.5 and +1.7, with intervals that include zero. Seed 13 was the most
  favourable of the three in both comparisons. The sign is positive in five of six seed pairs.
- **A frontier teacher's critique still adds nothing over no guidance**, and is if anything
  slightly harmful: −1.8 matched, −1.3 with all data, and the noisiest arm of the four (SD 1.9).
  This is the E01/E17 conclusion, now on three seeds.
- **The teacher's own rollouts are clearly the best data**, +6.2 over unguided and +4.7 over
  self-guided (both p < 0.001), consistent across every seed. They need a teacher that can solve
  the training questions, and E23 prices what that costs.
- **Self-guided still beats teacher-guided** (63.5 vs 60.2 matched, 64.9 vs 61.9 with all data),
  which is the paper's headline comparison and is unchanged (E19: +3.0, p 0.015).

**Protocol.** No new data: the same splits as E01/E17, retrained with seeds 17 and 23 (the kit's
LoRA recipe, budget 3, primary judge). Pool tasks `train_sup_{selfdist,guided,selftaught,teachdist}_s{17,23}`,
`train_selfdist_full_s{17,23}`, `eval_*`, `judge_*`, `results_E21`, `results_E21full`.

**Files.** `kit/` (matched) and `full/` (all episodes): `summary.txt`/`.json` with the seed table
and paired tests, `results.json`/`RESULTS.md` per test set, and `kit/train_cost.txt` for what each
arm cost to train.

**Caveats.** Three seeds still estimate an SD from few samples. The comparisons here use the
primary judge; E18 re-graded the seed-13 arms under three other graders. Holm is applied over the
two planned contrasts of each table.

## History

- **2026-09-20:** first run (pool). It revised the single-seed self-guided advantage over unguided
  rollouts reported by E01/E17 from significant to inconclusive.
