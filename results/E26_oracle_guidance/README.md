# E26 — Every untrained way of answering, including self-critique with the answer key

**Question.** How well does each untrained configuration answer the held-out questions, and does
privileged self-critique help a strong model the way it helps a small one?

**Answer.** It helps the small model enormously and the strong model not at all, and for the small
model it is as good as the teacher's critique, not better. Judge-correct
accuracy (Gemma-4-31B-it) on the 747 held-out questions:

| Configuration | Judge-correct | Answered | Steps | Tokens/question |
|---|---|---|---|---|
| Base student alone | 27.3 | 45.8 % | 2.97 | — |
| **Base student + its own critique (sees gold)** | **62.8** | 100 % | 2.99 | 10,085 |
| Base student + teacher critique (sees gold) | 64.8 | 100 % | 2.88 | 21,392 |
| *Base student + teacher critique, E00 setup (superseded)* | *56.2* | *99.6 %* | *2.95* | *10,972* |
| Teacher alone | **82.7** | 98.9 % | 2.89 | 5,980 |
| **Teacher + its own critique (sees gold)** | 81.7 | 99.2 % | 2.89 | 24,035 |

**Reading.**
- **A small model's own privileged critique is as good as a 284B teacher's critique of it**: 62.8
  against 64.8, −2.0 (CI −5.1 to +1.1, McNemar p 0.23), with half the tokens (10,085 vs 21,392).
  Unlike training (E06, E19), where self-guided data beats teacher-guided data, at inference the
  two critics cannot be told apart. `kit/comparisons.json` has the paired tests.
- **Privileged self-critique does nothing for the strong model**: 81.7 against 82.7 alone, while
  quadrupling tokens per question (24,035 vs 5,980); −1.1, p 0.44. Critique helps a model that cannot reliably
  act on what it knows, not one that already can.
- **Part of the base student's 27.3 is not capability but commitment.** Alone it leaves 54 % of
  episodes with no answer at all; under the collection protocol, where an answer is forced, the
  same model reaches 62.8 with its own critique. Rows 2-5 answer ~100 % of the time and are
  comparable with each other; row 1 is not directly comparable with them.
- Every row except the first requires the gold answer at inference, so they are upper bounds, not
  deployable systems.

**Protocol.** The two new arms run the collection harness (budget 3, a critic that is the agent
itself holding the gold answer) over the 747 held-out questions, then are judged like every other
arm. Pool tasks `prep_e26`, `oracle_self_student`, `oracle_self_teacher`, `cons_e26`,
`judge_oracle_*`, `results_E26`.

**Files.** `kit/reference.txt`/`.json`.

**Caveats.** One run per configuration (no seeds: nothing is trained here). The critic sees the
gold answer, which is how the collection protocol works but not how anything deployable works.

## History

- **2026-09-24: teacher-critique arm rerun under this experiment's protocol.** The row first came
  from E00, run through another provider with the student served by a different stack (56.2),
  which made self-critique look +6.6 points better. Pool task `oracle_teacher_student` reran it
  like the self-critique arm: vLLM student, harness defaults, DeepSeek-V4-Flash-0731 as critic
  through one gateway for the whole arm (747/747 episodes, none errored), judged by the primary
  judge. It scores 64.8, +8.6 over the E00 run (p 4e-6). A first attempt through the other gateway
  stopped after 55 episodes when that account ran out of credit; those episodes were set aside,
  not mixed in. E00's run stays in the table, marked superseded.

- **2026-09-21:** first run. The teacher self-critique row was first published empty because the
  consolidation step ran before that collection had finished; it was rebuilt and re-judged.
