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
| correct17 | heldout_2wikimultihopqa | 170 | yes | 0.053 | 0.203 | 0.759 | 0.776 | 0.841 | 2.95 | 0.05 | 5,402 | 23.0 | 0.0000 |
| correct17 | heldout_hotpotqa | 189 | yes | 0.296 | 0.381 | 0.656 | 0.667 | 0.759 | 2.79 | 0.21 | 5,054 | 22.0 | 0.0000 |
| correct17 | heldout_musique | 203 | yes | 0.049 | 0.183 | 0.399 | 0.453 | 0.660 | 2.93 | 0.06 | 5,293 | 23.0 | 0.0000 |
| correct17 | heldout_strategyqa | 185 | yes | 0.000 | 0.036 | 0.681 | 0.730 | 0.833 | 2.91 | 0.09 | 5,113 | 24.7 | 0.0000 |
| correct23 | heldout_2wikimultihopqa | 170 | yes | 0.053 | 0.207 | 0.747 | 0.735 | 0.846 | 2.94 | 0.06 | 5,300 | 22.7 | 0.0000 |
| correct23 | heldout_hotpotqa | 189 | yes | 0.249 | 0.345 | 0.640 | 0.667 | 0.767 | 2.75 | 0.25 | 4,978 | 21.8 | 0.0000 |
| correct23 | heldout_musique | 203 | yes | 0.049 | 0.186 | 0.399 | 0.448 | 0.663 | 2.93 | 0.07 | 5,292 | 23.8 | 0.0000 |
| correct23 | heldout_strategyqa | 185 | yes | 0.000 | 0.034 | 0.670 | 0.703 | 0.818 | 2.89 | 0.11 | 5,050 | 24.4 | 0.0000 |
| mixmatch13 | heldout_2wikimultihopqa | 170 | yes | 0.029 | 0.177 | 0.706 | 0.718 | 0.843 | 2.94 | 0.06 | 5,404 | 44.4 | 0.0000 |
| mixmatch13 | heldout_hotpotqa | 189 | yes | 0.249 | 0.340 | 0.630 | 0.645 | 0.765 | 2.76 | 0.24 | 4,994 | 42.0 | 0.0000 |
| mixmatch13 | heldout_musique | 203 | yes | 0.049 | 0.170 | 0.355 | 0.419 | 0.638 | 2.89 | 0.11 | 5,216 | 44.4 | 0.0000 |
| mixmatch13 | heldout_strategyqa | 185 | yes | 0.000 | 0.032 | 0.524 | 0.686 | 0.839 | 2.91 | 0.09 | 5,178 | 47.3 | 0.0000 |
| mixmatch17 | heldout_2wikimultihopqa | 170 | yes | 0.018 | 0.172 | 0.724 | 0.735 | 0.854 | 2.96 | 0.04 | 5,386 | 27.8 | 0.0000 |
| mixmatch17 | heldout_hotpotqa | 189 | yes | 0.259 | 0.369 | 0.651 | 0.667 | 0.778 | 2.75 | 0.25 | 4,956 | 27.1 | 0.0000 |
| mixmatch17 | heldout_musique | 203 | yes | 0.054 | 0.175 | 0.384 | 0.433 | 0.645 | 2.92 | 0.08 | 5,228 | 28.7 | 0.0000 |
| mixmatch17 | heldout_strategyqa | 185 | yes | 0.000 | 0.031 | 0.524 | 0.686 | 0.838 | 2.95 | 0.05 | 5,205 | 29.8 | 0.0000 |
| mixmatch23 | heldout_2wikimultihopqa | 170 | yes | 0.041 | 0.192 | 0.741 | 0.759 | 0.835 | 2.95 | 0.05 | 5,378 | 27.7 | 0.0000 |
| mixmatch23 | heldout_hotpotqa | 189 | yes | 0.259 | 0.342 | 0.609 | 0.630 | 0.751 | 2.81 | 0.19 | 5,127 | 28.1 | 0.0000 |
| mixmatch23 | heldout_musique | 203 | yes | 0.069 | 0.185 | 0.374 | 0.438 | 0.646 | 2.92 | 0.07 | 5,297 | 28.5 | 0.0000 |
| mixmatch23 | heldout_strategyqa | 185 | yes | 0.000 | 0.031 | 0.524 | 0.697 | 0.827 | 2.94 | 0.06 | 5,232 | 30.4 | 0.0000 |
| wrongonly | heldout_2wikimultihopqa | 170 | yes | 0.006 | 0.147 | 0.647 | 0.706 | 0.827 | 2.95 | 0.05 | 5,279 | 25.2 | 0.0000 |
| wrongonly | heldout_hotpotqa | 189 | yes | 0.159 | 0.271 | 0.577 | 0.598 | 0.746 | 2.81 | 0.19 | 5,119 | 24.1 | 0.0000 |
| wrongonly | heldout_musique | 203 | yes | 0.044 | 0.162 | 0.345 | 0.399 | 0.639 | 2.95 | 0.05 | 5,341 | 25.1 | 0.0000 |
| wrongonly | heldout_strategyqa | 185 | yes | 0.000 | 0.028 | 0.438 | 0.681 | 0.824 | 2.95 | 0.05 | 5,221 | 26.1 | 0.0000 |

## Pooled per arm

| arm | test sets | n | EM | F1 | cover | judge | steps | tokens/ep | API $ |
|---|---|---|---|---|---|---|---|---|---|
| base | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.052 | 0.113 | 0.232 | 0.273 | 2.97 | 5,067 | 0.0000 |
| correct13 | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.099 | 0.206 | 0.632 | 0.667 | 2.90 | 5,159 | 0.0000 |
| correct17 | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.100 | 0.201 | 0.616 | 0.649 | 2.89 | 5,213 | 0.0000 |
| correct23 | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.088 | 0.193 | 0.606 | 0.632 | 2.87 | 5,155 | 0.0000 |
| mixmatch13 | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.083 | 0.180 | 0.546 | 0.610 | 2.87 | 5,193 | 0.0000 |
| mixmatch17 | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.084 | 0.188 | 0.564 | 0.624 | 2.89 | 5,189 | 0.0000 |
| mixmatch23 | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.094 | 0.188 | 0.554 | 0.624 | 2.90 | 5,256 | 0.0000 |
| wrongonly | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.053 | 0.153 | 0.495 | 0.589 | 2.91 | 5,241 | 0.0000 |

## Paired comparisons (judge-correct, b − a)

| a -> b | scope | Δ pts | 95% CI | b wins / a wins | McNemar p |
|---|---|---|---|---|---|
| base -> correct13 | heldout_2wikimultihopqa | +43.5 | [+35.3, +51.8] | 79 / 5 | 0 |
| base -> correct13 | heldout_hotpotqa | +25.9 | [+18.5, +33.3] | 57 / 8 | 0 |
| base -> correct13 | heldout_musique | +32.0 | [+24.6, +39.9] | 74 / 9 | 0 |
| base -> correct13 | heldout_strategyqa | +57.3 | [+49.7, +64.3] | 108 / 2 | 0 |
| base -> correct13 | pooled | +39.4 | [+35.5, +43.4] | 318 / 24 | 0 |
| base -> correct17 | heldout_2wikimultihopqa | +42.4 | [+34.1, +50.6] | 76 / 4 | 0 |
| base -> correct17 | heldout_hotpotqa | +23.8 | [+16.4, +31.2] | 53 / 8 | 0 |
| base -> correct17 | heldout_musique | +28.1 | [+20.2, +36.0] | 69 / 12 | 0 |
| base -> correct17 | heldout_strategyqa | +57.8 | [+50.8, +65.4] | 108 / 1 | 0 |
| base -> correct17 | pooled | +37.6 | [+33.6, +41.6] | 306 / 25 | 0 |
| base -> correct23 | heldout_2wikimultihopqa | +38.2 | [+30.0, +46.5] | 71 / 6 | 0 |
| base -> correct23 | heldout_hotpotqa | +23.8 | [+16.4, +31.2] | 54 / 9 | 0 |
| base -> correct23 | heldout_musique | +27.6 | [+20.2, +35.0] | 65 / 9 | 0 |
| base -> correct23 | heldout_strategyqa | +55.1 | [+47.6, +62.7] | 103 / 1 | 0 |
| base -> correct23 | pooled | +35.9 | [+32.0, +39.8] | 293 / 25 | 0 |
| base -> mixmatch13 | heldout_2wikimultihopqa | +36.5 | [+28.2, +44.7] | 68 / 6 | 0 |
| base -> mixmatch13 | heldout_hotpotqa | +21.7 | [+14.3, +29.1] | 50 / 9 | 0 |
| base -> mixmatch13 | heldout_musique | +24.6 | [+17.2, +32.5] | 62 / 12 | 0 |
| base -> mixmatch13 | heldout_strategyqa | +53.5 | [+46.0, +61.1] | 101 / 2 | 0 |
| base -> mixmatch13 | pooled | +33.7 | [+29.8, +37.6] | 281 / 29 | 0 |
| base -> mixmatch17 | heldout_2wikimultihopqa | +38.2 | [+30.0, +46.5] | 71 / 6 | 0 |
| base -> mixmatch17 | heldout_hotpotqa | +23.8 | [+16.9, +31.2] | 52 / 7 | 0 |
| base -> mixmatch17 | heldout_musique | +26.1 | [+18.7, +33.5] | 64 / 11 | 0 |
| base -> mixmatch17 | heldout_strategyqa | +53.5 | [+46.0, +60.5] | 99 / 0 | 0 |
| base -> mixmatch17 | pooled | +35.1 | [+31.3, +39.0] | 286 / 24 | 0 |
| base -> mixmatch23 | heldout_2wikimultihopqa | +40.6 | [+32.4, +48.8] | 75 / 6 | 0 |
| base -> mixmatch23 | heldout_hotpotqa | +20.1 | [+12.7, +28.0] | 50 / 12 | 1e-06 |
| base -> mixmatch23 | heldout_musique | +26.6 | [+19.2, +34.5] | 66 / 12 | 0 |
| base -> mixmatch23 | heldout_strategyqa | +54.6 | [+47.0, +62.2] | 103 / 2 | 0 |
| base -> mixmatch23 | pooled | +35.1 | [+31.1, +39.1] | 294 / 32 | 0 |
| base -> wrongonly | heldout_2wikimultihopqa | +35.3 | [+27.1, +43.5] | 68 / 8 | 0 |
| base -> wrongonly | heldout_hotpotqa | +16.9 | [+9.0, +24.9] | 48 / 16 | 7.7e-05 |
| base -> wrongonly | heldout_musique | +22.7 | [+14.8, +30.5] | 61 / 15 | 0 |
| base -> wrongonly | heldout_strategyqa | +53.0 | [+45.4, +60.5] | 99 / 1 | 0 |
| base -> wrongonly | pooled | +31.6 | [+27.4, +35.7] | 276 / 40 | 0 |
| correct13 -> correct17 | heldout_2wikimultihopqa | -1.2 | [-6.5, +4.1] | 9 / 11 | 0.824 |
| correct13 -> correct17 | heldout_hotpotqa | -2.1 | [-6.9, +2.6] | 9 / 13 | 0.523 |
| correct13 -> correct17 | heldout_musique | -3.9 | [-9.8, +1.5] | 14 / 22 | 0.243 |
| correct13 -> correct17 | heldout_strategyqa | +0.5 | [-3.2, +4.3] | 7 / 6 | 1 |
| correct13 -> correct17 | pooled | -1.7 | [-4.3, +0.7] | 39 / 52 | 0.208 |
| correct13 -> correct23 | heldout_2wikimultihopqa | -5.3 | [-10.6, +0.0] | 7 / 16 | 0.0931 |
| correct13 -> correct23 | heldout_hotpotqa | -2.1 | [-7.4, +2.6] | 10 / 14 | 0.541 |
| correct13 -> correct23 | heldout_musique | -4.4 | [-9.8, +1.0] | 11 / 20 | 0.15 |
| correct13 -> correct23 | heldout_strategyqa | -2.2 | [-5.4, +1.1] | 3 / 7 | 0.344 |
| correct13 -> correct23 | pooled | -3.5 | [-5.9, -1.1] | 31 / 57 | 0.00734 |
| correct13 -> mixmatch13 | heldout_2wikimultihopqa | -7.1 | [-12.3, -1.8] | 6 / 18 | 0.0227 |
| correct13 -> mixmatch13 | heldout_hotpotqa | -4.2 | [-9.0, +0.5] | 7 / 15 | 0.134 |
| correct13 -> mixmatch13 | heldout_musique | -7.4 | [-13.8, -1.0] | 16 / 31 | 0.04 |
| correct13 -> mixmatch13 | heldout_strategyqa | -3.8 | [-8.6, +0.5] | 6 / 13 | 0.167 |
| correct13 -> mixmatch13 | pooled | -5.6 | [-8.4, -2.9] | 35 / 77 | 9e-05 |
| correct13 -> mixmatch17 | heldout_2wikimultihopqa | -5.3 | [-10.6, +0.0] | 7 / 16 | 0.0931 |
| correct13 -> mixmatch17 | heldout_hotpotqa | -2.1 | [-7.4, +3.2] | 10 / 14 | 0.541 |
| correct13 -> mixmatch17 | heldout_musique | -5.9 | [-12.3, +0.5] | 15 / 27 | 0.0884 |
| correct13 -> mixmatch17 | heldout_strategyqa | -3.8 | [-8.1, +0.5] | 5 / 12 | 0.143 |
| correct13 -> mixmatch17 | pooled | -4.3 | [-7.0, -1.6] | 37 / 69 | 0.00244 |
| correct13 -> mixmatch23 | heldout_2wikimultihopqa | -2.9 | [-8.2, +2.4] | 9 / 14 | 0.405 |
| correct13 -> mixmatch23 | heldout_hotpotqa | -5.8 | [-10.6, -1.1] | 5 / 16 | 0.0266 |
| correct13 -> mixmatch23 | heldout_musique | -5.4 | [-11.3, +1.0] | 16 / 27 | 0.126 |
| correct13 -> mixmatch23 | heldout_strategyqa | -2.7 | [-7.0, +1.1] | 5 / 10 | 0.302 |
| correct13 -> mixmatch23 | pooled | -4.3 | [-7.0, -1.6] | 35 / 67 | 0.00199 |
| correct13 -> wrongonly | heldout_2wikimultihopqa | -8.2 | [-14.1, -2.4] | 7 / 21 | 0.0125 |
| correct13 -> wrongonly | heldout_hotpotqa | -9.0 | [-14.3, -3.7] | 5 / 22 | 0.00151 |
| correct13 -> wrongonly | heldout_musique | -9.4 | [-15.3, -3.5] | 10 / 29 | 0.00338 |
| correct13 -> wrongonly | heldout_strategyqa | -4.3 | [-9.2, +0.5] | 7 / 15 | 0.134 |
| correct13 -> wrongonly | pooled | -7.8 | [-10.6, -5.1] | 29 / 87 | 0 |
| correct17 -> correct23 | heldout_2wikimultihopqa | -4.1 | [-10.0, +1.8] | 9 / 16 | 0.23 |
| correct17 -> correct23 | heldout_hotpotqa | +0.0 | [-4.2, +4.2] | 8 / 8 | 1 |
| correct17 -> correct23 | heldout_musique | -0.5 | [-5.9, +4.9] | 16 / 17 | 1 |
| correct17 -> correct23 | heldout_strategyqa | -2.7 | [-7.0, +1.6] | 6 / 11 | 0.332 |
| correct17 -> correct23 | pooled | -1.7 | [-4.3, +0.7] | 39 / 52 | 0.208 |
| correct17 -> mixmatch13 | heldout_2wikimultihopqa | -5.9 | [-11.8, -0.6] | 7 / 17 | 0.0639 |
| correct17 -> mixmatch13 | heldout_hotpotqa | -2.1 | [-6.3, +2.1] | 6 / 10 | 0.454 |
| correct17 -> mixmatch13 | heldout_musique | -3.5 | [-9.8, +3.0] | 19 / 26 | 0.371 |
| correct17 -> mixmatch13 | heldout_strategyqa | -4.3 | [-9.2, +0.5] | 7 / 15 | 0.134 |
| correct17 -> mixmatch13 | pooled | -3.9 | [-6.6, -1.2] | 39 / 68 | 0.00652 |
| correct17 -> mixmatch17 | heldout_2wikimultihopqa | -4.1 | [-10.0, +2.4] | 11 / 18 | 0.265 |
| correct17 -> mixmatch17 | heldout_hotpotqa | +0.0 | [-4.2, +4.2] | 8 / 8 | 1 |
| correct17 -> mixmatch17 | heldout_musique | -2.0 | [-7.9, +3.9] | 17 / 21 | 0.627 |
| correct17 -> mixmatch17 | heldout_strategyqa | -4.3 | [-9.2, +0.5] | 6 / 14 | 0.115 |
| correct17 -> mixmatch17 | pooled | -2.5 | [-5.1, +0.1] | 42 / 61 | 0.0756 |
| correct17 -> mixmatch23 | heldout_2wikimultihopqa | -1.8 | [-8.2, +4.7] | 14 / 17 | 0.72 |
| correct17 -> mixmatch23 | heldout_hotpotqa | -3.7 | [-7.9, +0.5] | 5 / 12 | 0.143 |
| correct17 -> mixmatch23 | heldout_musique | -1.5 | [-7.4, +4.4] | 18 / 21 | 0.749 |
| correct17 -> mixmatch23 | heldout_strategyqa | -3.2 | [-7.6, +0.5] | 5 / 11 | 0.21 |
| correct17 -> mixmatch23 | pooled | -2.5 | [-5.2, +0.1] | 42 / 61 | 0.0756 |
| correct17 -> wrongonly | heldout_2wikimultihopqa | -7.1 | [-12.9, -1.2] | 8 / 20 | 0.0357 |
| correct17 -> wrongonly | heldout_hotpotqa | -6.9 | [-11.6, -2.1] | 5 / 18 | 0.0106 |
| correct17 -> wrongonly | heldout_musique | -5.4 | [-10.8, +0.0] | 11 / 22 | 0.0801 |
| correct17 -> wrongonly | heldout_strategyqa | -4.9 | [-10.3, +0.0] | 7 / 16 | 0.0931 |
| correct17 -> wrongonly | pooled | -6.0 | [-8.6, -3.4] | 31 / 76 | 1.6e-05 |
| correct23 -> mixmatch13 | heldout_2wikimultihopqa | -1.8 | [-7.6, +4.1] | 11 / 14 | 0.69 |
| correct23 -> mixmatch13 | heldout_hotpotqa | -2.1 | [-6.9, +3.2] | 10 / 14 | 0.541 |
| correct23 -> mixmatch13 | heldout_musique | -3.0 | [-9.4, +3.5] | 19 / 25 | 0.451 |
| correct23 -> mixmatch13 | heldout_strategyqa | -1.6 | [-5.9, +2.7] | 7 / 10 | 0.629 |
| correct23 -> mixmatch13 | pooled | -2.1 | [-5.0, +0.7] | 47 / 63 | 0.152 |
| correct23 -> mixmatch17 | heldout_2wikimultihopqa | +0.0 | [-5.9, +5.9] | 12 / 12 | 1 |
| correct23 -> mixmatch17 | heldout_hotpotqa | +0.0 | [-4.8, +4.8] | 11 / 11 | 1 |
| correct23 -> mixmatch17 | heldout_musique | -1.5 | [-7.4, +4.4] | 17 / 20 | 0.743 |
| correct23 -> mixmatch17 | heldout_strategyqa | -1.6 | [-6.5, +2.7] | 8 / 11 | 0.648 |
| correct23 -> mixmatch17 | pooled | -0.8 | [-3.4, +1.9] | 48 / 54 | 0.621 |
| correct23 -> mixmatch23 | heldout_2wikimultihopqa | +2.4 | [-3.5, +8.2] | 14 / 10 | 0.541 |
| correct23 -> mixmatch23 | heldout_hotpotqa | -3.7 | [-8.5, +1.1] | 8 / 15 | 0.21 |
| correct23 -> mixmatch23 | heldout_musique | -1.0 | [-6.4, +4.4] | 16 / 18 | 0.864 |
| correct23 -> mixmatch23 | heldout_strategyqa | -0.5 | [-4.9, +3.2] | 7 / 8 | 1 |
| correct23 -> mixmatch23 | pooled | -0.8 | [-3.4, +1.7] | 45 / 51 | 0.61 |
| correct23 -> wrongonly | heldout_2wikimultihopqa | -2.9 | [-8.8, +2.9] | 10 / 15 | 0.424 |
| correct23 -> wrongonly | heldout_hotpotqa | -6.9 | [-11.6, -2.1] | 5 / 18 | 0.0106 |
| correct23 -> wrongonly | heldout_musique | -4.9 | [-10.8, +1.0] | 15 / 25 | 0.154 |
| correct23 -> wrongonly | heldout_strategyqa | -2.2 | [-6.5, +2.2] | 7 / 11 | 0.481 |
| correct23 -> wrongonly | pooled | -4.3 | [-6.8, -1.6] | 37 / 69 | 0.00244 |
| mixmatch13 -> mixmatch17 | heldout_2wikimultihopqa | +1.8 | [-3.5, +7.6] | 13 / 10 | 0.678 |
| mixmatch13 -> mixmatch17 | heldout_hotpotqa | +2.1 | [-2.1, +6.3] | 10 / 6 | 0.454 |
| mixmatch13 -> mixmatch17 | heldout_musique | +1.5 | [-3.9, +7.4] | 19 / 16 | 0.736 |
| mixmatch13 -> mixmatch17 | heldout_strategyqa | +0.0 | [-3.8, +3.8] | 7 / 7 | 1 |
| mixmatch13 -> mixmatch17 | pooled | +1.3 | [-1.1, +3.8] | 49 / 39 | 0.337 |
| mixmatch13 -> mixmatch23 | heldout_2wikimultihopqa | +4.1 | [-1.8, +10.0] | 17 / 10 | 0.248 |
| mixmatch13 -> mixmatch23 | heldout_hotpotqa | -1.6 | [-5.8, +2.6] | 7 / 10 | 0.629 |
| mixmatch13 -> mixmatch23 | heldout_musique | +2.0 | [-3.5, +7.4] | 17 / 13 | 0.585 |
| mixmatch13 -> mixmatch23 | heldout_strategyqa | +1.1 | [-3.2, +5.4] | 9 / 7 | 0.804 |
| mixmatch13 -> mixmatch23 | pooled | +1.3 | [-1.1, +3.8] | 50 / 40 | 0.343 |
| mixmatch13 -> wrongonly | heldout_2wikimultihopqa | -1.2 | [-7.1, +4.7] | 12 / 14 | 0.845 |
| mixmatch13 -> wrongonly | heldout_hotpotqa | -4.8 | [-9.5, +0.0] | 6 / 15 | 0.0784 |
| mixmatch13 -> wrongonly | heldout_musique | -2.0 | [-7.4, +3.5] | 13 / 17 | 0.585 |
| mixmatch13 -> wrongonly | heldout_strategyqa | -0.5 | [-4.9, +3.8] | 7 / 8 | 1 |
| mixmatch13 -> wrongonly | pooled | -2.1 | [-4.7, +0.4] | 38 / 54 | 0.117 |
| mixmatch17 -> mixmatch23 | heldout_2wikimultihopqa | +2.4 | [-2.9, +7.6] | 12 / 8 | 0.503 |
| mixmatch17 -> mixmatch23 | heldout_hotpotqa | -3.7 | [-8.5, +1.1] | 8 / 15 | 0.21 |
| mixmatch17 -> mixmatch23 | heldout_musique | +0.5 | [-5.4, +6.4] | 18 / 17 | 1 |
| mixmatch17 -> mixmatch23 | heldout_strategyqa | +1.1 | [-2.7, +4.9] | 7 / 5 | 0.774 |
| mixmatch17 -> mixmatch23 | pooled | +0.0 | [-2.4, +2.4] | 45 / 45 | 1 |
| mixmatch17 -> wrongonly | heldout_2wikimultihopqa | -2.9 | [-8.2, +2.4] | 8 / 13 | 0.383 |
| mixmatch17 -> wrongonly | heldout_hotpotqa | -6.9 | [-12.2, -1.6] | 7 / 20 | 0.0192 |
| mixmatch17 -> wrongonly | heldout_musique | -3.5 | [-8.9, +1.5] | 11 / 18 | 0.265 |
| mixmatch17 -> wrongonly | heldout_strategyqa | -0.5 | [-4.9, +3.8] | 7 / 8 | 1 |
| mixmatch17 -> wrongonly | pooled | -3.5 | [-6.0, -0.9] | 33 / 59 | 0.00878 |
| mixmatch23 -> wrongonly | heldout_2wikimultihopqa | -5.3 | [-11.8, +0.6] | 10 / 19 | 0.136 |
| mixmatch23 -> wrongonly | heldout_hotpotqa | -3.2 | [-7.9, +1.6] | 8 / 14 | 0.286 |
| mixmatch23 -> wrongonly | heldout_musique | -3.9 | [-9.8, +2.0] | 14 / 22 | 0.243 |
| mixmatch23 -> wrongonly | heldout_strategyqa | -1.6 | [-5.9, +2.7] | 7 / 10 | 0.629 |
| mixmatch23 -> wrongonly | pooled | -3.5 | [-6.2, -0.8] | 39 / 65 | 0.0138 |
