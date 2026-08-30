# Changelog

All notable changes. Format: Keep a Changelog; semver for the `archify` package.

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
