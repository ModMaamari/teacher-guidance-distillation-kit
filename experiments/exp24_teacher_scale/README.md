# exp24 — Plain teacher distillation at the self-guided scale

**Why.** The teacher's own rollouts train the best student per episode (E01: 67.7 % at ~1,400
usable episodes), but only 2,000 were collected because they run a 284B-parameter model as the
agent. Self-Guidance trains on 3,818. A reviewer will ask what plain distillation does with the
same number of usable episodes, which is the fair "normal distillation" baseline.

**Design.** Extend the teacher-rollout collection from 500 to 1,250 questions per dataset (the
command resumes and skips what exists), which at a 78 % keep rate yields about 3,900 usable
episodes, matching the self-guided split. Then train three seeds and compare with the self-guided
students, in accuracy and in end-to-end cost (E23): the teacher writes more output tokens per
episode and needs its 284B weights hosted, but it fails far less often, so it needs fewer episodes.

**Two gateways.** The first 2,000 episodes were collected through the primary gateway. On
2026-09-20 its DeepSeek deployment began returning HTTP 500 (the other models it serves were
unaffected), so the rest were collected through a second gateway serving the same model id. Every
call records the model id it used, so the episodes remain separable; `provider_split.py` compares
what the experiment depends on -- how often an episode ends correct, its steps and its tokens --
and its output is published with the results. A large gap belongs in the write-up, because the
paper already documents one teacher run whose accuracy moved when the provider and the token cap
changed (appendix).

**Run.** `collect_teachdist_more` (API, resumable), `prep_e24` (consolidate + build
`data/splits_teachdist_full`), `train_teachdist_full_s{13,17,23}`, `eval_*`, `judge_*`,
`results_E24`.
