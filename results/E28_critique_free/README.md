# E28 — Does the critique in the targets matter?

**Question.** Self-guided training targets open with the critic's guidance, written before the
student's own thought and action. No experiment separated that choice from the actions of the
same episodes. What does a student trained on the same examples without the critique score?

**Answer.** No measurable difference. Judge-correct accuracy (Gemma-4-31B-it) on the 747 held-out
questions, seeds 13, 17 and 23:

| Training targets | 13 | 17 | 23 | Mean |
|---|---|---|---|---|
| Self-guided, critique in targets | 66.7 | 64.9 | 63.2 | 64.9 ± 1.7 |
| Same examples, critique removed | 64.8 | 62.9 | 65.1 | 64.3 ± 1.2 |
| Unguided self-rollouts | 62.2 | 64.8 | 62.7 | 63.2 ± 1.4 |

Seed-averaged, critique removed -> critique in targets: **+0.7** points, 95 % CI −0.8 to +2.1,
sign-flip p 0.42; unguided -> critique removed: **+1.0**, CI −0.9 to +2.9, p 0.32 (Holm 0.65 for
both). Welch over the three seeds per side: p 0.61 and 0.38. (Means here are from correct-answer
counts; `kit/summary.txt` averages rounded values.)

**Protocol.** `make_split.py` copies the self-guided split (`data/splits_self`) and removes the
`teacher_guidance` field from every target (10,485 of 13,825 training examples; planning targets
have no such field). Inputs, examples and their order are unchanged, and the rest of each target is
byte-identical. Same LoRA recipe and seeds as the self-guided students; primary judge. Pool tasks
`train_nocrit_s{13,17,23}`, `eval_*`, `judge_*`, `results_E28`.

**Also here.** `target_verdicts.py` counts verdicts on answers inside the self-guided targets: of
3,784 answer targets, 227 open with a critique calling an answer incorrect or wrong (every one of
those answers passes cover match), and in 195 the previous step had given the same answer. On
StrategyQA no target after a finish step switches its yes/no answer (27 after a negative critique,
49 otherwise).

**Files.** `kit/summary.txt`/`.json`, `kit/results.json`/`RESULTS.md`, `kit/critique_free.json`,
`kit/target_verdicts.txt`/`.json`.

**Caveats.** Three seeds per arm; the interval does not exclude a gain of about two points.
