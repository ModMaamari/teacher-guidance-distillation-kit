# Results

## Per arm and test set

| arm | test set | n | done | EM | F1 | cover | judge | doc recall | steps | vol. finish | tokens/ep | latency s | API $ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| granite_base | heldout_2wikimultihopqa | 170 | yes | 0.018 | 0.120 | 0.306 | 0.353 | 0.810 | 2.98 | 0.02 | 5,182 | 25.5 | 0.0000 |
| granite_base | heldout_hotpotqa | 189 | yes | 0.169 | 0.240 | 0.381 | 0.429 | 0.759 | 2.91 | 0.09 | 5,120 | 20.1 | 0.0000 |
| granite_base | heldout_musique | 203 | yes | 0.020 | 0.084 | 0.153 | 0.172 | 0.597 | 3.00 | 0.00 | 5,052 | 17.5 | 0.0000 |
| granite_base | heldout_strategyqa | 185 | yes | 0.000 | 0.011 | 0.097 | 0.151 | 0.815 | 2.98 | 0.02 | 4,923 | 17.0 | 0.0000 |
| granite_trained | heldout_2wikimultihopqa | 170 | yes | 0.429 | 0.543 | 0.765 | 0.765 | 0.854 | 2.93 | 0.07 | 5,655 | 24.3 | 0.0000 |
| granite_trained | heldout_hotpotqa | 189 | yes | 0.339 | 0.425 | 0.587 | 0.635 | 0.786 | 2.83 | 0.17 | 5,249 | 22.6 | 0.0000 |
| granite_trained | heldout_musique | 203 | yes | 0.163 | 0.287 | 0.350 | 0.389 | 0.663 | 2.99 | 0.01 | 5,253 | 20.8 | 0.0000 |
| granite_trained | heldout_strategyqa | 185 | yes | 0.508 | 0.529 | 0.724 | 0.730 | 0.826 | 2.92 | 0.08 | 5,214 | 23.2 | 0.0000 |
| minicpm_base | heldout_2wikimultihopqa | 170 | yes | 0.029 | 0.037 | 0.047 | 0.047 | 0.934 | 2.96 | 0.04 | 8,262 | 40.7 | 0.0000 |
| minicpm_base | heldout_hotpotqa | 189 | yes | 0.037 | 0.038 | 0.042 | 0.042 | 0.823 | 2.96 | 0.04 | 8,917 | 42.9 | 0.0000 |
| minicpm_base | heldout_musique | 203 | yes | 0.000 | 0.000 | 0.000 | 0.000 | 0.744 | 3.00 | 0.00 | 8,570 | 32.0 | 0.0000 |
| minicpm_base | heldout_strategyqa | 185 | yes | 0.005 | 0.006 | 0.011 | 0.011 | 0.834 | 3.00 | 0.01 | 8,525 | 25.4 | 0.0000 |
| minicpm_trained | heldout_2wikimultihopqa | 170 | yes | 0.341 | 0.483 | 0.782 | 0.812 | 0.906 | 2.91 | 0.09 | 5,703 | 16.6 | 0.0000 |
| minicpm_trained | heldout_hotpotqa | 189 | yes | 0.360 | 0.462 | 0.598 | 0.661 | 0.786 | 2.87 | 0.13 | 5,382 | 16.1 | 0.0000 |
| minicpm_trained | heldout_musique | 203 | yes | 0.227 | 0.332 | 0.379 | 0.429 | 0.703 | 2.96 | 0.04 | 5,309 | 14.5 | 0.0000 |
| minicpm_trained | heldout_strategyqa | 185 | yes | 0.557 | 0.573 | 0.714 | 0.719 | 0.804 | 2.93 | 0.07 | 5,286 | 16.7 | 0.0000 |

## Pooled per arm

| arm | test sets | n | EM | F1 | cover | judge | steps | tokens/ep | API $ |
|---|---|---|---|---|---|---|---|---|---|
| granite_base | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.052 | 0.113 | 0.232 | 0.273 | 2.97 | 5,067 | 0.0000 |
| granite_trained | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.353 | 0.440 | 0.597 | 0.621 | 2.92 | 5,334 | 0.0000 |
| minicpm_base | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.017 | 0.019 | 0.024 | 0.024 | 2.98 | 8,576 | 0.0000 |
| minicpm_trained | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.368 | 0.459 | 0.609 | 0.647 | 2.92 | 5,412 | 0.0000 |

## Paired comparisons (judge-correct, b − a)

| a -> b | scope | Δ pts | 95% CI | b wins / a wins | McNemar p |
|---|---|---|---|---|---|
| granite_base -> granite_trained | heldout_2wikimultihopqa | +41.2 | [+32.9, +48.8] | 73 / 3 | 0 |
| granite_base -> granite_trained | heldout_hotpotqa | +20.6 | [+13.2, +28.0] | 51 / 12 | 1e-06 |
| granite_base -> granite_trained | heldout_musique | +21.7 | [+14.3, +29.1] | 57 / 13 | 0 |
| granite_base -> granite_trained | heldout_strategyqa | +57.8 | [+50.3, +65.4] | 108 / 1 | 0 |
| granite_base -> granite_trained | pooled | +34.8 | [+30.8, +38.7] | 289 / 29 | 0 |
| granite_base -> minicpm_base | heldout_2wikimultihopqa | -30.6 | [-38.2, -23.5] | 3 / 55 | 0 |
| granite_base -> minicpm_base | heldout_hotpotqa | -38.6 | [-46.0, -31.2] | 2 / 75 | 0 |
| granite_base -> minicpm_base | heldout_musique | -17.2 | [-22.7, -12.3] | 0 / 35 | 0 |
| granite_base -> minicpm_base | heldout_strategyqa | -14.1 | [-19.5, -8.6] | 1 / 27 | 0 |
| granite_base -> minicpm_base | pooled | -24.9 | [-28.1, -21.7] | 6 / 192 | 0 |
| granite_base -> minicpm_trained | heldout_2wikimultihopqa | +45.9 | [+37.6, +54.1] | 83 / 5 | 0 |
| granite_base -> minicpm_trained | heldout_hotpotqa | +23.3 | [+15.9, +30.7] | 53 / 9 | 0 |
| granite_base -> minicpm_trained | heldout_musique | +25.6 | [+18.2, +33.0] | 63 / 11 | 0 |
| granite_base -> minicpm_trained | heldout_strategyqa | +56.8 | [+49.2, +64.3] | 107 / 2 | 0 |
| granite_base -> minicpm_trained | pooled | +37.4 | [+33.3, +41.2] | 306 / 27 | 0 |
| granite_trained -> minicpm_base | heldout_2wikimultihopqa | -71.8 | [-78.8, -64.7] | 1 / 123 | 0 |
| granite_trained -> minicpm_base | heldout_hotpotqa | -59.3 | [-66.7, -51.8] | 1 / 113 | 0 |
| granite_trained -> minicpm_base | heldout_musique | -38.9 | [-45.3, -32.5] | 0 / 79 | 0 |
| granite_trained -> minicpm_base | heldout_strategyqa | -71.9 | [-78.4, -65.4] | 0 / 133 | 0 |
| granite_trained -> minicpm_base | pooled | -59.7 | [-63.2, -56.1] | 2 / 448 | 0 |
| granite_trained -> minicpm_trained | heldout_2wikimultihopqa | +4.7 | [-1.8, +11.2] | 19 / 11 | 0.2 |
| granite_trained -> minicpm_trained | heldout_hotpotqa | +2.6 | [-3.7, +9.0] | 23 / 18 | 0.533 |
| granite_trained -> minicpm_trained | heldout_musique | +3.9 | [-3.5, +11.3] | 35 / 27 | 0.374 |
| granite_trained -> minicpm_trained | heldout_strategyqa | -1.1 | [-7.6, +5.4] | 17 / 19 | 0.868 |
| granite_trained -> minicpm_trained | pooled | +2.5 | [-0.8, +5.9] | 94 / 75 | 0.166 |
| minicpm_base -> minicpm_trained | heldout_2wikimultihopqa | +76.5 | [+70.0, +82.9] | 131 / 1 | 0 |
| minicpm_base -> minicpm_trained | heldout_hotpotqa | +61.9 | [+55.0, +68.8] | 117 / 0 | 0 |
| minicpm_base -> minicpm_trained | heldout_musique | +42.9 | [+36.0, +49.8] | 87 / 0 | 0 |
| minicpm_base -> minicpm_trained | heldout_strategyqa | +70.8 | [+63.8, +77.3] | 131 / 0 | 0 |
| minicpm_base -> minicpm_trained | pooled | +62.3 | [+58.8, +65.7] | 466 / 1 | 0 |
