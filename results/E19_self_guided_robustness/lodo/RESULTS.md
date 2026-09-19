# Results

## Per arm and test set

| arm | test set | n | done | EM | F1 | cover | judge | doc recall | steps | vol. finish | tokens/ep | latency s | API $ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| basefull | full_2wikimultihopqa | 2000 | yes | 0.017 | 0.120 | 0.327 | 0.387 | 0.823 | 2.98 | 0.02 | 5,194 | 40.8 | 0.0000 |
| basefull | full_hotpotqa | 2000 | yes | 0.198 | 0.290 | 0.429 | 0.469 | 0.791 | 2.91 | 0.09 | 5,112 | 32.2 | 0.0000 |
| basefull | full_musique | 2000 | yes | 0.026 | 0.068 | 0.103 | 0.122 | 0.580 | 2.99 | 0.01 | 4,880 | 29.2 | 0.0000 |
| basefull | full_strategyqa | 1999 | yes | 0.000 | 0.012 | 0.102 | 0.169 | 0.814 | 2.98 | 0.02 | 4,848 | 23.7 | 0.0000 |
| fold_2wikimultihopqa | full_2wikimultihopqa | 2000 | yes | 0.054 | 0.213 | 0.721 | 0.733 | 0.837 | 2.91 | 0.09 | 5,258 | 23.5 | 0.0000 |
| fold_hotpotqa | full_hotpotqa | 2000 | yes | 0.265 | 0.399 | 0.679 | 0.725 | 0.796 | 2.77 | 0.23 | 4,985 | 22.7 | 0.0000 |
| fold_musique | full_musique | 2000 | yes | 0.054 | 0.162 | 0.333 | 0.406 | 0.630 | 2.94 | 0.06 | 5,236 | 43.0 | 0.0000 |
| fold_strategyqa | full_strategyqa | 1999 | yes | 0.000 | 0.034 | 0.591 | 0.648 | 0.805 | 2.89 | 0.10 | 5,066 | 31.8 | 0.0000 |

## Pooled per arm

| arm | test sets | n | EM | F1 | cover | judge | steps | tokens/ep | API $ |
|---|---|---|---|---|---|---|---|---|---|
| basefull | full_2wikimultihopqa, full_hotpotqa, full_musique, full_strategyqa | 7999 | 0.060 | 0.123 | 0.240 | 0.286 | 2.97 | 5,008 | 0.0000 |
| fold_2wikimultihopqa | full_2wikimultihopqa | 2000 | 0.054 | 0.213 | 0.721 | 0.733 | 2.91 | 5,258 | 0.0000 |
| fold_hotpotqa | full_hotpotqa | 2000 | 0.265 | 0.399 | 0.679 | 0.725 | 2.77 | 4,985 | 0.0000 |
| fold_musique | full_musique | 2000 | 0.054 | 0.162 | 0.333 | 0.406 | 2.94 | 5,236 | 0.0000 |
| fold_strategyqa | full_strategyqa | 1999 | 0.000 | 0.034 | 0.591 | 0.648 | 2.89 | 5,066 | 0.0000 |

## Paired comparisons (judge-correct, b − a)

| a -> b | scope | Δ pts | 95% CI | b wins / a wins | McNemar p |
|---|---|---|---|---|---|
| basefull -> fold_2wikimultihopqa | full_2wikimultihopqa | +34.6 | [+32.3, +37.0] | 751 / 58 | 0 |
| basefull -> fold_hotpotqa | full_hotpotqa | +25.7 | [+23.4, +27.8] | 570 / 57 | 0 |
| basefull -> fold_musique | full_musique | +28.4 | [+26.2, +30.6] | 612 / 44 | 0 |
| basefull -> fold_strategyqa | full_strategyqa | +47.9 | [+45.6, +50.3] | 996 / 38 | 0 |
