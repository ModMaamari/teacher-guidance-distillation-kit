# Results

## Per arm and test set

| arm | test set | n | done | EM | F1 | cover | judge | doc recall | steps | vol. finish | tokens/ep | latency s | API $ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| base | heldout_2wikimultihopqa | 170 | yes | 0.018 | 0.120 | 0.306 | 0.353 | 0.810 | 2.98 | 0.02 | 5,182 | 25.5 | 0.0000 |
| base | heldout_hotpotqa | 189 | yes | 0.169 | 0.240 | 0.381 | 0.429 | 0.759 | 2.91 | 0.09 | 5,120 | 20.1 | 0.0000 |
| base | heldout_musique | 203 | yes | 0.020 | 0.084 | 0.153 | 0.172 | 0.597 | 3.00 | 0.00 | 5,052 | 17.5 | 0.0000 |
| base | heldout_strategyqa | 185 | yes | 0.000 | 0.011 | 0.097 | 0.151 | 0.815 | 2.98 | 0.02 | 4,923 | 17.0 | 0.0000 |
| guided_full | heldout_2wikimultihopqa | 170 | yes | 0.429 | 0.543 | 0.765 | 0.765 | 0.854 | 2.93 | 0.07 | 5,655 | 24.3 | 0.0000 |
| guided_full | heldout_hotpotqa | 189 | yes | 0.339 | 0.425 | 0.587 | 0.635 | 0.786 | 2.83 | 0.17 | 5,249 | 22.6 | 0.0000 |
| guided_full | heldout_musique | 203 | yes | 0.163 | 0.287 | 0.350 | 0.389 | 0.663 | 2.99 | 0.01 | 5,253 | 20.8 | 0.0000 |
| guided_full | heldout_strategyqa | 185 | yes | 0.508 | 0.529 | 0.724 | 0.730 | 0.826 | 2.92 | 0.08 | 5,214 | 23.2 | 0.0000 |
| selfdist_full | heldout_2wikimultihopqa | 170 | yes | 0.047 | 0.198 | 0.747 | 0.765 | 0.828 | 2.97 | 0.03 | 5,053 | 38.9 | 0.0000 |
| selfdist_full | heldout_hotpotqa | 189 | yes | 0.243 | 0.329 | 0.598 | 0.614 | 0.767 | 2.85 | 0.15 | 4,880 | 36.2 | 0.0000 |
| selfdist_full | heldout_musique | 203 | yes | 0.044 | 0.173 | 0.374 | 0.409 | 0.605 | 2.97 | 0.03 | 4,750 | 36.1 | 0.0000 |
| selfdist_full | heldout_strategyqa | 185 | yes | 0.000 | 0.036 | 0.670 | 0.735 | 0.812 | 2.95 | 0.05 | 4,782 | 40.1 | 0.0000 |
| selfguided_full | heldout_2wikimultihopqa | 170 | yes | 0.053 | 0.207 | 0.782 | 0.788 | 0.860 | 2.93 | 0.07 | 5,316 | 18.4 | 0.0000 |
| selfguided_full | heldout_hotpotqa | 189 | yes | 0.270 | 0.373 | 0.661 | 0.688 | 0.783 | 2.78 | 0.22 | 4,936 | 17.9 | 0.0000 |
| selfguided_full | heldout_musique | 203 | yes | 0.069 | 0.206 | 0.429 | 0.493 | 0.679 | 2.93 | 0.07 | 5,233 | 18.6 | 0.0000 |
| selfguided_full | heldout_strategyqa | 185 | yes | 0.000 | 0.034 | 0.686 | 0.724 | 0.834 | 2.95 | 0.05 | 5,161 | 19.9 | 0.0000 |

## Pooled per arm

| arm | test sets | n | EM | F1 | cover | judge | steps | tokens/ep | API $ |
|---|---|---|---|---|---|---|---|---|---|
| base | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.052 | 0.113 | 0.232 | 0.273 | 2.97 | 5,067 | 0.0000 |
| guided_full | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.353 | 0.440 | 0.597 | 0.621 | 2.92 | 5,334 | 0.0000 |
| selfdist_full | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.084 | 0.184 | 0.589 | 0.623 | 2.93 | 4,860 | 0.0000 |
| selfguided_full | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.099 | 0.206 | 0.632 | 0.667 | 2.90 | 5,159 | 0.0000 |

## Paired comparisons (judge-correct, b − a)

| a -> b | scope | Δ pts | 95% CI | b wins / a wins | McNemar p |
|---|---|---|---|---|---|
| base -> guided_full | heldout_2wikimultihopqa | +41.2 | [+32.9, +48.8] | 73 / 3 | 0 |
| base -> guided_full | heldout_hotpotqa | +20.6 | [+13.2, +28.0] | 51 / 12 | 1e-06 |
| base -> guided_full | heldout_musique | +21.7 | [+14.3, +29.1] | 57 / 13 | 0 |
| base -> guided_full | heldout_strategyqa | +57.8 | [+50.3, +65.4] | 108 / 1 | 0 |
| base -> guided_full | pooled | +34.8 | [+30.8, +38.7] | 289 / 29 | 0 |
| base -> selfdist_full | heldout_2wikimultihopqa | +41.2 | [+32.9, +49.4] | 75 / 5 | 0 |
| base -> selfdist_full | heldout_hotpotqa | +18.5 | [+11.1, +25.9] | 45 / 10 | 2e-06 |
| base -> selfdist_full | heldout_musique | +23.6 | [+16.8, +30.5] | 55 / 7 | 0 |
| base -> selfdist_full | heldout_strategyqa | +58.4 | [+51.3, +66.0] | 108 / 0 | 0 |
| base -> selfdist_full | pooled | +34.9 | [+31.1, +38.8] | 283 / 22 | 0 |
| base -> selfguided_full | heldout_2wikimultihopqa | +43.5 | [+35.3, +51.8] | 79 / 5 | 0 |
| base -> selfguided_full | heldout_hotpotqa | +25.9 | [+18.5, +33.3] | 57 / 8 | 0 |
| base -> selfguided_full | heldout_musique | +32.0 | [+24.6, +39.9] | 74 / 9 | 0 |
| base -> selfguided_full | heldout_strategyqa | +57.3 | [+49.7, +64.3] | 108 / 2 | 0 |
| base -> selfguided_full | pooled | +39.4 | [+35.5, +43.4] | 318 / 24 | 0 |
| guided_full -> selfdist_full | heldout_2wikimultihopqa | +0.0 | [-5.9, +5.9] | 13 / 13 | 1 |
| guided_full -> selfdist_full | heldout_hotpotqa | -2.1 | [-7.4, +2.6] | 10 / 14 | 0.541 |
| guided_full -> selfdist_full | heldout_musique | +2.0 | [-5.4, +9.8] | 33 / 29 | 0.704 |
| guided_full -> selfdist_full | heldout_strategyqa | +0.5 | [-4.9, +5.9] | 14 / 13 | 1 |
| guided_full -> selfdist_full | pooled | +0.1 | [-2.9, +3.2] | 70 / 69 | 1 |
| guided_full -> selfguided_full | heldout_2wikimultihopqa | +2.4 | [-2.9, +7.6] | 13 / 9 | 0.523 |
| guided_full -> selfguided_full | heldout_hotpotqa | +5.3 | [-1.1, +11.6] | 25 / 15 | 0.154 |
| guided_full -> selfguided_full | heldout_musique | +10.3 | [+2.5, +18.7] | 47 / 26 | 0.0186 |
| guided_full -> selfguided_full | heldout_strategyqa | -0.5 | [-6.5, +5.4] | 14 / 15 | 1 |
| guided_full -> selfguided_full | pooled | +4.5 | [+1.2, +7.9] | 99 / 65 | 0.00976 |
| selfdist_full -> selfguided_full | heldout_2wikimultihopqa | +2.4 | [-2.9, +7.6] | 13 / 9 | 0.523 |
| selfdist_full -> selfguided_full | heldout_hotpotqa | +7.4 | [+2.1, +13.2] | 22 / 8 | 0.0161 |
| selfdist_full -> selfguided_full | heldout_musique | +8.4 | [+2.0, +14.8] | 31 / 14 | 0.0161 |
| selfdist_full -> selfguided_full | heldout_strategyqa | -1.1 | [-5.4, +3.2] | 8 / 10 | 0.815 |
| selfdist_full -> selfguided_full | pooled | +4.4 | [+1.7, +7.2] | 74 / 41 | 0.00269 |
