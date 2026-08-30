.PHONY: check test test-unit lint type indexes simulate replay-check clean

PY := uv run python

check: lint type test-unit indexes-verify

test:
	uv run pytest

test-unit:
	uv run pytest tests/unit -q

lint:
	uv run ruff check src tests scripts
	uv run ruff format --check src tests scripts

type:
	uv run mypy src

indexes:
	$(PY) scripts/build_indexes.py

indexes-verify:
	$(PY) scripts/build_indexes.py --verify

simulate:
	$(PY) scripts/run_simulation.py --profile baseline-v1 --seed 42

replay-check:
	$(PY) scripts/validate_run.py --replay-check

clean:
	rm -rf .pytest_cache .ruff_cache .mypy_cache dist htmlcov
