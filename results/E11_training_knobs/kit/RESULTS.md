# Results

## Per arm and test set

| arm | test set | n | done | EM | F1 | cover | judge | doc recall | steps | vol. finish | tokens/ep | latency s | API $ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| base | heldout_2wikimultihopqa | 170 | yes | 0.018 | 0.120 | 0.306 | 0.353 | 0.810 | 2.98 | 0.02 | 5,182 | 25.5 | 0.0000 |
| base | heldout_hotpotqa | 189 | yes | 0.169 | 0.240 | 0.381 | 0.429 | 0.759 | 2.91 | 0.09 | 5,120 | 20.1 | 0.0000 |
| base | heldout_musique | 203 | yes | 0.020 | 0.084 | 0.153 | 0.172 | 0.597 | 3.00 | 0.00 | 5,052 | 17.5 | 0.0000 |
| base | heldout_strategyqa | 185 | yes | 0.000 | 0.011 | 0.097 | 0.151 | 0.815 | 2.98 | 0.02 | 4,923 | 17.0 | 0.0000 |
| r16 | heldout_2wikimultihopqa | 170 | yes | 0.347 | 0.474 | 0.747 | 0.759 | 0.857 | 2.90 | 0.10 | 5,612 | 30.2 | 0.0000 |
| r16 | heldout_hotpotqa | 189 | yes | 0.318 | 0.405 | 0.561 | 0.635 | 0.770 | 2.87 | 0.13 | 5,368 | 15.1 | 0.0000 |
| r16 | heldout_musique | 203 | yes | 0.207 | 0.305 | 0.355 | 0.389 | 0.667 | 2.95 | 0.05 | 5,139 | 25.8 | 0.0000 |
| r16 | heldout_strategyqa | 185 | yes | 0.449 | 0.475 | 0.714 | 0.719 | 0.819 | 2.80 | 0.19 | 4,989 | 28.7 | 0.0000 |
| r32 | heldout_2wikimultihopqa | 170 | yes | 0.429 | 0.543 | 0.765 | 0.765 | 0.854 | 2.93 | 0.07 | 5,655 | 24.3 | 0.0000 |
| r32 | heldout_hotpotqa | 189 | yes | 0.339 | 0.425 | 0.587 | 0.635 | 0.786 | 2.83 | 0.17 | 5,249 | 22.6 | 0.0000 |
| r32 | heldout_musique | 203 | yes | 0.163 | 0.287 | 0.350 | 0.389 | 0.663 | 2.99 | 0.01 | 5,253 | 20.8 | 0.0000 |
| r32 | heldout_strategyqa | 185 | yes | 0.508 | 0.529 | 0.724 | 0.730 | 0.826 | 2.92 | 0.08 | 5,214 | 23.2 | 0.0000 |
| r64 | heldout_2wikimultihopqa | 170 | yes | 0.359 | 0.501 | 0.771 | 0.794 | 0.866 | 2.93 | 0.07 | 5,580 | 23.7 | 0.0000 |
| r64 | heldout_hotpotqa | 189 | yes | 0.344 | 0.442 | 0.598 | 0.651 | 0.788 | 2.83 | 0.17 | 5,236 | 23.2 | 0.0000 |
| r64 | heldout_musique | 203 | yes | 0.153 | 0.281 | 0.335 | 0.399 | 0.675 | 2.96 | 0.04 | 5,181 | 21.4 | 0.0000 |
| r64 | heldout_strategyqa | 185 | yes | 0.551 | 0.567 | 0.714 | 0.724 | 0.821 | 2.92 | 0.08 | 5,202 | 23.6 | 0.0000 |
| r8 | heldout_2wikimultihopqa | 170 | yes | 0.312 | 0.465 | 0.741 | 0.747 | 0.850 | 2.88 | 0.12 | 5,608 | 24.9 | 0.0000 |
| r8 | heldout_hotpotqa | 189 | yes | 0.339 | 0.426 | 0.587 | 0.656 | 0.780 | 2.86 | 0.14 | 5,289 | 22.6 | 0.0000 |
| r8 | heldout_musique | 203 | yes | 0.187 | 0.288 | 0.340 | 0.389 | 0.662 | 2.95 | 0.04 | 5,217 | 21.8 | 0.0000 |
| r8 | heldout_strategyqa | 185 | yes | 0.460 | 0.481 | 0.686 | 0.686 | 0.832 | 2.88 | 0.12 | 5,092 | 23.1 | 0.0000 |

## Pooled per arm

| arm | test sets | n | EM | F1 | cover | judge | steps | tokens/ep | API $ |
|---|---|---|---|---|---|---|---|---|---|
| base | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.052 | 0.113 | 0.232 | 0.273 | 2.97 | 5,067 | 0.0000 |
| r16 | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.327 | 0.411 | 0.585 | 0.617 | 2.88 | 5,267 | 0.0000 |
| r32 | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.353 | 0.440 | 0.597 | 0.621 | 2.92 | 5,334 | 0.0000 |
| r64 | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.347 | 0.442 | 0.594 | 0.633 | 2.91 | 5,291 | 0.0000 |
| r8 | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.321 | 0.411 | 0.580 | 0.612 | 2.89 | 5,293 | 0.0000 |

## Paired comparisons (judge-correct, b − a)

| a -> b | scope | Δ pts | 95% CI | b wins / a wins | McNemar p |
|---|---|---|---|---|---|
| base -> r16 | heldout_2wikimultihopqa | +40.6 | [+32.4, +48.8] | 75 / 6 | 0 |
| base -> r16 | heldout_hotpotqa | +20.6 | [+13.2, +28.0] | 48 / 9 | 0 |
| base -> r16 | heldout_musique | +21.7 | [+14.3, +28.6] | 55 / 11 | 0 |
| base -> r16 | heldout_strategyqa | +56.8 | [+49.2, +64.3] | 106 / 1 | 0 |
| base -> r16 | pooled | +34.4 | [+30.5, +38.3] | 284 / 27 | 0 |
| base -> r32 | heldout_2wikimultihopqa | +41.2 | [+32.9, +48.8] | 73 / 3 | 0 |
| base -> r32 | heldout_hotpotqa | +20.6 | [+13.2, +28.0] | 51 / 12 | 1e-06 |
| base -> r32 | heldout_musique | +21.7 | [+14.3, +29.1] | 57 / 13 | 0 |
| base -> r32 | heldout_strategyqa | +57.8 | [+50.3, +65.4] | 108 / 1 | 0 |
| base -> r32 | pooled | +34.8 | [+30.8, +38.7] | 289 / 29 | 0 |
| base -> r64 | heldout_2wikimultihopqa | +44.1 | [+36.5, +51.8] | 76 / 1 | 0 |
| base -> r64 | heldout_hotpotqa | +22.2 | [+14.8, +29.6] | 51 / 9 | 0 |
| base -> r64 | heldout_musique | +22.7 | [+15.3, +30.0] | 57 / 11 | 0 |
| base -> r64 | heldout_strategyqa | +57.3 | [+49.7, +64.9] | 108 / 2 | 0 |
| base -> r64 | pooled | +36.0 | [+32.1, +39.9] | 292 / 23 | 0 |
| base -> r8 | heldout_2wikimultihopqa | +39.4 | [+31.2, +47.6] | 71 / 4 | 0 |
| base -> r8 | heldout_hotpotqa | +22.8 | [+15.9, +29.6] | 49 / 6 | 0 |
| base -> r8 | heldout_musique | +21.7 | [+14.3, +29.1] | 56 / 12 | 0 |
| base -> r8 | heldout_strategyqa | +53.5 | [+46.0, +61.1] | 101 / 2 | 0 |
| base -> r8 | pooled | +33.9 | [+30.0, +37.8] | 277 / 24 | 0 |
| r16 -> r32 | heldout_2wikimultihopqa | +0.6 | [-4.1, +5.3] | 8 / 7 | 1 |
| r16 -> r32 | heldout_hotpotqa | +0.0 | [-5.3, +5.3] | 12 / 12 | 1 |
| r16 -> r32 | heldout_musique | +0.0 | [-6.4, +6.4] | 23 / 23 | 1 |
| r16 -> r32 | heldout_strategyqa | +1.1 | [-3.2, +5.4] | 10 / 8 | 0.815 |
| r16 -> r32 | pooled | +0.4 | [-2.3, +3.1] | 53 / 50 | 0.844 |
| r16 -> r64 | heldout_2wikimultihopqa | +3.5 | [-2.4, +9.4] | 16 / 10 | 0.327 |
| r16 -> r64 | heldout_hotpotqa | +1.6 | [-3.7, +6.9] | 15 / 12 | 0.701 |
| r16 -> r64 | heldout_musique | +1.0 | [-5.4, +7.4] | 22 / 20 | 0.878 |
| r16 -> r64 | heldout_strategyqa | +0.5 | [-4.9, +5.9] | 14 / 13 | 1 |
| r16 -> r64 | pooled | +1.6 | [-1.2, +4.5] | 67 / 55 | 0.319 |
| r16 -> r8 | heldout_2wikimultihopqa | -1.2 | [-6.5, +4.1] | 10 / 12 | 0.832 |
| r16 -> r8 | heldout_hotpotqa | +2.1 | [-3.2, +7.4] | 16 / 12 | 0.572 |
| r16 -> r8 | heldout_musique | +0.0 | [-5.9, +5.9] | 18 / 18 | 1 |
| r16 -> r8 | heldout_strategyqa | -3.2 | [-8.6, +2.2] | 10 / 16 | 0.327 |
| r16 -> r8 | pooled | -0.5 | [-3.4, +2.3] | 54 / 58 | 0.777 |
| r32 -> r64 | heldout_2wikimultihopqa | +2.9 | [-2.4, +8.8] | 15 / 10 | 0.424 |
| r32 -> r64 | heldout_hotpotqa | +1.6 | [-3.7, +6.9] | 15 / 12 | 0.701 |
| r32 -> r64 | heldout_musique | +1.0 | [-5.4, +7.4] | 24 / 22 | 0.883 |
| r32 -> r64 | heldout_strategyqa | -0.5 | [-5.4, +4.3] | 10 / 11 | 1 |
| r32 -> r64 | pooled | +1.2 | [-1.7, +4.0] | 64 / 55 | 0.463 |
| r32 -> r8 | heldout_2wikimultihopqa | -1.8 | [-6.5, +2.9] | 8 / 11 | 0.648 |
| r32 -> r8 | heldout_hotpotqa | +2.1 | [-3.2, +7.4] | 16 / 12 | 0.572 |
| r32 -> r8 | heldout_musique | +0.0 | [-6.4, +6.4] | 22 / 22 | 1 |
| r32 -> r8 | heldout_strategyqa | -4.3 | [-9.2, +0.5] | 7 / 15 | 0.134 |
| r32 -> r8 | pooled | -0.9 | [-3.8, +1.9] | 53 / 60 | 0.573 |
| r64 -> r8 | heldout_2wikimultihopqa | -4.7 | [-10.6, +1.2] | 9 / 17 | 0.169 |
| r64 -> r8 | heldout_hotpotqa | +0.5 | [-4.8, +5.8] | 14 / 13 | 1 |
| r64 -> r8 | heldout_musique | -1.0 | [-6.9, +5.4] | 20 / 22 | 0.878 |
| r64 -> r8 | heldout_strategyqa | -3.8 | [-9.2, +1.6] | 9 / 16 | 0.23 |
| r64 -> r8 | pooled | -2.1 | [-5.0, +0.7] | 52 / 68 | 0.171 |
