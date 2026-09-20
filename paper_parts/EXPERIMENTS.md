# Every experiment and what it found

Status as of 2026-09-20. Each entry states the question, the result and the caveats that limit it.

**How to read the numbers.** The metric is **judge-correct accuracy**: the percentage of the 747
held-out questions (HotpotQA 189, 2WikiMultihopQA 170, MuSiQue 203, StrategyQA 185) whose final
answer the judge Gemma-4-31B-it marks correct. Differences are in percentage points. Intervals are
paired bootstrap 95 % confidence intervals over questions and *p*-values are exact McNemar tests,
unless stated otherwise. The student is Granite-4.1-3B; the teacher is DeepSeek-V4-Flash, a 284B
mixture-of-experts model with 13B parameters active per token. "Correct episodes" always means the
collection-time string match (`cover_match`), not a judge.

| ID | Question | Status |
|---|---|---|
| E00 | Does training on teacher-guided episodes lift the student? | done |
| E01 | Guidance, correctness filter or plain distillation: which ingredient? | done |
| E02 | Do the results survive other training seeds? | done |
| E03 | Does a human agree with the judge, and does another judge? | done |
| E04 | How much guided data is needed? | done |
| E05 | Does the recipe work for another small student? | done |
| E06 | Does a stronger critic produce better data? | done |
| E07 | Is the gain benchmark contamination? | done |
| E08 | Does the conclusion depend on the 3-step budget? | done |
| E09 | What did training cost in general ability? | done |
| E10 | How much accuracy does late stopping cost? | done |
| E11 | Does adapter capacity (LoRA rank) matter? | done |
| E12 | Do the p-values survive multiple-comparison correction? | done |
| E13 | Does a trained student transfer to an unseen dataset? | done |
| E14 | Can the trained student be sampled? | done |
| E15 | How do the three collections compare at collection time? | done |
| E16 | Which available model is the most accurate judge? | done |
| E17 | Is self-guidance better than no guidance? | done |
| E18 | Does answer form or the grader move the ranking? | done |
| E19 | Do seeds, transfer and forgetting hold for the self-guided student? | done |
| E20 | Does the correctness filter earn its place? | done |
| E21 | Do the supervision comparisons hold across three seeds? | done |
| E23 | What does each route cost end to end? | done |
| E22 | Should the filter be a string match or an LLM judge? | **running** |
| E24 | What does plain teacher distillation reach on the same 7,999 questions? | **running** |

---

## E00 — Does training on teacher-guided episodes lift the student?

Four arms on the held-out questions: base student 27.2, base student critiqued live by the teacher
56.2, student trained on teacher-guided episodes 63.3, teacher answering alone 71.1.

Training is worth +36.1 points over the untrained student, and the trained student (63.3) beats the
live-critique setup (56.2) while using no external model at inference.

**Caveats.** The live-critique arm gives the critic the gold answer, so 56.2 is an upper bound, not
a deployable system. The 71.1 teacher run used a 1,200-token output cap through a different
provider; under the paper's protocol the teacher scores 82.7 (E08). One seed.

## E01 — Which ingredient matters, at matched supervision?

All arms cut to about 1,400 usable (correct) episodes from the same questions, one seed:
base 27.3, student's own unguided rollouts 61.5, teacher-guided rollouts 62.3, the teacher's own
rollouts 67.7.

A strong teacher's critique of the student's rollouts is worth +0.8 over no guidance at all
(CI −2.4 to +3.9, p 0.67) — that is, nothing. Imitating the teacher's own trajectories is worth
+6.3 (p < 0.001). E21 repeated all of this with three seeds.

## E02 — Seed variance (teacher-guided data)

Seeds 13, 17, 23 give 62.1, 61.6, 62.0, i.e. **61.9 ± 0.3**. Teacher-guided training is stable
across seeds. No pair of seeds differs significantly.

## E03 — Is the judge measuring correctness?

A human annotator, blind to arm and verdict, agreed with the judge on **94.9 %** of 196 answers
(Cohen's κ 0.898). Two other judges re-grading all 2,988 answers of E00's arms agree with it on
96.9 % (Kimi-K2.6, κ 0.937) and 98.4 % (Qwen3.6-35B, κ 0.968), and produce the same ranking of arms.

**Caveats.** One annotator. The sample is balanced on the judge's verdict by design, so κ describes
a deliberately hard mix.

## E04 — How much data is needed?

Nested subsets of teacher-guided episodes, one seed each: 500 episodes 57.6, 1,000 60.2, 2,000
60.0, 4,000 61.3, all 7,252 62.1.

500 collected episodes (274 of them correct, 1,029 training examples) already give **87 % of the
full gain**. From 1,000 episodes on, no difference is significant. Self-improvement of this kind
needs hundreds, not tens of thousands, of episodes.

## E05 — Does it work for another student?

MiniCPM5-2B on the same teacher-guided data: base 2.4 → trained **64.7**, against Granite's 62.1
(p 0.17). The 2.4 is not a typo: the MiniCPM base model almost never emits the `finish` action
(728 of 747 episodes end without an answer), so most of its lift is the agent protocol being
learned. The trained-vs-trained comparison is the informative one.

**Caveat.** Tested with teacher-guided data only, not self-guided.

## E06 — Does critic strength decide data quality?

Same student, same questions, three critics, one seed (13): self-critique **66.7**, GLM-5.3-flash
64.3, DeepSeek-V4-Flash 62.1; base 27.3.

The weakest critic (the 3B student itself, given the gold answer) produced the best data. E19 and
E21 repeated this across seeds.

**Caveat.** The GLM collection used Granite-4.2-3B as the actor, so its row is not strictly
comparable.

## E07 — Is it contamination?

14 of the 747 held-out questions (1.9 %) share a rare 8-gram with training examples. Removing them
moves base → trained from +36.1 to **+36.2** points. The flagged questions are easier for every
arm, including the untrained base (35.7 % vs 27.0 %), which points to shared Wikipedia source text
rather than leaked answers.

## E08 — Does the 3-step budget decide the outcome?

Judge-correct at budgets 1 / 3 / 5 / 8:

| Agent | B=1 | B=3 | B=5 | B=8 |
|---|---|---|---|---|
| base student | 0.5 | 27.3 | 28.1 | 26.2 |
| trained student (teacher-guided, seed 13) | 10.3 | 62.1 | 66.8 | 67.3 |
| teacher alone | 60.0 | 82.7 | 85.0 | 85.8 |

More steps help the trained student up to five (+4.7 from 3 to 5, Holm-corrected p 0.010) and never
help the base student. At one step the teacher already answers 60 % correctly while retrieving no
documents, which is knowledge rather than search. Tokens per question grow from 1.4–4.8k at one
step to 13–15k at eight. **`teacher_b3` (82.7) is the paper's teacher-alone reference.**

## E09 — What did training cost in general ability?

Teacher-guided student vs base weights, greedy: MMLU 63.51 → 63.27 (−0.23, p 0.76), GSM8K 89.16 →
88.40 (−0.76, p 0.39), HellaSwag 75.27 → 73.67 (−1.60, p 0.029); pooled over 4,529 items
**−0.84 points** (p 0.037).

## E10 — What does late stopping cost?

Episodes the agent ends itself are far more often correct than episodes the budget ends, but few
end that way: the base student finishes voluntarily in 2.4 % of episodes, the trained student in
11.0 %, the teacher in 24.0 %. When the budget ends an episode with no answer at all, accuracy
collapses to 10.6 % (base). This is why the base student gains nothing from extra steps (E08): its
failure is not retrieving badly but never committing.

## E11 — Does adapter capacity matter?

LoRA rank 8 / 16 / 32 / 64: 61.2 / 61.7 / 62.1 / 63.3. The spread is 2.1 points with no significant
pair, so rank is not the limiting factor. Rank 32 is used everywhere else.

## E12 — Do the p-values survive correction?

Holm and Benjamini-Hochberg applied to every pairwise test within each results table (16 families).
Every gain of a trained student over the base survives Holm. Among comparisons between trained
arms: the teacher's own rollouts over unguided and teacher-guided rollouts survive Holm; the
self-guided advantages that were significant at one seed survive only the weaker BH correction and
were later revised by E21.

## E13 — Does it transfer to an unseen dataset? (teacher-guided data)

Fold students train on three datasets and are evaluated on every question of the fourth:

| Unseen dataset | Base | Fold student | Δ |
|---|---|---|---|
| HotpotQA | 47.1 | 69.0 | +21.9 |
| 2WikiMultihopQA | 38.9 | 71.3 | +32.4 |
| MuSiQue | 11.7 | 32.8 | +21.1 |
| StrategyQA | 15.9 | 65.3 | +49.4 |

The students learn the task, not the datasets. One seed per fold.

## E14 — Can the trained student be sampled?

The first adapter was trained with a loss that read the wrong logit-scaling field for this
architecture. It decoded correctly greedily but produced nothing usable when sampled. After the
fix, on 300 held-out questions: greedy 61.0 % before and after; temperature 0.7 with nucleus
sampling 0.0 → 59.7 %; temperature 0.3 with min-p 0.1 0.0 → 61.7 %. The next-token distribution
went from entropy 10.9 with 1.2 % of its mass on valid tokens to entropy 0.22 with 100 %. Every
student in the paper uses the fixed loss.

## E15 — How do the collections compare at collection time?

Over the 7,999 collection questions: self-guided episodes are judged correct 61.5 % of the time,
DeepSeek-guided 62.3 % (difference +0.8, CI −0.2 to +1.8) — statistically tied. The self-critic is
a much worse grader of final answers than the teacher (it agrees with the judge on 38.6 % of its
verdicts against 78.4 %) and states the answer more often (17.5 % of its guidance events are
redacted against 7.4 %). Its value is the step-level critique, not grading.

## E16 — Which judge?

14 candidate judges on 145 labelled question-answer pairs. Gemma-4-31B-it was the most accurate:
**98.6 %**, κ 0.97, accepting 3.4 % of incorrect answers and rejecting none of the correct ones.
Kimi-K2.6, the judge behind E00's and E13's first run, scores 94.5 % and accepts 11.9 % of
incorrect answers, which is why everything was re-judged with Gemma.

**Caveat.** These reference labels were produced with an AI assistant, so they select the judge;
the judge's validity rests on E03's human labels.

## E17 — Is self-guidance better than no guidance?

Matched size (one seed): unguided 61.5, self-guided **64.7** (+3.2, CI +0.4 to +6.0, p 0.031),
teacher-guided 62.3. All data (one seed): unguided 62.3, self-guided **66.7** (+4.4, CI +1.7 to
+7.2, p 0.003), teacher-guided 62.1.

**Superseded in part by E21**: with three seeds these advantages shrink to +1.5 and +1.7 and are no
longer significant. Seed 13, reported here, was the most favourable of the three.

## E18 — Does answer form or the grader move the ranking?

Every arm re-graded four ways (primary judge, the same judge with a strict single-answer rubric,
Kimi-K2.6, Qwen3.6-35B). Students trained on their own trajectories answer in about 20 words,
DeepSeek-guided ones in 2.

The strict rubric moves any arm by at most **1.4 points** (self-guided 66.7 → 66.0). At full data,
self-guided beats teacher-guided by +3.9 to +4.6 and unguided by +3.4 to +4.7 under all four
graders. The matched-size self-guided advantage keeps its sign under all four (+2.3 to +3.2) but is
significant only under the primary judge. Verbosity is not what earns the score.

**Caveat.** Seed 13 only; E21 later showed that seed was favourable.

## E19 — Robustness of the self-guided student

**Seeds.** Self-guided 66.7 / 64.9 / 63.2 = **64.9 ± 1.7**, teacher-guided 62.1 / 61.6 / 62.0 =
**61.9 ± 0.3**. Paired per seed: +4.5 (p 0.010), +3.4 (p 0.046), +1.2 (p 0.51). Averaging each
question over the three seeds of each arm: **+3.0** (CI +0.7 to +5.4, permutation p 0.015). Every
self-guided seed beats every teacher-guided seed.

**Transfer.** Self-guided fold students on their unseen dataset: HotpotQA 72.5 (+25.7),
2WikiMultihopQA 73.3 (+34.6), MuSiQue 40.6 (+28.4), StrategyQA 64.8 (+47.9). They beat the
teacher-guided folds on three of four datasets and trail by 0.5 on StrategyQA.

**Forgetting.** Pooled over MMLU, GSM8K and HellaSwag: **−1.15 points** (p 0.002), concentrated in
GSM8K (−2.81, p 0.0003).

## E20 — Does the correctness filter earn its place?

Same self-guided episodes, only the filter changed; three seeds except where noted:

| Training episodes | Episodes | Examples | Train PFLOPs | Accuracy | vs correct only |
|---|---|---|---|---|---|
| none (base student) | — | — | — | 27.3 | — |
| **correct only (the method)** | 3,818 | 13,825 | 684 | **64.9 ± 1.7** | — |
| correct and incorrect, all | 7,208 | 26,610 | 1,312 | 62.6 ± 0.8 | **−2.3** [−3.9, −0.7], p 0.006 |
| correct and incorrect, size-matched | 3,642 | 13,828 | 682 | 61.9 ± 0.8 | **−3.0** [−4.7, −1.2], p 0.0008 |
| incorrect only (one seed) | 3,390 | 12,785 | 628 | 58.9 | −6.0 [−8.3, −3.7] |

Dropping the filter costs 2.3 points **and doubles the training compute**. At equal training-set
size the loss is as large, so it is not dilution: the failures teach wrong answers. Training only on
failed episodes still reaches 58.9 (+31.6 over the base), which is 84 % of the gain — most of what
self-guided data teaches is the agent protocol.

**Caveat.** The filter is the string match: of the episodes it drops, 22.9 % are judged correct;
of those it keeps, 4.4 % are judged wrong. E22 tests a judge-based filter.

## E21 — Do the supervision comparisons hold across three seeds?

Same splits as E01/E17, retrained with seeds 17 and 23. Matched size (~1,400 episodes):

| Training trajectories | Seeds 13 / 17 / 23 | Mean | vs unguided (seed-averaged) |
|---|---|---|---|
| unguided self-rollouts | 61.5 / 61.7 / 62.9 | 62.0 ± 0.8 | — |
| teacher-guided rollouts | 62.3 / 58.4 / 60.0 | 60.2 ± 1.9 | −1.8 [−4.1, +0.5], p 0.13 |
| **self-guided rollouts** | 64.7 / 63.6 / 62.3 | **63.5 ± 1.2** | +1.5 [−0.4, +3.4], p 0.13 |
| teacher's own rollouts | 67.7 / 66.9 / 70.0 | **68.2 ± 1.6** | **+6.2** [+3.6, +8.9], p 0.0001 |

All data: unguided 63.2 ± 1.4, teacher-guided 61.9 ± 0.3, self-guided 64.9 ± 1.7 (+1.7, CI −0.2 to
+3.6, p 0.089).

This revised two earlier single-seed results: self-guided over the student's own filtered rollouts
is **not established** (+1.5 to +1.7, not significant), and a frontier teacher's critique is not
merely useless but slightly negative (−1.8) and the noisiest arm. What holds is self-guided over
teacher-guided, and the teacher's own rollouts ahead of everything.

## E23 — What does each route cost end to end?

Measured call by call over every collected episode, priced as 2 × active parameters × tokens:

| Route | Actor tokens in/out | Critic tokens in/out | PFLOPs/episode | Total PFLOPs to build a student |
|---|---|---|---|---|
| unguided self-rollouts | 4,013 / 728 | — | 0.032 | **921** |
| **self-guided (ours)** | 5,260 / 1,239 | 6,674 / 1,350 (3.4B) | 0.099 | **1,395** |
| teacher's own rollouts | 3,956 / 3,224 (13B active) | — | 0.187 | **1,602** |
| teacher-guided (GLM) | 4,220 / 959 | 5,484 / 1,029 (18B) | 0.270 | **2,454** |
| teacher-guided (DeepSeek) | 6,733 / 1,371 | 6,875 / 1,926 (13B) | 0.284 | **2,661** |

"Total" is collecting until 3,818 episodes pass the filter (a route that fails more often must
collect more) plus 684 PFLOPs of training. Teacher-guided collection costs 2.7–2.9× self-guided per
episode. Training peaks at 18 GiB either way and inference is identical across trained students
(2.89 steps, 4.9–5.3k tokens per question).

**Correction this experiment produced.** A first pass counted only step calls and reported 0.221
PFLOPs per teacher-guided episode. Walking every call showed the plan-review calls are the
teacher's, giving 0.284.

## E22 — String filter or LLM-judge filter? *(running)*

The same self-guided episodes filtered two ways: the string match keeps 3,841 trainable episodes,
the judge keeps 4,447 (779 of them episodes the string match rejects). Three seeds each. Trainings
were 82–96 % complete at 15:51 on 2026-09-20; no results yet.

## E24 — Plain teacher distillation on the same questions *(running)*

The teacher's own rollouts over **the same 7,999 questions** as every other collection, no
guidance, one gateway. 2,990 of 7,999 episodes collected at 15:51 on 2026-09-20. At the observed
78 % keep rate this yields about 6,200 usable episodes against 3,818 for self-guided, so the result
will be reported next to the size-controlled comparison of E01/E21 rather than instead of it.

---

## Where the numbers live

Every experiment publishes to `results/E<NN>_<name>/`, containing `results.json` (per arm and test
set), `RESULTS.md`, and a `README.md` with the question, the answer, the protocol and the caveats.
`experiments/registry.yaml` maps each experiment to its folder, status and paper section.
