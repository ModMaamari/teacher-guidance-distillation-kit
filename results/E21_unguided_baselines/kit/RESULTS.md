# Results

## Per arm and test set

| arm | test set | n | done | EM | F1 | cover | judge | doc recall | steps | vol. finish | tokens/ep | latency s | API $ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| base | heldout_2wikimultihopqa | 170 | yes | 0.018 | 0.120 | 0.306 | 0.353 | 0.810 | 2.98 | 0.02 | 5,182 | 25.5 | 0.0000 |
| base | heldout_hotpotqa | 189 | yes | 0.169 | 0.240 | 0.381 | 0.429 | 0.759 | 2.91 | 0.09 | 5,120 | 20.1 | 0.0000 |
| base | heldout_musique | 203 | yes | 0.020 | 0.084 | 0.153 | 0.172 | 0.597 | 3.00 | 0.00 | 5,052 | 17.5 | 0.0000 |
| base | heldout_strategyqa | 185 | yes | 0.000 | 0.011 | 0.097 | 0.151 | 0.815 | 2.98 | 0.02 | 4,923 | 17.0 | 0.0000 |
| selfguided13 | heldout_2wikimultihopqa | 170 | yes | 0.076 | 0.230 | 0.806 | 0.794 | 0.862 | 2.92 | 0.08 | 5,320 | 41.6 | 0.0000 |
| selfguided13 | heldout_hotpotqa | 189 | yes | 0.254 | 0.345 | 0.661 | 0.677 | 0.807 | 2.82 | 0.18 | 5,131 | 39.4 | 0.0000 |
| selfguided13 | heldout_musique | 203 | yes | 0.059 | 0.187 | 0.389 | 0.438 | 0.649 | 2.95 | 0.05 | 5,387 | 41.6 | 0.0000 |
| selfguided13 | heldout_strategyqa | 185 | yes | 0.000 | 0.034 | 0.659 | 0.708 | 0.829 | 2.96 | 0.04 | 5,347 | 43.8 | 0.0000 |
| selfguided17 | heldout_2wikimultihopqa | 170 | yes | 0.059 | 0.208 | 0.747 | 0.765 | 0.847 | 2.97 | 0.03 | 5,362 | 18.7 | 0.0000 |
| selfguided17 | heldout_hotpotqa | 189 | yes | 0.286 | 0.391 | 0.693 | 0.693 | 0.780 | 2.76 | 0.24 | 4,992 | 24.2 | 0.0000 |
| selfguided17 | heldout_musique | 203 | yes | 0.049 | 0.184 | 0.394 | 0.424 | 0.653 | 2.94 | 0.06 | 5,253 | 19.1 | 0.0000 |
| selfguided17 | heldout_strategyqa | 185 | yes | 0.000 | 0.035 | 0.665 | 0.692 | 0.840 | 2.96 | 0.04 | 5,324 | 21.9 | 0.0000 |
| selfguided23 | heldout_2wikimultihopqa | 170 | yes | 0.053 | 0.224 | 0.788 | 0.782 | 0.862 | 2.92 | 0.08 | 5,246 | 45.0 | 0.0000 |
| selfguided23 | heldout_hotpotqa | 189 | yes | 0.286 | 0.388 | 0.630 | 0.661 | 0.788 | 2.82 | 0.18 | 5,063 | 42.0 | 0.0000 |
| selfguided23 | heldout_musique | 203 | yes | 0.108 | 0.224 | 0.379 | 0.409 | 0.663 | 2.94 | 0.06 | 5,274 | 46.5 | 0.0000 |
| selfguided23 | heldout_strategyqa | 185 | yes | 0.000 | 0.034 | 0.632 | 0.670 | 0.830 | 2.94 | 0.06 | 5,290 | 47.3 | 0.0000 |
| teacherguided13 | heldout_2wikimultihopqa | 170 | yes | 0.312 | 0.479 | 0.782 | 0.788 | 0.884 | 2.92 | 0.08 | 5,689 | 19.6 | 0.0000 |
| teacherguided13 | heldout_hotpotqa | 189 | yes | 0.328 | 0.421 | 0.587 | 0.640 | 0.791 | 2.87 | 0.13 | 5,324 | 15.6 | 0.0000 |
| teacherguided13 | heldout_musique | 203 | yes | 0.168 | 0.272 | 0.360 | 0.399 | 0.654 | 2.94 | 0.05 | 5,239 | 16.7 | 0.0000 |
| teacherguided13 | heldout_strategyqa | 185 | yes | 0.486 | 0.507 | 0.697 | 0.697 | 0.810 | 2.89 | 0.11 | 5,150 | 17.2 | 0.0000 |
| teacherguided17 | heldout_2wikimultihopqa | 170 | yes | 0.294 | 0.452 | 0.747 | 0.753 | 0.863 | 2.92 | 0.08 | 5,603 | 43.2 | 0.0000 |
| teacherguided17 | heldout_hotpotqa | 189 | yes | 0.344 | 0.427 | 0.582 | 0.614 | 0.783 | 2.88 | 0.12 | 5,384 | 41.2 | 0.0000 |
| teacherguided17 | heldout_musique | 203 | yes | 0.148 | 0.261 | 0.335 | 0.355 | 0.661 | 2.96 | 0.04 | 5,236 | 38.1 | 0.0000 |
| teacherguided17 | heldout_strategyqa | 185 | yes | 0.395 | 0.418 | 0.643 | 0.649 | 0.825 | 2.88 | 0.12 | 5,265 | 26.9 | 0.0000 |
| teacherguided23 | heldout_2wikimultihopqa | 170 | yes | 0.324 | 0.474 | 0.747 | 0.753 | 0.847 | 2.90 | 0.10 | 5,570 | 25.9 | 0.0000 |
| teacherguided23 | heldout_hotpotqa | 189 | yes | 0.349 | 0.423 | 0.582 | 0.630 | 0.794 | 2.84 | 0.16 | 5,251 | 25.5 | 0.0000 |
| teacherguided23 | heldout_musique | 203 | yes | 0.163 | 0.276 | 0.355 | 0.379 | 0.653 | 2.95 | 0.05 | 5,227 | 22.8 | 0.0000 |
| teacherguided23 | heldout_strategyqa | 185 | yes | 0.432 | 0.455 | 0.665 | 0.670 | 0.818 | 2.85 | 0.15 | 5,157 | 25.0 | 0.0000 |
| teacherrollouts13 | heldout_2wikimultihopqa | 170 | yes | 0.212 | 0.346 | 0.841 | 0.859 | 0.918 | 2.83 | 0.17 | 4,968 | 27.1 | 0.0000 |
| teacherrollouts13 | heldout_hotpotqa | 189 | yes | 0.407 | 0.467 | 0.635 | 0.682 | 0.852 | 2.95 | 0.05 | 5,138 | 22.2 | 0.0000 |
| teacherrollouts13 | heldout_musique | 203 | yes | 0.266 | 0.371 | 0.453 | 0.497 | 0.782 | 2.96 | 0.04 | 5,208 | 23.1 | 0.0000 |
| teacherrollouts13 | heldout_strategyqa | 185 | yes | 0.000 | 0.037 | 0.708 | 0.703 | 0.854 | 2.94 | 0.06 | 4,982 | 26.7 | 0.0000 |
| teacherrollouts17 | heldout_2wikimultihopqa | 170 | yes | 0.212 | 0.349 | 0.859 | 0.859 | 0.928 | 2.86 | 0.14 | 5,001 | 53.0 | 0.0000 |
| teacherrollouts17 | heldout_hotpotqa | 189 | yes | 0.402 | 0.466 | 0.630 | 0.661 | 0.847 | 2.95 | 0.05 | 5,105 | 42.3 | 0.0000 |
| teacherrollouts17 | heldout_musique | 203 | yes | 0.251 | 0.342 | 0.438 | 0.493 | 0.790 | 2.99 | 0.01 | 5,248 | 41.5 | 0.0000 |
| teacherrollouts17 | heldout_strategyqa | 185 | yes | 0.000 | 0.037 | 0.708 | 0.697 | 0.847 | 2.95 | 0.05 | 5,001 | 43.5 | 0.0000 |
| teacherrollouts23 | heldout_2wikimultihopqa | 170 | yes | 0.194 | 0.341 | 0.859 | 0.859 | 0.928 | 2.84 | 0.16 | 4,979 | 28.7 | 0.0000 |
| teacherrollouts23 | heldout_hotpotqa | 189 | yes | 0.413 | 0.477 | 0.677 | 0.682 | 0.865 | 2.93 | 0.07 | 5,080 | 22.5 | 0.0000 |
| teacherrollouts23 | heldout_musique | 203 | yes | 0.227 | 0.349 | 0.483 | 0.532 | 0.790 | 2.98 | 0.02 | 5,233 | 21.6 | 0.0000 |
| teacherrollouts23 | heldout_strategyqa | 185 | yes | 0.000 | 0.038 | 0.757 | 0.757 | 0.862 | 2.94 | 0.06 | 5,023 | 25.7 | 0.0000 |
| unguided13 | heldout_2wikimultihopqa | 170 | yes | 0.047 | 0.196 | 0.747 | 0.759 | 0.818 | 2.97 | 0.03 | 5,042 | 16.1 | 0.0000 |
| unguided13 | heldout_hotpotqa | 189 | yes | 0.249 | 0.337 | 0.635 | 0.645 | 0.767 | 2.87 | 0.13 | 4,916 | 14.8 | 0.0000 |
| unguided13 | heldout_musique | 203 | yes | 0.035 | 0.163 | 0.364 | 0.399 | 0.610 | 2.96 | 0.04 | 4,715 | 14.8 | 0.0000 |
| unguided13 | heldout_strategyqa | 185 | yes | 0.000 | 0.035 | 0.638 | 0.686 | 0.822 | 2.97 | 0.02 | 4,835 | 16.4 | 0.0000 |
| unguided17 | heldout_2wikimultihopqa | 170 | yes | 0.047 | 0.191 | 0.759 | 0.753 | 0.824 | 2.97 | 0.03 | 5,128 | 21.0 | 0.0000 |
| unguided17 | heldout_hotpotqa | 189 | yes | 0.238 | 0.339 | 0.614 | 0.640 | 0.757 | 2.88 | 0.12 | 4,908 | 20.1 | 0.0000 |
| unguided17 | heldout_musique | 203 | yes | 0.039 | 0.164 | 0.379 | 0.389 | 0.636 | 2.95 | 0.05 | 4,729 | 19.8 | 0.0000 |
| unguided17 | heldout_strategyqa | 185 | yes | 0.000 | 0.035 | 0.659 | 0.719 | 0.813 | 2.96 | 0.03 | 4,799 | 21.2 | 0.0000 |
| unguided23 | heldout_2wikimultihopqa | 170 | yes | 0.047 | 0.199 | 0.759 | 0.765 | 0.840 | 2.99 | 0.01 | 5,106 | 34.7 | 0.0000 |
| unguided23 | heldout_hotpotqa | 189 | yes | 0.254 | 0.341 | 0.630 | 0.640 | 0.767 | 2.86 | 0.14 | 4,811 | 33.3 | 0.0000 |
| unguided23 | heldout_musique | 203 | yes | 0.044 | 0.175 | 0.374 | 0.424 | 0.605 | 2.96 | 0.04 | 4,774 | 32.3 | 0.0000 |
| unguided23 | heldout_strategyqa | 185 | yes | 0.000 | 0.036 | 0.686 | 0.719 | 0.821 | 2.97 | 0.03 | 4,769 | 34.9 | 0.0000 |

## Pooled per arm

| arm | test sets | n | EM | F1 | cover | judge | steps | tokens/ep | API $ |
|---|---|---|---|---|---|---|---|---|---|
| base | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.052 | 0.113 | 0.232 | 0.273 | 2.97 | 5,067 | 0.0000 |
| selfguided13 | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.098 | 0.199 | 0.620 | 0.647 | 2.91 | 5,297 | 0.0000 |
| selfguided17 | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.099 | 0.205 | 0.617 | 0.636 | 2.91 | 5,229 | 0.0000 |
| selfguided23 | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.114 | 0.218 | 0.598 | 0.623 | 2.90 | 5,218 | 0.0000 |
| teacherguided13 | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.320 | 0.415 | 0.597 | 0.623 | 2.91 | 5,341 | 0.0000 |
| teacherguided17 | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.292 | 0.386 | 0.568 | 0.584 | 2.91 | 5,364 | 0.0000 |
| teacherguided23 | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.313 | 0.402 | 0.578 | 0.600 | 2.88 | 5,294 | 0.0000 |
| teacherrollouts13 | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.224 | 0.307 | 0.651 | 0.677 | 2.92 | 5,080 | 0.0000 |
| teacherrollouts17 | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.218 | 0.299 | 0.649 | 0.669 | 2.94 | 5,094 | 0.0000 |
| teacherrollouts23 | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.210 | 0.302 | 0.685 | 0.700 | 2.92 | 5,084 | 0.0000 |
| unguided13 | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.083 | 0.183 | 0.588 | 0.615 | 2.94 | 4,870 | 0.0000 |
| unguided17 | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.082 | 0.182 | 0.594 | 0.617 | 2.94 | 4,882 | 0.0000 |
| unguided23 | heldout_2wikimultihopqa, heldout_hotpotqa, heldout_musique, heldout_strategyqa | 747 | 0.087 | 0.188 | 0.604 | 0.629 | 2.94 | 4,858 | 0.0000 |

## Paired comparisons (judge-correct, b − a)

| a -> b | scope | Δ pts | 95% CI | b wins / a wins | McNemar p |
|---|---|---|---|---|---|
| base -> selfguided13 | heldout_2wikimultihopqa | +44.1 | [+36.5, +51.8] | 78 / 3 | 0 |
| base -> selfguided13 | heldout_hotpotqa | +24.9 | [+18.0, +32.3] | 53 / 6 | 0 |
| base -> selfguided13 | heldout_musique | +26.6 | [+19.7, +34.0] | 63 / 9 | 0 |
| base -> selfguided13 | heldout_strategyqa | +55.7 | [+48.1, +63.2] | 105 / 2 | 0 |
| base -> selfguided13 | pooled | +37.4 | [+33.5, +41.2] | 299 / 20 | 0 |
| base -> selfguided17 | heldout_2wikimultihopqa | +41.2 | [+32.9, +49.4] | 74 / 4 | 0 |
| base -> selfguided17 | heldout_hotpotqa | +26.5 | [+19.6, +33.3] | 54 / 4 | 0 |
| base -> selfguided17 | heldout_musique | +25.1 | [+17.7, +32.5] | 61 / 10 | 0 |
| base -> selfguided17 | heldout_strategyqa | +54.0 | [+46.5, +61.6] | 102 / 2 | 0 |
| base -> selfguided17 | pooled | +36.3 | [+32.5, +40.2] | 291 / 20 | 0 |
| base -> selfguided23 | heldout_2wikimultihopqa | +42.9 | [+34.7, +51.2] | 77 / 4 | 0 |
| base -> selfguided23 | heldout_hotpotqa | +23.3 | [+15.9, +30.7] | 52 / 8 | 0 |
| base -> selfguided23 | heldout_musique | +23.6 | [+16.3, +31.0] | 61 / 13 | 0 |
| base -> selfguided23 | heldout_strategyqa | +51.9 | [+43.8, +59.5] | 100 / 4 | 0 |
| base -> selfguided23 | pooled | +34.9 | [+30.9, +38.8] | 290 / 29 | 0 |
| base -> teacherguided13 | heldout_2wikimultihopqa | +43.5 | [+35.3, +51.2] | 77 / 3 | 0 |
| base -> teacherguided13 | heldout_hotpotqa | +21.2 | [+14.3, +28.6] | 48 / 8 | 0 |
| base -> teacherguided13 | heldout_musique | +22.7 | [+15.8, +29.6] | 55 / 9 | 0 |
| base -> teacherguided13 | heldout_strategyqa | +54.6 | [+47.0, +62.2] | 103 / 2 | 0 |
| base -> teacherguided13 | pooled | +34.9 | [+31.1, +38.8] | 283 / 22 | 0 |
| base -> teacherguided17 | heldout_2wikimultihopqa | +40.0 | [+31.8, +48.2] | 74 / 6 | 0 |
| base -> teacherguided17 | heldout_hotpotqa | +18.5 | [+11.1, +25.9] | 48 / 13 | 8e-06 |
| base -> teacherguided17 | heldout_musique | +18.2 | [+10.8, +25.6] | 52 / 15 | 6e-06 |
| base -> teacherguided17 | heldout_strategyqa | +49.7 | [+42.2, +57.3] | 95 / 3 | 0 |
| base -> teacherguided17 | pooled | +31.1 | [+27.0, +35.1] | 269 / 37 | 0 |
| base -> teacherguided23 | heldout_2wikimultihopqa | +40.0 | [+31.8, +48.2] | 72 / 4 | 0 |
| base -> teacherguided23 | heldout_hotpotqa | +20.1 | [+13.2, +27.5] | 47 / 9 | 0 |
| base -> teacherguided23 | heldout_musique | +20.7 | [+13.8, +28.1] | 53 / 11 | 0 |
| base -> teacherguided23 | heldout_strategyqa | +51.9 | [+44.3, +59.5] | 97 / 1 | 0 |
| base -> teacherguided23 | pooled | +32.7 | [+28.8, +36.4] | 269 / 25 | 0 |
| base -> teacherrollouts13 | heldout_2wikimultihopqa | +50.6 | [+42.9, +58.2] | 86 / 0 | 0 |
| base -> teacherrollouts13 | heldout_hotpotqa | +25.4 | [+17.5, +33.3] | 60 / 12 | 0 |
| base -> teacherrollouts13 | heldout_musique | +32.5 | [+25.1, +39.9] | 75 / 9 | 0 |
| base -> teacherrollouts13 | heldout_strategyqa | +55.1 | [+48.1, +62.7] | 103 / 1 | 0 |
| base -> teacherrollouts13 | pooled | +40.4 | [+36.4, +44.3] | 324 / 22 | 0 |
| base -> teacherrollouts17 | heldout_2wikimultihopqa | +50.6 | [+42.9, +58.2] | 87 / 1 | 0 |
| base -> teacherrollouts17 | heldout_hotpotqa | +23.3 | [+15.3, +31.2] | 55 / 11 | 0 |
| base -> teacherrollouts17 | heldout_musique | +32.0 | [+24.6, +39.4] | 74 / 9 | 0 |
| base -> teacherrollouts17 | heldout_strategyqa | +54.6 | [+47.0, +62.2] | 104 / 3 | 0 |
| base -> teacherrollouts17 | pooled | +39.6 | [+35.6, +43.6] | 320 / 24 | 0 |
| base -> teacherrollouts23 | heldout_2wikimultihopqa | +50.6 | [+42.9, +58.2] | 87 / 1 | 0 |
| base -> teacherrollouts23 | heldout_hotpotqa | +25.4 | [+17.5, +33.3] | 57 / 9 | 0 |
| base -> teacherrollouts23 | heldout_musique | +36.0 | [+28.6, +43.4] | 79 / 6 | 0 |
| base -> teacherrollouts23 | heldout_strategyqa | +60.5 | [+52.4, +68.1] | 117 / 5 | 0 |
| base -> teacherrollouts23 | pooled | +42.7 | [+38.7, +46.5] | 340 / 21 | 0 |
| base -> unguided13 | heldout_2wikimultihopqa | +40.6 | [+32.4, +48.8] | 74 / 5 | 0 |
| base -> unguided13 | heldout_hotpotqa | +21.7 | [+14.8, +29.1] | 48 / 7 | 0 |
| base -> unguided13 | heldout_musique | +22.7 | [+15.8, +29.6] | 54 / 8 | 0 |
| base -> unguided13 | heldout_strategyqa | +53.5 | [+46.0, +61.1] | 100 / 1 | 0 |
| base -> unguided13 | pooled | +34.1 | [+30.4, +38.0] | 276 / 21 | 0 |
| base -> unguided17 | heldout_2wikimultihopqa | +40.0 | [+31.8, +48.2] | 73 / 5 | 0 |
| base -> unguided17 | heldout_hotpotqa | +21.2 | [+14.3, +28.6] | 48 / 8 | 0 |
| base -> unguided17 | heldout_musique | +21.7 | [+14.8, +28.6] | 52 / 8 | 0 |
| base -> unguided17 | heldout_strategyqa | +56.8 | [+49.2, +64.3] | 106 / 1 | 0 |
| base -> unguided17 | pooled | +34.4 | [+30.5, +38.3] | 279 / 22 | 0 |
| base -> unguided23 | heldout_2wikimultihopqa | +41.2 | [+32.9, +49.4] | 75 / 5 | 0 |
| base -> unguided23 | heldout_hotpotqa | +21.2 | [+14.3, +28.0] | 47 / 7 | 0 |
| base -> unguided23 | heldout_musique | +25.1 | [+18.2, +32.5] | 59 / 8 | 0 |
| base -> unguided23 | heldout_strategyqa | +56.8 | [+49.2, +64.3] | 107 / 2 | 0 |
| base -> unguided23 | pooled | +35.6 | [+31.7, +39.5] | 288 / 22 | 0 |
| selfguided13 -> selfguided17 | heldout_2wikimultihopqa | -2.9 | [-9.4, +3.5] | 12 / 17 | 0.458 |
| selfguided13 -> selfguided17 | heldout_hotpotqa | +1.6 | [-3.2, +6.9] | 14 / 11 | 0.69 |
| selfguided13 -> selfguided17 | heldout_musique | -1.5 | [-7.9, +4.9] | 20 / 23 | 0.761 |
| selfguided13 -> selfguided17 | heldout_strategyqa | -1.6 | [-6.5, +3.2] | 8 / 11 | 0.648 |
| selfguided13 -> selfguided17 | pooled | -1.1 | [-3.9, +1.7] | 54 / 62 | 0.516 |
| selfguided13 -> selfguided23 | heldout_2wikimultihopqa | -1.2 | [-5.9, +3.5] | 7 / 9 | 0.804 |
| selfguided13 -> selfguided23 | heldout_hotpotqa | -1.6 | [-6.3, +2.6] | 8 / 11 | 0.648 |
| selfguided13 -> selfguided23 | heldout_musique | -3.0 | [-8.9, +3.0] | 15 / 21 | 0.405 |
| selfguided13 -> selfguided23 | heldout_strategyqa | -3.8 | [-8.6, +1.1] | 7 / 14 | 0.189 |
| selfguided13 -> selfguided23 | pooled | -2.4 | [-5.0, +0.1] | 37 / 55 | 0.0758 |
| selfguided13 -> teacherguided13 | heldout_2wikimultihopqa | -0.6 | [-6.5, +5.3] | 13 / 14 | 1 |
| selfguided13 -> teacherguided13 | heldout_hotpotqa | -3.7 | [-9.5, +2.1] | 13 / 20 | 0.296 |
| selfguided13 -> teacherguided13 | heldout_musique | -3.9 | [-10.3, +2.5] | 18 / 26 | 0.291 |
| selfguided13 -> teacherguided13 | heldout_strategyqa | -1.1 | [-7.0, +4.9] | 16 / 18 | 0.864 |
| selfguided13 -> teacherguided13 | pooled | -2.4 | [-5.5, +0.8] | 60 / 78 | 0.148 |
| selfguided13 -> teacherguided17 | heldout_2wikimultihopqa | -4.1 | [-10.6, +1.8] | 11 / 18 | 0.265 |
| selfguided13 -> teacherguided17 | heldout_hotpotqa | -6.3 | [-12.2, -0.5] | 11 / 23 | 0.0576 |
| selfguided13 -> teacherguided17 | heldout_musique | -8.4 | [-15.3, -2.0] | 16 / 33 | 0.0213 |
| selfguided13 -> teacherguided17 | heldout_strategyqa | -5.9 | [-13.0, +0.5] | 15 / 26 | 0.117 |
| selfguided13 -> teacherguided17 | pooled | -6.3 | [-9.5, -3.1] | 53 / 100 | 0.00018 |
| selfguided13 -> teacherguided23 | heldout_2wikimultihopqa | -4.1 | [-10.0, +1.8] | 10 / 17 | 0.248 |
| selfguided13 -> teacherguided23 | heldout_hotpotqa | -4.8 | [-10.1, +0.5] | 9 / 18 | 0.122 |
| selfguided13 -> teacherguided23 | heldout_musique | -5.9 | [-12.8, +1.0] | 19 / 31 | 0.119 |
| selfguided13 -> teacherguided23 | heldout_strategyqa | -3.8 | [-10.8, +2.7] | 17 / 24 | 0.349 |
| selfguided13 -> teacherguided23 | pooled | -4.7 | [-7.8, -1.6] | 55 / 90 | 0.00458 |
| selfguided13 -> teacherrollouts13 | heldout_2wikimultihopqa | +6.5 | [+0.6, +12.3] | 18 / 7 | 0.0433 |
| selfguided13 -> teacherrollouts13 | heldout_hotpotqa | +0.5 | [-5.8, +6.9] | 20 / 19 | 1 |
| selfguided13 -> teacherrollouts13 | heldout_musique | +5.9 | [-1.0, +12.8] | 33 / 21 | 0.134 |
| selfguided13 -> teacherrollouts13 | heldout_strategyqa | -0.5 | [-6.5, +5.4] | 16 / 17 | 1 |
| selfguided13 -> teacherrollouts13 | pooled | +3.1 | [-0.1, +6.3] | 87 / 64 | 0.073 |
| selfguided13 -> teacherrollouts17 | heldout_2wikimultihopqa | +6.5 | [+0.6, +12.3] | 18 / 7 | 0.0433 |
| selfguided13 -> teacherrollouts17 | heldout_hotpotqa | -1.6 | [-7.9, +4.8] | 18 / 21 | 0.749 |
| selfguided13 -> teacherrollouts17 | heldout_musique | +5.4 | [-1.5, +12.3] | 31 / 20 | 0.161 |
| selfguided13 -> teacherrollouts17 | heldout_strategyqa | -1.1 | [-7.0, +4.9] | 15 / 17 | 0.86 |
| selfguided13 -> teacherrollouts17 | pooled | +2.3 | [-0.9, +5.5] | 82 / 65 | 0.187 |
| selfguided13 -> teacherrollouts23 | heldout_2wikimultihopqa | +6.5 | [+0.6, +12.3] | 19 / 8 | 0.0522 |
| selfguided13 -> teacherrollouts23 | heldout_hotpotqa | +0.5 | [-5.8, +6.9] | 20 / 19 | 1 |
| selfguided13 -> teacherrollouts23 | heldout_musique | +9.4 | [+2.5, +16.3] | 37 / 18 | 0.0145 |
| selfguided13 -> teacherrollouts23 | heldout_strategyqa | +4.9 | [-1.6, +11.3] | 23 / 14 | 0.188 |
| selfguided13 -> teacherrollouts23 | pooled | +5.3 | [+2.0, +8.6] | 99 / 59 | 0.00183 |
| selfguided13 -> unguided13 | heldout_2wikimultihopqa | -3.5 | [-10.0, +2.4] | 11 / 17 | 0.345 |
| selfguided13 -> unguided13 | heldout_hotpotqa | -3.2 | [-8.5, +2.1] | 10 / 16 | 0.327 |
| selfguided13 -> unguided13 | heldout_musique | -3.9 | [-10.3, +2.5] | 18 / 26 | 0.291 |
| selfguided13 -> unguided13 | heldout_strategyqa | -2.2 | [-6.5, +2.2] | 6 / 10 | 0.454 |
| selfguided13 -> unguided13 | pooled | -3.2 | [-6.0, -0.4] | 45 / 69 | 0.0308 |
| selfguided13 -> unguided17 | heldout_2wikimultihopqa | -4.1 | [-10.0, +1.8] | 10 / 17 | 0.248 |
| selfguided13 -> unguided17 | heldout_hotpotqa | -3.7 | [-9.5, +2.1] | 12 / 19 | 0.281 |
| selfguided13 -> unguided17 | heldout_musique | -4.9 | [-11.3, +1.5] | 16 / 26 | 0.164 |
| selfguided13 -> unguided17 | heldout_strategyqa | +1.1 | [-3.8, +5.9] | 12 / 10 | 0.832 |
| selfguided13 -> unguided17 | pooled | -2.9 | [-5.8, +0.0] | 50 / 72 | 0.0568 |
| selfguided13 -> unguided23 | heldout_2wikimultihopqa | -2.9 | [-8.8, +2.9] | 11 / 16 | 0.442 |
| selfguided13 -> unguided23 | heldout_hotpotqa | -3.7 | [-9.0, +1.6] | 10 / 17 | 0.248 |
| selfguided13 -> unguided23 | heldout_musique | -1.5 | [-8.4, +5.4] | 22 / 25 | 0.771 |
| selfguided13 -> unguided23 | heldout_strategyqa | +1.1 | [-3.8, +5.9] | 12 / 10 | 0.832 |
| selfguided13 -> unguided23 | pooled | -1.7 | [-4.7, +1.2] | 55 / 68 | 0.279 |
| selfguided17 -> selfguided23 | heldout_2wikimultihopqa | +1.8 | [-2.9, +7.1] | 11 / 8 | 0.648 |
| selfguided17 -> selfguided23 | heldout_hotpotqa | -3.2 | [-8.5, +2.1] | 10 / 16 | 0.327 |
| selfguided17 -> selfguided23 | heldout_musique | -1.5 | [-7.4, +4.4] | 17 / 20 | 0.743 |
| selfguided17 -> selfguided23 | heldout_strategyqa | -2.2 | [-5.9, +1.6] | 4 / 8 | 0.388 |
| selfguided17 -> selfguided23 | pooled | -1.3 | [-3.9, +1.2] | 42 / 52 | 0.353 |
| selfguided17 -> teacherguided13 | heldout_2wikimultihopqa | +2.4 | [-4.1, +8.8] | 17 / 13 | 0.585 |
| selfguided17 -> teacherguided13 | heldout_hotpotqa | -5.3 | [-11.1, +0.5] | 11 / 21 | 0.11 |
| selfguided17 -> teacherguided13 | heldout_musique | -2.5 | [-9.4, +4.4] | 24 / 29 | 0.583 |
| selfguided17 -> teacherguided13 | heldout_strategyqa | +0.5 | [-5.4, +6.5] | 17 / 16 | 1 |
| selfguided17 -> teacherguided13 | pooled | -1.3 | [-4.5, +1.7] | 69 / 79 | 0.46 |
| selfguided17 -> teacherguided17 | heldout_2wikimultihopqa | -1.2 | [-7.6, +5.3] | 14 / 16 | 0.856 |
| selfguided17 -> teacherguided17 | heldout_hotpotqa | -7.9 | [-14.3, -1.6] | 13 / 28 | 0.0275 |
| selfguided17 -> teacherguided17 | heldout_musique | -6.9 | [-13.8, +0.0] | 19 / 33 | 0.0704 |
| selfguided17 -> teacherguided17 | heldout_strategyqa | -4.3 | [-11.3, +2.2] | 16 / 24 | 0.268 |
| selfguided17 -> teacherguided17 | pooled | -5.2 | [-8.6, -1.9] | 62 / 101 | 0.0028 |
| selfguided17 -> teacherguided23 | heldout_2wikimultihopqa | -1.2 | [-7.6, +5.9] | 16 / 18 | 0.864 |
| selfguided17 -> teacherguided23 | heldout_hotpotqa | -6.3 | [-12.2, -0.5] | 11 / 23 | 0.0576 |
| selfguided17 -> teacherguided23 | heldout_musique | -4.4 | [-11.3, +3.0] | 23 / 32 | 0.281 |
| selfguided17 -> teacherguided23 | heldout_strategyqa | -2.2 | [-9.2, +4.3] | 18 / 22 | 0.636 |
| selfguided17 -> teacherguided23 | pooled | -3.6 | [-6.8, -0.3] | 68 / 95 | 0.0414 |
| selfguided17 -> teacherrollouts13 | heldout_2wikimultihopqa | +9.4 | [+2.9, +16.5] | 26 / 10 | 0.0113 |
| selfguided17 -> teacherrollouts13 | heldout_hotpotqa | -1.1 | [-7.9, +5.8] | 20 / 22 | 0.878 |
| selfguided17 -> teacherrollouts13 | heldout_musique | +7.4 | [+0.0, +14.8] | 36 / 21 | 0.0627 |
| selfguided17 -> teacherrollouts13 | heldout_strategyqa | +1.1 | [-5.4, +7.6] | 20 / 18 | 0.871 |
| selfguided17 -> teacherrollouts13 | pooled | +4.2 | [+0.7, +7.6] | 102 / 71 | 0.0223 |
| selfguided17 -> teacherrollouts17 | heldout_2wikimultihopqa | +9.4 | [+2.9, +16.5] | 26 / 10 | 0.0113 |
| selfguided17 -> teacherrollouts17 | heldout_hotpotqa | -3.2 | [-9.5, +3.2] | 16 / 22 | 0.418 |
| selfguided17 -> teacherrollouts17 | heldout_musique | +6.9 | [-0.5, +14.3] | 36 / 22 | 0.0869 |
| selfguided17 -> teacherrollouts17 | heldout_strategyqa | +0.5 | [-5.4, +6.5] | 17 / 16 | 1 |
| selfguided17 -> teacherrollouts17 | pooled | +3.4 | [-0.1, +6.7] | 95 / 70 | 0.0614 |
| selfguided17 -> teacherrollouts23 | heldout_2wikimultihopqa | +9.4 | [+2.4, +16.5] | 27 / 11 | 0.0139 |
| selfguided17 -> teacherrollouts23 | heldout_hotpotqa | -1.1 | [-7.4, +5.3] | 17 / 19 | 0.868 |
| selfguided17 -> teacherrollouts23 | heldout_musique | +10.8 | [+3.5, +18.2] | 42 / 20 | 0.00715 |
| selfguided17 -> teacherrollouts23 | heldout_strategyqa | +6.5 | [+0.0, +13.5] | 26 / 14 | 0.0807 |
| selfguided17 -> teacherrollouts23 | pooled | +6.4 | [+2.9, +9.9] | 112 / 64 | 0.000367 |
| selfguided17 -> unguided13 | heldout_2wikimultihopqa | -0.6 | [-6.5, +5.3] | 12 / 13 | 1 |
| selfguided17 -> unguided13 | heldout_hotpotqa | -4.8 | [-10.1, +0.5] | 9 / 18 | 0.122 |
| selfguided17 -> unguided13 | heldout_musique | -2.5 | [-8.9, +3.9] | 18 / 23 | 0.533 |
| selfguided17 -> unguided13 | heldout_strategyqa | -0.5 | [-4.3, +3.2] | 6 / 7 | 1 |
| selfguided17 -> unguided13 | pooled | -2.1 | [-4.8, +0.5] | 45 / 61 | 0.145 |
| selfguided17 -> unguided17 | heldout_2wikimultihopqa | -1.2 | [-6.5, +4.1] | 10 / 12 | 0.832 |
| selfguided17 -> unguided17 | heldout_hotpotqa | -5.3 | [-10.6, +0.0] | 9 / 19 | 0.0872 |
| selfguided17 -> unguided17 | heldout_musique | -3.5 | [-9.4, +2.5] | 15 / 22 | 0.324 |
| selfguided17 -> unguided17 | heldout_strategyqa | +2.7 | [-1.6, +7.6] | 12 / 7 | 0.359 |
| selfguided17 -> unguided17 | pooled | -1.9 | [-4.5, +0.8] | 46 / 60 | 0.206 |
| selfguided17 -> unguided23 | heldout_2wikimultihopqa | +0.0 | [-5.9, +5.9] | 12 / 12 | 1 |
| selfguided17 -> unguided23 | heldout_hotpotqa | -5.3 | [-10.6, -0.5] | 7 / 17 | 0.0639 |
| selfguided17 -> unguided23 | heldout_musique | +0.0 | [-6.4, +6.4] | 23 / 23 | 1 |
| selfguided17 -> unguided23 | heldout_strategyqa | +2.7 | [-1.6, +7.0] | 11 / 6 | 0.332 |
| selfguided17 -> unguided23 | pooled | -0.7 | [-3.5, +2.0] | 53 / 58 | 0.704 |
| selfguided23 -> teacherguided13 | heldout_2wikimultihopqa | +0.6 | [-5.9, +7.1] | 16 / 15 | 1 |
| selfguided23 -> teacherguided13 | heldout_hotpotqa | -2.1 | [-7.4, +3.2] | 10 / 14 | 0.541 |
| selfguided23 -> teacherguided13 | heldout_musique | -1.0 | [-7.9, +5.9] | 24 / 26 | 0.888 |
| selfguided23 -> teacherguided13 | heldout_strategyqa | +2.7 | [-3.2, +8.6] | 19 / 14 | 0.487 |
| selfguided23 -> teacherguided13 | pooled | +0.0 | [-3.1, +3.1] | 69 / 69 | 1 |
| selfguided23 -> teacherguided17 | heldout_2wikimultihopqa | -2.9 | [-10.0, +3.5] | 15 / 20 | 0.5 |
| selfguided23 -> teacherguided17 | heldout_hotpotqa | -4.8 | [-10.6, +1.1] | 12 / 21 | 0.163 |
| selfguided23 -> teacherguided17 | heldout_musique | -5.4 | [-12.3, +1.5] | 21 / 32 | 0.169 |
| selfguided23 -> teacherguided17 | heldout_strategyqa | -2.2 | [-8.1, +3.8] | 14 / 18 | 0.597 |
| selfguided23 -> teacherguided17 | pooled | -3.9 | [-7.1, -0.7] | 62 / 91 | 0.0233 |
| selfguided23 -> teacherguided23 | heldout_2wikimultihopqa | -2.9 | [-9.4, +4.1] | 15 / 20 | 0.5 |
| selfguided23 -> teacherguided23 | heldout_hotpotqa | -3.2 | [-9.0, +2.6] | 12 / 18 | 0.362 |
| selfguided23 -> teacherguided23 | heldout_musique | -3.0 | [-9.8, +3.9] | 23 / 29 | 0.488 |
| selfguided23 -> teacherguided23 | heldout_strategyqa | +0.0 | [-6.5, +6.5] | 19 / 19 | 1 |
| selfguided23 -> teacherguided23 | pooled | -2.3 | [-5.5, +0.9] | 69 / 86 | 0.199 |
| selfguided23 -> teacherrollouts13 | heldout_2wikimultihopqa | +7.6 | [+1.2, +14.1] | 23 / 10 | 0.0351 |
| selfguided23 -> teacherrollouts13 | heldout_hotpotqa | +2.1 | [-3.7, +7.9] | 18 / 14 | 0.597 |
| selfguided23 -> teacherrollouts13 | heldout_musique | +8.9 | [+2.0, +15.8] | 37 / 19 | 0.0222 |
| selfguided23 -> teacherrollouts13 | heldout_strategyqa | +3.2 | [-2.7, +9.7] | 20 / 14 | 0.392 |
| selfguided23 -> teacherrollouts13 | pooled | +5.5 | [+2.3, +8.8] | 98 / 57 | 0.00124 |
| selfguided23 -> teacherrollouts17 | heldout_2wikimultihopqa | +7.6 | [+1.2, +14.1] | 22 / 9 | 0.0294 |
| selfguided23 -> teacherrollouts17 | heldout_hotpotqa | +0.0 | [-5.8, +5.8] | 17 / 17 | 1 |
| selfguided23 -> teacherrollouts17 | heldout_musique | +8.4 | [+1.5, +15.3] | 35 / 18 | 0.027 |
| selfguided23 -> teacherrollouts17 | heldout_strategyqa | +2.7 | [-3.2, +9.2] | 19 / 14 | 0.487 |
| selfguided23 -> teacherrollouts17 | pooled | +4.7 | [+1.5, +7.9] | 93 / 58 | 0.00548 |
| selfguided23 -> teacherrollouts23 | heldout_2wikimultihopqa | +7.6 | [+1.2, +14.1] | 23 / 10 | 0.0351 |
| selfguided23 -> teacherrollouts23 | heldout_hotpotqa | +2.1 | [-3.7, +7.9] | 18 / 14 | 0.597 |
| selfguided23 -> teacherrollouts23 | heldout_musique | +12.3 | [+4.9, +19.7] | 44 / 19 | 0.00223 |
| selfguided23 -> teacherrollouts23 | heldout_strategyqa | +8.6 | [+2.2, +15.1] | 26 / 10 | 0.0113 |
| selfguided23 -> teacherrollouts23 | pooled | +7.8 | [+4.4, +11.1] | 111 / 53 | 7e-06 |
| selfguided23 -> unguided13 | heldout_2wikimultihopqa | -2.4 | [-8.2, +3.5] | 10 / 14 | 0.541 |
| selfguided23 -> unguided13 | heldout_hotpotqa | -1.6 | [-6.3, +3.2] | 9 / 12 | 0.664 |
| selfguided23 -> unguided13 | heldout_musique | -1.0 | [-7.4, +4.9] | 19 / 21 | 0.875 |
| selfguided23 -> unguided13 | heldout_strategyqa | +1.6 | [-2.2, +5.4] | 8 / 5 | 0.581 |
| selfguided23 -> unguided13 | pooled | -0.8 | [-3.4, +1.7] | 46 / 52 | 0.614 |
| selfguided23 -> unguided17 | heldout_2wikimultihopqa | -2.9 | [-8.8, +2.9] | 11 / 16 | 0.442 |
| selfguided23 -> unguided17 | heldout_hotpotqa | -2.1 | [-6.9, +2.6] | 8 / 12 | 0.503 |
| selfguided23 -> unguided17 | heldout_musique | -2.0 | [-7.9, +3.9] | 17 / 21 | 0.627 |
| selfguided23 -> unguided17 | heldout_strategyqa | +4.9 | [+1.1, +9.2] | 12 / 3 | 0.0352 |
| selfguided23 -> unguided17 | pooled | -0.5 | [-3.1, +2.1] | 48 / 52 | 0.764 |
| selfguided23 -> unguided23 | heldout_2wikimultihopqa | -1.8 | [-8.2, +4.1] | 12 / 15 | 0.701 |
| selfguided23 -> unguided23 | heldout_hotpotqa | -2.1 | [-6.3, +2.1] | 7 / 11 | 0.481 |
| selfguided23 -> unguided23 | heldout_musique | +1.5 | [-4.9, +7.9] | 24 / 21 | 0.766 |
| selfguided23 -> unguided23 | heldout_strategyqa | +4.9 | [+0.0, +9.7] | 15 / 6 | 0.0784 |
| selfguided23 -> unguided23 | pooled | +0.7 | [-2.1, +3.4] | 58 / 53 | 0.704 |
| teacherguided13 -> teacherguided17 | heldout_2wikimultihopqa | -3.5 | [-8.8, +1.8] | 8 / 14 | 0.286 |
| teacherguided13 -> teacherguided17 | heldout_hotpotqa | -2.6 | [-8.5, +3.2] | 12 / 17 | 0.458 |
| teacherguided13 -> teacherguided17 | heldout_musique | -4.4 | [-11.3, +2.5] | 20 / 29 | 0.253 |
| teacherguided13 -> teacherguided17 | heldout_strategyqa | -4.9 | [-10.3, +0.0] | 7 / 16 | 0.0931 |
| teacherguided13 -> teacherguided17 | pooled | -3.9 | [-6.7, -0.9] | 47 / 76 | 0.0113 |
| teacherguided13 -> teacherguided23 | heldout_2wikimultihopqa | -3.5 | [-8.8, +1.8] | 8 / 14 | 0.286 |
| teacherguided13 -> teacherguided23 | heldout_hotpotqa | -1.1 | [-6.9, +4.8] | 14 / 16 | 0.856 |
| teacherguided13 -> teacherguided23 | heldout_musique | -2.0 | [-8.4, +3.9] | 19 / 23 | 0.644 |
| teacherguided13 -> teacherguided23 | heldout_strategyqa | -2.7 | [-8.6, +3.2] | 13 / 18 | 0.473 |
| teacherguided13 -> teacherguided23 | pooled | -2.3 | [-5.2, +0.7] | 54 / 71 | 0.152 |
| teacherguided13 -> teacherrollouts13 | heldout_2wikimultihopqa | +7.1 | [+1.8, +12.3] | 17 / 5 | 0.0169 |
| teacherguided13 -> teacherrollouts13 | heldout_hotpotqa | +4.2 | [-1.6, +10.1] | 20 / 12 | 0.215 |
| teacherguided13 -> teacherrollouts13 | heldout_musique | +9.8 | [+2.5, +17.2] | 40 / 20 | 0.0135 |
| teacherguided13 -> teacherrollouts13 | heldout_strategyqa | +0.5 | [-5.9, +7.0] | 19 / 18 | 1 |
| teacherguided13 -> teacherrollouts13 | pooled | +5.5 | [+2.3, +8.8] | 96 / 55 | 0.00106 |
| teacherguided13 -> teacherrollouts17 | heldout_2wikimultihopqa | +7.1 | [+1.2, +12.9] | 19 / 7 | 0.029 |
| teacherguided13 -> teacherrollouts17 | heldout_hotpotqa | +2.1 | [-3.7, +7.9] | 18 / 14 | 0.597 |
| teacherguided13 -> teacherrollouts17 | heldout_musique | +9.4 | [+3.0, +15.8] | 34 / 15 | 0.0094 |
| teacherguided13 -> teacherrollouts17 | heldout_strategyqa | +0.0 | [-5.9, +5.9] | 16 / 16 | 1 |
| teacherguided13 -> teacherrollouts17 | pooled | +4.7 | [+1.6, +7.9] | 87 / 52 | 0.00377 |
| teacherguided13 -> teacherrollouts23 | heldout_2wikimultihopqa | +7.1 | [+1.2, +12.9] | 20 / 8 | 0.0357 |
| teacherguided13 -> teacherrollouts23 | heldout_hotpotqa | +4.2 | [-1.6, +10.1] | 21 / 13 | 0.229 |
| teacherguided13 -> teacherrollouts23 | heldout_musique | +13.3 | [+6.4, +20.2] | 43 / 16 | 0.000584 |
| teacherguided13 -> teacherrollouts23 | heldout_strategyqa | +5.9 | [+0.0, +11.9] | 23 / 12 | 0.0895 |
| teacherguided13 -> teacherrollouts23 | pooled | +7.8 | [+4.5, +11.1] | 107 / 49 | 4e-06 |
| teacherguided13 -> unguided13 | heldout_2wikimultihopqa | -2.9 | [-8.8, +2.9] | 11 / 16 | 0.442 |
| teacherguided13 -> unguided13 | heldout_hotpotqa | +0.5 | [-4.8, +6.3] | 15 / 14 | 1 |
| teacherguided13 -> unguided13 | heldout_musique | +0.0 | [-6.9, +6.9] | 25 / 25 | 1 |
| teacherguided13 -> unguided13 | heldout_strategyqa | -1.1 | [-7.0, +4.9] | 16 / 18 | 0.864 |
| teacherguided13 -> unguided13 | pooled | -0.8 | [-3.9, +2.4] | 67 / 73 | 0.673 |
| teacherguided13 -> unguided17 | heldout_2wikimultihopqa | -3.5 | [-9.4, +1.8] | 9 / 15 | 0.307 |
| teacherguided13 -> unguided17 | heldout_hotpotqa | +0.0 | [-5.3, +5.3] | 13 / 13 | 1 |
| teacherguided13 -> unguided17 | heldout_musique | -1.0 | [-7.4, +5.4] | 21 / 23 | 0.88 |
| teacherguided13 -> unguided17 | heldout_strategyqa | +2.2 | [-3.2, +7.6] | 16 / 12 | 0.572 |
| teacherguided13 -> unguided17 | pooled | -0.5 | [-3.5, +2.4] | 59 / 63 | 0.786 |
| teacherguided13 -> unguided23 | heldout_2wikimultihopqa | -2.4 | [-7.6, +2.9] | 8 / 12 | 0.503 |
| teacherguided13 -> unguided23 | heldout_hotpotqa | +0.0 | [-5.3, +5.3] | 13 / 13 | 1 |
| teacherguided13 -> unguided23 | heldout_musique | +2.5 | [-4.9, +9.8] | 32 / 27 | 0.603 |
| teacherguided13 -> unguided23 | heldout_strategyqa | +2.2 | [-3.8, +8.1] | 18 / 14 | 0.597 |
| teacherguided13 -> unguided23 | pooled | +0.7 | [-2.4, +3.8] | 71 / 66 | 0.733 |
| teacherguided17 -> teacherguided23 | heldout_2wikimultihopqa | +0.0 | [-5.3, +5.3] | 11 / 11 | 1 |
| teacherguided17 -> teacherguided23 | heldout_hotpotqa | +1.6 | [-4.8, +7.4] | 18 / 15 | 0.728 |
| teacherguided17 -> teacherguided23 | heldout_musique | +2.5 | [-4.4, +9.4] | 27 / 22 | 0.568 |
| teacherguided17 -> teacherguided23 | heldout_strategyqa | +2.2 | [-2.2, +6.5] | 11 / 7 | 0.481 |
| teacherguided17 -> teacherguided23 | pooled | +1.6 | [-1.3, +4.5] | 67 / 55 | 0.319 |
| teacherguided17 -> teacherrollouts13 | heldout_2wikimultihopqa | +10.6 | [+4.1, +17.1] | 25 / 7 | 0.0021 |
| teacherguided17 -> teacherrollouts13 | heldout_hotpotqa | +6.9 | [+0.5, +13.8] | 27 / 14 | 0.0596 |
| teacherguided17 -> teacherrollouts13 | heldout_musique | +14.3 | [+6.4, +21.7] | 47 / 18 | 0.000422 |
| teacherguided17 -> teacherrollouts13 | heldout_strategyqa | +5.4 | [-1.1, +11.9] | 24 / 14 | 0.143 |
| teacherguided17 -> teacherrollouts13 | pooled | +9.4 | [+6.0, +12.8] | 123 / 53 | 0 |
| teacherguided17 -> teacherrollouts17 | heldout_2wikimultihopqa | +10.6 | [+4.1, +17.1] | 26 / 8 | 0.00294 |
| teacherguided17 -> teacherrollouts17 | heldout_hotpotqa | +4.8 | [-1.6, +11.1] | 24 / 15 | 0.2 |
| teacherguided17 -> teacherrollouts17 | heldout_musique | +13.8 | [+6.4, +21.2] | 45 / 17 | 0.000497 |
| teacherguided17 -> teacherrollouts17 | heldout_strategyqa | +4.9 | [-1.6, +11.3] | 23 / 14 | 0.188 |
| teacherguided17 -> teacherrollouts17 | pooled | +8.6 | [+5.2, +11.9] | 118 / 54 | 1e-06 |
| teacherguided17 -> teacherrollouts23 | heldout_2wikimultihopqa | +10.6 | [+4.1, +17.1] | 27 / 9 | 0.00393 |
| teacherguided17 -> teacherrollouts23 | heldout_hotpotqa | +6.9 | [+0.0, +13.2] | 27 / 14 | 0.0596 |
| teacherguided17 -> teacherrollouts23 | heldout_musique | +17.7 | [+9.8, +25.6] | 54 / 18 | 2.6e-05 |
| teacherguided17 -> teacherrollouts23 | heldout_strategyqa | +10.8 | [+3.8, +17.8] | 32 / 12 | 0.00366 |
| teacherguided17 -> teacherrollouts23 | pooled | +11.7 | [+8.0, +15.1] | 140 / 53 | 0 |
| teacherguided17 -> unguided13 | heldout_2wikimultihopqa | +0.6 | [-5.3, +7.1] | 15 / 14 | 1 |
| teacherguided17 -> unguided13 | heldout_hotpotqa | +3.2 | [-3.2, +10.1] | 23 / 17 | 0.43 |
| teacherguided17 -> unguided13 | heldout_musique | +4.4 | [-3.0, +11.8] | 33 / 24 | 0.289 |
| teacherguided17 -> unguided13 | heldout_strategyqa | +3.8 | [-2.2, +9.7] | 20 / 13 | 0.296 |
| teacherguided17 -> unguided13 | pooled | +3.1 | [-0.1, +6.4] | 91 / 68 | 0.0807 |
| teacherguided17 -> unguided17 | heldout_2wikimultihopqa | +0.0 | [-6.5, +6.5] | 14 / 14 | 1 |
| teacherguided17 -> unguided17 | heldout_hotpotqa | +2.6 | [-3.7, +9.0] | 21 / 16 | 0.511 |
| teacherguided17 -> unguided17 | heldout_musique | +3.5 | [-3.0, +9.8] | 26 / 19 | 0.371 |
| teacherguided17 -> unguided17 | heldout_strategyqa | +7.0 | [+1.1, +13.0] | 22 / 9 | 0.0294 |
| teacherguided17 -> unguided17 | pooled | +3.4 | [+0.3, +6.4] | 83 / 58 | 0.0429 |
| teacherguided17 -> unguided23 | heldout_2wikimultihopqa | +1.2 | [-4.7, +7.6] | 15 / 13 | 0.851 |
| teacherguided17 -> unguided23 | heldout_hotpotqa | +2.6 | [-3.7, +9.0] | 22 / 17 | 0.522 |
| teacherguided17 -> unguided23 | heldout_musique | +6.9 | [+0.0, +14.3] | 34 / 20 | 0.0759 |
| teacherguided17 -> unguided23 | heldout_strategyqa | +7.0 | [+1.1, +13.5] | 24 / 11 | 0.041 |
| teacherguided17 -> unguided23 | pooled | +4.5 | [+1.3, +7.8] | 95 / 61 | 0.00803 |
| teacherguided23 -> teacherrollouts13 | heldout_2wikimultihopqa | +10.6 | [+4.7, +16.5] | 23 / 5 | 0.000912 |
| teacherguided23 -> teacherrollouts13 | heldout_hotpotqa | +5.3 | [-1.6, +12.2] | 26 / 16 | 0.164 |
| teacherguided23 -> teacherrollouts13 | heldout_musique | +11.8 | [+4.9, +19.2] | 41 / 17 | 0.00223 |
| teacherguided23 -> teacherrollouts13 | heldout_strategyqa | +3.2 | [-3.2, +9.7] | 23 / 17 | 0.43 |
| teacherguided23 -> teacherrollouts13 | pooled | +7.8 | [+4.4, +11.1] | 113 / 55 | 9e-06 |
| teacherguided23 -> teacherrollouts17 | heldout_2wikimultihopqa | +10.6 | [+4.7, +17.1] | 25 / 7 | 0.0021 |
| teacherguided23 -> teacherrollouts17 | heldout_hotpotqa | +3.2 | [-3.2, +10.1] | 23 / 17 | 0.43 |
| teacherguided23 -> teacherrollouts17 | heldout_musique | +11.3 | [+4.4, +18.2] | 39 / 16 | 0.00267 |
| teacherguided23 -> teacherrollouts17 | heldout_strategyqa | +2.7 | [-3.8, +9.2] | 22 / 17 | 0.522 |
| teacherguided23 -> teacherrollouts17 | pooled | +7.0 | [+3.8, +10.2] | 109 / 57 | 6.6e-05 |
| teacherguided23 -> teacherrollouts23 | heldout_2wikimultihopqa | +10.6 | [+4.1, +17.1] | 25 / 7 | 0.0021 |
| teacherguided23 -> teacherrollouts23 | heldout_hotpotqa | +5.3 | [-1.1, +12.2] | 25 / 15 | 0.154 |
| teacherguided23 -> teacherrollouts23 | heldout_musique | +15.3 | [+7.9, +22.7] | 47 / 16 | 0.000117 |
| teacherguided23 -> teacherrollouts23 | heldout_strategyqa | +8.6 | [+1.6, +15.7] | 30 / 14 | 0.0226 |
| teacherguided23 -> teacherrollouts23 | pooled | +10.0 | [+6.7, +13.4] | 127 / 52 | 0 |
| teacherguided23 -> unguided13 | heldout_2wikimultihopqa | +0.6 | [-5.9, +7.1] | 17 / 16 | 1 |
| teacherguided23 -> unguided13 | heldout_hotpotqa | +1.6 | [-3.7, +6.9] | 15 / 12 | 0.701 |
| teacherguided23 -> unguided13 | heldout_musique | +2.0 | [-5.4, +9.4] | 31 / 27 | 0.694 |
| teacherguided23 -> unguided13 | heldout_strategyqa | +1.6 | [-4.3, +8.1] | 19 / 16 | 0.736 |
| teacherguided23 -> unguided13 | pooled | +1.5 | [-1.7, +4.7] | 82 / 71 | 0.419 |
| teacherguided23 -> unguided17 | heldout_2wikimultihopqa | +0.0 | [-6.5, +6.5] | 15 / 15 | 1 |
| teacherguided23 -> unguided17 | heldout_hotpotqa | +1.1 | [-3.7, +6.3] | 13 / 11 | 0.839 |
| teacherguided23 -> unguided17 | heldout_musique | +1.0 | [-5.9, +7.9] | 28 / 26 | 0.892 |
| teacherguided23 -> unguided17 | heldout_strategyqa | +4.9 | [-1.1, +11.3] | 22 / 13 | 0.175 |
| teacherguided23 -> unguided17 | pooled | +1.7 | [-1.3, +4.8] | 78 / 65 | 0.316 |
| teacherguided23 -> unguided23 | heldout_2wikimultihopqa | +1.2 | [-5.3, +7.1] | 15 / 13 | 0.851 |
| teacherguided23 -> unguided23 | heldout_hotpotqa | +1.1 | [-3.7, +5.8] | 12 / 10 | 0.832 |
| teacherguided23 -> unguided23 | heldout_musique | +4.4 | [-3.5, +12.3] | 38 / 29 | 0.328 |
| teacherguided23 -> unguided23 | heldout_strategyqa | +4.9 | [-1.1, +11.3] | 22 / 13 | 0.175 |
| teacherguided23 -> unguided23 | pooled | +2.9 | [-0.3, +6.0] | 87 / 65 | 0.0882 |
| teacherrollouts13 -> teacherrollouts17 | heldout_2wikimultihopqa | +0.0 | [-3.5, +3.5] | 5 / 5 | 1 |
| teacherrollouts13 -> teacherrollouts17 | heldout_hotpotqa | -2.1 | [-6.9, +2.6] | 8 / 12 | 0.503 |
| teacherrollouts13 -> teacherrollouts17 | heldout_musique | -0.5 | [-6.4, +4.9] | 17 / 18 | 1 |
| teacherrollouts13 -> teacherrollouts17 | heldout_strategyqa | -0.5 | [-5.9, +4.9] | 12 / 13 | 1 |
| teacherrollouts13 -> teacherrollouts17 | pooled | -0.8 | [-3.2, +1.6] | 42 / 48 | 0.598 |
| teacherrollouts13 -> teacherrollouts23 | heldout_2wikimultihopqa | +0.0 | [-4.1, +4.1] | 6 / 6 | 1 |
| teacherrollouts13 -> teacherrollouts23 | heldout_hotpotqa | +0.0 | [-4.2, +4.2] | 8 / 8 | 1 |
| teacherrollouts13 -> teacherrollouts23 | heldout_musique | +3.5 | [-2.5, +9.4] | 23 / 16 | 0.337 |
| teacherrollouts13 -> teacherrollouts23 | heldout_strategyqa | +5.4 | [+0.0, +10.8] | 19 / 9 | 0.0872 |
| teacherrollouts13 -> teacherrollouts23 | pooled | +2.3 | [-0.3, +4.8] | 56 / 39 | 0.1 |
| teacherrollouts13 -> unguided13 | heldout_2wikimultihopqa | -10.0 | [-16.5, -3.5] | 7 / 24 | 0.00333 |
| teacherrollouts13 -> unguided13 | heldout_hotpotqa | -3.7 | [-10.1, +2.6] | 17 / 24 | 0.349 |
| teacherrollouts13 -> unguided13 | heldout_musique | -9.8 | [-17.2, -2.5] | 22 / 42 | 0.0169 |
| teacherrollouts13 -> unguided13 | heldout_strategyqa | -1.6 | [-8.1, +4.3] | 16 / 19 | 0.736 |
| teacherrollouts13 -> unguided13 | pooled | -6.3 | [-9.6, -2.9] | 62 / 109 | 0.000404 |
| teacherrollouts13 -> unguided17 | heldout_2wikimultihopqa | -10.6 | [-17.1, -4.1] | 7 / 25 | 0.0021 |
| teacherrollouts13 -> unguided17 | heldout_hotpotqa | -4.2 | [-10.1, +1.6] | 12 / 20 | 0.215 |
| teacherrollouts13 -> unguided17 | heldout_musique | -10.8 | [-18.2, -3.5] | 21 / 43 | 0.00815 |
| teacherrollouts13 -> unguided17 | heldout_strategyqa | +1.6 | [-4.3, +7.6] | 18 / 15 | 0.728 |
| teacherrollouts13 -> unguided17 | pooled | -6.0 | [-9.4, -2.7] | 58 / 103 | 0.000487 |
| teacherrollouts13 -> unguided23 | heldout_2wikimultihopqa | -9.4 | [-15.9, -3.5] | 6 / 22 | 0.00372 |
| teacherrollouts13 -> unguided23 | heldout_hotpotqa | -4.2 | [-10.6, +2.1] | 14 / 22 | 0.243 |
| teacherrollouts13 -> unguided23 | heldout_musique | -7.4 | [-14.8, +0.5] | 24 / 39 | 0.0769 |
| teacherrollouts13 -> unguided23 | heldout_strategyqa | +1.6 | [-4.9, +8.1] | 19 / 16 | 0.736 |
| teacherrollouts13 -> unguided23 | pooled | -4.8 | [-8.2, -1.5] | 63 / 99 | 0.00579 |
| teacherrollouts17 -> teacherrollouts23 | heldout_2wikimultihopqa | +0.0 | [-3.5, +3.5] | 5 / 5 | 1 |
| teacherrollouts17 -> teacherrollouts23 | heldout_hotpotqa | +2.1 | [-2.6, +6.9] | 12 / 8 | 0.503 |
| teacherrollouts17 -> teacherrollouts23 | heldout_musique | +3.9 | [-2.0, +9.8] | 24 / 16 | 0.268 |
| teacherrollouts17 -> teacherrollouts23 | heldout_strategyqa | +5.9 | [+0.5, +11.9] | 20 / 9 | 0.0614 |
| teacherrollouts17 -> teacherrollouts23 | pooled | +3.1 | [+0.5, +5.6] | 61 / 38 | 0.0265 |
| teacherrollouts17 -> unguided13 | heldout_2wikimultihopqa | -10.0 | [-16.5, -3.5] | 7 / 24 | 0.00333 |
| teacherrollouts17 -> unguided13 | heldout_hotpotqa | -1.6 | [-7.9, +5.3] | 19 / 22 | 0.755 |
| teacherrollouts17 -> unguided13 | heldout_musique | -9.4 | [-16.8, -2.0] | 20 / 39 | 0.0183 |
| teacherrollouts17 -> unguided13 | heldout_strategyqa | -1.1 | [-7.6, +4.9] | 16 / 18 | 0.864 |
| teacherrollouts17 -> unguided13 | pooled | -5.5 | [-8.8, -2.1] | 62 / 103 | 0.00176 |
| teacherrollouts17 -> unguided17 | heldout_2wikimultihopqa | -10.6 | [-17.1, -4.1] | 7 / 25 | 0.0021 |
| teacherrollouts17 -> unguided17 | heldout_hotpotqa | -2.1 | [-7.9, +3.7] | 14 / 18 | 0.597 |
| teacherrollouts17 -> unguided17 | heldout_musique | -10.3 | [-17.7, -3.0] | 18 / 39 | 0.00751 |
| teacherrollouts17 -> unguided17 | heldout_strategyqa | +2.2 | [-4.3, +8.6] | 21 / 17 | 0.627 |
| teacherrollouts17 -> unguided17 | pooled | -5.2 | [-8.4, -1.9] | 60 / 99 | 0.00247 |
| teacherrollouts17 -> unguided23 | heldout_2wikimultihopqa | -9.4 | [-15.9, -3.5] | 7 / 23 | 0.00522 |
| teacherrollouts17 -> unguided23 | heldout_hotpotqa | -2.1 | [-8.5, +4.2] | 17 / 21 | 0.627 |
| teacherrollouts17 -> unguided23 | heldout_musique | -6.9 | [-14.3, +0.5] | 23 / 37 | 0.0925 |
| teacherrollouts17 -> unguided23 | heldout_strategyqa | +2.2 | [-3.8, +8.1] | 17 / 13 | 0.585 |
| teacherrollouts17 -> unguided23 | pooled | -4.0 | [-7.4, -0.8] | 64 / 94 | 0.0208 |
| teacherrollouts23 -> unguided13 | heldout_2wikimultihopqa | -10.0 | [-16.5, -3.5] | 8 / 25 | 0.00455 |
| teacherrollouts23 -> unguided13 | heldout_hotpotqa | -3.7 | [-10.1, +2.6] | 15 / 22 | 0.324 |
| teacherrollouts23 -> unguided13 | heldout_musique | -13.3 | [-20.7, -5.9] | 17 / 44 | 0.00073 |
| teacherrollouts23 -> unguided13 | heldout_strategyqa | -7.0 | [-14.1, +0.0] | 15 / 28 | 0.066 |
| teacherrollouts23 -> unguided13 | pooled | -8.6 | [-11.9, -5.1] | 55 / 119 | 1e-06 |
| teacherrollouts23 -> unguided17 | heldout_2wikimultihopqa | -10.6 | [-17.1, -4.1] | 7 / 25 | 0.0021 |
| teacherrollouts23 -> unguided17 | heldout_hotpotqa | -4.2 | [-10.1, +1.6] | 12 / 20 | 0.215 |
| teacherrollouts23 -> unguided17 | heldout_musique | -14.3 | [-21.2, -7.4] | 14 / 43 | 0.000154 |
| teacherrollouts23 -> unguided17 | heldout_strategyqa | -3.8 | [-10.8, +3.2] | 18 / 25 | 0.36 |
| teacherrollouts23 -> unguided17 | pooled | -8.3 | [-11.7, -5.0] | 51 / 113 | 1e-06 |
| teacherrollouts23 -> unguided23 | heldout_2wikimultihopqa | -9.4 | [-15.9, -2.9] | 8 / 24 | 0.007 |
| teacherrollouts23 -> unguided23 | heldout_hotpotqa | -4.2 | [-10.6, +2.1] | 13 / 21 | 0.229 |
| teacherrollouts23 -> unguided23 | heldout_musique | -10.8 | [-18.2, -3.5] | 20 / 42 | 0.00715 |
| teacherrollouts23 -> unguided23 | heldout_strategyqa | -3.8 | [-10.3, +2.7] | 17 / 24 | 0.349 |
| teacherrollouts23 -> unguided23 | pooled | -7.1 | [-10.4, -3.8] | 58 / 111 | 5.6e-05 |
| unguided13 -> unguided17 | heldout_2wikimultihopqa | -0.6 | [-5.3, +4.1] | 8 / 9 | 1 |
| unguided13 -> unguided17 | heldout_hotpotqa | -0.5 | [-4.8, +3.7] | 7 / 8 | 1 |
| unguided13 -> unguided17 | heldout_musique | -1.0 | [-6.4, +4.4] | 15 / 17 | 0.86 |
| unguided13 -> unguided17 | heldout_strategyqa | +3.2 | [+0.0, +6.5] | 8 / 2 | 0.109 |
| unguided13 -> unguided17 | pooled | +0.3 | [-2.0, +2.5] | 38 / 36 | 0.908 |
| unguided13 -> unguided23 | heldout_2wikimultihopqa | +0.6 | [-4.1, +5.9] | 10 / 9 | 1 |
| unguided13 -> unguided23 | heldout_hotpotqa | -0.5 | [-4.8, +3.2] | 7 / 8 | 1 |
| unguided13 -> unguided23 | heldout_musique | +2.5 | [-3.9, +8.9] | 24 / 19 | 0.542 |
| unguided13 -> unguided23 | heldout_strategyqa | +3.2 | [-0.5, +7.6] | 10 / 4 | 0.18 |
| unguided13 -> unguided23 | pooled | +1.5 | [-1.1, +4.0] | 51 / 40 | 0.294 |
| unguided17 -> unguided23 | heldout_2wikimultihopqa | +1.2 | [-2.9, +5.3] | 7 / 5 | 0.774 |
| unguided17 -> unguided23 | heldout_hotpotqa | +0.0 | [-3.7, +3.7] | 6 / 6 | 1 |
| unguided17 -> unguided23 | heldout_musique | +3.5 | [-1.5, +8.4] | 16 / 9 | 0.23 |
| unguided17 -> unguided23 | heldout_strategyqa | +0.0 | [-4.3, +4.3] | 9 / 9 | 1 |
| unguided17 -> unguided23 | pooled | +1.2 | [-0.9, +3.4] | 38 / 29 | 0.328 |
