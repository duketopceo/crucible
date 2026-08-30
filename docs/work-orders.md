# Work Orders

Format: id, title, scope, acceptance criteria, status. Commit titles reference the WO id.

## Active

| WO | Title | Milestone | Status |
|---|---|---|---|
| WO-000 | Repository control plane | M0 | done (initial commit) |
| WO-001 | Domain models: lot, serial, work order, asset, hold, disposition | M2 | todo |
| WO-002 | Station resources + routing (six core workstations) | M2 | todo |
| WO-003 | Canonical event envelope + append-only event log | M2 | todo |
| WO-004 | Genealogy graph + containment queries | M2 | todo |
| WO-005 | Invariant test suite + replay determinism check | M2 | todo |
| WO-006 | Run manifest (seed, profile, model version) + `scripts/run_simulation.py` | M2 | todo |
| WO-010 | MQTT publication + topic contract | M4 | todo |
| WO-011 | Ingest worker → raw store → modeled tables | M4 | todo |
| WO-012 | OPC UA equipment simulator adapter | M4 | todo |
| WO-020 | BI marts + embedded dashboard + incident walkthrough | M6 | todo |

## Definition of done (every WO)

- Acceptance criteria met and demonstrated by tests.
- `make check` green; invariants green.
- File index entry added/updated; CHANGELOG entry; assumptions register touched if parameters changed.
- No unrelated refactors; conventional commit with WO id.
