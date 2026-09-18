# Results

## Per arm and test set

| arm | test set | n | done | EM | F1 | cover | judge | doc recall | steps | vol. finish | tokens/ep | latency s | API $ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| base | heldout_2wikimultihopqa | 170 | yes | 0.018 | 0.120 | 0.306 | 0.353 | 0.810 | 2.98 | 0.02 | 5,182 | 25.5 | 0.0000 |
| base | heldout_hotpotqa | 189 | yes | 0.169 | 0.240 | 0.381 | 0.429 | 0.759 | 2.91 | 0.09 | 5,120 | 20.1 | 0.0000 |
| base | heldout_musique | 203 | yes | 0.020 | 0.084 | 0.153 | 0.172 | 0.597 | 3.00 | 0.00 | 5,052 | 17.5 | 0.0000 |
| base | heldout_strategyqa | 185 | yes | 0.000 | 0.011 | 0.097 | 0.151 | 0.815 | 2.98 | 0.02 | 4,923 | 17.0 | 0.0000 |
| ep1000 | heldout_2wikimultihopqa | 170 | yes | 0.329 | 0.503 | 0.782 | 0.776 | 0.882 | 2.91 | 0.09 | 5,510 | 23.8 | 0.0000 |
| ep1000 | heldout_hotpotqa | 189 | yes | 0.360 | 0.436 | 0.593 | 0.619 | 0.799 | 2.82 | 0.18 | 5,345 | 26.2 | 0.0000 |
| ep1000 | heldout_musique | 203 | yes | 0.138 | 0.235 | 0.330 | 0.355 | 0.705 | 2.96 | 0.04 | 5,273 | 21.5 | 0.0000 |
| ep1000 | heldout_strategyqa | 185 | yes | 0.416 | 0.442 | 0.692 | 0.697 | 0.818 | 2.88 | 0.11 | 5,238 | 25.7 | 0.0000 |
| ep2000 | heldout_2wikimultihopqa | 170 | yes | 0.335 | 0.494 | 0.753 | 0.753 | 0.866 | 2.91 | 0.09 | 5,632 | 42.5 | 0.0000 |
| ep2000 | heldout_hotpotqa | 189 | yes | 0.344 | 0.426 | 0.582 | 0.630 | 0.780 | 2.87 | 0.13 | 5,387 | 40.3 | 0.0000 |
| ep2000 | heldout_musique | 203 | yes | 0.172 | 0.286 | 0.340 | 0.379 | 0.656 | 2.97 | 0.03 | 5,324 | 37.9 | 0.0000 |
| ep2000 | heldout_strategyqa | 185 | yes | 0.465 | 0.486 | 0.670 | 0.670 | 0.814 | 2.90 | 0.10 | 5,255 | 40.5 | 0.0000 |
| ep4000 | heldout_2wikimultihopqa | 170 | yes | 0.265 | 0.413 | 0.771 | 0.771 | 0.874 | 2.89 | 0.11 | 5,635 | 46.7 | 0.0000 |
| ep4000 | heldout_hotpotqa | 189 | yes | 0.349 | 0.424 | 0.603 | 0.645 | 0.799 | 2.83 | 0.17 | 5,400 | 45.4 | 0.0000 |
| ep4000 | heldout_musique | 203 | yes | 0.153 | 0.269 | 0.330 | 0.355 | 0.649 | 2.94 | 0.06 | 5,265 | 42.0 | 0.0000 |
| ep4000 | heldout_strategyqa | 185 | yes | 0.481 | 0.506 | 0.714 | 0.719 | 0.826 | 2.84 | 0.15 | 5,113 | 44.2 | 0.0000 |
| ep500 | heldout_2wikimultihopqa | 170 | yes | 0.418 | 0.555 | 0.759 | 0.741 | 0.879 | 2.91 | 0.09 | 5,422 | 22.9 | 0.0000 |
| ep500 | heldout_hotpotqa | 189 | yes | 0.370 | 0.441 | 0.550 | 0.587 | 0.765 | 2.87 | 0.13 | 5,126 | 21.6 | 0.0000 |
| ep500 | heldout_musique | 203 | yes | 0.148 | 0.252 | 0.340 | 0.364 | 0.693 | 2.93 | 0.07 | 5,173 | 21.2 | 0.0000 |
| ep500 | heldout_strategyqa | 185 | yes | 0.535 | 0.546 | 0.643 | 0.643 | 0.789 | 2.91 | 0.09 | 5,100 | 22.6 | 0.0000 |
| full | heldout_2wikimultihopqa | 170 | yes | 0.429 | 0.543 | 0.765 | 0.765 | 0.854 | 2.93 | 0.07 | 5,655 | 24.3 | 0.0000 |
| full | heldout_hotpotqa | 189 | yes | 0.339 | 0.425 | 0.587 | 0.635 | 0.786 | 2.83 | 0.17 | 5,249 | 22.6 | 0.0000 |
| full | heldout_musique | 203 | yes | 0.163 | 0.287 | 0.350 | 0.389 | 0.663 | 2.99 | 0.01 | 5,253 | 20.8 | 0.0000 |
| full | heldout_strategyqa | 185 | yes | 0.508 | 0.529 | 0.724 | 0.730 | 0.826 | 2.92 | 0.08 | 5,214 | 23.2 | 0.0000 |

## Pooled per arm

| arm | test sets | n | EM | F1 | cover | judge | steps | tokens/ep | API $ |
|---|---|---|---|---|---|---|---|---|---|
| base | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.052 | 0.113 | 0.232 | 0.273 | 2.97 | 5,067 | 0.0000 |
| ep1000 | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.307 | 0.398 | 0.589 | 0.602 | 2.89 | 5,336 | 0.0000 |
| ep2000 | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.325 | 0.418 | 0.577 | 0.600 | 2.91 | 5,393 | 0.0000 |
| ep4000 | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.309 | 0.400 | 0.594 | 0.613 | 2.88 | 5,346 | 0.0000 |
| ep500 | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.361 | 0.442 | 0.564 | 0.576 | 2.90 | 5,200 | 0.0000 |
| full | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.353 | 0.440 | 0.597 | 0.621 | 2.92 | 5,334 | 0.0000 |

## Paired comparisons (judge-correct, b − a)

| a -> b | scope | Δ pts | 95% CI | b wins / a wins | McNemar p |
|---|---|---|---|---|---|
| base -> ep1000 | heldout_2wikimultihopqa | +42.4 | [+34.1, +50.6] | 77 / 5 | 0 |
| base -> ep1000 | heldout_hotpotqa | +19.1 | [+12.2, +26.5] | 45 / 9 | 1e-06 |
| base -> ep1000 | heldout_musique | +18.2 | [+11.3, +25.6] | 49 / 12 | 2e-06 |
| base -> ep1000 | heldout_strategyqa | +54.6 | [+47.6, +62.2] | 102 / 1 | 0 |
| base -> ep1000 | pooled | +32.9 | [+29.0, +36.8] | 273 / 27 | 0 |
| base -> ep2000 | heldout_2wikimultihopqa | +40.0 | [+32.4, +48.2] | 72 / 4 | 0 |
| base -> ep2000 | heldout_hotpotqa | +20.1 | [+12.7, +27.5] | 48 / 10 | 0 |
| base -> ep2000 | heldout_musique | +20.7 | [+13.8, +28.1] | 53 / 11 | 0 |
| base -> ep2000 | heldout_strategyqa | +51.9 | [+44.3, +59.5] | 97 / 1 | 0 |
| base -> ep2000 | pooled | +32.7 | [+28.8, +36.5] | 270 / 26 | 0 |
| base -> ep4000 | heldout_2wikimultihopqa | +41.8 | [+33.5, +50.0] | 75 / 4 | 0 |
| base -> ep4000 | heldout_hotpotqa | +21.7 | [+14.3, +29.1] | 50 / 9 | 0 |
| base -> ep4000 | heldout_musique | +18.2 | [+11.8, +24.6] | 46 / 9 | 0 |
| base -> ep4000 | heldout_strategyqa | +56.8 | [+49.2, +64.3] | 106 / 1 | 0 |
| base -> ep4000 | pooled | +34.0 | [+30.2, +37.9] | 277 / 23 | 0 |
| base -> ep500 | heldout_2wikimultihopqa | +38.8 | [+30.6, +47.1] | 73 / 7 | 0 |
| base -> ep500 | heldout_hotpotqa | +15.9 | [+9.0, +23.3] | 41 / 11 | 3.6e-05 |
| base -> ep500 | heldout_musique | +19.2 | [+11.8, +27.1] | 55 / 16 | 4e-06 |
| base -> ep500 | heldout_strategyqa | +49.2 | [+41.6, +56.8] | 93 / 2 | 0 |
| base -> ep500 | pooled | +30.2 | [+26.4, +34.3] | 262 / 36 | 0 |
| base -> full | heldout_2wikimultihopqa | +41.2 | [+32.9, +48.8] | 73 / 3 | 0 |
| base -> full | heldout_hotpotqa | +20.6 | [+13.2, +28.0] | 51 / 12 | 1e-06 |
| base -> full | heldout_musique | +21.7 | [+14.3, +29.1] | 57 / 13 | 0 |
| base -> full | heldout_strategyqa | +57.8 | [+50.3, +65.4] | 108 / 1 | 0 |
| base -> full | pooled | +34.8 | [+30.8, +38.7] | 289 / 29 | 0 |
| ep1000 -> ep2000 | heldout_2wikimultihopqa | -2.4 | [-7.6, +2.9] | 8 / 12 | 0.503 |
| ep1000 -> ep2000 | heldout_hotpotqa | +1.1 | [-4.8, +7.4] | 18 / 16 | 0.864 |
| ep1000 -> ep2000 | heldout_musique | +2.5 | [-3.9, +8.9] | 26 / 21 | 0.56 |
| ep1000 -> ep2000 | heldout_strategyqa | -2.7 | [-8.1, +2.2] | 9 / 14 | 0.405 |
| ep1000 -> ep2000 | pooled | -0.3 | [-3.2, +2.7] | 61 / 63 | 0.928 |
| ep1000 -> ep4000 | heldout_2wikimultihopqa | -0.6 | [-7.1, +5.9] | 14 / 15 | 1 |
| ep1000 -> ep4000 | heldout_hotpotqa | +2.6 | [-2.6, +8.5] | 17 / 12 | 0.458 |
| ep1000 -> ep4000 | heldout_musique | +0.0 | [-5.9, +5.9] | 18 / 18 | 1 |
| ep1000 -> ep4000 | heldout_strategyqa | +2.2 | [-2.7, +7.0] | 13 / 9 | 0.523 |
| ep1000 -> ep4000 | pooled | +1.1 | [-1.7, +4.0] | 62 / 54 | 0.516 |
| ep1000 -> ep500 | heldout_2wikimultihopqa | -3.5 | [-10.0, +2.9] | 13 / 19 | 0.377 |
| ep1000 -> ep500 | heldout_hotpotqa | -3.2 | [-8.5, +1.6] | 9 / 15 | 0.307 |
| ep1000 -> ep500 | heldout_musique | +1.0 | [-5.4, +7.4] | 24 / 22 | 0.883 |
| ep1000 -> ep500 | heldout_strategyqa | -5.4 | [-10.8, -0.5] | 7 / 17 | 0.0639 |
| ep1000 -> ep500 | pooled | -2.7 | [-5.6, +0.3] | 53 / 73 | 0.0901 |
| ep1000 -> full | heldout_2wikimultihopqa | -1.2 | [-7.1, +4.1] | 11 / 13 | 0.839 |
| ep1000 -> full | heldout_hotpotqa | +1.6 | [-3.7, +7.4] | 16 / 13 | 0.711 |
| ep1000 -> full | heldout_musique | +3.5 | [-3.5, +10.3] | 28 / 21 | 0.392 |
| ep1000 -> full | heldout_strategyqa | +3.2 | [-1.6, +8.6] | 15 / 9 | 0.307 |
| ep1000 -> full | pooled | +1.9 | [-1.1, +5.0] | 70 / 56 | 0.247 |
| ep2000 -> ep4000 | heldout_2wikimultihopqa | +1.8 | [-4.1, +7.6] | 14 / 11 | 0.69 |
| ep2000 -> ep4000 | heldout_hotpotqa | +1.6 | [-3.7, +6.9] | 14 / 11 | 0.69 |
| ep2000 -> ep4000 | heldout_musique | -2.5 | [-8.9, +3.9] | 20 / 25 | 0.551 |
| ep2000 -> ep4000 | heldout_strategyqa | +4.9 | [+0.0, +10.3] | 16 / 7 | 0.0931 |
| ep2000 -> ep4000 | pooled | +1.3 | [-1.6, +4.2] | 64 / 54 | 0.407 |
| ep2000 -> ep500 | heldout_2wikimultihopqa | -1.2 | [-7.1, +4.7] | 12 / 14 | 0.845 |
| ep2000 -> ep500 | heldout_hotpotqa | -4.2 | [-9.5, +1.1] | 10 / 18 | 0.185 |
| ep2000 -> ep500 | heldout_musique | -1.5 | [-8.9, +5.9] | 28 / 31 | 0.795 |
| ep2000 -> ep500 | heldout_strategyqa | -2.7 | [-7.6, +2.2] | 9 / 14 | 0.405 |
| ep2000 -> ep500 | pooled | -2.4 | [-5.3, +0.7] | 59 / 77 | 0.145 |
| ep2000 -> full | heldout_2wikimultihopqa | +1.2 | [-4.1, +6.5] | 12 / 10 | 0.832 |
| ep2000 -> full | heldout_hotpotqa | +0.5 | [-5.3, +6.3] | 17 / 16 | 1 |
| ep2000 -> full | heldout_musique | +1.0 | [-5.9, +7.4] | 25 / 23 | 0.885 |
| ep2000 -> full | heldout_strategyqa | +5.9 | [+0.5, +11.9] | 20 / 9 | 0.0614 |
| ep2000 -> full | pooled | +2.1 | [-0.8, +5.2] | 74 / 58 | 0.191 |
| ep4000 -> ep500 | heldout_2wikimultihopqa | -2.9 | [-10.0, +3.5] | 15 / 20 | 0.5 |
| ep4000 -> ep500 | heldout_hotpotqa | -5.8 | [-11.6, +0.0] | 11 / 22 | 0.0801 |
| ep4000 -> ep500 | heldout_musique | +1.0 | [-5.9, +7.9] | 27 / 25 | 0.89 |
| ep4000 -> ep500 | heldout_strategyqa | -7.6 | [-12.4, -3.2] | 3 / 17 | 0.00258 |
| ep4000 -> ep500 | pooled | -3.8 | [-6.8, -0.7] | 56 / 84 | 0.0222 |
| ep4000 -> full | heldout_2wikimultihopqa | -0.6 | [-5.9, +4.7] | 11 / 12 | 1 |
| ep4000 -> full | heldout_hotpotqa | -1.1 | [-6.3, +4.2] | 12 / 14 | 0.845 |
| ep4000 -> full | heldout_musique | +3.5 | [-3.0, +9.4] | 24 / 17 | 0.349 |
| ep4000 -> full | heldout_strategyqa | +1.1 | [-3.2, +5.4] | 10 / 8 | 0.815 |
| ep4000 -> full | pooled | +0.8 | [-1.9, +3.5] | 57 / 51 | 0.631 |
| ep500 -> full | heldout_2wikimultihopqa | +2.4 | [-4.7, +9.4] | 20 / 16 | 0.618 |
| ep500 -> full | heldout_hotpotqa | +4.8 | [-1.1, +10.6] | 22 / 13 | 0.175 |
| ep500 -> full | heldout_musique | +2.5 | [-4.9, +9.4] | 30 / 25 | 0.59 |
| ep500 -> full | heldout_strategyqa | +8.6 | [+3.2, +14.1] | 22 / 6 | 0.00372 |
| ep500 -> full | pooled | +4.5 | [+1.3, +7.8] | 94 / 60 | 0.00763 |
