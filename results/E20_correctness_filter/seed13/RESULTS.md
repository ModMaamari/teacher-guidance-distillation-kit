# Results

## Per arm and test set

| arm | test set | n | done | EM | F1 | cover | judge | doc recall | steps | vol. finish | tokens/ep | latency s | API $ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| base | heldout_2wikimultihopqa | 170 | yes | 0.018 | 0.120 | 0.306 | 0.353 | 0.810 | 2.98 | 0.02 | 5,182 | 25.5 | 0.0000 |
| base | heldout_hotpotqa | 189 | yes | 0.169 | 0.240 | 0.381 | 0.429 | 0.759 | 2.91 | 0.09 | 5,120 | 20.1 | 0.0000 |
| base | heldout_musique | 203 | yes | 0.020 | 0.084 | 0.153 | 0.172 | 0.597 | 3.00 | 0.00 | 5,052 | 17.5 | 0.0000 |
| base | heldout_strategyqa | 185 | yes | 0.000 | 0.011 | 0.097 | 0.151 | 0.815 | 2.98 | 0.02 | 4,923 | 17.0 | 0.0000 |
| correct13 | heldout_2wikimultihopqa | 170 | yes | 0.053 | 0.207 | 0.782 | 0.788 | 0.860 | 2.93 | 0.07 | 5,316 | 18.4 | 0.0000 |
| correct13 | heldout_hotpotqa | 189 | yes | 0.270 | 0.373 | 0.661 | 0.688 | 0.783 | 2.78 | 0.22 | 4,936 | 17.9 | 0.0000 |
| correct13 | heldout_musique | 203 | yes | 0.069 | 0.206 | 0.429 | 0.493 | 0.679 | 2.93 | 0.07 | 5,233 | 18.6 | 0.0000 |
| correct13 | heldout_strategyqa | 185 | yes | 0.000 | 0.034 | 0.686 | 0.724 | 0.834 | 2.95 | 0.05 | 5,161 | 19.9 | 0.0000 |
| mixall13 | heldout_2wikimultihopqa | 170 | yes | 0.053 | 0.206 | 0.735 | 0.776 | 0.837 | 2.92 | 0.08 | 5,241 | 24.5 | 0.0000 |
| mixall13 | heldout_hotpotqa | 189 | yes | 0.249 | 0.354 | 0.640 | 0.656 | 0.765 | 2.76 | 0.24 | 4,910 | 23.2 | 0.0000 |
| mixall13 | heldout_musique | 203 | yes | 0.074 | 0.190 | 0.399 | 0.424 | 0.638 | 2.93 | 0.07 | 5,185 | 23.9 | 0.0000 |
| mixall13 | heldout_strategyqa | 185 | yes | 0.000 | 0.032 | 0.508 | 0.697 | 0.823 | 2.94 | 0.06 | 5,132 | 25.8 | 0.0000 |
| mixmatch13 | heldout_2wikimultihopqa | 170 | yes | 0.029 | 0.177 | 0.706 | 0.718 | 0.843 | 2.94 | 0.06 | 5,404 | 44.4 | 0.0000 |
| mixmatch13 | heldout_hotpotqa | 189 | yes | 0.249 | 0.340 | 0.630 | 0.645 | 0.765 | 2.76 | 0.24 | 4,994 | 42.0 | 0.0000 |
| mixmatch13 | heldout_musique | 203 | yes | 0.049 | 0.170 | 0.355 | 0.419 | 0.638 | 2.89 | 0.11 | 5,216 | 44.4 | 0.0000 |
| mixmatch13 | heldout_strategyqa | 185 | yes | 0.000 | 0.032 | 0.524 | 0.686 | 0.839 | 2.91 | 0.09 | 5,178 | 47.3 | 0.0000 |
| wrongonly | heldout_2wikimultihopqa | 170 | yes | 0.006 | 0.147 | 0.647 | 0.706 | 0.827 | 2.95 | 0.05 | 5,279 | 25.2 | 0.0000 |
| wrongonly | heldout_hotpotqa | 189 | yes | 0.159 | 0.271 | 0.577 | 0.598 | 0.746 | 2.81 | 0.19 | 5,119 | 24.1 | 0.0000 |
| wrongonly | heldout_musique | 203 | yes | 0.044 | 0.162 | 0.345 | 0.399 | 0.639 | 2.95 | 0.05 | 5,341 | 25.1 | 0.0000 |
| wrongonly | heldout_strategyqa | 185 | yes | 0.000 | 0.028 | 0.438 | 0.681 | 0.824 | 2.95 | 0.05 | 5,221 | 26.1 | 0.0000 |

## Pooled per arm

| arm | test sets | n | EM | F1 | cover | judge | steps | tokens/ep | API $ |
|---|---|---|---|---|---|---|---|---|---|
| base | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.052 | 0.113 | 0.232 | 0.273 | 2.97 | 5,067 | 0.0000 |
| correct13 | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.099 | 0.206 | 0.632 | 0.667 | 2.90 | 5,159 | 0.0000 |
| mixall13 | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.095 | 0.196 | 0.564 | 0.630 | 2.89 | 5,115 | 0.0000 |
| mixmatch13 | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.083 | 0.180 | 0.546 | 0.610 | 2.87 | 5,193 | 0.0000 |
| wrongonly | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.053 | 0.153 | 0.495 | 0.589 | 2.91 | 5,241 | 0.0000 |

## Paired comparisons (judge-correct, b − a)

| a -> b | scope | Δ pts | 95% CI | b wins / a wins | McNemar p |
|---|---|---|---|---|---|
| base -> correct13 | heldout_2wikimultihopqa | +43.5 | [+35.3, +51.8] | 79 / 5 | 0 |
| base -> correct13 | heldout_hotpotqa | +25.9 | [+18.5, +33.3] | 57 / 8 | 0 |
| base -> correct13 | heldout_musique | +32.0 | [+24.6, +39.9] | 74 / 9 | 0 |
| base -> correct13 | heldout_strategyqa | +57.3 | [+49.7, +64.3] | 108 / 2 | 0 |
| base -> correct13 | pooled | +39.4 | [+35.5, +43.4] | 318 / 24 | 0 |
| base -> mixall13 | heldout_2wikimultihopqa | +42.4 | [+34.1, +50.6] | 77 / 5 | 0 |
| base -> mixall13 | heldout_hotpotqa | +22.8 | [+15.3, +30.2] | 51 / 8 | 0 |
| base -> mixall13 | heldout_musique | +25.1 | [+17.7, +33.0] | 63 / 12 | 0 |
| base -> mixall13 | heldout_strategyqa | +54.6 | [+47.0, +61.6] | 102 / 1 | 0 |
| base -> mixall13 | pooled | +35.7 | [+31.7, +39.6] | 293 / 26 | 0 |
| base -> mixmatch13 | heldout_2wikimultihopqa | +36.5 | [+28.2, +44.7] | 68 / 6 | 0 |
| base -> mixmatch13 | heldout_hotpotqa | +21.7 | [+14.3, +29.1] | 50 / 9 | 0 |
| base -> mixmatch13 | heldout_musique | +24.6 | [+17.2, +32.5] | 62 / 12 | 0 |
| base -> mixmatch13 | heldout_strategyqa | +53.5 | [+46.0, +61.1] | 101 / 2 | 0 |
| base -> mixmatch13 | pooled | +33.7 | [+29.8, +37.6] | 281 / 29 | 0 |
| base -> wrongonly | heldout_2wikimultihopqa | +35.3 | [+27.1, +43.5] | 68 / 8 | 0 |
| base -> wrongonly | heldout_hotpotqa | +16.9 | [+9.0, +24.9] | 48 / 16 | 7.7e-05 |
| base -> wrongonly | heldout_musique | +22.7 | [+14.8, +30.5] | 61 / 15 | 0 |
| base -> wrongonly | heldout_strategyqa | +53.0 | [+45.4, +60.5] | 99 / 1 | 0 |
| base -> wrongonly | pooled | +31.6 | [+27.4, +35.7] | 276 / 40 | 0 |
| correct13 -> mixall13 | heldout_2wikimultihopqa | -1.2 | [-6.5, +4.1] | 9 / 11 | 0.824 |
| correct13 -> mixall13 | heldout_hotpotqa | -3.2 | [-7.9, +1.6] | 8 / 14 | 0.286 |
| correct13 -> mixall13 | heldout_musique | -6.9 | [-13.3, -0.5] | 16 / 30 | 0.0541 |
| correct13 -> mixall13 | heldout_strategyqa | -2.7 | [-7.6, +2.2] | 8 / 13 | 0.383 |
| correct13 -> mixall13 | pooled | -3.6 | [-6.4, -0.9] | 41 / 68 | 0.0124 |
| correct13 -> mixmatch13 | heldout_2wikimultihopqa | -7.1 | [-12.3, -1.8] | 6 / 18 | 0.0227 |
| correct13 -> mixmatch13 | heldout_hotpotqa | -4.2 | [-9.0, +0.5] | 7 / 15 | 0.134 |
| correct13 -> mixmatch13 | heldout_musique | -7.4 | [-13.8, -1.0] | 16 / 31 | 0.04 |
| correct13 -> mixmatch13 | heldout_strategyqa | -3.8 | [-8.6, +0.5] | 6 / 13 | 0.167 |
| correct13 -> mixmatch13 | pooled | -5.6 | [-8.4, -2.9] | 35 / 77 | 9e-05 |
| correct13 -> wrongonly | heldout_2wikimultihopqa | -8.2 | [-14.1, -2.4] | 7 / 21 | 0.0125 |
| correct13 -> wrongonly | heldout_hotpotqa | -9.0 | [-14.3, -3.7] | 5 / 22 | 0.00151 |
| correct13 -> wrongonly | heldout_musique | -9.4 | [-15.3, -3.5] | 10 / 29 | 0.00338 |
| correct13 -> wrongonly | heldout_strategyqa | -4.3 | [-9.2, +0.5] | 7 / 15 | 0.134 |
| correct13 -> wrongonly | pooled | -7.8 | [-10.6, -5.1] | 29 / 87 | 0 |
| mixall13 -> mixmatch13 | heldout_2wikimultihopqa | -5.9 | [-11.2, -0.6] | 5 / 15 | 0.0414 |
| mixall13 -> mixmatch13 | heldout_hotpotqa | -1.1 | [-5.3, +3.2] | 7 / 9 | 0.804 |
| mixall13 -> mixmatch13 | heldout_musique | -0.5 | [-6.4, +5.4] | 19 / 20 | 1 |
| mixall13 -> mixmatch13 | heldout_strategyqa | -1.1 | [-5.4, +3.2] | 8 / 10 | 0.815 |
| mixall13 -> mixmatch13 | pooled | -2.0 | [-4.5, +0.4] | 39 / 54 | 0.146 |
| mixall13 -> wrongonly | heldout_2wikimultihopqa | -7.1 | [-12.9, -1.2] | 7 / 19 | 0.029 |
| mixall13 -> wrongonly | heldout_hotpotqa | -5.8 | [-10.1, -1.6] | 4 / 15 | 0.0192 |
| mixall13 -> wrongonly | heldout_musique | -2.5 | [-7.9, +3.0] | 13 / 18 | 0.473 |
| mixall13 -> wrongonly | heldout_strategyqa | -1.6 | [-6.5, +2.7] | 8 / 11 | 0.648 |
| mixall13 -> wrongonly | pooled | -4.2 | [-6.7, -1.6] | 32 / 63 | 0.00192 |
| mixmatch13 -> wrongonly | heldout_2wikimultihopqa | -1.2 | [-7.1, +4.7] | 12 / 14 | 0.845 |
| mixmatch13 -> wrongonly | heldout_hotpotqa | -4.8 | [-9.5, +0.0] | 6 / 15 | 0.0784 |
| mixmatch13 -> wrongonly | heldout_musique | -2.0 | [-7.4, +3.5] | 13 / 17 | 0.585 |
| mixmatch13 -> wrongonly | heldout_strategyqa | -0.5 | [-4.9, +3.8] | 7 / 8 | 1 |
| mixmatch13 -> wrongonly | pooled | -2.1 | [-4.7, +0.4] | 38 / 54 | 0.117 |
