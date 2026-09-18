# Results

## Per arm and test set

| arm | test set | n | done | EM | F1 | cover | judge | doc recall | steps | vol. finish | tokens/ep | latency s | API $ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| base | heldout_2wikimultihopqa | 170 | yes | 0.018 | 0.120 | 0.306 | 0.353 | 0.810 | 2.98 | 0.02 | 5,182 | 25.5 | 0.0000 |
| base | heldout_hotpotqa | 189 | yes | 0.169 | 0.240 | 0.381 | 0.429 | 0.759 | 2.91 | 0.09 | 5,120 | 20.1 | 0.0000 |
| base | heldout_musique | 203 | yes | 0.020 | 0.084 | 0.153 | 0.172 | 0.597 | 3.00 | 0.00 | 5,052 | 17.5 | 0.0000 |
| base | heldout_strategyqa | 185 | yes | 0.000 | 0.011 | 0.097 | 0.151 | 0.815 | 2.98 | 0.02 | 4,923 | 17.0 | 0.0000 |
| deepseek_taught | heldout_2wikimultihopqa | 170 | yes | 0.429 | 0.543 | 0.765 | 0.765 | 0.854 | 2.93 | 0.07 | 5,655 | 24.3 | 0.0000 |
| deepseek_taught | heldout_hotpotqa | 189 | yes | 0.339 | 0.425 | 0.587 | 0.635 | 0.786 | 2.83 | 0.17 | 5,249 | 22.6 | 0.0000 |
| deepseek_taught | heldout_musique | 203 | yes | 0.163 | 0.287 | 0.350 | 0.389 | 0.663 | 2.99 | 0.01 | 5,253 | 20.8 | 0.0000 |
| deepseek_taught | heldout_strategyqa | 185 | yes | 0.508 | 0.529 | 0.724 | 0.730 | 0.826 | 2.92 | 0.08 | 5,214 | 23.2 | 0.0000 |
| glm_taught | heldout_2wikimultihopqa | 170 | yes | 0.106 | 0.254 | 0.865 | 0.841 | 0.929 | 2.91 | 0.09 | 5,024 | 31.2 | 0.0000 |
| glm_taught | heldout_hotpotqa | 189 | yes | 0.238 | 0.346 | 0.661 | 0.667 | 0.809 | 2.92 | 0.08 | 5,225 | 38.7 | 0.0000 |
| glm_taught | heldout_musique | 203 | yes | 0.054 | 0.188 | 0.394 | 0.458 | 0.730 | 3.00 | 0.00 | 5,644 | 40.0 | 0.0000 |
| glm_taught | heldout_strategyqa | 185 | yes | 0.005 | 0.044 | 0.654 | 0.638 | 0.820 | 2.83 | 0.17 | 4,694 | 34.1 | 0.0000 |
| self_taught | heldout_2wikimultihopqa | 170 | yes | 0.053 | 0.207 | 0.782 | 0.788 | 0.860 | 2.93 | 0.07 | 5,316 | 18.4 | 0.0000 |
| self_taught | heldout_hotpotqa | 189 | yes | 0.270 | 0.373 | 0.661 | 0.688 | 0.783 | 2.78 | 0.22 | 4,936 | 17.9 | 0.0000 |
| self_taught | heldout_musique | 203 | yes | 0.069 | 0.206 | 0.429 | 0.493 | 0.679 | 2.93 | 0.07 | 5,233 | 18.6 | 0.0000 |
| self_taught | heldout_strategyqa | 185 | yes | 0.000 | 0.034 | 0.686 | 0.724 | 0.834 | 2.95 | 0.05 | 5,161 | 19.9 | 0.0000 |

## Pooled per arm

| arm | test sets | n | EM | F1 | cover | judge | steps | tokens/ep | API $ |
|---|---|---|---|---|---|---|---|---|---|
| base | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.052 | 0.113 | 0.232 | 0.273 | 2.97 | 5,067 | 0.0000 |
| deepseek_taught | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.353 | 0.440 | 0.597 | 0.621 | 2.92 | 5,334 | 0.0000 |
| glm_taught | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.100 | 0.207 | 0.633 | 0.643 | 2.91 | 5,162 | 0.0000 |
| self_taught | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.099 | 0.206 | 0.632 | 0.667 | 2.90 | 5,159 | 0.0000 |

## Paired comparisons (judge-correct, b − a)

| a -> b | scope | Δ pts | 95% CI | b wins / a wins | McNemar p |
|---|---|---|---|---|---|
| base -> deepseek_taught | heldout_2wikimultihopqa | +41.2 | [+32.9, +48.8] | 73 / 3 | 0 |
| base -> deepseek_taught | heldout_hotpotqa | +20.6 | [+13.2, +28.0] | 51 / 12 | 1e-06 |
| base -> deepseek_taught | heldout_musique | +21.7 | [+14.3, +29.1] | 57 / 13 | 0 |
| base -> deepseek_taught | heldout_strategyqa | +57.8 | [+50.3, +65.4] | 108 / 1 | 0 |
| base -> deepseek_taught | pooled | +34.8 | [+30.8, +38.7] | 289 / 29 | 0 |
| base -> glm_taught | heldout_2wikimultihopqa | +48.8 | [+41.2, +56.5] | 83 / 0 | 0 |
| base -> glm_taught | heldout_hotpotqa | +23.8 | [+16.4, +31.2] | 56 / 11 | 0 |
| base -> glm_taught | heldout_musique | +28.6 | [+21.2, +36.0] | 67 / 9 | 0 |
| base -> glm_taught | heldout_strategyqa | +48.6 | [+41.1, +56.2] | 92 / 2 | 0 |
| base -> glm_taught | pooled | +37.0 | [+33.1, +40.8] | 298 / 22 | 0 |
| base -> self_taught | heldout_2wikimultihopqa | +43.5 | [+35.3, +51.8] | 79 / 5 | 0 |
| base -> self_taught | heldout_hotpotqa | +25.9 | [+18.5, +33.3] | 57 / 8 | 0 |
| base -> self_taught | heldout_musique | +32.0 | [+24.6, +39.9] | 74 / 9 | 0 |
| base -> self_taught | heldout_strategyqa | +57.3 | [+49.7, +64.3] | 108 / 2 | 0 |
| base -> self_taught | pooled | +39.4 | [+35.5, +43.4] | 318 / 24 | 0 |
| deepseek_taught -> glm_taught | heldout_2wikimultihopqa | +7.6 | [+1.8, +13.5] | 20 / 7 | 0.0192 |
| deepseek_taught -> glm_taught | heldout_hotpotqa | +3.2 | [-2.6, +9.0] | 19 / 13 | 0.377 |
| deepseek_taught -> glm_taught | heldout_musique | +6.9 | [-0.5, +14.3] | 39 / 25 | 0.103 |
| deepseek_taught -> glm_taught | heldout_strategyqa | -9.2 | [-15.7, -2.7] | 10 / 27 | 0.00763 |
| deepseek_taught -> glm_taught | pooled | +2.1 | [-1.2, +5.5] | 88 / 72 | 0.236 |
| deepseek_taught -> self_taught | heldout_2wikimultihopqa | +2.4 | [-2.9, +7.6] | 13 / 9 | 0.523 |
| deepseek_taught -> self_taught | heldout_hotpotqa | +5.3 | [-1.1, +11.6] | 25 / 15 | 0.154 |
| deepseek_taught -> self_taught | heldout_musique | +10.3 | [+2.5, +18.7] | 47 / 26 | 0.0186 |
| deepseek_taught -> self_taught | heldout_strategyqa | -0.5 | [-6.5, +5.4] | 14 / 15 | 1 |
| deepseek_taught -> self_taught | pooled | +4.5 | [+1.2, +7.9] | 99 / 65 | 0.00976 |
| glm_taught -> self_taught | heldout_2wikimultihopqa | -5.3 | [-11.8, +1.2] | 11 / 20 | 0.15 |
| glm_taught -> self_taught | heldout_hotpotqa | +2.1 | [-3.7, +7.9] | 18 / 14 | 0.597 |
| glm_taught -> self_taught | heldout_musique | +3.5 | [-3.5, +10.8] | 32 / 25 | 0.427 |
| glm_taught -> self_taught | heldout_strategyqa | +8.6 | [+3.2, +14.1] | 23 / 7 | 0.00522 |
| glm_taught -> self_taught | pooled | +2.4 | [-0.8, +5.6] | 84 / 66 | 0.165 |
