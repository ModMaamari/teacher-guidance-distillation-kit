# Every experiment and what it found

Status as of 2026-10-04 (E26 revised 2026-09-24; E27 completed, E28 and E29 added 2026-09-26;
E30 added 2026-09-27; E31 added 2026-09-29; E32 added 2026-10-04). All 33 experiments are finished;
E32 on the external benchmarks is running. Each entry gives the question, the result, and what limits it.

**How to read the numbers.** The metric is **judge-correct accuracy**: the percentage of the 747
held-out questions (HotpotQA 189, 2WikiMultihopQA 170, MuSiQue 203, StrategyQA 185) whose final
answer the judge Gemma-4-31B-it marks correct. Differences are percentage points. Intervals are
paired bootstrap 95 % confidence intervals over questions; *p*-values are exact McNemar, except
"seed-averaged" tests, which average each question over an arm's seeds and use a sign-flip
permutation test. The student is Granite-4.1-3B (3.4B parameters). The teacher is
DeepSeek-V4-Flash (284B total, 13B active per token). "Correct episodes" always means the
collection-time string match (`cover_match`), not a judge, unless stated.

| ID | Question | Status |
|---|---|---|
| E00 | Does training on teacher-guided episodes lift the student? | done |
| E01 | Guidance, correctness filter or plain distillation: which ingredient? | done |
| E02 | Do results survive other training seeds? | done |
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
| E15 | How do the collections compare at collection time? | done |
| E16 | Which available model is the most accurate judge? | done |
| E17 | Is self-guidance better than no guidance? | done |
| E18 | Does answer form or the grader move the ranking? | done |
| E19 | Do seeds, transfer and forgetting hold for the self-guided student? | done |
| E20 | Does the correctness filter earn its place? | done |
| E21 | Do the supervision comparisons hold across three seeds? | done |
| E22 | Should the filter be a string match or an LLM judge? | done |
| E23 | What does each route cost end to end? | done |
| E24 | What does plain teacher distillation reach at the same scale? | done |
| E25 | Six seeds: does self-guidance beat plain self-distillation? | done |
| E26 | How well does each untrained configuration answer? | done |
| E27 | Does the self-guided advantage hold on external benchmarks? | done |
| E28 | Does the critique inside the training targets matter? | done |
| E29 | Does the gain survive removing the critic's retry channel? | done |
| E30 | Does self-guidance beat the same compute spent on more unguided attempts? | done |
| E31 | Does STaR (answer-hinted rationalization) match self-guidance? | done |
| E32 | Does outcome-reward RL (GRPO) match self-guidance at equal compute? | done |

---

## E00 — Does training on teacher-guided episodes lift the student?

Base student 27.2, base student critiqued live by the teacher 56.2, student trained on
teacher-guided episodes 63.3, teacher answering alone 71.1.

Training is worth +36.1 points, and the trained student beats the live-critique setup while using
no external model at inference.

**Caveats.** The live-critique arm gives the critic the gold answer: an upper bound, not a
deployable system. The 71.1 teacher run used a 1,200-token output cap through a different
provider; under this paper's protocol the teacher scores 82.7 (E08). One seed. The live-critique arm was
rerun under the collection protocol in E26 and scores 64.8 there; 56.2 is superseded.

## E01 — Which ingredient matters, at matched supervision?

All arms cut to ~1,400 usable episodes from the same questions, one seed: base 27.3, the student's
own unguided rollouts 61.5, teacher-guided rollouts 62.3, the teacher's own rollouts 67.7.

A strong teacher's critique is worth +0.8 over no guidance (p 0.67), i.e. nothing. Imitating the
teacher's own trajectories is worth +6.3 (p < 0.001). E21 repeated all of it with three seeds.

## E02 — Seed variance (teacher-guided data)

Seeds 13/17/23 give 62.1, 61.6, 62.0 = **61.9 ± 0.3**. No pair of seeds differs significantly.

## E03 — Is the judge measuring correctness?

A human annotator, blind to arm and verdict, agreed with the judge on **94.9 %** of 196 answers
(Cohen's κ 0.898). Two other judges re-grading all 2,988 answers of E00's arms agree with it on
96.9 % (Kimi-K2.6, κ 0.937) and 98.4 % (Qwen3.6-35B, κ 0.968) and rank the arms identically.

**Caveats.** One annotator; the sample is balanced on the judge's verdict, so κ describes a
deliberately hard mix.

## E04 — How much data is needed?

Nested subsets of teacher-guided episodes, one seed each: 500 episodes 57.6, 1,000 60.2, 2,000
60.0, 4,000 61.3, all 7,252 62.1. **500 collected episodes give 87 % of the full gain**; from 1,000
on, no difference is significant.

## E05 — Does it work for another student?

MiniCPM5-2B on the same teacher-guided data: 2.4 → **64.7**, against Granite's 62.1 (p 0.17). The
2.4 is real: the MiniCPM base model almost never emits `finish` (728 of 747 episodes end with no
answer), so most of its lift is the agent protocol. The trained-vs-trained comparison is the
informative one. **Caveat.** Teacher-guided data only.

## E06 — Does critic strength decide data quality?

Same student, same questions, three critics, one seed: self-critique **66.7**, GLM-5.3-flash 64.3,
DeepSeek-V4-Flash 62.1; base 27.3. The weakest critic — the 3B student itself, holding the gold
answer — produced the best data. **Caveat.** The GLM collection used a different actor
(Granite-4.2-3B), so its row is not strictly comparable.

## E07 — Is it contamination?

14 of 747 held-out questions (1.9 %) share a rare 8-gram with training examples. Removing them
moves base → trained from +36.1 to **+36.2**. Flagged questions are easier for every arm including
the untrained base (35.7 % vs 27.0 %), which points to shared Wikipedia source text.

## E08 — Does the 3-step budget decide the outcome?

| Agent | B=1 | B=3 | B=5 | B=8 |
|---|---|---|---|---|
| base student | 0.5 | 27.3 | 28.1 | 26.2 |
| trained student (teacher-guided, seed 13) | 10.3 | 62.1 | 66.8 | 67.3 |
| teacher alone | 60.0 | 82.7 | 85.0 | 85.8 |

More steps help the trained student to five (+4.7 from 3 to 5, Holm p 0.010) and never help the
base student. At one step the teacher already answers 60.0 % while retrieving no documents —
knowledge, not search. Tokens per question grow from 1.4–4.8k at one step to 13–15k at eight.
**`teacher_b3` (82.7) is this paper's teacher-alone reference.**

## E09 — What did training cost in general ability?

Teacher-guided student vs base weights, greedy: MMLU 63.51 → 63.27 (−0.23, p 0.76), GSM8K 89.16 →
88.40 (−0.76, p 0.39), HellaSwag 75.27 → 73.67 (−1.60, p 0.029); pooled over 4,529 items
**−0.84 points** (p 0.037).

## E10 — What does late stopping cost?

Episodes the agent ends itself are far more often correct, but few end that way: the base student
finishes voluntarily in 2.4 % of episodes, the trained student 11.0 %, the teacher 24.0 %. When the
budget ends an episode with no answer, accuracy is 10.6 % (base). This is why extra steps don't
help the base student (E08): it fails to commit, not to retrieve.

## E11 — Does adapter capacity matter?

LoRA rank 8/16/32/64: 61.2 / 61.7 / 62.1 / 63.3 — 2.1 points apart, no significant pair.

## E12 — Do the p-values survive correction?

Holm and Benjamini-Hochberg over every pairwise test within each results table (16 families). All
gains over the base student survive Holm. Among trained arms, the teacher's own rollouts over
unguided and teacher-guided rollouts survive Holm; single-seed self-guided advantages survived only
BH and were later revised by E21 and E25.

## E13 — Transfer to an unseen dataset (teacher-guided data)

Fold students train on three datasets, evaluated on every question of the fourth: HotpotQA 47.1 →
69.0 (+21.9), 2Wiki 38.9 → 71.3 (+32.4), MuSiQue 11.7 → 32.8 (+21.1), StrategyQA 15.9 → 65.3
(+49.4). One seed per fold.

## E14 — Can the trained student be sampled?

The first adapter trained at the wrong logit scale decoded correctly greedily but produced nothing
usable when sampled. After the fix, on 300 held-out questions: greedy 61.0 % before and after;
temperature 0.7 nucleus 0.0 → 59.7 %; temperature 0.3 min-p 0.1 0.0 → 61.7 %. Next-token entropy
went from 10.9 with 1.2 % of mass on valid tokens to 0.22 with 100 %.

## E15 — How do the collections compare at collection time?

Over the 7,999 collection questions: self-guided episodes are judged correct 61.5 % of the time,
DeepSeek-guided 62.3 % (+0.8, CI −0.2 to +1.8) — tied. The self-critic is a much worse grader of
final answers (agrees with the judge on 38.6 % of its verdicts against 78.4 %) and states the
answer more often (17.5 % of guidance events redacted against 7.4 %).

## E16 — Which judge?

14 candidates on 145 labelled pairs. Gemma-4-31B-it: **98.6 %** accurate, κ 0.97, accepting 3.4 % of
incorrect answers and rejecting no correct one. Kimi-K2.6 (the first judge of E00/E13) scores 94.5 %
and accepts 11.9 % of incorrect answers, which is why everything was re-judged.
**Caveat.** These reference labels came from an AI assistant, so they select the judge only; its
validity rests on E03.

## E17 — Is self-guidance better than no guidance?

Matched size, one seed: unguided 61.5, self-guided **64.7** (+3.2, p 0.031), teacher-guided 62.3.
All data, one seed: unguided 62.3, self-guided **66.7** (+4.4, p 0.003), teacher-guided 62.1.
**Superseded by E21 and E25:** seed 13 was the most favourable of six; the six-seed estimate is
+2.3.

## E18 — Does answer form or the grader move the ranking?

Every arm re-graded four ways (primary judge, a strict single-answer rubric, Kimi-K2.6,
Qwen3.6-35B). Students trained on their own trajectories answer in ~20 words, DeepSeek-guided ones
in 2. The strict rubric moves any arm by at most **1.4 points**. With all data, self-guided beats
teacher-guided by +3.9 to +4.6 and unguided by +3.4 to +4.7 under all four graders; the matched-size
advantage keeps its sign under all four (+2.3 to +3.2) but is significant only under the primary
judge. **Caveat.** Seed 13 only, and E21/E25 later showed that seed was favourable.

## E19 — Robustness of the self-guided student

**Seeds.** Self-guided 66.7 / 64.9 / 63.2 = **64.9 ± 1.7**; teacher-guided 62.1 / 61.6 / 62.0 =
**61.9 ± 0.3**. Paired per seed: +4.5 (p 0.010), +3.4 (p 0.046), +1.2 (p 0.51). Seed-averaged
**+3.0** (CI +0.7 to +5.4, p 0.015). Every self-guided seed beats every teacher-guided seed.
**Transfer.** Self-guided folds on their unseen dataset: 72.5 (+25.7), 73.3 (+34.6), 40.6 (+28.4),
64.8 (+47.9); better than teacher-guided folds on three of four datasets.
**Forgetting.** Pooled −1.15 points (p 0.002), concentrated in GSM8K (−2.81).

## E20 — Does the correctness filter earn its place?

Same self-guided episodes, only the filter changed; three seeds except where noted:

| Training episodes | Episodes | Examples | Train PFLOPs | Accuracy | vs correct only |
|---|---|---|---|---|---|
| **correct only (the method)** | 3,818 | 13,825 | 684 | **64.9 ± 1.7** | — |
| correct and incorrect, all | 7,208 | 26,610 | 1,312 | 62.6 ± 0.8 | **−2.3**, p 0.006 |
| correct and incorrect, size-matched | 3,642 | 13,828 | 682 | 61.9 ± 0.8 | **−3.0**, p 0.0008 |
| incorrect only (one seed) | 3,390 | 12,785 | 628 | 58.9 | −6.0 |

Dropping the filter costs 2.3 points **and doubles training compute**; at equal size the loss is as
large, so it is not dilution. Training only on failed episodes still reaches 58.9 (+31.6 over base),
84 % of the gain. **Caveat.** The filter is a string match: it drops 22.9 % of episodes the judge
would accept and keeps 4.4 % it would reject.

## E21 — Do the supervision comparisons hold across three seeds?

Matched size (~1,400 episodes), three seeds:

| Training trajectories | Seeds 13 / 17 / 23 | Mean | vs unguided |
|---|---|---|---|
| unguided self-rollouts | 61.5 / 61.7 / 62.9 | 62.0 ± 0.8 | — |
| teacher-guided rollouts | 62.3 / 58.4 / 60.0 | 60.2 ± 1.9 | −1.8, p 0.13 |
| **self-guided rollouts** | 64.7 / 63.6 / 62.3 | **63.5 ± 1.2** | +1.5, p 0.13 |
| teacher's own rollouts | 67.7 / 66.9 / 70.0 | **68.2 ± 1.6** | **+6.2**, p 0.0001 |

All data: unguided 63.2 ± 1.4, teacher-guided 61.9 ± 0.3, self-guided 64.9 ± 1.7 (+1.7, p 0.089).
This revised two single-seed results: a frontier teacher's critique is not merely useless but
slightly negative, and the self-guided advantage over filtered self-rollouts was inconclusive at
three seeds (resolved by E25).

## E22 — String filter or LLM-judge filter?

| Filter | Episodes kept | Examples | Train PFLOPs | Accuracy |
|---|---|---|---|---|
| **cover match (the kit's filter, free)** | 3,818 | 13,825 | 684 | **64.9 ± 1.7** |
| LLM judge | 4,416 | 15,960 | 790 | 63.7 ± 1.2 |

Seed-averaged **−1.2** (CI −2.7 to +0.3, p 0.13), negative in all three seeds. The 598 extra
episodes the judge admits — right answer, loose wording — cost 15 % more training compute plus a
judge call on every episode collected, and buy nothing.

## E23 — What does each route cost end to end?

Measured call by call over every collected episode; compute ≈ 2 × active parameters × tokens:

| Route | Actor tokens in/out | Critic tokens in/out | PFLOPs/episode | Total PFLOPs to build a student |
|---|---|---|---|---|
| unguided self-rollouts | 4,013 / 728 | — | 0.032 | **921** |
| **self-guided (ours)** | 5,260 / 1,239 | 6,674 / 1,350 (3.4B) | 0.099 | **1,395** |
| teacher's own rollouts | 3,956 / 3,224 (13B active) | — | 0.187 | **1,602** |
| teacher-guided (GLM) | 4,220 / 959 | 5,484 / 1,029 (18B) | 0.270 | **2,454** |
| teacher-guided (DeepSeek) | 6,733 / 1,371 | 6,875 / 1,926 (13B) | 0.284 | **2,661** |

"Total" is collecting until 3,818 episodes pass the filter plus 684 PFLOPs of training. Training
peaks at 18 GiB for every route; inference is identical across trained students (2.89 steps,
4.9–5.3k tokens per question). A first pass reported 0.221 for teacher-guided collection by
counting only step calls; the plan-review calls are the teacher's, giving 0.284.

## E24 — Plain teacher distillation at the same scale

The teacher answers the **same 7,999 questions** with no critic; correct episodes train three
students:

| Training trajectories | Episodes kept | Examples | Seeds 13 / 17 / 23 | Mean |
|---|---|---|---|---|
| Self-guided (ours) | 3,818 | 13,825 | 66.7 / 64.9 / 63.2 | **64.9 ± 1.7** |
| **Teacher's own rollouts** | 5,533 | 15,805 | 71.8 / 72.3 / 69.2 | **71.1 ± 1.6** |

Seed-averaged **+6.2** (CI +3.6 to +8.8, p 0.0001) — the same gap as at matched size, so it is about
whose actions are imitated, not the extra episodes. The teacher also wastes less: 76.4 % of its
episodes pass the filter against 53.0 %. Collected through a single gateway (verified in
`provider_split.txt`).

## E25 — Six seeds: self-guidance vs plain self-distillation

| Arm | 13 | 17 | 23 | 29 | 31 | 37 | Mean |
|---|---|---|---|---|---|---|---|
| **Self-guided** | 66.7 | 64.9 | 63.2 | 63.6 | 64.9 | 65.2 | **64.8 ± 1.2** |
| Unguided self-rollouts | 62.3 | 64.8 | 62.6 | 62.0 | 60.6 | 62.4 | **62.5 ± 1.4** |

Seed-averaged **+2.3** (CI +0.7 to +4.0, **p 0.008**), positive in all six seed pairs. At three seeds
the same comparison was +1.7 with p 0.089: the estimate barely moved, the interval shrank. Single
seeds of this comparison range from +0.1 to +4.4.

## E26 — Every untrained way of answering

| Configuration | Judge-correct | Answered | Tokens/question |
|---|---|---|---|
| Base student alone | 27.3 | 45.8 % | — |
| **Base student + its own critique (sees gold)** | **62.8** | 100 % | 10,085 |
| Base student + teacher critique (sees gold) | 64.8 | 100 % | 21,392 |
| *Base student + teacher critique, E00 setup (superseded)* | *56.2* | *99.6 %* | *10,972* |
| **Teacher alone** | **82.7** | 98.9 % | 5,980 |
| Teacher + its own critique (sees gold) | 81.7 | 99.2 % | 24,035 |

At inference the two critics of the base student cannot be told apart: its own privileged critique
gives 62.8 against 64.8 for the teacher's, −2.0 (CI −5.1 to +1.1, McNemar p 0.23), with half the
tokens. The same critique does nothing for the teacher (81.7 vs 82.7, p 0.44) at four times the
tokens. Rows 2–6 need the gold answer, so they are upper bounds. Row 1 answers only 45.8 % of the
time, so it is not directly comparable with the others.

**Revised 2026-09-24.** The teacher-critique row first came from E00, run through another provider
with the student served by a different stack, and read 56.2, which made self-critique look +6.6
better. Rerun under E26's own protocol (vLLM student, harness defaults, one gateway for the whole
arm), the same arm scores 64.8, +8.6 over the E00 run (p 4e-6). The inference-time advantage of
self-critique does not survive a like-for-like comparison.

## E27 — Do the results hold on external benchmarks?

The same fifteen students (six self-guided, six unguided, three trained on teacher rollouts), no
retraining, on two benchmarks no arm was trained for:

| Benchmark | Base | Unguided (6 seeds) | Self-guided (6 seeds) | Teacher rollouts (3 seeds) | Self vs unguided |
|---|---|---|---|---|---|
| In domain (E25, E24) | 27.3 | 62.5 ± 1.4 | **64.8 ± 1.2** | **71.1 ± 1.6** | **+2.3**, p 0.008 |
| MultiHop-RAG (news, 600 q) | 23.7 | 62.2 ± 1.7 | 63.7 ± 0.8 | **66.5 ± 2.0** | +1.5, p 0.087 |
| FRAMES (Wikipedia, 598 q) | 7.0 | 29.2 ± 1.2 | 29.7 ± 0.9 | 30.6 ± 0.8 | +0.5, p 0.58 |

The direction is consistent, the size is not: the self-guided increment is largely in-domain. Both
trained arms transfer strongly over the base student, so what transfers is the agent protocol.
MultiHop-RAG shares a rare 8-gram with **0 of 600** training questions.

The teacher-rollout lead shrinks out of domain too: +2.8 over self-guided on MultiHop-RAG (CI +0.0
to +5.6, p 0.045) and +0.9 on FRAMES (p 0.44), against +6.2 in domain. **Caveats.** ~600 questions each (±1.6 points), evaluation only, one judge.
Conversion details, and the two defects the smoke test caught, are in the experiment's README.

## E28 — Does the critique inside the training targets matter?

Self-guided targets open with the critic's guidance, then the student's thought and action. Same
examples, same order, critique field removed (10,485 of 13,825 targets), three seeds:

| Training targets | 13 | 17 | 23 | Mean |
|---|---|---|---|---|
| Self-guided, critique in targets | 66.7 | 64.9 | 63.2 | **64.9 ± 1.7** |
| Same examples, critique removed | 64.8 | 62.9 | 65.1 | **64.3 ± 1.2** |
| Unguided self-rollouts | 62.3 | 64.8 | 62.6 | 63.2 ± 1.4 |

Seed-averaged, critique removed → critique in targets **+0.7** (CI −0.8 to +2.1, p 0.42). The
critique text is not what the student learns from; the gain lives in *which* trajectories the
critique produced. **Caveat.** Three seeds; the interval allows up to about two points.

## E29 — Does the gain survive removing the critic's retry channel?

The critic can reject a `finish` during collection and let the episode go on; at inference a finish
always ends it. 507 kept self-guided episodes contain such a rejection. Two ways to remove it,
three seeds each:

| Training data | Examples | 13 | 17 | 23 | Mean | Train PFLOPs | Voluntary finish |
|---|---|---|---|---|---|---|---|
| Self-guided, full | 13,825 | 66.7 | 64.9 | 63.2 | **64.9 ± 1.7** | 684 | 11.1 % |
| Episodes with a rejected finish dropped | 11,985 | 63.3 | 64.7 | 66.7 | **64.9 ± 1.7** | 595 | 1.6 % |
| Rejected-finish target and the next dropped | 12,888 | 64.4 | 64.4 | 64.4 | **64.4 ± 0.0** | 623 | 1.8 % |
| Unguided self-rollouts | 13,510 | 62.3 | 64.8 | 62.6 | 63.2 ± 1.4 | 602 | 6.5 % |

Full → episodes dropped **−0.0** (CI −1.5 to +1.4, p 1.00); full → targets dropped **−0.5** (CI −2.0
to +0.9, p 0.50). Both intervals exclude a loss the size of the whole six-seed gain (+2.3), so the
retry channel does not produce it, and the clean variant trains on 13 % less compute. What changes
is behaviour: nine in ten early-finish targets in the full data are finishes the critic rejected
(520 against 55 accepted), and without them the student almost stops finishing early (11.1 % →
1.6 %), using about 4 % more tokens. The identical 64.4 for three seeds is a coincidence (different
adapters that disagree on 78–92 questions). **Caveat.** Three seeds; against unguided the variants
give +1.6 (p 0.083) and +1.2 (p 0.25), as the full arm did at three seeds (+1.7, p 0.089).

## E30 — Self-guidance against the same compute spent on more unguided attempts

Self-guided collection costs about three unguided rollouts per episode. Two more unguided attempts
per question (temperature 0.7, over the same 7,999 questions) make three, for 768 PFLOPs of
collection against self-guidance's 790; with training, the `first` build costs 1,478 against
1,474. Correct episodes only, as always:

| Training data | Questions | Seeds | Mean | Self-guided lead |
|---|---|---|---|---|
| **Self-guided** | 3,818 | 6 | **64.8 ± 1.2** | — |
| First correct of three attempts (`first`) | 4,440 | 6 | 62.8 ± 0.5 | **+2.0** (CI +0.4 to +3.6, **p 0.017**, Holm 0.017) |
| `first` cut to 3,818 episodes (`match`) | 3,818 | 3 | 63.3 ± 0.6 | +1.5 (p 0.12) |
| Every correct attempt, ~3× the data (`all`) | 4,440 | 3 | 63.4 ± 1.0 | +1.3 (p 0.15) |
| One unguided attempt (E25) | 3,753 | 6 | 62.5 ± 1.4 | +2.3 (p 0.008) |

Welch over the twelve per-seed accuracies of self-guided and `first`: p 0.010; self-guided leads at
five of six seeds. Three attempts solve more trainable questions at least once (61.2 % against
53.0 % for one self-guided episode; 863 questions only the attempts solve, 264 only self-guidance),
yet the extra 687 solved questions add +0.3 points over one attempt (p 0.61). Self-guidance is
better than the same compute spent on more self-samples; what it adds is different trajectories,
not more solved questions. Out of domain the lead keeps its direction but not its significance:
self-guided over `first` +1.1 on MultiHop-RAG (p 0.19) and +0.6 on FRAMES (p 0.52), no primary
contrast surviving Holm, as in E27. **Caveats.** `match` and `all` have three seeds each.

## E31 — STaR: correct attempts plus answer-hinted rationalizations

STaR keeps the model's correct attempts, retries every failed question with the gold answer as a
hint, and trains on the hinted episodes that end correct with the hint removed. Here a hinted step
is kept only if nothing it wrote names the answer before a retrieved document does.

| Training data | Questions | Build PFLOPs | Seeds | Mean | Self-guided lead |
|---|---|---|---|---|---|
| **Self-guided** | 3,818 | 1,474 | 6 | **64.8 ± 1.2** | — |
| STaR, 2 iterations | 7,000 | 2,725 | 6 | 64.0 ± 1.3 | +0.8 (CI −1.1 to +2.6, p 0.42) |
| STaR, 1 iteration | 6,971 | 1,367 | 3 | 63.0 ± 0.6 | +1.7 (p 0.092; Welch over seeds 0.026) |
| Unguided self-rollouts | 3,753 | 859 | 6 | 62.5 ± 1.4 | +2.3 (p 0.008) |

At equal compute STaR trails by 1.7; at 1.85 times the compute by 0.8; neither is significant, and
STaR-2 is not significantly above unguided rollouts either (+1.5, p 0.080). Rationalization solves
97.8 % of the failed questions, so STaR trains on nearly twice the questions -- and, as in E30, more
solved questions do not buy accuracy. **Caveats.** In domain only; STaR-1 has three seeds; the
grounding gate is stricter than STaR's.

## E32 — Outcome-reward RL (GRPO) at self-guidance's compute

GRPO from the base student: 32 questions × 8 episodes per round sampled under the evaluation
protocol, rewarded by answer F1, one on-policy step per round; adapters published at 1,474 PFLOPs
(self-guidance's whole build) and 2,948.

| Training | Build PFLOPs | Seeds | Mean | vs self-guided |
|---|---|---|---|---|
| **RL, equal compute** | 1,474 | 3 | **69.2 ± 1.6** | **+4.5** (CI +2.1 to +6.8, p 0.0002, Holm 0.0002) |
| **RL, twice the compute** | 2,948 | 3 | **70.8 ± 1.0** | +6.1 (p 0.0001) |
| Self-guided | 1,474 | 6 | 64.8 ± 1.2 | — |
| Unguided self-rollouts | 859 | 6 | 62.5 ± 1.4 | −2.3 |
| *Teacher rollouts (E24)* | 2,233 | 3 | 71.1 ± 1.6 | +6.2 |

RL beats self-guidance at every seed and on every dataset, and at twice the compute reaches the
teacher's own rollouts with no teacher. Not a judge artefact: the length-insensitive cover match
agrees (63.6–67.2 vs 60.6–63.2), and the judge is, if anything, stricter with RL's one-word answers.
It also uses 27 % fewer tokens per question at inference.

**It took three versions.** v1 rewarded the cover match and was reward-hacked (verbose answers
containing the gold string) and collapsed: 0.0 / 0.0 / 9.1 %. v2 rewarded F1 but sampled in the
collection harness, whose final-step grammar forces a finish, and never learned to finish under
evaluation: 0.4 / 5.5 %. v3 samples under the evaluation protocol and gates on a dev evaluation at
round 15 (all seeds passed: dev F1 0.13 → 0.53–0.58). **Caveats.** Three seeds; in domain (external
benchmarks queued); one configuration, untuned; RL starts from the base student.

---

## Where the numbers live

Each experiment publishes to `results/E<NN>_<name>/` with `results.json`, `RESULTS.md` and a
`README.md` stating the question, the answer, the protocol and the caveats.
`experiments/registry.yaml` maps every experiment to its folder, status and paper section.
