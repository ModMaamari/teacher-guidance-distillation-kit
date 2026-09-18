# exp19 — Robustness of the self-guided student

**Why.** The seed, transfer and forgetting checks (E02, E13, E09) were measured on students trained
on DeepSeek-guided trajectories. If self-guidance is the method the paper proposes, the same checks
belong on the self-guided student.

## Design

- **Seeds:** the self-guided student (E06 `selftaught`, seed 13) retrained with seeds 17 and 23.
- **Transfer:** four leave-one-dataset-out students on the self-guided episodes
  (`data/splits_self/lodo/fold_*`), each evaluated on every question of its unseen dataset,
  against the base student on the same questions (`basefull`).
- **Forgetting:** MMLU, GSM8K and HellaSwag, self-guided student vs base.

## Run

Pool tasks: `train_selftaught_s{17,23}`, `train_selflodo_*`, `eval_selflodo_*`, `eval_basefull_*`,
`forget_selftaught`, `judge_*`, `results_E19`.
