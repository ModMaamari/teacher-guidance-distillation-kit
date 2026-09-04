"""Unit tests (CPU, seconds): python -m pytest tests/ -q"""
from __future__ import annotations

import asyncio
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import tgd  # noqa: F401,E402
from tgd.splits import is_dev, pool_of  # noqa: E402
from tgd.metrics import aggregate, episode_tokens  # noqa: E402


def test_pool_is_deterministic_and_roughly_ten_percent():
    qids = [f"q{i}" for i in range(20000)]
    a = [pool_of(q) for q in qids]
    b = [pool_of(q) for q in qids]
    assert a == b
    frac = sum(x == "heldout_test" for x in a) / len(a)
    assert 0.09 < frac < 0.11
    assert pool_of("abc", salt="other") in ("heldout_test", "trainable")
    assert sum(is_dev(q) for q in qids) / len(qids) < 0.05


def test_provider_resolution(monkeypatch):
    from agentsim.config import config
    assert config.get_provider_from_model_id("oai/x") == "oai"
    assert config.get_provider_from_model_id("oai-judge/org/model") == "oai"
    assert config.get_provider_from_model_id("mock/anything") == "mock"
    assert config.get_provider_from_model_id("vllm/student") == "vllm"
    monkeypatch.setenv("OAI_JUDGE_BASE_URL", "http://example/v1")
    base, key, name = config.oai_endpoint("oai-judge/org/model")
    assert (base, key, name) == ("http://example/v1", None, "org/model")
    assert config.provider_available("oai-judge/org/model")
    monkeypatch.delenv("OAI_BASE_URL", raising=False)
    assert not config.provider_available("oai/unconfigured")


def test_mock_outputs_validate_against_schemas():
    from agentsim.clients.mock_provider import mock_completion
    from agentsim.teacher_guidance.json_utils import parse_student_action, parse_teacher_evaluation
    first = mock_completion("You are an information-seeking retrieval agent ...\nQuestion: Who?\nPrevious actions: []\n")
    action, meta = parse_student_action(first)
    assert action.action.tool == "search"
    later = mock_completion("You are an information-seeking retrieval agent ...\nQuestion: Who?\nPrevious actions: [{\"tool\": \"search\"}]\n")
    action, meta = parse_student_action(later)
    assert action.action.tool == "finish"
    ev, _ = parse_teacher_evaluation(mock_completion("You are a teacher evaluating one step of ...\nQuestion: Who?\n"))
    assert ev.teacher_decision == "continue"
    assert json.loads(mock_completion("You are grading one answer\nQuestion: q\nGold answer: Paris\nModel answer: paris, france\n"))["correct"] == 1


def test_judge_parse():
    from scripts.judge import parse_verdict
    assert parse_verdict('text {"correct": 1, "reason": "ok"} trailing')["correct"] == 1
    assert parse_verdict('{"correct": "0"}')["correct"] == 0
    assert parse_verdict("no json") is None
    assert parse_verdict('{"score": 1}') is None


def test_metrics_aggregate_and_tokens():
    ep = {"qid": "a", "final_metrics": {"exact_match": True, "f1": 1.0, "cover_match": True, "doc_recall": 0.5},
          "used_steps": 2, "stop_reason": "finish", "elapsed_s": 1.0,
          "plan": {"gen_stats": {"prompt_tokens": 10, "completion_tokens": 5}},
          "steps": [{"gen_stats": {"prompt_tokens": 100, "completion_tokens": 20}, "action_valid": True},
                    {"student_calls": [{"usage": {"prompt_tokens": 50, "completion_tokens": 5, "cost": 0.001}}],
                     "teacher_calls": [{"usage": {"prompt_tokens": 70, "completion_tokens": 30}}], "action_valid": False}]}
    t = episode_tokens(ep)
    assert (t["student_in"], t["student_out"], t["teacher_in"], t["teacher_out"], t["plan_in"]) == (150, 25, 70, 30, 10)
    agg = aggregate([ep], judge={"a": 1})
    assert agg["em"] == 1.0 and agg["invalid_action_steps"] == 1 and agg["judge_correct"] == 1.0
    assert agg["total_tokens_per_ep"] == 290.0 and abs(agg["api_cost_usd"] - 0.001) < 1e-9


def test_hybrid_client_routes_local_student():
    from tgd.guided_loop import LOCAL_STUDENT, HybridLLMClient
    from tgd.mock_policy import MockPolicy

    class FakeTeacher:
        async def get_completion(self, prompt, model=None, **kw):
            return f"teacher:{model}"

        async def get_completion_with_fallback(self, models, **kw):
            return f"teacher:{models[0]}", models[0]

    c = HybridLLMClient(MockPolicy(), FakeTeacher(), serialize_gpu=False)
    out = asyncio.run(c.get_completion("Question: x\nPrevious actions: []\n", model=LOCAL_STUDENT, return_raw=True))
    assert "search" in out["text"] and out["usage"]["prompt_tokens"] > 0
    assert asyncio.run(c.get_completion("p", model="mock/t")) == "teacher:mock/t"


def test_benchmark_answer_parsers():
    """The forgetting check scores generatively, so its parsers must be exact about what
    counts as the requested format and lenient only as a documented fallback."""
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "eval_benchmarks", Path(__file__).resolve().parents[1] / "scripts" / "eval_benchmarks.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    assert mod.parse_mcq("B") == ("B", "B")
    assert mod.parse_mcq("B.") == ("B", "B")
    assert mod.parse_mcq("A) 0") == ("A", "A")
    assert mod.parse_mcq("The answer is C") == (None, "C")          # lenient only
    assert mod.parse_mcq('{"answer": "D"}') == (None, "D")          # agent-format relapse
    assert mod.parse_mcq("hello") == (None, None)                    # unparseable
    assert mod.parse_mcq("") == (None, None)

    assert mod.parse_numeric("#### 18") == ("18", "18")
    assert mod.parse_numeric("blah\n#### 1,200") == ("1200", "1200")
    assert mod.parse_numeric("The answer is 42") == (None, "42")
    assert mod.parse_numeric("") == (None, None)

    row = {"kind": "mcq", "gold": "B", "choices": ["a", "b", "c", "d"], "question": "q"}
    assert mod.score(row, "B")["strict_correct"] == 1
    assert mod.score(row, "The answer is B")["strict_correct"] == 0
    assert mod.score(row, "The answer is B")["lenient_correct"] == 1
    assert mod.score(row, "zzz")["format_fail"] == 1
    num = {"kind": "numeric", "gold": "18", "choices": [], "question": "q"}
    assert mod.score(num, "#### 18.00")["strict_correct"] == 1


def _load_script(name):
    import importlib.util
    path = Path(__file__).resolve().parents[1] / "scripts" / f"{name}.py"
    spec = importlib.util.spec_from_file_location(f"_script_{name}", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_kl_direction_matches_its_definition():
    """The argument order of F.kl_div is easy to get backwards, and getting it backwards
    silently trains the opposite objective. Pin it against the definition."""
    import torch

    train = _load_script("train_sft")
    torch.manual_seed(0)
    student = torch.randn(8, 32)
    base = torch.randn(8, 32)

    p_s = torch.softmax(student, -1)
    p_b = torch.softmax(base, -1)
    expect_forward = (p_b * (p_b.log() - p_s.log())).sum(-1).mean()   # KL(base || student)
    expect_reverse = (p_s * (p_s.log() - p_b.log())).sum(-1).mean()   # KL(student || base)

    assert torch.allclose(train.kl_term(student, base, "forward"), expect_forward, atol=1e-5)
    assert torch.allclose(train.kl_term(student, base, "reverse"), expect_reverse, atol=1e-5)
    assert train.kl_term(student, student, "reverse").abs() < 1e-5    # zero against itself

    # Masking the supervised token changes the value but keeps the term finite and non-negative.
    tgt = torch.randint(0, 32, (8,))
    masked = train.kl_term(student, base, "reverse", target_ids=tgt)
    assert torch.isfinite(masked) and masked >= 0
    assert not torch.allclose(masked, expect_reverse, atol=1e-5)


def test_truncation_params_are_sent_only_when_sampling():
    """Greedy must stay greedy: no truncation knob may leak into a temperature-0 request."""
    from tgd.vllm_backend import VllmPolicy

    sent = {}

    class FakeResponse:
        def raise_for_status(self):
            pass

        def json(self):
            return {"choices": [{"message": {"content": "ok"}}], "usage": {}}

    class FakeClient:
        def post(self, url, json):
            sent.clear()
            sent.update(json)
            return FakeResponse()

    pol = VllmPolicy(min_p=0.1, top_k=50, top_p=0.9, seed=7)
    pol._client = FakeClient()
    msgs = [{"role": "user", "content": "hi"}]

    pol._one(msgs, 16, 0.0)
    assert sent["temperature"] == 0.0
    assert not {"top_p", "min_p", "top_k", "seed"} & set(sent)

    pol._one(msgs, 16, 0.7)
    assert (sent["top_p"], sent["min_p"], sent["top_k"], sent["seed"]) == (0.9, 0.1, 50, 7)

    pol2 = VllmPolicy()                      # defaults: nucleus only, no min_p / top_k
    pol2._client = FakeClient()
    pol2._one(msgs, 16, 0.7)
    assert "min_p" not in sent and "top_k" not in sent


def test_diagnostic_prompt_builders_read_the_shipped_data():
    """The stability diagnostics must load the gzipped episodes and benchmark files as shipped."""
    root = Path(__file__).resolve().parents[1]
    diag = _load_script("diag_distributions")

    episodes = root / "data/episodes/episodes.jsonl.gz"
    if episodes.exists():
        rows = diag.agent_prompts(str(episodes), 4)
        assert 0 < len(rows) <= 4
        assert all(r.get("messages") for r in rows)

    mmlu = root / "data/benchmarks/mmlu/test.jsonl"
    if mmlu.exists():
        rows = diag.mmlu_prompts(str(mmlu), 4)
        assert 0 < len(rows) <= 4
        assert all(r.get("messages") for r in rows)


def test_position_profile_buckets_partition_every_index():
    """Each completion position must fall in exactly one bucket, or the profile silently
    drops or double-counts tokens."""
    prof = _load_script("diag_position_profile")
    for k in list(range(300)) + [999, 100000]:
        hits = [(a, b) for a, b in prof.BUCKETS if a <= k < b]
        assert len(hits) == 1, f"position {k} matched {len(hits)} buckets"
    assert prof.BUCKETS[0] == (0, 1)          # the first generated token, measured alone
    assert prof.BUCKETS[-1][1] == float("inf")   # last bucket open-ended: nothing is dropped
    assert prof.summarise([]) == {}
    s = prof.summarise([1.0, 2.0, 3.0])
    assert s["n"] == 3 and s["median"] == 2.0


def test_logit_scaling_conflict_detection():
    """TRL's chunked loss reads config.logit_scale. A model that rescales logits under a
    different field name trains at the wrong scale — greedy still works, sampling breaks —
    so the mismatch has to be caught before training, not after evaluation."""
    train = _load_script("train_sft")

    class Cfg:
        pass

    granite = Cfg()
    granite.logits_scaling = 10.0            # Granite's field; TRL never reads it
    msg = train.logit_scaling_conflict(granite)
    assert msg and "logits_scaling" in msg and "10.0" in msg

    understood = Cfg()
    understood.logit_scale = 4.0             # the field TRL itself applies
    assert train.logit_scaling_conflict(understood) is None

    plain = Cfg()                            # no rescaling at all
    assert train.logit_scaling_conflict(plain) is None

    neutral = Cfg()
    neutral.logits_scaling = 1.0             # present but a no-op
    assert train.logit_scaling_conflict(neutral) is None
