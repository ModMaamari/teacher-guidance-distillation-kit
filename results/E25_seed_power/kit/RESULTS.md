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
| selfguided29 | heldout_2wikimultihopqa | 170 | yes | 0.059 | 0.221 | 0.800 | 0.794 | 0.844 | 2.92 | 0.08 | 5,326 | 23.0 | 0.0000 |
| selfguided29 | heldout_hotpotqa | 189 | yes | 0.265 | 0.360 | 0.635 | 0.656 | 0.767 | 2.81 | 0.19 | 5,022 | 22.3 | 0.0000 |
| selfguided29 | heldout_musique | 203 | yes | 0.069 | 0.192 | 0.389 | 0.429 | 0.653 | 2.93 | 0.07 | 5,200 | 22.7 | 0.0000 |
| selfguided29 | heldout_strategyqa | 185 | yes | 0.000 | 0.035 | 0.665 | 0.697 | 0.835 | 2.94 | 0.06 | 5,144 | 24.8 | 0.0000 |
| selfguided31 | heldout_2wikimultihopqa | 170 | yes | 0.041 | 0.202 | 0.765 | 0.759 | 0.854 | 2.95 | 0.05 | 5,412 | 25.1 | 0.0000 |
| selfguided31 | heldout_hotpotqa | 189 | yes | 0.280 | 0.384 | 0.651 | 0.682 | 0.762 | 2.76 | 0.24 | 4,873 | 23.0 | 0.0000 |
| selfguided31 | heldout_musique | 203 | yes | 0.074 | 0.205 | 0.419 | 0.473 | 0.649 | 2.94 | 0.06 | 5,212 | 23.7 | 0.0000 |
| selfguided31 | heldout_strategyqa | 185 | yes | 0.000 | 0.036 | 0.686 | 0.708 | 0.817 | 2.89 | 0.11 | 5,107 | 26.4 | 0.0000 |
| selfguided37 | heldout_2wikimultihopqa | 170 | yes | 0.059 | 0.225 | 0.806 | 0.788 | 0.856 | 2.96 | 0.04 | 5,331 | 17.9 | 0.0000 |
| selfguided37 | heldout_hotpotqa | 189 | yes | 0.296 | 0.390 | 0.645 | 0.677 | 0.780 | 2.79 | 0.21 | 4,986 | 17.0 | 0.0000 |
| selfguided37 | heldout_musique | 203 | yes | 0.064 | 0.201 | 0.419 | 0.468 | 0.658 | 2.91 | 0.09 | 5,268 | 17.8 | 0.0000 |
| selfguided37 | heldout_strategyqa | 185 | yes | 0.000 | 0.035 | 0.681 | 0.703 | 0.823 | 2.95 | 0.05 | 5,268 | 15.3 | 0.0000 |
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
| unguided29 | heldout_2wikimultihopqa | 170 | yes | 0.053 | 0.194 | 0.747 | 0.753 | 0.809 | 2.97 | 0.03 | 5,108 | 19.4 | 0.0000 |
| unguided29 | heldout_hotpotqa | 189 | yes | 0.228 | 0.327 | 0.603 | 0.614 | 0.754 | 2.85 | 0.15 | 4,830 | 19.0 | 0.0000 |
| unguided29 | heldout_musique | 203 | yes | 0.044 | 0.176 | 0.379 | 0.438 | 0.614 | 2.96 | 0.04 | 4,748 | 18.4 | 0.0000 |
| unguided29 | heldout_strategyqa | 185 | yes | 0.000 | 0.035 | 0.665 | 0.703 | 0.817 | 2.96 | 0.03 | 4,875 | 21.0 | 0.0000 |
| unguided31 | heldout_2wikimultihopqa | 170 | yes | 0.053 | 0.198 | 0.753 | 0.729 | 0.825 | 2.97 | 0.03 | 5,062 | 19.2 | 0.0000 |
| unguided31 | heldout_hotpotqa | 189 | yes | 0.238 | 0.331 | 0.598 | 0.614 | 0.746 | 2.86 | 0.14 | 4,855 | 18.6 | 0.0000 |
| unguided31 | heldout_musique | 203 | yes | 0.049 | 0.173 | 0.369 | 0.394 | 0.595 | 2.95 | 0.05 | 4,729 | 18.2 | 0.0000 |
| unguided31 | heldout_strategyqa | 185 | yes | 0.000 | 0.035 | 0.654 | 0.719 | 0.818 | 2.97 | 0.03 | 4,830 | 21.0 | 0.0000 |
| unguided37 | heldout_2wikimultihopqa | 170 | yes | 0.053 | 0.196 | 0.759 | 0.753 | 0.841 | 2.95 | 0.05 | 5,058 | 15.5 | 0.0000 |
| unguided37 | heldout_hotpotqa | 189 | yes | 0.222 | 0.317 | 0.640 | 0.656 | 0.767 | 2.84 | 0.16 | 4,763 | 15.0 | 0.0000 |
| unguided37 | heldout_musique | 203 | yes | 0.020 | 0.148 | 0.389 | 0.424 | 0.591 | 2.97 | 0.03 | 4,780 | 14.8 | 0.0000 |
| unguided37 | heldout_strategyqa | 185 | yes | 0.000 | 0.033 | 0.622 | 0.692 | 0.826 | 2.96 | 0.04 | 4,818 | 16.0 | 0.0000 |

## Pooled per arm

| arm | test sets | n | EM | F1 | cover | judge | steps | tokens/ep | API $ |
|---|---|---|---|---|---|---|---|---|---|
| base | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.052 | 0.113 | 0.232 | 0.273 | 2.97 | 5,067 | 0.0000 |
| selfguided13 | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.099 | 0.206 | 0.632 | 0.667 | 2.90 | 5,159 | 0.0000 |
| selfguided17 | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.100 | 0.201 | 0.616 | 0.649 | 2.89 | 5,213 | 0.0000 |
| selfguided23 | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.088 | 0.193 | 0.606 | 0.632 | 2.87 | 5,155 | 0.0000 |
| selfguided29 | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.099 | 0.202 | 0.613 | 0.636 | 2.90 | 5,170 | 0.0000 |
| selfguided31 | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.100 | 0.208 | 0.623 | 0.649 | 2.88 | 5,146 | 0.0000 |
| selfguided37 | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.106 | 0.213 | 0.629 | 0.652 | 2.90 | 5,211 | 0.0000 |
| unguided13 | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.084 | 0.184 | 0.589 | 0.623 | 2.93 | 4,860 | 0.0000 |
| unguided17 | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.080 | 0.182 | 0.605 | 0.648 | 2.92 | 4,853 | 0.0000 |
| unguided23 | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.080 | 0.181 | 0.594 | 0.626 | 2.94 | 4,896 | 0.0000 |
| unguided29 | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.082 | 0.183 | 0.590 | 0.620 | 2.94 | 4,882 | 0.0000 |
| unguided31 | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.086 | 0.185 | 0.585 | 0.606 | 2.94 | 4,862 | 0.0000 |
| unguided37 | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.074 | 0.173 | 0.594 | 0.624 | 2.93 | 4,848 | 0.0000 |

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
| base -> selfguided29 | heldout_2wikimultihopqa | +44.1 | [+35.9, +52.3] | 79 / 4 | 0 |
| base -> selfguided29 | heldout_hotpotqa | +22.8 | [+15.9, +29.6] | 50 / 7 | 0 |
| base -> selfguided29 | heldout_musique | +25.6 | [+18.2, +33.0] | 64 / 12 | 0 |
| base -> selfguided29 | heldout_strategyqa | +54.6 | [+47.0, +62.2] | 102 / 1 | 0 |
| base -> selfguided29 | pooled | +36.3 | [+32.4, +40.2] | 295 / 24 | 0 |
| base -> selfguided31 | heldout_2wikimultihopqa | +40.6 | [+32.9, +48.8] | 73 / 4 | 0 |
| base -> selfguided31 | heldout_hotpotqa | +25.4 | [+18.0, +32.8] | 55 / 7 | 0 |
| base -> selfguided31 | heldout_musique | +30.0 | [+22.7, +37.4] | 69 / 8 | 0 |
| base -> selfguided31 | heldout_strategyqa | +55.7 | [+48.1, +63.2] | 104 / 1 | 0 |
| base -> selfguided31 | pooled | +37.6 | [+33.7, +41.5] | 301 / 20 | 0 |
| base -> selfguided37 | heldout_2wikimultihopqa | +43.5 | [+35.3, +51.8] | 78 / 4 | 0 |
| base -> selfguided37 | heldout_hotpotqa | +24.9 | [+18.0, +32.3] | 53 / 6 | 0 |
| base -> selfguided37 | heldout_musique | +29.6 | [+21.7, +37.4] | 73 / 13 | 0 |
| base -> selfguided37 | heldout_strategyqa | +55.1 | [+47.6, +62.7] | 103 / 1 | 0 |
| base -> selfguided37 | pooled | +37.9 | [+33.9, +41.8] | 307 / 24 | 0 |
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
| base -> unguided29 | heldout_2wikimultihopqa | +40.0 | [+31.8, +48.2] | 72 / 4 | 0 |
| base -> unguided29 | heldout_hotpotqa | +18.5 | [+11.6, +25.4] | 44 / 9 | 1e-06 |
| base -> unguided29 | heldout_musique | +26.6 | [+19.7, +33.5] | 60 / 6 | 0 |
| base -> unguided29 | heldout_strategyqa | +55.1 | [+48.1, +62.7] | 103 / 1 | 0 |
| base -> unguided29 | pooled | +34.7 | [+30.9, +38.6] | 279 / 20 | 0 |
| base -> unguided31 | heldout_2wikimultihopqa | +37.6 | [+29.4, +45.9] | 70 / 6 | 0 |
| base -> unguided31 | heldout_hotpotqa | +18.5 | [+11.6, +25.4] | 43 / 8 | 1e-06 |
| base -> unguided31 | heldout_musique | +22.2 | [+15.8, +28.6] | 51 / 6 | 0 |
| base -> unguided31 | heldout_strategyqa | +56.8 | [+49.7, +63.8] | 105 / 0 | 0 |
| base -> unguided31 | pooled | +33.3 | [+29.6, +37.1] | 269 / 20 | 0 |
| base -> unguided37 | heldout_2wikimultihopqa | +40.0 | [+31.8, +48.2] | 73 / 5 | 0 |
| base -> unguided37 | heldout_hotpotqa | +22.8 | [+15.9, +30.2] | 51 / 8 | 0 |
| base -> unguided37 | heldout_musique | +25.1 | [+18.2, +32.0] | 57 / 6 | 0 |
| base -> unguided37 | heldout_strategyqa | +54.0 | [+46.5, +61.6] | 101 / 1 | 0 |
| base -> unguided37 | pooled | +35.1 | [+31.3, +38.8] | 282 / 20 | 0 |
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
| selfguided13 -> selfguided29 | heldout_2wikimultihopqa | +0.6 | [-4.7, +5.9] | 12 / 11 | 1 |
| selfguided13 -> selfguided29 | heldout_hotpotqa | -3.2 | [-7.9, +1.6] | 7 / 13 | 0.263 |
| selfguided13 -> selfguided29 | heldout_musique | -6.4 | [-11.8, -1.0] | 9 / 22 | 0.0294 |
| selfguided13 -> selfguided29 | heldout_strategyqa | -2.7 | [-5.9, +0.5] | 2 / 7 | 0.18 |
| selfguided13 -> selfguided29 | pooled | -3.1 | [-5.5, -0.7] | 30 / 53 | 0.0152 |
| selfguided13 -> selfguided31 | heldout_2wikimultihopqa | -2.9 | [-8.2, +2.4] | 8 / 13 | 0.383 |
| selfguided13 -> selfguided31 | heldout_hotpotqa | -0.5 | [-5.3, +4.2] | 9 / 10 | 1 |
| selfguided13 -> selfguided31 | heldout_musique | -2.0 | [-7.9, +3.9] | 16 / 20 | 0.618 |
| selfguided13 -> selfguided31 | heldout_strategyqa | -1.6 | [-5.9, +2.7] | 6 / 9 | 0.607 |
| selfguided13 -> selfguided31 | pooled | -1.7 | [-4.3, +0.7] | 39 / 52 | 0.208 |
| selfguided13 -> selfguided37 | heldout_2wikimultihopqa | +0.0 | [-5.3, +5.3] | 10 / 10 | 1 |
| selfguided13 -> selfguided37 | heldout_hotpotqa | -1.1 | [-6.3, +4.2] | 12 / 14 | 0.845 |
| selfguided13 -> selfguided37 | heldout_musique | -2.5 | [-8.4, +3.5] | 18 / 23 | 0.533 |
| selfguided13 -> selfguided37 | heldout_strategyqa | -2.2 | [-5.9, +1.6] | 4 / 8 | 0.388 |
| selfguided13 -> selfguided37 | pooled | -1.5 | [-4.0, +1.1] | 44 / 55 | 0.315 |
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
| selfguided13 -> unguided29 | heldout_2wikimultihopqa | -3.5 | [-8.2, +1.2] | 5 / 11 | 0.21 |
| selfguided13 -> unguided29 | heldout_hotpotqa | -7.4 | [-13.2, -1.6] | 10 / 24 | 0.0243 |
| selfguided13 -> unguided29 | heldout_musique | -5.4 | [-12.3, +1.5] | 20 / 31 | 0.161 |
| selfguided13 -> unguided29 | heldout_strategyqa | -2.2 | [-5.9, +1.6] | 5 / 9 | 0.424 |
| selfguided13 -> unguided29 | pooled | -4.7 | [-7.6, -1.9] | 40 / 75 | 0.00141 |
| selfguided13 -> unguided31 | heldout_2wikimultihopqa | -5.9 | [-11.2, -0.6] | 6 / 16 | 0.0525 |
| selfguided13 -> unguided31 | heldout_hotpotqa | -7.4 | [-13.2, -1.6] | 10 / 24 | 0.0243 |
| selfguided13 -> unguided31 | heldout_musique | -9.8 | [-16.8, -3.0] | 16 / 36 | 0.00779 |
| selfguided13 -> unguided31 | heldout_strategyqa | -0.5 | [-4.9, +3.2] | 7 / 8 | 1 |
| selfguided13 -> unguided31 | pooled | -6.0 | [-9.0, -3.1] | 39 / 84 | 6.1e-05 |
| selfguided13 -> unguided37 | heldout_2wikimultihopqa | -3.5 | [-8.2, +1.2] | 6 / 12 | 0.238 |
| selfguided13 -> unguided37 | heldout_hotpotqa | -3.2 | [-8.5, +2.1] | 9 / 15 | 0.307 |
| selfguided13 -> unguided37 | heldout_musique | -6.9 | [-14.3, +0.0] | 21 / 35 | 0.0814 |
| selfguided13 -> unguided37 | heldout_strategyqa | -3.2 | [-7.6, +1.1] | 5 / 11 | 0.21 |
| selfguided13 -> unguided37 | pooled | -4.3 | [-7.1, -1.5] | 41 / 73 | 0.0035 |
| selfguided17 -> selfguided23 | heldout_2wikimultihopqa | -4.1 | [-10.0, +1.8] | 9 / 16 | 0.23 |
| selfguided17 -> selfguided23 | heldout_hotpotqa | +0.0 | [-4.2, +4.2] | 8 / 8 | 1 |
| selfguided17 -> selfguided23 | heldout_musique | -0.5 | [-5.9, +4.9] | 16 / 17 | 1 |
| selfguided17 -> selfguided23 | heldout_strategyqa | -2.7 | [-7.0, +1.6] | 6 / 11 | 0.332 |
| selfguided17 -> selfguided23 | pooled | -1.7 | [-4.3, +0.7] | 39 / 52 | 0.208 |
| selfguided17 -> selfguided29 | heldout_2wikimultihopqa | +1.8 | [-4.1, +7.6] | 14 / 11 | 0.69 |
| selfguided17 -> selfguided29 | heldout_hotpotqa | -1.1 | [-5.3, +3.2] | 7 / 9 | 0.804 |
| selfguided17 -> selfguided29 | heldout_musique | -2.5 | [-7.9, +3.0] | 13 / 18 | 0.473 |
| selfguided17 -> selfguided29 | heldout_strategyqa | -3.2 | [-7.0, +0.5] | 3 / 9 | 0.146 |
| selfguided17 -> selfguided29 | pooled | -1.3 | [-3.6, +1.1] | 37 / 47 | 0.326 |
| selfguided17 -> selfguided31 | heldout_2wikimultihopqa | -1.8 | [-6.5, +2.9] | 7 / 10 | 0.629 |
| selfguided17 -> selfguided31 | heldout_hotpotqa | +1.6 | [-2.6, +5.8] | 10 / 7 | 0.629 |
| selfguided17 -> selfguided31 | heldout_musique | +2.0 | [-3.5, +7.4] | 17 / 13 | 0.585 |
| selfguided17 -> selfguided31 | heldout_strategyqa | -2.2 | [-6.5, +2.2] | 6 / 10 | 0.454 |
| selfguided17 -> selfguided31 | pooled | +0.0 | [-2.3, +2.3] | 40 / 40 | 1 |
| selfguided17 -> selfguided37 | heldout_2wikimultihopqa | +1.2 | [-4.1, +5.9] | 10 / 8 | 0.815 |
| selfguided17 -> selfguided37 | heldout_hotpotqa | +1.1 | [-3.7, +5.8] | 11 / 9 | 0.824 |
| selfguided17 -> selfguided37 | heldout_musique | +1.5 | [-4.9, +7.9] | 23 / 20 | 0.761 |
| selfguided17 -> selfguided37 | heldout_strategyqa | -2.7 | [-6.5, +1.1] | 4 / 9 | 0.267 |
| selfguided17 -> selfguided37 | pooled | +0.3 | [-2.3, +2.8] | 48 / 46 | 0.918 |
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
| selfguided17 -> unguided29 | heldout_2wikimultihopqa | -2.4 | [-7.6, +2.9] | 9 / 13 | 0.523 |
| selfguided17 -> unguided29 | heldout_hotpotqa | -5.3 | [-11.1, +0.5] | 11 / 21 | 0.11 |
| selfguided17 -> unguided29 | heldout_musique | -1.5 | [-8.4, +5.4] | 25 / 28 | 0.784 |
| selfguided17 -> unguided29 | heldout_strategyqa | -2.7 | [-7.0, +1.6] | 6 / 11 | 0.332 |
| selfguided17 -> unguided29 | pooled | -2.9 | [-5.8, +0.0] | 51 / 73 | 0.0589 |
| selfguided17 -> unguided31 | heldout_2wikimultihopqa | -4.7 | [-10.6, +0.6] | 8 / 16 | 0.152 |
| selfguided17 -> unguided31 | heldout_hotpotqa | -5.3 | [-10.1, -0.5] | 6 / 16 | 0.0525 |
| selfguided17 -> unguided31 | heldout_musique | -5.9 | [-12.3, +1.0] | 18 / 30 | 0.111 |
| selfguided17 -> unguided31 | heldout_strategyqa | -1.1 | [-5.4, +3.2] | 7 / 9 | 0.804 |
| selfguided17 -> unguided31 | pooled | -4.3 | [-7.0, -1.6] | 39 / 71 | 0.00294 |
| selfguided17 -> unguided37 | heldout_2wikimultihopqa | -2.4 | [-8.2, +3.5] | 10 / 14 | 0.541 |
| selfguided17 -> unguided37 | heldout_hotpotqa | -1.1 | [-5.3, +3.2] | 8 / 10 | 0.815 |
| selfguided17 -> unguided37 | heldout_musique | -3.0 | [-9.8, +3.9] | 23 / 29 | 0.488 |
| selfguided17 -> unguided37 | heldout_strategyqa | -3.8 | [-8.6, +0.5] | 6 / 13 | 0.167 |
| selfguided17 -> unguided37 | pooled | -2.5 | [-5.2, +0.3] | 47 / 66 | 0.09 |
| selfguided23 -> selfguided29 | heldout_2wikimultihopqa | +5.9 | [+0.0, +11.8] | 17 / 7 | 0.0639 |
| selfguided23 -> selfguided29 | heldout_hotpotqa | -1.1 | [-5.8, +3.7] | 10 / 12 | 0.832 |
| selfguided23 -> selfguided29 | heldout_musique | -2.0 | [-7.9, +3.9] | 16 / 20 | 0.618 |
| selfguided23 -> selfguided29 | heldout_strategyqa | -0.5 | [-4.3, +3.2] | 6 / 7 | 1 |
| selfguided23 -> selfguided29 | pooled | +0.4 | [-2.1, +2.9] | 49 / 46 | 0.838 |
| selfguided23 -> selfguided31 | heldout_2wikimultihopqa | +2.4 | [-2.9, +7.6] | 12 / 8 | 0.503 |
| selfguided23 -> selfguided31 | heldout_hotpotqa | +1.6 | [-3.2, +6.3] | 12 / 9 | 0.664 |
| selfguided23 -> selfguided31 | heldout_musique | +2.5 | [-3.0, +7.9] | 19 / 14 | 0.487 |
| selfguided23 -> selfguided31 | heldout_strategyqa | +0.5 | [-3.2, +4.9] | 8 / 7 | 1 |
| selfguided23 -> selfguided31 | pooled | +1.7 | [-0.7, +4.2] | 51 / 38 | 0.203 |
| selfguided23 -> selfguided37 | heldout_2wikimultihopqa | +5.3 | [+0.0, +10.6] | 15 / 6 | 0.0784 |
| selfguided23 -> selfguided37 | heldout_hotpotqa | +1.1 | [-4.2, +6.3] | 14 / 12 | 0.845 |
| selfguided23 -> selfguided37 | heldout_musique | +2.0 | [-3.9, +7.9] | 19 / 15 | 0.608 |
| selfguided23 -> selfguided37 | heldout_strategyqa | +0.0 | [-3.8, +3.8] | 6 / 6 | 1 |
| selfguided23 -> selfguided37 | pooled | +2.0 | [-0.5, +4.5] | 54 / 39 | 0.146 |
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
| selfguided23 -> unguided29 | heldout_2wikimultihopqa | +1.8 | [-4.1, +7.1] | 13 / 10 | 0.678 |
| selfguided23 -> unguided29 | heldout_hotpotqa | -5.3 | [-10.6, +0.0] | 8 / 18 | 0.0755 |
| selfguided23 -> unguided29 | heldout_musique | -1.0 | [-8.4, +6.4] | 27 / 29 | 0.894 |
| selfguided23 -> unguided29 | heldout_strategyqa | +0.0 | [-4.3, +4.3] | 8 / 8 | 1 |
| selfguided23 -> unguided29 | pooled | -1.2 | [-4.0, +1.6] | 56 / 65 | 0.467 |
| selfguided23 -> unguided31 | heldout_2wikimultihopqa | -0.6 | [-5.9, +4.7] | 9 / 10 | 1 |
| selfguided23 -> unguided31 | heldout_hotpotqa | -5.3 | [-10.6, +0.0] | 9 / 19 | 0.0872 |
| selfguided23 -> unguided31 | heldout_musique | -5.4 | [-11.3, +0.5] | 14 / 25 | 0.108 |
| selfguided23 -> unguided31 | heldout_strategyqa | +1.6 | [-2.2, +5.4] | 9 / 6 | 0.607 |
| selfguided23 -> unguided31 | pooled | -2.5 | [-5.1, +0.1] | 41 / 60 | 0.0728 |
| selfguided23 -> unguided37 | heldout_2wikimultihopqa | +1.8 | [-3.5, +7.1] | 12 / 9 | 0.664 |
| selfguided23 -> unguided37 | heldout_hotpotqa | -1.1 | [-5.8, +3.7] | 9 / 11 | 0.824 |
| selfguided23 -> unguided37 | heldout_musique | -2.5 | [-9.8, +4.4] | 25 / 30 | 0.59 |
| selfguided23 -> unguided37 | heldout_strategyqa | -1.1 | [-5.4, +3.2] | 8 / 10 | 0.815 |
| selfguided23 -> unguided37 | pooled | -0.8 | [-3.6, +2.0] | 54 / 60 | 0.64 |
| selfguided29 -> selfguided31 | heldout_2wikimultihopqa | -3.5 | [-8.8, +1.8] | 7 / 13 | 0.263 |
| selfguided29 -> selfguided31 | heldout_hotpotqa | +2.6 | [-1.6, +6.9] | 11 / 6 | 0.332 |
| selfguided29 -> selfguided31 | heldout_musique | +4.4 | [-1.0, +9.8] | 21 / 12 | 0.163 |
| selfguided29 -> selfguided31 | heldout_strategyqa | +1.1 | [-3.2, +5.4] | 9 / 7 | 0.804 |
| selfguided29 -> selfguided31 | pooled | +1.3 | [-1.1, +3.8] | 48 / 38 | 0.332 |
| selfguided29 -> selfguided37 | heldout_2wikimultihopqa | -0.6 | [-5.3, +4.1] | 8 / 9 | 1 |
| selfguided29 -> selfguided37 | heldout_hotpotqa | +2.1 | [-2.6, +6.9] | 13 / 9 | 0.523 |
| selfguided29 -> selfguided37 | heldout_musique | +3.9 | [-2.0, +9.8] | 23 / 15 | 0.256 |
| selfguided29 -> selfguided37 | heldout_strategyqa | +0.5 | [-2.7, +3.8] | 6 / 5 | 1 |
| selfguided29 -> selfguided37 | pooled | +1.6 | [-0.8, +4.0] | 50 / 38 | 0.241 |
| selfguided29 -> unguided13 | heldout_2wikimultihopqa | -2.9 | [-7.6, +1.8] | 6 / 11 | 0.332 |
| selfguided29 -> unguided13 | heldout_hotpotqa | -4.2 | [-9.5, +1.1] | 9 / 17 | 0.169 |
| selfguided29 -> unguided13 | heldout_musique | -2.0 | [-8.4, +4.4] | 20 / 24 | 0.652 |
| selfguided29 -> unguided13 | heldout_strategyqa | +3.8 | [-0.5, +8.1] | 12 / 5 | 0.143 |
| selfguided29 -> unguided13 | pooled | -1.3 | [-4.0, +1.3] | 47 / 57 | 0.378 |
| selfguided29 -> unguided17 | heldout_2wikimultihopqa | -3.5 | [-9.4, +2.4] | 9 / 15 | 0.307 |
| selfguided29 -> unguided17 | heldout_hotpotqa | +0.5 | [-4.8, +5.8] | 13 / 12 | 1 |
| selfguided29 -> unguided17 | heldout_musique | +2.5 | [-4.4, +8.9] | 27 / 22 | 0.568 |
| selfguided29 -> unguided17 | heldout_strategyqa | +4.9 | [+0.5, +9.7] | 14 / 5 | 0.0636 |
| selfguided29 -> unguided17 | pooled | +1.2 | [-1.6, +4.0] | 63 / 54 | 0.46 |
| selfguided29 -> unguided23 | heldout_2wikimultihopqa | -5.3 | [-11.2, +0.0] | 8 / 17 | 0.108 |
| selfguided29 -> unguided23 | heldout_hotpotqa | +0.0 | [-4.8, +4.8] | 11 / 11 | 1 |
| selfguided29 -> unguided23 | heldout_musique | -0.5 | [-6.9, +5.9] | 21 / 22 | 1 |
| selfguided29 -> unguided23 | heldout_strategyqa | +1.6 | [-2.7, +6.5] | 11 / 8 | 0.648 |
| selfguided29 -> unguided23 | pooled | -0.9 | [-3.6, +1.7] | 51 / 58 | 0.566 |
| selfguided29 -> unguided29 | heldout_2wikimultihopqa | -4.1 | [-9.4, +1.2] | 7 / 14 | 0.189 |
| selfguided29 -> unguided29 | heldout_hotpotqa | -4.2 | [-10.1, +1.6] | 13 / 21 | 0.229 |
| selfguided29 -> unguided29 | heldout_musique | +1.0 | [-5.9, +7.9] | 26 / 24 | 0.888 |
| selfguided29 -> unguided29 | heldout_strategyqa | +0.5 | [-3.8, +4.9] | 10 / 9 | 1 |
| selfguided29 -> unguided29 | pooled | -1.6 | [-4.5, +1.3] | 56 / 68 | 0.323 |
| selfguided29 -> unguided31 | heldout_2wikimultihopqa | -6.5 | [-11.2, -2.4] | 2 / 13 | 0.00739 |
| selfguided29 -> unguided31 | heldout_hotpotqa | -4.2 | [-9.5, +0.5] | 8 / 16 | 0.152 |
| selfguided29 -> unguided31 | heldout_musique | -3.5 | [-9.8, +3.0] | 19 / 26 | 0.371 |
| selfguided29 -> unguided31 | heldout_strategyqa | +2.2 | [-2.2, +6.5] | 10 / 6 | 0.454 |
| selfguided29 -> unguided31 | pooled | -2.9 | [-5.5, -0.4] | 39 / 61 | 0.0352 |
| selfguided29 -> unguided37 | heldout_2wikimultihopqa | -4.1 | [-9.4, +1.2] | 8 / 15 | 0.21 |
| selfguided29 -> unguided37 | heldout_hotpotqa | +0.0 | [-4.8, +4.8] | 10 / 10 | 1 |
| selfguided29 -> unguided37 | heldout_musique | -0.5 | [-7.4, +5.9] | 24 / 25 | 1 |
| selfguided29 -> unguided37 | heldout_strategyqa | -0.5 | [-4.9, +3.8] | 8 / 9 | 1 |
| selfguided29 -> unguided37 | pooled | -1.2 | [-3.9, +1.6] | 50 / 59 | 0.444 |
| selfguided31 -> selfguided37 | heldout_2wikimultihopqa | +2.9 | [-2.4, +7.6] | 12 / 7 | 0.359 |
| selfguided31 -> selfguided37 | heldout_hotpotqa | -0.5 | [-5.3, +4.2] | 10 / 11 | 1 |
| selfguided31 -> selfguided37 | heldout_musique | -0.5 | [-6.4, +5.4] | 19 / 20 | 1 |
| selfguided31 -> selfguided37 | heldout_strategyqa | -0.5 | [-4.3, +2.7] | 5 / 6 | 1 |
| selfguided31 -> selfguided37 | pooled | +0.3 | [-2.1, +2.8] | 46 / 44 | 0.916 |
| selfguided31 -> unguided13 | heldout_2wikimultihopqa | +0.6 | [-4.1, +5.3] | 9 / 8 | 1 |
| selfguided31 -> unguided13 | heldout_hotpotqa | -6.9 | [-12.2, -1.6] | 8 / 21 | 0.0241 |
| selfguided31 -> unguided13 | heldout_musique | -6.4 | [-12.8, +0.0] | 16 / 29 | 0.0725 |
| selfguided31 -> unguided13 | heldout_strategyqa | +2.7 | [-1.6, +7.0] | 11 / 6 | 0.332 |
| selfguided31 -> unguided13 | pooled | -2.7 | [-5.3, +0.0] | 44 / 64 | 0.067 |
| selfguided31 -> unguided17 | heldout_2wikimultihopqa | +0.0 | [-5.9, +5.9] | 12 / 12 | 1 |
| selfguided31 -> unguided17 | heldout_hotpotqa | -2.1 | [-7.4, +3.2] | 11 / 15 | 0.557 |
| selfguided31 -> unguided17 | heldout_musique | -2.0 | [-7.9, +3.9] | 17 / 21 | 0.627 |
| selfguided31 -> unguided17 | heldout_strategyqa | +3.8 | [+0.0, +8.1] | 11 / 4 | 0.118 |
| selfguided31 -> unguided17 | pooled | -0.1 | [-2.8, +2.5] | 51 / 52 | 1 |
| selfguided31 -> unguided23 | heldout_2wikimultihopqa | -1.8 | [-7.6, +3.5] | 10 / 13 | 0.678 |
| selfguided31 -> unguided23 | heldout_hotpotqa | -2.6 | [-7.4, +2.1] | 8 / 13 | 0.383 |
| selfguided31 -> unguided23 | heldout_musique | -4.9 | [-10.8, +1.0] | 15 / 25 | 0.154 |
| selfguided31 -> unguided23 | heldout_strategyqa | +0.5 | [-4.3, +5.4] | 11 / 10 | 1 |
| selfguided31 -> unguided23 | pooled | -2.3 | [-5.0, +0.4] | 44 / 61 | 0.118 |
| selfguided31 -> unguided29 | heldout_2wikimultihopqa | -0.6 | [-5.9, +4.7] | 10 / 11 | 1 |
| selfguided31 -> unguided29 | heldout_hotpotqa | -6.9 | [-12.7, -1.1] | 9 / 22 | 0.0294 |
| selfguided31 -> unguided29 | heldout_musique | -3.5 | [-10.3, +3.5] | 21 / 28 | 0.392 |
| selfguided31 -> unguided29 | heldout_strategyqa | -0.5 | [-5.4, +4.3] | 10 / 11 | 1 |
| selfguided31 -> unguided29 | pooled | -2.9 | [-5.8, -0.1] | 50 / 72 | 0.0568 |
| selfguided31 -> unguided31 | heldout_2wikimultihopqa | -2.9 | [-8.8, +2.4] | 9 / 14 | 0.405 |
| selfguided31 -> unguided31 | heldout_hotpotqa | -6.9 | [-12.2, -1.6] | 7 / 20 | 0.0192 |
| selfguided31 -> unguided31 | heldout_musique | -7.9 | [-13.8, -2.5] | 10 / 26 | 0.0113 |
| selfguided31 -> unguided31 | heldout_strategyqa | +1.1 | [-3.2, +5.4] | 10 / 8 | 0.815 |
| selfguided31 -> unguided31 | pooled | -4.3 | [-7.0, -1.6] | 36 / 68 | 0.00221 |
| selfguided31 -> unguided37 | heldout_2wikimultihopqa | -0.6 | [-6.5, +5.3] | 12 / 13 | 1 |
| selfguided31 -> unguided37 | heldout_hotpotqa | -2.6 | [-7.4, +2.1] | 9 / 14 | 0.405 |
| selfguided31 -> unguided37 | heldout_musique | -4.9 | [-11.8, +2.0] | 21 / 31 | 0.212 |
| selfguided31 -> unguided37 | heldout_strategyqa | -1.6 | [-6.5, +3.2] | 9 / 12 | 0.664 |
| selfguided31 -> unguided37 | pooled | -2.5 | [-5.5, +0.3] | 51 / 70 | 0.101 |
| selfguided37 -> unguided13 | heldout_2wikimultihopqa | -2.4 | [-7.6, +2.9] | 9 / 13 | 0.523 |
| selfguided37 -> unguided13 | heldout_hotpotqa | -6.3 | [-11.6, -1.1] | 8 / 20 | 0.0357 |
| selfguided37 -> unguided13 | heldout_musique | -5.9 | [-13.3, +1.0] | 22 / 34 | 0.141 |
| selfguided37 -> unguided13 | heldout_strategyqa | +3.2 | [-1.1, +7.6] | 11 / 5 | 0.21 |
| selfguided37 -> unguided13 | pooled | -2.9 | [-5.8, -0.1] | 50 / 72 | 0.0568 |
| selfguided37 -> unguided17 | heldout_2wikimultihopqa | -2.9 | [-8.2, +2.4] | 8 / 13 | 0.383 |
| selfguided37 -> unguided17 | heldout_hotpotqa | -1.6 | [-6.9, +3.7] | 12 / 15 | 0.701 |
| selfguided37 -> unguided17 | heldout_musique | -1.5 | [-8.9, +5.9] | 27 / 30 | 0.791 |
| selfguided37 -> unguided17 | heldout_strategyqa | +4.3 | [+0.5, +8.6] | 12 / 4 | 0.0768 |
| selfguided37 -> unguided17 | pooled | -0.4 | [-3.4, +2.5] | 59 / 62 | 0.856 |
| selfguided37 -> unguided23 | heldout_2wikimultihopqa | -4.7 | [-10.6, +1.2] | 8 / 16 | 0.152 |
| selfguided37 -> unguided23 | heldout_hotpotqa | -2.1 | [-7.4, +3.2] | 11 / 15 | 0.557 |
| selfguided37 -> unguided23 | heldout_musique | -4.4 | [-11.8, +2.5] | 23 / 32 | 0.281 |
| selfguided37 -> unguided23 | heldout_strategyqa | +1.1 | [-3.2, +5.4] | 10 / 8 | 0.815 |
| selfguided37 -> unguided23 | pooled | -2.5 | [-5.3, +0.3] | 52 / 71 | 0.104 |
| selfguided37 -> unguided29 | heldout_2wikimultihopqa | -3.5 | [-8.8, +1.8] | 7 / 13 | 0.263 |
| selfguided37 -> unguided29 | heldout_hotpotqa | -6.3 | [-12.2, -1.1] | 9 / 21 | 0.0428 |
| selfguided37 -> unguided29 | heldout_musique | -3.0 | [-10.3, +4.4] | 27 / 33 | 0.519 |
| selfguided37 -> unguided29 | heldout_strategyqa | +0.0 | [-4.3, +4.3] | 9 / 9 | 1 |
| selfguided37 -> unguided29 | pooled | -3.2 | [-6.2, -0.3] | 52 / 76 | 0.0416 |
| selfguided37 -> unguided31 | heldout_2wikimultihopqa | -5.9 | [-10.6, -1.2] | 4 / 14 | 0.0309 |
| selfguided37 -> unguided31 | heldout_hotpotqa | -6.3 | [-11.1, -1.6] | 6 / 18 | 0.0227 |
| selfguided37 -> unguided31 | heldout_musique | -7.4 | [-14.3, -0.5] | 18 / 33 | 0.0489 |
| selfguided37 -> unguided31 | heldout_strategyqa | +1.6 | [-2.7, +5.4] | 9 / 6 | 0.607 |
| selfguided37 -> unguided31 | pooled | -4.5 | [-7.2, -1.9] | 37 / 71 | 0.00138 |
| selfguided37 -> unguided37 | heldout_2wikimultihopqa | -3.5 | [-8.8, +1.8] | 8 / 14 | 0.286 |
| selfguided37 -> unguided37 | heldout_hotpotqa | -2.1 | [-7.4, +3.2] | 12 / 16 | 0.572 |
| selfguided37 -> unguided37 | heldout_musique | -4.4 | [-11.8, +3.0] | 25 / 34 | 0.298 |
| selfguided37 -> unguided37 | heldout_strategyqa | -1.1 | [-5.4, +3.2] | 8 / 10 | 0.815 |
| selfguided37 -> unguided37 | pooled | -2.8 | [-5.8, +0.1] | 53 / 74 | 0.0755 |
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
| unguided13 -> unguided29 | heldout_2wikimultihopqa | -1.2 | [-5.9, +3.5] | 7 / 9 | 0.804 |
| unguided13 -> unguided29 | heldout_hotpotqa | +0.0 | [-4.8, +5.3] | 12 / 12 | 1 |
| unguided13 -> unguided29 | heldout_musique | +3.0 | [-3.0, +8.9] | 21 / 15 | 0.405 |
| unguided13 -> unguided29 | heldout_strategyqa | -3.2 | [-7.6, +1.1] | 5 / 11 | 0.21 |
| unguided13 -> unguided29 | pooled | -0.3 | [-2.7, +2.3] | 45 / 47 | 0.917 |
| unguided13 -> unguided31 | heldout_2wikimultihopqa | -3.5 | [-7.6, +0.6] | 4 / 10 | 0.18 |
| unguided13 -> unguided31 | heldout_hotpotqa | +0.0 | [-4.8, +4.8] | 10 / 10 | 1 |
| unguided13 -> unguided31 | heldout_musique | -1.5 | [-7.4, +4.4] | 16 / 19 | 0.736 |
| unguided13 -> unguided31 | heldout_strategyqa | -1.6 | [-5.4, +2.2] | 5 / 8 | 0.581 |
| unguided13 -> unguided31 | pooled | -1.6 | [-4.0, +0.8] | 35 / 47 | 0.224 |
| unguided13 -> unguided37 | heldout_2wikimultihopqa | -1.2 | [-6.5, +4.1] | 9 / 11 | 0.824 |
| unguided13 -> unguided37 | heldout_hotpotqa | +4.2 | [+0.0, +8.5] | 13 / 5 | 0.0963 |
| unguided13 -> unguided37 | heldout_musique | +1.5 | [-4.4, +7.4] | 19 / 16 | 0.736 |
| unguided13 -> unguided37 | heldout_strategyqa | -4.3 | [-8.6, -0.5] | 3 / 11 | 0.0574 |
| unguided13 -> unguided37 | pooled | +0.1 | [-2.3, +2.7] | 44 / 43 | 1 |
| unguided17 -> unguided23 | heldout_2wikimultihopqa | -1.8 | [-7.1, +3.5] | 10 / 13 | 0.678 |
| unguided17 -> unguided23 | heldout_hotpotqa | -0.5 | [-5.3, +4.2] | 10 / 11 | 1 |
| unguided17 -> unguided23 | heldout_musique | -3.0 | [-8.4, +2.5] | 13 / 19 | 0.377 |
| unguided17 -> unguided23 | heldout_strategyqa | -3.2 | [-7.0, +0.5] | 3 / 9 | 0.146 |
| unguided17 -> unguided23 | pooled | -2.1 | [-4.5, +0.3] | 36 / 52 | 0.109 |
| unguided17 -> unguided29 | heldout_2wikimultihopqa | -0.6 | [-5.9, +4.7] | 9 / 10 | 1 |
| unguided17 -> unguided29 | heldout_hotpotqa | -4.8 | [-10.1, +0.0] | 7 / 16 | 0.0931 |
| unguided17 -> unguided29 | heldout_musique | -1.5 | [-7.4, +4.4] | 17 / 20 | 0.743 |
| unguided17 -> unguided29 | heldout_strategyqa | -4.3 | [-8.6, -0.5] | 4 / 12 | 0.0768 |
| unguided17 -> unguided29 | pooled | -2.8 | [-5.3, -0.3] | 37 / 58 | 0.0396 |
| unguided17 -> unguided31 | heldout_2wikimultihopqa | -2.9 | [-8.2, +2.4] | 8 / 13 | 0.383 |
| unguided17 -> unguided31 | heldout_hotpotqa | -4.8 | [-9.5, -0.5] | 5 / 14 | 0.0636 |
| unguided17 -> unguided31 | heldout_musique | -5.9 | [-11.3, +0.0] | 12 / 24 | 0.0652 |
| unguided17 -> unguided31 | heldout_strategyqa | -2.7 | [-6.5, +1.1] | 4 / 9 | 0.267 |
| unguided17 -> unguided31 | pooled | -4.2 | [-6.6, -1.7] | 29 / 60 | 0.00134 |
| unguided17 -> unguided37 | heldout_2wikimultihopqa | -0.6 | [-5.9, +4.7] | 10 / 11 | 1 |
| unguided17 -> unguided37 | heldout_hotpotqa | -0.5 | [-5.3, +4.2] | 9 / 10 | 1 |
| unguided17 -> unguided37 | heldout_musique | -3.0 | [-9.8, +3.9] | 22 / 28 | 0.48 |
| unguided17 -> unguided37 | heldout_strategyqa | -5.4 | [-9.7, -1.6] | 3 / 13 | 0.0213 |
| unguided17 -> unguided37 | pooled | -2.4 | [-5.1, +0.3] | 44 / 62 | 0.0982 |
| unguided23 -> unguided29 | heldout_2wikimultihopqa | +1.2 | [-2.9, +5.3] | 8 / 6 | 0.791 |
| unguided23 -> unguided29 | heldout_hotpotqa | -4.2 | [-9.5, +0.5] | 8 / 16 | 0.152 |
| unguided23 -> unguided29 | heldout_musique | +1.5 | [-3.9, +7.4] | 19 / 16 | 0.736 |
| unguided23 -> unguided29 | heldout_strategyqa | -1.1 | [-4.3, +2.2] | 4 / 6 | 0.754 |
| unguided23 -> unguided29 | pooled | -0.7 | [-3.1, +1.7] | 39 / 44 | 0.661 |
| unguided23 -> unguided31 | heldout_2wikimultihopqa | -1.2 | [-6.5, +4.1] | 9 / 11 | 0.824 |
| unguided23 -> unguided31 | heldout_hotpotqa | -4.2 | [-9.0, +0.5] | 6 / 14 | 0.115 |
| unguided23 -> unguided31 | heldout_musique | -3.0 | [-8.9, +3.0] | 14 / 20 | 0.392 |
| unguided23 -> unguided31 | heldout_strategyqa | +0.5 | [-2.2, +3.2] | 4 / 3 | 1 |
| unguided23 -> unguided31 | pooled | -2.0 | [-4.4, +0.3] | 33 / 48 | 0.119 |
| unguided23 -> unguided37 | heldout_2wikimultihopqa | +1.2 | [-3.5, +5.9] | 9 / 7 | 0.804 |
| unguided23 -> unguided37 | heldout_hotpotqa | +0.0 | [-4.2, +4.2] | 8 / 8 | 1 |
| unguided23 -> unguided37 | heldout_musique | +0.0 | [-5.9, +5.9] | 18 / 18 | 1 |
| unguided23 -> unguided37 | heldout_strategyqa | -2.2 | [-6.5, +2.2] | 6 / 10 | 0.454 |
| unguided23 -> unguided37 | pooled | -0.3 | [-2.7, +2.0] | 41 / 43 | 0.913 |
| unguided29 -> unguided31 | heldout_2wikimultihopqa | -2.4 | [-7.1, +1.8] | 5 / 9 | 0.424 |
| unguided29 -> unguided31 | heldout_hotpotqa | +0.0 | [-4.2, +4.2] | 9 / 9 | 1 |
| unguided29 -> unguided31 | heldout_musique | -4.4 | [-9.8, +1.0] | 11 / 20 | 0.15 |
| unguided29 -> unguided31 | heldout_strategyqa | +1.6 | [-2.2, +5.4] | 8 / 5 | 0.581 |
| unguided29 -> unguided31 | pooled | -1.3 | [-3.6, +0.9] | 33 / 43 | 0.302 |
| unguided29 -> unguided37 | heldout_2wikimultihopqa | +0.0 | [-4.1, +4.1] | 6 / 6 | 1 |
| unguided29 -> unguided37 | heldout_hotpotqa | +4.2 | [+0.0, +8.5] | 13 / 5 | 0.0963 |
| unguided29 -> unguided37 | heldout_musique | -1.5 | [-7.4, +4.4] | 16 / 19 | 0.736 |
| unguided29 -> unguided37 | heldout_strategyqa | -1.1 | [-5.4, +3.2] | 7 / 9 | 0.804 |
| unguided29 -> unguided37 | pooled | +0.4 | [-2.0, +2.7] | 42 / 39 | 0.824 |
| unguided31 -> unguided37 | heldout_2wikimultihopqa | +2.4 | [-2.4, +7.6] | 11 / 7 | 0.481 |
| unguided31 -> unguided37 | heldout_hotpotqa | +4.2 | [+0.0, +8.5] | 13 / 5 | 0.0963 |
| unguided31 -> unguided37 | heldout_musique | +3.0 | [-3.0, +8.9] | 22 / 16 | 0.418 |
| unguided31 -> unguided37 | heldout_strategyqa | -2.7 | [-6.5, +1.6] | 5 / 10 | 0.302 |
| unguided31 -> unguided37 | pooled | +1.7 | [-0.8, +4.3] | 51 / 38 | 0.203 |
