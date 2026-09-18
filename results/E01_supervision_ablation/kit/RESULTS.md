# Results

## Per arm and test set

| arm | test set | n | done | EM | F1 | cover | judge | doc recall | steps | vol. finish | tokens/ep | latency s | API $ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| base | heldout_2wikimultihopqa | 170 | yes | 0.018 | 0.120 | 0.306 | 0.353 | 0.810 | 2.98 | 0.02 | 5,182 | 25.5 | 0.0000 |
| base | heldout_hotpotqa | 189 | yes | 0.169 | 0.240 | 0.381 | 0.429 | 0.759 | 2.91 | 0.09 | 5,120 | 20.1 | 0.0000 |
| base | heldout_musique | 203 | yes | 0.020 | 0.084 | 0.153 | 0.172 | 0.597 | 3.00 | 0.00 | 5,052 | 17.5 | 0.0000 |
| base | heldout_strategyqa | 185 | yes | 0.000 | 0.011 | 0.097 | 0.151 | 0.815 | 2.98 | 0.02 | 4,923 | 17.0 | 0.0000 |
| guided | heldout_2wikimultihopqa | 170 | yes | 0.312 | 0.479 | 0.782 | 0.788 | 0.884 | 2.92 | 0.08 | 5,689 | 19.6 | 0.0000 |
| guided | heldout_hotpotqa | 189 | yes | 0.328 | 0.421 | 0.587 | 0.640 | 0.791 | 2.87 | 0.13 | 5,324 | 15.6 | 0.0000 |
| guided | heldout_musique | 203 | yes | 0.168 | 0.272 | 0.360 | 0.399 | 0.654 | 2.94 | 0.05 | 5,239 | 16.7 | 0.0000 |
| guided | heldout_strategyqa | 185 | yes | 0.486 | 0.507 | 0.697 | 0.697 | 0.810 | 2.89 | 0.11 | 5,150 | 17.2 | 0.0000 |
| selfdist | heldout_2wikimultihopqa | 170 | yes | 0.047 | 0.196 | 0.747 | 0.759 | 0.818 | 2.97 | 0.03 | 5,042 | 16.1 | 0.0000 |
| selfdist | heldout_hotpotqa | 189 | yes | 0.249 | 0.337 | 0.635 | 0.645 | 0.767 | 2.87 | 0.13 | 4,916 | 14.8 | 0.0000 |
| selfdist | heldout_musique | 203 | yes | 0.035 | 0.163 | 0.364 | 0.399 | 0.610 | 2.96 | 0.04 | 4,715 | 14.8 | 0.0000 |
| selfdist | heldout_strategyqa | 185 | yes | 0.000 | 0.035 | 0.638 | 0.686 | 0.822 | 2.97 | 0.02 | 4,835 | 16.4 | 0.0000 |
| teachdist | heldout_2wikimultihopqa | 170 | yes | 0.212 | 0.346 | 0.841 | 0.859 | 0.918 | 2.83 | 0.17 | 4,968 | 27.1 | 0.0000 |
| teachdist | heldout_hotpotqa | 189 | yes | 0.407 | 0.467 | 0.635 | 0.682 | 0.852 | 2.95 | 0.05 | 5,138 | 22.2 | 0.0000 |
| teachdist | heldout_musique | 203 | yes | 0.266 | 0.371 | 0.453 | 0.497 | 0.782 | 2.96 | 0.04 | 5,208 | 23.1 | 0.0000 |
| teachdist | heldout_strategyqa | 185 | yes | 0.000 | 0.037 | 0.708 | 0.703 | 0.854 | 2.94 | 0.06 | 4,982 | 26.7 | 0.0000 |

## Pooled per arm

| arm | test sets | n | EM | F1 | cover | judge | steps | tokens/ep | API $ |
|---|---|---|---|---|---|---|---|---|---|
| base | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.052 | 0.113 | 0.232 | 0.273 | 2.97 | 5,067 | 0.0000 |
| guided | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.320 | 0.415 | 0.597 | 0.623 | 2.91 | 5,341 | 0.0000 |
| selfdist | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.083 | 0.183 | 0.588 | 0.615 | 2.94 | 4,870 | 0.0000 |
| teachdist | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.224 | 0.307 | 0.651 | 0.677 | 2.92 | 5,080 | 0.0000 |

## Paired comparisons (judge-correct, b − a)

| a -> b | scope | Δ pts | 95% CI | b wins / a wins | McNemar p |
|---|---|---|---|---|---|
| base -> guided | heldout_2wikimultihopqa | +43.5 | [+35.3, +51.2] | 77 / 3 | 0 |
| base -> guided | heldout_hotpotqa | +21.2 | [+14.3, +28.6] | 48 / 8 | 0 |
| base -> guided | heldout_musique | +22.7 | [+15.8, +29.6] | 55 / 9 | 0 |
| base -> guided | heldout_strategyqa | +54.6 | [+47.0, +62.2] | 103 / 2 | 0 |
| base -> guided | pooled | +34.9 | [+31.1, +38.8] | 283 / 22 | 0 |
| base -> selfdist | heldout_2wikimultihopqa | +40.6 | [+32.4, +48.8] | 74 / 5 | 0 |
| base -> selfdist | heldout_hotpotqa | +21.7 | [+14.8, +29.1] | 48 / 7 | 0 |
| base -> selfdist | heldout_musique | +22.7 | [+15.8, +29.6] | 54 / 8 | 0 |
| base -> selfdist | heldout_strategyqa | +53.5 | [+46.0, +61.1] | 100 / 1 | 0 |
| base -> selfdist | pooled | +34.1 | [+30.4, +38.0] | 276 / 21 | 0 |
| base -> teachdist | heldout_2wikimultihopqa | +50.6 | [+42.9, +58.2] | 86 / 0 | 0 |
| base -> teachdist | heldout_hotpotqa | +25.4 | [+17.5, +33.3] | 60 / 12 | 0 |
| base -> teachdist | heldout_musique | +32.5 | [+25.1, +39.9] | 75 / 9 | 0 |
| base -> teachdist | heldout_strategyqa | +55.1 | [+48.1, +62.7] | 103 / 1 | 0 |
| base -> teachdist | pooled | +40.4 | [+36.4, +44.3] | 324 / 22 | 0 |
| guided -> selfdist | heldout_2wikimultihopqa | -2.9 | [-8.8, +2.9] | 11 / 16 | 0.442 |
| guided -> selfdist | heldout_hotpotqa | +0.5 | [-4.8, +6.3] | 15 / 14 | 1 |
| guided -> selfdist | heldout_musique | +0.0 | [-6.9, +6.9] | 25 / 25 | 1 |
| guided -> selfdist | heldout_strategyqa | -1.1 | [-7.0, +4.9] | 16 / 18 | 0.864 |
| guided -> selfdist | pooled | -0.8 | [-3.9, +2.4] | 67 / 73 | 0.673 |
| guided -> teachdist | heldout_2wikimultihopqa | +7.1 | [+1.8, +12.3] | 17 / 5 | 0.0169 |
| guided -> teachdist | heldout_hotpotqa | +4.2 | [-1.6, +10.1] | 20 / 12 | 0.215 |
| guided -> teachdist | heldout_musique | +9.8 | [+2.5, +17.2] | 40 / 20 | 0.0135 |
| guided -> teachdist | heldout_strategyqa | +0.5 | [-5.9, +7.0] | 19 / 18 | 1 |
| guided -> teachdist | pooled | +5.5 | [+2.3, +8.8] | 96 / 55 | 0.00106 |
| selfdist -> teachdist | heldout_2wikimultihopqa | +10.0 | [+3.5, +16.5] | 24 / 7 | 0.00333 |
| selfdist -> teachdist | heldout_hotpotqa | +3.7 | [-2.6, +10.1] | 24 / 17 | 0.349 |
| selfdist -> teachdist | heldout_musique | +9.8 | [+2.5, +17.2] | 42 / 22 | 0.0169 |
| selfdist -> teachdist | heldout_strategyqa | +1.6 | [-4.3, +8.1] | 19 / 16 | 0.736 |
| selfdist -> teachdist | pooled | +6.3 | [+2.9, +9.6] | 109 / 62 | 0.000404 |
