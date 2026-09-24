# E27 — Does the self-guided advantage hold on external benchmarks?

**Question.** E25 established, over six seeds, that self-guided trajectories train a better student
than the student's own correctness-filtered rollouts: +2.3 points on the four benchmarks the
trajectories were collected from. Does that advantage appear on benchmarks no arm was trained for?

**Answer.** Only weakly. The same twelve students (six self-guided, six unguided) were evaluated,
without retraining, on two external multi-hop benchmarks. Judge-correct accuracy (Gemma-4-31B-it):

| Benchmark | Base | Unguided (6 seeds) | Self-guided (6 seeds) | Teacher rollouts (3 seeds) | Self vs unguided |
|---|---|---|---|---|---|
| In domain (E25, E24) | 27.3 | 62.5 ± 1.4 | **64.8 ± 1.2** | **71.1 ± 1.6** | **+2.3** [+0.7, +4.0], p 0.008 |
| MultiHop-RAG (news, 600 q) | 23.7 | 62.2 ± 1.7 | 63.7 ± 0.8 | **66.5 ± 2.0** | +1.5 [−0.1, +3.1], p 0.087 |
| FRAMES (Wikipedia, 598 q) | 7.0 | 29.2 ± 1.2 | 29.7 ± 0.9 | 30.6 ± 0.8 | +0.5 [−1.1, +2.1], p 0.58 |

Against the self-guided students, the teacher-rollout students gain **+2.8** on MultiHop-RAG
(CI +0.0 to +5.6, p 0.045) and +0.9 on FRAMES (p 0.44); against the unguided ones, +4.3
(p 0.0025) and +1.4 (p 0.25).

**Reading.**
- **The direction is consistent, the size is not.** Self-guided is ahead on both external
  benchmarks, but by +1.5 and +0.5 rather than +2.3, and neither reaches significance on ~600
  questions. The advantage of privileged self-critique over plain rejection sampling looks
  partly specific to the distribution the trajectories came from.
- **The teacher-rollout advantage transfers better than the self-critique one.** It keeps its lead
  over both other arms on MultiHop-RAG (+2.8 over self-guided, p 0.045; +4.3 over unguided,
  p 0.0025) and points the same way on FRAMES, where all three arms sit within 1.4 points. The
  ordering of the three data sources is the same out of domain as in it, only compressed.
- **Training itself transfers very well.** Both trained arms lift the base student enormously on
  data they never saw: 23.7 → ~63 on MultiHop-RAG and 7.0 → ~29 on FRAMES. What transfers is the
  agent protocol, which both arms learn; what does not clearly transfer is the extra increment
  self-critique adds on top.
- **FRAMES is hard for models this size** (base 7.0, trained ~30), so its interval is wide relative
  to the effect; MultiHop-RAG is closer to the training distribution in difficulty.

**Benchmarks and why.** MultiHop-RAG (2024, news; ships a 609-document corpus) and FRAMES (2024,
Wikipedia, 824 questions). Both postdate our training sets, neither derives from HotpotQA,
2WikiMultihopQA, MuSiQue or StrategyQA, and both are used as standard tests of multi-hop retrieval
agents. `kit/leak_check.txt` runs E07's 8-gram contamination test: **0 of 600** MultiHop-RAG and
**0 of 598** FRAMES questions share a rare 8-gram with any training question.

**Conversion.** The harness retrieves with BM25 over each question's own candidate documents, which
neither benchmark ships, so `build_datasets.py` builds them: the evidence documents a question
cites, plus distractors from the same corpus (MultiHop-RAG) or from other questions' articles
(FRAMES), ten documents per question. FRAMES article text comes from the Wikipedia API. The
converted data is not tracked in this repository; the script reproduces it.

**Checks before the comparison.** `check_conversion.py` runs eight episodes per benchmark and
fails the pipeline unless every episode answers, the agent uses its tools, and gold documents are
actually retrievable. It caught two real defects: gold document ids were missing from the converted
questions, so doc recall was blind, and the Wikipedia fetch was silently caching HTTP 403s as empty
articles.

**Files.** `kit/summary_multihoprag.txt`/`.json`, `kit/summary_framesqa.txt`/`.json`,
`kit/leak_check.txt`.

**Caveats.** ~600 questions per benchmark (the interval is about ±1.6 points), so a real +1 to +2
effect would not be detectable here. Evaluation only: no arm was collected or trained on these
benchmarks, which is the point, but it also means the comparison inherits whatever the in-domain
training gave each arm. One judge.

## History

- **2026-09-21:** first run (pool).
