# Forgetting check — 1 run(s), metric: strict

Arms: `base` vs `selftaught`. Same items, one server, adapter is the only difference.

| Scope | Arm | Mean | SD | Variance | 95% CI of the mean | Per-run |
|---|---|---|---|---|---|---|
| MMLU | base | 63.51% | 0.00 | 0.000e-4 | [63.51, 63.51] | 63.51 |
|  | selftaught | 63.04% | 0.00 | 0.000e-4 | [63.04, 63.04] | 63.04 |
| GSM8K | base | 89.16% | 0.00 | 0.000e-4 | [89.16, 89.16] | 89.16 |
|  | selftaught | 86.35% | 0.00 | 0.000e-4 | [86.35, 86.35] | 86.35 |
| HellaSwag | base | 75.27% | 0.00 | 0.000e-4 | [75.27, 75.27] | 75.27 |
|  | selftaught | 74.80% | 0.00 | 0.000e-4 | [74.80, 74.80] | 74.80 |
| Pooled | base | 74.87% | 0.00 | 0.000e-4 | [74.87, 74.87] | 74.87 |
|  | selftaught | 73.72% | 0.00 | 0.000e-4 | [73.72, 73.72] | 73.72 |

## Significance

| Scope | Δ mean (pts) | paired t | df | t p | Wilcoxon p | item-level McNemar p | decisions |
|---|---|---|---|---|---|---|---|
| MMLU | -0.47 | nan | — | — | — | 0.4452 | 1,710 |
| GSM8K | -2.81 | nan | — | — | — | 0.000341 | 1,319 |
| HellaSwag | -0.47 | nan | — | — | — | 0.5341 | 1,500 |
| Pooled | -1.15 | nan | — | — | — | 0.002247 | 4,529 |
