# Crucible — Agent Operating Rules

Research-grounded synthetic investment-casting simulation. The simulation owns truth; LLMs propose or explain; validators decide admissibility.

## Navigation (read before any edit)

1. Read `REPO_INDEX.md` first.
2. Read the target file's entry in `index/FILE_INDEX.yaml` — its `depends_on`, `consumed_by`, `breaks_if_changed`, and `verification` fields.
3. Read all files listed in `depends_on` for entries marked `change_risk: high`.
4. Modify the smallest possible surface area.

## Hard rules

- Never invent a schema, event type, threshold, parameter value, or public source. If unlisted, it goes in the assumptions register first.
- Label all synthetic data (`synthetic: true`) and generated documents (`generated: true`). Provenance fields are mandatory on every event.
- Raw events are append-only and immutable. Modeled tables must be rebuildable from raw events + versioned reference data.
- Preserve backward compatibility or bump `schema_version` and document the migration.
- Never commit secrets, OpenRouter keys, or external datasets (use `scripts/fetch_external_data.py` + checksums instead).
- No claiming any output represents SpaceX or a real foundry. This is a generic reference line.
- No unrelated refactors. Match existing style. Conventional commits.

## Workflow

- Work from work orders (`docs/work-orders.md`) with acceptance criteria. Reference the WO id in commit titles, e.g. `WO-003: implement canonical event envelope`.
- Run focused tests before broad tests: `make test-unit`, then `make test`.
- Every simulation run must have a fixed random seed recorded in the run manifest. Same seed + config = identical event stream (replay invariant).
- When behavior changes, update in the same commit: file index entry, `CHANGELOG.md`, assumptions register (if a parameter changed), and `last_reviewed` timestamp.
- Report uncertainty and failed checks explicitly. Do not declare victory on compile-only signals.

## Verification gates

- `make check` must pass before any commit.
- `make replay-check` must pass after any simulation-engine change (M2+).
- Invariant tests in `tests/invariants/` are non-negotiable; a failing invariant blocks merge.
