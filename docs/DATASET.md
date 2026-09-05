# The dataset, end to end

What the shipped data *is*, in the order it was built. `docs/DATA.md` is the field-by-field
reference for each file; this page is the picture those files fit into, and the vocabulary the
rest of the kit uses.

## The five things, and how they nest

```
question  (one QA item, has its own document corpus)
  └── episode          one attempt at that question, budget 3 steps
        ├── plan       drafted by the student, revised by the teacher
        └── step ×3    student acts → tool runs → teacher critiques
              └── training sample   one row of SFT data, derived from a step or a plan
```

**Question.** One item from a source dataset, keyed by `qid`. Carries the query, the gold
answer, the supporting facts that justify it, and metadata (`num_hops`, `question_type`,
`level`). All four sources are *multi-hop*: answering requires combining facts across
documents, which is what makes step-by-step behaviour worth teaching.

**Corpus.** Each question ships its own document set — the only thing the retrieval tool can
search for that question. Document ids are namespaced (`<qid>::doc3`), so retrieval for one
question can never reach another's documents. This keeps every episode self-contained and makes
the task reproducible without an external index.

**Episode.** One complete attempt at one question by the student, with the teacher supervising
every step, under a budget of 3 steps. **7,999 of them**, roughly 2,000 per dataset. This is the
central unit of the collected data. *"Trajectory" means the same thing.* Episode ids look like
`sample_147` — a naming artefact from collection, not a separate concept.

**Step.** One turn inside an episode, `t = 1, 2, 3`. Each step records the full exchange:

| Field | What it holds |
|---|---|
| `student_prompt` / `student_raw` | what the student was asked, and what it returned verbatim |
| `student_action` | the parsed action: `thought`, `decision`, `action.tool` + params, `new_facts_extracted` |
| `tool_observation` | what the tool returned (retrieved documents, extraction results, status) |
| `teacher_private_diagnosis` | detailed error analysis — **never shown to the student** |
| `student_visible_guidance` | a score and a short critique — this *is* shown |
| `metrics` | per-step correctness: `json_valid`, `action_schema_valid`, `invalid_action`, `retrieved_gold_doc`, … |
| `leakage_check` | whether the teacher's wording leaked the gold answer or a hidden document; sanitisations applied |

The split between private diagnosis and visible guidance is the point of the design: the teacher
sees the gold answer, the student must not, and every step is checked for leaks in both
directions.

**Training sample.** One row of supervised fine-tuning data derived from an episode:
`{prompt, completion, metadata}`. The prompt is a system + user message; the completion is the
assistant message the model learns to produce. The teacher's guidance is folded *into* the
target as though it were the student's own reasoning — "guidance as internal thought", the core
idea of the method. Two kinds:

| Kind | Count | Target |
|---|---|---|
| `plan` | 3,708 | the revised plan for the whole question |
| `action` | 10,750 | one step's thought + action |

## The tools a student can call

Observed across the collected episodes, most to least used: `search` (retrieve documents),
`finish` (commit to an answer), `extract` (pull a fact from a retrieved document), `verify`
(check a claim against evidence), `decompose` (break the question into sub-questions),
`reformulate` (rewrite a failing query), `synthesize` (combine facts). Each action also carries a
`decision.category` recording *why* the student chose it.

Two `stop_reason` values occur: `budget_forced_finish` (the common case — the 3-step budget ran
out) and `teacher_accept` (the teacher judged the answer complete early).

## How it was built

**1. Questions and corpora prepared** per dataset, each question with its own document set.

**2. Episodes collected.** The student attempted every question while the teacher critiqued each
step. Student temperature 0.2, teacher 0.1, budget 3, guidance level 3 throughout. Two teacher
checkpoints were used across the run and every episode records which one, so the mix is
auditable rather than hidden.

| Dataset | Episodes | Correct final answer | Answer grounded in retrieved evidence |
|---|---|---|---|
| 2WikiMultihopQA | 2,000 | 1,385 | 1,629 |
| HotpotQA | 2,000 | 1,296 | 1,802 |
| MuSiQue | 2,000 | 595 | 1,491 |
| StrategyQA | 1,999 | 1,111 | 1,139 |

MuSiQue is much harder than the rest — worth remembering when reading per-dataset results.

**3. Questions assigned to pools.** Each `qid` is hashed to `heldout_test` (10 %) or `trainable`
(90 %). The hash is deterministic and salted, so the assignment is stable across machines and
re-runs, and no shuffling seed can quietly change it.

**4. Episodes filtered into training samples.** This step is deliberately aggressive, and it is
where most of the data goes:

| Dropped | Why | Count |
|---|---|---|
| episode's final answer was wrong | a wrong trajectory teaches a wrong trajectory | 2,865 of 7,252 trainable |
| target asserts a gold answer never present in the prompt | "correct but ungrounded" — teaches answering without evidence | 119 |
| target still contains a masking placeholder | an artefact would be learned as text | 22 |
| malformed target, or duplicates a held-out question | — | 2 |

7,252 trainable episodes → 4,387 correct → **14,835 samples** (14,458 train + 377 dev).

**5. Leakage audited.** `data/splits/leakage_report.json` checks, for every test set: `qid`
overlap with training, verbatim question text appearing in training, near-duplicate questions,
and pool-assignment mismatches. All report **zero**.

## The splits

**Held-out test — `data/splits/test/`.** Two sizes per dataset: `heldout_*` is the 10 % pool
(747 questions total, the standard test set) and `full_*` is every question in the dataset,
for a larger but slower evaluation. Test files include *every* question in the pool, whether or
not the collection episode got it right — otherwise the test set would be biased toward
questions the student already handled.

**Group B, uniform — `data/splits/uniform/`.** Train on all four datasets, test on the held-out
10 % of each. 14,458 train + 377 dev samples from 3,959 questions. This is the default.

**Group A, leave-one-dataset-out — `data/splits/lodo/fold_<ds>/`.** Four folds. Each trains on
three datasets and tests on the fourth, which the model has never seen, *plus* the held-out
questions of the three it did see. This separates "learned the task" from "learned these
datasets".

## Files you will actually open

| Path | What it is |
|---|---|
| `data/questions/<ds>/*_questions.jsonl.gz` | the questions |
| `data/questions/<ds>/*_corpus.jsonl.gz` | their documents |
| `data/episodes/episodes.jsonl.gz` | all 7,999 episodes (82 MB) |
| `data/episodes/index.jsonl` | one small row per episode — scan this instead of the big file |
| `data/splits/uniform/{train,dev}.jsonl` | SFT data — **not shipped**; run `make data` (~2 min) to build it from the episodes |
| `data/splits/test/*.jsonl` | evaluation question sets |
| `data/splits/{stats,leakage_report,pools}.json` | counts, the audit, and the pool assignment |

All `.jsonl.gz` files are gzipped; `tgd.io.read_jsonl` reads either form transparently, so
scripts take the path as-is.

**One thing is built, not shipped.** The SFT train/dev files are 82 MB and derive
deterministically from the episodes, so the repository tracks the inputs and not the output.
`make data` rebuilds them in about two minutes, byte-identically on any machine, and also
re-runs the leakage audit. Everything else on this page ships as-is: the episodes, the
questions and corpora, the test question sets, the pool assignment, the stats and the audit.

## Two things to know before using it

**The published episodes are cleaned.** Provider response bodies and routing prefixes are
stripped, so they are shareable but not byte-identical to raw harness output. Anything you
collect yourself passes through the same cleaning (`tgd/episodes.py`).

**Half the collected data never reaches training, by design.** If you rebuild the splits with
different filters, expect the sample count to move a lot — and expect quality to move with it.
The filters exist because a wrong or ungrounded trajectory is worse than no trajectory.
