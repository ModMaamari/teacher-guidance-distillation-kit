# Results

## Per arm and test set

| arm | test set | n | done | EM | F1 | cover | judge | doc recall | steps | vol. finish | tokens/ep | latency s | API $ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| base | heldout_2wikimultihopqa | 170 | yes | 0.018 | 0.120 | 0.306 | 0.353 | 0.810 | 2.98 | 0.02 | 5,182 | 25.5 | 0.0000 |
| base | heldout_hotpotqa | 189 | yes | 0.169 | 0.240 | 0.381 | 0.429 | 0.759 | 2.91 | 0.09 | 5,120 | 20.1 | 0.0000 |
| base | heldout_musique | 203 | yes | 0.020 | 0.084 | 0.153 | 0.172 | 0.597 | 3.00 | 0.00 | 5,052 | 17.5 | 0.0000 |
| base | heldout_strategyqa | 185 | yes | 0.000 | 0.011 | 0.097 | 0.151 | 0.815 | 2.98 | 0.02 | 4,923 | 17.0 | 0.0000 |
| self13 | heldout_2wikimultihopqa | 170 | yes | 0.053 | 0.207 | 0.782 | 0.788 | 0.860 | 2.93 | 0.07 | 5,316 | 18.4 | 0.0000 |
| self13 | heldout_hotpotqa | 189 | yes | 0.270 | 0.373 | 0.661 | 0.688 | 0.783 | 2.78 | 0.22 | 4,936 | 17.9 | 0.0000 |
| self13 | heldout_musique | 203 | yes | 0.069 | 0.206 | 0.429 | 0.493 | 0.679 | 2.93 | 0.07 | 5,233 | 18.6 | 0.0000 |
| self13 | heldout_strategyqa | 185 | yes | 0.000 | 0.034 | 0.686 | 0.724 | 0.834 | 2.95 | 0.05 | 5,161 | 19.9 | 0.0000 |
| self17 | heldout_2wikimultihopqa | 170 | yes | 0.053 | 0.203 | 0.759 | 0.776 | 0.841 | 2.95 | 0.05 | 5,402 | 23.0 | 0.0000 |
| self17 | heldout_hotpotqa | 189 | yes | 0.296 | 0.381 | 0.656 | 0.667 | 0.759 | 2.79 | 0.21 | 5,054 | 22.0 | 0.0000 |
| self17 | heldout_musique | 203 | yes | 0.049 | 0.183 | 0.399 | 0.453 | 0.660 | 2.93 | 0.06 | 5,293 | 23.0 | 0.0000 |
| self17 | heldout_strategyqa | 185 | yes | 0.000 | 0.036 | 0.681 | 0.730 | 0.833 | 2.91 | 0.09 | 5,113 | 24.7 | 0.0000 |
| self23 | heldout_2wikimultihopqa | 170 | yes | 0.053 | 0.207 | 0.747 | 0.735 | 0.846 | 2.94 | 0.06 | 5,300 | 22.7 | 0.0000 |
| self23 | heldout_hotpotqa | 189 | yes | 0.249 | 0.345 | 0.640 | 0.667 | 0.767 | 2.75 | 0.25 | 4,978 | 21.8 | 0.0000 |
| self23 | heldout_musique | 203 | yes | 0.049 | 0.186 | 0.399 | 0.448 | 0.663 | 2.93 | 0.07 | 5,292 | 23.8 | 0.0000 |
| self23 | heldout_strategyqa | 185 | yes | 0.000 | 0.034 | 0.670 | 0.703 | 0.818 | 2.89 | 0.11 | 5,050 | 24.4 | 0.0000 |
| tg13 | heldout_2wikimultihopqa | 170 | yes | 0.429 | 0.543 | 0.765 | 0.765 | 0.854 | 2.93 | 0.07 | 5,655 | 24.3 | 0.0000 |
| tg13 | heldout_hotpotqa | 189 | yes | 0.339 | 0.425 | 0.587 | 0.635 | 0.786 | 2.83 | 0.17 | 5,249 | 22.6 | 0.0000 |
| tg13 | heldout_musique | 203 | yes | 0.163 | 0.287 | 0.350 | 0.389 | 0.663 | 2.99 | 0.01 | 5,253 | 20.8 | 0.0000 |
| tg13 | heldout_strategyqa | 185 | yes | 0.508 | 0.529 | 0.724 | 0.730 | 0.826 | 2.92 | 0.08 | 5,214 | 23.2 | 0.0000 |
| tg17 | heldout_2wikimultihopqa | 170 | yes | 0.300 | 0.444 | 0.776 | 0.782 | 0.871 | 2.93 | 0.07 | 5,680 | 26.4 | 0.0000 |
| tg17 | heldout_hotpotqa | 189 | yes | 0.370 | 0.462 | 0.577 | 0.630 | 0.780 | 2.89 | 0.11 | 5,456 | 25.2 | 0.0000 |
| tg17 | heldout_musique | 203 | yes | 0.172 | 0.271 | 0.345 | 0.369 | 0.688 | 2.96 | 0.04 | 5,247 | 24.2 | 0.0000 |
| tg17 | heldout_strategyqa | 185 | yes | 0.454 | 0.480 | 0.714 | 0.719 | 0.817 | 2.90 | 0.09 | 5,179 | 24.8 | 0.0000 |
| tg23 | heldout_2wikimultihopqa | 170 | yes | 0.359 | 0.486 | 0.741 | 0.765 | 0.840 | 2.92 | 0.08 | 5,716 | 25.8 | 0.0000 |
| tg23 | heldout_hotpotqa | 189 | yes | 0.349 | 0.428 | 0.571 | 0.630 | 0.757 | 2.79 | 0.21 | 5,178 | 23.5 | 0.0000 |
| tg23 | heldout_musique | 203 | yes | 0.172 | 0.273 | 0.315 | 0.369 | 0.680 | 2.96 | 0.04 | 5,206 | 22.4 | 0.0000 |
| tg23 | heldout_strategyqa | 185 | yes | 0.508 | 0.529 | 0.730 | 0.751 | 0.828 | 2.86 | 0.14 | 5,108 | 23.1 | 0.0000 |

## Pooled per arm

| arm | test sets | n | EM | F1 | cover | judge | steps | tokens/ep | API $ |
|---|---|---|---|---|---|---|---|---|---|
| base | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.052 | 0.113 | 0.232 | 0.273 | 2.97 | 5,067 | 0.0000 |
| self13 | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.099 | 0.206 | 0.632 | 0.667 | 2.90 | 5,159 | 0.0000 |
| self17 | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.100 | 0.201 | 0.616 | 0.649 | 2.89 | 5,213 | 0.0000 |
| self23 | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.088 | 0.193 | 0.606 | 0.632 | 2.87 | 5,155 | 0.0000 |
| tg13 | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.353 | 0.440 | 0.597 | 0.621 | 2.92 | 5,334 | 0.0000 |
| tg17 | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.321 | 0.411 | 0.593 | 0.616 | 2.92 | 5,382 | 0.0000 |
| tg23 | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.343 | 0.424 | 0.580 | 0.620 | 2.88 | 5,291 | 0.0000 |

## Paired comparisons (judge-correct, b − a)

| a -> b | scope | Δ pts | 95% CI | b wins / a wins | McNemar p |
|---|---|---|---|---|---|
| base -> self13 | heldout_2wikimultihopqa | +43.5 | [+35.3, +51.8] | 79 / 5 | 0 |
| base -> self13 | heldout_hotpotqa | +25.9 | [+18.5, +33.3] | 57 / 8 | 0 |
| base -> self13 | heldout_musique | +32.0 | [+24.6, +39.9] | 74 / 9 | 0 |
| base -> self13 | heldout_strategyqa | +57.3 | [+49.7, +64.3] | 108 / 2 | 0 |
| base -> self13 | pooled | +39.4 | [+35.5, +43.4] | 318 / 24 | 0 |
| base -> self17 | heldout_2wikimultihopqa | +42.4 | [+34.1, +50.6] | 76 / 4 | 0 |
| base -> self17 | heldout_hotpotqa | +23.8 | [+16.4, +31.2] | 53 / 8 | 0 |
| base -> self17 | heldout_musique | +28.1 | [+20.2, +36.0] | 69 / 12 | 0 |
| base -> self17 | heldout_strategyqa | +57.8 | [+50.8, +65.4] | 108 / 1 | 0 |
| base -> self17 | pooled | +37.6 | [+33.6, +41.6] | 306 / 25 | 0 |
| base -> self23 | heldout_2wikimultihopqa | +38.2 | [+30.0, +46.5] | 71 / 6 | 0 |
| base -> self23 | heldout_hotpotqa | +23.8 | [+16.4, +31.2] | 54 / 9 | 0 |
| base -> self23 | heldout_musique | +27.6 | [+20.2, +35.0] | 65 / 9 | 0 |
| base -> self23 | heldout_strategyqa | +55.1 | [+47.6, +62.7] | 103 / 1 | 0 |
| base -> self23 | pooled | +35.9 | [+32.0, +39.8] | 293 / 25 | 0 |
| base -> tg13 | heldout_2wikimultihopqa | +41.2 | [+32.9, +48.8] | 73 / 3 | 0 |
| base -> tg13 | heldout_hotpotqa | +20.6 | [+13.2, +28.0] | 51 / 12 | 1e-06 |
| base -> tg13 | heldout_musique | +21.7 | [+14.3, +29.1] | 57 / 13 | 0 |
| base -> tg13 | heldout_strategyqa | +57.8 | [+50.3, +65.4] | 108 / 1 | 0 |
| base -> tg13 | pooled | +34.8 | [+30.8, +38.7] | 289 / 29 | 0 |
| base -> tg17 | heldout_2wikimultihopqa | +42.9 | [+35.3, +50.6] | 75 / 2 | 0 |
| base -> tg17 | heldout_hotpotqa | +20.1 | [+13.2, +27.5] | 47 / 9 | 0 |
| base -> tg17 | heldout_musique | +19.7 | [+12.3, +27.1] | 54 / 14 | 1e-06 |
| base -> tg17 | heldout_strategyqa | +56.8 | [+49.7, +63.8] | 105 / 0 | 0 |
| base -> tg17 | pooled | +34.3 | [+30.4, +38.1] | 281 / 25 | 0 |
| base -> tg23 | heldout_2wikimultihopqa | +41.2 | [+33.5, +48.8] | 72 / 2 | 0 |
| base -> tg23 | heldout_hotpotqa | +20.1 | [+12.7, +27.5] | 49 / 11 | 1e-06 |
| base -> tg23 | heldout_musique | +19.7 | [+12.3, +27.1] | 54 / 14 | 1e-06 |
| base -> tg23 | heldout_strategyqa | +60.0 | [+53.0, +67.0] | 111 / 0 | 0 |
| base -> tg23 | pooled | +34.7 | [+30.8, +38.6] | 286 / 27 | 0 |
| self13 -> self17 | heldout_2wikimultihopqa | -1.2 | [-6.5, +4.1] | 9 / 11 | 0.824 |
| self13 -> self17 | heldout_hotpotqa | -2.1 | [-6.9, +2.6] | 9 / 13 | 0.523 |
| self13 -> self17 | heldout_musique | -3.9 | [-9.8, +1.5] | 14 / 22 | 0.243 |
| self13 -> self17 | heldout_strategyqa | +0.5 | [-3.2, +4.3] | 7 / 6 | 1 |
| self13 -> self17 | pooled | -1.7 | [-4.3, +0.7] | 39 / 52 | 0.208 |
| self13 -> self23 | heldout_2wikimultihopqa | -5.3 | [-10.6, +0.0] | 7 / 16 | 0.0931 |
| self13 -> self23 | heldout_hotpotqa | -2.1 | [-7.4, +2.6] | 10 / 14 | 0.541 |
| self13 -> self23 | heldout_musique | -4.4 | [-9.8, +1.0] | 11 / 20 | 0.15 |
| self13 -> self23 | heldout_strategyqa | -2.2 | [-5.4, +1.1] | 3 / 7 | 0.344 |
| self13 -> self23 | pooled | -3.5 | [-5.9, -1.1] | 31 / 57 | 0.00734 |
| self13 -> tg13 | heldout_2wikimultihopqa | -2.4 | [-7.6, +2.9] | 9 / 13 | 0.523 |
| self13 -> tg13 | heldout_hotpotqa | -5.3 | [-11.6, +1.1] | 15 / 25 | 0.154 |
| self13 -> tg13 | heldout_musique | -10.3 | [-18.7, -2.5] | 26 / 47 | 0.0186 |
| self13 -> tg13 | heldout_strategyqa | +0.5 | [-5.4, +6.5] | 15 / 14 | 1 |
| self13 -> tg13 | pooled | -4.5 | [-7.9, -1.2] | 65 / 99 | 0.00976 |
| self13 -> tg17 | heldout_2wikimultihopqa | -0.6 | [-7.1, +5.9] | 15 / 16 | 1 |
| self13 -> tg17 | heldout_hotpotqa | -5.8 | [-11.6, +0.0] | 10 / 21 | 0.0708 |
| self13 -> tg17 | heldout_musique | -12.3 | [-19.7, -4.9] | 19 / 44 | 0.00223 |
| self13 -> tg17 | heldout_strategyqa | -0.5 | [-6.5, +5.4] | 14 / 15 | 1 |
| self13 -> tg17 | pooled | -5.1 | [-8.3, -1.9] | 58 / 96 | 0.00275 |
| self13 -> tg23 | heldout_2wikimultihopqa | -2.4 | [-8.8, +4.1] | 14 / 18 | 0.597 |
| self13 -> tg23 | heldout_hotpotqa | -5.8 | [-12.2, +0.5] | 13 / 24 | 0.0989 |
| self13 -> tg23 | heldout_musique | -12.3 | [-20.2, -4.9] | 19 / 44 | 0.00223 |
| self13 -> tg23 | heldout_strategyqa | +2.7 | [-3.8, +9.2] | 21 / 16 | 0.511 |
| self13 -> tg23 | pooled | -4.7 | [-8.2, -1.3] | 67 / 102 | 0.00872 |
| self17 -> self23 | heldout_2wikimultihopqa | -4.1 | [-10.0, +1.8] | 9 / 16 | 0.23 |
| self17 -> self23 | heldout_hotpotqa | +0.0 | [-4.2, +4.2] | 8 / 8 | 1 |
| self17 -> self23 | heldout_musique | -0.5 | [-5.9, +4.9] | 16 / 17 | 1 |
| self17 -> self23 | heldout_strategyqa | -2.7 | [-7.0, +1.6] | 6 / 11 | 0.332 |
| self17 -> self23 | pooled | -1.7 | [-4.3, +0.7] | 39 / 52 | 0.208 |
| self17 -> tg13 | heldout_2wikimultihopqa | -1.2 | [-7.1, +4.1] | 11 / 13 | 0.839 |
| self17 -> tg13 | heldout_hotpotqa | -3.2 | [-8.5, +2.6] | 12 / 18 | 0.362 |
| self17 -> tg13 | heldout_musique | -6.4 | [-14.3, +1.0] | 25 / 38 | 0.13 |
| self17 -> tg13 | heldout_strategyqa | +0.0 | [-5.4, +5.4] | 13 / 13 | 1 |
| self17 -> tg13 | pooled | -2.8 | [-5.9, +0.4] | 61 / 82 | 0.0941 |
| self17 -> tg17 | heldout_2wikimultihopqa | +0.6 | [-6.5, +7.6] | 18 / 17 | 1 |
| self17 -> tg17 | heldout_hotpotqa | -3.7 | [-9.0, +1.6] | 10 / 17 | 0.248 |
| self17 -> tg17 | heldout_musique | -8.4 | [-15.8, -1.5] | 19 / 36 | 0.03 |
| self17 -> tg17 | heldout_strategyqa | -1.1 | [-6.5, +4.3] | 13 / 15 | 0.851 |
| self17 -> tg17 | pooled | -3.4 | [-6.6, -0.3] | 60 / 85 | 0.0459 |
| self17 -> tg23 | heldout_2wikimultihopqa | -1.2 | [-7.6, +5.3] | 14 / 16 | 0.856 |
| self17 -> tg23 | heldout_hotpotqa | -3.7 | [-9.5, +2.1] | 13 / 20 | 0.296 |
| self17 -> tg23 | heldout_musique | -8.4 | [-15.8, -1.5] | 19 / 36 | 0.03 |
| self17 -> tg23 | heldout_strategyqa | +2.2 | [-3.8, +8.6] | 19 / 15 | 0.608 |
| self17 -> tg23 | pooled | -2.9 | [-6.2, +0.3] | 65 / 87 | 0.0882 |
| self23 -> tg13 | heldout_2wikimultihopqa | +2.9 | [-3.5, +8.8] | 17 / 12 | 0.458 |
| self23 -> tg13 | heldout_hotpotqa | -3.2 | [-9.0, +2.6] | 12 / 18 | 0.362 |
| self23 -> tg13 | heldout_musique | -5.9 | [-13.8, +1.5] | 26 / 38 | 0.169 |
| self23 -> tg13 | heldout_strategyqa | +2.7 | [-2.7, +8.1] | 17 / 12 | 0.458 |
| self23 -> tg13 | pooled | -1.1 | [-4.2, +2.3] | 72 / 80 | 0.57 |
| self23 -> tg17 | heldout_2wikimultihopqa | +4.7 | [-1.8, +11.2] | 19 / 11 | 0.2 |
| self23 -> tg17 | heldout_hotpotqa | -3.7 | [-9.0, +1.6] | 10 / 17 | 0.248 |
| self23 -> tg17 | heldout_musique | -7.9 | [-15.3, -1.0] | 19 / 35 | 0.0402 |
| self23 -> tg17 | heldout_strategyqa | +1.6 | [-4.3, +7.6] | 17 / 14 | 0.72 |
| self23 -> tg17 | pooled | -1.6 | [-4.7, +1.6] | 65 / 77 | 0.356 |
| self23 -> tg23 | heldout_2wikimultihopqa | +2.9 | [-2.9, +8.8] | 16 / 11 | 0.442 |
| self23 -> tg23 | heldout_hotpotqa | -3.7 | [-10.1, +2.1] | 14 / 21 | 0.311 |
| self23 -> tg23 | heldout_musique | -7.9 | [-14.8, -1.0] | 18 / 34 | 0.0365 |
| self23 -> tg23 | heldout_strategyqa | +4.9 | [-1.1, +10.8] | 21 / 12 | 0.163 |
| self23 -> tg23 | pooled | -1.2 | [-4.4, +1.9] | 69 / 78 | 0.51 |
| tg13 -> tg17 | heldout_2wikimultihopqa | +1.8 | [-3.5, +7.1] | 12 / 9 | 0.664 |
| tg13 -> tg17 | heldout_hotpotqa | -0.5 | [-5.8, +4.8] | 12 / 13 | 1 |
| tg13 -> tg17 | heldout_musique | -2.0 | [-8.4, +4.4] | 22 / 26 | 0.665 |
| tg13 -> tg17 | heldout_strategyqa | -1.1 | [-5.9, +3.8] | 9 / 11 | 0.824 |
| tg13 -> tg17 | pooled | -0.5 | [-3.4, +2.3] | 55 / 59 | 0.779 |
| tg13 -> tg23 | heldout_2wikimultihopqa | +0.0 | [-5.3, +5.3] | 11 / 11 | 1 |
| tg13 -> tg23 | heldout_hotpotqa | -0.5 | [-6.3, +5.3] | 16 / 17 | 1 |
| tg13 -> tg23 | heldout_musique | -2.0 | [-7.9, +3.9] | 18 / 22 | 0.636 |
| tg13 -> tg23 | heldout_strategyqa | +2.2 | [-2.7, +7.0] | 13 / 9 | 0.523 |
| tg13 -> tg23 | pooled | -0.1 | [-2.9, +2.7] | 58 / 59 | 1 |
| tg17 -> tg23 | heldout_2wikimultihopqa | -1.8 | [-7.1, +3.5] | 9 / 12 | 0.664 |
| tg17 -> tg23 | heldout_hotpotqa | +0.0 | [-5.3, +5.3] | 12 / 12 | 1 |
| tg17 -> tg23 | heldout_musique | +0.0 | [-6.4, +6.4] | 22 / 22 | 1 |
| tg17 -> tg23 | heldout_strategyqa | +3.2 | [-2.2, +8.6] | 15 / 9 | 0.307 |
| tg17 -> tg23 | pooled | +0.4 | [-2.4, +3.2] | 58 / 55 | 0.851 |
