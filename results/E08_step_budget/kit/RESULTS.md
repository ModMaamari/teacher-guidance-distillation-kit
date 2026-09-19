# Results

## Per arm and test set

| arm | test set | n | done | EM | F1 | cover | judge | doc recall | steps | vol. finish | tokens/ep | latency s | API $ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| base_b1 | heldout_2wikimultihopqa | 170 | yes | 0.000 | 0.000 | 0.000 | 0.000 | 0.778 | 1.00 | 0.00 | 1,401 | 7.9 | 0.0000 |
| base_b1 | heldout_hotpotqa | 189 | yes | 0.000 | 0.000 | 0.000 | 0.000 | 0.770 | 1.00 | 0.00 | 1,417 | 7.2 | 0.0000 |
| base_b1 | heldout_musique | 203 | yes | 0.000 | 0.000 | 0.000 | 0.000 | 0.550 | 1.00 | 0.00 | 1,485 | 9.3 | 0.0000 |
| base_b1 | heldout_strategyqa | 185 | yes | 0.000 | 0.002 | 0.022 | 0.022 | 0.804 | 1.00 | 0.00 | 1,367 | 7.2 | 0.0000 |
| base_b3 | heldout_2wikimultihopqa | 170 | yes | 0.018 | 0.120 | 0.306 | 0.353 | 0.810 | 2.98 | 0.02 | 5,182 | 25.5 | 0.0000 |
| base_b3 | heldout_hotpotqa | 189 | yes | 0.169 | 0.240 | 0.381 | 0.429 | 0.759 | 2.91 | 0.09 | 5,120 | 20.1 | 0.0000 |
| base_b3 | heldout_musique | 203 | yes | 0.020 | 0.084 | 0.153 | 0.172 | 0.597 | 3.00 | 0.00 | 5,052 | 17.5 | 0.0000 |
| base_b3 | heldout_strategyqa | 185 | yes | 0.000 | 0.011 | 0.097 | 0.151 | 0.815 | 2.98 | 0.02 | 4,923 | 17.0 | 0.0000 |
| base_b5 | heldout_2wikimultihopqa | 170 | yes | 0.035 | 0.135 | 0.294 | 0.394 | 0.824 | 4.90 | 0.04 | 9,180 | 38.1 | 0.0000 |
| base_b5 | heldout_hotpotqa | 189 | yes | 0.175 | 0.234 | 0.344 | 0.407 | 0.772 | 4.72 | 0.11 | 9,069 | 31.3 | 0.0000 |
| base_b5 | heldout_musique | 203 | yes | 0.025 | 0.075 | 0.138 | 0.153 | 0.656 | 4.97 | 0.02 | 8,818 | 27.9 | 0.0000 |
| base_b5 | heldout_strategyqa | 185 | yes | 0.000 | 0.011 | 0.114 | 0.189 | 0.813 | 4.96 | 0.02 | 8,718 | 28.9 | 0.0000 |
| base_b8 | heldout_2wikimultihopqa | 170 | yes | 0.029 | 0.112 | 0.253 | 0.347 | 0.831 | 7.96 | 0.02 | 15,738 | 78.7 | 0.0000 |
| base_b8 | heldout_hotpotqa | 189 | yes | 0.185 | 0.243 | 0.349 | 0.392 | 0.786 | 7.27 | 0.17 | 14,740 | 63.1 | 0.0000 |
| base_b8 | heldout_musique | 203 | yes | 0.039 | 0.086 | 0.143 | 0.143 | 0.668 | 7.91 | 0.03 | 14,803 | 56.3 | 0.0000 |
| base_b8 | heldout_strategyqa | 185 | yes | 0.000 | 0.011 | 0.108 | 0.184 | 0.825 | 7.83 | 0.04 | 14,491 | 57.9 | 0.0000 |
| teacher_b1 | heldout_2wikimultihopqa | 170 | yes | 0.347 | 0.476 | 0.624 | 0.641 | 0.000 | 1.00 | 0.00 | 4,193 | 276.8 | 0.0000 |
| teacher_b1 | heldout_hotpotqa | 189 | yes | 0.429 | 0.538 | 0.609 | 0.720 | 0.000 | 1.00 | 0.00 | 4,407 | 208.3 | 0.0000 |
| teacher_b1 | heldout_musique | 203 | yes | 0.212 | 0.360 | 0.409 | 0.453 | 0.000 | 1.00 | 0.00 | 6,724 | 376.0 | 0.0000 |
| teacher_b1 | heldout_strategyqa | 185 | yes | 0.092 | 0.155 | 0.595 | 0.600 | 0.000 | 1.00 | 0.00 | 3,512 | 235.4 | 0.0000 |
| teacher_b3 | heldout_2wikimultihopqa | 170 | yes | 0.312 | 0.431 | 0.900 | 0.912 | 0.934 | 2.80 | 0.20 | 6,135 | 473.8 | 0.0000 |
| teacher_b3 | heldout_hotpotqa | 189 | yes | 0.529 | 0.636 | 0.852 | 0.910 | 0.891 | 2.85 | 0.15 | 6,811 | 438.2 | 0.0000 |
| teacher_b3 | heldout_musique | 203 | yes | 0.350 | 0.485 | 0.611 | 0.690 | 0.776 | 2.95 | 0.05 | 9,058 | 420.8 | 0.0000 |
| teacher_b3 | heldout_strategyqa | 185 | yes | 0.005 | 0.052 | 0.773 | 0.816 | 0.860 | 2.96 | 0.04 | 6,662 | 307.2 | 0.0000 |
| teacher_b5 | heldout_2wikimultihopqa | 170 | yes | 0.271 | 0.410 | 0.912 | 0.941 | 0.977 | 3.71 | 0.69 | 7,991 | 552.9 | 0.0000 |
| teacher_b5 | heldout_hotpotqa | 189 | yes | 0.503 | 0.641 | 0.831 | 0.910 | 0.931 | 4.05 | 0.52 | 9,266 | 559.9 | 0.0000 |
| teacher_b5 | heldout_musique | 203 | yes | 0.369 | 0.523 | 0.670 | 0.744 | 0.893 | 4.48 | 0.27 | 12,549 | 477.8 | 0.0000 |
| teacher_b5 | heldout_strategyqa | 185 | yes | 0.005 | 0.051 | 0.784 | 0.822 | 0.902 | 4.53 | 0.27 | 10,021 | 252.3 | 0.0000 |
| teacher_b8 | heldout_2wikimultihopqa | 170 | yes | 0.329 | 0.467 | 0.947 | 0.953 | 0.977 | 4.40 | 0.82 | 9,213 | 490.7 | 0.0000 |
| teacher_b8 | heldout_hotpotqa | 189 | yes | 0.513 | 0.637 | 0.847 | 0.905 | 0.944 | 5.21 | 0.61 | 12,394 | 795.5 | 0.0000 |
| teacher_b8 | heldout_musique | 203 | yes | 0.340 | 0.511 | 0.660 | 0.759 | 0.921 | 6.37 | 0.38 | 16,747 | 472.5 | 0.0000 |
| teacher_b8 | heldout_strategyqa | 185 | yes | 0.000 | 0.051 | 0.800 | 0.832 | 0.914 | 6.42 | 0.37 | 14,432 | 195.4 | 0.0000 |
| trained_b1 | heldout_2wikimultihopqa | 170 | yes | 0.047 | 0.047 | 0.047 | 0.047 | 0.690 | 1.00 | 0.00 | 1,750 | 16.8 | 0.0000 |
| trained_b1 | heldout_hotpotqa | 189 | yes | 0.005 | 0.013 | 0.016 | 0.016 | 0.651 | 1.00 | 0.00 | 1,724 | 15.7 | 0.0000 |
| trained_b1 | heldout_musique | 203 | yes | 0.000 | 0.022 | 0.020 | 0.030 | 0.439 | 1.00 | 0.00 | 1,736 | 16.6 | 0.0000 |
| trained_b1 | heldout_strategyqa | 185 | yes | 0.286 | 0.290 | 0.324 | 0.324 | 0.414 | 1.00 | 0.00 | 1,706 | 17.6 | 0.0000 |
| trained_b3 | heldout_2wikimultihopqa | 170 | yes | 0.429 | 0.543 | 0.765 | 0.765 | 0.854 | 2.93 | 0.07 | 5,655 | 24.3 | 0.0000 |
| trained_b3 | heldout_hotpotqa | 189 | yes | 0.339 | 0.425 | 0.587 | 0.635 | 0.786 | 2.83 | 0.17 | 5,249 | 22.6 | 0.0000 |
| trained_b3 | heldout_musique | 203 | yes | 0.163 | 0.287 | 0.350 | 0.389 | 0.663 | 2.99 | 0.01 | 5,253 | 20.8 | 0.0000 |
| trained_b3 | heldout_strategyqa | 185 | yes | 0.508 | 0.529 | 0.724 | 0.730 | 0.826 | 2.92 | 0.08 | 5,214 | 23.2 | 0.0000 |
| trained_b5 | heldout_2wikimultihopqa | 170 | yes | 0.341 | 0.492 | 0.800 | 0.806 | 0.897 | 4.40 | 0.29 | 10,065 | 42.7 | 0.0000 |
| trained_b5 | heldout_hotpotqa | 189 | yes | 0.339 | 0.429 | 0.587 | 0.651 | 0.772 | 4.13 | 0.39 | 8,277 | 35.0 | 0.0000 |
| trained_b5 | heldout_musique | 203 | yes | 0.197 | 0.321 | 0.443 | 0.502 | 0.741 | 4.64 | 0.20 | 8,884 | 35.8 | 0.0000 |
| trained_b5 | heldout_strategyqa | 185 | yes | 0.443 | 0.472 | 0.735 | 0.741 | 0.837 | 4.56 | 0.21 | 8,996 | 40.8 | 0.0000 |
| trained_b8 | heldout_2wikimultihopqa | 170 | yes | 0.271 | 0.456 | 0.806 | 0.829 | 0.909 | 6.49 | 0.35 | 15,912 | 107.7 | 0.0000 |
| trained_b8 | heldout_hotpotqa | 189 | yes | 0.291 | 0.379 | 0.566 | 0.619 | 0.775 | 5.67 | 0.49 | 12,001 | 85.1 | 0.0000 |
| trained_b8 | heldout_musique | 203 | yes | 0.148 | 0.286 | 0.463 | 0.512 | 0.742 | 6.93 | 0.28 | 13,910 | 84.7 | 0.0000 |
| trained_b8 | heldout_strategyqa | 185 | yes | 0.443 | 0.477 | 0.751 | 0.762 | 0.854 | 6.92 | 0.25 | 14,071 | 101.6 | 0.0000 |

## Pooled per arm

| arm | test sets | n | EM | F1 | cover | judge | steps | tokens/ep | API $ |
|---|---|---|---|---|---|---|---|---|---|
| base_b1 | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.000 | 0.000 | 0.005 | 0.005 | 1.00 | 1,419 | 0.0000 |
| base_b3 | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.052 | 0.113 | 0.232 | 0.273 | 2.97 | 5,067 | 0.0000 |
| base_b5 | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.059 | 0.113 | 0.220 | 0.281 | 4.89 | 8,939 | 0.0000 |
| base_b8 | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.064 | 0.113 | 0.211 | 0.262 | 7.74 | 14,923 | 0.0000 |
| teacher_b1 | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.268 | 0.381 | 0.554 | 0.600 | 1.00 | 4,766 | 0.0000 |
| teacher_b3 | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.301 | 0.404 | 0.778 | 0.827 | 2.89 | 7,231 | 0.0000 |
| teacher_b5 | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.290 | 0.410 | 0.794 | 0.850 | 4.21 | 10,055 | 0.0000 |
| teacher_b8 | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.297 | 0.419 | 0.807 | 0.858 | 5.64 | 13,358 | 0.0000 |
| trained_b1 | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.083 | 0.092 | 0.100 | 0.103 | 1.00 | 1,729 | 0.0000 |
| trained_b3 | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.353 | 0.440 | 0.597 | 0.621 | 2.92 | 5,334 | 0.0000 |
| trained_b5 | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.327 | 0.425 | 0.633 | 0.668 | 4.44 | 9,027 | 0.0000 |
| trained_b8 | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.285 | 0.395 | 0.639 | 0.673 | 6.51 | 13,922 | 0.0000 |

## Paired comparisons (judge-correct, b − a)

| a -> b | scope | Δ pts | 95% CI | b wins / a wins | McNemar p |
|---|---|---|---|---|---|
| base_b1 -> base_b3 | heldout_2wikimultihopqa | +35.3 | [+28.2, +42.4] | 60 / 0 | 0 |
| base_b1 -> base_b3 | heldout_hotpotqa | +42.9 | [+36.0, +49.7] | 81 / 0 | 0 |
| base_b1 -> base_b3 | heldout_musique | +17.2 | [+12.3, +22.7] | 35 / 0 | 0 |
| base_b1 -> base_b3 | heldout_strategyqa | +13.0 | [+7.6, +18.4] | 26 / 2 | 3e-06 |
| base_b1 -> base_b3 | pooled | +26.8 | [+23.6, +30.0] | 202 / 2 | 0 |
| base_b1 -> base_b5 | heldout_2wikimultihopqa | +39.4 | [+32.4, +47.1] | 67 / 0 | 0 |
| base_b1 -> base_b5 | heldout_hotpotqa | +40.7 | [+33.9, +47.6] | 77 / 0 | 0 |
| base_b1 -> base_b5 | heldout_musique | +15.3 | [+10.3, +20.2] | 31 / 0 | 0 |
| base_b1 -> base_b5 | heldout_strategyqa | +16.8 | [+11.3, +22.7] | 32 / 1 | 0 |
| base_b1 -> base_b5 | pooled | +27.6 | [+24.2, +30.9] | 207 / 1 | 0 |
| base_b1 -> base_b8 | heldout_2wikimultihopqa | +34.7 | [+27.7, +41.8] | 59 / 0 | 0 |
| base_b1 -> base_b8 | heldout_hotpotqa | +39.1 | [+32.3, +46.0] | 74 / 0 | 0 |
| base_b1 -> base_b8 | heldout_musique | +14.3 | [+9.8, +19.2] | 29 / 0 | 0 |
| base_b1 -> base_b8 | heldout_strategyqa | +16.2 | [+10.8, +22.2] | 32 / 2 | 0 |
| base_b1 -> base_b8 | pooled | +25.7 | [+22.6, +28.8] | 194 / 2 | 0 |
| base_b1 -> teacher_b1 | heldout_2wikimultihopqa | +64.1 | [+56.5, +71.2] | 109 / 0 | 0 |
| base_b1 -> teacher_b1 | heldout_hotpotqa | +72.0 | [+65.6, +78.3] | 136 / 0 | 0 |
| base_b1 -> teacher_b1 | heldout_musique | +45.3 | [+38.4, +52.2] | 92 / 0 | 0 |
| base_b1 -> teacher_b1 | heldout_strategyqa | +57.8 | [+50.8, +64.9] | 107 / 0 | 0 |
| base_b1 -> teacher_b1 | pooled | +59.4 | [+55.8, +62.9] | 444 / 0 | 0 |
| base_b1 -> teacher_b3 | heldout_2wikimultihopqa | +91.2 | [+86.5, +95.3] | 155 / 0 | 0 |
| base_b1 -> teacher_b3 | heldout_hotpotqa | +91.0 | [+86.8, +94.7] | 172 / 0 | 0 |
| base_b1 -> teacher_b3 | heldout_musique | +69.0 | [+62.6, +75.4] | 140 / 0 | 0 |
| base_b1 -> teacher_b3 | heldout_strategyqa | +79.5 | [+73.5, +85.4] | 148 / 1 | 0 |
| base_b1 -> teacher_b3 | pooled | +82.2 | [+79.4, +84.9] | 615 / 1 | 0 |
| base_b1 -> teacher_b5 | heldout_2wikimultihopqa | +94.1 | [+90.6, +97.7] | 160 / 0 | 0 |
| base_b1 -> teacher_b5 | heldout_hotpotqa | +91.0 | [+86.8, +94.7] | 172 / 0 | 0 |
| base_b1 -> teacher_b5 | heldout_musique | +74.4 | [+68.0, +80.3] | 151 / 0 | 0 |
| base_b1 -> teacher_b5 | heldout_strategyqa | +80.0 | [+74.1, +86.0] | 149 / 1 | 0 |
| base_b1 -> teacher_b5 | pooled | +84.5 | [+81.8, +87.0] | 632 / 1 | 0 |
| base_b1 -> teacher_b8 | heldout_2wikimultihopqa | +95.3 | [+91.8, +98.2] | 162 / 0 | 0 |
| base_b1 -> teacher_b8 | heldout_hotpotqa | +90.5 | [+86.2, +94.7] | 171 / 0 | 0 |
| base_b1 -> teacher_b8 | heldout_musique | +75.9 | [+69.5, +81.8] | 154 / 0 | 0 |
| base_b1 -> teacher_b8 | heldout_strategyqa | +81.1 | [+75.1, +87.0] | 151 / 1 | 0 |
| base_b1 -> teacher_b8 | pooled | +85.3 | [+82.6, +87.8] | 638 / 1 | 0 |
| base_b1 -> trained_b1 | heldout_2wikimultihopqa | +4.7 | [+1.8, +8.2] | 8 / 0 | 0.00781 |
| base_b1 -> trained_b1 | heldout_hotpotqa | +1.6 | [+0.0, +3.7] | 3 / 0 | 0.25 |
| base_b1 -> trained_b1 | heldout_musique | +3.0 | [+1.0, +5.4] | 6 / 0 | 0.0312 |
| base_b1 -> trained_b1 | heldout_strategyqa | +30.3 | [+23.8, +37.3] | 57 / 1 | 0 |
| base_b1 -> trained_b1 | pooled | +9.8 | [+7.6, +11.9] | 74 / 1 | 0 |
| base_b1 -> trained_b3 | heldout_2wikimultihopqa | +76.5 | [+70.0, +82.3] | 130 / 0 | 0 |
| base_b1 -> trained_b3 | heldout_hotpotqa | +63.5 | [+56.6, +70.4] | 120 / 0 | 0 |
| base_b1 -> trained_b3 | heldout_musique | +38.9 | [+32.5, +45.3] | 79 / 0 | 0 |
| base_b1 -> trained_b3 | heldout_strategyqa | +70.8 | [+64.3, +77.3] | 131 / 0 | 0 |
| base_b1 -> trained_b3 | pooled | +61.6 | [+58.1, +65.1] | 460 / 0 | 0 |
| base_b1 -> trained_b5 | heldout_2wikimultihopqa | +80.6 | [+74.7, +86.5] | 137 / 0 | 0 |
| base_b1 -> trained_b5 | heldout_hotpotqa | +65.1 | [+58.2, +72.0] | 123 / 0 | 0 |
| base_b1 -> trained_b5 | heldout_musique | +50.2 | [+43.4, +57.1] | 102 / 0 | 0 |
| base_b1 -> trained_b5 | heldout_strategyqa | +71.9 | [+65.4, +78.4] | 134 / 1 | 0 |
| base_b1 -> trained_b5 | pooled | +66.3 | [+62.8, +69.6] | 496 / 1 | 0 |
| base_b1 -> trained_b8 | heldout_2wikimultihopqa | +82.9 | [+77.1, +88.2] | 141 / 0 | 0 |
| base_b1 -> trained_b8 | heldout_hotpotqa | +61.9 | [+55.0, +68.8] | 117 / 0 | 0 |
| base_b1 -> trained_b8 | heldout_musique | +51.2 | [+44.3, +58.1] | 104 / 0 | 0 |
| base_b1 -> trained_b8 | heldout_strategyqa | +74.1 | [+67.6, +80.0] | 137 / 0 | 0 |
| base_b1 -> trained_b8 | pooled | +66.8 | [+63.4, +70.2] | 499 / 0 | 0 |
| base_b3 -> base_b5 | heldout_2wikimultihopqa | +4.1 | [-2.4, +10.6] | 21 / 14 | 0.311 |
| base_b3 -> base_b5 | heldout_hotpotqa | -2.1 | [-8.5, +4.2] | 16 / 20 | 0.618 |
| base_b3 -> base_b5 | heldout_musique | -2.0 | [-7.4, +3.5] | 15 / 19 | 0.608 |
| base_b3 -> base_b5 | heldout_strategyqa | +3.8 | [-1.6, +9.2] | 17 / 10 | 0.248 |
| base_b3 -> base_b5 | pooled | +0.8 | [-2.1, +3.9] | 69 / 63 | 0.664 |
| base_b3 -> base_b8 | heldout_2wikimultihopqa | -0.6 | [-7.1, +5.9] | 16 / 17 | 1 |
| base_b3 -> base_b8 | heldout_hotpotqa | -3.7 | [-10.1, +2.6] | 17 / 24 | 0.349 |
| base_b3 -> base_b8 | heldout_musique | -3.0 | [-8.4, +2.5] | 14 / 20 | 0.392 |
| base_b3 -> base_b8 | heldout_strategyqa | +3.2 | [-2.7, +9.2] | 19 / 13 | 0.377 |
| base_b3 -> base_b8 | pooled | -1.1 | [-4.2, +2.0] | 66 / 74 | 0.554 |
| base_b3 -> teacher_b1 | heldout_2wikimultihopqa | +28.8 | [+19.4, +38.2] | 66 / 17 | 0 |
| base_b3 -> teacher_b1 | heldout_hotpotqa | +29.1 | [+20.6, +37.6] | 71 / 16 | 0 |
| base_b3 -> teacher_b1 | heldout_musique | +28.1 | [+20.2, +36.0] | 68 / 11 | 0 |
| base_b3 -> teacher_b1 | heldout_strategyqa | +44.9 | [+36.2, +53.5] | 92 / 9 | 0 |
| base_b3 -> teacher_b1 | pooled | +32.7 | [+28.4, +37.0] | 297 / 53 | 0 |
| base_b3 -> teacher_b3 | heldout_2wikimultihopqa | +55.9 | [+48.2, +63.5] | 97 / 2 | 0 |
| base_b3 -> teacher_b3 | heldout_hotpotqa | +48.1 | [+40.7, +55.6] | 94 / 3 | 0 |
| base_b3 -> teacher_b3 | heldout_musique | +51.7 | [+44.8, +58.6] | 106 / 1 | 0 |
| base_b3 -> teacher_b3 | heldout_strategyqa | +66.5 | [+59.5, +73.5] | 124 / 1 | 0 |
| base_b3 -> teacher_b3 | pooled | +55.4 | [+51.7, +59.0] | 421 / 7 | 0 |
| base_b3 -> teacher_b5 | heldout_2wikimultihopqa | +58.8 | [+51.2, +66.5] | 101 / 1 | 0 |
| base_b3 -> teacher_b5 | heldout_hotpotqa | +48.1 | [+40.7, +55.6] | 93 / 2 | 0 |
| base_b3 -> teacher_b5 | heldout_musique | +57.1 | [+50.2, +64.0] | 117 / 1 | 0 |
| base_b3 -> teacher_b5 | heldout_strategyqa | +67.0 | [+60.0, +73.5] | 125 / 1 | 0 |
| base_b3 -> teacher_b5 | pooled | +57.7 | [+53.9, +61.3] | 436 / 5 | 0 |
| base_b3 -> teacher_b8 | heldout_2wikimultihopqa | +60.0 | [+52.3, +67.7] | 103 / 1 | 0 |
| base_b3 -> teacher_b8 | heldout_hotpotqa | +47.6 | [+40.2, +55.0] | 93 / 3 | 0 |
| base_b3 -> teacher_b8 | heldout_musique | +58.6 | [+51.2, +65.5] | 122 / 3 | 0 |
| base_b3 -> teacher_b8 | heldout_strategyqa | +68.1 | [+61.1, +75.1] | 127 / 1 | 0 |
| base_b3 -> teacher_b8 | pooled | +58.5 | [+54.8, +62.1] | 445 / 8 | 0 |
| base_b3 -> trained_b1 | heldout_2wikimultihopqa | -30.6 | [-38.8, -22.9] | 6 / 58 | 0 |
| base_b3 -> trained_b1 | heldout_hotpotqa | -41.3 | [-48.7, -33.9] | 2 / 80 | 0 |
| base_b3 -> trained_b1 | heldout_musique | -14.3 | [-20.2, -8.4] | 5 / 34 | 2e-06 |
| base_b3 -> trained_b1 | heldout_strategyqa | +17.3 | [+8.6, +25.9] | 51 / 19 | 0.000166 |
| base_b3 -> trained_b1 | pooled | -17.0 | [-21.0, -13.0] | 64 / 191 | 0 |
| base_b3 -> trained_b3 | heldout_2wikimultihopqa | +41.2 | [+32.9, +48.8] | 73 / 3 | 0 |
| base_b3 -> trained_b3 | heldout_hotpotqa | +20.6 | [+13.2, +28.0] | 51 / 12 | 1e-06 |
| base_b3 -> trained_b3 | heldout_musique | +21.7 | [+14.3, +29.1] | 57 / 13 | 0 |
| base_b3 -> trained_b3 | heldout_strategyqa | +57.8 | [+50.3, +65.4] | 108 / 1 | 0 |
| base_b3 -> trained_b3 | pooled | +34.8 | [+30.8, +38.7] | 289 / 29 | 0 |
| base_b3 -> trained_b5 | heldout_2wikimultihopqa | +45.3 | [+37.6, +53.5] | 80 / 3 | 0 |
| base_b3 -> trained_b5 | heldout_hotpotqa | +22.2 | [+14.8, +29.6] | 52 / 10 | 0 |
| base_b3 -> trained_b5 | heldout_musique | +33.0 | [+25.6, +40.4] | 74 / 7 | 0 |
| base_b3 -> trained_b5 | heldout_strategyqa | +58.9 | [+51.3, +66.5] | 113 / 4 | 0 |
| base_b3 -> trained_b5 | pooled | +39.5 | [+35.5, +43.4] | 319 / 24 | 0 |
| base_b3 -> trained_b8 | heldout_2wikimultihopqa | +47.6 | [+39.4, +55.9] | 84 / 3 | 0 |
| base_b3 -> trained_b8 | heldout_hotpotqa | +19.1 | [+12.2, +26.5] | 46 / 10 | 1e-06 |
| base_b3 -> trained_b8 | heldout_musique | +34.0 | [+26.6, +41.4] | 76 / 7 | 0 |
| base_b3 -> trained_b8 | heldout_strategyqa | +61.1 | [+54.0, +68.1] | 113 / 0 | 0 |
| base_b3 -> trained_b8 | pooled | +40.0 | [+36.1, +43.8] | 319 / 20 | 0 |
| base_b5 -> base_b8 | heldout_2wikimultihopqa | -4.7 | [-11.8, +2.4] | 14 / 22 | 0.243 |
| base_b5 -> base_b8 | heldout_hotpotqa | -1.6 | [-7.9, +4.2] | 15 / 18 | 0.728 |
| base_b5 -> base_b8 | heldout_musique | -1.0 | [-6.4, +4.9] | 16 / 18 | 0.864 |
| base_b5 -> base_b8 | heldout_strategyqa | -0.5 | [-5.9, +4.9] | 12 / 13 | 1 |
| base_b5 -> base_b8 | pooled | -1.9 | [-4.8, +1.1] | 57 / 71 | 0.25 |
| base_b5 -> teacher_b1 | heldout_2wikimultihopqa | +24.7 | [+14.1, +34.7] | 65 / 23 | 9e-06 |
| base_b5 -> teacher_b1 | heldout_hotpotqa | +31.2 | [+22.2, +39.7] | 75 / 16 | 0 |
| base_b5 -> teacher_b1 | heldout_musique | +30.0 | [+21.7, +37.9] | 74 / 13 | 0 |
| base_b5 -> teacher_b1 | heldout_strategyqa | +41.1 | [+32.4, +49.2] | 84 / 8 | 0 |
| base_b5 -> teacher_b1 | pooled | +31.9 | [+27.4, +36.3] | 298 / 60 | 0 |
| base_b5 -> teacher_b3 | heldout_2wikimultihopqa | +51.8 | [+44.1, +59.4] | 88 / 0 | 0 |
| base_b5 -> teacher_b3 | heldout_hotpotqa | +50.3 | [+42.9, +57.7] | 96 / 1 | 0 |
| base_b5 -> teacher_b3 | heldout_musique | +53.7 | [+46.3, +61.1] | 114 / 5 | 0 |
| base_b5 -> teacher_b3 | heldout_strategyqa | +62.7 | [+55.7, +69.7] | 117 / 1 | 0 |
| base_b5 -> teacher_b3 | pooled | +54.6 | [+50.9, +58.4] | 415 / 7 | 0 |
| base_b5 -> teacher_b5 | heldout_2wikimultihopqa | +54.7 | [+47.1, +62.4] | 93 / 0 | 0 |
| base_b5 -> teacher_b5 | heldout_hotpotqa | +50.3 | [+42.9, +57.1] | 95 / 0 | 0 |
| base_b5 -> teacher_b5 | heldout_musique | +59.1 | [+51.7, +66.5] | 124 / 4 | 0 |
| base_b5 -> teacher_b5 | heldout_strategyqa | +63.2 | [+56.2, +70.3] | 119 / 2 | 0 |
| base_b5 -> teacher_b5 | pooled | +56.9 | [+53.1, +60.5] | 431 / 6 | 0 |
| base_b5 -> teacher_b8 | heldout_2wikimultihopqa | +55.9 | [+48.2, +63.5] | 95 / 0 | 0 |
| base_b5 -> teacher_b8 | heldout_hotpotqa | +49.7 | [+42.3, +57.1] | 94 / 0 | 0 |
| base_b5 -> teacher_b8 | heldout_musique | +60.6 | [+52.7, +68.0] | 129 / 6 | 0 |
| base_b5 -> teacher_b8 | heldout_strategyqa | +64.3 | [+57.3, +71.4] | 120 / 1 | 0 |
| base_b5 -> teacher_b8 | pooled | +57.7 | [+53.9, +61.3] | 438 / 7 | 0 |
| base_b5 -> trained_b1 | heldout_2wikimultihopqa | -34.7 | [-42.4, -27.1] | 3 / 62 | 0 |
| base_b5 -> trained_b1 | heldout_hotpotqa | -39.1 | [-46.6, -31.8] | 2 / 76 | 0 |
| base_b5 -> trained_b1 | heldout_musique | -12.3 | [-17.2, -7.4] | 3 / 28 | 5e-06 |
| base_b5 -> trained_b1 | heldout_strategyqa | +13.5 | [+4.3, +22.7] | 49 / 24 | 0.00463 |
| base_b5 -> trained_b1 | pooled | -17.8 | [-21.8, -13.8] | 57 / 190 | 0 |
| base_b5 -> trained_b3 | heldout_2wikimultihopqa | +37.1 | [+29.4, +44.7] | 66 / 3 | 0 |
| base_b5 -> trained_b3 | heldout_hotpotqa | +22.8 | [+15.3, +30.2] | 52 / 9 | 0 |
| base_b5 -> trained_b3 | heldout_musique | +23.6 | [+15.8, +31.0] | 61 / 13 | 0 |
| base_b5 -> trained_b3 | heldout_strategyqa | +54.0 | [+46.5, +61.6] | 101 / 1 | 0 |
| base_b5 -> trained_b3 | pooled | +34.0 | [+30.1, +37.8] | 280 / 26 | 0 |
| base_b5 -> trained_b5 | heldout_2wikimultihopqa | +41.2 | [+33.5, +48.8] | 72 / 2 | 0 |
| base_b5 -> trained_b5 | heldout_hotpotqa | +24.3 | [+16.9, +32.3] | 55 / 9 | 0 |
| base_b5 -> trained_b5 | heldout_musique | +35.0 | [+27.1, +42.4] | 79 / 8 | 0 |
| base_b5 -> trained_b5 | heldout_strategyqa | +55.1 | [+47.0, +62.7] | 106 / 4 | 0 |
| base_b5 -> trained_b5 | pooled | +38.7 | [+34.8, +42.6] | 312 / 23 | 0 |
| base_b5 -> trained_b8 | heldout_2wikimultihopqa | +43.5 | [+35.9, +51.8] | 76 / 2 | 0 |
| base_b5 -> trained_b8 | heldout_hotpotqa | +21.2 | [+13.8, +28.6] | 49 / 9 | 0 |
| base_b5 -> trained_b8 | heldout_musique | +36.0 | [+28.1, +43.8] | 83 / 10 | 0 |
| base_b5 -> trained_b8 | heldout_strategyqa | +57.3 | [+49.7, +64.3] | 106 / 0 | 0 |
| base_b5 -> trained_b8 | pooled | +39.2 | [+35.3, +43.1] | 314 / 21 | 0 |
| base_b8 -> teacher_b1 | heldout_2wikimultihopqa | +29.4 | [+19.4, +38.8] | 68 / 18 | 0 |
| base_b8 -> teacher_b1 | heldout_hotpotqa | +32.8 | [+23.3, +41.8] | 80 / 18 | 0 |
| base_b8 -> teacher_b1 | heldout_musique | +31.0 | [+23.2, +38.9] | 73 / 10 | 0 |
| base_b8 -> teacher_b1 | heldout_strategyqa | +41.6 | [+33.0, +50.3] | 87 / 10 | 0 |
| base_b8 -> teacher_b1 | pooled | +33.7 | [+29.3, +38.1] | 308 / 56 | 0 |
| base_b8 -> teacher_b3 | heldout_2wikimultihopqa | +56.5 | [+48.2, +64.1] | 98 / 2 | 0 |
| base_b8 -> teacher_b3 | heldout_hotpotqa | +51.8 | [+44.4, +59.8] | 100 / 2 | 0 |
| base_b8 -> teacher_b3 | heldout_musique | +54.7 | [+47.3, +62.1] | 114 / 3 | 0 |
| base_b8 -> teacher_b3 | heldout_strategyqa | +63.2 | [+56.2, +70.3] | 118 / 1 | 0 |
| base_b8 -> teacher_b3 | pooled | +56.5 | [+52.7, +60.2] | 430 / 8 | 0 |
| base_b8 -> teacher_b5 | heldout_2wikimultihopqa | +59.4 | [+51.2, +67.1] | 102 / 1 | 0 |
| base_b8 -> teacher_b5 | heldout_hotpotqa | +51.8 | [+44.4, +59.3] | 99 / 1 | 0 |
| base_b8 -> teacher_b5 | heldout_musique | +60.1 | [+52.7, +67.0] | 124 / 2 | 0 |
| base_b8 -> teacher_b5 | heldout_strategyqa | +63.8 | [+56.8, +70.3] | 118 / 0 | 0 |
| base_b8 -> teacher_b5 | pooled | +58.8 | [+55.1, +62.4] | 443 / 4 | 0 |
| base_b8 -> teacher_b8 | heldout_2wikimultihopqa | +60.6 | [+52.9, +68.2] | 104 / 1 | 0 |
| base_b8 -> teacher_b8 | heldout_hotpotqa | +51.3 | [+43.9, +58.7] | 98 / 1 | 0 |
| base_b8 -> teacher_b8 | heldout_musique | +61.6 | [+54.7, +68.5] | 127 / 2 | 0 |
| base_b8 -> teacher_b8 | heldout_strategyqa | +64.9 | [+57.8, +71.9] | 121 / 1 | 0 |
| base_b8 -> teacher_b8 | pooled | +59.6 | [+56.0, +63.2] | 450 / 5 | 0 |
| base_b8 -> trained_b1 | heldout_2wikimultihopqa | -30.0 | [-38.2, -22.4] | 5 / 56 | 0 |
| base_b8 -> trained_b1 | heldout_hotpotqa | -37.6 | [-45.0, -30.2] | 2 / 73 | 0 |
| base_b8 -> trained_b1 | heldout_musique | -11.3 | [-16.8, -5.9] | 5 / 28 | 6.6e-05 |
| base_b8 -> trained_b1 | heldout_strategyqa | +14.1 | [+5.4, +22.7] | 49 / 23 | 0.00294 |
| base_b8 -> trained_b1 | pooled | -15.9 | [-19.8, -11.9] | 61 / 180 | 0 |
| base_b8 -> trained_b3 | heldout_2wikimultihopqa | +41.8 | [+34.1, +49.4] | 72 / 1 | 0 |
| base_b8 -> trained_b3 | heldout_hotpotqa | +24.3 | [+16.4, +32.3] | 56 / 10 | 0 |
| base_b8 -> trained_b3 | heldout_musique | +24.6 | [+17.2, +32.0] | 62 / 12 | 0 |
| base_b8 -> trained_b3 | heldout_strategyqa | +54.6 | [+47.0, +62.2] | 104 / 3 | 0 |
| base_b8 -> trained_b3 | pooled | +35.9 | [+32.0, +39.8] | 294 / 26 | 0 |
| base_b8 -> trained_b5 | heldout_2wikimultihopqa | +45.9 | [+38.2, +53.5] | 78 / 0 | 0 |
| base_b8 -> trained_b5 | heldout_hotpotqa | +25.9 | [+18.0, +33.9] | 60 / 11 | 0 |
| base_b8 -> trained_b5 | heldout_musique | +36.0 | [+28.6, +43.4] | 77 / 4 | 0 |
| base_b8 -> trained_b5 | heldout_strategyqa | +55.7 | [+47.6, +63.8] | 109 / 6 | 0 |
| base_b8 -> trained_b5 | pooled | +40.6 | [+36.7, +44.6] | 324 / 21 | 0 |
| base_b8 -> trained_b8 | heldout_2wikimultihopqa | +48.2 | [+40.6, +55.9] | 82 / 0 | 0 |
| base_b8 -> trained_b8 | heldout_hotpotqa | +22.8 | [+15.3, +30.2] | 52 / 9 | 0 |
| base_b8 -> trained_b8 | heldout_musique | +37.0 | [+29.6, +43.8] | 79 / 4 | 0 |
| base_b8 -> trained_b8 | heldout_strategyqa | +57.8 | [+50.3, +65.4] | 110 / 3 | 0 |
| base_b8 -> trained_b8 | pooled | +41.1 | [+37.2, +44.9] | 323 / 16 | 0 |
| teacher_b1 -> teacher_b3 | heldout_2wikimultihopqa | +27.1 | [+18.8, +35.3] | 54 / 8 | 0 |
| teacher_b1 -> teacher_b3 | heldout_hotpotqa | +19.1 | [+12.7, +25.9] | 42 / 6 | 0 |
| teacher_b1 -> teacher_b3 | heldout_musique | +23.6 | [+16.3, +31.0] | 58 / 10 | 0 |
| teacher_b1 -> teacher_b3 | heldout_strategyqa | +21.6 | [+14.1, +29.2] | 50 / 10 | 0 |
| teacher_b1 -> teacher_b3 | pooled | +22.8 | [+19.0, +26.5] | 204 / 34 | 0 |
| teacher_b1 -> teacher_b5 | heldout_2wikimultihopqa | +30.0 | [+21.8, +38.2] | 58 / 7 | 0 |
| teacher_b1 -> teacher_b5 | heldout_hotpotqa | +19.1 | [+12.2, +25.9] | 44 / 8 | 0 |
| teacher_b1 -> teacher_b5 | heldout_musique | +29.1 | [+22.2, +36.0] | 64 / 5 | 0 |
| teacher_b1 -> teacher_b5 | heldout_strategyqa | +22.2 | [+14.1, +30.3] | 52 / 11 | 0 |
| teacher_b1 -> teacher_b5 | pooled | +25.0 | [+21.3, +28.8] | 218 / 31 | 0 |
| teacher_b1 -> teacher_b8 | heldout_2wikimultihopqa | +31.2 | [+23.5, +39.4] | 58 / 5 | 0 |
| teacher_b1 -> teacher_b8 | heldout_hotpotqa | +18.5 | [+12.2, +24.9] | 41 / 6 | 0 |
| teacher_b1 -> teacher_b8 | heldout_musique | +30.5 | [+23.6, +37.4] | 65 / 3 | 0 |
| teacher_b1 -> teacher_b8 | heldout_strategyqa | +23.2 | [+15.7, +30.8] | 51 / 8 | 0 |
| teacher_b1 -> teacher_b8 | pooled | +25.8 | [+22.2, +29.4] | 215 / 22 | 0 |
| teacher_b1 -> trained_b1 | heldout_2wikimultihopqa | -59.4 | [-67.1, -51.2] | 3 / 104 | 0 |
| teacher_b1 -> trained_b1 | heldout_hotpotqa | -70.4 | [-76.7, -64.0] | 0 / 133 | 0 |
| teacher_b1 -> trained_b1 | heldout_musique | -42.4 | [-49.8, -35.0] | 4 / 90 | 0 |
| teacher_b1 -> trained_b1 | heldout_strategyqa | -27.6 | [-37.3, -17.3] | 26 / 77 | 0 |
| teacher_b1 -> trained_b1 | pooled | -49.7 | [-53.8, -45.4] | 33 / 404 | 0 |
| teacher_b1 -> trained_b3 | heldout_2wikimultihopqa | +12.3 | [+2.9, +21.8] | 46 / 25 | 0.017 |
| teacher_b1 -> trained_b3 | heldout_hotpotqa | -8.5 | [-16.9, +0.0] | 27 / 43 | 0.0722 |
| teacher_b1 -> trained_b3 | heldout_musique | -6.4 | [-15.3, +2.5] | 38 / 51 | 0.203 |
| teacher_b1 -> trained_b3 | heldout_strategyqa | +13.0 | [+4.3, +21.6] | 45 / 21 | 0.00427 |
| teacher_b1 -> trained_b3 | pooled | +2.1 | [-2.4, +6.7] | 156 / 140 | 0.383 |
| teacher_b1 -> trained_b5 | heldout_2wikimultihopqa | +16.5 | [+6.5, +26.5] | 52 / 24 | 0.00176 |
| teacher_b1 -> trained_b5 | heldout_hotpotqa | -6.9 | [-14.8, +1.6] | 25 / 38 | 0.13 |
| teacher_b1 -> trained_b5 | heldout_musique | +4.9 | [-4.4, +13.8] | 49 / 39 | 0.337 |
| teacher_b1 -> trained_b5 | heldout_strategyqa | +14.1 | [+5.9, +22.2] | 44 / 18 | 0.0013 |
| teacher_b1 -> trained_b5 | pooled | +6.8 | [+2.4, +11.2] | 170 / 119 | 0.0032 |
| teacher_b1 -> trained_b8 | heldout_2wikimultihopqa | +18.8 | [+9.4, +28.2] | 53 / 21 | 0.000256 |
| teacher_b1 -> trained_b8 | heldout_hotpotqa | -10.1 | [-18.5, -1.6] | 24 / 43 | 0.0271 |
| teacher_b1 -> trained_b8 | heldout_musique | +5.9 | [-2.5, +14.8] | 45 / 33 | 0.213 |
| teacher_b1 -> trained_b8 | heldout_strategyqa | +16.2 | [+8.1, +24.3] | 46 / 16 | 0.000176 |
| teacher_b1 -> trained_b8 | pooled | +7.4 | [+2.9, +11.7] | 168 / 113 | 0.00124 |
| teacher_b3 -> teacher_b5 | heldout_2wikimultihopqa | +2.9 | [-0.6, +6.5] | 7 / 2 | 0.18 |
| teacher_b3 -> teacher_b5 | heldout_hotpotqa | +0.0 | [-3.2, +3.2] | 5 / 5 | 1 |
| teacher_b3 -> teacher_b5 | heldout_musique | +5.4 | [+1.0, +9.8] | 16 / 5 | 0.0266 |
| teacher_b3 -> teacher_b5 | heldout_strategyqa | +0.5 | [-4.3, +5.4] | 10 / 9 | 1 |
| teacher_b3 -> teacher_b5 | pooled | +2.3 | [+0.3, +4.3] | 38 / 21 | 0.0363 |
| teacher_b3 -> teacher_b8 | heldout_2wikimultihopqa | +4.1 | [+1.8, +7.1] | 7 / 0 | 0.0156 |
| teacher_b3 -> teacher_b8 | heldout_hotpotqa | -0.5 | [-3.7, +2.6] | 4 / 5 | 1 |
| teacher_b3 -> teacher_b8 | heldout_musique | +6.9 | [+2.0, +11.8] | 21 / 7 | 0.0125 |
| teacher_b3 -> teacher_b8 | heldout_strategyqa | +1.6 | [-2.7, +5.9] | 10 / 7 | 0.629 |
| teacher_b3 -> teacher_b8 | pooled | +3.1 | [+1.1, +5.2] | 42 / 19 | 0.00444 |
| teacher_b3 -> trained_b1 | heldout_2wikimultihopqa | -86.5 | [-91.8, -80.6] | 1 / 148 | 0 |
| teacher_b3 -> trained_b1 | heldout_hotpotqa | -89.4 | [-93.7, -84.7] | 0 / 169 | 0 |
| teacher_b3 -> trained_b1 | heldout_musique | -66.0 | [-72.9, -59.1] | 2 / 136 | 0 |
| teacher_b3 -> trained_b1 | heldout_strategyqa | -49.2 | [-57.3, -41.1] | 7 / 98 | 0 |
| teacher_b3 -> trained_b1 | pooled | -72.4 | [-75.8, -68.9] | 10 / 551 | 0 |
| teacher_b3 -> trained_b3 | heldout_2wikimultihopqa | -14.7 | [-21.8, -8.2] | 7 / 32 | 7e-05 |
| teacher_b3 -> trained_b3 | heldout_hotpotqa | -27.5 | [-34.4, -21.2] | 2 / 54 | 0 |
| teacher_b3 -> trained_b3 | heldout_musique | -30.0 | [-38.4, -22.2] | 14 / 75 | 0 |
| teacher_b3 -> trained_b3 | heldout_strategyqa | -8.6 | [-15.7, -1.6] | 16 / 32 | 0.0293 |
| teacher_b3 -> trained_b3 | pooled | -20.6 | [-24.2, -16.9] | 39 / 193 | 0 |
| teacher_b3 -> trained_b5 | heldout_2wikimultihopqa | -10.6 | [-17.6, -4.1] | 9 / 27 | 0.00393 |
| teacher_b3 -> trained_b5 | heldout_hotpotqa | -25.9 | [-32.8, -19.6] | 2 / 51 | 0 |
| teacher_b3 -> trained_b5 | heldout_musique | -18.7 | [-26.6, -10.8] | 17 / 55 | 8e-06 |
| teacher_b3 -> trained_b5 | heldout_strategyqa | -7.6 | [-14.1, -1.1] | 13 / 27 | 0.0385 |
| teacher_b3 -> trained_b5 | pooled | -15.9 | [-19.5, -12.3] | 41 / 160 | 0 |
| teacher_b3 -> trained_b8 | heldout_2wikimultihopqa | -8.2 | [-14.7, -1.2] | 11 / 25 | 0.0288 |
| teacher_b3 -> trained_b8 | heldout_hotpotqa | -29.1 | [-36.0, -22.2] | 2 / 57 | 0 |
| teacher_b3 -> trained_b8 | heldout_musique | -17.7 | [-25.1, -10.8] | 12 / 48 | 3e-06 |
| teacher_b3 -> trained_b8 | heldout_strategyqa | -5.4 | [-12.4, +1.6] | 16 / 26 | 0.164 |
| teacher_b3 -> trained_b8 | pooled | -15.4 | [-18.9, -11.8] | 41 / 156 | 0 |
| teacher_b5 -> teacher_b8 | heldout_2wikimultihopqa | +1.2 | [+0.0, +2.9] | 2 / 0 | 0.5 |
| teacher_b5 -> teacher_b8 | heldout_hotpotqa | -0.5 | [-3.2, +2.1] | 3 / 4 | 1 |
| teacher_b5 -> teacher_b8 | heldout_musique | +1.5 | [-2.5, +5.4] | 11 / 8 | 0.648 |
| teacher_b5 -> teacher_b8 | heldout_strategyqa | +1.1 | [-3.2, +5.4] | 10 / 8 | 0.815 |
| teacher_b5 -> teacher_b8 | pooled | +0.8 | [-0.9, +2.5] | 26 / 20 | 0.461 |
| teacher_b5 -> trained_b1 | heldout_2wikimultihopqa | -89.4 | [-94.1, -84.7] | 0 / 152 | 0 |
| teacher_b5 -> trained_b1 | heldout_hotpotqa | -89.4 | [-93.7, -84.7] | 0 / 169 | 0 |
| teacher_b5 -> trained_b1 | heldout_musique | -71.4 | [-77.8, -64.5] | 2 / 147 | 0 |
| teacher_b5 -> trained_b1 | heldout_strategyqa | -49.7 | [-57.8, -41.1] | 9 / 101 | 0 |
| teacher_b5 -> trained_b1 | pooled | -74.7 | [-77.9, -71.4] | 11 / 569 | 0 |
| teacher_b5 -> trained_b3 | heldout_2wikimultihopqa | -17.6 | [-24.1, -11.2] | 4 / 34 | 1e-06 |
| teacher_b5 -> trained_b3 | heldout_hotpotqa | -27.5 | [-34.4, -21.2] | 2 / 54 | 0 |
| teacher_b5 -> trained_b3 | heldout_musique | -35.5 | [-43.4, -27.6] | 11 / 83 | 0 |
| teacher_b5 -> trained_b3 | heldout_strategyqa | -9.2 | [-16.2, -2.2] | 16 / 33 | 0.0213 |
| teacher_b5 -> trained_b3 | pooled | -22.9 | [-26.6, -19.3] | 33 / 204 | 0 |
| teacher_b5 -> trained_b5 | heldout_2wikimultihopqa | -13.5 | [-19.4, -7.6] | 4 / 27 | 3.4e-05 |
| teacher_b5 -> trained_b5 | heldout_hotpotqa | -25.9 | [-32.3, -19.6] | 2 / 51 | 0 |
| teacher_b5 -> trained_b5 | heldout_musique | -24.1 | [-32.0, -16.3] | 14 / 63 | 0 |
| teacher_b5 -> trained_b5 | heldout_strategyqa | -8.1 | [-15.1, -1.1] | 14 / 29 | 0.0315 |
| teacher_b5 -> trained_b5 | pooled | -18.2 | [-21.7, -14.7] | 34 / 170 | 0 |
| teacher_b5 -> trained_b8 | heldout_2wikimultihopqa | -11.2 | [-17.1, -5.3] | 5 / 24 | 0.000546 |
| teacher_b5 -> trained_b8 | heldout_hotpotqa | -29.1 | [-36.0, -22.8] | 1 / 56 | 0 |
| teacher_b5 -> trained_b8 | heldout_musique | -23.2 | [-30.0, -16.3] | 9 / 56 | 0 |
| teacher_b5 -> trained_b8 | heldout_strategyqa | -5.9 | [-13.5, +1.1] | 19 / 30 | 0.152 |
| teacher_b5 -> trained_b8 | pooled | -17.7 | [-21.1, -14.2] | 34 / 166 | 0 |
| teacher_b8 -> trained_b1 | heldout_2wikimultihopqa | -90.6 | [-94.7, -85.9] | 0 / 154 | 0 |
| teacher_b8 -> trained_b1 | heldout_hotpotqa | -88.9 | [-93.1, -84.1] | 0 / 168 | 0 |
| teacher_b8 -> trained_b1 | heldout_musique | -72.9 | [-79.3, -66.5] | 2 / 150 | 0 |
| teacher_b8 -> trained_b1 | heldout_strategyqa | -50.8 | [-58.9, -42.7] | 6 / 100 | 0 |
| teacher_b8 -> trained_b1 | pooled | -75.5 | [-78.7, -72.2] | 8 / 572 | 0 |
| teacher_b8 -> trained_b3 | heldout_2wikimultihopqa | -18.8 | [-25.9, -12.3] | 3 / 35 | 0 |
| teacher_b8 -> trained_b3 | heldout_hotpotqa | -27.0 | [-33.9, -20.6] | 2 / 53 | 0 |
| teacher_b8 -> trained_b3 | heldout_musique | -37.0 | [-44.8, -29.1] | 11 / 86 | 0 |
| teacher_b8 -> trained_b3 | heldout_strategyqa | -10.3 | [-16.8, -3.8] | 11 / 30 | 0.00432 |
| teacher_b8 -> trained_b3 | pooled | -23.7 | [-27.3, -20.1] | 27 / 204 | 0 |
| teacher_b8 -> trained_b5 | heldout_2wikimultihopqa | -14.7 | [-21.2, -8.8] | 4 / 29 | 1.1e-05 |
| teacher_b8 -> trained_b5 | heldout_hotpotqa | -25.4 | [-31.8, -19.1] | 2 / 50 | 0 |
| teacher_b8 -> trained_b5 | heldout_musique | -25.6 | [-34.0, -17.7] | 15 / 67 | 0 |
| teacher_b8 -> trained_b5 | heldout_strategyqa | -9.2 | [-15.1, -3.2] | 9 / 26 | 0.00599 |
| teacher_b8 -> trained_b5 | pooled | -19.0 | [-22.5, -15.5] | 30 / 172 | 0 |
| teacher_b8 -> trained_b8 | heldout_2wikimultihopqa | -12.3 | [-18.2, -6.5] | 4 / 25 | 0.000104 |
| teacher_b8 -> trained_b8 | heldout_hotpotqa | -28.6 | [-35.4, -21.7] | 2 / 56 | 0 |
| teacher_b8 -> trained_b8 | heldout_musique | -24.6 | [-32.0, -17.2] | 9 / 59 | 0 |
| teacher_b8 -> trained_b8 | heldout_strategyqa | -7.0 | [-13.5, -0.5] | 12 / 25 | 0.047 |
| teacher_b8 -> trained_b8 | pooled | -18.5 | [-21.8, -15.0] | 27 / 165 | 0 |
| trained_b1 -> trained_b3 | heldout_2wikimultihopqa | +71.8 | [+64.7, +78.2] | 123 / 1 | 0 |
| trained_b1 -> trained_b3 | heldout_hotpotqa | +61.9 | [+54.5, +68.8] | 118 / 1 | 0 |
| trained_b1 -> trained_b3 | heldout_musique | +36.0 | [+29.1, +42.9] | 74 / 1 | 0 |
| trained_b1 -> trained_b3 | heldout_strategyqa | +40.5 | [+33.0, +48.1] | 76 / 1 | 0 |
| trained_b1 -> trained_b3 | pooled | +51.8 | [+48.1, +55.4] | 391 / 4 | 0 |
| trained_b1 -> trained_b5 | heldout_2wikimultihopqa | +75.9 | [+69.4, +82.3] | 130 / 1 | 0 |
| trained_b1 -> trained_b5 | heldout_hotpotqa | +63.5 | [+56.6, +70.4] | 121 / 1 | 0 |
| trained_b1 -> trained_b5 | heldout_musique | +47.3 | [+40.4, +54.2] | 97 / 1 | 0 |
| trained_b1 -> trained_b5 | heldout_strategyqa | +41.6 | [+33.5, +49.7] | 83 / 6 | 0 |
| trained_b1 -> trained_b5 | pooled | +56.5 | [+52.7, +60.2] | 431 / 9 | 0 |
| trained_b1 -> trained_b8 | heldout_2wikimultihopqa | +78.2 | [+71.8, +84.7] | 134 / 1 | 0 |
| trained_b1 -> trained_b8 | heldout_hotpotqa | +60.3 | [+52.9, +67.2] | 115 / 1 | 0 |
| trained_b1 -> trained_b8 | heldout_musique | +48.3 | [+40.9, +55.2] | 100 / 2 | 0 |
| trained_b1 -> trained_b8 | heldout_strategyqa | +43.8 | [+36.2, +51.3] | 84 / 3 | 0 |
| trained_b1 -> trained_b8 | pooled | +57.0 | [+53.4, +60.8] | 433 / 7 | 0 |
| trained_b3 -> trained_b5 | heldout_2wikimultihopqa | +4.1 | [-0.6, +8.8] | 12 / 5 | 0.143 |
| trained_b3 -> trained_b5 | heldout_hotpotqa | +1.6 | [-3.2, +6.3] | 13 / 10 | 0.678 |
| trained_b3 -> trained_b5 | heldout_musique | +11.3 | [+4.9, +17.7] | 35 / 12 | 0.00109 |
| trained_b3 -> trained_b5 | heldout_strategyqa | +1.1 | [-3.8, +5.9] | 11 / 9 | 0.824 |
| trained_b3 -> trained_b5 | pooled | +4.7 | [+2.0, +7.4] | 71 / 36 | 0.000923 |
| trained_b3 -> trained_b8 | heldout_2wikimultihopqa | +6.5 | [+1.8, +11.2] | 14 / 3 | 0.0127 |
| trained_b3 -> trained_b8 | heldout_hotpotqa | -1.6 | [-7.4, +4.2] | 14 / 17 | 0.72 |
| trained_b3 -> trained_b8 | heldout_musique | +12.3 | [+5.4, +19.2] | 39 / 14 | 0.000802 |
| trained_b3 -> trained_b8 | heldout_strategyqa | +3.2 | [-1.1, +7.6] | 12 / 6 | 0.238 |
| trained_b3 -> trained_b8 | pooled | +5.2 | [+2.3, +8.0] | 79 / 40 | 0.000445 |
| trained_b5 -> trained_b8 | heldout_2wikimultihopqa | +2.4 | [-1.8, +6.5] | 9 / 5 | 0.424 |
| trained_b5 -> trained_b8 | heldout_hotpotqa | -3.2 | [-8.5, +2.1] | 11 / 17 | 0.345 |
| trained_b5 -> trained_b8 | heldout_musique | +1.0 | [-4.9, +6.9] | 20 / 18 | 0.871 |
| trained_b5 -> trained_b8 | heldout_strategyqa | +2.2 | [-2.7, +7.0] | 12 / 8 | 0.503 |
| trained_b5 -> trained_b8 | pooled | +0.5 | [-2.0, +3.2] | 52 / 48 | 0.764 |
