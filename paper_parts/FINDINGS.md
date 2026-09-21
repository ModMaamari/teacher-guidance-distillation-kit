# What this project found, strongest first

Status as of 2026-09-21, 09:00. Findings are ordered by how much they should change what a
practitioner or a reviewer believes: first what the evidence supports most strongly and most
usefully, then mechanism, then the checks that make the numbers trustworthy.

**Metric.** Judge-correct accuracy on the 747 held-out questions, graded by Gemma-4-31B-it.
Differences are percentage points; intervals are paired bootstrap 95 % CIs; *p*-values are exact
McNemar, or a sign-flip permutation test where a comparison is seed-averaged. Student:
Granite-4.1-3B. Teacher: DeepSeek-V4-Flash (284B total, 13B active).

---

## 1. Imitating a capable model's own trajectories beats every form of critique — by a wide, reproducible margin

**Evidence.** At matched supervision (~1,400 episodes, three seeds) the teacher's own rollouts
train a **68.2 ± 1.6** student, against 62.0 ± 0.8 for the student's own rollouts (**+6.2**, CI +3.6
to +8.9, p 0.0001) and 63.5 ± 1.2 for self-guided ones (+4.7, p 0.0004). Collected over the *same
7,999 questions* rather than cut to the same size, the gap is identical: **71.1 ± 1.6** against
64.9 ± 1.7 (**+6.2**, CI +3.6 to +8.8, p 0.0001). Every one of six seed pairs is positive. The
teacher also wastes less collection: 76.4 % of its episodes pass the correctness filter against
53.0 %.

**Supported by.** E01 (single seed, +6.3), E21 (three seeds, matched), E24 (three seeds, full
scale), E12 (survives Holm).

**Why it matters.** It is the clearest practical recommendation in the project: if a capable model
may generate training data, have it *solve* the tasks, not critique the student. It is also the
finding that most constrains our own method's claim.

## 2. Critic strength is not what makes guidance useful — a 3B model critiquing itself beats a 284B model critiquing it

**Evidence.** Over three seeds each, self-guided trajectories train a 64.9 ± 1.7 student against
61.9 ± 0.3 for DeepSeek-guided ones: seed-averaged **+3.0** (CI +0.7 to +5.4, p 0.015), with every
self-guided seed above every teacher-guided seed, and the gap holding under four graders (+3.9 to
+4.6 at seed 13). The same ordering appears **at inference**: given the gold answer, the base
student critiquing itself answers **62.8 %** against **56.2 %** critiqued by the teacher, using
fewer tokens (10,085 vs 10,972) and no external model. A third critic, GLM-5.3-flash (320B), lands
between them at 64.3.

**Supported by.** E06, E19, E02, E18, E12 (training); E26 (inference).

**Why it matters.** It contradicts the assumption behind teacher-based distillation pipelines that
a better critic yields better supervision. What mattered was that the critic shares the student's
distribution and holds privileged information, not its capability.

## 3. A frontier teacher's step-level critique adds nothing over the student's own filtered successes

**Evidence.** At matched size, teacher-guided rollouts train a 60.2 ± 1.9 student against 62.0 ±
0.8 for unguided ones: **−1.8** (CI −4.1 to +0.5, p 0.13). With all data, 61.9 ± 0.3 against 63.2 ±
1.4 (−1.3, p 0.25). Teacher-guided is also the noisiest arm. Collecting it costs 0.284 PFLOPs per
episode against 0.099 for self-guided and 0.032 for plain rollouts — most of it spent in the critic.

**Supported by.** E01 (+0.8, p 0.67 at one seed), E17, E21 (three seeds), E23 (cost).

**Why it matters.** The most expensive component of the standard pipeline contributes nothing, at
two data scales and three seeds. This is the project's most cost-relevant negative result.

## 4. Self-improvement with no external model works, and privileged self-critique adds a few points in domain — but little beyond it

**Evidence.** Self-guided training lifts the student from 27.3 to 64.9 ± 1.7 with no external model
at collection, training or inference. Against the student's *own* filtered rollouts, six seeds per
arm give **+2.3** (64.8 ± 1.2 vs 62.5 ± 1.4, CI +0.7 to +4.0, **p 0.008**), positive in all six seed
pairs. On two external benchmarks the same twelve students give **+1.5** (MultiHop-RAG, p 0.087)
and **+0.5** (FRAMES, p 0.58), while both arms still transfer strongly over the base student
(23.7 → ~63 and 7.0 → ~29).

**Supported by.** E17 (single seed, +3.2/+4.4), E21 (three seeds, inconclusive), E25 (six seeds,
established), E27 (external benchmarks, weak).

**Why it matters, and the caution.** The headline — a small model can improve itself with no
teacher — stands. The specific claim that privileged self-critique adds signal *beyond* keeping its
own correct episodes is established in domain and is small (about a third of the way to the
teacher-rollout result), and it does not clearly transfer to new benchmarks. Self-guided collection
also costs about three times plain self-rollouts (0.099 vs 0.032 PFLOPs per episode), so those 2.3
points are bought, not free.

## 5. Building a student this way costs 2–3× less end to end than any teacher-based route

**Evidence.** Measured call by call, priced as 2 × active parameters × tokens. Collecting until
3,818 episodes pass the filter and training on them costs **1,395 PFLOPs** with Self-Guidance,
against 2,661 with a DeepSeek critic and 2,454 with GLM; plain self-rollouts cost 921 and the
teacher's own rollouts 1,602. Self-Guidance hosts 6.8 GB of weights; teacher routes need 150–290 GB
resident. Inference is identical for every trained student (2.89 steps, 4.9–5.3k tokens per
question) and training peaks at 18 GiB.

**Supported by.** E23 (measurement), E20 (training compute), E08 (teacher inference tokens).

**Why it matters.** The accuracy differences between routes are a few points; the cost differences
are factors. Any recommendation that ignores collection cost is incomplete.

## 6. Keeping only correct episodes is worth 2.3 points and half the training compute — and a cheap string test is as good as an LLM judge

**Evidence.** Training on everything collected costs **−2.3 points** (62.6 ± 0.8 vs 64.9 ± 1.7, p
0.006) while doubling training compute (1,312 vs 684 PFLOPs). At equal training-set size the loss is
as large (−3.0, p 0.0008), so it is not dilution. Doubling the unfiltered data recovers 0.7 points
(p 0.44). Replacing the string match with an LLM judge keeps 598 more episodes and trains a
*slightly worse* student (63.7 ± 1.2 vs 64.9 ± 1.7, −1.2, p 0.13) at 15 % more training compute plus
a judge call per episode collected.

**Supported by.** E20 (three seeds, both contrasts survive Holm), E22 (three seeds).

**Why it matters.** Rejection sampling is usually justified by intuition; here it is measured in
accuracy and compute, and the cheapest possible correctness test is enough.

## 7. Most of what a small agent learns from its own episodes is the protocol, not the answers

**Evidence.** Trained *only* on the 3,390 episodes that ended with a **wrong** answer, the student
reaches **58.9** against the base student's 27.3 — **+31.6 points**, 84 % of the gain of
correct-only training, while remaining 6.0 points behind it. The untrained student's main failure is
stopping: it finishes voluntarily in 2.4 % of episodes and leaves 54 % of them with no answer at
all; extra steps don't help it (27.3 / 28.1 / 26.2 at 3 / 5 / 8). On external benchmarks both
trained arms transfer nearly equally (finding 4), which is the same story from another angle.

**Supported by.** E20 (incorrect-only arm), E10 (stopping), E08 (budget), E26 (answer rates),
E27 (transfer).

**Why it matters.** It explains the large base-to-trained gap without invoking knowledge transfer,
and predicts that cheap unfiltered trajectories already teach the agent loop.

## 8. Privileged critique helps a model that cannot act on what it knows — not one that already can

**Evidence.** Given the gold answer, the base student's own critique lifts it from 27.3 to **62.8**.
The same privileged self-critique applied to the teacher changes nothing: **81.7** against **82.7**
alone, at four times the tokens (24,035 vs 5,980 per question).

**Supported by.** E26.

**Why it matters.** It bounds where this family of methods can be expected to work, and explains why
the weakest critic produced the best data (finding 2): the gain comes from the answer key
compensating for a weak policy, not from critique in general.

## 9. The trained student learns the task, not the datasets

**Evidence.** Self-guided students trained on three datasets and evaluated on every question of the
fourth gain **+25.7** (HotpotQA), **+34.6** (2Wiki), **+28.4** (MuSiQue) and **+47.9** (StrategyQA),
each CI at least 23 points above zero, beating teacher-guided folds on three of four. On two
external benchmarks never seen in any form, the trained students reach ~63 % (MultiHop-RAG, base
23.7) and ~29 % (FRAMES, base 7.0).

**Supported by.** E19 (self-guided folds), E13 (teacher-guided folds), E27 (external benchmarks).

## 10. A few hundred episodes are enough

**Evidence.** 500 collected episodes (274 correct, 1,029 training examples, 0.2 GPU-hours of
training) give 57.6 — **87 % of the gain** from all 7,252. From 1,000 episodes (60.2) to all of them
(62.1), no difference is significant.

**Supported by.** E04.

## 11. The recipe transfers to another model family, and costs about one point of general ability

**Evidence.** MiniCPM5-2B on the same data reaches 64.7, on par with Granite's 62.1 (p 0.17).
Forgetting, pooled over MMLU, GSM8K and HellaSwag: −0.84 for the teacher-guided student (p 0.037)
and −1.15 for the self-guided one (p 0.002), the latter concentrated in GSM8K (−2.81).

**Supported by.** E05, E09, E19.

## 12. Extra steps only help an agent that knows when to stop; the teacher's advantage is knowledge, not search

**Evidence.** From 3 to 5 steps the trained student gains +4.7 (Holm p 0.010) then saturates; the
base student never gains. At a **single** step the teacher alone already answers 60.0 % while
retrieving no documents, rising to 82.7 % at three steps.

**Supported by.** E08, E10.

## 13. The measurements are not artefacts of the judge or of answer style

**Evidence.** The judge was chosen from 14 candidates on labelled pairs (98.6 % accurate, κ 0.97),
agrees with a human on 94.9 % of 196 blind answers (κ 0.898), and with two other judges on 96.9 %
and 98.4 %, which rank the arms identically. Students trained on their own trajectories answer in
~20 words against 2 for DeepSeek-guided ones, yet a strict single-answer rubric moves any arm by at
most **1.4 points**, and the full-data comparisons keep sign and significance under all four
graders.

**Supported by.** E16, E03, E18.

## 14. The gains are not benchmark contamination

**Evidence.** 14 of 747 held-out questions (1.9 %) share a rare 8-gram with training examples;
removing them moves the base-to-trained gain from +36.1 to **+36.2**. On the external benchmark,
**0 of 600** MultiHop-RAG questions share a rare 8-gram with any training question.

**Supported by.** E07, E27.

## 15. At these effect sizes, three seeds are not enough — and our own single-seed results misled us twice

**Evidence.** Seed SD is 1.7 points for self-guided training against 0.3 for teacher-guided; adapter
rank is not the cause (ranks 8–64 span 2.1 points, no significant pair). Two single-seed results
moved materially: self-guided over unguided rollouts fell from +3.2/+4.4 (significant) to +1.5/+1.7
(not), and only six seeds resolved it at +2.3 (p 0.008); teacher-guided over unguided flipped from
+0.8 to −1.8. Single-seed readings of the self-vs-unguided comparison span +0.1 to +4.4.

**Supported by.** E02, E19, E21, E25, E11.

**Why it matters.** It is a methodological finding about this literature as much as about this
method: agent ablations reporting one seed at these effect sizes are not reliable, and we report
where our own were not.

## 16. Practitioner traps we hit and measured

- **A cheap correctness filter disagrees with a judge more than expected**, and that is fine: the
  string match drops 22.9 % of episodes a judge would accept and keeps 4.4 % it would reject (E20),
  yet judge-filtering trains no better a student (E22).
- **A model's accuracy depends on its serving configuration.** The same teacher scored 71.1 with a
  1,200-token output cap through one provider and 82.7 with a 6,000-token cap under this paper's
  protocol (E00 vs E08); 16 % of its step calls exceed 1,190 output tokens. Two deployments of the
  same model id also differ in success rate (76 % vs 78 % of episodes passing the filter), which is
  why E24's collection was redone on a single gateway rather than mixed.
- **A silent loss bug can leave greedy decoding intact while destroying sampling**: 61.0 % greedy
  before and after the fix, but 0 % sampled, recovering to 59.7–61.7 % (E14).
- **Guidance flatters itself at collection time.** On the same held-out questions, episodes
  collected with the teacher's critique are correct 56.1 % of the time against 52.9 % unguided, yet
  the students trained on them are no better (finding 3).
- **Evaluation directories accumulate test sets.** Aggregating an arm's whole directory silently
  pooled a new benchmark with the held-out questions in one result table (base read 20.0 instead of
  27.3) until the tooling was changed to select test sets explicitly.

---

## Still running

The three teacher-rollout students (E24) are being evaluated on MultiHop-RAG and FRAMES, to test
whether finding 1 — the largest effect in the project — also transfers to benchmarks no arm was
trained for. Expected within a few hours.

## What is not claimed

Students of 2–3B parameters, four Wikipedia-based multi-hop benchmarks plus two external ones,
short step budgets, one critique format. Self-Guidance needs gold answers at collection time.
Transfer folds and the second student family have one seed each. The live-critique, self-critique
and teacher-alone reference points are upper bounds: their critics receive the gold answer, so they
are not deployable configurations.
