# E09 — Forgetting (partial)

**Done so far.** The original all-4 adapter (E00) against the base weights, 4,529 items answered in
chat format (`docs/RESULTS.md`, `docs/FORGETTING.md`): MMLU −0.9 points (95 % CI −2.1 to +0.3),
GSM8K −2.2 (−3.8 to −0.7, p 0.007), HellaSwag −1.1 (−2.5 to +0.3); pooled −1.4 (−2.1 to −0.5,
p 0.001). That adapter was trained through the loss path later fixed (E14); these greedy numbers
are unaffected by that fix.

**Still to do.** Rerun on the corrected adapter (E14) and on every new trained arm, and copy the
report here.
