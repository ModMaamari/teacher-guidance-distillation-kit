# Results

## Per arm and test set

| arm | test set | n | done | EM | F1 | cover | judge | doc recall | steps | vol. finish | tokens/ep | latency s | API $ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| base | heldout_2wikimultihopqa | 170 | yes | 0.018 | 0.120 | 0.306 | 0.353 | 0.810 | 2.98 | 0.02 | 5,182 | 25.5 | 0.0000 |
| base | heldout_hotpotqa | 189 | yes | 0.169 | 0.240 | 0.381 | 0.429 | 0.759 | 2.91 | 0.09 | 5,120 | 20.1 | 0.0000 |
| base | heldout_musique | 203 | yes | 0.020 | 0.084 | 0.153 | 0.172 | 0.597 | 3.00 | 0.00 | 5,052 | 17.5 | 0.0000 |
| base | heldout_strategyqa | 185 | yes | 0.000 | 0.011 | 0.097 | 0.151 | 0.815 | 2.98 | 0.02 | 4,923 | 17.0 | 0.0000 |
| selfguided13 | heldout_2wikimultihopqa | 170 | yes | 0.053 | 0.207 | 0.782 | 0.788 | 0.860 | 2.93 | 0.07 | 5,316 | 18.4 | 0.0000 |
| selfguided13 | heldout_hotpotqa | 189 | yes | 0.270 | 0.373 | 0.661 | 0.688 | 0.783 | 2.78 | 0.22 | 4,936 | 17.9 | 0.0000 |
| selfguided13 | heldout_musique | 203 | yes | 0.069 | 0.206 | 0.429 | 0.493 | 0.679 | 2.93 | 0.07 | 5,233 | 18.6 | 0.0000 |
| selfguided13 | heldout_strategyqa | 185 | yes | 0.000 | 0.034 | 0.686 | 0.724 | 0.834 | 2.95 | 0.05 | 5,161 | 19.9 | 0.0000 |
| selfguided17 | heldout_2wikimultihopqa | 170 | yes | 0.053 | 0.203 | 0.759 | 0.776 | 0.841 | 2.95 | 0.05 | 5,402 | 23.0 | 0.0000 |
| selfguided17 | heldout_hotpotqa | 189 | yes | 0.296 | 0.381 | 0.656 | 0.667 | 0.759 | 2.79 | 0.21 | 5,054 | 22.0 | 0.0000 |
| selfguided17 | heldout_musique | 203 | yes | 0.049 | 0.183 | 0.399 | 0.453 | 0.660 | 2.93 | 0.06 | 5,293 | 23.0 | 0.0000 |
| selfguided17 | heldout_strategyqa | 185 | yes | 0.000 | 0.036 | 0.681 | 0.730 | 0.833 | 2.91 | 0.09 | 5,113 | 24.7 | 0.0000 |
| selfguided23 | heldout_2wikimultihopqa | 170 | yes | 0.053 | 0.207 | 0.747 | 0.735 | 0.846 | 2.94 | 0.06 | 5,300 | 22.7 | 0.0000 |
| selfguided23 | heldout_hotpotqa | 189 | yes | 0.249 | 0.345 | 0.640 | 0.667 | 0.767 | 2.75 | 0.25 | 4,978 | 21.8 | 0.0000 |
| selfguided23 | heldout_musique | 203 | yes | 0.049 | 0.186 | 0.399 | 0.448 | 0.663 | 2.93 | 0.07 | 5,292 | 23.8 | 0.0000 |
| selfguided23 | heldout_strategyqa | 185 | yes | 0.000 | 0.034 | 0.670 | 0.703 | 0.818 | 2.89 | 0.11 | 5,050 | 24.4 | 0.0000 |
| teacherguided13 | heldout_2wikimultihopqa | 170 | yes | 0.429 | 0.543 | 0.765 | 0.765 | 0.854 | 2.93 | 0.07 | 5,655 | 24.3 | 0.0000 |
| teacherguided13 | heldout_hotpotqa | 189 | yes | 0.339 | 0.425 | 0.587 | 0.635 | 0.786 | 2.83 | 0.17 | 5,249 | 22.6 | 0.0000 |
| teacherguided13 | heldout_musique | 203 | yes | 0.163 | 0.287 | 0.350 | 0.389 | 0.663 | 2.99 | 0.01 | 5,253 | 20.8 | 0.0000 |
| teacherguided13 | heldout_strategyqa | 185 | yes | 0.508 | 0.529 | 0.724 | 0.730 | 0.826 | 2.92 | 0.08 | 5,214 | 23.2 | 0.0000 |
| teacherguided17 | heldout_2wikimultihopqa | 170 | yes | 0.300 | 0.444 | 0.776 | 0.782 | 0.871 | 2.93 | 0.07 | 5,680 | 26.4 | 0.0000 |
| teacherguided17 | heldout_hotpotqa | 189 | yes | 0.370 | 0.462 | 0.577 | 0.630 | 0.780 | 2.89 | 0.11 | 5,456 | 25.2 | 0.0000 |
| teacherguided17 | heldout_musique | 203 | yes | 0.172 | 0.271 | 0.345 | 0.369 | 0.688 | 2.96 | 0.04 | 5,247 | 24.2 | 0.0000 |
| teacherguided17 | heldout_strategyqa | 185 | yes | 0.454 | 0.480 | 0.714 | 0.719 | 0.817 | 2.90 | 0.09 | 5,179 | 24.8 | 0.0000 |
| teacherguided23 | heldout_2wikimultihopqa | 170 | yes | 0.359 | 0.486 | 0.741 | 0.765 | 0.840 | 2.92 | 0.08 | 5,716 | 25.8 | 0.0000 |
| teacherguided23 | heldout_hotpotqa | 189 | yes | 0.349 | 0.428 | 0.571 | 0.630 | 0.757 | 2.79 | 0.21 | 5,178 | 23.5 | 0.0000 |
| teacherguided23 | heldout_musique | 203 | yes | 0.172 | 0.273 | 0.315 | 0.369 | 0.680 | 2.96 | 0.04 | 5,206 | 22.4 | 0.0000 |
| teacherguided23 | heldout_strategyqa | 185 | yes | 0.508 | 0.529 | 0.730 | 0.751 | 0.828 | 2.86 | 0.14 | 5,108 | 23.1 | 0.0000 |
| unguided13 | heldout_2wikimultihopqa | 170 | yes | 0.047 | 0.198 | 0.747 | 0.765 | 0.828 | 2.97 | 0.03 | 5,053 | 38.9 | 0.0000 |
| unguided13 | heldout_hotpotqa | 189 | yes | 0.243 | 0.329 | 0.598 | 0.614 | 0.767 | 2.85 | 0.15 | 4,880 | 36.2 | 0.0000 |
| unguided13 | heldout_musique | 203 | yes | 0.044 | 0.173 | 0.374 | 0.409 | 0.605 | 2.97 | 0.03 | 4,750 | 36.1 | 0.0000 |
| unguided13 | heldout_strategyqa | 185 | yes | 0.000 | 0.036 | 0.670 | 0.735 | 0.812 | 2.95 | 0.05 | 4,782 | 40.1 | 0.0000 |
| unguided17 | heldout_2wikimultihopqa | 170 | yes | 0.053 | 0.204 | 0.753 | 0.759 | 0.822 | 2.96 | 0.04 | 5,040 | 19.5 | 0.0000 |
| unguided17 | heldout_hotpotqa | 189 | yes | 0.233 | 0.326 | 0.640 | 0.661 | 0.775 | 2.84 | 0.16 | 4,852 | 18.3 | 0.0000 |
| unguided17 | heldout_musique | 203 | yes | 0.035 | 0.162 | 0.389 | 0.453 | 0.629 | 2.96 | 0.04 | 4,749 | 18.6 | 0.0000 |
| unguided17 | heldout_strategyqa | 185 | yes | 0.000 | 0.037 | 0.670 | 0.746 | 0.810 | 2.94 | 0.05 | 4,796 | 20.5 | 0.0000 |
| unguided23 | heldout_2wikimultihopqa | 170 | yes | 0.059 | 0.209 | 0.759 | 0.741 | 0.819 | 2.98 | 0.02 | 5,062 | 19.3 | 0.0000 |
| unguided23 | heldout_hotpotqa | 189 | yes | 0.228 | 0.318 | 0.635 | 0.656 | 0.767 | 2.86 | 0.14 | 4,871 | 18.4 | 0.0000 |
| unguided23 | heldout_musique | 203 | yes | 0.035 | 0.165 | 0.369 | 0.424 | 0.619 | 2.97 | 0.03 | 4,784 | 18.4 | 0.0000 |
| unguided23 | heldout_strategyqa | 185 | yes | 0.000 | 0.035 | 0.649 | 0.714 | 0.809 | 2.97 | 0.03 | 4,892 | 21.1 | 0.0000 |

## Pooled per arm

| arm | test sets | n | EM | F1 | cover | judge | steps | tokens/ep | API $ |
|---|---|---|---|---|---|---|---|---|---|
| base | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.052 | 0.113 | 0.232 | 0.273 | 2.97 | 5,067 | 0.0000 |
| selfguided13 | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.099 | 0.206 | 0.632 | 0.667 | 2.90 | 5,159 | 0.0000 |
| selfguided17 | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.100 | 0.201 | 0.616 | 0.649 | 2.89 | 5,213 | 0.0000 |
| selfguided23 | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.088 | 0.193 | 0.606 | 0.632 | 2.87 | 5,155 | 0.0000 |
| teacherguided13 | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.353 | 0.440 | 0.597 | 0.621 | 2.92 | 5,334 | 0.0000 |
| teacherguided17 | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.321 | 0.411 | 0.593 | 0.616 | 2.92 | 5,382 | 0.0000 |
| teacherguided23 | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.343 | 0.424 | 0.580 | 0.620 | 2.88 | 5,291 | 0.0000 |
| unguided13 | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.084 | 0.184 | 0.589 | 0.623 | 2.93 | 4,860 | 0.0000 |
| unguided17 | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.080 | 0.182 | 0.605 | 0.648 | 2.92 | 4,853 | 0.0000 |
| unguided23 | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.080 | 0.181 | 0.594 | 0.626 | 2.94 | 4,896 | 0.0000 |

## Paired comparisons (judge-correct, b − a)

| a -> b | scope | Δ pts | 95% CI | b wins / a wins | McNemar p |
|---|---|---|---|---|---|
| base -> selfguided13 | heldout_2wikimultihopqa | +43.5 | [+35.3, +51.8] | 79 / 5 | 0 |
| base -> selfguided13 | heldout_hotpotqa | +25.9 | [+18.5, +33.3] | 57 / 8 | 0 |
| base -> selfguided13 | heldout_musique | +32.0 | [+24.6, +39.9] | 74 / 9 | 0 |
| base -> selfguided13 | heldout_strategyqa | +57.3 | [+49.7, +64.3] | 108 / 2 | 0 |
| base -> selfguided13 | pooled | +39.4 | [+35.5, +43.4] | 318 / 24 | 0 |
| base -> selfguided17 | heldout_2wikimultihopqa | +42.4 | [+34.1, +50.6] | 76 / 4 | 0 |
| base -> selfguided17 | heldout_hotpotqa | +23.8 | [+16.4, +31.2] | 53 / 8 | 0 |
| base -> selfguided17 | heldout_musique | +28.1 | [+20.2, +36.0] | 69 / 12 | 0 |
| base -> selfguided17 | heldout_strategyqa | +57.8 | [+50.8, +65.4] | 108 / 1 | 0 |
| base -> selfguided17 | pooled | +37.6 | [+33.6, +41.6] | 306 / 25 | 0 |
| base -> selfguided23 | heldout_2wikimultihopqa | +38.2 | [+30.0, +46.5] | 71 / 6 | 0 |
| base -> selfguided23 | heldout_hotpotqa | +23.8 | [+16.4, +31.2] | 54 / 9 | 0 |
| base -> selfguided23 | heldout_musique | +27.6 | [+20.2, +35.0] | 65 / 9 | 0 |
| base -> selfguided23 | heldout_strategyqa | +55.1 | [+47.6, +62.7] | 103 / 1 | 0 |
| base -> selfguided23 | pooled | +35.9 | [+32.0, +39.8] | 293 / 25 | 0 |
| base -> teacherguided13 | heldout_2wikimultihopqa | +41.2 | [+32.9, +48.8] | 73 / 3 | 0 |
| base -> teacherguided13 | heldout_hotpotqa | +20.6 | [+13.2, +28.0] | 51 / 12 | 1e-06 |
| base -> teacherguided13 | heldout_musique | +21.7 | [+14.3, +29.1] | 57 / 13 | 0 |
| base -> teacherguided13 | heldout_strategyqa | +57.8 | [+50.3, +65.4] | 108 / 1 | 0 |
| base -> teacherguided13 | pooled | +34.8 | [+30.8, +38.7] | 289 / 29 | 0 |
| base -> teacherguided17 | heldout_2wikimultihopqa | +42.9 | [+35.3, +50.6] | 75 / 2 | 0 |
| base -> teacherguided17 | heldout_hotpotqa | +20.1 | [+13.2, +27.5] | 47 / 9 | 0 |
| base -> teacherguided17 | heldout_musique | +19.7 | [+12.3, +27.1] | 54 / 14 | 1e-06 |
| base -> teacherguided17 | heldout_strategyqa | +56.8 | [+49.7, +63.8] | 105 / 0 | 0 |
| base -> teacherguided17 | pooled | +34.3 | [+30.4, +38.1] | 281 / 25 | 0 |
| base -> teacherguided23 | heldout_2wikimultihopqa | +41.2 | [+33.5, +48.8] | 72 / 2 | 0 |
| base -> teacherguided23 | heldout_hotpotqa | +20.1 | [+12.7, +27.5] | 49 / 11 | 1e-06 |
| base -> teacherguided23 | heldout_musique | +19.7 | [+12.3, +27.1] | 54 / 14 | 1e-06 |
| base -> teacherguided23 | heldout_strategyqa | +60.0 | [+53.0, +67.0] | 111 / 0 | 0 |
| base -> teacherguided23 | pooled | +34.7 | [+30.8, +38.6] | 286 / 27 | 0 |
| base -> unguided13 | heldout_2wikimultihopqa | +41.2 | [+32.9, +49.4] | 75 / 5 | 0 |
| base -> unguided13 | heldout_hotpotqa | +18.5 | [+11.1, +25.9] | 45 / 10 | 2e-06 |
| base -> unguided13 | heldout_musique | +23.6 | [+16.8, +30.5] | 55 / 7 | 0 |
| base -> unguided13 | heldout_strategyqa | +58.4 | [+51.3, +66.0] | 108 / 0 | 0 |
| base -> unguided13 | pooled | +34.9 | [+31.1, +38.8] | 283 / 22 | 0 |
| base -> unguided17 | heldout_2wikimultihopqa | +40.6 | [+32.4, +48.8] | 75 / 6 | 0 |
| base -> unguided17 | heldout_hotpotqa | +23.3 | [+16.4, +30.7] | 52 / 8 | 0 |
| base -> unguided17 | heldout_musique | +28.1 | [+21.2, +35.0] | 63 / 6 | 0 |
| base -> unguided17 | heldout_strategyqa | +59.5 | [+52.4, +66.5] | 111 / 1 | 0 |
| base -> unguided17 | pooled | +37.5 | [+33.6, +41.4] | 301 / 21 | 0 |
| base -> unguided23 | heldout_2wikimultihopqa | +38.8 | [+30.6, +47.1] | 71 / 5 | 0 |
| base -> unguided23 | heldout_hotpotqa | +22.8 | [+15.9, +29.6] | 49 / 6 | 0 |
| base -> unguided23 | heldout_musique | +25.1 | [+18.2, +32.0] | 58 / 7 | 0 |
| base -> unguided23 | heldout_strategyqa | +56.2 | [+48.6, +63.8] | 105 / 1 | 0 |
| base -> unguided23 | pooled | +35.3 | [+31.5, +39.2] | 283 / 19 | 0 |
| selfguided13 -> selfguided17 | heldout_2wikimultihopqa | -1.2 | [-6.5, +4.1] | 9 / 11 | 0.824 |
| selfguided13 -> selfguided17 | heldout_hotpotqa | -2.1 | [-6.9, +2.6] | 9 / 13 | 0.523 |
| selfguided13 -> selfguided17 | heldout_musique | -3.9 | [-9.8, +1.5] | 14 / 22 | 0.243 |
| selfguided13 -> selfguided17 | heldout_strategyqa | +0.5 | [-3.2, +4.3] | 7 / 6 | 1 |
| selfguided13 -> selfguided17 | pooled | -1.7 | [-4.3, +0.7] | 39 / 52 | 0.208 |
| selfguided13 -> selfguided23 | heldout_2wikimultihopqa | -5.3 | [-10.6, +0.0] | 7 / 16 | 0.0931 |
| selfguided13 -> selfguided23 | heldout_hotpotqa | -2.1 | [-7.4, +2.6] | 10 / 14 | 0.541 |
| selfguided13 -> selfguided23 | heldout_musique | -4.4 | [-9.8, +1.0] | 11 / 20 | 0.15 |
| selfguided13 -> selfguided23 | heldout_strategyqa | -2.2 | [-5.4, +1.1] | 3 / 7 | 0.344 |
| selfguided13 -> selfguided23 | pooled | -3.5 | [-5.9, -1.1] | 31 / 57 | 0.00734 |
| selfguided13 -> teacherguided13 | heldout_2wikimultihopqa | -2.4 | [-7.6, +2.9] | 9 / 13 | 0.523 |
| selfguided13 -> teacherguided13 | heldout_hotpotqa | -5.3 | [-11.6, +1.1] | 15 / 25 | 0.154 |
| selfguided13 -> teacherguided13 | heldout_musique | -10.3 | [-18.7, -2.5] | 26 / 47 | 0.0186 |
| selfguided13 -> teacherguided13 | heldout_strategyqa | +0.5 | [-5.4, +6.5] | 15 / 14 | 1 |
| selfguided13 -> teacherguided13 | pooled | -4.5 | [-7.9, -1.2] | 65 / 99 | 0.00976 |
| selfguided13 -> teacherguided17 | heldout_2wikimultihopqa | -0.6 | [-7.1, +5.9] | 15 / 16 | 1 |
| selfguided13 -> teacherguided17 | heldout_hotpotqa | -5.8 | [-11.6, +0.0] | 10 / 21 | 0.0708 |
| selfguided13 -> teacherguided17 | heldout_musique | -12.3 | [-19.7, -4.9] | 19 / 44 | 0.00223 |
| selfguided13 -> teacherguided17 | heldout_strategyqa | -0.5 | [-6.5, +5.4] | 14 / 15 | 1 |
| selfguided13 -> teacherguided17 | pooled | -5.1 | [-8.3, -1.9] | 58 / 96 | 0.00275 |
| selfguided13 -> teacherguided23 | heldout_2wikimultihopqa | -2.4 | [-8.8, +4.1] | 14 / 18 | 0.597 |
| selfguided13 -> teacherguided23 | heldout_hotpotqa | -5.8 | [-12.2, +0.5] | 13 / 24 | 0.0989 |
| selfguided13 -> teacherguided23 | heldout_musique | -12.3 | [-20.2, -4.9] | 19 / 44 | 0.00223 |
| selfguided13 -> teacherguided23 | heldout_strategyqa | +2.7 | [-3.8, +9.2] | 21 / 16 | 0.511 |
| selfguided13 -> teacherguided23 | pooled | -4.7 | [-8.2, -1.3] | 67 / 102 | 0.00872 |
| selfguided13 -> unguided13 | heldout_2wikimultihopqa | -2.4 | [-7.6, +2.9] | 9 / 13 | 0.523 |
| selfguided13 -> unguided13 | heldout_hotpotqa | -7.4 | [-13.2, -2.1] | 8 / 22 | 0.0161 |
| selfguided13 -> unguided13 | heldout_musique | -8.4 | [-14.8, -2.0] | 14 / 31 | 0.0161 |
| selfguided13 -> unguided13 | heldout_strategyqa | +1.1 | [-3.2, +5.4] | 10 / 8 | 0.815 |
| selfguided13 -> unguided13 | pooled | -4.4 | [-7.2, -1.7] | 41 / 74 | 0.00269 |
| selfguided13 -> unguided17 | heldout_2wikimultihopqa | -2.9 | [-8.8, +2.4] | 9 / 14 | 0.405 |
| selfguided13 -> unguided17 | heldout_hotpotqa | -2.6 | [-8.5, +3.2] | 13 / 18 | 0.473 |
| selfguided13 -> unguided17 | heldout_musique | -3.9 | [-11.3, +3.0] | 24 / 32 | 0.35 |
| selfguided13 -> unguided17 | heldout_strategyqa | +2.2 | [-2.2, +6.5] | 10 / 6 | 0.454 |
| selfguided13 -> unguided17 | pooled | -1.9 | [-4.8, +1.1] | 56 / 70 | 0.247 |
| selfguided13 -> unguided23 | heldout_2wikimultihopqa | -4.7 | [-10.0, +0.0] | 6 / 14 | 0.115 |
| selfguided13 -> unguided23 | heldout_hotpotqa | -3.2 | [-9.0, +2.6] | 13 / 19 | 0.377 |
| selfguided13 -> unguided23 | heldout_musique | -6.9 | [-13.8, +0.0] | 19 / 33 | 0.0704 |
| selfguided13 -> unguided23 | heldout_strategyqa | -1.1 | [-5.4, +3.2] | 7 / 9 | 0.804 |
| selfguided13 -> unguided23 | pooled | -4.0 | [-6.8, -1.2] | 45 / 75 | 0.00785 |
| selfguided17 -> selfguided23 | heldout_2wikimultihopqa | -4.1 | [-10.0, +1.8] | 9 / 16 | 0.23 |
| selfguided17 -> selfguided23 | heldout_hotpotqa | +0.0 | [-4.2, +4.2] | 8 / 8 | 1 |
| selfguided17 -> selfguided23 | heldout_musique | -0.5 | [-5.9, +4.9] | 16 / 17 | 1 |
| selfguided17 -> selfguided23 | heldout_strategyqa | -2.7 | [-7.0, +1.6] | 6 / 11 | 0.332 |
| selfguided17 -> selfguided23 | pooled | -1.7 | [-4.3, +0.7] | 39 / 52 | 0.208 |
| selfguided17 -> teacherguided13 | heldout_2wikimultihopqa | -1.2 | [-7.1, +4.1] | 11 / 13 | 0.839 |
| selfguided17 -> teacherguided13 | heldout_hotpotqa | -3.2 | [-8.5, +2.6] | 12 / 18 | 0.362 |
| selfguided17 -> teacherguided13 | heldout_musique | -6.4 | [-14.3, +1.0] | 25 / 38 | 0.13 |
| selfguided17 -> teacherguided13 | heldout_strategyqa | +0.0 | [-5.4, +5.4] | 13 / 13 | 1 |
| selfguided17 -> teacherguided13 | pooled | -2.8 | [-5.9, +0.4] | 61 / 82 | 0.0941 |
| selfguided17 -> teacherguided17 | heldout_2wikimultihopqa | +0.6 | [-6.5, +7.6] | 18 / 17 | 1 |
| selfguided17 -> teacherguided17 | heldout_hotpotqa | -3.7 | [-9.0, +1.6] | 10 / 17 | 0.248 |
| selfguided17 -> teacherguided17 | heldout_musique | -8.4 | [-15.8, -1.5] | 19 / 36 | 0.03 |
| selfguided17 -> teacherguided17 | heldout_strategyqa | -1.1 | [-6.5, +4.3] | 13 / 15 | 0.851 |
| selfguided17 -> teacherguided17 | pooled | -3.4 | [-6.6, -0.3] | 60 / 85 | 0.0459 |
| selfguided17 -> teacherguided23 | heldout_2wikimultihopqa | -1.2 | [-7.6, +5.3] | 14 / 16 | 0.856 |
| selfguided17 -> teacherguided23 | heldout_hotpotqa | -3.7 | [-9.5, +2.1] | 13 / 20 | 0.296 |
| selfguided17 -> teacherguided23 | heldout_musique | -8.4 | [-15.8, -1.5] | 19 / 36 | 0.03 |
| selfguided17 -> teacherguided23 | heldout_strategyqa | +2.2 | [-3.8, +8.6] | 19 / 15 | 0.608 |
| selfguided17 -> teacherguided23 | pooled | -2.9 | [-6.2, +0.3] | 65 / 87 | 0.0882 |
| selfguided17 -> unguided13 | heldout_2wikimultihopqa | -1.2 | [-7.1, +4.1] | 11 / 13 | 0.839 |
| selfguided17 -> unguided13 | heldout_hotpotqa | -5.3 | [-10.6, -0.5] | 7 / 17 | 0.0639 |
| selfguided17 -> unguided13 | heldout_musique | -4.4 | [-11.3, +2.0] | 20 / 29 | 0.253 |
| selfguided17 -> unguided13 | heldout_strategyqa | +0.5 | [-3.8, +5.4] | 10 / 9 | 1 |
| selfguided17 -> unguided13 | pooled | -2.7 | [-5.5, +0.1] | 48 / 68 | 0.0773 |
| selfguided17 -> unguided17 | heldout_2wikimultihopqa | -1.8 | [-7.1, +4.1] | 10 / 13 | 0.678 |
| selfguided17 -> unguided17 | heldout_hotpotqa | -0.5 | [-5.3, +4.2] | 11 / 12 | 1 |
| selfguided17 -> unguided17 | heldout_musique | +0.0 | [-6.4, +6.4] | 22 / 22 | 1 |
| selfguided17 -> unguided17 | heldout_strategyqa | +1.6 | [-2.7, +5.9] | 10 / 7 | 0.629 |
| selfguided17 -> unguided17 | pooled | -0.1 | [-2.8, +2.5] | 53 / 54 | 1 |
| selfguided17 -> unguided23 | heldout_2wikimultihopqa | -3.5 | [-9.4, +1.8] | 9 / 15 | 0.307 |
| selfguided17 -> unguided23 | heldout_hotpotqa | -1.1 | [-5.3, +3.2] | 8 / 10 | 0.815 |
| selfguided17 -> unguided23 | heldout_musique | -3.0 | [-9.4, +3.0] | 17 / 23 | 0.43 |
| selfguided17 -> unguided23 | heldout_strategyqa | -1.6 | [-5.9, +2.7] | 7 / 10 | 0.629 |
| selfguided17 -> unguided23 | pooled | -2.3 | [-4.8, +0.3] | 41 / 58 | 0.107 |
| selfguided23 -> teacherguided13 | heldout_2wikimultihopqa | +2.9 | [-3.5, +8.8] | 17 / 12 | 0.458 |
| selfguided23 -> teacherguided13 | heldout_hotpotqa | -3.2 | [-9.0, +2.6] | 12 / 18 | 0.362 |
| selfguided23 -> teacherguided13 | heldout_musique | -5.9 | [-13.8, +1.5] | 26 / 38 | 0.169 |
| selfguided23 -> teacherguided13 | heldout_strategyqa | +2.7 | [-2.7, +8.1] | 17 / 12 | 0.458 |
| selfguided23 -> teacherguided13 | pooled | -1.1 | [-4.2, +2.3] | 72 / 80 | 0.57 |
| selfguided23 -> teacherguided17 | heldout_2wikimultihopqa | +4.7 | [-1.8, +11.2] | 19 / 11 | 0.2 |
| selfguided23 -> teacherguided17 | heldout_hotpotqa | -3.7 | [-9.0, +1.6] | 10 / 17 | 0.248 |
| selfguided23 -> teacherguided17 | heldout_musique | -7.9 | [-15.3, -1.0] | 19 / 35 | 0.0402 |
| selfguided23 -> teacherguided17 | heldout_strategyqa | +1.6 | [-4.3, +7.6] | 17 / 14 | 0.72 |
| selfguided23 -> teacherguided17 | pooled | -1.6 | [-4.7, +1.6] | 65 / 77 | 0.356 |
| selfguided23 -> teacherguided23 | heldout_2wikimultihopqa | +2.9 | [-2.9, +8.8] | 16 / 11 | 0.442 |
| selfguided23 -> teacherguided23 | heldout_hotpotqa | -3.7 | [-10.1, +2.1] | 14 / 21 | 0.311 |
| selfguided23 -> teacherguided23 | heldout_musique | -7.9 | [-14.8, -1.0] | 18 / 34 | 0.0365 |
| selfguided23 -> teacherguided23 | heldout_strategyqa | +4.9 | [-1.1, +10.8] | 21 / 12 | 0.163 |
| selfguided23 -> teacherguided23 | pooled | -1.2 | [-4.4, +1.9] | 69 / 78 | 0.51 |
| selfguided23 -> unguided13 | heldout_2wikimultihopqa | +2.9 | [-1.8, +7.6] | 10 / 5 | 0.302 |
| selfguided23 -> unguided13 | heldout_hotpotqa | -5.3 | [-10.6, +0.0] | 8 / 18 | 0.0755 |
| selfguided23 -> unguided13 | heldout_musique | -3.9 | [-10.8, +3.0] | 22 / 30 | 0.332 |
| selfguided23 -> unguided13 | heldout_strategyqa | +3.2 | [-1.1, +7.6] | 12 / 6 | 0.238 |
| selfguided23 -> unguided13 | pooled | -0.9 | [-3.6, +1.9] | 52 / 59 | 0.569 |
| selfguided23 -> unguided17 | heldout_2wikimultihopqa | +2.4 | [-4.1, +8.2] | 16 / 12 | 0.572 |
| selfguided23 -> unguided17 | heldout_hotpotqa | -0.5 | [-5.3, +4.2] | 11 / 12 | 1 |
| selfguided23 -> unguided17 | heldout_musique | +0.5 | [-6.4, +6.9] | 24 / 23 | 1 |
| selfguided23 -> unguided17 | heldout_strategyqa | +4.3 | [+0.5, +8.6] | 12 / 4 | 0.0768 |
| selfguided23 -> unguided17 | pooled | +1.6 | [-1.2, +4.4] | 63 / 51 | 0.303 |
| selfguided23 -> unguided23 | heldout_2wikimultihopqa | +0.6 | [-5.3, +6.5] | 13 / 12 | 1 |
| selfguided23 -> unguided23 | heldout_hotpotqa | -1.1 | [-6.3, +3.7] | 11 / 13 | 0.839 |
| selfguided23 -> unguided23 | heldout_musique | -2.5 | [-8.9, +3.9] | 20 / 25 | 0.551 |
| selfguided23 -> unguided23 | heldout_strategyqa | +1.1 | [-3.2, +5.4] | 10 / 8 | 0.815 |
| selfguided23 -> unguided23 | pooled | -0.5 | [-3.2, +2.3] | 54 / 58 | 0.777 |
| teacherguided13 -> teacherguided17 | heldout_2wikimultihopqa | +1.8 | [-3.5, +7.1] | 12 / 9 | 0.664 |
| teacherguided13 -> teacherguided17 | heldout_hotpotqa | -0.5 | [-5.8, +4.8] | 12 / 13 | 1 |
| teacherguided13 -> teacherguided17 | heldout_musique | -2.0 | [-8.4, +4.4] | 22 / 26 | 0.665 |
| teacherguided13 -> teacherguided17 | heldout_strategyqa | -1.1 | [-5.9, +3.8] | 9 / 11 | 0.824 |
| teacherguided13 -> teacherguided17 | pooled | -0.5 | [-3.4, +2.3] | 55 / 59 | 0.779 |
| teacherguided13 -> teacherguided23 | heldout_2wikimultihopqa | +0.0 | [-5.3, +5.3] | 11 / 11 | 1 |
| teacherguided13 -> teacherguided23 | heldout_hotpotqa | -0.5 | [-6.3, +5.3] | 16 / 17 | 1 |
| teacherguided13 -> teacherguided23 | heldout_musique | -2.0 | [-7.9, +3.9] | 18 / 22 | 0.636 |
| teacherguided13 -> teacherguided23 | heldout_strategyqa | +2.2 | [-2.7, +7.0] | 13 / 9 | 0.523 |
| teacherguided13 -> teacherguided23 | pooled | -0.1 | [-2.9, +2.7] | 58 / 59 | 1 |
| teacherguided13 -> unguided13 | heldout_2wikimultihopqa | +0.0 | [-5.9, +5.9] | 13 / 13 | 1 |
| teacherguided13 -> unguided13 | heldout_hotpotqa | -2.1 | [-7.4, +2.6] | 10 / 14 | 0.541 |
| teacherguided13 -> unguided13 | heldout_musique | +2.0 | [-5.4, +9.8] | 33 / 29 | 0.704 |
| teacherguided13 -> unguided13 | heldout_strategyqa | +0.5 | [-4.9, +5.9] | 14 / 13 | 1 |
| teacherguided13 -> unguided13 | pooled | +0.1 | [-2.9, +3.2] | 70 / 69 | 1 |
| teacherguided13 -> unguided17 | heldout_2wikimultihopqa | -0.6 | [-7.1, +5.9] | 14 / 15 | 1 |
| teacherguided13 -> unguided17 | heldout_hotpotqa | +2.6 | [-2.1, +7.4] | 14 / 9 | 0.405 |
| teacherguided13 -> unguided17 | heldout_musique | +6.4 | [-1.0, +13.8] | 38 / 25 | 0.13 |
| teacherguided13 -> unguided17 | heldout_strategyqa | +1.6 | [-3.8, +7.0] | 14 / 11 | 0.69 |
| teacherguided13 -> unguided17 | pooled | +2.7 | [-0.4, +5.8] | 80 / 60 | 0.108 |
| teacherguided13 -> unguided23 | heldout_2wikimultihopqa | -2.4 | [-7.6, +2.9] | 9 / 13 | 0.523 |
| teacherguided13 -> unguided23 | heldout_hotpotqa | +2.1 | [-3.7, +7.9] | 17 / 13 | 0.585 |
| teacherguided13 -> unguided23 | heldout_musique | +3.5 | [-3.9, +10.8] | 33 / 26 | 0.435 |
| teacherguided13 -> unguided23 | heldout_strategyqa | -1.6 | [-7.6, +3.8] | 13 / 16 | 0.711 |
| teacherguided13 -> unguided23 | pooled | +0.5 | [-2.5, +3.6] | 72 / 68 | 0.8 |
| teacherguided17 -> teacherguided23 | heldout_2wikimultihopqa | -1.8 | [-7.1, +3.5] | 9 / 12 | 0.664 |
| teacherguided17 -> teacherguided23 | heldout_hotpotqa | +0.0 | [-5.3, +5.3] | 12 / 12 | 1 |
| teacherguided17 -> teacherguided23 | heldout_musique | +0.0 | [-6.4, +6.4] | 22 / 22 | 1 |
| teacherguided17 -> teacherguided23 | heldout_strategyqa | +3.2 | [-2.2, +8.6] | 15 / 9 | 0.307 |
| teacherguided17 -> teacherguided23 | pooled | +0.4 | [-2.4, +3.2] | 58 / 55 | 0.851 |
| teacherguided17 -> unguided13 | heldout_2wikimultihopqa | -1.8 | [-7.6, +4.7] | 13 / 16 | 0.711 |
| teacherguided17 -> unguided13 | heldout_hotpotqa | -1.6 | [-6.9, +3.2] | 10 / 13 | 0.678 |
| teacherguided17 -> unguided13 | heldout_musique | +3.9 | [-3.0, +11.3] | 32 / 24 | 0.35 |
| teacherguided17 -> unguided13 | heldout_strategyqa | +1.6 | [-4.3, +7.6] | 17 / 14 | 0.72 |
| teacherguided17 -> unguided13 | pooled | +0.7 | [-2.4, +3.8] | 72 / 67 | 0.735 |
| teacherguided17 -> unguided17 | heldout_2wikimultihopqa | -2.4 | [-8.8, +4.1] | 13 / 17 | 0.585 |
| teacherguided17 -> unguided17 | heldout_hotpotqa | +3.2 | [-1.6, +7.9] | 14 / 8 | 0.286 |
| teacherguided17 -> unguided17 | heldout_musique | +8.4 | [+1.5, +15.3] | 35 / 18 | 0.027 |
| teacherguided17 -> unguided17 | heldout_strategyqa | +2.7 | [-3.2, +8.6] | 19 / 14 | 0.487 |
| teacherguided17 -> unguided17 | pooled | +3.2 | [+0.1, +6.3] | 81 / 57 | 0.0498 |
| teacherguided17 -> unguided23 | heldout_2wikimultihopqa | -4.1 | [-10.0, +1.8] | 9 / 16 | 0.23 |
| teacherguided17 -> unguided23 | heldout_hotpotqa | +2.6 | [-2.6, +7.9] | 15 / 10 | 0.424 |
| teacherguided17 -> unguided23 | heldout_musique | +5.4 | [-2.0, +13.3] | 36 / 25 | 0.2 |
| teacherguided17 -> unguided23 | heldout_strategyqa | -0.5 | [-7.0, +5.9] | 17 / 18 | 1 |
| teacherguided17 -> unguided23 | pooled | +1.1 | [-2.0, +4.3] | 77 / 69 | 0.563 |
| teacherguided23 -> unguided13 | heldout_2wikimultihopqa | +0.0 | [-5.9, +5.9] | 13 / 13 | 1 |
| teacherguided23 -> unguided13 | heldout_hotpotqa | -1.6 | [-6.9, +4.2] | 13 / 16 | 0.711 |
| teacherguided23 -> unguided13 | heldout_musique | +3.9 | [-3.5, +11.3] | 32 / 24 | 0.35 |
| teacherguided23 -> unguided13 | heldout_strategyqa | -1.6 | [-7.0, +3.8] | 13 / 16 | 0.711 |
| teacherguided23 -> unguided13 | pooled | +0.3 | [-2.8, +3.4] | 71 / 69 | 0.933 |
| teacherguided23 -> unguided17 | heldout_2wikimultihopqa | -0.6 | [-6.5, +5.3] | 13 / 14 | 1 |
| teacherguided23 -> unguided17 | heldout_hotpotqa | +3.2 | [-3.2, +9.5] | 21 / 15 | 0.405 |
| teacherguided23 -> unguided17 | heldout_musique | +8.4 | [+1.5, +15.3] | 34 / 17 | 0.0241 |
| teacherguided23 -> unguided17 | heldout_strategyqa | -0.5 | [-6.5, +5.4] | 16 / 17 | 1 |
| teacherguided23 -> unguided17 | pooled | +2.8 | [-0.4, +6.0] | 84 / 63 | 0.0987 |
| teacherguided23 -> unguided23 | heldout_2wikimultihopqa | -2.4 | [-8.2, +3.5] | 11 / 15 | 0.557 |
| teacherguided23 -> unguided23 | heldout_hotpotqa | +2.6 | [-3.2, +8.5] | 19 / 14 | 0.487 |
| teacherguided23 -> unguided23 | heldout_musique | +5.4 | [-1.5, +12.3] | 31 / 20 | 0.161 |
| teacherguided23 -> unguided23 | heldout_strategyqa | -3.8 | [-10.3, +2.7] | 15 / 22 | 0.324 |
| teacherguided23 -> unguided23 | pooled | +0.7 | [-2.5, +3.9] | 76 / 71 | 0.742 |
| unguided13 -> unguided17 | heldout_2wikimultihopqa | -0.6 | [-5.9, +4.7] | 10 / 11 | 1 |
| unguided13 -> unguided17 | heldout_hotpotqa | +4.8 | [+0.0, +9.5] | 15 / 6 | 0.0784 |
| unguided13 -> unguided17 | heldout_musique | +4.4 | [-2.0, +10.8] | 26 / 17 | 0.222 |
| unguided13 -> unguided17 | heldout_strategyqa | +1.1 | [-2.7, +4.9] | 7 / 5 | 0.774 |
| unguided13 -> unguided17 | pooled | +2.5 | [+0.0, +5.1] | 58 / 39 | 0.0671 |
| unguided13 -> unguided23 | heldout_2wikimultihopqa | -2.4 | [-7.6, +2.9] | 10 / 14 | 0.541 |
| unguided13 -> unguided23 | heldout_hotpotqa | +4.2 | [-0.5, +9.5] | 16 / 8 | 0.152 |
| unguided13 -> unguided23 | heldout_musique | +1.5 | [-3.5, +6.4] | 14 / 11 | 0.69 |
| unguided13 -> unguided23 | heldout_strategyqa | -2.2 | [-5.9, +1.6] | 5 / 9 | 0.424 |
| unguided13 -> unguided23 | pooled | +0.4 | [-2.0, +2.8] | 45 / 42 | 0.83 |
| unguided17 -> unguided23 | heldout_2wikimultihopqa | -1.8 | [-7.1, +3.5] | 10 / 13 | 0.678 |
| unguided17 -> unguided23 | heldout_hotpotqa | -0.5 | [-5.3, +4.2] | 10 / 11 | 1 |
| unguided17 -> unguided23 | heldout_musique | -3.0 | [-8.4, +2.5] | 13 / 19 | 0.377 |
| unguided17 -> unguided23 | heldout_strategyqa | -3.2 | [-7.0, +0.5] | 3 / 9 | 0.146 |
| unguided17 -> unguided23 | pooled | -2.1 | [-4.5, +0.3] | 36 / 52 | 0.109 |
