# Results

## Per arm and test set

| arm | test set | n | done | EM | F1 | cover | judge | doc recall | steps | vol. finish | tokens/ep | latency s | API $ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| base | heldout_2wikimultihopqa | 170 | yes | 0.018 | 0.120 | 0.306 | 0.353 | 0.810 | 2.98 | 0.02 | 5,182 | 25.5 | 0.0000 |
| base | heldout_hotpotqa | 189 | yes | 0.169 | 0.240 | 0.381 | 0.429 | 0.759 | 2.91 | 0.09 | 5,120 | 20.1 | 0.0000 |
| base | heldout_musique | 203 | yes | 0.020 | 0.084 | 0.153 | 0.172 | 0.597 | 3.00 | 0.00 | 5,052 | 17.5 | 0.0000 |
| base | heldout_strategyqa | 185 | yes | 0.000 | 0.011 | 0.097 | 0.151 | 0.815 | 2.98 | 0.02 | 4,923 | 17.0 | 0.0000 |
| full13 | heldout_2wikimultihopqa | 170 | yes | 0.053 | 0.207 | 0.782 | 0.788 | 0.860 | 2.93 | 0.07 | 5,316 | 18.4 | 0.0000 |
| full13 | heldout_hotpotqa | 189 | yes | 0.270 | 0.373 | 0.661 | 0.688 | 0.783 | 2.78 | 0.22 | 4,936 | 17.9 | 0.0000 |
| full13 | heldout_musique | 203 | yes | 0.069 | 0.206 | 0.429 | 0.493 | 0.679 | 2.93 | 0.07 | 5,233 | 18.6 | 0.0000 |
| full13 | heldout_strategyqa | 185 | yes | 0.000 | 0.034 | 0.686 | 0.724 | 0.834 | 2.95 | 0.05 | 5,161 | 19.9 | 0.0000 |
| full17 | heldout_2wikimultihopqa | 170 | yes | 0.053 | 0.203 | 0.759 | 0.776 | 0.841 | 2.95 | 0.05 | 5,402 | 23.0 | 0.0000 |
| full17 | heldout_hotpotqa | 189 | yes | 0.296 | 0.381 | 0.656 | 0.667 | 0.759 | 2.79 | 0.21 | 5,054 | 22.0 | 0.0000 |
| full17 | heldout_musique | 203 | yes | 0.049 | 0.183 | 0.399 | 0.453 | 0.660 | 2.93 | 0.06 | 5,293 | 23.0 | 0.0000 |
| full17 | heldout_strategyqa | 185 | yes | 0.000 | 0.036 | 0.681 | 0.730 | 0.833 | 2.91 | 0.09 | 5,113 | 24.7 | 0.0000 |
| full23 | heldout_2wikimultihopqa | 170 | yes | 0.053 | 0.207 | 0.747 | 0.735 | 0.846 | 2.94 | 0.06 | 5,300 | 22.7 | 0.0000 |
| full23 | heldout_hotpotqa | 189 | yes | 0.249 | 0.345 | 0.640 | 0.667 | 0.767 | 2.75 | 0.25 | 4,978 | 21.8 | 0.0000 |
| full23 | heldout_musique | 203 | yes | 0.049 | 0.186 | 0.399 | 0.448 | 0.663 | 2.93 | 0.07 | 5,292 | 23.8 | 0.0000 |
| full23 | heldout_strategyqa | 185 | yes | 0.000 | 0.034 | 0.670 | 0.703 | 0.818 | 2.89 | 0.11 | 5,050 | 24.4 | 0.0000 |
| noepisode13 | heldout_2wikimultihopqa | 170 | yes | 0.035 | 0.185 | 0.747 | 0.771 | 0.854 | 2.99 | 0.01 | 5,457 | 43.4 | 0.0000 |
| noepisode13 | heldout_hotpotqa | 189 | yes | 0.206 | 0.315 | 0.645 | 0.640 | 0.765 | 2.98 | 0.02 | 5,464 | 44.0 | 0.0000 |
| noepisode13 | heldout_musique | 203 | yes | 0.064 | 0.190 | 0.419 | 0.448 | 0.650 | 2.98 | 0.02 | 5,384 | 44.5 | 0.0000 |
| noepisode13 | heldout_strategyqa | 185 | yes | 0.000 | 0.032 | 0.649 | 0.703 | 0.836 | 2.99 | 0.01 | 5,244 | 31.9 | 0.0000 |
| noepisode17 | heldout_2wikimultihopqa | 170 | yes | 0.024 | 0.180 | 0.765 | 0.776 | 0.843 | 2.99 | 0.01 | 5,404 | 41.4 | 0.0000 |
| noepisode17 | heldout_hotpotqa | 189 | yes | 0.233 | 0.345 | 0.677 | 0.698 | 0.778 | 2.97 | 0.03 | 5,365 | 42.3 | 0.0000 |
| noepisode17 | heldout_musique | 203 | yes | 0.054 | 0.177 | 0.384 | 0.438 | 0.669 | 2.98 | 0.01 | 5,348 | 25.2 | 0.0000 |
| noepisode17 | heldout_strategyqa | 185 | yes | 0.000 | 0.033 | 0.670 | 0.703 | 0.831 | 2.98 | 0.02 | 5,286 | 26.9 | 0.0000 |
| noepisode23 | heldout_2wikimultihopqa | 170 | yes | 0.047 | 0.206 | 0.771 | 0.782 | 0.840 | 2.99 | 0.01 | 5,390 | 40.7 | 0.0000 |
| noepisode23 | heldout_hotpotqa | 189 | yes | 0.233 | 0.337 | 0.651 | 0.682 | 0.770 | 2.98 | 0.02 | 5,461 | 42.2 | 0.0000 |
| noepisode23 | heldout_musique | 203 | yes | 0.049 | 0.176 | 0.404 | 0.473 | 0.667 | 2.98 | 0.01 | 5,371 | 23.1 | 0.0000 |
| noepisode23 | heldout_strategyqa | 185 | yes | 0.000 | 0.036 | 0.719 | 0.757 | 0.813 | 2.99 | 0.01 | 5,304 | 24.6 | 0.0000 |
| notarget13 | heldout_2wikimultihopqa | 170 | yes | 0.035 | 0.194 | 0.782 | 0.788 | 0.831 | 3.00 | 0.00 | 5,499 | 45.6 | 0.0000 |
| notarget13 | heldout_hotpotqa | 189 | yes | 0.243 | 0.343 | 0.640 | 0.651 | 0.780 | 2.96 | 0.04 | 5,298 | 36.1 | 0.0000 |
| notarget13 | heldout_musique | 203 | yes | 0.059 | 0.187 | 0.394 | 0.443 | 0.649 | 2.98 | 0.02 | 5,327 | 43.8 | 0.0000 |
| notarget13 | heldout_strategyqa | 185 | yes | 0.000 | 0.034 | 0.692 | 0.724 | 0.811 | 2.99 | 0.01 | 5,308 | 48.4 | 0.0000 |
| notarget17 | heldout_2wikimultihopqa | 170 | yes | 0.018 | 0.187 | 0.759 | 0.776 | 0.857 | 2.99 | 0.01 | 5,424 | 43.7 | 0.0000 |
| notarget17 | heldout_hotpotqa | 189 | yes | 0.249 | 0.359 | 0.656 | 0.677 | 0.749 | 2.96 | 0.04 | 5,253 | 33.8 | 0.0000 |
| notarget17 | heldout_musique | 203 | yes | 0.059 | 0.187 | 0.379 | 0.443 | 0.647 | 2.98 | 0.01 | 5,382 | 41.2 | 0.0000 |
| notarget17 | heldout_strategyqa | 185 | yes | 0.000 | 0.035 | 0.670 | 0.708 | 0.826 | 2.97 | 0.03 | 5,272 | 45.1 | 0.0000 |
| notarget23 | heldout_2wikimultihopqa | 170 | yes | 0.041 | 0.194 | 0.759 | 0.776 | 0.828 | 3.00 | 0.00 | 5,559 | 23.6 | 0.0000 |
| notarget23 | heldout_hotpotqa | 189 | yes | 0.249 | 0.340 | 0.593 | 0.624 | 0.765 | 2.96 | 0.04 | 5,357 | 23.0 | 0.0000 |
| notarget23 | heldout_musique | 203 | yes | 0.030 | 0.167 | 0.409 | 0.478 | 0.647 | 3.00 | 0.00 | 5,482 | 24.2 | 0.0000 |
| notarget23 | heldout_strategyqa | 185 | yes | 0.000 | 0.035 | 0.708 | 0.724 | 0.828 | 2.98 | 0.01 | 5,338 | 24.5 | 0.0000 |
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

## Pooled per arm

| arm | test sets | n | EM | F1 | cover | judge | steps | tokens/ep | API $ |
|---|---|---|---|---|---|---|---|---|---|
| base | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.052 | 0.113 | 0.232 | 0.273 | 2.97 | 5,067 | 0.0000 |
| full13 | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.099 | 0.206 | 0.632 | 0.667 | 2.90 | 5,159 | 0.0000 |
| full17 | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.100 | 0.201 | 0.616 | 0.649 | 2.89 | 5,213 | 0.0000 |
| full23 | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.088 | 0.193 | 0.606 | 0.632 | 2.87 | 5,155 | 0.0000 |
| noepisode13 | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.078 | 0.181 | 0.608 | 0.633 | 2.98 | 5,387 | 0.0000 |
| noepisode17 | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.079 | 0.184 | 0.616 | 0.647 | 2.98 | 5,350 | 0.0000 |
| noepisode23 | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.083 | 0.189 | 0.628 | 0.667 | 2.99 | 5,382 | 0.0000 |
| notarget13 | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.086 | 0.190 | 0.619 | 0.644 | 2.98 | 5,354 | 0.0000 |
| notarget17 | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.083 | 0.193 | 0.608 | 0.644 | 2.98 | 5,332 | 0.0000 |
| notarget23 | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.080 | 0.184 | 0.609 | 0.644 | 2.98 | 5,432 | 0.0000 |
| unguided13 | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.084 | 0.184 | 0.589 | 0.623 | 2.93 | 4,860 | 0.0000 |
| unguided17 | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.080 | 0.182 | 0.605 | 0.648 | 2.92 | 4,853 | 0.0000 |
| unguided23 | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.080 | 0.181 | 0.594 | 0.626 | 2.94 | 4,896 | 0.0000 |

## Paired comparisons (judge-correct, b − a)

| a -> b | scope | Δ pts | 95% CI | b wins / a wins | McNemar p |
|---|---|---|---|---|---|
| base -> full13 | heldout_2wikimultihopqa | +43.5 | [+35.3, +51.8] | 79 / 5 | 0 |
| base -> full13 | heldout_hotpotqa | +25.9 | [+18.5, +33.3] | 57 / 8 | 0 |
| base -> full13 | heldout_musique | +32.0 | [+24.6, +39.9] | 74 / 9 | 0 |
| base -> full13 | heldout_strategyqa | +57.3 | [+49.7, +64.3] | 108 / 2 | 0 |
| base -> full13 | pooled | +39.4 | [+35.5, +43.4] | 318 / 24 | 0 |
| base -> full17 | heldout_2wikimultihopqa | +42.4 | [+34.1, +50.6] | 76 / 4 | 0 |
| base -> full17 | heldout_hotpotqa | +23.8 | [+16.4, +31.2] | 53 / 8 | 0 |
| base -> full17 | heldout_musique | +28.1 | [+20.2, +36.0] | 69 / 12 | 0 |
| base -> full17 | heldout_strategyqa | +57.8 | [+50.8, +65.4] | 108 / 1 | 0 |
| base -> full17 | pooled | +37.6 | [+33.6, +41.6] | 306 / 25 | 0 |
| base -> full23 | heldout_2wikimultihopqa | +38.2 | [+30.0, +46.5] | 71 / 6 | 0 |
| base -> full23 | heldout_hotpotqa | +23.8 | [+16.4, +31.2] | 54 / 9 | 0 |
| base -> full23 | heldout_musique | +27.6 | [+20.2, +35.0] | 65 / 9 | 0 |
| base -> full23 | heldout_strategyqa | +55.1 | [+47.6, +62.7] | 103 / 1 | 0 |
| base -> full23 | pooled | +35.9 | [+32.0, +39.8] | 293 / 25 | 0 |
| base -> noepisode13 | heldout_2wikimultihopqa | +41.8 | [+33.5, +50.0] | 76 / 5 | 0 |
| base -> noepisode13 | heldout_hotpotqa | +21.2 | [+13.8, +29.1] | 51 / 11 | 0 |
| base -> noepisode13 | heldout_musique | +27.6 | [+20.2, +35.0] | 66 / 10 | 0 |
| base -> noepisode13 | heldout_strategyqa | +55.1 | [+47.6, +62.7] | 104 / 2 | 0 |
| base -> noepisode13 | pooled | +36.0 | [+32.0, +39.9] | 297 / 28 | 0 |
| base -> noepisode17 | heldout_2wikimultihopqa | +42.4 | [+34.1, +50.6] | 78 / 6 | 0 |
| base -> noepisode17 | heldout_hotpotqa | +27.0 | [+19.6, +34.4] | 58 / 7 | 0 |
| base -> noepisode17 | heldout_musique | +26.6 | [+19.2, +34.0] | 65 / 11 | 0 |
| base -> noepisode17 | heldout_strategyqa | +55.1 | [+47.6, +62.7] | 103 / 1 | 0 |
| base -> noepisode17 | pooled | +37.4 | [+33.3, +41.2] | 304 / 25 | 0 |
| base -> noepisode23 | heldout_2wikimultihopqa | +42.9 | [+35.3, +50.6] | 76 / 3 | 0 |
| base -> noepisode23 | heldout_hotpotqa | +25.4 | [+18.5, +32.8] | 55 / 7 | 0 |
| base -> noepisode23 | heldout_musique | +30.0 | [+22.7, +37.4] | 70 / 9 | 0 |
| base -> noepisode23 | heldout_strategyqa | +60.5 | [+53.5, +67.6] | 112 / 0 | 0 |
| base -> noepisode23 | pooled | +39.4 | [+35.5, +43.2] | 313 / 19 | 0 |
| base -> notarget13 | heldout_2wikimultihopqa | +43.5 | [+35.3, +51.8] | 78 / 4 | 0 |
| base -> notarget13 | heldout_hotpotqa | +22.2 | [+14.8, +30.2] | 53 / 11 | 0 |
| base -> notarget13 | heldout_musique | +27.1 | [+19.7, +34.5] | 64 / 9 | 0 |
| base -> notarget13 | heldout_strategyqa | +57.3 | [+50.3, +64.9] | 107 / 1 | 0 |
| base -> notarget13 | pooled | +37.1 | [+33.2, +41.0] | 302 / 25 | 0 |
| base -> notarget17 | heldout_2wikimultihopqa | +42.4 | [+34.7, +50.6] | 76 / 4 | 0 |
| base -> notarget17 | heldout_hotpotqa | +24.9 | [+17.5, +32.3] | 54 / 7 | 0 |
| base -> notarget17 | heldout_musique | +27.1 | [+19.7, +34.5] | 65 / 10 | 0 |
| base -> notarget17 | heldout_strategyqa | +55.7 | [+48.1, +63.2] | 105 / 2 | 0 |
| base -> notarget17 | pooled | +37.1 | [+33.2, +41.0] | 300 / 23 | 0 |
| base -> notarget23 | heldout_2wikimultihopqa | +42.4 | [+34.1, +50.6] | 77 / 5 | 0 |
| base -> notarget23 | heldout_hotpotqa | +19.6 | [+12.2, +27.0] | 47 / 10 | 1e-06 |
| base -> notarget23 | heldout_musique | +30.5 | [+23.2, +38.4] | 72 / 10 | 0 |
| base -> notarget23 | heldout_strategyqa | +57.3 | [+50.3, +64.3] | 106 / 0 | 0 |
| base -> notarget23 | pooled | +37.1 | [+33.1, +41.0] | 302 / 25 | 0 |
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
| full13 -> full17 | heldout_2wikimultihopqa | -1.2 | [-6.5, +4.1] | 9 / 11 | 0.824 |
| full13 -> full17 | heldout_hotpotqa | -2.1 | [-6.9, +2.6] | 9 / 13 | 0.523 |
| full13 -> full17 | heldout_musique | -3.9 | [-9.8, +1.5] | 14 / 22 | 0.243 |
| full13 -> full17 | heldout_strategyqa | +0.5 | [-3.2, +4.3] | 7 / 6 | 1 |
| full13 -> full17 | pooled | -1.7 | [-4.3, +0.7] | 39 / 52 | 0.208 |
| full13 -> full23 | heldout_2wikimultihopqa | -5.3 | [-10.6, +0.0] | 7 / 16 | 0.0931 |
| full13 -> full23 | heldout_hotpotqa | -2.1 | [-7.4, +2.6] | 10 / 14 | 0.541 |
| full13 -> full23 | heldout_musique | -4.4 | [-9.8, +1.0] | 11 / 20 | 0.15 |
| full13 -> full23 | heldout_strategyqa | -2.2 | [-5.4, +1.1] | 3 / 7 | 0.344 |
| full13 -> full23 | pooled | -3.5 | [-5.9, -1.1] | 31 / 57 | 0.00734 |
| full13 -> noepisode13 | heldout_2wikimultihopqa | -1.8 | [-6.5, +2.4] | 6 / 9 | 0.607 |
| full13 -> noepisode13 | heldout_hotpotqa | -4.8 | [-9.5, +0.0] | 6 / 15 | 0.0784 |
| full13 -> noepisode13 | heldout_musique | -4.4 | [-9.8, +1.0] | 12 / 21 | 0.163 |
| full13 -> noepisode13 | heldout_strategyqa | -2.2 | [-6.5, +2.2] | 6 / 10 | 0.454 |
| full13 -> noepisode13 | pooled | -3.4 | [-5.8, -0.9] | 30 / 55 | 0.00884 |
| full13 -> noepisode17 | heldout_2wikimultihopqa | -1.2 | [-5.3, +2.9] | 6 / 8 | 0.791 |
| full13 -> noepisode17 | heldout_hotpotqa | +1.1 | [-2.6, +4.8] | 8 / 6 | 0.791 |
| full13 -> noepisode17 | heldout_musique | -5.4 | [-11.3, +1.0] | 15 / 26 | 0.117 |
| full13 -> noepisode17 | heldout_strategyqa | -2.2 | [-6.5, +2.2] | 7 / 11 | 0.481 |
| full13 -> noepisode17 | pooled | -2.0 | [-4.5, +0.4] | 36 / 51 | 0.133 |
| full13 -> noepisode23 | heldout_2wikimultihopqa | -0.6 | [-5.9, +4.1] | 9 / 10 | 1 |
| full13 -> noepisode23 | heldout_hotpotqa | -0.5 | [-5.8, +4.8] | 12 / 13 | 1 |
| full13 -> noepisode23 | heldout_musique | -2.0 | [-7.9, +3.9] | 17 / 21 | 0.627 |
| full13 -> noepisode23 | heldout_strategyqa | +3.2 | [-1.1, +7.6] | 11 / 5 | 0.21 |
| full13 -> noepisode23 | pooled | +0.0 | [-2.7, +2.5] | 49 / 49 | 1 |
| full13 -> notarget13 | heldout_2wikimultihopqa | +0.0 | [-5.9, +5.9] | 12 / 12 | 1 |
| full13 -> notarget13 | heldout_hotpotqa | -3.7 | [-8.5, +1.1] | 7 / 14 | 0.189 |
| full13 -> notarget13 | heldout_musique | -4.9 | [-10.3, +0.5] | 11 / 21 | 0.11 |
| full13 -> notarget13 | heldout_strategyqa | +0.0 | [-3.2, +3.2] | 4 / 4 | 1 |
| full13 -> notarget13 | pooled | -2.3 | [-4.7, +0.1] | 34 / 51 | 0.0821 |
| full13 -> notarget17 | heldout_2wikimultihopqa | -1.2 | [-6.5, +4.1] | 9 / 11 | 0.824 |
| full13 -> notarget17 | heldout_hotpotqa | -1.1 | [-5.8, +3.7] | 10 / 12 | 0.832 |
| full13 -> notarget17 | heldout_musique | -4.9 | [-10.8, +1.0] | 15 / 25 | 0.154 |
| full13 -> notarget17 | heldout_strategyqa | -1.6 | [-5.4, +1.6] | 4 / 7 | 0.549 |
| full13 -> notarget17 | pooled | -2.3 | [-4.8, +0.3] | 38 / 55 | 0.0966 |
| full13 -> notarget23 | heldout_2wikimultihopqa | -1.2 | [-5.9, +3.5] | 7 / 9 | 0.804 |
| full13 -> notarget23 | heldout_hotpotqa | -6.3 | [-11.6, -1.1] | 7 / 19 | 0.029 |
| full13 -> notarget23 | heldout_musique | -1.5 | [-7.4, +4.4] | 17 / 20 | 0.743 |
| full13 -> notarget23 | heldout_strategyqa | +0.0 | [-3.8, +3.8] | 7 / 7 | 1 |
| full13 -> notarget23 | pooled | -2.3 | [-4.8, +0.1] | 38 / 55 | 0.0966 |
| full13 -> unguided13 | heldout_2wikimultihopqa | -2.4 | [-7.6, +2.9] | 9 / 13 | 0.523 |
| full13 -> unguided13 | heldout_hotpotqa | -7.4 | [-13.2, -2.1] | 8 / 22 | 0.0161 |
| full13 -> unguided13 | heldout_musique | -8.4 | [-14.8, -2.0] | 14 / 31 | 0.0161 |
| full13 -> unguided13 | heldout_strategyqa | +1.1 | [-3.2, +5.4] | 10 / 8 | 0.815 |
| full13 -> unguided13 | pooled | -4.4 | [-7.2, -1.7] | 41 / 74 | 0.00269 |
| full13 -> unguided17 | heldout_2wikimultihopqa | -2.9 | [-8.8, +2.4] | 9 / 14 | 0.405 |
| full13 -> unguided17 | heldout_hotpotqa | -2.6 | [-8.5, +3.2] | 13 / 18 | 0.473 |
| full13 -> unguided17 | heldout_musique | -3.9 | [-11.3, +3.0] | 24 / 32 | 0.35 |
| full13 -> unguided17 | heldout_strategyqa | +2.2 | [-2.2, +6.5] | 10 / 6 | 0.454 |
| full13 -> unguided17 | pooled | -1.9 | [-4.8, +1.1] | 56 / 70 | 0.247 |
| full13 -> unguided23 | heldout_2wikimultihopqa | -4.7 | [-10.0, +0.0] | 6 / 14 | 0.115 |
| full13 -> unguided23 | heldout_hotpotqa | -3.2 | [-9.0, +2.6] | 13 / 19 | 0.377 |
| full13 -> unguided23 | heldout_musique | -6.9 | [-13.8, +0.0] | 19 / 33 | 0.0704 |
| full13 -> unguided23 | heldout_strategyqa | -1.1 | [-5.4, +3.2] | 7 / 9 | 0.804 |
| full13 -> unguided23 | pooled | -4.0 | [-6.8, -1.2] | 45 / 75 | 0.00785 |
| full17 -> full23 | heldout_2wikimultihopqa | -4.1 | [-10.0, +1.8] | 9 / 16 | 0.23 |
| full17 -> full23 | heldout_hotpotqa | +0.0 | [-4.2, +4.2] | 8 / 8 | 1 |
| full17 -> full23 | heldout_musique | -0.5 | [-5.9, +4.9] | 16 / 17 | 1 |
| full17 -> full23 | heldout_strategyqa | -2.7 | [-7.0, +1.6] | 6 / 11 | 0.332 |
| full17 -> full23 | pooled | -1.7 | [-4.3, +0.7] | 39 / 52 | 0.208 |
| full17 -> noepisode13 | heldout_2wikimultihopqa | -0.6 | [-5.9, +4.7] | 10 / 11 | 1 |
| full17 -> noepisode13 | heldout_hotpotqa | -2.6 | [-7.9, +2.1] | 9 / 14 | 0.405 |
| full17 -> noepisode13 | heldout_musique | -0.5 | [-6.9, +5.4] | 20 / 21 | 1 |
| full17 -> noepisode13 | heldout_strategyqa | -2.7 | [-7.0, +1.1] | 5 / 10 | 0.302 |
| full17 -> noepisode13 | pooled | -1.6 | [-4.2, +1.1] | 44 / 56 | 0.271 |
| full17 -> noepisode17 | heldout_2wikimultihopqa | +0.0 | [-4.7, +4.7] | 8 / 8 | 1 |
| full17 -> noepisode17 | heldout_hotpotqa | +3.2 | [-1.6, +7.9] | 13 / 7 | 0.263 |
| full17 -> noepisode17 | heldout_musique | -1.5 | [-7.9, +4.9] | 19 / 22 | 0.755 |
| full17 -> noepisode17 | heldout_strategyqa | -2.7 | [-7.0, +1.1] | 5 / 10 | 0.302 |
| full17 -> noepisode17 | pooled | -0.3 | [-2.8, +2.3] | 45 / 47 | 0.917 |
| full17 -> noepisode23 | heldout_2wikimultihopqa | +0.6 | [-3.5, +5.3] | 8 / 7 | 1 |
| full17 -> noepisode23 | heldout_hotpotqa | +1.6 | [-2.6, +6.3] | 11 / 8 | 0.648 |
| full17 -> noepisode23 | heldout_musique | +2.0 | [-3.9, +7.9] | 20 / 16 | 0.618 |
| full17 -> noepisode23 | heldout_strategyqa | +2.7 | [-1.6, +7.0] | 11 / 6 | 0.332 |
| full17 -> noepisode23 | pooled | +1.7 | [-0.7, +4.2] | 50 / 37 | 0.198 |
| full17 -> notarget13 | heldout_2wikimultihopqa | +1.2 | [-3.5, +5.9] | 10 / 8 | 0.815 |
| full17 -> notarget13 | heldout_hotpotqa | -1.6 | [-6.3, +3.2] | 9 / 12 | 0.664 |
| full17 -> notarget13 | heldout_musique | -1.0 | [-6.4, +4.4] | 16 / 18 | 0.864 |
| full17 -> notarget13 | heldout_strategyqa | -0.5 | [-4.3, +3.8] | 7 / 8 | 1 |
| full17 -> notarget13 | pooled | -0.5 | [-2.9, +1.9] | 42 / 46 | 0.749 |
| full17 -> notarget17 | heldout_2wikimultihopqa | +0.0 | [-5.3, +5.3] | 10 / 10 | 1 |
| full17 -> notarget17 | heldout_hotpotqa | +1.1 | [-3.7, +5.8] | 12 / 10 | 0.832 |
| full17 -> notarget17 | heldout_musique | -1.0 | [-5.9, +3.9] | 13 / 15 | 0.851 |
| full17 -> notarget17 | heldout_strategyqa | -2.2 | [-5.9, +1.6] | 4 / 8 | 0.388 |
| full17 -> notarget17 | pooled | -0.5 | [-2.8, +1.7] | 39 / 43 | 0.741 |
| full17 -> notarget23 | heldout_2wikimultihopqa | +0.0 | [-4.7, +4.7] | 9 / 9 | 1 |
| full17 -> notarget23 | heldout_hotpotqa | -4.2 | [-9.0, +0.5] | 7 / 15 | 0.134 |
| full17 -> notarget23 | heldout_musique | +2.5 | [-3.0, +7.9] | 19 / 14 | 0.487 |
| full17 -> notarget23 | heldout_strategyqa | -0.5 | [-3.8, +3.2] | 5 / 6 | 1 |
| full17 -> notarget23 | pooled | -0.5 | [-2.9, +1.9] | 40 / 44 | 0.744 |
| full17 -> unguided13 | heldout_2wikimultihopqa | -1.2 | [-7.1, +4.1] | 11 / 13 | 0.839 |
| full17 -> unguided13 | heldout_hotpotqa | -5.3 | [-10.6, -0.5] | 7 / 17 | 0.0639 |
| full17 -> unguided13 | heldout_musique | -4.4 | [-11.3, +2.0] | 20 / 29 | 0.253 |
| full17 -> unguided13 | heldout_strategyqa | +0.5 | [-3.8, +5.4] | 10 / 9 | 1 |
| full17 -> unguided13 | pooled | -2.7 | [-5.5, +0.1] | 48 / 68 | 0.0773 |
| full17 -> unguided17 | heldout_2wikimultihopqa | -1.8 | [-7.1, +4.1] | 10 / 13 | 0.678 |
| full17 -> unguided17 | heldout_hotpotqa | -0.5 | [-5.3, +4.2] | 11 / 12 | 1 |
| full17 -> unguided17 | heldout_musique | +0.0 | [-6.4, +6.4] | 22 / 22 | 1 |
| full17 -> unguided17 | heldout_strategyqa | +1.6 | [-2.7, +5.9] | 10 / 7 | 0.629 |
| full17 -> unguided17 | pooled | -0.1 | [-2.8, +2.5] | 53 / 54 | 1 |
| full17 -> unguided23 | heldout_2wikimultihopqa | -3.5 | [-9.4, +1.8] | 9 / 15 | 0.307 |
| full17 -> unguided23 | heldout_hotpotqa | -1.1 | [-5.3, +3.2] | 8 / 10 | 0.815 |
| full17 -> unguided23 | heldout_musique | -3.0 | [-9.4, +3.0] | 17 / 23 | 0.43 |
| full17 -> unguided23 | heldout_strategyqa | -1.6 | [-5.9, +2.7] | 7 / 10 | 0.629 |
| full17 -> unguided23 | pooled | -2.3 | [-4.8, +0.3] | 41 / 58 | 0.107 |
| full23 -> noepisode13 | heldout_2wikimultihopqa | +3.5 | [-1.2, +8.8] | 13 / 7 | 0.263 |
| full23 -> noepisode13 | heldout_hotpotqa | -2.6 | [-8.5, +2.6] | 12 / 17 | 0.458 |
| full23 -> noepisode13 | heldout_musique | +0.0 | [-5.4, +5.4] | 16 / 16 | 1 |
| full23 -> noepisode13 | heldout_strategyqa | +0.0 | [-4.3, +4.3] | 9 / 9 | 1 |
| full23 -> noepisode13 | pooled | +0.1 | [-2.4, +2.8] | 50 / 49 | 1 |
| full23 -> noepisode17 | heldout_2wikimultihopqa | +4.1 | [-0.6, +9.4] | 13 / 6 | 0.167 |
| full23 -> noepisode17 | heldout_hotpotqa | +3.2 | [-1.1, +7.4] | 11 / 5 | 0.21 |
| full23 -> noepisode17 | heldout_musique | -1.0 | [-6.9, +5.4] | 19 / 21 | 0.875 |
| full23 -> noepisode17 | heldout_strategyqa | +0.0 | [-4.3, +4.3] | 8 / 8 | 1 |
| full23 -> noepisode17 | pooled | +1.5 | [-1.1, +4.0] | 51 / 40 | 0.294 |
| full23 -> noepisode23 | heldout_2wikimultihopqa | +4.7 | [+0.0, +9.4] | 13 / 5 | 0.0963 |
| full23 -> noepisode23 | heldout_hotpotqa | +1.6 | [-3.2, +6.3] | 13 / 10 | 0.678 |
| full23 -> noepisode23 | heldout_musique | +2.5 | [-3.5, +8.4] | 20 / 15 | 0.5 |
| full23 -> noepisode23 | heldout_strategyqa | +5.4 | [+1.6, +9.7] | 13 / 3 | 0.0213 |
| full23 -> noepisode23 | pooled | +3.5 | [+0.9, +6.0] | 59 / 33 | 0.00878 |
| full23 -> notarget13 | heldout_2wikimultihopqa | +5.3 | [+0.6, +10.0] | 13 / 4 | 0.049 |
| full23 -> notarget13 | heldout_hotpotqa | -1.6 | [-6.3, +3.2] | 9 / 12 | 0.664 |
| full23 -> notarget13 | heldout_musique | -0.5 | [-5.9, +5.4] | 16 / 17 | 1 |
| full23 -> notarget13 | heldout_strategyqa | +2.2 | [-0.5, +5.4] | 6 / 2 | 0.289 |
| full23 -> notarget13 | pooled | +1.2 | [-1.1, +3.5] | 44 / 35 | 0.368 |
| full23 -> notarget17 | heldout_2wikimultihopqa | +4.1 | [-0.6, +9.4] | 13 / 6 | 0.167 |
| full23 -> notarget17 | heldout_hotpotqa | +1.1 | [-4.2, +6.3] | 14 / 12 | 0.845 |
| full23 -> notarget17 | heldout_musique | -0.5 | [-5.9, +4.4] | 14 / 15 | 1 |
| full23 -> notarget17 | heldout_strategyqa | +0.5 | [-3.2, +4.3] | 7 / 6 | 1 |
| full23 -> notarget17 | pooled | +1.2 | [-1.2, +3.6] | 48 / 39 | 0.391 |
| full23 -> notarget23 | heldout_2wikimultihopqa | +4.1 | [-0.6, +8.8] | 12 / 5 | 0.143 |
| full23 -> notarget23 | heldout_hotpotqa | -4.2 | [-9.5, +0.5] | 8 / 16 | 0.152 |
| full23 -> notarget23 | heldout_musique | +3.0 | [-3.0, +8.9] | 21 / 15 | 0.405 |
| full23 -> notarget23 | heldout_strategyqa | +2.2 | [-1.6, +5.9] | 8 / 4 | 0.388 |
| full23 -> notarget23 | pooled | +1.2 | [-1.2, +3.6] | 49 / 40 | 0.397 |
| full23 -> unguided13 | heldout_2wikimultihopqa | +2.9 | [-1.8, +7.6] | 10 / 5 | 0.302 |
| full23 -> unguided13 | heldout_hotpotqa | -5.3 | [-10.6, +0.0] | 8 / 18 | 0.0755 |
| full23 -> unguided13 | heldout_musique | -3.9 | [-10.8, +3.0] | 22 / 30 | 0.332 |
| full23 -> unguided13 | heldout_strategyqa | +3.2 | [-1.1, +7.6] | 12 / 6 | 0.238 |
| full23 -> unguided13 | pooled | -0.9 | [-3.6, +1.9] | 52 / 59 | 0.569 |
| full23 -> unguided17 | heldout_2wikimultihopqa | +2.4 | [-4.1, +8.2] | 16 / 12 | 0.572 |
| full23 -> unguided17 | heldout_hotpotqa | -0.5 | [-5.3, +4.2] | 11 / 12 | 1 |
| full23 -> unguided17 | heldout_musique | +0.5 | [-6.4, +6.9] | 24 / 23 | 1 |
| full23 -> unguided17 | heldout_strategyqa | +4.3 | [+0.5, +8.6] | 12 / 4 | 0.0768 |
| full23 -> unguided17 | pooled | +1.6 | [-1.2, +4.4] | 63 / 51 | 0.303 |
| full23 -> unguided23 | heldout_2wikimultihopqa | +0.6 | [-5.3, +6.5] | 13 / 12 | 1 |
| full23 -> unguided23 | heldout_hotpotqa | -1.1 | [-6.3, +3.7] | 11 / 13 | 0.839 |
| full23 -> unguided23 | heldout_musique | -2.5 | [-8.9, +3.9] | 20 / 25 | 0.551 |
| full23 -> unguided23 | heldout_strategyqa | +1.1 | [-3.2, +5.4] | 10 / 8 | 0.815 |
| full23 -> unguided23 | pooled | -0.5 | [-3.2, +2.3] | 54 / 58 | 0.777 |
| noepisode13 -> noepisode17 | heldout_2wikimultihopqa | +0.6 | [-4.1, +5.3] | 9 / 8 | 1 |
| noepisode13 -> noepisode17 | heldout_hotpotqa | +5.8 | [+1.1, +10.6] | 16 / 5 | 0.0266 |
| noepisode13 -> noepisode17 | heldout_musique | -1.0 | [-6.9, +4.9] | 17 / 19 | 0.868 |
| noepisode13 -> noepisode17 | heldout_strategyqa | +0.0 | [-3.8, +3.8] | 7 / 7 | 1 |
| noepisode13 -> noepisode17 | pooled | +1.3 | [-1.2, +3.8] | 49 / 39 | 0.337 |
| noepisode13 -> noepisode23 | heldout_2wikimultihopqa | +1.2 | [-4.1, +6.5] | 11 / 9 | 0.824 |
| noepisode13 -> noepisode23 | heldout_hotpotqa | +4.2 | [-0.5, +9.5] | 16 / 8 | 0.152 |
| noepisode13 -> noepisode23 | heldout_musique | +2.5 | [-3.5, +8.4] | 22 / 17 | 0.522 |
| noepisode13 -> noepisode23 | heldout_strategyqa | +5.4 | [+0.5, +10.3] | 16 / 6 | 0.0525 |
| noepisode13 -> noepisode23 | pooled | +3.4 | [+0.7, +6.0] | 65 / 40 | 0.0187 |
| noepisode13 -> notarget13 | heldout_2wikimultihopqa | +1.8 | [-4.1, +7.6] | 14 / 11 | 0.69 |
| noepisode13 -> notarget13 | heldout_hotpotqa | +1.1 | [-3.7, +5.8] | 12 / 10 | 0.832 |
| noepisode13 -> notarget13 | heldout_musique | -0.5 | [-6.4, +5.4] | 17 / 18 | 1 |
| noepisode13 -> notarget13 | heldout_strategyqa | +2.2 | [-2.7, +7.0] | 12 / 8 | 0.503 |
| noepisode13 -> notarget13 | pooled | +1.1 | [-1.6, +3.8] | 55 / 47 | 0.488 |
| noepisode13 -> notarget17 | heldout_2wikimultihopqa | +0.6 | [-4.7, +5.9] | 11 / 10 | 1 |
| noepisode13 -> notarget17 | heldout_hotpotqa | +3.7 | [-1.1, +9.0] | 16 / 9 | 0.23 |
| noepisode13 -> notarget17 | heldout_musique | -0.5 | [-6.4, +5.4] | 19 / 20 | 1 |
| noepisode13 -> notarget17 | heldout_strategyqa | +0.5 | [-3.8, +4.9] | 9 / 8 | 1 |
| noepisode13 -> notarget17 | pooled | +1.1 | [-1.6, +3.8] | 55 / 47 | 0.488 |
| noepisode13 -> notarget23 | heldout_2wikimultihopqa | +0.6 | [-4.7, +5.9] | 10 / 9 | 1 |
| noepisode13 -> notarget23 | heldout_hotpotqa | -1.6 | [-6.3, +3.2] | 10 / 13 | 0.678 |
| noepisode13 -> notarget23 | heldout_musique | +3.0 | [-3.0, +8.9] | 22 / 16 | 0.418 |
| noepisode13 -> notarget23 | heldout_strategyqa | +2.2 | [-1.6, +5.9] | 8 / 4 | 0.388 |
| noepisode13 -> notarget23 | pooled | +1.1 | [-1.5, +3.5] | 50 / 42 | 0.466 |
| noepisode13 -> unguided13 | heldout_2wikimultihopqa | -0.6 | [-5.9, +4.7] | 11 / 12 | 1 |
| noepisode13 -> unguided13 | heldout_hotpotqa | -2.6 | [-8.5, +2.6] | 12 / 17 | 0.458 |
| noepisode13 -> unguided13 | heldout_musique | -3.9 | [-10.8, +3.0] | 20 / 28 | 0.312 |
| noepisode13 -> unguided13 | heldout_strategyqa | +3.2 | [-1.6, +8.1] | 14 / 8 | 0.286 |
| noepisode13 -> unguided13 | pooled | -1.1 | [-4.0, +1.7] | 57 / 65 | 0.526 |
| noepisode13 -> unguided17 | heldout_2wikimultihopqa | -1.2 | [-7.1, +4.7] | 11 / 13 | 0.839 |
| noepisode13 -> unguided17 | heldout_hotpotqa | +2.1 | [-3.7, +7.9] | 18 / 14 | 0.597 |
| noepisode13 -> unguided17 | heldout_musique | +0.5 | [-6.4, +6.9] | 24 / 23 | 1 |
| noepisode13 -> unguided17 | heldout_strategyqa | +4.3 | [+0.5, +8.6] | 11 / 3 | 0.0574 |
| noepisode13 -> unguided17 | pooled | +1.5 | [-1.3, +4.3] | 64 / 53 | 0.355 |
| noepisode13 -> unguided23 | heldout_2wikimultihopqa | -2.9 | [-8.8, +2.9] | 10 / 15 | 0.424 |
| noepisode13 -> unguided23 | heldout_hotpotqa | +1.6 | [-3.7, +6.9] | 14 / 11 | 0.69 |
| noepisode13 -> unguided23 | heldout_musique | -2.5 | [-9.4, +4.4] | 21 / 26 | 0.56 |
| noepisode13 -> unguided23 | heldout_strategyqa | +1.1 | [-3.2, +5.4] | 9 / 7 | 0.804 |
| noepisode13 -> unguided23 | pooled | -0.7 | [-3.5, +2.1] | 54 / 59 | 0.707 |
| noepisode17 -> noepisode23 | heldout_2wikimultihopqa | +0.6 | [-4.1, +5.3] | 9 / 8 | 1 |
| noepisode17 -> noepisode23 | heldout_hotpotqa | -1.6 | [-6.3, +3.2] | 9 / 12 | 0.664 |
| noepisode17 -> noepisode23 | heldout_musique | +3.5 | [-2.0, +9.4] | 21 / 14 | 0.311 |
| noepisode17 -> noepisode23 | heldout_strategyqa | +5.4 | [+1.6, +9.7] | 13 / 3 | 0.0213 |
| noepisode17 -> noepisode23 | pooled | +2.0 | [-0.4, +4.5] | 52 / 37 | 0.137 |
| noepisode17 -> notarget13 | heldout_2wikimultihopqa | +1.2 | [-4.1, +6.5] | 11 / 9 | 0.824 |
| noepisode17 -> notarget13 | heldout_hotpotqa | -4.8 | [-9.0, -0.5] | 4 / 13 | 0.049 |
| noepisode17 -> notarget13 | heldout_musique | +0.5 | [-5.9, +6.9] | 22 / 21 | 1 |
| noepisode17 -> notarget13 | heldout_strategyqa | +2.2 | [-2.2, +7.0] | 12 / 8 | 0.503 |
| noepisode17 -> notarget13 | pooled | -0.3 | [-2.9, +2.4] | 49 / 51 | 0.92 |
| noepisode17 -> notarget17 | heldout_2wikimultihopqa | +0.0 | [-5.3, +5.3] | 10 / 10 | 1 |
| noepisode17 -> notarget17 | heldout_hotpotqa | -2.1 | [-6.3, +2.1] | 7 / 11 | 0.481 |
| noepisode17 -> notarget17 | heldout_musique | +0.5 | [-5.4, +6.4] | 20 / 19 | 1 |
| noepisode17 -> notarget17 | heldout_strategyqa | +0.5 | [-2.7, +4.3] | 6 / 5 | 1 |
| noepisode17 -> notarget17 | pooled | -0.3 | [-2.7, +2.3] | 43 / 45 | 0.915 |
| noepisode17 -> notarget23 | heldout_2wikimultihopqa | +0.0 | [-4.1, +4.1] | 7 / 7 | 1 |
| noepisode17 -> notarget23 | heldout_hotpotqa | -7.4 | [-12.2, -3.2] | 3 / 17 | 0.00258 |
| noepisode17 -> notarget23 | heldout_musique | +3.9 | [-2.0, +9.4] | 21 / 13 | 0.229 |
| noepisode17 -> notarget23 | heldout_strategyqa | +2.2 | [-1.1, +5.9] | 8 / 4 | 0.388 |
| noepisode17 -> notarget23 | pooled | -0.3 | [-2.7, +2.0] | 39 / 41 | 0.911 |
| noepisode17 -> unguided13 | heldout_2wikimultihopqa | -1.2 | [-6.5, +4.1] | 9 / 11 | 0.824 |
| noepisode17 -> unguided13 | heldout_hotpotqa | -8.5 | [-13.8, -3.2] | 5 / 21 | 0.00249 |
| noepisode17 -> unguided13 | heldout_musique | -3.0 | [-8.9, +3.5] | 17 / 23 | 0.43 |
| noepisode17 -> unguided13 | heldout_strategyqa | +3.2 | [-1.1, +7.6] | 11 / 5 | 0.21 |
| noepisode17 -> unguided13 | pooled | -2.4 | [-5.0, +0.1] | 42 / 60 | 0.0918 |
| noepisode17 -> unguided17 | heldout_2wikimultihopqa | -1.8 | [-7.1, +3.5] | 10 / 13 | 0.678 |
| noepisode17 -> unguided17 | heldout_hotpotqa | -3.7 | [-9.0, +1.6] | 9 / 16 | 0.23 |
| noepisode17 -> unguided17 | heldout_musique | +1.5 | [-4.9, +7.9] | 24 / 21 | 0.766 |
| noepisode17 -> unguided17 | heldout_strategyqa | +4.3 | [+0.5, +8.1] | 11 / 3 | 0.0574 |
| noepisode17 -> unguided17 | pooled | +0.1 | [-2.5, +2.8] | 54 / 53 | 1 |
| noepisode17 -> unguided23 | heldout_2wikimultihopqa | -3.5 | [-8.8, +2.4] | 9 / 15 | 0.307 |
| noepisode17 -> unguided23 | heldout_hotpotqa | -4.2 | [-9.5, +1.1] | 10 / 18 | 0.185 |
| noepisode17 -> unguided23 | heldout_musique | -1.5 | [-7.4, +4.4] | 18 / 21 | 0.749 |
| noepisode17 -> unguided23 | heldout_strategyqa | +1.1 | [-3.2, +5.4] | 9 / 7 | 0.804 |
| noepisode17 -> unguided23 | pooled | -2.0 | [-4.8, +0.7] | 46 / 61 | 0.176 |
| noepisode23 -> notarget13 | heldout_2wikimultihopqa | +0.6 | [-4.1, +5.3] | 8 / 7 | 1 |
| noepisode23 -> notarget13 | heldout_hotpotqa | -3.2 | [-7.9, +1.6] | 7 / 13 | 0.263 |
| noepisode23 -> notarget13 | heldout_musique | -3.0 | [-8.9, +3.0] | 15 / 21 | 0.405 |
| noepisode23 -> notarget13 | heldout_strategyqa | -3.2 | [-7.6, +1.1] | 5 / 11 | 0.21 |
| noepisode23 -> notarget13 | pooled | -2.3 | [-4.7, +0.1] | 35 / 52 | 0.0857 |
| noepisode23 -> notarget17 | heldout_2wikimultihopqa | -0.6 | [-5.9, +4.7] | 10 / 11 | 1 |
| noepisode23 -> notarget17 | heldout_hotpotqa | -0.5 | [-5.3, +4.2] | 10 / 11 | 1 |
| noepisode23 -> notarget17 | heldout_musique | -3.0 | [-8.9, +3.0] | 15 / 21 | 0.405 |
| noepisode23 -> notarget17 | heldout_strategyqa | -4.9 | [-9.2, -1.1] | 3 / 12 | 0.0352 |
| noepisode23 -> notarget17 | pooled | -2.3 | [-4.8, +0.3] | 38 / 55 | 0.0966 |
| noepisode23 -> notarget23 | heldout_2wikimultihopqa | -0.6 | [-5.3, +4.1] | 8 / 9 | 1 |
| noepisode23 -> notarget23 | heldout_hotpotqa | -5.8 | [-10.6, -1.1] | 6 / 17 | 0.0347 |
| noepisode23 -> notarget23 | heldout_musique | +0.5 | [-5.4, +6.4] | 20 / 19 | 1 |
| noepisode23 -> notarget23 | heldout_strategyqa | -3.2 | [-7.0, +0.5] | 4 / 10 | 0.18 |
| noepisode23 -> notarget23 | pooled | -2.3 | [-4.8, +0.1] | 38 / 55 | 0.0966 |
| noepisode23 -> unguided13 | heldout_2wikimultihopqa | -1.8 | [-7.1, +3.5] | 9 / 12 | 0.664 |
| noepisode23 -> unguided13 | heldout_hotpotqa | -6.9 | [-12.7, -1.1] | 9 / 22 | 0.0294 |
| noepisode23 -> unguided13 | heldout_musique | -6.4 | [-12.3, -0.5] | 13 / 26 | 0.0533 |
| noepisode23 -> unguided13 | heldout_strategyqa | -2.2 | [-6.5, +2.2] | 7 / 11 | 0.481 |
| noepisode23 -> unguided13 | pooled | -4.4 | [-7.1, -1.7] | 38 / 71 | 0.00203 |
| noepisode23 -> unguided17 | heldout_2wikimultihopqa | -2.4 | [-7.1, +2.4] | 7 / 11 | 0.481 |
| noepisode23 -> unguided17 | heldout_hotpotqa | -2.1 | [-7.9, +3.7] | 13 / 17 | 0.585 |
| noepisode23 -> unguided17 | heldout_musique | -2.0 | [-8.9, +4.9] | 22 / 26 | 0.665 |
| noepisode23 -> unguided17 | heldout_strategyqa | -1.1 | [-5.4, +3.2] | 7 / 9 | 0.804 |
| noepisode23 -> unguided17 | pooled | -1.9 | [-4.7, +0.9] | 49 / 63 | 0.219 |
| noepisode23 -> unguided23 | heldout_2wikimultihopqa | -4.1 | [-9.4, +1.2] | 7 / 14 | 0.189 |
| noepisode23 -> unguided23 | heldout_hotpotqa | -2.6 | [-7.4, +2.1] | 9 / 14 | 0.405 |
| noepisode23 -> unguided23 | heldout_musique | -4.9 | [-10.8, +1.0] | 15 / 25 | 0.154 |
| noepisode23 -> unguided23 | heldout_strategyqa | -4.3 | [-9.2, +1.1] | 8 / 16 | 0.152 |
| noepisode23 -> unguided23 | pooled | -4.0 | [-6.7, -1.3] | 39 / 69 | 0.00502 |
| notarget13 -> notarget17 | heldout_2wikimultihopqa | -1.2 | [-6.5, +4.1] | 10 / 12 | 0.832 |
| notarget13 -> notarget17 | heldout_hotpotqa | +2.6 | [-2.1, +7.4] | 14 / 9 | 0.405 |
| notarget13 -> notarget17 | heldout_musique | +0.0 | [-5.4, +5.4] | 16 / 16 | 1 |
| notarget13 -> notarget17 | heldout_strategyqa | -1.6 | [-5.9, +2.2] | 6 / 9 | 0.607 |
| notarget13 -> notarget17 | pooled | +0.0 | [-2.5, +2.5] | 46 / 46 | 1 |
| notarget13 -> notarget23 | heldout_2wikimultihopqa | -1.2 | [-5.9, +3.5] | 7 / 9 | 0.804 |
| notarget13 -> notarget23 | heldout_hotpotqa | -2.6 | [-6.3, +1.1] | 5 / 10 | 0.302 |
| notarget13 -> notarget23 | heldout_musique | +3.5 | [-2.0, +8.9] | 20 / 13 | 0.296 |
| notarget13 -> notarget23 | heldout_strategyqa | +0.0 | [-4.3, +4.3] | 8 / 8 | 1 |
| notarget13 -> notarget23 | pooled | +0.0 | [-2.4, +2.3] | 40 / 40 | 1 |
| notarget13 -> unguided13 | heldout_2wikimultihopqa | -2.4 | [-7.1, +2.4] | 7 / 11 | 0.481 |
| notarget13 -> unguided13 | heldout_hotpotqa | -3.7 | [-9.5, +2.1] | 12 / 19 | 0.281 |
| notarget13 -> unguided13 | heldout_musique | -3.5 | [-10.3, +3.0] | 20 / 27 | 0.382 |
| notarget13 -> unguided13 | heldout_strategyqa | +1.1 | [-3.2, +5.4] | 9 / 7 | 0.804 |
| notarget13 -> unguided13 | pooled | -2.1 | [-5.0, +0.7] | 48 / 64 | 0.156 |
| notarget13 -> unguided17 | heldout_2wikimultihopqa | -2.9 | [-8.2, +2.4] | 8 / 13 | 0.383 |
| notarget13 -> unguided17 | heldout_hotpotqa | +1.1 | [-4.8, +6.3] | 16 / 14 | 0.856 |
| notarget13 -> unguided17 | heldout_musique | +1.0 | [-5.9, +7.9] | 26 / 24 | 0.888 |
| notarget13 -> unguided17 | heldout_strategyqa | +2.2 | [-2.2, +6.5] | 10 / 6 | 0.454 |
| notarget13 -> unguided17 | pooled | +0.4 | [-2.4, +3.2] | 60 / 57 | 0.853 |
| notarget13 -> unguided23 | heldout_2wikimultihopqa | -4.7 | [-10.0, +0.0] | 5 / 13 | 0.0963 |
| notarget13 -> unguided23 | heldout_hotpotqa | +0.5 | [-4.8, +6.3] | 15 / 14 | 1 |
| notarget13 -> unguided23 | heldout_musique | -2.0 | [-8.9, +4.9] | 22 / 26 | 0.665 |
| notarget13 -> unguided23 | heldout_strategyqa | -1.1 | [-5.4, +3.2] | 8 / 10 | 0.815 |
| notarget13 -> unguided23 | pooled | -1.7 | [-4.5, +1.1] | 50 / 63 | 0.259 |
| notarget17 -> notarget23 | heldout_2wikimultihopqa | +0.0 | [-4.7, +4.7] | 9 / 9 | 1 |
| notarget17 -> notarget23 | heldout_hotpotqa | -5.3 | [-10.6, -0.5] | 7 / 17 | 0.0639 |
| notarget17 -> notarget23 | heldout_musique | +3.5 | [-1.5, +8.4] | 16 / 9 | 0.23 |
| notarget17 -> notarget23 | heldout_strategyqa | +1.6 | [-1.6, +5.4] | 7 / 4 | 0.549 |
| notarget17 -> notarget23 | pooled | +0.0 | [-2.3, +2.3] | 39 / 39 | 1 |
| notarget17 -> unguided13 | heldout_2wikimultihopqa | -1.2 | [-6.5, +4.1] | 9 / 11 | 0.824 |
| notarget17 -> unguided13 | heldout_hotpotqa | -6.3 | [-12.2, -1.1] | 9 / 21 | 0.0428 |
| notarget17 -> unguided13 | heldout_musique | -3.5 | [-9.8, +3.0] | 19 / 26 | 0.371 |
| notarget17 -> unguided13 | heldout_strategyqa | +2.7 | [-1.6, +7.6] | 12 / 7 | 0.359 |
| notarget17 -> unguided13 | pooled | -2.1 | [-5.0, +0.7] | 49 / 65 | 0.16 |
| notarget17 -> unguided17 | heldout_2wikimultihopqa | -1.8 | [-7.6, +4.1] | 12 / 15 | 0.701 |
| notarget17 -> unguided17 | heldout_hotpotqa | -1.6 | [-7.4, +4.2] | 14 / 17 | 0.72 |
| notarget17 -> unguided17 | heldout_musique | +1.0 | [-4.9, +6.9] | 21 / 19 | 0.875 |
| notarget17 -> unguided17 | heldout_strategyqa | +3.8 | [+0.0, +8.1] | 11 / 4 | 0.118 |
| notarget17 -> unguided17 | pooled | +0.4 | [-2.4, +3.2] | 58 / 55 | 0.851 |
| notarget17 -> unguided23 | heldout_2wikimultihopqa | -3.5 | [-10.0, +2.4] | 11 / 17 | 0.345 |
| notarget17 -> unguided23 | heldout_hotpotqa | -2.1 | [-7.4, +3.7] | 12 / 16 | 0.572 |
| notarget17 -> unguided23 | heldout_musique | -2.0 | [-7.9, +3.9] | 17 / 21 | 0.627 |
| notarget17 -> unguided23 | heldout_strategyqa | +0.5 | [-3.8, +4.9] | 9 / 8 | 1 |
| notarget17 -> unguided23 | pooled | -1.7 | [-4.4, +0.9] | 49 / 62 | 0.255 |
| notarget23 -> unguided13 | heldout_2wikimultihopqa | -1.2 | [-5.9, +3.5] | 7 / 9 | 0.804 |
| notarget23 -> unguided13 | heldout_hotpotqa | -1.1 | [-6.3, +3.7] | 11 / 13 | 0.839 |
| notarget23 -> unguided13 | heldout_musique | -6.9 | [-13.3, -0.5] | 15 / 29 | 0.0488 |
| notarget23 -> unguided13 | heldout_strategyqa | +1.1 | [-3.2, +5.4] | 9 / 7 | 0.804 |
| notarget23 -> unguided13 | pooled | -2.1 | [-4.8, +0.4] | 42 / 58 | 0.133 |
| notarget23 -> unguided17 | heldout_2wikimultihopqa | -1.8 | [-7.1, +3.5] | 10 / 13 | 0.678 |
| notarget23 -> unguided17 | heldout_hotpotqa | +3.7 | [-2.1, +9.5] | 19 / 12 | 0.281 |
| notarget23 -> unguided17 | heldout_musique | -2.5 | [-8.9, +3.9] | 19 / 24 | 0.542 |
| notarget23 -> unguided17 | heldout_strategyqa | +2.2 | [-1.6, +5.9] | 8 / 4 | 0.388 |
| notarget23 -> unguided17 | pooled | +0.4 | [-2.3, +3.1] | 56 / 53 | 0.848 |
| notarget23 -> unguided23 | heldout_2wikimultihopqa | -3.5 | [-8.8, +1.2] | 7 / 13 | 0.263 |
| notarget23 -> unguided23 | heldout_hotpotqa | +3.2 | [-2.1, +8.5] | 16 / 10 | 0.327 |
| notarget23 -> unguided23 | heldout_musique | -5.4 | [-11.8, +1.0] | 16 / 27 | 0.126 |
| notarget23 -> unguided23 | heldout_strategyqa | -1.1 | [-5.4, +3.2] | 7 / 9 | 0.804 |
| notarget23 -> unguided23 | pooled | -1.7 | [-4.4, +0.9] | 46 / 59 | 0.241 |
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
| unguided17 -> unguided23 | heldout_2wikimultihopqa | -1.8 | [-7.1, +3.5] | 10 / 13 | 0.678 |
| unguided17 -> unguided23 | heldout_hotpotqa | -0.5 | [-5.3, +4.2] | 10 / 11 | 1 |
| unguided17 -> unguided23 | heldout_musique | -3.0 | [-8.4, +2.5] | 13 / 19 | 0.377 |
| unguided17 -> unguided23 | heldout_strategyqa | -3.2 | [-7.0, +0.5] | 3 / 9 | 0.146 |
| unguided17 -> unguided23 | pooled | -2.1 | [-4.5, +0.3] | 36 / 52 | 0.109 |
