# Teacher comparison

7,999 questions shared by every arm. Baseline: **self**; differences are arm − baseline in percentage points.

| arm | student | teacher | self-teaching | config | episodes | judged |
|---|---|---|---|---|---|---|
| self | ibm-granite/granite-4.1-3b | ibm-granite/granite-4.1-3b | yes | dfc43e9c5a8d8f4a | 7,999 | 7,999 |
| deepseek | ibm-granite/granite-4.1-3b | deepseek-ai/deepseek-v4-flash, deepseek-ai/deepseek-v4-flash-0731 | no | 1716bb7efcbd32d0 | 7,999 | 7,999 |
| glm | ibm-granite/granite-4.2-3b | z-ai/glm-5.3-flash | no | dfc43e9c5a8d8f4a | 7,999 | 7,999 |

**Warnings**

* the arms have different students, so differences mix the teacher's effect with the student's
* the arms were collected with different configs (config_hash), so settings other than the teacher differ too

## Outcome

| arm | n | judge | cover | EM | F1 | doc recall | grounded | steps | SFT examples | SFT / episode | teacher tok / ep | student tok / ep | API $ / ep |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| self | 7,999 | 61.5 % | 53.0 % | 9.2 % | 0.195 | 0.761 | 76.0 % | 2.99 | 15,915 | 1.99 | 5,449 | 9,074 | 0.00000 |
| deepseek | 7,999 | 62.3 % | 54.8 % | 26.4 % | 0.364 | 0.790 | 75.8 % | 2.92 | 16,567 | 2.07 | 5,503 | 11,402 | 0.00000 |
| glm | 7,999 | 65.6 % | 58.2 % | 10.4 % | 0.209 | 0.843 | 74.1 % | 2.74 | 15,490 | 1.94 | 5,338 | 6,354 | 0.00000 |

### Judge-correct by dataset

| dataset | self | deepseek | glm |
|---|---|---|---|
| 2wikimultihopqa | 72.8 % | 71.7 % | 78.9 % |
| hotpotqa | 70.5 % | 70.8 % | 72.8 % |
| musique | 37.5 % | 36.2 % | 44.5 % |
| strategyqa | 65.0 % | 70.3 % | 66.1 % |

## Paired differences against the baseline

| arm | scope | metric | n | Δ pts | 95 % CI | arm wins / baseline wins | McNemar p |
|---|---|---|---|---|---|---|---|
| deepseek | ALL | judge | 7,999 | +0.8 | [-0.2, +1.8] | 921 / 857 | 0.135 |
| deepseek | ALL | cover | 7,999 | +1.8 | [+0.8, +2.9] | 1019 / 873 | 0.000853 |
| deepseek | 2wikimultihopqa | judge | 2,000 | -1.1 | [-3.2, +1.0] | 210 / 232 | 0.318 |
| deepseek | 2wikimultihopqa | cover | 2,000 | -1.4 | [-3.4, +0.7] | 204 / 231 | 0.212 |
| deepseek | hotpotqa | judge | 2,000 | +0.2 | [-1.6, +2.1] | 183 / 178 | 0.833 |
| deepseek | hotpotqa | cover | 2,000 | -1.7 | [-3.6, +0.2] | 178 / 212 | 0.0946 |
| deepseek | musique | judge | 2,000 | -1.2 | [-3.5, +1.1] | 257 / 282 | 0.301 |
| deepseek | musique | cover | 2,000 | -0.2 | [-2.4, +1.8] | 237 / 241 | 0.891 |
| deepseek | strategyqa | judge | 1,999 | +5.3 | [+3.3, +7.3] | 271 / 165 | <1e-6 |
| deepseek | strategyqa | cover | 1,999 | +10.6 | [+8.2, +12.9] | 400 / 189 | <1e-6 |
| glm | ALL | judge | 7,999 | +4.1 | [+3.1, +5.2] | 1070 / 740 | <1e-6 |
| glm | ALL | cover | 7,999 | +5.2 | [+4.1, +6.2] | 1184 / 771 | <1e-6 |
| glm | 2wikimultihopqa | judge | 2,000 | +6.2 | [+4.2, +8.2] | 272 / 149 | <1e-6 |
| glm | 2wikimultihopqa | cover | 2,000 | +1.3 | [-0.9, +3.5] | 256 / 230 | 0.257 |
| glm | hotpotqa | judge | 2,000 | +2.2 | [+0.3, +4.2] | 217 / 172 | 0.0256 |
| glm | hotpotqa | cover | 2,000 | +3.0 | [+1.1, +5.0] | 225 / 164 | 0.00231 |
| glm | musique | judge | 2,000 | +7.0 | [+4.7, +9.4] | 363 / 222 | <1e-6 |
| glm | musique | cover | 2,000 | +8.8 | [+6.5, +11.0] | 356 / 181 | <1e-6 |
| glm | strategyqa | judge | 1,999 | +1.1 | [-0.9, +3.0] | 218 / 197 | 0.326 |
| glm | strategyqa | cover | 1,999 | +7.5 | [+5.3, +9.8] | 347 / 196 | <1e-6 |

## Teacher behaviour

| arm | guidance redacted for stating the answer | episodes with a redaction | answer statements that reached the student | generic fallback feedback | plan changed | teacher-accept rate | teacher-accept precision | teacher verdict agrees with judge | teacher approves wrong answers | teacher rejects right answers |
|---|---|---|---|---|---|---|---|---|---|---|
| self | 17.4 % | 53.3 % | 0 | 0.0 % | 46.0 % | 1.1 % | 58.8 % | 38.6 % | 0.0 % | 100.0 % |
| deepseek | 7.4 % | 22.7 % | 0 | 0.1 % | 74.3 % | 6.9 % | 99.5 % | 78.4 % | 0.5 % | 34.5 % |
| glm | 18.2 % | 44.6 % | 0 | 0.0 % | 3.0 % | 9.3 % | 99.6 % | 97.1 % | 1.8 % | 3.5 % |

Rates over guidance events count the plan review and every reviewed step. Teacher-behaviour rates use the judge verdict as the truth when the arm was judged, cover otherwise. "Answer statements that reached the student" re-checks the student-visible guidance and must be 0.
