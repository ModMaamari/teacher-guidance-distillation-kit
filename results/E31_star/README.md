# E31 — STaR: the student's correct attempts plus answer-hinted rationalizations

**Question.** STaR (Zelikman et al., 2022) is the standard way to self-train on gold answers
without a critic: keep the model's correct attempts, and for the questions it got wrong, show it
the answer as a hint, keep the hinted attempts that end correct, and train on them with the hint
removed. It uses exactly the privileged information Self-Guidance uses. Does it match
Self-Guidance?

**Answer.** It comes close only at nearly twice the compute, and no difference is significant.
Judge-correct accuracy (Gemma-4-31B-it) on the 747 held-out questions:

| Training data | Questions | Examples | Build PFLOPs | Seeds | Per seed | Mean |
|---|---|---|---|---|---|---|
| **Self-guided (E25)** | 3,818 | 13,825 | 1,474 | 6 | 66.7 / 64.9 / 63.2 / 63.6 / 64.9 / 65.2 | **64.8 ± 1.2** |
| STaR, 2 iterations | 7,000 | 23,954 | 2,725 | 6 | 63.3 / 63.9 / 64.0 / 65.3 / 65.5 / 61.9 | 64.0 ± 1.3 |
| STaR, 1 iteration | 6,971 | 23,374 | 1,367 | 3 | 62.8 / 62.6 / 63.7 | 63.0 ± 0.6 |
| Unguided self-rollouts (E25) | 3,753 | 13,510 | 859 | 6 | 62.3 / 64.8 / 62.6 / 62.0 / 60.6 / 62.4 | 62.5 ± 1.4 |

Seed-averaged paired test (each question averaged over a family's seeds), bootstrap 95 % CI,
sign-flip p; Holm over the two planned primary contrasts:

| Contrast | Δ | 95 % CI | p | Holm |
|---|---|---|---|---|
| STaR-2 → self-guided (primary) | +0.8 | −1.1 to +2.6 | 0.42 | 0.42 |
| unguided → STaR-2 (primary) | +1.5 | −0.1 to +3.2 | 0.080 | 0.16 |
| STaR-1 → self-guided | +1.7 | −0.2 to +3.6 | 0.092 | — |
| unguided → STaR-1 | +0.6 | −1.0 to +2.2 | 0.49 | — |
| STaR-1 → STaR-2 | +0.9 | −0.6 to +2.5 | 0.26 | — |

Over seeds (Welch on the per-seed accuracies): self-guided vs STaR-2 p 0.33; STaR-2 vs unguided
p 0.076; self-guided vs STaR-1 p 0.027 (6 vs 3 seeds, from answer counts). Seed pairs STaR-2 → self-guided: +3.4,
+1.1, −0.8, −1.7, −0.5, +3.4.

**Reading, against the outcomes stated before the runs.** The pre-stated middle case applies:
*STaR ≈ self-guided*. Neither primary contrast is significant; self-guided is ahead in point
estimate at both STaR iterations. At the same build compute (STaR-1, 1,367 against 1,474 PFLOPs),
STaR trails by 1.7 (p 0.092 over questions, 0.027 over seeds); spending 1.85 times the compute on a
second iteration narrows the gap to 0.8. STaR is itself not significantly better than the
student's own filtered rollouts (+1.5, p 0.080). The paper can say that Self-Guidance is at least
as good as STaR at lower compute, not that it beats it.

**Coverage again is not what decides it.** Rationalization turns almost every failure into a
training episode: 3,422 of 3,499 hinted retries end correct in iteration 1 (97.8 %), and STaR
trains on 6,971 questions against Self-Guidance's 3,818, with 1.7 times the examples. As in E30,
more solved questions do not buy accuracy.

**Protocol.** Attempts are unguided episodes (iteration 1 reuses E25's `data/episodes_selfdist`;
iteration 2 collects them with the merged seed-13 STaR-1 model on the 7,252 trainable questions).
Each trainable question the attempt failed gets one more episode whose step prompts carry
`Answer hint (the known correct answer): "<gold>"` (`collect_episodes.py --answer-hint`; the plan
prompt is not hinted). Training strips the hint, and keeps a hinted step only if nothing it wrote
-- thought, query, facts, final answer -- names the answer before a retrieved document does; the
student's own earlier outputs do not count (`tgd.episode_lib`, unit-tested). 6,588 of the STaR-1
examples come from hinted steps (3,279 questions); 4,671 of STaR-2's (2,501 questions). Same LoRA
recipe; each STaR iteration retrains from the base model, as in STaR. Collection compute measured
call by call: attempts 258 and 230 PFLOPs, rationalizations 115 and 88; training 994 and 1,040
(the STaR-2 build includes training the STaR-1 model that collected its data).

**Files.** `kit/summary.txt`/`.json`, `kit/results.json`/`RESULTS.md`, `kit/train_cost.txt`/`.json`,
`kit/episodes_star{1,2}_merge_stats.json` (attempts kept, replaced, rationalizations correct).

**Caveats.** In domain only (the external benchmarks were not run for these students). STaR-1 has
three seeds. The grounding gate is stricter than STaR's (which keeps any rationale that reaches the
answer), so it removes some rationalized steps a plain STaR would train on; it also removes the
steps where the hint leaks, which is what makes the comparison fair.
