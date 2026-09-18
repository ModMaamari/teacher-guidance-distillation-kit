# Forgetting check — 1 run(s), metric: strict

Arms: `base` vs `seed13`. Same items, one server, adapter is the only difference.

| Scope | Arm | Mean | SD | Variance | 95% CI of the mean | Per-run |
|---|---|---|---|---|---|---|
| MMLU | base | 63.51% | 0.00 | 0.000e-4 | [63.51, 63.51] | 63.51 |
|  | seed13 | 63.27% | 0.00 | 0.000e-4 | [63.27, 63.27] | 63.27 |
| GSM8K | base | 89.16% | 0.00 | 0.000e-4 | [89.16, 89.16] | 89.16 |
|  | seed13 | 88.40% | 0.00 | 0.000e-4 | [88.40, 88.40] | 88.40 |
| HellaSwag | base | 75.27% | 0.00 | 0.000e-4 | [75.27, 75.27] | 75.27 |
|  | seed13 | 73.67% | 0.00 | 0.000e-4 | [73.67, 73.67] | 73.67 |
| Pooled | base | 74.87% | 0.00 | 0.000e-4 | [74.87, 74.87] | 74.87 |
|  | seed13 | 74.03% | 0.00 | 0.000e-4 | [74.03, 74.03] | 74.03 |

## Significance

| Scope | Δ mean (pts) | paired t | df | t p | Wilcoxon p | item-level McNemar p | decisions |
|---|---|---|---|---|---|---|---|
| MMLU | -0.23 | nan | — | — | — | 0.7596 | 1,710 |
| GSM8K | -0.76 | nan | — | — | — | 0.3866 | 1,319 |
| HellaSwag | -1.60 | nan | — | — | — | 0.0293 | 1,500 |
| Pooled | -0.84 | nan | — | — | — | 0.03723 | 4,529 |
