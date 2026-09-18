# Results

## Per arm and test set

| arm | test set | n | done | EM | F1 | cover | judge | doc recall | steps | vol. finish | tokens/ep | latency s | API $ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all4 | heldout_2wikimultihopqa | 170 | yes | 0.359 | 0.506 | 0.806 | 0.824 | 0.885 | 2.90 | 0.10 | 5,644 | 18.8 | 0.0000 |
| all4 | heldout_hotpotqa | 189 | yes | 0.354 | 0.431 | 0.582 | 0.640 | 0.794 | 2.79 | 0.21 | 5,247 | 17.5 | 0.0000 |
| all4 | heldout_musique | 203 | yes | 0.168 | 0.272 | 0.364 | 0.374 | 0.661 | 2.96 | 0.04 | 5,269 | 16.7 | 0.0000 |
| all4 | heldout_strategyqa | 185 | yes | 0.508 | 0.530 | 0.724 | 0.735 | 0.829 | 2.90 | 0.10 | 5,241 | 18.5 | 0.0000 |
| base | full_2wikimultihopqa | 2000 | yes | 0.019 | 0.128 | 0.335 | 0.389 | 0.821 | 2.98 | 0.02 | 5,191 | 11.9 | 0.0000 |
| base | full_hotpotqa | 2000 | yes | 0.192 | 0.286 | 0.427 | 0.471 | 0.789 | 2.92 | 0.08 | 5,099 | 11.0 | 0.0000 |
| base | full_musique | 2000 | yes | 0.025 | 0.061 | 0.093 | 0.117 | 0.581 | 2.99 | 0.01 | 4,884 | 7.6 | 0.0000 |
| base | full_strategyqa | 1999 | yes | 0.000 | 0.012 | 0.096 | 0.159 | 0.814 | 2.98 | 0.02 | 4,837 | 7.0 | 0.0000 |
| base | heldout_2wikimultihopqa | 170 | yes | 0.006 | 0.112 | 0.288 | 0.377 | 0.818 | 2.98 | 0.02 | 5,232 | 16.9 | 0.0000 |
| base | heldout_hotpotqa | 189 | yes | 0.196 | 0.253 | 0.376 | 0.429 | 0.759 | 2.94 | 0.06 | 5,155 | 13.8 | 0.0000 |
| base | heldout_musique | 203 | yes | 0.030 | 0.090 | 0.138 | 0.148 | 0.608 | 3.00 | 0.00 | 4,988 | 8.3 | 0.0000 |
| base | heldout_strategyqa | 185 | yes | 0.000 | 0.010 | 0.092 | 0.157 | 0.814 | 2.99 | 0.01 | 4,815 | 7.5 | 0.0000 |
| fold_2wikimultihopqa | full_2wikimultihopqa | 2000 | yes | 0.270 | 0.416 | 0.698 | 0.713 | 0.833 | 2.93 | 0.07 | 5,550 | 14.7 | 0.0000 |
| fold_2wikimultihopqa | heldout_hotpotqa | 189 | yes | 0.365 | 0.457 | 0.598 | 0.645 | 0.780 | 2.85 | 0.15 | 5,345 | 15.3 | 0.0000 |
| fold_2wikimultihopqa | heldout_musique | 203 | yes | 0.143 | 0.254 | 0.305 | 0.345 | 0.667 | 2.96 | 0.04 | 5,209 | 13.1 | 0.0000 |
| fold_2wikimultihopqa | heldout_strategyqa | 185 | yes | 0.503 | 0.520 | 0.697 | 0.703 | 0.827 | 2.88 | 0.11 | 5,191 | 14.4 | 0.0000 |
| fold_hotpotqa | full_hotpotqa | 2000 | yes | 0.373 | 0.497 | 0.636 | 0.690 | 0.812 | 2.86 | 0.14 | 5,312 | 14.1 | 0.0000 |
| fold_hotpotqa | heldout_2wikimultihopqa | 170 | yes | 0.312 | 0.462 | 0.771 | 0.776 | 0.888 | 2.90 | 0.10 | 5,544 | 13.8 | 0.0000 |
| fold_hotpotqa | heldout_musique | 203 | yes | 0.163 | 0.285 | 0.345 | 0.389 | 0.672 | 2.97 | 0.02 | 5,212 | 12.0 | 0.0000 |
| fold_hotpotqa | heldout_strategyqa | 185 | yes | 0.530 | 0.547 | 0.719 | 0.714 | 0.829 | 2.93 | 0.07 | 5,302 | 14.3 | 0.0000 |
| fold_musique | full_musique | 2000 | yes | 0.133 | 0.221 | 0.269 | 0.328 | 0.665 | 2.96 | 0.04 | 5,263 | 13.2 | 0.0000 |
| fold_musique | heldout_2wikimultihopqa | 170 | yes | 0.265 | 0.437 | 0.794 | 0.794 | 0.888 | 2.91 | 0.09 | 5,564 | 14.9 | 0.0000 |
| fold_musique | heldout_hotpotqa | 189 | yes | 0.312 | 0.405 | 0.577 | 0.640 | 0.794 | 2.82 | 0.18 | 5,298 | 14.5 | 0.0000 |
| fold_musique | heldout_strategyqa | 185 | yes | 0.460 | 0.485 | 0.724 | 0.724 | 0.818 | 2.90 | 0.09 | 5,202 | 15.0 | 0.0000 |
| fold_strategyqa | full_strategyqa | 1999 | yes | 0.336 | 0.364 | 0.608 | 0.653 | 0.801 | 2.89 | 0.11 | 5,093 | 13.2 | 0.0000 |
| fold_strategyqa | heldout_2wikimultihopqa | 170 | yes | 0.365 | 0.496 | 0.759 | 0.759 | 0.869 | 2.91 | 0.09 | 5,587 | 15.2 | 0.0000 |
| fold_strategyqa | heldout_hotpotqa | 189 | yes | 0.339 | 0.426 | 0.582 | 0.609 | 0.767 | 2.81 | 0.19 | 5,198 | 14.5 | 0.0000 |
| fold_strategyqa | heldout_musique | 203 | yes | 0.168 | 0.260 | 0.286 | 0.305 | 0.647 | 2.95 | 0.05 | 5,195 | 13.1 | 0.0000 |
| teacher | full_2wikimultihopqa | 252 | yes | 0.198 | 0.345 | 0.798 | 0.825 | — | 2.70 | 0.30 | 3,850 | 0.0 | 0.0384 |
| teacher | full_hotpotqa | 254 | yes | 0.516 | 0.630 | 0.791 | 0.819 | — | 2.61 | 0.39 | 3,614 | 0.0 | 0.0358 |
| teacher | full_musique | 229 | yes | 0.288 | 0.377 | 0.454 | 0.493 | — | 2.93 | 0.07 | 4,230 | 0.0 | 0.0368 |
| teacher | full_strategyqa | 273 | yes | 0.015 | 0.054 | 0.535 | 0.623 | — | 2.76 | 0.24 | 3,720 | 0.0 | 0.0409 |
| teacher | heldout_2wikimultihopqa | 170 | yes | 0.224 | 0.362 | 0.841 | 0.841 | — | 2.69 | 0.31 | 3,902 | 0.0 | 0.0264 |
| teacher | heldout_hotpotqa | 189 | yes | 0.455 | 0.549 | 0.735 | 0.783 | — | 2.67 | 0.32 | 3,746 | 0.0 | 0.0275 |
| teacher | heldout_musique | 203 | yes | 0.296 | 0.392 | 0.483 | 0.537 | — | 2.90 | 0.10 | 4,164 | 0.0 | 0.0321 |
| teacher | heldout_strategyqa | 185 | yes | 0.011 | 0.048 | 0.600 | 0.708 | — | 2.75 | 0.25 | 3,723 | 0.0 | 0.0279 |

## Pooled per arm

| arm | test sets | n | EM | F1 | cover | judge | steps | tokens/ep | API $ |
|---|---|---|---|---|---|---|---|---|---|
| all4 | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.343 | 0.430 | 0.609 | 0.633 | 2.89 | 5,342 | 0.0000 |
| base | full_2wikimultihopqa, full_hotpotqa, full_musique, full_strategyqa, heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 8746 | 0.059 | 0.121 | 0.236 | 0.283 | 2.97 | 5,006 | 0.0000 |
| fold_2wikimultihopqa | full_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 2577 | 0.283 | 0.414 | 0.659 | 0.678 | 2.92 | 5,482 | 0.0000 |
| fold_hotpotqa | full_hotpotqa, heldout_2wikimultihopqa, heldout_musique, heldout_strategyqa | 2558 | 0.364 | 0.482 | 0.628 | 0.674 | 2.88 | 5,319 | 0.0000 |
| fold_musique | full_musique, heldout_2wikimultihopqa, heldout_hotpotqa, heldout_strategyqa | 2544 | 0.179 | 0.268 | 0.360 | 0.411 | 2.94 | 5,282 | 0.0000 |
| fold_strategyqa | full_strategyqa, heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique | 2561 | 0.325 | 0.369 | 0.591 | 0.629 | 2.89 | 5,142 | 0.0000 |
| teacher | full_2wikimultihopqa, full_hotpotqa, full_musique, full_strategyqa, heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 1755 | 0.249 | 0.343 | 0.651 | 0.701 | 2.75 | 3,862 | 0.2658 |

## Paired comparisons (judge-correct, b − a)

| a -> b | scope | Δ pts | 95% CI | b wins / a wins | McNemar p |
|---|---|---|---|---|---|
| all4 -> base | heldout_2wikimultihopqa | -44.7 | [-52.3, -37.1] | 2 / 78 | 0 |
| all4 -> base | heldout_hotpotqa | -21.2 | [-28.6, -13.8] | 11 / 51 | 0 |
| all4 -> base | heldout_musique | -22.7 | [-29.6, -15.8] | 7 / 53 | 0 |
| all4 -> base | heldout_strategyqa | -57.8 | [-65.4, -50.8] | 1 / 108 | 0 |
| all4 -> base | pooled | -36.0 | [-39.8, -32.1] | 21 / 290 | 0 |
| all4 -> fold_2wikimultihopqa | heldout_hotpotqa | +0.5 | [-4.8, +5.8] | 15 / 14 | 1 |
| all4 -> fold_2wikimultihopqa | heldout_musique | -3.0 | [-8.9, +3.0] | 17 / 23 | 0.43 |
| all4 -> fold_2wikimultihopqa | heldout_strategyqa | -3.2 | [-8.1, +1.1] | 7 / 13 | 0.263 |
| all4 -> fold_2wikimultihopqa | pooled | -1.9 | [-5.0, +1.2] | 39 / 50 | 0.289 |
| all4 -> fold_hotpotqa | heldout_2wikimultihopqa | -4.7 | [-10.0, +0.6] | 8 / 16 | 0.152 |
| all4 -> fold_hotpotqa | heldout_musique | +1.5 | [-4.9, +7.9] | 24 / 21 | 0.766 |
| all4 -> fold_hotpotqa | heldout_strategyqa | -2.2 | [-7.6, +3.2] | 10 / 14 | 0.541 |
| all4 -> fold_hotpotqa | pooled | -1.6 | [-5.0, +1.8] | 42 / 51 | 0.407 |
| all4 -> fold_musique | heldout_2wikimultihopqa | -2.9 | [-8.2, +1.8] | 7 / 12 | 0.359 |
| all4 -> fold_musique | heldout_hotpotqa | +0.0 | [-5.3, +5.3] | 14 / 14 | 1 |
| all4 -> fold_musique | heldout_strategyqa | -1.1 | [-6.5, +4.3] | 12 / 14 | 0.845 |
| all4 -> fold_musique | pooled | -1.3 | [-4.4, +1.7] | 33 / 40 | 0.483 |
| all4 -> fold_strategyqa | heldout_2wikimultihopqa | -6.5 | [-12.3, -0.6] | 7 / 18 | 0.0433 |
| all4 -> fold_strategyqa | heldout_hotpotqa | -3.2 | [-9.5, +3.2] | 16 / 22 | 0.418 |
| all4 -> fold_strategyqa | heldout_musique | -6.9 | [-12.8, -1.0] | 13 / 27 | 0.0385 |
| all4 -> fold_strategyqa | pooled | -5.5 | [-8.9, -2.0] | 36 / 67 | 0.00293 |
| all4 -> teacher | heldout_2wikimultihopqa | +1.8 | [-4.7, +8.2] | 17 / 14 | 0.72 |
| all4 -> teacher | heldout_hotpotqa | +14.3 | [+7.9, +20.6] | 35 / 8 | 4.2e-05 |
| all4 -> teacher | heldout_musique | +16.3 | [+9.4, +23.2] | 46 / 13 | 1.9e-05 |
| all4 -> teacher | heldout_strategyqa | -2.7 | [-10.3, +4.3] | 22 / 27 | 0.568 |
| all4 -> teacher | pooled | +7.8 | [+4.3, +11.2] | 120 / 62 | 2.1e-05 |
| base -> fold_2wikimultihopqa | full_2wikimultihopqa | +32.4 | [+30.1, +34.8] | 704 / 56 | 0 |
| base -> fold_2wikimultihopqa | heldout_hotpotqa | +21.7 | [+15.3, +28.6] | 45 / 4 | 0 |
| base -> fold_2wikimultihopqa | heldout_musique | +19.7 | [+12.8, +26.6] | 48 / 8 | 0 |
| base -> fold_2wikimultihopqa | heldout_strategyqa | +54.6 | [+47.0, +62.2] | 104 / 3 | 0 |
| base -> fold_2wikimultihopqa | pooled | +32.2 | [+30.2, +34.2] | 901 / 71 | 0 |
| base -> fold_hotpotqa | full_hotpotqa | +21.9 | [+19.7, +24.1] | 525 / 87 | 0 |
| base -> fold_hotpotqa | heldout_2wikimultihopqa | +40.0 | [+31.8, +48.2] | 73 / 5 | 0 |
| base -> fold_hotpotqa | heldout_musique | +24.1 | [+17.2, +31.0] | 57 / 8 | 0 |
| base -> fold_hotpotqa | heldout_strategyqa | +55.7 | [+48.1, +63.2] | 106 / 3 | 0 |
| base -> fold_hotpotqa | pooled | +25.7 | [+23.7, +27.8] | 761 / 103 | 0 |
| base -> fold_musique | full_musique | +21.1 | [+19.1, +23.2] | 490 / 67 | 0 |
| base -> fold_musique | heldout_2wikimultihopqa | +41.8 | [+33.5, +50.0] | 75 / 4 | 0 |
| base -> fold_musique | heldout_hotpotqa | +21.2 | [+14.3, +28.0] | 47 / 7 | 0 |
| base -> fold_musique | heldout_strategyqa | +56.8 | [+49.2, +64.3] | 108 / 3 | 0 |
| base -> fold_musique | pooled | +25.1 | [+23.2, +27.0] | 720 / 81 | 0 |
| base -> fold_strategyqa | full_strategyqa | +49.4 | [+47.0, +51.8] | 1031 / 43 | 0 |
| base -> fold_strategyqa | heldout_2wikimultihopqa | +38.2 | [+30.6, +46.5] | 69 / 4 | 0 |
| base -> fold_strategyqa | heldout_hotpotqa | +18.0 | [+10.6, +25.4] | 43 / 9 | 2e-06 |
| base -> fold_strategyqa | heldout_musique | +15.8 | [+9.8, +22.2] | 40 / 8 | 3e-06 |
| base -> fold_strategyqa | pooled | +43.7 | [+41.6, +45.8] | 1183 / 64 | 0 |
| base -> teacher | full_2wikimultihopqa | +43.6 | [+37.3, +50.0] | 113 / 3 | 0 |
| base -> teacher | full_hotpotqa | +36.6 | [+30.7, +42.5] | 95 / 2 | 0 |
| base -> teacher | full_musique | +41.0 | [+34.5, +48.0] | 98 / 4 | 0 |
| base -> teacher | full_strategyqa | +46.2 | [+39.9, +52.4] | 129 / 3 | 0 |
| base -> teacher | heldout_2wikimultihopqa | +46.5 | [+38.2, +54.1] | 82 / 3 | 0 |
| base -> teacher | heldout_hotpotqa | +35.4 | [+28.6, +42.3] | 68 / 1 | 0 |
| base -> teacher | heldout_musique | +38.9 | [+32.0, +45.8] | 82 / 3 | 0 |
| base -> teacher | heldout_strategyqa | +55.1 | [+48.1, +62.2] | 103 / 1 | 0 |
| base -> teacher | pooled | +43.1 | [+40.7, +45.6] | 729 / 17 | 0 |
| fold_2wikimultihopqa -> fold_hotpotqa | heldout_musique | +4.4 | [-2.0, +10.8] | 27 / 18 | 0.233 |
| fold_2wikimultihopqa -> fold_hotpotqa | heldout_strategyqa | +1.1 | [-3.8, +5.9] | 12 / 10 | 0.832 |
| fold_2wikimultihopqa -> fold_hotpotqa | pooled | +2.8 | [-1.3, +7.0] | 39 / 28 | 0.222 |
| fold_2wikimultihopqa -> fold_musique | heldout_hotpotqa | -0.5 | [-6.3, +5.3] | 14 / 15 | 1 |
| fold_2wikimultihopqa -> fold_musique | heldout_strategyqa | +2.2 | [-3.2, +8.1] | 17 / 13 | 0.585 |
| fold_2wikimultihopqa -> fold_musique | pooled | +0.8 | [-3.2, +4.8] | 31 / 28 | 0.795 |
| fold_2wikimultihopqa -> fold_strategyqa | heldout_hotpotqa | -3.7 | [-9.5, +2.1] | 12 / 19 | 0.281 |
| fold_2wikimultihopqa -> fold_strategyqa | heldout_musique | -3.9 | [-9.8, +2.0] | 15 / 23 | 0.256 |
| fold_2wikimultihopqa -> fold_strategyqa | pooled | -3.8 | [-7.9, +0.3] | 27 / 42 | 0.0912 |
| fold_2wikimultihopqa -> teacher | full_2wikimultihopqa | +14.3 | [+8.7, +19.8] | 47 / 11 | 2e-06 |
| fold_2wikimultihopqa -> teacher | heldout_hotpotqa | +13.8 | [+7.9, +19.6] | 31 / 5 | 1.3e-05 |
| fold_2wikimultihopqa -> teacher | heldout_musique | +19.2 | [+11.8, +26.6] | 51 / 12 | 1e-06 |
| fold_2wikimultihopqa -> teacher | heldout_strategyqa | +0.5 | [-6.5, +7.6] | 24 / 23 | 1 |
| fold_2wikimultihopqa -> teacher | pooled | +12.3 | [+8.9, +15.6] | 153 / 51 | 0 |
| fold_hotpotqa -> fold_musique | heldout_2wikimultihopqa | +1.8 | [-4.1, +7.6] | 14 / 11 | 0.69 |
| fold_hotpotqa -> fold_musique | heldout_strategyqa | +1.1 | [-4.9, +7.0] | 17 / 15 | 0.86 |
| fold_hotpotqa -> fold_musique | pooled | +1.4 | [-2.8, +5.6] | 31 / 26 | 0.597 |
| fold_hotpotqa -> fold_strategyqa | heldout_2wikimultihopqa | -1.8 | [-8.2, +4.1] | 13 / 16 | 0.711 |
| fold_hotpotqa -> fold_strategyqa | heldout_musique | -8.4 | [-14.8, -2.5] | 13 / 30 | 0.0137 |
| fold_hotpotqa -> fold_strategyqa | pooled | -5.4 | [-9.9, -1.1] | 26 / 46 | 0.0245 |
| fold_hotpotqa -> teacher | full_hotpotqa | +13.8 | [+7.9, +19.7] | 50 / 15 | 1.6e-05 |
| fold_hotpotqa -> teacher | heldout_2wikimultihopqa | +6.5 | [-1.2, +13.5] | 26 / 15 | 0.117 |
| fold_hotpotqa -> teacher | heldout_musique | +14.8 | [+6.9, +22.7] | 50 / 20 | 0.00044 |
| fold_hotpotqa -> teacher | heldout_strategyqa | -0.5 | [-7.6, +6.5] | 22 / 23 | 1 |
| fold_hotpotqa -> teacher | pooled | +9.2 | [+5.8, +12.8] | 148 / 73 | 1e-06 |
| fold_musique -> fold_strategyqa | heldout_2wikimultihopqa | -3.5 | [-9.4, +2.4] | 11 / 17 | 0.345 |
| fold_musique -> fold_strategyqa | heldout_hotpotqa | -3.2 | [-9.0, +3.2] | 14 / 20 | 0.392 |
| fold_musique -> fold_strategyqa | pooled | -3.3 | [-7.8, +1.1] | 25 / 37 | 0.162 |
| fold_musique -> teacher | full_musique | +21.0 | [+14.0, +28.0] | 61 / 13 | 0 |
| fold_musique -> teacher | heldout_2wikimultihopqa | +4.7 | [-1.8, +11.2] | 19 / 11 | 0.2 |
| fold_musique -> teacher | heldout_hotpotqa | +14.3 | [+7.9, +20.6] | 35 / 8 | 4.2e-05 |
| fold_musique -> teacher | heldout_strategyqa | -1.6 | [-9.7, +5.9] | 25 / 28 | 0.784 |
| fold_musique -> teacher | pooled | +10.3 | [+6.7, +13.8] | 140 / 60 | 0 |
| fold_strategyqa -> teacher | full_strategyqa | +2.2 | [-3.7, +8.1] | 37 / 31 | 0.545 |
| fold_strategyqa -> teacher | heldout_2wikimultihopqa | +8.2 | [+1.2, +15.3] | 28 / 14 | 0.0436 |
| fold_strategyqa -> teacher | heldout_hotpotqa | +17.5 | [+11.1, +24.3] | 39 / 6 | 1e-06 |
| fold_strategyqa -> teacher | heldout_musique | +23.2 | [+16.3, +30.0] | 55 / 8 | 0 |
| fold_strategyqa -> teacher | pooled | +12.0 | [+8.6, +15.3] | 159 / 59 | 0 |
