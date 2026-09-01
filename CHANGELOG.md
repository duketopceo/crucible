# Changelog

All notable changes. Format: Keep a Changelog; semver for the `crucible` package.

## [Unreleased]

### Changed — M1: research foundation + naming cleanup

- Renamed package `archify` → `crucible` (platform name); Archify Foundry Twin is now the reference model.
- Added `ROADMAP.md`: canonical build plan with M0–M8 milestones and work-order map.
- Reconciled milestones: M1 (research/spec) added; M3 (stochastic) moved onto the critical path.
- Fleshed out `docs/work-orders.md` with acceptance criteria for every work order.
- Expanded `docs/factory-process.md` from stub to six-station spec.
- Removed redundant `docs/architecture.md` (folded into `docs/technical-research-foundation.md`).
- Fixed `index/FILE_INDEX.yaml` coverage; excluded `__init__.py` and `uv.lock` from the index gate.
- Standardized env vars (`CRUCIBLE_*`) and event envelope (`simulation_run_id` prefix `sim-`).
- Added Kaggle casting license finding (CC BY-NC-ND) to `docs/seed-data-research.md`.
- Added `LEARNING.md`: general teaching scope for the project domain.

## [0.1.0] — 2026-08-30

### Added — M0: repository control plane (WO-000)

- AGENTS.md: agent operating rules, verification gates, provenance policy.
- README.md: honest-claims policy (verification yes, real-world validation not claimed).
- REPO_INDEX.md: directory map with change risk, key invariants, validation commands.
- index/FILE_INDEX.yaml: per-file index with deps and break-risk.
- index/AGENT_NAVIGATION.md: task-type → path routing.
- pyproject.toml: package skeleton (pydantic, pyyaml; simpy/transport/api/dev extras).
- Makefile: check / test / indexes / simulate / replay-check targets.
- docs/: architecture, factory-process, data-provenance, assumptions-register, work-orders, milestones.
- config/factory.yaml: versioned generic reference-line factory model (M2 stations).
- CI: GitHub Actions skeleton (lint + type + unit + index freshness).
- .env.example, .gitignore, LICENSE (MIT).
