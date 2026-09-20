# Results

## Per arm and test set

| arm | test set | n | done | EM | F1 | cover | judge | doc recall | steps | vol. finish | tokens/ep | latency s | API $ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| base | heldout_2wikimultihopqa | 170 | yes | 0.018 | 0.120 | 0.306 | 0.353 | 0.810 | 2.98 | 0.02 | 5,182 | 25.5 | 0.0000 |
| base | heldout_hotpotqa | 189 | yes | 0.169 | 0.240 | 0.381 | 0.429 | 0.759 | 2.91 | 0.09 | 5,120 | 20.1 | 0.0000 |
| base | heldout_musique | 203 | yes | 0.020 | 0.084 | 0.153 | 0.172 | 0.597 | 3.00 | 0.00 | 5,052 | 17.5 | 0.0000 |
| base | heldout_strategyqa | 185 | yes | 0.000 | 0.011 | 0.097 | 0.151 | 0.815 | 2.98 | 0.02 | 4,923 | 17.0 | 0.0000 |
| cover13 | heldout_2wikimultihopqa | 170 | yes | 0.053 | 0.207 | 0.782 | 0.788 | 0.860 | 2.93 | 0.07 | 5,316 | 18.4 | 0.0000 |
| cover13 | heldout_hotpotqa | 189 | yes | 0.270 | 0.373 | 0.661 | 0.688 | 0.783 | 2.78 | 0.22 | 4,936 | 17.9 | 0.0000 |
| cover13 | heldout_musique | 203 | yes | 0.069 | 0.206 | 0.429 | 0.493 | 0.679 | 2.93 | 0.07 | 5,233 | 18.6 | 0.0000 |
| cover13 | heldout_strategyqa | 185 | yes | 0.000 | 0.034 | 0.686 | 0.724 | 0.834 | 2.95 | 0.05 | 5,161 | 19.9 | 0.0000 |
| cover17 | heldout_2wikimultihopqa | 170 | yes | 0.053 | 0.203 | 0.759 | 0.776 | 0.841 | 2.95 | 0.05 | 5,402 | 23.0 | 0.0000 |
| cover17 | heldout_hotpotqa | 189 | yes | 0.296 | 0.381 | 0.656 | 0.667 | 0.759 | 2.79 | 0.21 | 5,054 | 22.0 | 0.0000 |
| cover17 | heldout_musique | 203 | yes | 0.049 | 0.183 | 0.399 | 0.453 | 0.660 | 2.93 | 0.06 | 5,293 | 23.0 | 0.0000 |
| cover17 | heldout_strategyqa | 185 | yes | 0.000 | 0.036 | 0.681 | 0.730 | 0.833 | 2.91 | 0.09 | 5,113 | 24.7 | 0.0000 |
| cover23 | heldout_2wikimultihopqa | 170 | yes | 0.053 | 0.207 | 0.747 | 0.735 | 0.846 | 2.94 | 0.06 | 5,300 | 22.7 | 0.0000 |
| cover23 | heldout_hotpotqa | 189 | yes | 0.249 | 0.345 | 0.640 | 0.667 | 0.767 | 2.75 | 0.25 | 4,978 | 21.8 | 0.0000 |
| cover23 | heldout_musique | 203 | yes | 0.049 | 0.186 | 0.399 | 0.448 | 0.663 | 2.93 | 0.07 | 5,292 | 23.8 | 0.0000 |
| cover23 | heldout_strategyqa | 185 | yes | 0.000 | 0.034 | 0.670 | 0.703 | 0.818 | 2.89 | 0.11 | 5,050 | 24.4 | 0.0000 |
| judgefilt13 | heldout_2wikimultihopqa | 170 | yes | 0.041 | 0.200 | 0.776 | 0.788 | 0.871 | 2.95 | 0.05 | 5,325 | 22.8 | 0.0000 |
| judgefilt13 | heldout_hotpotqa | 189 | yes | 0.249 | 0.346 | 0.635 | 0.656 | 0.778 | 2.74 | 0.26 | 4,972 | 22.2 | 0.0000 |
| judgefilt13 | heldout_musique | 203 | yes | 0.059 | 0.191 | 0.399 | 0.468 | 0.668 | 2.91 | 0.09 | 5,278 | 23.6 | 0.0000 |
| judgefilt13 | heldout_strategyqa | 185 | yes | 0.000 | 0.031 | 0.519 | 0.708 | 0.821 | 2.92 | 0.07 | 5,193 | 24.2 | 0.0000 |
| judgefilt17 | heldout_2wikimultihopqa | 170 | yes | 0.059 | 0.222 | 0.771 | 0.794 | 0.856 | 2.91 | 0.09 | 5,276 | 22.7 | 0.0000 |
| judgefilt17 | heldout_hotpotqa | 189 | yes | 0.275 | 0.369 | 0.630 | 0.635 | 0.772 | 2.76 | 0.24 | 4,981 | 22.4 | 0.0000 |
| judgefilt17 | heldout_musique | 203 | yes | 0.069 | 0.189 | 0.389 | 0.448 | 0.672 | 2.92 | 0.08 | 5,329 | 23.2 | 0.0000 |
| judgefilt17 | heldout_strategyqa | 185 | yes | 0.000 | 0.030 | 0.530 | 0.714 | 0.817 | 2.95 | 0.05 | 5,292 | 24.7 | 0.0000 |
| judgefilt23 | heldout_2wikimultihopqa | 170 | yes | 0.029 | 0.174 | 0.735 | 0.741 | 0.827 | 2.95 | 0.05 | 5,370 | 23.3 | 0.0000 |
| judgefilt23 | heldout_hotpotqa | 189 | yes | 0.270 | 0.357 | 0.609 | 0.656 | 0.759 | 2.73 | 0.28 | 4,884 | 21.8 | 0.0000 |
| judgefilt23 | heldout_musique | 203 | yes | 0.054 | 0.171 | 0.394 | 0.429 | 0.653 | 2.94 | 0.06 | 5,355 | 23.8 | 0.0000 |
| judgefilt23 | heldout_strategyqa | 185 | yes | 0.000 | 0.032 | 0.524 | 0.697 | 0.818 | 2.91 | 0.09 | 5,140 | 24.7 | 0.0000 |

## Pooled per arm

| arm | test sets | n | EM | F1 | cover | judge | steps | tokens/ep | API $ |
|---|---|---|---|---|---|---|---|---|---|
| base | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.052 | 0.113 | 0.232 | 0.273 | 2.97 | 5,067 | 0.0000 |
| cover13 | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.099 | 0.206 | 0.632 | 0.667 | 2.90 | 5,159 | 0.0000 |
| cover17 | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.100 | 0.201 | 0.616 | 0.649 | 2.89 | 5,213 | 0.0000 |
| cover23 | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.088 | 0.193 | 0.606 | 0.632 | 2.87 | 5,155 | 0.0000 |
| judgefilt13 | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.088 | 0.193 | 0.574 | 0.648 | 2.88 | 5,190 | 0.0000 |
| judgefilt17 | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.102 | 0.203 | 0.572 | 0.640 | 2.88 | 5,220 | 0.0000 |
| judgefilt23 | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.090 | 0.184 | 0.558 | 0.624 | 2.88 | 5,186 | 0.0000 |

## Paired comparisons (judge-correct, b − a)

| a -> b | scope | Δ pts | 95% CI | b wins / a wins | McNemar p |
|---|---|---|---|---|---|
| base -> cover13 | heldout_2wikimultihopqa | +43.5 | [+35.3, +51.8] | 79 / 5 | 0 |
| base -> cover13 | heldout_hotpotqa | +25.9 | [+18.5, +33.3] | 57 / 8 | 0 |
| base -> cover13 | heldout_musique | +32.0 | [+24.6, +39.9] | 74 / 9 | 0 |
| base -> cover13 | heldout_strategyqa | +57.3 | [+49.7, +64.3] | 108 / 2 | 0 |
| base -> cover13 | pooled | +39.4 | [+35.5, +43.4] | 318 / 24 | 0 |
| base -> cover17 | heldout_2wikimultihopqa | +42.4 | [+34.1, +50.6] | 76 / 4 | 0 |
| base -> cover17 | heldout_hotpotqa | +23.8 | [+16.4, +31.2] | 53 / 8 | 0 |
| base -> cover17 | heldout_musique | +28.1 | [+20.2, +36.0] | 69 / 12 | 0 |
| base -> cover17 | heldout_strategyqa | +57.8 | [+50.8, +65.4] | 108 / 1 | 0 |
| base -> cover17 | pooled | +37.6 | [+33.6, +41.6] | 306 / 25 | 0 |
| base -> cover23 | heldout_2wikimultihopqa | +38.2 | [+30.0, +46.5] | 71 / 6 | 0 |
| base -> cover23 | heldout_hotpotqa | +23.8 | [+16.4, +31.2] | 54 / 9 | 0 |
| base -> cover23 | heldout_musique | +27.6 | [+20.2, +35.0] | 65 / 9 | 0 |
| base -> cover23 | heldout_strategyqa | +55.1 | [+47.6, +62.7] | 103 / 1 | 0 |
| base -> cover23 | pooled | +35.9 | [+32.0, +39.8] | 293 / 25 | 0 |
| base -> judgefilt13 | heldout_2wikimultihopqa | +43.5 | [+35.3, +51.8] | 79 / 5 | 0 |
| base -> judgefilt13 | heldout_hotpotqa | +22.8 | [+15.3, +30.2] | 51 / 8 | 0 |
| base -> judgefilt13 | heldout_musique | +29.6 | [+22.2, +37.0] | 70 / 10 | 0 |
| base -> judgefilt13 | heldout_strategyqa | +55.7 | [+48.1, +63.2] | 104 / 1 | 0 |
| base -> judgefilt13 | pooled | +37.5 | [+33.5, +41.4] | 304 / 24 | 0 |
| base -> judgefilt17 | heldout_2wikimultihopqa | +44.1 | [+35.9, +52.3] | 80 / 5 | 0 |
| base -> judgefilt17 | heldout_hotpotqa | +20.6 | [+13.2, +28.6] | 50 / 11 | 0 |
| base -> judgefilt17 | heldout_musique | +27.6 | [+20.2, +35.0] | 65 / 9 | 0 |
| base -> judgefilt17 | heldout_strategyqa | +56.2 | [+48.6, +63.8] | 106 / 2 | 0 |
| base -> judgefilt17 | pooled | +36.7 | [+32.7, +40.6] | 301 / 27 | 0 |
| base -> judgefilt23 | heldout_2wikimultihopqa | +38.8 | [+30.6, +47.1] | 71 / 5 | 0 |
| base -> judgefilt23 | heldout_hotpotqa | +22.8 | [+14.8, +30.7] | 55 / 12 | 0 |
| base -> judgefilt23 | heldout_musique | +25.6 | [+18.2, +33.0] | 62 / 10 | 0 |
| base -> judgefilt23 | heldout_strategyqa | +54.6 | [+47.0, +62.2] | 102 / 1 | 0 |
| base -> judgefilt23 | pooled | +35.1 | [+31.1, +39.0] | 290 / 28 | 0 |
| cover13 -> cover17 | heldout_2wikimultihopqa | -1.2 | [-6.5, +4.1] | 9 / 11 | 0.824 |
| cover13 -> cover17 | heldout_hotpotqa | -2.1 | [-6.9, +2.6] | 9 / 13 | 0.523 |
| cover13 -> cover17 | heldout_musique | -3.9 | [-9.8, +1.5] | 14 / 22 | 0.243 |
| cover13 -> cover17 | heldout_strategyqa | +0.5 | [-3.2, +4.3] | 7 / 6 | 1 |
| cover13 -> cover17 | pooled | -1.7 | [-4.3, +0.7] | 39 / 52 | 0.208 |
| cover13 -> cover23 | heldout_2wikimultihopqa | -5.3 | [-10.6, +0.0] | 7 / 16 | 0.0931 |
| cover13 -> cover23 | heldout_hotpotqa | -2.1 | [-7.4, +2.6] | 10 / 14 | 0.541 |
| cover13 -> cover23 | heldout_musique | -4.4 | [-9.8, +1.0] | 11 / 20 | 0.15 |
| cover13 -> cover23 | heldout_strategyqa | -2.2 | [-5.4, +1.1] | 3 / 7 | 0.344 |
| cover13 -> cover23 | pooled | -3.5 | [-5.9, -1.1] | 31 / 57 | 0.00734 |
| cover13 -> judgefilt13 | heldout_2wikimultihopqa | +0.0 | [-4.7, +4.7] | 9 / 9 | 1 |
| cover13 -> judgefilt13 | heldout_hotpotqa | -3.2 | [-8.5, +2.1] | 9 / 15 | 0.307 |
| cover13 -> judgefilt13 | heldout_musique | -2.5 | [-8.4, +3.5] | 17 / 22 | 0.522 |
| cover13 -> judgefilt13 | heldout_strategyqa | -1.6 | [-5.9, +2.7] | 7 / 10 | 0.629 |
| cover13 -> judgefilt13 | pooled | -1.9 | [-4.5, +0.7] | 42 / 56 | 0.189 |
| cover13 -> judgefilt17 | heldout_2wikimultihopqa | +0.6 | [-4.1, +5.3] | 8 / 7 | 1 |
| cover13 -> judgefilt17 | heldout_hotpotqa | -5.3 | [-10.1, -0.5] | 6 / 16 | 0.0525 |
| cover13 -> judgefilt17 | heldout_musique | -4.4 | [-10.3, +1.5] | 15 / 24 | 0.2 |
| cover13 -> judgefilt17 | heldout_strategyqa | -1.1 | [-5.4, +3.2] | 7 / 9 | 0.804 |
| cover13 -> judgefilt17 | pooled | -2.7 | [-5.2, -0.1] | 36 / 56 | 0.047 |
| cover13 -> judgefilt23 | heldout_2wikimultihopqa | -4.7 | [-10.6, +1.2] | 10 / 18 | 0.185 |
| cover13 -> judgefilt23 | heldout_hotpotqa | -3.2 | [-8.5, +2.1] | 9 / 15 | 0.307 |
| cover13 -> judgefilt23 | heldout_musique | -6.4 | [-12.8, +0.0] | 16 / 29 | 0.0725 |
| cover13 -> judgefilt23 | heldout_strategyqa | -2.7 | [-6.5, +1.1] | 4 / 9 | 0.267 |
| cover13 -> judgefilt23 | pooled | -4.3 | [-7.0, -1.6] | 39 / 71 | 0.00294 |
| cover17 -> cover23 | heldout_2wikimultihopqa | -4.1 | [-10.0, +1.8] | 9 / 16 | 0.23 |
| cover17 -> cover23 | heldout_hotpotqa | +0.0 | [-4.2, +4.2] | 8 / 8 | 1 |
| cover17 -> cover23 | heldout_musique | -0.5 | [-5.9, +4.9] | 16 / 17 | 1 |
| cover17 -> cover23 | heldout_strategyqa | -2.7 | [-7.0, +1.6] | 6 / 11 | 0.332 |
| cover17 -> cover23 | pooled | -1.7 | [-4.3, +0.7] | 39 / 52 | 0.208 |
| cover17 -> judgefilt13 | heldout_2wikimultihopqa | +1.2 | [-4.1, +6.5] | 12 / 10 | 0.832 |
| cover17 -> judgefilt13 | heldout_hotpotqa | -1.1 | [-4.8, +2.6] | 6 / 8 | 0.791 |
| cover17 -> judgefilt13 | heldout_musique | +1.5 | [-4.4, +7.4] | 20 / 17 | 0.743 |
| cover17 -> judgefilt13 | heldout_strategyqa | -2.2 | [-6.5, +2.2] | 6 / 10 | 0.454 |
| cover17 -> judgefilt13 | pooled | -0.1 | [-2.5, +2.3] | 44 / 45 | 1 |
| cover17 -> judgefilt17 | heldout_2wikimultihopqa | +1.8 | [-2.9, +6.5] | 10 / 7 | 0.629 |
| cover17 -> judgefilt17 | heldout_hotpotqa | -3.2 | [-7.9, +1.6] | 8 / 14 | 0.286 |
| cover17 -> judgefilt17 | heldout_musique | -0.5 | [-5.9, +4.9] | 16 / 17 | 1 |
| cover17 -> judgefilt17 | heldout_strategyqa | -1.6 | [-6.5, +3.2] | 9 / 12 | 0.664 |
| cover17 -> judgefilt17 | pooled | -0.9 | [-3.5, +1.6] | 43 / 50 | 0.534 |
| cover17 -> judgefilt23 | heldout_2wikimultihopqa | -3.5 | [-8.8, +1.8] | 8 / 14 | 0.286 |
| cover17 -> judgefilt23 | heldout_hotpotqa | -1.1 | [-5.8, +3.7] | 9 / 11 | 0.824 |
| cover17 -> judgefilt23 | heldout_musique | -2.5 | [-9.4, +4.4] | 23 / 28 | 0.576 |
| cover17 -> judgefilt23 | heldout_strategyqa | -3.2 | [-8.1, +1.6] | 7 / 13 | 0.263 |
| cover17 -> judgefilt23 | pooled | -2.5 | [-5.2, +0.3] | 47 / 66 | 0.09 |
| cover23 -> judgefilt13 | heldout_2wikimultihopqa | +5.3 | [+0.0, +10.6] | 16 / 7 | 0.0931 |
| cover23 -> judgefilt13 | heldout_hotpotqa | -1.1 | [-5.8, +3.7] | 9 / 11 | 0.824 |
| cover23 -> judgefilt13 | heldout_musique | +2.0 | [-3.0, +6.9] | 15 / 11 | 0.557 |
| cover23 -> judgefilt13 | heldout_strategyqa | +0.5 | [-3.2, +4.9] | 8 / 7 | 1 |
| cover23 -> judgefilt13 | pooled | +1.6 | [-0.8, +4.0] | 48 / 36 | 0.23 |
| cover23 -> judgefilt17 | heldout_2wikimultihopqa | +5.9 | [+0.6, +11.2] | 16 / 6 | 0.0525 |
| cover23 -> judgefilt17 | heldout_hotpotqa | -3.2 | [-7.9, +1.6] | 8 / 14 | 0.286 |
| cover23 -> judgefilt17 | heldout_musique | +0.0 | [-5.4, +5.4] | 16 / 16 | 1 |
| cover23 -> judgefilt17 | heldout_strategyqa | +1.1 | [-3.2, +5.4] | 10 / 8 | 0.815 |
| cover23 -> judgefilt17 | pooled | +0.8 | [-1.7, +3.4] | 50 / 44 | 0.606 |
| cover23 -> judgefilt23 | heldout_2wikimultihopqa | +0.6 | [-5.3, +6.5] | 13 / 12 | 1 |
| cover23 -> judgefilt23 | heldout_hotpotqa | -1.1 | [-5.8, +3.7] | 9 / 11 | 0.824 |
| cover23 -> judgefilt23 | heldout_musique | -2.0 | [-8.9, +4.9] | 22 / 26 | 0.665 |
| cover23 -> judgefilt23 | heldout_strategyqa | -0.5 | [-4.9, +3.8] | 7 / 8 | 1 |
| cover23 -> judgefilt23 | pooled | -0.8 | [-3.5, +1.9] | 51 / 57 | 0.631 |
| judgefilt13 -> judgefilt17 | heldout_2wikimultihopqa | +0.6 | [-4.7, +5.9] | 11 / 10 | 1 |
| judgefilt13 -> judgefilt17 | heldout_hotpotqa | -2.1 | [-7.4, +3.2] | 10 / 14 | 0.541 |
| judgefilt13 -> judgefilt17 | heldout_musique | -2.0 | [-7.9, +3.9] | 18 / 22 | 0.636 |
| judgefilt13 -> judgefilt17 | heldout_strategyqa | +0.5 | [-3.8, +4.9] | 9 / 8 | 1 |
| judgefilt13 -> judgefilt17 | pooled | -0.8 | [-3.5, +1.9] | 48 / 54 | 0.621 |
| judgefilt13 -> judgefilt23 | heldout_2wikimultihopqa | -4.7 | [-11.2, +1.2] | 11 / 19 | 0.2 |
| judgefilt13 -> judgefilt23 | heldout_hotpotqa | +0.0 | [-5.3, +5.3] | 12 / 12 | 1 |
| judgefilt13 -> judgefilt23 | heldout_musique | -3.9 | [-10.3, +3.0] | 20 / 28 | 0.312 |
| judgefilt13 -> judgefilt23 | heldout_strategyqa | -1.1 | [-5.4, +3.2] | 7 / 9 | 0.804 |
| judgefilt13 -> judgefilt23 | pooled | -2.4 | [-5.2, +0.4] | 50 / 68 | 0.117 |
| judgefilt17 -> judgefilt23 | heldout_2wikimultihopqa | -5.3 | [-11.2, +0.6] | 9 / 18 | 0.122 |
| judgefilt17 -> judgefilt23 | heldout_hotpotqa | +2.1 | [-2.6, +6.9] | 13 / 9 | 0.523 |
| judgefilt17 -> judgefilt23 | heldout_musique | -2.0 | [-8.9, +4.4] | 22 / 26 | 0.665 |
| judgefilt17 -> judgefilt23 | heldout_strategyqa | -1.6 | [-5.9, +2.7] | 6 / 9 | 0.607 |
| judgefilt17 -> judgefilt23 | pooled | -1.6 | [-4.3, +1.1] | 50 / 62 | 0.299 |
