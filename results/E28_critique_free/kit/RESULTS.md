# Results

## Per arm and test set

| arm | test set | n | done | EM | F1 | cover | judge | doc recall | steps | vol. finish | tokens/ep | latency s | API $ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| base | heldout_2wikimultihopqa | 170 | yes | 0.018 | 0.120 | 0.306 | 0.353 | 0.810 | 2.98 | 0.02 | 5,182 | 25.5 | 0.0000 |
| base | heldout_hotpotqa | 189 | yes | 0.169 | 0.240 | 0.381 | 0.429 | 0.759 | 2.91 | 0.09 | 5,120 | 20.1 | 0.0000 |
| base | heldout_musique | 203 | yes | 0.020 | 0.084 | 0.153 | 0.172 | 0.597 | 3.00 | 0.00 | 5,052 | 17.5 | 0.0000 |
| base | heldout_strategyqa | 185 | yes | 0.000 | 0.011 | 0.097 | 0.151 | 0.815 | 2.98 | 0.02 | 4,923 | 17.0 | 0.0000 |
| nocrit13 | heldout_2wikimultihopqa | 170 | yes | 0.053 | 0.217 | 0.765 | 0.765 | 0.852 | 2.94 | 0.06 | 5,021 | 16.2 | 0.0000 |
| nocrit13 | heldout_hotpotqa | 189 | yes | 0.275 | 0.366 | 0.651 | 0.682 | 0.775 | 2.77 | 0.23 | 4,639 | 16.1 | 0.0000 |
| nocrit13 | heldout_musique | 203 | yes | 0.049 | 0.187 | 0.384 | 0.443 | 0.648 | 2.92 | 0.08 | 4,989 | 16.8 | 0.0000 |
| nocrit13 | heldout_strategyqa | 185 | yes | 0.000 | 0.035 | 0.692 | 0.730 | 0.818 | 2.91 | 0.09 | 4,880 | 17.7 | 0.0000 |
| nocrit17 | heldout_2wikimultihopqa | 170 | yes | 0.059 | 0.208 | 0.765 | 0.771 | 0.846 | 2.95 | 0.05 | 5,087 | 16.6 | 0.0000 |
| nocrit17 | heldout_hotpotqa | 189 | yes | 0.254 | 0.347 | 0.619 | 0.635 | 0.770 | 2.78 | 0.22 | 4,770 | 16.4 | 0.0000 |
| nocrit17 | heldout_musique | 203 | yes | 0.049 | 0.164 | 0.384 | 0.419 | 0.642 | 2.91 | 0.09 | 5,024 | 17.6 | 0.0000 |
| nocrit17 | heldout_strategyqa | 185 | yes | 0.000 | 0.037 | 0.692 | 0.724 | 0.830 | 2.91 | 0.09 | 4,886 | 17.3 | 0.0000 |
| nocrit23 | heldout_2wikimultihopqa | 170 | yes | 0.035 | 0.192 | 0.747 | 0.741 | 0.828 | 2.98 | 0.02 | 5,177 | 20.6 | 0.0000 |
| nocrit23 | heldout_hotpotqa | 189 | yes | 0.275 | 0.362 | 0.651 | 0.672 | 0.783 | 2.75 | 0.25 | 4,671 | 20.0 | 0.0000 |
| nocrit23 | heldout_musique | 203 | yes | 0.103 | 0.231 | 0.429 | 0.483 | 0.667 | 2.95 | 0.05 | 5,161 | 21.4 | 0.0000 |
| nocrit23 | heldout_strategyqa | 185 | yes | 0.000 | 0.037 | 0.692 | 0.730 | 0.824 | 2.91 | 0.09 | 4,842 | 20.9 | 0.0000 |
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
| nocrit13 | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.095 | 0.201 | 0.615 | 0.648 | 2.88 | 4,881 | 0.0000 |
| nocrit17 | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.091 | 0.189 | 0.606 | 0.629 | 2.89 | 4,940 | 0.0000 |
| nocrit23 | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.106 | 0.207 | 0.623 | 0.651 | 2.89 | 4,962 | 0.0000 |
| selfguided13 | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.099 | 0.206 | 0.632 | 0.667 | 2.90 | 5,159 | 0.0000 |
| selfguided17 | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.100 | 0.201 | 0.616 | 0.649 | 2.89 | 5,213 | 0.0000 |
| selfguided23 | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.088 | 0.193 | 0.606 | 0.632 | 2.87 | 5,155 | 0.0000 |
| unguided13 | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.084 | 0.184 | 0.589 | 0.623 | 2.93 | 4,860 | 0.0000 |
| unguided17 | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.080 | 0.182 | 0.605 | 0.648 | 2.92 | 4,853 | 0.0000 |
| unguided23 | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.080 | 0.181 | 0.594 | 0.626 | 2.94 | 4,896 | 0.0000 |

## Paired comparisons (judge-correct, b − a)

| a -> b | scope | Δ pts | 95% CI | b wins / a wins | McNemar p |
|---|---|---|---|---|---|
| base -> nocrit13 | heldout_2wikimultihopqa | +41.2 | [+32.9, +49.4] | 75 / 5 | 0 |
| base -> nocrit13 | heldout_hotpotqa | +25.4 | [+18.0, +32.8] | 56 / 8 | 0 |
| base -> nocrit13 | heldout_musique | +27.1 | [+19.7, +34.5] | 66 / 11 | 0 |
| base -> nocrit13 | heldout_strategyqa | +57.8 | [+50.3, +64.9] | 108 / 1 | 0 |
| base -> nocrit13 | pooled | +37.5 | [+33.5, +41.4] | 305 / 25 | 0 |
| base -> nocrit17 | heldout_2wikimultihopqa | +41.8 | [+33.5, +50.0] | 75 / 4 | 0 |
| base -> nocrit17 | heldout_hotpotqa | +20.6 | [+13.2, +28.0] | 50 / 11 | 0 |
| base -> nocrit17 | heldout_musique | +24.6 | [+17.2, +32.0] | 62 / 12 | 0 |
| base -> nocrit17 | heldout_strategyqa | +57.3 | [+49.7, +64.9] | 108 / 2 | 0 |
| base -> nocrit17 | pooled | +35.6 | [+31.6, +39.5] | 295 / 29 | 0 |
| base -> nocrit23 | heldout_2wikimultihopqa | +38.8 | [+30.6, +47.1] | 71 / 5 | 0 |
| base -> nocrit23 | heldout_hotpotqa | +24.3 | [+16.4, +31.8] | 56 / 10 | 0 |
| base -> nocrit23 | heldout_musique | +31.0 | [+23.6, +38.4] | 71 / 8 | 0 |
| base -> nocrit23 | heldout_strategyqa | +57.8 | [+50.8, +65.4] | 108 / 1 | 0 |
| base -> nocrit23 | pooled | +37.8 | [+33.9, +41.6] | 306 / 24 | 0 |
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
| nocrit13 -> nocrit17 | heldout_2wikimultihopqa | +0.6 | [-4.1, +5.9] | 10 / 9 | 1 |
| nocrit13 -> nocrit17 | heldout_hotpotqa | -4.8 | [-9.5, +0.0] | 7 / 16 | 0.0931 |
| nocrit13 -> nocrit17 | heldout_musique | -2.5 | [-8.4, +3.9] | 18 / 23 | 0.533 |
| nocrit13 -> nocrit17 | heldout_strategyqa | -0.5 | [-5.4, +4.3] | 9 / 10 | 1 |
| nocrit13 -> nocrit17 | pooled | -1.9 | [-4.5, +0.7] | 44 / 58 | 0.198 |
| nocrit13 -> nocrit23 | heldout_2wikimultihopqa | -2.4 | [-7.6, +2.9] | 9 / 13 | 0.523 |
| nocrit13 -> nocrit23 | heldout_hotpotqa | -1.1 | [-4.8, +2.6] | 5 / 7 | 0.774 |
| nocrit13 -> nocrit23 | heldout_musique | +3.9 | [-2.0, +9.8] | 23 / 15 | 0.256 |
| nocrit13 -> nocrit23 | heldout_strategyqa | +0.0 | [-4.3, +3.8] | 7 / 7 | 1 |
| nocrit13 -> nocrit23 | pooled | +0.3 | [-2.1, +2.7] | 44 / 42 | 0.914 |
| nocrit13 -> selfguided13 | heldout_2wikimultihopqa | +2.4 | [-2.4, +7.1] | 10 / 6 | 0.454 |
| nocrit13 -> selfguided13 | heldout_hotpotqa | +0.5 | [-4.2, +5.3] | 11 / 10 | 1 |
| nocrit13 -> selfguided13 | heldout_musique | +4.9 | [-1.0, +11.3] | 25 / 15 | 0.154 |
| nocrit13 -> selfguided13 | heldout_strategyqa | -0.5 | [-4.3, +3.2] | 6 / 7 | 1 |
| nocrit13 -> selfguided13 | pooled | +1.9 | [-0.7, +4.4] | 52 / 38 | 0.17 |
| nocrit13 -> selfguided17 | heldout_2wikimultihopqa | +1.2 | [-4.1, +6.5] | 12 / 10 | 0.832 |
| nocrit13 -> selfguided17 | heldout_hotpotqa | -1.6 | [-5.8, +3.2] | 8 / 11 | 0.648 |
| nocrit13 -> selfguided17 | heldout_musique | +1.0 | [-5.9, +7.9] | 25 / 23 | 0.885 |
| nocrit13 -> selfguided17 | heldout_strategyqa | +0.0 | [-3.8, +3.8] | 7 / 7 | 1 |
| nocrit13 -> selfguided17 | pooled | +0.1 | [-2.5, +2.8] | 52 / 51 | 1 |
| nocrit13 -> selfguided23 | heldout_2wikimultihopqa | -2.9 | [-7.6, +1.8] | 6 / 11 | 0.332 |
| nocrit13 -> selfguided23 | heldout_hotpotqa | -1.6 | [-6.3, +3.2] | 10 / 13 | 0.678 |
| nocrit13 -> selfguided23 | heldout_musique | +0.5 | [-5.9, +6.9] | 21 / 20 | 1 |
| nocrit13 -> selfguided23 | heldout_strategyqa | -2.7 | [-7.0, +1.1] | 5 / 10 | 0.302 |
| nocrit13 -> selfguided23 | pooled | -1.6 | [-4.3, +0.9] | 42 / 54 | 0.261 |
| nocrit13 -> unguided13 | heldout_2wikimultihopqa | +0.0 | [-4.7, +4.7] | 9 / 9 | 1 |
| nocrit13 -> unguided13 | heldout_hotpotqa | -6.9 | [-12.2, -1.6] | 7 / 20 | 0.0192 |
| nocrit13 -> unguided13 | heldout_musique | -3.5 | [-10.3, +3.5] | 22 / 29 | 0.401 |
| nocrit13 -> unguided13 | heldout_strategyqa | +0.5 | [-4.3, +5.4] | 11 / 10 | 1 |
| nocrit13 -> unguided13 | pooled | -2.5 | [-5.3, +0.3] | 49 / 68 | 0.0957 |
| nocrit13 -> unguided17 | heldout_2wikimultihopqa | -0.6 | [-5.9, +4.7] | 10 / 11 | 1 |
| nocrit13 -> unguided17 | heldout_hotpotqa | -2.1 | [-7.4, +3.7] | 12 / 16 | 0.572 |
| nocrit13 -> unguided17 | heldout_musique | +1.0 | [-5.9, +7.9] | 27 / 25 | 0.89 |
| nocrit13 -> unguided17 | heldout_strategyqa | +1.6 | [-2.7, +5.9] | 10 / 7 | 0.629 |
| nocrit13 -> unguided17 | pooled | +0.0 | [-2.8, +2.8] | 59 / 59 | 1 |
| nocrit13 -> unguided23 | heldout_2wikimultihopqa | -2.4 | [-8.2, +3.5] | 10 / 14 | 0.541 |
| nocrit13 -> unguided23 | heldout_hotpotqa | -2.6 | [-7.9, +2.6] | 11 / 16 | 0.442 |
| nocrit13 -> unguided23 | heldout_musique | -2.0 | [-8.4, +4.4] | 20 / 24 | 0.652 |
| nocrit13 -> unguided23 | heldout_strategyqa | -1.6 | [-5.9, +2.7] | 7 / 10 | 0.629 |
| nocrit13 -> unguided23 | pooled | -2.1 | [-5.0, +0.5] | 48 / 64 | 0.156 |
| nocrit17 -> nocrit23 | heldout_2wikimultihopqa | -2.9 | [-7.6, +1.8] | 6 / 11 | 0.332 |
| nocrit17 -> nocrit23 | heldout_hotpotqa | +3.7 | [-1.1, +8.5] | 15 / 8 | 0.21 |
| nocrit17 -> nocrit23 | heldout_musique | +6.4 | [+0.5, +12.3] | 25 / 12 | 0.047 |
| nocrit17 -> nocrit23 | heldout_strategyqa | +0.5 | [-3.8, +4.9] | 8 / 7 | 1 |
| nocrit17 -> nocrit23 | pooled | +2.1 | [-0.3, +4.7] | 54 / 38 | 0.117 |
| nocrit17 -> selfguided13 | heldout_2wikimultihopqa | +1.8 | [-2.9, +6.5] | 11 / 8 | 0.648 |
| nocrit17 -> selfguided13 | heldout_hotpotqa | +5.3 | [+0.5, +10.1] | 16 / 6 | 0.0525 |
| nocrit17 -> selfguided13 | heldout_musique | +7.4 | [+1.5, +13.3] | 27 / 12 | 0.0237 |
| nocrit17 -> selfguided13 | heldout_strategyqa | +0.0 | [-3.8, +3.8] | 6 / 6 | 1 |
| nocrit17 -> selfguided13 | pooled | +3.8 | [+1.2, +6.3] | 60 / 32 | 0.00461 |
| nocrit17 -> selfguided17 | heldout_2wikimultihopqa | +0.6 | [-4.7, +5.9] | 11 / 10 | 1 |
| nocrit17 -> selfguided17 | heldout_hotpotqa | +3.2 | [-1.1, +7.4] | 11 / 5 | 0.21 |
| nocrit17 -> selfguided17 | heldout_musique | +3.5 | [-2.0, +8.9] | 21 / 14 | 0.311 |
| nocrit17 -> selfguided17 | heldout_strategyqa | +0.5 | [-3.8, +4.9] | 8 / 7 | 1 |
| nocrit17 -> selfguided17 | pooled | +2.0 | [-0.4, +4.4] | 51 / 36 | 0.133 |
| nocrit17 -> selfguided23 | heldout_2wikimultihopqa | -3.5 | [-8.8, +1.8] | 7 / 13 | 0.263 |
| nocrit17 -> selfguided23 | heldout_hotpotqa | +3.2 | [-1.6, +7.9] | 13 / 7 | 0.263 |
| nocrit17 -> selfguided23 | heldout_musique | +3.0 | [-3.0, +8.9] | 22 / 16 | 0.418 |
| nocrit17 -> selfguided23 | heldout_strategyqa | -2.2 | [-5.9, +1.6] | 5 / 9 | 0.424 |
| nocrit17 -> selfguided23 | pooled | +0.3 | [-2.3, +2.8] | 47 / 45 | 0.917 |
| nocrit17 -> unguided13 | heldout_2wikimultihopqa | -0.6 | [-5.9, +4.7] | 11 / 12 | 1 |
| nocrit17 -> unguided13 | heldout_hotpotqa | -2.1 | [-7.4, +3.2] | 12 / 16 | 0.572 |
| nocrit17 -> unguided13 | heldout_musique | -1.0 | [-7.4, +4.9] | 19 / 21 | 0.875 |
| nocrit17 -> unguided13 | heldout_strategyqa | +1.1 | [-3.8, +5.9] | 12 / 10 | 0.832 |
| nocrit17 -> unguided13 | pooled | -0.7 | [-3.4, +2.1] | 54 / 59 | 0.707 |
| nocrit17 -> unguided17 | heldout_2wikimultihopqa | -1.2 | [-7.1, +4.7] | 11 / 13 | 0.839 |
| nocrit17 -> unguided17 | heldout_hotpotqa | +2.6 | [-2.6, +7.9] | 15 / 10 | 0.424 |
| nocrit17 -> unguided17 | heldout_musique | +3.5 | [-3.5, +10.3] | 28 / 21 | 0.392 |
| nocrit17 -> unguided17 | heldout_strategyqa | +2.2 | [-2.7, +7.0] | 13 / 9 | 0.523 |
| nocrit17 -> unguided17 | pooled | +1.9 | [-0.9, +4.8] | 67 / 53 | 0.235 |
| nocrit17 -> unguided23 | heldout_2wikimultihopqa | -2.9 | [-8.8, +2.4] | 9 / 14 | 0.405 |
| nocrit17 -> unguided23 | heldout_hotpotqa | +2.1 | [-2.6, +6.9] | 13 / 9 | 0.523 |
| nocrit17 -> unguided23 | heldout_musique | +0.5 | [-5.9, +6.4] | 21 / 20 | 1 |
| nocrit17 -> unguided23 | heldout_strategyqa | -1.1 | [-6.5, +4.3] | 11 / 13 | 0.839 |
| nocrit17 -> unguided23 | pooled | -0.3 | [-2.9, +2.5] | 54 / 56 | 0.924 |
| nocrit23 -> selfguided13 | heldout_2wikimultihopqa | +4.7 | [+0.0, +9.4] | 13 / 5 | 0.0963 |
| nocrit23 -> selfguided13 | heldout_hotpotqa | +1.6 | [-3.2, +6.3] | 12 / 9 | 0.664 |
| nocrit23 -> selfguided13 | heldout_musique | +1.0 | [-4.4, +6.9] | 18 / 16 | 0.864 |
| nocrit23 -> selfguided13 | heldout_strategyqa | -0.5 | [-4.3, +3.2] | 6 / 7 | 1 |
| nocrit23 -> selfguided13 | pooled | +1.6 | [-0.8, +4.0] | 49 / 37 | 0.235 |
| nocrit23 -> selfguided17 | heldout_2wikimultihopqa | +3.5 | [-2.4, +9.4] | 15 / 9 | 0.307 |
| nocrit23 -> selfguided17 | heldout_hotpotqa | -0.5 | [-4.8, +4.2] | 9 / 10 | 1 |
| nocrit23 -> selfguided17 | heldout_musique | -3.0 | [-8.9, +3.5] | 17 / 23 | 0.43 |
| nocrit23 -> selfguided17 | heldout_strategyqa | +0.0 | [-4.3, +4.3] | 8 / 8 | 1 |
| nocrit23 -> selfguided17 | pooled | -0.1 | [-2.8, +2.5] | 49 / 50 | 1 |
| nocrit23 -> selfguided23 | heldout_2wikimultihopqa | -0.6 | [-5.3, +4.1] | 8 / 9 | 1 |
| nocrit23 -> selfguided23 | heldout_hotpotqa | -0.5 | [-5.3, +4.2] | 10 / 11 | 1 |
| nocrit23 -> selfguided23 | heldout_musique | -3.5 | [-9.4, +2.5] | 15 / 22 | 0.324 |
| nocrit23 -> selfguided23 | heldout_strategyqa | -2.7 | [-6.5, +1.1] | 4 / 9 | 0.267 |
| nocrit23 -> selfguided23 | pooled | -1.9 | [-4.4, +0.5] | 37 / 51 | 0.165 |
| nocrit23 -> unguided13 | heldout_2wikimultihopqa | +2.4 | [-2.9, +7.6] | 13 / 9 | 0.523 |
| nocrit23 -> unguided13 | heldout_hotpotqa | -5.8 | [-11.6, +0.0] | 10 / 21 | 0.0708 |
| nocrit23 -> unguided13 | heldout_musique | -7.4 | [-14.3, -0.5] | 17 / 32 | 0.0444 |
| nocrit23 -> unguided13 | heldout_strategyqa | +0.5 | [-3.2, +4.3] | 7 / 6 | 1 |
| nocrit23 -> unguided13 | pooled | -2.8 | [-5.6, +0.0] | 47 / 68 | 0.0617 |
| nocrit23 -> unguided17 | heldout_2wikimultihopqa | +1.8 | [-4.7, +8.2] | 16 / 13 | 0.711 |
| nocrit23 -> unguided17 | heldout_hotpotqa | -1.1 | [-6.3, +4.2] | 12 / 14 | 0.845 |
| nocrit23 -> unguided17 | heldout_musique | -3.0 | [-9.4, +3.5] | 18 / 24 | 0.441 |
| nocrit23 -> unguided17 | heldout_strategyqa | +1.6 | [-2.2, +5.4] | 8 / 5 | 0.581 |
| nocrit23 -> unguided17 | pooled | -0.3 | [-2.9, +2.4] | 54 / 56 | 0.924 |
| nocrit23 -> unguided23 | heldout_2wikimultihopqa | +0.0 | [-5.9, +5.9] | 13 / 13 | 1 |
| nocrit23 -> unguided23 | heldout_hotpotqa | -1.6 | [-6.9, +4.2] | 13 / 16 | 0.711 |
| nocrit23 -> unguided23 | heldout_musique | -5.9 | [-12.8, +1.0] | 20 / 32 | 0.126 |
| nocrit23 -> unguided23 | heldout_strategyqa | -1.6 | [-5.9, +2.7] | 6 / 9 | 0.607 |
| nocrit23 -> unguided23 | pooled | -2.4 | [-5.3, +0.5] | 52 / 70 | 0.123 |
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
