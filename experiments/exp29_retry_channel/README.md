# exp29 — Does the gain survive removing the critic's retry channel?

**Why.** During collection the critic may reject a `finish` and let the episode continue. At
inference a `finish` always ends the episode, so two things follow. First, targets that critique a
rejected finish describe states the deployed student never reaches. Second, on yes/no and
two-candidate questions a rejection is close to being told the answer: "not that one" leaves one
option. 507 of the 3,818 kept self-guided episodes (13 %) contain a rejected finish.

**Design.** Same episodes, same recipe, three seeds each; only the retry channel is removed, two
ways (`build_splits.py --retry`):

| Variant | Training data | Examples | Questions |
|---|---|---|---|
| full (existing) | every kept self-guided episode | 13,825 | 3,818 |
| `drop-episodes` | episodes containing a rejected finish removed | 11,985 | 3,315 |
| `drop-targets` | the rejected-finish target and the one after it removed | 12,888 | 3,815 |

Compared against the full self-guided students and the unguided ones (three seeds each), with the
seed-averaged paired test and Holm over the two planned contrasts.

**What each outcome means, written before the runs.**
- *Both variants hold the self-guided level:* the retry channel is not what produced the gain, and
  the cleaner variant should become the method.
- *Both drop to the unguided level:* the gain came from oracle retries, and the paper must say so.
- *Only `drop-episodes` drops:* the effect is about which questions are kept, not about the
  targets, and the size change (−503 questions) has to be controlled before concluding.

**Run.** Pool tasks `prep_e29`, `train_retry_{episodes,targets}_s{13,17,23}`, `eval_*`, `judge_*`,
`results_E29`.
