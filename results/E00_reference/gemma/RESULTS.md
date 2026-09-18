# Results

## Per arm and test set

| arm | test set | n | done | EM | F1 | cover | judge | doc recall | steps | vol. finish | tokens/ep | latency s | API $ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| base | heldout_2wikimultihopqa | 170 | yes | 0.006 | 0.112 | 0.288 | 0.371 | 0.818 | 2.98 | 0.02 | 5,232 | 16.9 | 0.0000 |
| base | heldout_hotpotqa | 189 | yes | 0.196 | 0.253 | 0.376 | 0.429 | 0.759 | 2.94 | 0.06 | 5,155 | 13.8 | 0.0000 |
| base | heldout_musique | 203 | yes | 0.030 | 0.090 | 0.138 | 0.148 | 0.608 | 3.00 | 0.00 | 4,988 | 8.3 | 0.0000 |
| base | heldout_strategyqa | 185 | yes | 0.000 | 0.010 | 0.092 | 0.157 | 0.814 | 2.99 | 0.01 | 4,815 | 7.5 | 0.0000 |
| guided | heldout_2wikimultihopqa | 170 | yes | 0.253 | 0.361 | 0.559 | 0.571 | 0.821 | 2.96 | 0.04 | 11,464 | 21.6 | 0.0390 |
| guided | heldout_hotpotqa | 189 | yes | 0.344 | 0.425 | 0.540 | 0.603 | 0.759 | 2.88 | 0.12 | 11,459 | 21.6 | 0.0434 |
| guided | heldout_musique | 203 | yes | 0.113 | 0.247 | 0.315 | 0.369 | 0.605 | 2.98 | 0.01 | 10,486 | 22.3 | 0.0441 |
| guided | heldout_strategyqa | 185 | yes | 0.341 | 0.369 | 0.595 | 0.724 | 0.816 | 2.99 | 0.01 | 10,554 | 22.1 | 0.0408 |
| teacher | heldout_2wikimultihopqa | 170 | yes | 0.224 | 0.362 | 0.841 | 0.841 | — | 2.69 | 0.31 | 3,902 | 0.0 | 0.0264 |
| teacher | heldout_hotpotqa | 189 | yes | 0.455 | 0.549 | 0.735 | 0.783 | — | 2.67 | 0.32 | 3,746 | 0.0 | 0.0275 |
| teacher | heldout_musique | 203 | yes | 0.296 | 0.392 | 0.483 | 0.537 | — | 2.90 | 0.10 | 4,164 | 0.0 | 0.0321 |
| teacher | heldout_strategyqa | 185 | yes | 0.011 | 0.048 | 0.600 | 0.708 | — | 2.75 | 0.25 | 3,723 | 0.0 | 0.0279 |
| trained | heldout_2wikimultihopqa | 170 | yes | 0.359 | 0.506 | 0.806 | 0.824 | 0.885 | 2.90 | 0.10 | 5,644 | 18.8 | 0.0000 |
| trained | heldout_hotpotqa | 189 | yes | 0.354 | 0.431 | 0.582 | 0.640 | 0.794 | 2.79 | 0.21 | 5,247 | 17.5 | 0.0000 |
| trained | heldout_musique | 203 | yes | 0.168 | 0.272 | 0.364 | 0.374 | 0.661 | 2.96 | 0.04 | 5,269 | 16.7 | 0.0000 |
| trained | heldout_strategyqa | 185 | yes | 0.508 | 0.530 | 0.724 | 0.735 | 0.829 | 2.90 | 0.10 | 5,241 | 18.5 | 0.0000 |

## Pooled per arm

| arm | test sets | n | EM | F1 | cover | judge | steps | tokens/ep | API $ |
|---|---|---|---|---|---|---|---|---|---|
| base | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.059 | 0.117 | 0.221 | 0.272 | 2.98 | 5,043 | 0.0000 |
| guided | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.260 | 0.348 | 0.497 | 0.562 | 2.95 | 10,972 | 0.1673 |
| teacher | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.249 | 0.340 | 0.657 | 0.711 | 2.76 | 3,889 | 0.1138 |
| trained | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.343 | 0.430 | 0.609 | 0.633 | 2.89 | 5,342 | 0.0000 |

## Paired comparisons (judge-correct, b − a)

| a -> b | scope | Δ pts | 95% CI | b wins / a wins | McNemar p |
|---|---|---|---|---|---|
| base -> guided | heldout_2wikimultihopqa | +20.0 | [+11.2, +28.8] | 49 / 15 | 2.4e-05 |
| base -> guided | heldout_hotpotqa | +17.5 | [+11.1, +23.8] | 38 / 5 | 0 |
| base -> guided | heldout_musique | +22.2 | [+15.3, +29.1] | 53 / 8 | 0 |
| base -> guided | heldout_strategyqa | +56.8 | [+49.7, +63.8] | 105 / 0 | 0 |
| base -> guided | pooled | +29.0 | [+25.3, +32.8] | 245 / 28 | 0 |
| base -> teacher | heldout_2wikimultihopqa | +47.1 | [+39.4, +54.7] | 83 / 3 | 0 |
| base -> teacher | heldout_hotpotqa | +35.4 | [+28.6, +42.3] | 68 / 1 | 0 |
| base -> teacher | heldout_musique | +38.9 | [+32.0, +45.8] | 82 / 3 | 0 |
| base -> teacher | heldout_strategyqa | +55.1 | [+48.1, +62.2] | 103 / 1 | 0 |
| base -> teacher | pooled | +43.9 | [+40.2, +47.5] | 336 / 8 | 0 |
| base -> trained | heldout_2wikimultihopqa | +45.3 | [+37.6, +52.9] | 79 / 2 | 0 |
| base -> trained | heldout_hotpotqa | +21.2 | [+13.8, +28.6] | 51 / 11 | 0 |
| base -> trained | heldout_musique | +22.7 | [+15.8, +29.6] | 53 / 7 | 0 |
| base -> trained | heldout_strategyqa | +57.8 | [+50.8, +65.4] | 108 / 1 | 0 |
| base -> trained | pooled | +36.1 | [+32.3, +39.9] | 291 / 21 | 0 |
| guided -> teacher | heldout_2wikimultihopqa | +27.1 | [+18.8, +35.3] | 55 / 9 | 0 |
| guided -> teacher | heldout_hotpotqa | +18.0 | [+11.6, +24.3] | 40 / 6 | 0 |
| guided -> teacher | heldout_musique | +16.8 | [+9.4, +24.1] | 50 / 16 | 3.3e-05 |
| guided -> teacher | heldout_strategyqa | -1.6 | [-8.6, +5.4] | 19 / 22 | 0.755 |
| guided -> teacher | pooled | +14.9 | [+11.2, +18.6] | 164 / 53 | 0 |
| guided -> trained | heldout_2wikimultihopqa | +25.3 | [+17.6, +32.9] | 49 / 6 | 0 |
| guided -> trained | heldout_hotpotqa | +3.7 | [-3.2, +10.6] | 25 / 18 | 0.36 |
| guided -> trained | heldout_musique | +0.5 | [-6.4, +6.9] | 24 / 23 | 1 |
| guided -> trained | heldout_strategyqa | +1.1 | [-4.3, +6.5] | 14 / 12 | 0.845 |
| guided -> trained | pooled | +7.1 | [+3.8, +10.4] | 112 / 59 | 6.2e-05 |
| teacher -> trained | heldout_2wikimultihopqa | -1.8 | [-8.2, +4.7] | 14 / 17 | 0.72 |
| teacher -> trained | heldout_hotpotqa | -14.3 | [-20.6, -7.9] | 8 / 35 | 4.2e-05 |
| teacher -> trained | heldout_musique | -16.3 | [-23.2, -9.4] | 13 / 46 | 1.9e-05 |
| teacher -> trained | heldout_strategyqa | +2.7 | [-4.3, +10.3] | 27 / 22 | 0.568 |
| teacher -> trained | pooled | -7.8 | [-11.2, -4.3] | 62 / 120 | 2.1e-05 |
