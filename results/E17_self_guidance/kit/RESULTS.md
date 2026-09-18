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
| selfguided | heldout_2wikimultihopqa | 170 | yes | 0.076 | 0.230 | 0.806 | 0.794 | 0.862 | 2.92 | 0.08 | 5,320 | 41.6 | 0.0000 |
| selfguided | heldout_hotpotqa | 189 | yes | 0.254 | 0.345 | 0.661 | 0.677 | 0.807 | 2.82 | 0.18 | 5,131 | 39.4 | 0.0000 |
| selfguided | heldout_musique | 203 | yes | 0.059 | 0.187 | 0.389 | 0.438 | 0.649 | 2.95 | 0.05 | 5,387 | 41.6 | 0.0000 |
| selfguided | heldout_strategyqa | 185 | yes | 0.000 | 0.034 | 0.659 | 0.708 | 0.829 | 2.96 | 0.04 | 5,347 | 43.8 | 0.0000 |
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
| selfguided | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.098 | 0.199 | 0.620 | 0.647 | 2.91 | 5,297 | 0.0000 |
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
| base -> selfguided | heldout_2wikimultihopqa | +44.1 | [+36.5, +51.8] | 78 / 3 | 0 |
| base -> selfguided | heldout_hotpotqa | +24.9 | [+18.0, +32.3] | 53 / 6 | 0 |
| base -> selfguided | heldout_musique | +26.6 | [+19.7, +34.0] | 63 / 9 | 0 |
| base -> selfguided | heldout_strategyqa | +55.7 | [+48.1, +63.2] | 105 / 2 | 0 |
| base -> selfguided | pooled | +37.4 | [+33.5, +41.2] | 299 / 20 | 0 |
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
| guided -> selfguided | heldout_2wikimultihopqa | +0.6 | [-5.3, +6.5] | 14 / 13 | 1 |
| guided -> selfguided | heldout_hotpotqa | +3.7 | [-2.1, +9.5] | 20 / 13 | 0.296 |
| guided -> selfguided | heldout_musique | +3.9 | [-2.5, +10.3] | 26 / 18 | 0.291 |
| guided -> selfguided | heldout_strategyqa | +1.1 | [-4.9, +7.0] | 18 / 16 | 0.864 |
| guided -> selfguided | pooled | +2.4 | [-0.8, +5.5] | 78 / 60 | 0.148 |
| guided -> teachdist | heldout_2wikimultihopqa | +7.1 | [+1.8, +12.3] | 17 / 5 | 0.0169 |
| guided -> teachdist | heldout_hotpotqa | +4.2 | [-1.6, +10.1] | 20 / 12 | 0.215 |
| guided -> teachdist | heldout_musique | +9.8 | [+2.5, +17.2] | 40 / 20 | 0.0135 |
| guided -> teachdist | heldout_strategyqa | +0.5 | [-5.9, +7.0] | 19 / 18 | 1 |
| guided -> teachdist | pooled | +5.5 | [+2.3, +8.8] | 96 / 55 | 0.00106 |
| selfdist -> selfguided | heldout_2wikimultihopqa | +3.5 | [-2.4, +10.0] | 17 / 11 | 0.345 |
| selfdist -> selfguided | heldout_hotpotqa | +3.2 | [-2.1, +8.5] | 16 / 10 | 0.327 |
| selfdist -> selfguided | heldout_musique | +3.9 | [-2.5, +10.3] | 26 / 18 | 0.291 |
| selfdist -> selfguided | heldout_strategyqa | +2.2 | [-2.2, +6.5] | 10 / 6 | 0.454 |
| selfdist -> selfguided | pooled | +3.2 | [+0.4, +6.0] | 69 / 45 | 0.0308 |
| selfdist -> teachdist | heldout_2wikimultihopqa | +10.0 | [+3.5, +16.5] | 24 / 7 | 0.00333 |
| selfdist -> teachdist | heldout_hotpotqa | +3.7 | [-2.6, +10.1] | 24 / 17 | 0.349 |
| selfdist -> teachdist | heldout_musique | +9.8 | [+2.5, +17.2] | 42 / 22 | 0.0169 |
| selfdist -> teachdist | heldout_strategyqa | +1.6 | [-4.3, +8.1] | 19 / 16 | 0.736 |
| selfdist -> teachdist | pooled | +6.3 | [+2.9, +9.6] | 109 / 62 | 0.000404 |
| selfguided -> teachdist | heldout_2wikimultihopqa | +6.5 | [+0.6, +12.3] | 18 / 7 | 0.0433 |
| selfguided -> teachdist | heldout_hotpotqa | +0.5 | [-5.8, +6.9] | 20 / 19 | 1 |
| selfguided -> teachdist | heldout_musique | +5.9 | [-1.0, +12.8] | 33 / 21 | 0.134 |
| selfguided -> teachdist | heldout_strategyqa | -0.5 | [-6.5, +5.4] | 16 / 17 | 1 |
| selfguided -> teachdist | pooled | +3.1 | [-0.1, +6.3] | 87 / 64 | 0.073 |
