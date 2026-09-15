# Teacher-guidance datasets: DeepSeek, GLM and self-teaching

This page documents three teacher-guidance (TG) datasets collected with this kit on the same
7,999 questions, and compares them. For each dataset it records the student, the teacher, how
the episodes were collected and judged, and every metric used. All numbers come from
`scripts/compare_teachers.py` (outputs in `runs/compare_teachers/`) and the judge verdict files
listed at the end; they were last regenerated on 2026-09-15.

In every table the column order is **Self**, **DeepSeek**, **GLM**.

## Summary

* **Same student, different teacher (Self vs DeepSeek).** Both datasets use the student
  `ibm-granite/granite-4.1-3b`. Judge-correct is 61.5 % with the student as its own
  teacher and 62.3 % with DeepSeek-V4-Flash as the teacher: DeepSeek − Self =
  +0.8 points, 95 % CI −0.3 to +1.8, McNemar p 0.141, not a significant difference. Per dataset, only StrategyQA differs
  significantly (+5.3 points, 95 % CI +3.2 to +7.3, McNemar p 1e-06); on 2WikiMultihopQA, HotpotQA and MuSiQue the confidence
  intervals include zero.
* **The rule-based metrics separate the two more than the judge does**, because the answers
  differ in form. The self-taught student's final answers have a median of 20
  words against 3 in the DeepSeek dataset, and 1 of its 1,999 StrategyQA
  answers is a bare "yes" or "no" against 895. Exact match is 9.2 % vs
  26.4 %.
* **Training yield.** The self-taught dataset yields 15,915 SFT examples from its
  rule-correct episodes, the DeepSeek dataset 16,567 (−3.9 % for Self), with most of the
  gap on StrategyQA.
* **The self-teacher is a weak grader of final answers.** Its own verdict on the final answer
  agrees with the judge in 38.6 % of episodes (DeepSeek 78.4 %, GLM 97.1 %),
  and it marks 99.96 % of judge-correct answers as incorrect. Its guidance stated the gold
  answer and was redacted in 17.4 % of guidance events (DeepSeek 7.4 %, GLM
  18.2 %). In all three datasets, no student-visible message states the gold answer.
* **GLM has the highest judge-correct score** (65.6 %; GLM − Self +4.1 points, 95 % CI +3.1 to +5.2, McNemar p < 1e-6,
  GLM − DeepSeek +3.3 points, 95 % CI +2.3 to +4.4, McNemar p < 1e-6) but it is lower than DeepSeek on StrategyQA
  (−4.3 points, 95 % CI −6.5 to −2.1, McNemar p 0.000196). Its student is `ibm-granite/granite-4.2-3b`, not 4.1, so its differences
  from the other two mix the effect of the teacher with the effect of the student.

## The three datasets

| | **Self** | **DeepSeek** | **GLM** |
|---|---|---|---|
| Location | `data/episodes_self/` (not committed) | `data/episodes/` (shipped with the kit) | `data/episodes_glm/` (not committed) |
| Student | `ibm-granite/granite-4.1-3b` | `ibm-granite/granite-4.1-3b` | `ibm-granite/granite-4.2-3b` |
| Teacher | `ibm-granite/granite-4.1-3b` (the student itself) | DeepSeek-V4-Flash: `deepseek-ai/DeepSeek-V4-Flash` (5,475 episodes) and `deepseek-ai/DeepSeek-V4-Flash-0731` (2,524 episodes) | `z-ai/glm-5.3-flash` |
| Collected (UTC, first → last episode) | 2026-09-14 18:28 → 2026-09-15 00:26 | 2026-08-30 19:35 → 2026-08-31 14:44 | 2026-09-12 14:27 → 2026-09-13 19:02 |
| Collector config hash | `dfc43e9c5a8d8f4a` | `1716bb7efcbd32d0` | `dfc43e9c5a8d8f4a` |
| Episodes | 7,999 | 7,999 | 7,999 |
| Errored episodes | 0 | 0 | 0 |
| Episodes with a judge verdict | 7,998 | 7,999 | 7,999 |

All three contain exactly the same questions (identical `qid` sets and dataset labels):
2WikiMultihopQA 2,000, HotpotQA 2,000, MuSiQue 2,000 and StrategyQA 1,999. Each episode is one
attempt at one question: the student drafts a plan that the teacher reviews, then takes up to
three tool-using steps, each reviewed by the teacher, and gives a final answer. The teacher sees
the gold answer and supporting facts; what it tells the student passes through the leakage
sanitiser (`agentsim/teacher_guidance/leakage.py`), which replaces any statement of the gold
answer with `[answer hidden]` unless the answer already appears in the question.

**Self.** One model plays both roles. `ibm-granite/granite-4.1-3b` was served by a single vLLM
server (bfloat16, context length 32,768 tokens; requests set `enable_thinking: false` in the chat
template arguments) on one GPU, and the collector called it as both student and teacher (`vllm/student` for both roles;
the ids were renamed to the model name at consolidation). Up to 32 workers ran concurrently, 8 per
dataset. Collected with `slurm/collect_local.sbatch`.

**DeepSeek.** The dataset shipped with the kit and described in `docs/DATASET.md`. The teacher was
DeepSeek-V4-Flash behind an OpenAI-compatible API; two checkpoints were used during the run and each
episode records which one. Student temperature 0.2, teacher temperature 0.1, budget 3, guidance
level 3.

**GLM.** Student `ibm-granite/granite-4.2-3b` served by vLLM (bfloat16, context length 16,384 tokens;
requests set `enable_thinking: false` in the chat template arguments, so the model's reasoning mode
was off). Teacher `z-ai/glm-5.3-flash` through OpenRouter with reasoning
effort `low`, routed over a provider fallback ladder; the providers that served the teacher were
DeepInfra in 6,724 episodes, Relace in 1,273 and both in 2 (recorded per episode in
`teacher_providers_used`).

### Collection settings

Self and GLM share collector config hash `dfc43e9c5a8d8f4a`, which covers these settings of
`scripts/collect_episodes.py`: a step budget of 3 that is not disclosed to the student; plan review
by the teacher (up to 3 planning rounds, at most 6 plan steps); guidance level 3 ("diagnostic
feedback", at most 60 words, with no tool, query, document-title or answer hints); strict leak
policy; teacher temperature 0.1 and 2,500 output tokens (5,000 on a repair retry); student
temperature 0.2 and 3,000 output tokens; retrieval over each question's own corpus. The hash
excludes the student and teacher model ids, the teacher router, the corpus path and the dataset name.

The DeepSeek dataset was collected about two weeks earlier with an earlier version of the collector
and has a different config hash (`1716bb7efcbd32d0`). Its documented settings (budget 3, guidance
level 3, student temperature 0.2, teacher temperature 0.1) match, but the episodes do not record
the full configuration, so it is not possible to list which other settings differ.

## How the datasets were judged

All three datasets were judged by the same model with the same prompt, using `scripts/judge.py`.

* **Judge model:** Gemma-4-31B-it, served as `RedHatAI/gemma-4-31B-it-FP8-block` on one
  OpenAI-compatible endpoint, with the same model on a second endpoint as the fallback for calls the
  first could not answer. Verdicts by endpoint: Self 7,979 primary / 19 fallback; DeepSeek 7,985 primary / 14 fallback; GLM 7,999 primary / 0 fallback.
* **Input:** only the question, the gold answer and the episode's final answer. The judge never sees
  the trajectory, the teacher or which dataset an answer comes from.
* **Decoding:** temperature 0, at most 600 output tokens.
* **Prompt** (the default in `scripts/judge.py`):

  ```
  You are grading one answer to a multi-hop question.

  Question: {question}
  Gold answer: {gold}
  Model answer: {answer}

  The model answer is CORRECT if it conveys the gold answer, even if worded differently,
  more verbose, or with extra correct detail. It is INCORRECT if it states something
  different, says it does not know, or is empty.
  Return ONLY a JSON object: {"correct": 0 or 1, "reason": "<10 words>"}
  ```

* **Verdict:** the last JSON object in the reply that carries a `correct` key (a reply that corrects
  itself ends with its final verdict).

**Why this judge.** Before judging, 14 candidate judge models were compared on 145 hand-labelled
question–answer pairs (86 correct, 59 incorrect answers; 15 further items were ambiguous and
excluded). Gemma-4-31B-it had 98.6 % accuracy, Cohen's κ 0.97, accepted 3.4 % of the incorrect
answers, rejected none of the correct ones, and rejected all 15 control items in which a wrong
answer was graded against a deliberately altered gold answer. Kimi-K2.6, the judge behind
`docs/RESULTS.md`, scored 94.5 % and accepted 11.9 % of incorrect answers on the same items, so
judge-correct numbers in `docs/RESULTS.md` are not directly comparable with the ones here.

**Episodes without a verdict:** `c027d949f7b4a6af5869` (StrategyQA) in the Self dataset, whose final answer is `[answer hidden]`. The judge replied that it could not grade the answer, so this episode is excluded from judge-correct and from the paired judge comparisons (which therefore use one question fewer).

## Metric definitions

Answer metrics are computed by `agentsim/teacher_guidance/metrics.py` when an episode is collected
and stored in `final_metrics`; teacher-behaviour metrics are computed by `scripts/compare_teachers.py`.

* **Judge-correct:** fraction of judged episodes the judge marked correct.
* **Rule-based correct** (`answer_correct`, the `cover_match` rule). Both answers are normalised
  (lower-cased, punctuation removed, `a`/`an`/`the` removed, `&` read as `and`). The prediction is
  accepted if (1) it equals the gold answer; or (2) the gold answer occurs as a contiguous token span
  in the prediction, where a gold answer of one token of at most 3 characters that is not a
  capitalised name (for example `no`) must be the prediction's first token; or (3) the gold has at
  least 2 content tokens and at least 60 % of them occur in the prediction (a small set of pronouns,
  copulas and name particles is ignored); or (4) the prediction is a contiguous span of a longer gold
  answer and contains a number or covers at least half of the gold's tokens; or (5) the gold is a
  single token of at least 4 characters and one of the prediction's tokens is a prefix-extension of
  it (or vice versa) covering at least 60 % of the longer token.
* **Exact match:** normalised prediction equals normalised gold.
* **Token F1:** harmonic mean of token precision and recall between the normalised prediction and
  gold (SQuAD F1).
* **Gold supporting-document recall:** gold supporting documents the student retrieved, divided by
  the number of gold supporting documents.
* **Answer grounded:** for an answer other than `yes`/`no` that has substantive content tokens, at
  least 50 % of those tokens occur in the evidence the student gathered (extracted spans and retrieved
  document text). For a `yes`/`no` answer, or one without substantive content tokens, all gold
  supporting documents were retrieved or at least one fact was extracted.
* **Steps used:** tool-using steps taken, out of the budget of 3.
* **SFT examples:** training examples that `tgd.episode_lib.build_episode_examples` produces from
  every episode whose rule-based answer is correct: one plan example if the plan passes the leakage
  gate, plus one example for each step with a tool action whose guidance and thought pass the gate.
  Counted over all 7,999 questions. `scripts/build_splits.py` additionally keeps only the trainable
  pool (about 90 % of questions) and applies further filters, so a training split contains fewer.
* **Guidance event:** the teacher's plan review plus each step the teacher reviewed.
* **Guidance redacted:** guidance events whose student-visible text stated the gold answer and was
  therefore redacted by the sanitiser (`leakage_check.gold_answer_leaked`), divided by guidance events.
* **Student-visible messages still stating the gold answer:** a re-check of the guidance the student
  actually received (step guidance and plan feedback) for statements of the gold answer, skipped when
  the gold answer appears in the question. Must be 0.
* **Plan changed:** the teacher's plan review led to a revised plan (`plan_review.metrics.plan_changed`).
* **Teacher accepted:** the episode ended with `stop_reason = teacher_accept` (the teacher judged the
  answer complete before the budget ran out); the rest end with `budget_forced_finish`.
* **Teacher's final verdict:** the teacher's own 0/1 grade of the final answer
  (`final_metrics.teacher_answer_correct`), compared with the judge verdict on the episodes where it
  is recorded.
* **Paired differences:** a comparison written `A − B` is computed on the questions that have a
  verdict (or rule-based score) in both datasets, as the mean over those questions of A's 0/1
  correctness minus B's, in percentage points. The 95 % confidence interval is a percentile bootstrap
  with 10,000 resamples (seed 13); the p-value is an exact two-sided McNemar test on the questions
  where exactly one of the two is correct (`tgd/stats.py`).

## Results

### Judge-correct

| Dataset | Self | DeepSeek | GLM |
|---|---|---|---|
| 2WikiMultihopQA | 72.8 % | 71.7 % | 78.9 % |
| HotpotQA | 70.6 % | 70.8 % | 72.8 % |
| MuSiQue | 37.5 % | 36.3 % | 44.6 % |
| StrategyQA | 65.1 % | 70.3 % | 66.1 % |
| **All** | 61.5 % | 62.3 % | 65.6 % |

### Paired differences in judge-correct

| Comparison (left − right) | Dataset | Questions | Difference (points) | 95 % CI | Only left correct / only right correct | McNemar p |
|---|---|---|---|---|---|---|
| DeepSeek − Self | 2WikiMultihopQA | 2,000 | −1.1 | [−3.2, +1.0] | 210 / 232 | 0.318 |
| DeepSeek − Self | HotpotQA | 2,000 | +0.3 | [−1.6, +2.1] | 183 / 178 | 0.833 |
| DeepSeek − Self | MuSiQue | 2,000 | −1.3 | [−3.5, +1.1] | 257 / 282 | 0.301 |
| DeepSeek − Self | StrategyQA | 1,998 | +5.3 | [+3.2, +7.3] | 270 / 165 | 1e-06 |
| DeepSeek − Self | **All** | 7,998 | +0.8 | [−0.3, +1.8] | 920 / 857 | 0.141 |
| GLM − Self | 2WikiMultihopQA | 2,000 | +6.2 | [+4.2, +8.2] | 272 / 149 | < 1e-6 |
| GLM − Self | HotpotQA | 2,000 | +2.3 | [+0.3, +4.2] | 217 / 172 | 0.0256 |
| GLM − Self | MuSiQue | 2,000 | +7.0 | [+4.7, +9.5] | 363 / 222 | < 1e-6 |
| GLM − Self | StrategyQA | 1,998 | +1.1 | [−0.9, +3.1] | 218 / 197 | 0.326 |
| GLM − Self | **All** | 7,998 | +4.1 | [+3.1, +5.2] | 1070 / 740 | < 1e-6 |
| GLM − DeepSeek | 2WikiMultihopQA | 2,000 | +7.2 | [+5.3, +9.3] | 283 / 138 | < 1e-6 |
| GLM − DeepSeek | HotpotQA | 2,000 | +2.0 | [+0.1, +4.0] | 210 / 170 | 0.0453 |
| GLM − DeepSeek | MuSiQue | 2,000 | +8.3 | [+5.9, +10.7] | 376 / 210 | < 1e-6 |
| GLM − DeepSeek | StrategyQA | 1,999 | −4.3 | [−6.5, −2.1] | 213 / 298 | 0.000196 |
| GLM − DeepSeek | **All** | 7,999 | +3.3 | [+2.3, +4.4] | 1082 / 816 | < 1e-6 |

### Paired differences in rule-based correct

| Comparison (left − right) | Dataset | Questions | Difference (points) | 95 % CI | Only left correct / only right correct | McNemar p |
|---|---|---|---|---|---|---|
| DeepSeek − Self | 2WikiMultihopQA | 2,000 | −1.4 | [−3.4, +0.7] | 204 / 231 | 0.212 |
| DeepSeek − Self | HotpotQA | 2,000 | −1.7 | [−3.7, +0.2] | 178 / 212 | 0.0946 |
| DeepSeek − Self | MuSiQue | 2,000 | −0.2 | [−2.4, +1.8] | 237 / 241 | 0.891 |
| DeepSeek − Self | StrategyQA | 1,999 | +10.6 | [+8.3, +12.9] | 400 / 189 | < 1e-6 |
| DeepSeek − Self | **All** | 7,999 | +1.8 | [+0.8, +2.9] | 1019 / 873 | 0.000853 |
| GLM − Self | 2WikiMultihopQA | 2,000 | +1.3 | [−0.9, +3.5] | 256 / 230 | 0.257 |
| GLM − Self | HotpotQA | 2,000 | +3.1 | [+1.1, +5.0] | 225 / 164 | 0.00231 |
| GLM − Self | MuSiQue | 2,000 | +8.8 | [+6.5, +11.0] | 356 / 181 | < 1e-6 |
| GLM − Self | StrategyQA | 1,999 | +7.6 | [+5.3, +9.8] | 347 / 196 | < 1e-6 |
| GLM − Self | **All** | 7,999 | +5.2 | [+4.1, +6.2] | 1184 / 771 | < 1e-6 |

### Answer metrics by dataset

#### Rule-based correct (`answer_correct`)

| Dataset | Self | DeepSeek | GLM |
|---|---|---|---|
| 2WikiMultihopQA | 70.6 % | 69.3 % | 71.9 % |
| HotpotQA | 66.5 % | 64.8 % | 69.6 % |
| MuSiQue | 30.0 % | 29.8 % | 38.7 % |
| StrategyQA | 45.0 % | 55.6 % | 52.6 % |
| **All** | 53.0 % | 54.8 % | 58.2 % |

#### Exact match

| Dataset | Self | DeepSeek | GLM |
|---|---|---|---|
| 2WikiMultihopQA | 4.2 % | 24.5 % | 8.8 % |
| HotpotQA | 27.0 % | 37.3 % | 25.9 % |
| MuSiQue | 5.6 % | 13.5 % | 6.4 % |
| StrategyQA | 0.1 % | 30.5 % | 0.9 % |
| **All** | 9.2 % | 26.4 % | 10.5 % |

#### Token F1

| Dataset | Self | DeepSeek | GLM |
|---|---|---|---|
| 2WikiMultihopQA | 0.196 | 0.385 | 0.222 |
| HotpotQA | 0.403 | 0.498 | 0.393 |
| MuSiQue | 0.154 | 0.241 | 0.174 |
| StrategyQA | 0.029 | 0.332 | 0.047 |
| **All** | 0.195 | 0.364 | 0.209 |

#### Gold supporting-document recall

| Dataset | Self | DeepSeek | GLM |
|---|---|---|---|
| 2WikiMultihopQA | 0.847 | 0.862 | 0.917 |
| HotpotQA | 0.793 | 0.807 | 0.857 |
| MuSiQue | 0.602 | 0.676 | 0.757 |
| StrategyQA | 0.802 | 0.817 | 0.839 |
| **All** | 0.761 | 0.790 | 0.843 |

#### Answer grounded in gathered evidence

| Dataset | Self | DeepSeek | GLM |
|---|---|---|---|
| 2WikiMultihopQA | 89.7 % | 81.5 % | 83.5 % |
| HotpotQA | 92.8 % | 90.1 % | 90.6 % |
| MuSiQue | 73.1 % | 74.6 % | 70.2 % |
| StrategyQA | 48.5 % | 57.0 % | 52.2 % |
| **All** | 76.0 % | 75.8 % | 74.1 % |

#### Steps used (of 3)

| Dataset | Self | DeepSeek | GLM |
|---|---|---|---|
| 2WikiMultihopQA | 2.99 | 2.92 | 2.82 |
| HotpotQA | 2.98 | 2.85 | 2.77 |
| MuSiQue | 2.99 | 2.97 | 2.75 |
| StrategyQA | 2.99 | 2.96 | 2.63 |
| **All** | 2.99 | 2.93 | 2.74 |

### Training yield

#### SFT examples from rule-correct episodes

| Dataset | Self | DeepSeek | GLM |
|---|---|---|---|
| 2WikiMultihopQA | 5,329 | 5,299 | 5,031 |
| HotpotQA | 5,166 | 4,851 | 4,956 |
| MuSiQue | 2,266 | 2,299 | 2,680 |
| StrategyQA | 3,154 | 4,118 | 2,823 |
| **All** | 15,915 | 16,567 | 15,490 |

#### SFT examples per episode

| Dataset | Self | DeepSeek | GLM |
|---|---|---|---|
| 2WikiMultihopQA | 2.66 | 2.65 | 2.52 |
| HotpotQA | 2.58 | 2.43 | 2.48 |
| MuSiQue | 1.13 | 1.15 | 1.34 |
| StrategyQA | 1.58 | 2.06 | 1.41 |
| **All** | 1.99 | 2.07 | 1.94 |

### Teacher behaviour

| All 7,999 questions | Self | DeepSeek | GLM |
|---|---|---|---|
| Guidance events redacted because they stated the gold answer | 17.4 % | 7.4 % | 18.2 % |
| Episodes with at least one redaction | 53.3 % | 22.7 % | 44.6 % |
| Student-visible messages still stating the gold answer | 0 | 0 | 0 |
| Generic fallback feedback substituted for unusable teacher output | 0.0 % | 0.1 % | 0.0 % |
| Plan changed after the teacher's plan review | 46.0 % | 74.3 % | 3.0 % |
| Episodes ended by the teacher accepting the answer | 1.1 % | 6.9 % | 9.3 % |
| …of those, judge-correct | 58.8 % | 99.5 % | 99.6 % |
| Teacher's final verdict agrees with the judge | 38.6 % | 78.4 % | 97.1 % |
| Teacher's verdict "correct" on judge-incorrect answers | 0.00 % | 0.46 % | 1.78 % |
| Teacher's verdict "incorrect" on judge-correct answers | 99.96 % | 34.47 % | 3.55 % |
| Teacher tokens per episode (prompt + output) | 5,449 | 5,503 | 5,338 |
| Student tokens per episode (plan and steps, prompt + output) | 9,074 | 11,402 | 6,354 |

#### Guidance events redacted, by dataset

| Dataset | Self | DeepSeek | GLM |
|---|---|---|---|
| 2WikiMultihopQA | 13.9 % | 3.9 % | 12.1 % |
| HotpotQA | 23.5 % | 13.3 % | 19.5 % |
| MuSiQue | 16.9 % | 6.8 % | 13.6 % |
| StrategyQA | 15.5 % | 5.7 % | 28.1 % |
| **All** | 17.4 % | 7.4 % | 18.2 % |

#### Teacher's final verdict agrees with the judge, by dataset

| Dataset | Self | DeepSeek | GLM |
|---|---|---|---|
| 2WikiMultihopQA | 27.3 % | 80.6 % | 98.3 % |
| HotpotQA | 29.5 % | 86.1 % | 97.4 % |
| MuSiQue | 62.6 % | 84.5 % | 95.5 % |
| StrategyQA | 35.0 % | 62.3 % | 97.2 % |
| **All** | 38.6 % | 78.4 % | 97.1 % |

### Form of the final answers

| Median words in the final answer | Self | DeepSeek | GLM |
|---|---|---|---|
| 2WikiMultihopQA | 17 | 6 | 18 |
| HotpotQA | 9 | 3 | 12 |
| MuSiQue | 16 | 2 | 19 |
| StrategyQA | 52 | 9 | 54 |
| **All** | 20 | 3 | 21 |

| | Self | DeepSeek | GLM |
|---|---|---|---|
| StrategyQA final answers that are exactly "yes" or "no" (of 1,999) | 1 | 895 | 26 |
| Episodes ended by `budget_forced_finish` | 7,914 | 7,448 | 7,254 |
| Episodes ended by `teacher_accept` | 85 | 551 | 745 |
| Final answers containing the placeholder `[answer hidden]` | 1 | 0 | 1 |

## What the numbers show

1. **With the student fixed, replacing DeepSeek-V4-Flash by the student itself as teacher does not
   change judge-correct significantly overall** (+0.8 points, 95 % CI −0.3 to +1.8, McNemar p 0.141). The one significant
   per-dataset difference is StrategyQA, in DeepSeek's favour (+5.3 points, 95 % CI +3.2 to +7.3, McNemar p 1e-06).
2. **The rule-based and exact-match metrics favour DeepSeek more than the judge does, and the
   difference is concentrated on StrategyQA** (rule-based: +10.6 points, 95 % CI +8.3 to +12.9, McNemar p < 1e-6). In the
   DeepSeek dataset 895 StrategyQA answers are a bare "yes" or "no"; in the self-taught
   dataset 1 is. The rule-based match requires a short gold answer such as `no` to be the
   first token of the prediction, while the judge accepts a longer answer that conveys it.
3. **Teacher behaviour differs more than outcomes.** The self-teacher changes the student's plan less
   often (46.0 % vs 74.3 %), ends episodes early less often (85 vs
   551 episodes), and its early acceptances are judge-correct in 58.8 % of
   cases vs 99.5 %. Its own final verdicts mark 99.96 % of judge-correct answers
   incorrect.
4. **Leakage control held in all three datasets.** Redaction was needed more often with the
   self-teacher (17.4 % of guidance events) and GLM (18.2 %) than with DeepSeek
   (7.4 %); in every dataset, zero student-visible messages state the gold answer.
5. **GLM** scores highest on judge-correct, has the highest gold supporting-document recall
   (0.843 vs 0.761 Self and 0.790 DeepSeek), uses the fewest steps and
   student tokens, and its teacher's final verdicts agree with the judge in 97.1 % of episodes.
   Because its student differs, these differences cannot be attributed to the teacher alone.

## Limitations

* **GLM uses a different student** (`granite-4.2-3b`), so comparisons involving GLM do not isolate
  the teacher.
* **The DeepSeek dataset was collected with a different collector configuration** (hash
  `1716bb7efcbd32d0`), and the settings that differ are not recorded in the episodes.
* **One collection run per dataset.** Student and teacher sample at temperatures 0.2 and 0.1; the
  collections were not repeated, so run-to-run variation is not measured.
* **One judge.** The verdicts come from a single model in a single pass. It was validated on 145
  labelled items, not on these datasets.
* **These are properties of the collected episodes.** Whether a student trained on the self-taught
  or GLM dataset performs as well as one trained on the DeepSeek dataset has not been measured here.

## Collection notes

* **DeepSeek:** the shipped dataset; `docs/DATASET.md` describes its construction.
* **GLM:** collected in 4-hour jobs. Episodes that errored, mostly because of provider rate limits,
  were re-collected until none remained; consolidation keeps an error-free episode for every
  question.
* **Self:** a first attempt that called the student and teacher through a shared API endpoint was
  stopped after about an hour because the endpoint was saturated; its episodes are not part of the
  dataset. The dataset was then collected on one GPU with `slurm/collect_local.sbatch` in two jobs.
  In the first, workers were killed on reaching the job's memory limit (a leak in the simulate loop,
  fixed in commit `d3464b1`), and 14 episodes errored when vLLM calls exceeded their 60-second timeout
  (raised to 300 seconds in `8215f5f`). The second job re-collected the errored questions and
  completed the rest; consolidation kept an error-free episode for every question.
* **Pending replacement:** the Self episode for StrategyQA question `c027d949f7b4a6af5869` ended with the literal placeholder `[answer hidden]` as its final answer: the student repeated the sanitiser's placeholder from the redacted guidance instead of answering. The judge cannot grade it. The episode has been moved out of the run and the question is queued for re-collection with the same setup; this page will be regenerated when the replacement is judged.

## Reproducing the comparison

```bash
# self-teaching collection on one GPU (student and teacher are the same served model)
MODEL=ibm-granite/granite-4.1-3b OUT=runs/collect_self_gpu \
  sbatch -p <partition> --gres=gpu:<type>:1 slurm/collect_local.sbatch
python scripts/consolidate_episodes.py --runs runs/collect_self_gpu --out data/episodes_self --gzip \
  --strict --expect 2wikimultihopqa=2000 --expect hotpotqa=2000 --expect musique=2000 \
  --expect strategyqa=1999 --rename-model vllm/student=ibm-granite/granite-4.1-3b

# judge every dataset with the same judge (primary endpoint first, fallback second)
for arm in self:data/episodes_self shipped:data/episodes glm:data/episodes_glm; do
  python scripts/judge.py --judge oai-<name>/<judge-model>,oai-<name2>/<judge-model> \
    --episodes ${arm#*:}/episodes.jsonl.gz --out runs/judge_${arm%%:*} --concurrency 16 --attempts 4
done

python scripts/compare_teachers.py \
  --arm self=data/episodes_self,runs/judge_self/verdicts.jsonl \
  --arm deepseek=data/episodes,runs/judge_shipped/verdicts.jsonl \
  --arm glm=data/episodes_glm,runs/judge_glm/verdicts.jsonl \
  --baseline self --out runs/compare_teachers
```

## Files

| Path | Content | In the repository |
|---|---|---|
| `data/episodes/` | DeepSeek dataset | yes |
| `data/episodes_glm/` | GLM dataset (65 MB compressed) | no |
| `data/episodes_self/` | self-taught dataset (75 MB compressed) | no |
| `runs/judge_shipped/`, `runs/judge_glm/`, `runs/judge_self/` | `verdicts.jsonl`, one verdict per episode | no (`runs/` is not tracked) |
| `runs/compare_teachers/` | `REPORT.md`, `comparison.json`, `per_question.jsonl` | no |
