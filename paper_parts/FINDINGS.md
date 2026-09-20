# What this project found, strongest first

Status as of 2026-09-20. Findings are ordered by how much they change what a practitioner or a
reviewer should believe: first the ones that answer the question the project set out to ask, then
the ones that explain the mechanism, then the ones that establish the numbers can be trusted.

**Metric.** Judge-correct accuracy on the 747 held-out questions, graded by Gemma-4-31B-it.
Differences are percentage points, intervals are paired bootstrap 95 % CIs, *p*-values are exact
McNemar unless a seed-averaged permutation test is named. Student: Granite-4.1-3B. Teacher:
DeepSeek-V4-Flash (284B total, 13B active).

---

## 1. Critic strength is not what makes guidance useful — a 3B model critiquing itself beats a 284B model critiquing it

**Evidence.** Over three training seeds, students trained on self-guided trajectories reach
64.9 ± 1.7 against 61.9 ± 0.3 for DeepSeek-guided trajectories. Averaging each question over the
three seeds of each arm gives **+3.0 points** (CI +0.7 to +5.4, permutation p 0.015). Every
self-guided seed (lowest 63.2) beats every teacher-guided seed (highest 62.1). At seed 13 the gap
holds under four different graders (+3.9 to +4.6, all p ≤ 0.033). A third critic, GLM-5.3-flash
(320B), lands in between at 64.3.

**Supported by.** E06 (three critics), E19 (three seeds, paired), E02 (teacher-guided seed
variance), E18 (four graders), E12 (correction).

**Why it matters.** It contradicts the assumption behind teacher-based distillation pipelines that
a better critic yields better training data. What mattered here was that the critic shares the
student's distribution and holds privileged information (the gold answer), not its capability.

## 2. The teacher's own trajectories are the best training data, by a wide margin

**Evidence.** At matched supervision (~1,400 usable episodes per arm, three seeds), students
trained on the teacher's own rollouts reach **68.2 ± 1.6**, against 62.0 ± 0.8 for the student's own
rollouts (**+6.2**, CI +3.6 to +8.9, p 0.0001) and 63.5 ± 1.2 for self-guided ones (+4.7, p 0.0004).
Every seed pair is positive. They achieve this with fewer training examples (4,189 vs ~5,250),
because the teacher solves questions in fewer steps.

**Supported by.** E01 (single seed, +6.3), E21 (three seeds), E12 (survives Holm).

**Why it matters.** It is the practical recommendation whenever a capable teacher may generate
training data: imitate what the teacher *does*, do not have it critique the student. E23 prices
that choice, and E24 (running) tests it at full scale.

## 3. A frontier teacher's step-level critique adds nothing over the student's own filtered successes

**Evidence.** At matched size, teacher-guided rollouts train a student of 60.2 ± 1.9 against
62.0 ± 0.8 for the student's own unguided rollouts: **−1.8** (CI −4.1 to +0.5, p 0.13). With all
data, 61.9 ± 0.3 against 63.2 ± 1.4 (−1.3, p 0.25). Teacher-guided is also the noisiest arm of the
four. Collecting it costs 2.9× the compute of self-guided collection, most of it spent in the
critic.

**Supported by.** E01 (+0.8, p 0.67 at one seed), E17, E21 (three seeds), E23 (cost).

**Why it matters.** The expensive component of the standard pipeline is the one that contributes
nothing. This holds across three seeds and two data scales, and it is the most cost-relevant
negative result in the project.

## 4. Self-improvement without any external model works, but its advantage over plain self-distillation is small and unproven

**Evidence.** Self-guided training lifts the student from 27.3 to 64.9 ± 1.7 using no external
model at collection, training or inference. Against the student's *own* unguided,
correctness-filtered rollouts, however, the advantage is **+1.5 points** at matched size
(CI −0.4 to +3.4, p 0.13) and **+1.7** with all data (CI −0.2 to +3.6, p 0.089) — neither
significant over three seeds.

**Supported by.** E17 (+3.2 and +4.4 at seed 13, both significant), E21 (three seeds, revised),
E19 (seed spread 1.7 points).

**Why it matters, and a caution.** The headline that a small model can improve itself stands, but
the specific claim that *privileged self-critique* adds signal beyond simply keeping its own
correct episodes does not survive three seeds. Our own single-seed result (seed 13) was the most
favourable of three. This is recorded in the paper's abstract, §4.2 and limitations rather than
left as published.

## 5. Building a student this way is 2–3× cheaper end to end than any teacher-based route

**Evidence.** Measured call by call, then priced as 2 × active parameters × tokens. Collecting
until 3,818 episodes pass the filter and training on them costs **1,395 PFLOPs** with
Self-Guidance, against 2,661 with a DeepSeek critic and 2,454 with GLM; the student's own unguided
rollouts cost 921 and the teacher's own rollouts 1,602. Per episode, teacher-guided collection
costs 0.284 PFLOPs against 0.099. Self-Guidance hosts 6.8 GB of weights; the teacher routes need
150–290 GB resident because any expert can be selected for any token. Inference is identical for
every trained student (2.89 steps, 4.9–5.3k tokens per question), and training peaks at 18 GiB.

**Supported by.** E23 (measurement), E20 (training compute), E08 (teacher inference tokens).

**Why it matters.** The accuracy differences between routes are a few points; the cost differences
are factors. Any recommendation that ignores collection cost is incomplete.

## 6. The correctness filter is worth 2.3 points and halves the training bill

**Evidence.** Training on every collected episode instead of only the correct ones costs
**−2.3 points** (62.6 ± 0.8 vs 64.9 ± 1.7, CI −3.9 to −0.7, p 0.006) while doubling training
compute (1,312 vs 684 PFLOPs, 26,610 vs 13,825 examples). At equal training-set size the loss is as
large (−3.0, p 0.0008), so it is not dilution — the failures teach wrong answers. Doubling the
unfiltered data recovers only 0.7 points (p 0.44).

**Supported by.** E20 (three seeds, two contrasts, both survive Holm).

**Why it matters.** Rejection sampling is usually justified by intuition; here it is measured, in
both accuracy and compute, and the collection cost is identical either way because the failures are
collected regardless.

## 7. Most of what a small agent learns from its own episodes is the protocol, not the answers

**Evidence.** A student trained *only* on the 3,390 episodes that ended with a **wrong** answer
reaches **58.9** against the base student's 27.3 — **+31.6 points**, 84 % of the gain that
correct-only training delivers, while remaining 6.0 points behind it. Separately, the untrained
student's main failure is not retrieval but stopping: it finishes voluntarily in 2.4 % of episodes,
and when the budget ends an episode with no answer, accuracy is 10.6 %. After training, 11.0 % of
episodes end voluntarily.

**Supported by.** E20 (incorrect-only arm), E10 (stopping behaviour), E08 (base student gains
nothing from more steps: 27.3 / 28.1 / 26.2 at 3 / 5 / 8).

**Why it matters.** It explains the large base-to-trained gap without invoking knowledge transfer,
and it predicts that cheap, unfiltered trajectory data is enough to teach the agent loop, while
correctness is what buys the last few points.

## 8. The trained student learns the task, not the datasets

**Evidence.** Self-guided students trained on three datasets and evaluated on every question of the
fourth gain **+25.7** (HotpotQA), **+34.6** (2Wiki), **+28.4** (MuSiQue) and **+47.9** (StrategyQA)
over the base student, each CI at least 23 points above zero. They beat teacher-guided fold students
on three of four datasets (72.5 vs 69.0, 73.3 vs 71.3, 40.6 vs 32.8) and trail by 0.5 on StrategyQA.

**Supported by.** E19 (self-guided folds), E13 (teacher-guided folds, +21.1 to +49.4).

**Why it matters.** The gains are not memorisation of a dataset's question style, and transfer is at
least as good without any teacher. One seed per fold.

## 9. A few hundred episodes are enough

**Evidence.** 500 collected episodes (274 correct, 1,029 training examples, 0.2 GPU-hours of
training) give 57.6, which is **87 % of the gain** from all 7,252. From 1,000 episodes (60.2) to all
of them (62.1), no difference is significant.

**Supported by.** E04 (nested subsets, one seed per size).

**Why it matters.** The method is reachable for anyone with a single GPU and a few hours, and
collection budget is not the binding constraint.

## 10. The recipe transfers to another model family, and costs about one point of general ability

**Evidence.** MiniCPM5-2B trained on the same data reaches 64.7, on par with Granite's 62.1
(p 0.17). Forgetting, pooled over MMLU, GSM8K and HellaSwag: −0.84 points for the teacher-guided
student (p 0.037) and −1.15 for the self-guided one (p 0.002), the latter concentrated in GSM8K
(−2.81).

**Supported by.** E05 (second family), E09 and E19 (forgetting).

**Why it matters.** The result is not a quirk of one checkpoint, and the price in general ability is
small but real and worth stating.

## 11. Extra steps only help an agent that knows when to stop; the teacher's advantage is knowledge, not search

**Evidence.** From 3 to 5 steps the trained student gains +4.7 (Holm p 0.010) and then saturates
(67.3 at 8); the base student never gains (27.3 / 28.1 / 26.2). At a **single** step the teacher
alone already answers 60.0 % correctly while retrieving no documents, rising to 82.7 at three steps.

**Supported by.** E08 (budget sweep), E10 (stopping).

**Why it matters.** It separates two things usually conflated in agent evaluations: how well a model
searches, and how much it already knows.

## 12. The measurements are not artefacts of the judge or of answer style

**Evidence.** The judge was selected from 14 candidates on labelled pairs (98.6 % accurate, κ 0.97),
agrees with a human on 94.9 % of 196 blind answers (κ 0.898), and agrees with two other judges on
96.9 % and 98.4 %, which rank the arms identically. Students trained on their own trajectories
answer in ~20 words against 2 for DeepSeek-guided ones, yet a strict single-answer rubric moves any
arm by at most **1.4 points**, and the full-data comparisons keep sign and significance under all
four graders.

**Supported by.** E16 (selection), E03 (human labels, swap judges), E18 (strict rubric, four
graders).

**Why it matters.** The central comparisons do not depend on one grader's leniency toward verbose
answers — the most likely objection to LLM-judged agent evaluations.

## 13. The gains are not benchmark contamination

**Evidence.** 14 of 747 held-out questions (1.9 %) share a rare 8-gram with training examples.
Removing them moves the base-to-trained gain from +36.1 to **+36.2**. The flagged questions are
easier for every arm including the untrained base (35.7 % vs 27.0 %).

**Supported by.** E07.

## 14. Self-guided training is less stable across seeds, and single-seed ablations misled us

**Evidence.** Seed SD is 1.7 points for self-guided training against 0.3 for teacher-guided. Adapter
rank is not the cause (ranks 8–64 span 2.1 points with no significant pair). Two single-seed
results later moved materially: self-guided over unguided rollouts fell from +3.2/+4.4 (significant)
to +1.5/+1.7 (not), and teacher-guided over unguided flipped from +0.8 to −1.8.

**Supported by.** E02, E19 (seed spreads), E21 (revisions), E11 (rank).

**Why it matters.** It is a methodological finding about this literature as much as about this
method: at these effect sizes, single-seed agent ablations are not reliable, and we report where our
own were not.

## 15. Practitioner traps we hit and measured

**A cheap correctness filter disagrees with a judge more than expected.** The string match drops
22.9 % of episodes a judge would accept (right answer, different wording) and keeps 4.4 % it would
reject (E20). Whether a judge-based filter trains a better student is E22, still running.

**A model's accuracy depends on its serving configuration.** The same teacher scored 71.1 with a
1,200-token output cap through one provider and 82.7 with a 6,000-token cap under the paper's
protocol (E00 vs E08), and 16 % of its step calls exceed 1,190 output tokens.

**A silent loss bug can leave greedy decoding intact while destroying sampling.** Training at the
wrong logit scale gave 61.0 % greedy both before and after the fix, but 0 % when sampled, recovering
to 59.7–61.7 % afterwards (E14).

**Guidance measured at collection time flatters itself.** On the same held-out questions, episodes
collected with the teacher's critique are correct 56.1 % of the time against 52.9 % unguided
(string match) — the critique helps the *episode*, yet the students trained on those episodes are
no better (finding 3).

---

## Open questions, being answered now

- **E22 (running).** Does filtering with an LLM judge (4,447 episodes kept) beat the string match
  (3,841)? This is the one untested lever in finding 6.
- **E24 (running).** Does the teacher's rollout advantage (finding 2) hold when collected over the
  same 7,999 questions as every other route? The teacher keeps ~78 % of its episodes against 53 %,
  so it will also have more training data, and the write-up will report this next to the
  size-controlled result rather than in place of it.

## What is not claimed

Students of 2–3B parameters, four Wikipedia-based multi-hop benchmarks and short step budgets.
Self-Guidance needs gold answers at collection time. Transfer folds and the second student family
have one seed each. The live-critique and teacher-alone reference points are upper bounds: the live
critic receives the gold answer, so they are not deployable configurations.
