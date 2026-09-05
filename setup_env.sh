#!/usr/bin/env bash
# Create the three virtual environments. Run on a machine with the GPU driver visible
# (a GPU node / interactive GPU session) so the CUDA wheels resolve correctly.
#
#   bash setup_env.sh            # all three
#   ONLY=base bash setup_env.sh  # just the CPU env (data, judge, teacher arm, results)
#
# Env vars: PY (python >= 3.11, default python3), TORCH_INDEX (default cu124 wheels),
#           ONLY (base | train | serve).
set -euo pipefail
cd "$(dirname "$0")"
PY=${PY:-python3}
TORCH_INDEX=${TORCH_INDEX:-https://download.pytorch.org/whl/cu124}
ONLY=${ONLY:-}
export HF_HOME=${HF_HOME:-$PWD/.cache/hf}
export PIP_CACHE_DIR=${PIP_CACHE_DIR:-$PWD/.cache/pip}
mkdir -p "$HF_HOME" "$PIP_CACHE_DIR"
echo "== $($PY --version) | HF_HOME=$HF_HOME =="

want() { [ -z "$ONLY" ] || [ "$ONLY" = "$1" ]; }
# Virtualenvs put their interpreter in bin/ on POSIX and Scripts/ on Windows; ask
# rather than assume, so this script works under Git Bash / MSYS too.
venv_py()  { for c in "$1/bin/python" "$1/Scripts/python.exe"; do [ -x "$c" ] && { echo "$c"; return; }; done; echo ""; }
venv_has() { [ -n "$(venv_py "$1")" ]; }

if want base && ! venv_has .venv; then
  $PY -m venv .venv
  "$(venv_py .venv)" -m pip -q install -U pip wheel
  "$(venv_py .venv)" -m pip -q install torch --index-url https://download.pytorch.org/whl/cpu
  "$(venv_py .venv)" -m pip -q install -r requirements/base.txt
fi
if want base; then "$(venv_py .venv)" -c "import agentsim, tgd; print('base env ok')"; fi

if want train && ! venv_has .venv_train; then
  $PY -m venv .venv_train
  "$(venv_py .venv_train)" -m pip -q install -U pip wheel
  "$(venv_py .venv_train)" -m pip -q install "torch==2.6.*" --index-url "$TORCH_INDEX" || "$(venv_py .venv_train)" -m pip -q install torch
  "$(venv_py .venv_train)" -m pip -q install -r requirements/train.txt
fi
if want train; then "$(venv_py .venv_train)" - <<'PYEOF'
import torch, transformers, trl, peft
print(f"train env ok | torch {torch.__version__} | cuda {torch.cuda.is_available()} | "
      f"transformers {transformers.__version__} | trl {trl.__version__} | peft {peft.__version__}")
PYEOF
fi

if want serve && ! venv_has .venv_vllm; then
  $PY -m venv .venv_vllm
  "$(venv_py .venv_vllm)" -m pip -q install -U pip wheel
  "$(venv_py .venv_vllm)" -m pip -q install -r requirements/serve.txt || echo "vLLM install failed: use --student hf for evaluation"
fi
if want serve; then "$(venv_py .venv_vllm)" -c "import vllm; print('serve env ok | vllm', vllm.__version__)" || true; fi

echo
echo "environments ready. Next: 'make data' to build the SFT train/dev files, then 'make smoke'."
exit 0
