# Convenience targets; every one maps to a documented command.
# The CPU virtualenv, wherever this platform puts its interpreter (POSIX bin/, Windows
# Scripts/), falling back to whatever python3 is on PATH.
PY ?= $(shell for c in .venv/bin/python .venv/Scripts/python.exe; do [ -x "$$c" ] && echo "$$c" && exit 0; done; echo python3)

.DEFAULT_GOAL := help
.PHONY: help env test smoke data leakage clean-runs
help:           ## show this help
	@grep -hE '^[a-z-]+:.*##' $(MAKEFILE_LIST) | sed 's/:.*##/\t/' | expand -t16
env:            ## build the three virtual environments
	bash setup_env.sh
test:           ## unit tests (CPU, seconds after the first cold import)
	$(PY) -m pytest tests -q
smoke:          ## whole pipeline with mock models, no GPU / API (~1-3 min)
	bash tests/smoke_offline.sh
data:           ## rebuild data/splits from data/episodes + data/questions, then audit
	$(PY) scripts/build_splits.py && $(PY) scripts/check_leakage.py
leakage:        ## audit the existing splits
	$(PY) scripts/check_leakage.py
clean-runs:     ## remove smoke-test artifacts
	rm -rf runs/smoke_offline runs/smoke_gpu
