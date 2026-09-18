import json, sys, statistics as st, collections
SP = sys.argv[1]
rows = [json.loads(l) for l in open(f"{SP}/results.jsonl")]
by = collections.defaultdict(list)
for r in rows: by[(r["gateway"], r["model"])].append(r)
def kappa(pairs):
    n = len(pairs)
    if not n: return float("nan")
    po = sum(a == b for a, b in pairs) / n
    pa = sum(a for a, _ in pairs) / n; pb = sum(b for _, b in pairs) / n
    pe = pa * pb + (1 - pa) * (1 - pb)
    return (po - pe) / (1 - pe) if pe < 1 else float("nan")
out = []
for (gw, m), rs in by.items():
    n = len(rs)
    v = [r for r in rs if r["verdict"] is not None]
    strict = sum(1 for r in rs if r["verdict"] == r["label"]) / n
    easy = [r for r in rs if r["id"].startswith("E")]; hard = [r for r in rs if r["id"].startswith("H")]
    acc = lambda s: sum(1 for r in s if r["verdict"] == r["label"]) / len(s) if s else float("nan")
    neg = [r for r in rs if r["label"] == 0]; pos = [r for r in rs if r["label"] == 1]
    far = sum(1 for r in neg if r["verdict"] == 1) / len(neg) if neg else float("nan")
    frr = sum(1 for r in pos if r["verdict"] == 0) / len(pos) if pos else float("nan")
    flip = [r for r in rs if r["kind"] == "E4_gold_flipped_wrong"]
    lat = st.median([r["latency"] for r in rs if r["status"] == "ok"] or [0])
    toks = [r["out_tokens"] for r in rs if r["out_tokens"]]
    costs = [r["cost"] for r in rs if r["cost"] is not None]
    out.append(dict(gw=gw, model=m, n=n, parsed=len(v) / n, strict=strict, easy=acc(easy), hard=acc(hard),
                    far=far, frr=frr, flip=acc(flip), kappa=kappa([(r["verdict"], r["label"]) for r in v]),
                    lat=lat, tok=st.mean(toks) if toks else 0, cost_k=1000 * st.mean(costs) if costs else None,
                    errs=collections.Counter(r["status"] for r in rs if r["status"] != "ok")))
out.sort(key=lambda d: (-d["strict"], -(d["kappa"] if d["kappa"] == d["kappa"] else -1)))
print(f"{'model':<50}{'gw':<8}{'n':>4}{'parsed':>7}{'acc':>6}{'easy':>6}{'hard':>6}{'κ':>6}{'falseOK':>8}{'falseNO':>8}{'flip':>6}{'lat s':>6}{'tok':>6}{'$/1k':>8}  errors")
for d in out:
    ck = f"{d['cost_k']:.3f}" if d["cost_k"] is not None else "-"
    print(f"{d['model']:<50}{d['gw']:<8}{d['n']:>4}{100*d['parsed']:>6.0f}%{100*d['strict']:>5.1f}{100*d['easy']:>6.1f}{100*d['hard']:>6.1f}{d['kappa']:>6.2f}"
          f"{100*d['far']:>7.1f}%{100*d['frr']:>7.1f}%{100*d['flip']:>5.0f}%{d['lat']:>6.1f}{d['tok']:>6.0f}{ck:>8}  {dict(d['errs']) or ''}")
json.dump(out, open(f"{SP}/scores.json", "w"), indent=1, default=str)
