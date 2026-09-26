# E29 — Does the self-guided gain survive removing the retry channel?

**Question.** During collection the critic may reject a `finish` and let the episode continue; at
inference a `finish` always ends the episode. 507 of the kept self-guided episodes contain such a
rejected finish. Their targets describe states the deployed student never reaches, and on yes/no
questions a rejection nearly gives the answer away. Is that retry channel what produced the gain?

**Answer.** No. Removing it leaves accuracy where it was. Judge-correct accuracy (Gemma-4-31B-it)
on the 747 held-out questions, seeds 13, 17 and 23:

| Training data | Examples | Questions | 13 | 17 | 23 | Mean | Train PFLOPs | Voluntary finish |
|---|---|---|---|---|---|---|---|---|
| Self-guided, full (E25) | 13,825 | 3,818 | 66.7 | 64.9 | 63.2 | **64.9 ± 1.7** | 684 | 11.1 % |
| Episodes with a rejected finish dropped | 11,985 | 3,315 | 63.3 | 64.7 | 66.7 | **64.9 ± 1.7** | 595 | 1.6 % |
| Rejected-finish target and the next one dropped | 12,888 | 3,815 | 64.4 | 64.4 | 64.4 | **64.4 ± 0.0** | 623 | 1.8 % |
| Unguided self-rollouts (E25) | 13,510 | 3,753 | 62.3 | 64.8 | 62.6 | 63.2 ± 1.4 | 602 | 6.5 % |

Seed-averaged paired test (each question averaged over an arm's seeds), bootstrap 95 % CI,
sign-flip p, Holm over the two planned contrasts:

| Contrast | Δ | 95 % CI | p | Holm |
|---|---|---|---|---|
| full → episodes dropped | −0.0 | −1.5 to +1.4 | 1.00 | 1.00 |
| full → targets dropped | −0.5 | −2.0 to +0.9 | 0.50 | 1.00 |
| unguided → episodes dropped | +1.6 | −0.2 to +3.5 | 0.083 | — |
| unguided → targets dropped | +1.2 | −0.7 to +3.1 | 0.25 | — |

Both intervals exclude a loss as large as the whole six-seed gain over unguided rollouts (+2.3,
E25), so the retry channel cannot account for that gain. Against unguided rollouts both variants
sit where the full self-guided arm sat at three seeds (+1.7, p 0.089, E21); three seeds per arm
were not enough to establish that gap then either.

This is the first pre-stated outcome in `experiments/exp29_retry_channel/README.md`: *both variants
hold the self-guided level, so the retry channel is not what produced the gain, and the cleaner
variant can replace it.* Dropping the episodes also trains on 13 % less compute.

**What does change: early finishing.** Without the retry channel the student almost stops ending
episodes on its own (voluntary finish 11.1 % → 1.6 % and 1.8 %; unguided 6.5 %, base 3.2 %) and
uses about 4 % more tokens per question (5,175 → 5,373). The reason is in the data: in the
trainable pool, 507 kept episodes contain 520 finishes the critic rejected, against 55 episodes
that end early with the critic's acceptance. About nine in ten early-finish targets the full student
learns from are finishes the critic turned down. Accuracy is unaffected either way.

**Checks.** The three "targets dropped" seeds landing on the same 481 of 747 is a coincidence: the
three adapters differ (checksums), their episode files differ, and they disagree with each other on
78 to 92 questions, as far apart as the seeds of the full arm (88 to 91). Every run was trained on
its own split with its own seed (`train_config.json`).

**Protocol.** `scripts/build_splits.py --retry drop-episodes|drop-targets` on the self-guided
episodes (`data/episodes_self`); a rejected finish is a `finish` step that is not the episode's last
step. `drop-targets` removes that step's target and the following one (numbered by `step["t"]`).
Same LoRA recipe and seeds as the self-guided students. Pool tasks `prep_e29`,
`train_retry_{episodes,targets}_s{13,17,23}`, `eval_*`, `judge_*`, `results_E29`.

**Files.** `kit/summary.txt`/`.json` (accuracy, steps, tokens, voluntary finish, all tests),
`kit/results.json`/`RESULTS.md`, `kit/train_cost.txt`/`.json` (examples, tokens, PFLOPs, GPU-hours,
peak memory: 18.1 GiB for every arm).

**Caveats.** Three seeds per arm. The intervals bound the loss from removing the channel at about
1.5 to 2 points; they do not exclude a small effect. The unguided comparison needs E25-scale seeds
to be decided for the new variants.
