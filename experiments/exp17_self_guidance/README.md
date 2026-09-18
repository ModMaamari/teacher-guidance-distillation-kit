# exp17 — Is self-guidance better than no guidance?

**Why.** E01 found that, at matched size, teacher-guided rollouts train no better student than the
student's own unguided rollouts, keeping the correct ones. E06 found that episodes where the
student guided itself (it sees the gold answer as the privileged teacher) train the best student
of the three teachers. But E06 was at full size and E01 had no self-guided arm, so neither answers
whether self-guidance beats no guidance. That decides whether "self-guidance" names a method or
only a data source.

## Design

Two more trained arms, evaluated and judged exactly like E01:

| Arm | Trajectories | Size |
|---|---|---|
| `sup_selftaught` | the self-taught episodes (E15/E06), correct ones kept | cut to E01's matched usable count (1,412) |
| `selfdist_full` | the student's own unguided rollouts (E01), correct ones kept | all of them (3,753 usable) |

Comparisons:
- **Matched size:** `sup_selftaught` against E01's `selfdist`, `guided` and `teachdist`.
- **Full size:** `selfdist_full` against E06's self-taught (66.7 %) and DeepSeek-taught (62.1 %)
  students.

## Run

Pool tasks: `prep_e17`, `train_sup_selftaught`, `train_selfdist_full`, `eval_*`, `judge_*`,
`results_E17` (`experiments/pool/`).
