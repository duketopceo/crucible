# Contributing

Crucible is built to be maintainable by humans and coding agents. Before contributing, read in order:

1. `AGENTS.md` — operating rules and hard constraints.
2. `REPO_INDEX.md` — directory map and change risk.
3. `docs/agent-navigation-and-indexing.md` — file-index contract and change template.

## Workflow

- Work from a work order (`docs/work-orders.md`). Reference the WO id in the commit title, e.g. `WO-003: implement canonical event envelope`.
- Run `make check` before committing. Invariants and replay checks are non-negotiable for simulation changes.
- Update `index/FILE_INDEX.yaml`, `CHANGELOG.md`, and the assumptions register in the same commit when behavior changes.

## Non-negotiables

- Never invent a schema, event type, threshold, parameter value, or public source.
- Never commit secrets, API keys, or external datasets without confirmed redistribution rights.
- Never claim output represents SpaceX or a real foundry.
- Label all synthetic data (`synthetic: true`) and generated documents (`generated: true`).

## Honest claims

This project verifies its simulation but does not claim real-world validation. Keep that boundary in every change.
