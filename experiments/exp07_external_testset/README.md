# exp07 — Contamination, and a test set the student cannot have memorised

**Tier 2.** HotpotQA, 2WikiMultihopQA, MuSiQue and StrategyQA are old and widely mirrored,
so they are plausibly in the pretraining data of every model here. Leave-one-dataset-out
shows *transfer*, but every fold still tests on a public benchmark. Two things close it.

## 1. Measure overlap you already have

`contamination_check.py` reports n-gram overlap between held-out test questions and the
training examples actually fed to the optimiser. This finds leakage the qid-level audit
cannot see: the same fact asked in different words, or a near-duplicate question.

```bash
python contamination_check.py --split data/splits/uniform \
       --test 'data/splits/test/heldout_*_questions.jsonl' --n 8
```

`scripts/check_leakage.py` already guarantees no qid appears in both. This is the softer,
more honest check, and reporting a small non-zero number is better than claiming zero.

## 2. Add one genuinely external set

Pick something released after your students' pretraining cutoffs, or hand-written. The kit
takes any dataset in its own format, so this is a data task, not a code task:

```
data/questions/<name>/<name>_questions.jsonl
data/questions/<name>/<name>_corpus.jsonl.gz
```

`docs/DATA.md` §4 gives the schema. `prepare_external.py` converts a simple
question/answer/documents JSONL into it and validates the result.

Then evaluate every arm on it:

```bash
export PARTITION=<gpu-partition>
bash run.sh
```

## Reporting

A method that holds up on an uncontaminated set is worth a paragraph in the abstract. If
accuracy drops sharply there, report it: the honest framing is that the four public sets
overstate absolute accuracy while the *relative* ordering of arms survives, which is still
the paper's claim.
