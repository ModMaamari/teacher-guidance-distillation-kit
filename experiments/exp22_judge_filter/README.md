# exp22 — Should the correctness filter be a string match or an LLM judge?

**Why.** Every split keeps episodes whose final answer *covers* the gold answer, a string test with
no LLM (`tgd.metrics.cover_match`). E20 showed the filter is worth 2.3 points, and that this cheap
test drops 22.9 % of episodes the judge would accept (right answer, different wording) while
keeping 4.4 % it would reject. So: does filtering with the judge instead train a better student,
and what does that filter cost?

**Design.** The same self-guided episodes, filtered two ways, three seeds each:

| Arm | Filter | Trainable episodes kept |
|---|---|---|
| `cover` | cover match, the kit's filter (free) | 3,841 |
| `judgefilt` | Gemma-4-31B-it verdicts on the collected episodes | 4,447 |

The judge verdicts already exist (`runs/judge_self`, every collected episode judged), so the only
new cost is training. The judge's own cost is priced per episode in E23, because a route that
filters with an LLM pays for judging every episode it collects, not only the ones it keeps.

**Run.** `prep_e22` builds `data/splits_self_judge` (`build_splits.py --keep judge
--judge-verdicts`), then `train_judgefilt_s{13,17,23}`, `eval_*`, `judge_*`, `results_E22`.
