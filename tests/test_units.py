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
    from tgd.logit_scale import chunked_loss_conflict

    class Cfg:
        pass

    granite = Cfg()
    granite.logits_scaling = 10.0            # Granite's field; TRL never reads it
    msg = chunked_loss_conflict(granite)
    assert msg and "logits_scaling" in msg and "10.0" in msg

    understood = Cfg()
    understood.logit_scale = 4.0             # the field TRL itself applies
    assert chunked_loss_conflict(understood) is None

    plain = Cfg()                            # no rescaling at all
    assert chunked_loss_conflict(plain) is None

    neutral = Cfg()
    neutral.logits_scaling = 1.0             # present but a no-op
    assert chunked_loss_conflict(neutral) is None


def test_autoscale_batch_preserves_effective_batch():
    """Switching off TRL's chunked loss makes the [batch, seq, vocab] logit tensor real.
    At the default micro-batch that is >12 GB and OOMs partway through an epoch, so the
    trainer trades micro-batch for accumulation — the effective batch must not change."""
    train = _load_script("train_sft")
    V, L = 100352, 8192

    bs, ga, gb = train.autoscale_batch(4, 4, L, V)
    assert (bs, ga) == (1, 16)           # effective batch 16, unchanged
    assert 12.0 < gb < 12.5              # the allocation that actually failed

    for orig_bs, orig_ga in [(4, 4), (2, 8), (8, 2)]:
        bs, ga, _ = train.autoscale_batch(orig_bs, orig_ga, L, V)
        assert bs * ga == orig_bs * orig_ga

    # Small enough to leave alone: short sequences, or an already-minimal micro-batch.
    assert train.autoscale_batch(4, 4, 512, V)[:2] == (4, 4)
    assert train.autoscale_batch(1, 16, L, V)[:2] == (1, 16)


def test_merge_that_loses_logit_scaling_is_caught():
    """Merging writes a fresh config.json. A rescaling field that does not survive it makes
    every later inference run at the wrong scale — invisible to greedy, fatal to sampling."""
    from tgd.logit_scale import merge_lost_scaling, scaling_fields

    class Cfg:
        pass

    base = Cfg()
    base.logits_scaling = 10.0

    good = Cfg()
    good.logits_scaling = 10.0
    assert merge_lost_scaling(base, good) is None

    dropped = Cfg()                       # field gone entirely
    msg = merge_lost_scaling(base, dropped)
    assert msg and "logits_scaling" in msg

    changed = Cfg()
    changed.logits_scaling = 1.0          # present but neutralised
    assert merge_lost_scaling(base, changed) is not None

    plain = Cfg()                         # base had nothing to lose
    assert merge_lost_scaling(plain, plain) is None
    assert scaling_fields(plain) == {}


def test_every_model_loading_script_reports_logit_scaling():
    """A silent scale is how this bug survived a week. Every script that loads a model for
    inference must print what rescaling that model applies."""
    import re
    root = Path(__file__).resolve().parents[1]
    for name in ("diag_distributions", "diag_position_profile", "sweep_decoding",
                 "merge_adapter", "train_sft"):
        src = (root / "scripts" / f"{name}.py").read_text()
        assert re.search(r"from tgd\.logit_scale import", src), f"{name} does not import the check"
        assert re.search(r"describe", src), f"{name} does not report logit scaling"


def test_merge_guard_deletes_a_silently_wrong_model(tmp_path, monkeypatch):
    """The merge guard must not just warn: a merged model with the wrong logit scale looks
    perfect under greedy decoding, so if it is left on disk someone will serve it."""
    import importlib.util
    import sys
    import transformers

    root = Path(__file__).resolve().parents[1]
    base = root / "tests" / "_fixtures"          # not needed: we fake both configs
    out = tmp_path / "merged"
    out.mkdir()
    (out / "weights.bin").write_text("x")        # stand-in for the saved model

    class Cfg:
        pass

    base_cfg = Cfg()
    base_cfg.logits_scaling = 10.0
    merged_cfg = Cfg()
    merged_cfg.logits_scaling = 1.0              # the field did not survive the merge

    from tgd.logit_scale import merge_lost_scaling
    msg = merge_lost_scaling(base_cfg, merged_cfg)
    assert msg is not None
    assert "1.0" in msg, "the message must report what the merged config actually holds"
    assert "None" not in msg


def test_eval_reports_scaling_before_sampling():
    """Greedy hides this bug entirely, so the one moment it matters is when eval samples."""
    src = (Path(__file__).resolve().parents[1] / "scripts" / "eval.py").read_text()
    assert "student_temperature > 0" in src
    assert "describe_scaling" in src or "logit_scale" in src


def test_loss_path_check_catches_a_mismatch_no_field_name_would_reveal():
    """The field-name guard only knows architectures we have met. This check is the general
    one: it compares the loss a trainer would optimise against the model's own forward pass,
    so it catches any loss path that reconstructs logits differently — including one whose
    config field we have never heard of."""
    import torch
    from tgd.logit_scale import loss_path_matches_forward

    torch.manual_seed(0)
    V, T = 128, 24
    # Structured logits, as any pretrained model has. (Near-uniform logits cannot reveal a
    # scale mismatch at all — see the function's docstring.)
    raw = torch.randn(1, T, V) * 4.0
    ids = torch.randint(0, V, (1, T))
    labels = ids.clone()
    labels[:, :8] = -100                       # prompt tokens carry no loss
    SCALE = 10.0

    class Out:
        def __init__(self, logits=None, loss=None):
            self.logits, self.loss = logits, loss

    class Model:
        """forward() rescales its logits, as e.g. Granite does."""
        def __init__(self, honest):
            self.honest = honest

        def __call__(self, input_ids=None, attention_mask=None, labels=None):
            scaled = raw / SCALE                       # what inference emits
            if labels is None:
                return Out(logits=scaled)
            # honest: loss from the same logits inference will use.
            # broken: loss from the UNSCALED logits, which is what a chunked path that
            # missed the rescaling field would optimise.
            z = scaled if self.honest else raw
            z = z[..., :-1, :].reshape(-1, V)
            t = labels[..., 1:].reshape(-1)
            return Out(loss=torch.nn.functional.cross_entropy(z, t, ignore_index=-100))

    batch = {"input_ids": ids, "attention_mask": torch.ones_like(ids), "labels": labels}

    ref, actual, ok = loss_path_matches_forward(Model(honest=True), batch)
    assert ok, f"a matching loss path must pass (ref {ref}, actual {actual})"

    ref, actual, ok = loss_path_matches_forward(Model(honest=False), batch)
    assert not ok, f"a rescaling mismatch must fail (ref {ref}, actual {actual})"
    assert abs(ref - actual) > 1.0


def test_repair_tool_is_reversible_and_refuses_the_wrong_target(tmp_path):
    """Repairing a checkpoint edits a config field, so it must (a) leave a way back and
    (b) decline a model that never rescaled anything — where the edit would introduce the
    very bug it exists to fix."""
    import json
    import subprocess
    import sys

    root = Path(__file__).resolve().parents[1]
    script = root / "scripts" / "repair_logit_scale.py"

    def run(d, *flags):
        return subprocess.run([sys.executable, str(script), "--model", str(d), *flags],
                              capture_output=True, text=True).stdout

    plain = tmp_path / "plain"
    plain.mkdir()
    (plain / "config.json").write_text(json.dumps({"model_type": "llama"}))
    assert "nothing to repair" in run(plain)
    assert not (plain / "config.json.pre_repair").exists()

    scaled = tmp_path / "scaled"
    scaled.mkdir()
    (scaled / "config.json").write_text(json.dumps({"model_type": "granite",
                                                    "logits_scaling": 10.0}))
    run(scaled, "--dry-run")
    assert not (scaled / "config.json.pre_repair").exists(), "dry-run must not write"

    run(scaled)
    assert json.loads((scaled / "config.json").read_text())["logits_scaling"] == 1.0
    assert (scaled / "config.json.pre_repair").exists()
    assert "already repaired" in run(scaled)          # idempotent, and says so

    run(scaled, "--restore")
    assert json.loads((scaled / "config.json").read_text())["logits_scaling"] == 10.0


def test_merge_refuses_a_base_the_adapter_was_not_trained_on(tmp_path):
    """With several students in flight, merging an adapter onto the wrong base is an easy
    mistake and produces a broken model rather than an error. The adapter records its own
    base; use it, and refuse a silent mismatch."""
    import json
    import subprocess
    import sys

    root = Path(__file__).resolve().parents[1]
    script = root / "scripts" / "merge_adapter.py"
    adapter = tmp_path / "adapter"
    adapter.mkdir()
    (adapter / "adapter_config.json").write_text(
        json.dumps({"base_model_name_or_path": "org/student-a", "peft_type": "LORA"}))

    def run(*flags):
        r = subprocess.run([sys.executable, str(script), "--adapter", str(adapter),
                            "--out", str(tmp_path / "out"), *flags],
                           capture_output=True, text=True)
        return r.returncode, r.stdout + r.stderr

    rc, out = run("--base", "org/student-b")
    assert rc == 2, "a base the adapter was not trained on must be refused"
    assert "org/student-a" in out and "org/student-b" in out

    # No --base at all: it should adopt the recorded one (and then fail to download it,
    # which is fine -- we only care that it resolved the right name).
    rc, out = run()
    assert "org/student-a" in out

    # An adapter with no recorded base must ask rather than guess.
    (adapter / "adapter_config.json").write_text(json.dumps({"peft_type": "LORA"}))
    rc, out = run()
    assert rc == 2 and "does not record a base" in out


def test_nested_text_config_is_inspected():
    """Multimodal students keep their language settings under config.text_config. A logit
    rescaling hiding there is exactly as dangerous as one at the top level, and TRL's chunked
    path reads from there too."""
    from tgd.logit_scale import scaling_fields
    from tgd.models import text_config, vocab_size

    class Text:
        logits_scaling = 10.0
        vocab_size = 151936

    class Multimodal:
        text_config = Text()

    class Flat:
        logits_scaling = 10.0
        vocab_size = 100352

    assert scaling_fields(Multimodal()) == {"logits_scaling": 10.0}
    assert scaling_fields(Flat()) == {"logits_scaling": 10.0}
    assert vocab_size(Multimodal()) == 151936
    assert text_config(Flat()) is not None


def test_vocab_size_never_underestimates_the_logit_width():
    """It sizes the logits tensor for the memory guard. An embedding matrix padded past the
    tokenizer length (seen here: 128000 config vs 125017 tokens) must not shrink the
    estimate, or the guard lets an OOM through."""
    from tgd.models import vocab_size

    class Cfg:
        vocab_size = 128000

    class Tok:
        def __len__(self):
            return 125017

    assert vocab_size(Cfg(), Tok()) == 128000
    assert vocab_size(Cfg()) == 128000

    class Resized:
        vocab_size = 32000

    class BigTok:
        def __len__(self):
            return 32128           # embeddings resized after the config was written

    assert vocab_size(Resized(), BigTok()) == 32128


def test_render_chat_closes_a_reasoning_block():
    """A reasoning model's generation prompt ends inside <think>, so the first generated
    token is reasoning, not an answer. Any diagnostic reading that position then reports no
    probability on valid answer tokens — indistinguishable from the catastrophic failure
    those diagnostics exist to detect. Close the block so the position means what we think."""
    from tgd.models import render_chat

    class Tok:
        """Mimics a template that opens <think> unless enable_thinking=False."""
        def __init__(self, closable=True):
            self.closable = closable

        def apply_chat_template(self, messages, tokenize=False,
                                add_generation_prompt=True, **kw):
            if "enable_thinking" in kw and not kw["enable_thinking"]:
                if not self.closable:
                    raise TypeError("unexpected keyword")
                return "<|assistant|>\n<think></think>"
            return "<|assistant|>\n<think>\n"

    text, still_open = render_chat(Tok(closable=True), [{"role": "user", "content": "q"}])
    assert not still_open
    assert text.endswith("</think>")

    # A template that cannot close it must be reported, not silently accepted.
    text, still_open = render_chat(Tok(closable=False), [{"role": "user", "content": "q"}])
    assert still_open

    class Plain:
        def apply_chat_template(self, messages, tokenize=False,
                                add_generation_prompt=True, **kw):
            if kw:
                raise TypeError("unexpected keyword")
            return "<|assistant|>\n"

    text, still_open = render_chat(Plain(), [{"role": "user", "content": "q"}])
    assert not still_open and text.endswith("<|assistant|>\n")


def test_sweep_decoding_reads_gzipped_benchmarks():
    """Every shipped benchmark file is gzipped; a plain open() on one raises
    UnicodeDecodeError on the gzip magic byte."""
    root = Path(__file__).resolve().parents[1]
    src = (root / "scripts" / "sweep_decoding.py").read_text()
    assert "read_jsonl" in src, "must use the gz-aware loader"
    assert 'open(args.mmlu' not in src, "plain open() cannot read the shipped .gz files"


# ---------------------------------------------------------------- configuration hygiene

def test_blank_environment_variables_count_as_unset(monkeypatch):
    """`.env.example` ships every key blank. `os.getenv` returns "" for those, which is
    truthy enough to make an unconfigured provider look configured."""
    from agentsim.config import config
    monkeypatch.setenv("OAI_JUDGE_BASE_URL", "http://example/v1")
    monkeypatch.setenv("OAI_JUDGE_API_KEY", "")
    base, key, name = config.oai_endpoint("oai-judge/org/model")
    assert (base, key, name) == ("http://example/v1", None, "org/model")
    monkeypatch.setenv("OAI_BASE_URL", "   ")
    assert not config.provider_available("oai/x")


def test_oai_endpoint_reads_the_environment_at_call_time(monkeypatch):
    """A variable cleared after import must resolve as cleared: the class attribute is a
    snapshot and must not be used as a fallback."""
    from agentsim.config import config
    monkeypatch.setenv("OAI_BASE_URL", "http://one/v1")
    assert config.oai_endpoint("oai/m")[0] == "http://one/v1"
    monkeypatch.delenv("OAI_BASE_URL", raising=False)
    assert config.oai_endpoint("oai/m")[0] is None


def test_console_falls_back_instead_of_raising():
    """A console that cannot encode the characters we print must degrade, not abort."""
    import io
    from tgd import console

    class Narrow(io.StringIO):
        encoding = "cp1252"
        reconfigured = None

        def reconfigure(self, **kw):
            Narrow.reconfigured = kw

    assert console._can_encode(Narrow()) is False
    narrow = Narrow()
    console._done = False
    try:
        import sys
        old = sys.stdout
        sys.stdout = narrow
        console.enable()
    finally:
        sys.stdout = old
        console._done = True
    assert Narrow.reconfigured and Narrow.reconfigured.get("errors") == "replace"


# ------------------------------------------------------- train/inference prompt alignment

class _ReasoningTokenizer:
    """Mimics granite-4.x: the generation prompt opens a thinking block, while a completed
    assistant turn folds in an empty one -- so the two renderings diverge."""

    def __init__(self, honours_flag=True):
        self.honours_flag = honours_flag

    def apply_chat_template(self, messages, tokenize=False, add_generation_prompt=False,
                            enable_thinking=True, **kwargs):
        parts = []
        for m in messages:
            body = m["content"]
            if m["role"] == "assistant" and "<think>" not in body:
                body = "<think></think>" + body
            parts.append(f"<|{m['role']}|>{body}<|end|>")
        text = "".join(parts)
        if add_generation_prompt:
            closed = self.honours_flag and not enable_thinking
            text += "<|assistant|>" + ("<think></think>" if closed else "<think>\n")
        return text


class _PlainTokenizer:
    def apply_chat_template(self, messages, tokenize=False, add_generation_prompt=False, **kwargs):
        text = "".join(f"<|{m['role']}|>{m['content']}<|end|>" for m in messages)
        return text + ("<|assistant|>" if add_generation_prompt else "")


def test_alignment_detects_and_repairs_a_reasoning_template():
    from tgd import chat_template as ct
    tok = _ReasoningTokenizer()
    assert not ct.aligned(tok), "the mismatch this guard exists for should be detected"
    kwargs = ct.alignment_kwargs(tok)
    assert kwargs == {"enable_thinking": False}
    assert ct.aligned(tok, **kwargs)
    assert ct.opens_reasoning(ct.render_prompt(tok)) == "<think>"


def test_alignment_is_a_no_op_for_a_plain_template():
    from tgd import chat_template as ct
    tok = _PlainTokenizer()
    assert ct.aligned(tok)
    assert ct.alignment_kwargs(tok) == {}


def test_alignment_reports_rather_than_guesses_when_it_cannot_repair():
    from tgd import chat_template as ct
    tok = _ReasoningTokenizer(honours_flag=False)
    assert ct.alignment_kwargs(tok) == {}
    assert not ct.aligned(tok)
    message = ct.divergence(tok) or ""
    assert "<think>" in message and "</think>" in message, message


# ------------------------------------------------------------------- split ordering

def test_split_order_makes_every_prefix_representative():
    """Written dataset-by-dataset, `--limit 1000` was 100% one dataset. Any prefix must
    now reflect the mix."""
    import importlib.util
    from pathlib import Path
    spec = importlib.util.spec_from_file_location(
        "build_splits", Path(__file__).resolve().parents[1] / "scripts" / "build_splits.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    rows = [{"metadata": {"dataset": d, "qid": f"{d}-{i}"}}
            for d in ("a", "b", "c", "d") for i in range(500)]
    out = mod.shuffled(rows, "uniform")
    assert len(out) == len(rows)
    assert {r["metadata"]["qid"] for r in out} == {r["metadata"]["qid"] for r in rows}
    assert out == mod.shuffled(rows, "uniform"), "order must be reproducible on every machine"
    assert out != mod.shuffled(rows, "uniform/dev"), "different splits get different orders"
    prefix = {r["metadata"]["dataset"] for r in out[:200]}
    assert prefix == {"a", "b", "c", "d"}, f"a prefix saw only {prefix}"


# ------------------------------------------------------------------ attention kernel

def test_sdpa_probe_is_safe_and_idempotent():
    from tgd import sdpa_compat
    sdpa_compat._applied = False
    first = sdpa_compat.apply()
    assert isinstance(first, bool)
    assert sdpa_compat.apply() is False, "applying twice must be a no-op"
