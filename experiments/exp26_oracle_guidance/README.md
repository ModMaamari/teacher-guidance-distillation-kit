# exp26 — Every untrained way of answering, including self-critique with the answer key

**Why.** The paper's reference points are incomplete. It reports the base student alone (27.3 %),
the base student critiqued live by the teacher (56.2 %) and the teacher alone (82.7 %), but not the
two configurations a reader will ask about: the student critiquing *itself* with the gold answer,
and the teacher critiquing itself the same way. The first is the method's own collection-time
setting measured under evaluation; the second asks whether privileged self-critique helps a model
that is already strong.

**Design.** Both agents answer the same 747 held-out questions with the same harness, budget 3, and
a critic that is the agent itself holding the gold answer (the collection protocol), then the
episodes are judged with the primary judge.

| Arm | Agent | Critic | Exists before this experiment |
|---|---|---|---|
| base student alone | Granite-4.1-3B | none | yes (evaluation) |
| **base student + self-critique** | Granite-4.1-3B | itself, sees gold | **new** |
| base student + teacher critique | Granite-4.1-3B | DeepSeek, sees gold | yes (E00) |
| teacher alone | DeepSeek-V4-Flash | none | yes (E08) |
| **teacher + self-critique** | DeepSeek-V4-Flash | itself, sees gold | **new** |

**A comparability warning this experiment exists to make visible.** These arms do not all end their
episodes the same way. On the held-out questions the base student, evaluated alone, fails to emit a
finish action in 550 of 747 episodes and leaves 405 answers empty, while the same model under the
collection harness answers every episode. Some of the gap between 27.3 % and the guided arms is
therefore about whether an answer was produced at all, not about the guidance. `reference_table.py`
prints an "answered" column for every arm so the comparison is made with that in view.

Every arm whose critic sees the gold answer is an upper bound, not a deployable system.

**Run.** Pool tasks `prep_e26` (a questions directory of only the held-out questions),
`oracle_self_student` (GPU), `oracle_self_teacher` (API, queued behind E24's collection so the two
do not compete for the endpoint), `cons_e26`, `judge_oracle_*`, `results_E26`.

**Cost.** The student arm is one GPU job of about 1-2 hours. The teacher arm is roughly 747
episodes with the model in both roles, about 16k tokens per episode, which is a few US dollars at
current rates.
