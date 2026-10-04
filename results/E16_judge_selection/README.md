# E16 — Choosing the judge

**Question.** Which available model grades final answers most accurately?

**Answer.** Gemma-4-31B-it, the most accurate model other than the teacher: 98.6 % accuracy, Cohen's κ 0.97, accepts 3.4 % of incorrect answers and
rejects none of the correct ones; Kimi-K2.6, the judge behind E00 and E13, scores 94.5 % and accepts
11.9 % of incorrect answers. `scores.json` has all 14 deployments (13 models; Gemma-4-31B-it on two endpoints). DeepSeek-V4-Flash-0731,
the teacher, graded all 145 correctly but is not used as the judge, because its own answers are among
those graded.

**Protocol.** 145 question–answer pairs with known labels (86 correct, 59 incorrect), drawn from
GLM-dataset answers: an easy set (exact matches, verbose yes/no answers, answers swapped between
questions, and 15 control items graded against a deliberately altered gold answer) and a hard set
(answers containing the gold, near misses, yes/no answers that do not lead with the verdict); 15
ambiguous items were excluded. Each model graded every item with the kit's judge prompt
(`scripts/judge.py`), temperature 0, up to 2,000 output tokens. `calls.jsonl` has every call;
`score.py` computes `scores.json`. Two endpoints served the models (`endpoint_a`, `endpoint_b`).

**Caveat — the labels were assigned by the AI assistant that built the benchmark, not by a
human.** That makes this a model-selection study, not a validation of the judge; E03 adds human
labels.

**Source.** Scratch benchmark run on 2026-09-14, preserved here.
