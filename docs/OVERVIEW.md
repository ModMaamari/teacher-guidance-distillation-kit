# How the pieces fit

```
                      data/questions/<ds>/{questions,corpus}.jsonl
                                     │
        scripts/collect_episodes.py  │  student (vLLM) + teacher (API)  ──►  runs/collect/
        scripts/consolidate_episodes.py                                 ──►  data/episodes/episodes.jsonl.gz
                                     │
        scripts/build_splits.py      │  pool = hash(qid)  ──►  data/splits/{uniform, lodo/fold_*, test/}
        scripts/check_leakage.py     │                    ──►  data/splits/leakage_report.json
                                     │
        scripts/train_sft.py         │  LoRA SFT          ──►  runs/train/<name>/adapter
        scripts/serve_vllm.sh        │  base + adapters on :8300
                                     │
        scripts/eval.py --arm student|guided|teacher      ──►  runs/eval/<arm>/<test-set>/episodes.jsonl
        scripts/judge.py             │  any judge API     ──►  runs/judge/verdicts.jsonl
        scripts/collect_results.py   │                    ──►  runs/results/{results.json, RESULTS.md}
                                     │
        scripts/eval_benchmarks.py   │  forgetting check   ──►  runs/forgetting/
        scripts/merge_adapter.py     │  adapter ──► standalone weights, for the diagnostics below
        scripts/diag_distributions.py│  next-token entropy / top-1 / valid mass
        scripts/sweep_decoding.py    │  task metrics across temperature and truncation
        scripts/diag_position_profile.py  entropy by position within the completion
```

The first two rows are the expensive part. Everything below the split line runs off a
finished adapter, so the diagnostics and the forgetting check can be repeated cheaply while
you iterate on training.

## Code map

| Path | Role |
|---|---|
| `agentsim/` | the simulation harness: prompt renderer (`teacher_guidance/prompts.py`), tool executor and per-question BM25 retrieval (`teacher_guidance/tool_executor.py`, `teacher_guidance/local_retrieval.py`), teacher critic and plan review components (`components/control/`), leakage gate (`teacher_guidance/leakage.py`), metrics, the provider client (`clients/llm_client.py`, `config.py`), the `simulate` CLI used for collection |
| `tgd/hf_agent_loop.py` | the teacherless student loop (used by the student arms), batched over episodes |
| `tgd/guided_loop.py` | the guided and teacher-alone arms, driving the harness components with a hybrid client |
| `tgd/vllm_backend.py`, `tgd/mock_policy.py` | student policies: a vLLM server client; an offline mock |
| `tgd/episode_lib.py` | turns an episode into "guidance as internal thought" SFT examples, with the placeholder and leakage gates |
| `tgd/episodes.py`, `tgd/splits.py`, `tgd/metrics.py`, `tgd/io.py`, `tgd/logging_utils.py` | publishable episode view, hash split, aggregate metrics, JSONL I/O, logging |
| `templates/workflows/` | the harness workflow definitions per step budget; `templates/prompts/` prompt fragments |
| `templates/simulations/` | collection templates written by `collect_episodes.py` |
| `scripts/merge_adapter.py`, `scripts/diag_distributions.py`, `scripts/diag_position_profile.py`, `scripts/sweep_decoding.py` | decoding-stability toolkit: fold the LoRA into base weights, measure the next-token distribution on in- and out-of-distribution prompts, locate where along a completion it flattens, sweep temperature against truncation (`docs/STABILITY.md`) |
| `scripts/prepare_benchmarks.py`, `scripts/eval_benchmarks.py`, `scripts/forgetting_report.py` | the forgetting check: build MMLU / GSM8K / HellaSwag eval splits, score any arm on them, then aggregate repeated runs into statistics and box plots (`docs/FORGETTING.md`) |

## The data

`docs/DATASET.md` explains the units — question, episode, step, training sample — and how the
shipped data was collected and filtered. `docs/DATA.md` is the per-file reference.

## Conventions

* Every long job takes a fixed `--out` directory, appends results as they land, writes
  `status.json`, and marks completion with `.done`. Re-running is always safe.
* Model ids carry their provider as a prefix (`docs/PROVIDERS.md`); the student inside
  the student arms is addressed by its served name or HF id instead.
* Logs are UTC-timestamped. Nothing under `runs/` is needed to rebuild anything else.
