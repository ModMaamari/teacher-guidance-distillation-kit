# Results

## Per arm and test set

| arm | test set | n | done | EM | F1 | cover | judge | doc recall | steps | vol. finish | tokens/ep | latency s | API $ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| base | heldout_2wikimultihopqa | 170 | yes | 0.018 | 0.120 | 0.306 | 0.353 | 0.810 | 2.98 | 0.02 | 5,182 | 25.5 | 0.0000 |
| base | heldout_hotpotqa | 189 | yes | 0.169 | 0.240 | 0.381 | 0.429 | 0.759 | 2.91 | 0.09 | 5,120 | 20.1 | 0.0000 |
| base | heldout_musique | 203 | yes | 0.020 | 0.084 | 0.153 | 0.172 | 0.597 | 3.00 | 0.00 | 5,052 | 17.5 | 0.0000 |
| base | heldout_strategyqa | 185 | yes | 0.000 | 0.011 | 0.097 | 0.151 | 0.815 | 2.98 | 0.02 | 4,923 | 17.0 | 0.0000 |
| seed13 | heldout_2wikimultihopqa | 170 | yes | 0.429 | 0.543 | 0.765 | 0.765 | 0.854 | 2.93 | 0.07 | 5,655 | 24.3 | 0.0000 |
| seed13 | heldout_hotpotqa | 189 | yes | 0.339 | 0.425 | 0.587 | 0.635 | 0.786 | 2.83 | 0.17 | 5,249 | 22.6 | 0.0000 |
| seed13 | heldout_musique | 203 | yes | 0.163 | 0.287 | 0.350 | 0.389 | 0.663 | 2.99 | 0.01 | 5,253 | 20.8 | 0.0000 |
| seed13 | heldout_strategyqa | 185 | yes | 0.508 | 0.529 | 0.724 | 0.730 | 0.826 | 2.92 | 0.08 | 5,214 | 23.2 | 0.0000 |
| seed17 | heldout_2wikimultihopqa | 170 | yes | 0.300 | 0.444 | 0.776 | 0.782 | 0.871 | 2.93 | 0.07 | 5,680 | 26.4 | 0.0000 |
| seed17 | heldout_hotpotqa | 189 | yes | 0.370 | 0.462 | 0.577 | 0.630 | 0.780 | 2.89 | 0.11 | 5,456 | 25.2 | 0.0000 |
| seed17 | heldout_musique | 203 | yes | 0.172 | 0.271 | 0.345 | 0.369 | 0.688 | 2.96 | 0.04 | 5,247 | 24.2 | 0.0000 |
| seed17 | heldout_strategyqa | 185 | yes | 0.454 | 0.480 | 0.714 | 0.719 | 0.817 | 2.90 | 0.09 | 5,179 | 24.8 | 0.0000 |
| seed23 | heldout_2wikimultihopqa | 170 | yes | 0.359 | 0.486 | 0.741 | 0.765 | 0.840 | 2.92 | 0.08 | 5,716 | 25.8 | 0.0000 |
| seed23 | heldout_hotpotqa | 189 | yes | 0.349 | 0.428 | 0.571 | 0.630 | 0.757 | 2.79 | 0.21 | 5,178 | 23.5 | 0.0000 |
| seed23 | heldout_musique | 203 | yes | 0.172 | 0.273 | 0.315 | 0.369 | 0.680 | 2.96 | 0.04 | 5,206 | 22.4 | 0.0000 |
| seed23 | heldout_strategyqa | 185 | yes | 0.508 | 0.529 | 0.730 | 0.751 | 0.828 | 2.86 | 0.14 | 5,108 | 23.1 | 0.0000 |

## Pooled per arm

| arm | test sets | n | EM | F1 | cover | judge | steps | tokens/ep | API $ |
|---|---|---|---|---|---|---|---|---|---|
| base | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.052 | 0.113 | 0.232 | 0.273 | 2.97 | 5,067 | 0.0000 |
| seed13 | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.353 | 0.440 | 0.597 | 0.621 | 2.92 | 5,334 | 0.0000 |
| seed17 | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.321 | 0.411 | 0.593 | 0.616 | 2.92 | 5,382 | 0.0000 |
| seed23 | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.343 | 0.424 | 0.580 | 0.620 | 2.88 | 5,291 | 0.0000 |

## Paired comparisons (judge-correct, b − a)

| a -> b | scope | Δ pts | 95% CI | b wins / a wins | McNemar p |
|---|---|---|---|---|---|
| base -> seed13 | heldout_2wikimultihopqa | +41.2 | [+32.9, +48.8] | 73 / 3 | 0 |
| base -> seed13 | heldout_hotpotqa | +20.6 | [+13.2, +28.0] | 51 / 12 | 1e-06 |
| base -> seed13 | heldout_musique | +21.7 | [+14.3, +29.1] | 57 / 13 | 0 |
| base -> seed13 | heldout_strategyqa | +57.8 | [+50.3, +65.4] | 108 / 1 | 0 |
| base -> seed13 | pooled | +34.8 | [+30.8, +38.7] | 289 / 29 | 0 |
| base -> seed17 | heldout_2wikimultihopqa | +42.9 | [+35.3, +50.6] | 75 / 2 | 0 |
| base -> seed17 | heldout_hotpotqa | +20.1 | [+13.2, +27.5] | 47 / 9 | 0 |
| base -> seed17 | heldout_musique | +19.7 | [+12.3, +27.1] | 54 / 14 | 1e-06 |
| base -> seed17 | heldout_strategyqa | +56.8 | [+49.7, +63.8] | 105 / 0 | 0 |
| base -> seed17 | pooled | +34.3 | [+30.4, +38.1] | 281 / 25 | 0 |
| base -> seed23 | heldout_2wikimultihopqa | +41.2 | [+33.5, +48.8] | 72 / 2 | 0 |
| base -> seed23 | heldout_hotpotqa | +20.1 | [+12.7, +27.5] | 49 / 11 | 1e-06 |
| base -> seed23 | heldout_musique | +19.7 | [+12.3, +27.1] | 54 / 14 | 1e-06 |
| base -> seed23 | heldout_strategyqa | +60.0 | [+53.0, +67.0] | 111 / 0 | 0 |
| base -> seed23 | pooled | +34.7 | [+30.8, +38.6] | 286 / 27 | 0 |
| seed13 -> seed17 | heldout_2wikimultihopqa | +1.8 | [-3.5, +7.1] | 12 / 9 | 0.664 |
| seed13 -> seed17 | heldout_hotpotqa | -0.5 | [-5.8, +4.8] | 12 / 13 | 1 |
| seed13 -> seed17 | heldout_musique | -2.0 | [-8.4, +4.4] | 22 / 26 | 0.665 |
| seed13 -> seed17 | heldout_strategyqa | -1.1 | [-5.9, +3.8] | 9 / 11 | 0.824 |
| seed13 -> seed17 | pooled | -0.5 | [-3.4, +2.3] | 55 / 59 | 0.779 |
| seed13 -> seed23 | heldout_2wikimultihopqa | +0.0 | [-5.3, +5.3] | 11 / 11 | 1 |
| seed13 -> seed23 | heldout_hotpotqa | -0.5 | [-6.3, +5.3] | 16 / 17 | 1 |
| seed13 -> seed23 | heldout_musique | -2.0 | [-7.9, +3.9] | 18 / 22 | 0.636 |
| seed13 -> seed23 | heldout_strategyqa | +2.2 | [-2.7, +7.0] | 13 / 9 | 0.523 |
| seed13 -> seed23 | pooled | -0.1 | [-2.9, +2.7] | 58 / 59 | 1 |
| seed17 -> seed23 | heldout_2wikimultihopqa | -1.8 | [-7.1, +3.5] | 9 / 12 | 0.664 |
| seed17 -> seed23 | heldout_hotpotqa | +0.0 | [-5.3, +5.3] | 12 / 12 | 1 |
| seed17 -> seed23 | heldout_musique | +0.0 | [-6.4, +6.4] | 22 / 22 | 1 |
| seed17 -> seed23 | heldout_strategyqa | +3.2 | [-2.2, +8.6] | 15 / 9 | 0.307 |
| seed17 -> seed23 | pooled | +0.4 | [-2.4, +3.2] | 58 / 55 | 0.851 |
