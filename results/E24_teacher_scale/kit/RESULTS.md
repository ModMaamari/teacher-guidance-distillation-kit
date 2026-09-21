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
| teachdist13 | heldout_2wikimultihopqa | 170 | yes | 0.206 | 0.349 | 0.859 | 0.859 | 0.950 | 2.85 | 0.15 | 5,021 | 21.2 | 0.0000 |
| teachdist13 | heldout_hotpotqa | 189 | yes | 0.444 | 0.519 | 0.682 | 0.741 | 0.860 | 2.85 | 0.15 | 4,940 | 18.0 | 0.0000 |
| teachdist13 | heldout_musique | 203 | yes | 0.281 | 0.393 | 0.483 | 0.547 | 0.791 | 2.98 | 0.02 | 5,246 | 18.1 | 0.0000 |
| teachdist13 | heldout_strategyqa | 185 | yes | 0.000 | 0.042 | 0.762 | 0.751 | 0.867 | 2.91 | 0.09 | 4,967 | 22.8 | 0.0000 |
| teachdist17 | heldout_2wikimultihopqa | 170 | yes | 0.200 | 0.345 | 0.853 | 0.871 | 0.949 | 2.82 | 0.18 | 4,978 | 22.5 | 0.0000 |
| teachdist17 | heldout_hotpotqa | 189 | yes | 0.434 | 0.506 | 0.677 | 0.714 | 0.852 | 2.83 | 0.17 | 4,864 | 20.0 | 0.0000 |
| teachdist17 | heldout_musique | 203 | yes | 0.300 | 0.410 | 0.517 | 0.596 | 0.800 | 2.97 | 0.03 | 5,220 | 18.0 | 0.0000 |
| teachdist17 | heldout_strategyqa | 185 | yes | 0.000 | 0.040 | 0.735 | 0.735 | 0.867 | 2.91 | 0.09 | 4,989 | 22.4 | 0.0000 |
| teachdist23 | heldout_2wikimultihopqa | 170 | yes | 0.182 | 0.325 | 0.841 | 0.847 | 0.935 | 2.83 | 0.16 | 4,987 | 29.4 | 0.0000 |
| teachdist23 | heldout_hotpotqa | 189 | yes | 0.397 | 0.481 | 0.651 | 0.693 | 0.839 | 2.84 | 0.16 | 4,888 | 24.9 | 0.0000 |
| teachdist23 | heldout_musique | 203 | yes | 0.266 | 0.373 | 0.478 | 0.522 | 0.796 | 2.95 | 0.05 | 5,185 | 24.8 | 0.0000 |
| teachdist23 | heldout_strategyqa | 185 | yes | 0.005 | 0.047 | 0.746 | 0.735 | 0.857 | 2.92 | 0.08 | 4,972 | 28.4 | 0.0000 |

## Pooled per arm

| arm | test sets | n | EM | F1 | cover | judge | steps | tokens/ep | API $ |
|---|---|---|---|---|---|---|---|---|---|
| base | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.052 | 0.113 | 0.232 | 0.273 | 2.97 | 5,067 | 0.0000 |
| selfguided13 | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.099 | 0.206 | 0.632 | 0.667 | 2.90 | 5,159 | 0.0000 |
| selfguided17 | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.100 | 0.201 | 0.616 | 0.649 | 2.89 | 5,213 | 0.0000 |
| selfguided23 | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.088 | 0.193 | 0.606 | 0.632 | 2.87 | 5,155 | 0.0000 |
| teachdist13 | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.236 | 0.328 | 0.688 | 0.718 | 2.90 | 5,048 | 0.0000 |
| teachdist17 | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.237 | 0.328 | 0.688 | 0.723 | 2.88 | 5,018 | 0.0000 |
| teachdist23 | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.215 | 0.309 | 0.671 | 0.692 | 2.89 | 5,012 | 0.0000 |

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
| base -> teachdist13 | heldout_2wikimultihopqa | +50.6 | [+42.9, +58.2] | 86 / 0 | 0 |
| base -> teachdist13 | heldout_hotpotqa | +31.2 | [+23.3, +39.1] | 67 / 8 | 0 |
| base -> teachdist13 | heldout_musique | +37.4 | [+30.0, +44.8] | 83 / 7 | 0 |
| base -> teachdist13 | heldout_strategyqa | +60.0 | [+52.4, +67.6] | 114 / 3 | 0 |
| base -> teachdist13 | pooled | +44.4 | [+40.4, +48.3] | 350 / 18 | 0 |
| base -> teachdist17 | heldout_2wikimultihopqa | +51.8 | [+44.7, +59.4] | 88 / 0 | 0 |
| base -> teachdist17 | heldout_hotpotqa | +28.6 | [+21.2, +36.5] | 63 / 9 | 0 |
| base -> teachdist17 | heldout_musique | +42.4 | [+35.0, +49.8] | 90 / 4 | 0 |
| base -> teachdist17 | heldout_strategyqa | +58.4 | [+51.3, +65.4] | 109 / 1 | 0 |
| base -> teachdist17 | pooled | +45.0 | [+41.1, +48.9] | 350 / 14 | 0 |
| base -> teachdist23 | heldout_2wikimultihopqa | +49.4 | [+41.8, +57.1] | 85 / 1 | 0 |
| base -> teachdist23 | heldout_hotpotqa | +26.5 | [+18.5, +34.4] | 61 / 11 | 0 |
| base -> teachdist23 | heldout_musique | +35.0 | [+27.6, +42.4] | 77 / 6 | 0 |
| base -> teachdist23 | heldout_strategyqa | +58.4 | [+50.8, +66.0] | 111 / 3 | 0 |
| base -> teachdist23 | pooled | +41.9 | [+37.9, +45.8] | 334 / 21 | 0 |
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
| selfguided13 -> teachdist13 | heldout_2wikimultihopqa | +7.1 | [+0.6, +13.5] | 22 / 10 | 0.0501 |
| selfguided13 -> teachdist13 | heldout_hotpotqa | +5.3 | [-0.5, +11.6] | 23 / 13 | 0.132 |
| selfguided13 -> teachdist13 | heldout_musique | +5.4 | [-2.0, +12.8] | 36 / 25 | 0.2 |
| selfguided13 -> teachdist13 | heldout_strategyqa | +2.7 | [-3.8, +9.2] | 21 / 16 | 0.511 |
| selfguided13 -> teachdist13 | pooled | +5.1 | [+1.7, +8.4] | 102 / 64 | 0.00395 |
| selfguided13 -> teachdist17 | heldout_2wikimultihopqa | +8.2 | [+1.8, +14.7] | 23 / 9 | 0.0201 |
| selfguided13 -> teachdist17 | heldout_hotpotqa | +2.6 | [-3.2, +8.5] | 19 / 14 | 0.487 |
| selfguided13 -> teachdist17 | heldout_musique | +10.3 | [+3.5, +17.2] | 38 / 17 | 0.00646 |
| selfguided13 -> teachdist17 | heldout_strategyqa | +1.1 | [-4.9, +7.0] | 17 / 15 | 0.86 |
| selfguided13 -> teachdist17 | pooled | +5.6 | [+2.4, +8.8] | 97 / 55 | 0.000825 |
| selfguided13 -> teachdist23 | heldout_2wikimultihopqa | +5.9 | [+0.0, +11.8] | 19 / 9 | 0.0872 |
| selfguided13 -> teachdist23 | heldout_hotpotqa | +0.5 | [-5.8, +6.9] | 20 / 19 | 1 |
| selfguided13 -> teachdist23 | heldout_musique | +3.0 | [-3.9, +9.8] | 30 / 24 | 0.497 |
| selfguided13 -> teachdist23 | heldout_strategyqa | +1.1 | [-5.9, +8.1] | 22 / 20 | 0.878 |
| selfguided13 -> teachdist23 | pooled | +2.5 | [-0.8, +5.9] | 91 / 72 | 0.158 |
| selfguided17 -> selfguided23 | heldout_2wikimultihopqa | -4.1 | [-10.0, +1.8] | 9 / 16 | 0.23 |
| selfguided17 -> selfguided23 | heldout_hotpotqa | +0.0 | [-4.2, +4.2] | 8 / 8 | 1 |
| selfguided17 -> selfguided23 | heldout_musique | -0.5 | [-5.9, +4.9] | 16 / 17 | 1 |
| selfguided17 -> selfguided23 | heldout_strategyqa | -2.7 | [-7.0, +1.6] | 6 / 11 | 0.332 |
| selfguided17 -> selfguided23 | pooled | -1.7 | [-4.3, +0.7] | 39 / 52 | 0.208 |
| selfguided17 -> teachdist13 | heldout_2wikimultihopqa | +8.2 | [+1.2, +15.3] | 25 / 11 | 0.0288 |
| selfguided17 -> teachdist13 | heldout_hotpotqa | +7.4 | [+1.1, +13.8] | 25 / 11 | 0.0288 |
| selfguided17 -> teachdist13 | heldout_musique | +9.4 | [+2.5, +16.3] | 37 / 18 | 0.0145 |
| selfguided17 -> teachdist13 | heldout_strategyqa | +2.2 | [-3.8, +8.6] | 19 / 15 | 0.608 |
| selfguided17 -> teachdist13 | pooled | +6.8 | [+3.5, +10.2] | 106 / 55 | 7.1e-05 |
| selfguided17 -> teachdist17 | heldout_2wikimultihopqa | +9.4 | [+2.4, +16.5] | 26 / 10 | 0.0113 |
| selfguided17 -> teachdist17 | heldout_hotpotqa | +4.8 | [-0.5, +10.6] | 19 / 10 | 0.136 |
| selfguided17 -> teachdist17 | heldout_musique | +14.3 | [+7.4, +21.2] | 43 / 14 | 0.000154 |
| selfguided17 -> teachdist17 | heldout_strategyqa | +0.5 | [-5.4, +6.5] | 16 / 15 | 1 |
| selfguided17 -> teachdist17 | pooled | +7.4 | [+4.2, +10.6] | 104 / 49 | 1e-05 |
| selfguided17 -> teachdist23 | heldout_2wikimultihopqa | +7.1 | [+0.6, +13.5] | 21 / 9 | 0.0428 |
| selfguided17 -> teachdist23 | heldout_hotpotqa | +2.6 | [-3.2, +8.5] | 20 / 15 | 0.5 |
| selfguided17 -> teachdist23 | heldout_musique | +6.9 | [+0.0, +13.8] | 33 / 19 | 0.0704 |
| selfguided17 -> teachdist23 | heldout_strategyqa | +0.5 | [-5.9, +7.0] | 20 / 19 | 1 |
| selfguided17 -> teachdist23 | pooled | +4.3 | [+1.1, +7.6] | 94 / 62 | 0.0128 |
| selfguided23 -> teachdist13 | heldout_2wikimultihopqa | +12.3 | [+5.9, +18.8] | 27 / 6 | 0.000324 |
| selfguided23 -> teachdist13 | heldout_hotpotqa | +7.4 | [+1.1, +13.8] | 26 / 12 | 0.0336 |
| selfguided23 -> teachdist13 | heldout_musique | +9.8 | [+3.0, +17.2] | 38 / 18 | 0.0105 |
| selfguided23 -> teachdist13 | heldout_strategyqa | +4.9 | [-1.6, +11.9] | 25 / 16 | 0.211 |
| selfguided23 -> teachdist13 | pooled | +8.6 | [+5.2, +11.9] | 116 / 52 | 1e-06 |
| selfguided23 -> teachdist17 | heldout_2wikimultihopqa | +13.5 | [+7.1, +20.0] | 28 / 5 | 6.6e-05 |
| selfguided23 -> teachdist17 | heldout_hotpotqa | +4.8 | [-0.5, +10.1] | 19 / 10 | 0.136 |
| selfguided23 -> teachdist17 | heldout_musique | +14.8 | [+7.9, +21.7] | 42 / 12 | 5.2e-05 |
| selfguided23 -> teachdist17 | heldout_strategyqa | +3.2 | [-2.7, +9.7] | 21 / 15 | 0.405 |
| selfguided23 -> teachdist17 | pooled | +9.1 | [+5.9, +12.3] | 110 / 42 | 0 |
| selfguided23 -> teachdist23 | heldout_2wikimultihopqa | +11.2 | [+4.7, +17.6] | 25 / 6 | 0.000878 |
| selfguided23 -> teachdist23 | heldout_hotpotqa | +2.6 | [-3.2, +8.5] | 20 / 15 | 0.5 |
| selfguided23 -> teachdist23 | heldout_musique | +7.4 | [+1.0, +13.8] | 30 / 15 | 0.0357 |
| selfguided23 -> teachdist23 | heldout_strategyqa | +3.2 | [-3.8, +10.3] | 26 / 20 | 0.461 |
| selfguided23 -> teachdist23 | pooled | +6.0 | [+2.8, +9.2] | 101 / 56 | 0.00041 |
| teachdist13 -> teachdist17 | heldout_2wikimultihopqa | +1.2 | [-1.8, +4.1] | 4 / 2 | 0.688 |
| teachdist13 -> teachdist17 | heldout_hotpotqa | -2.6 | [-7.4, +2.1] | 7 / 12 | 0.359 |
| teachdist13 -> teachdist17 | heldout_musique | +4.9 | [-0.5, +10.3] | 20 / 10 | 0.0987 |
| teachdist13 -> teachdist17 | heldout_strategyqa | -1.6 | [-7.0, +3.8] | 11 / 14 | 0.69 |
| teachdist13 -> teachdist17 | pooled | +0.5 | [-1.9, +2.9] | 42 / 38 | 0.738 |
| teachdist13 -> teachdist23 | heldout_2wikimultihopqa | -1.2 | [-4.7, +2.4] | 4 / 6 | 0.754 |
| teachdist13 -> teachdist23 | heldout_hotpotqa | -4.8 | [-10.1, +0.5] | 9 / 18 | 0.122 |
| teachdist13 -> teachdist23 | heldout_musique | -2.5 | [-7.4, +2.5] | 11 / 16 | 0.442 |
| teachdist13 -> teachdist23 | heldout_strategyqa | -1.6 | [-7.6, +4.3] | 15 / 18 | 0.728 |
| teachdist13 -> teachdist23 | pooled | -2.5 | [-5.1, +0.0] | 39 / 58 | 0.0671 |
| teachdist17 -> teachdist23 | heldout_2wikimultihopqa | -2.4 | [-6.5, +1.8] | 4 / 8 | 0.388 |
| teachdist17 -> teachdist23 | heldout_hotpotqa | -2.1 | [-6.9, +2.6] | 8 / 12 | 0.503 |
| teachdist17 -> teachdist23 | heldout_musique | -7.4 | [-12.8, -2.0] | 9 / 24 | 0.0135 |
| teachdist17 -> teachdist23 | heldout_strategyqa | +0.0 | [-5.4, +5.4] | 13 / 13 | 1 |
| teachdist17 -> teachdist23 | pooled | -3.1 | [-5.6, -0.5] | 34 / 57 | 0.0206 |
