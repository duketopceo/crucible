# Agent Navigation

Task-type → path routing. Read `AGENTS.md` and `REPO_INDEX.md` first, always.

| Task | Start at | Then |
|---|---|---|
| Understand the factory process | `docs/factory-process.md` | `config/factory.yaml` |
| Add/modify an event type | `schemas/json/` | `src/archify/events/`, update `index/EVENT_INDEX.yaml` |
| Change simulation behavior | `src/archify/simulation/` | `make replay-check` after every change |
| Add a parameter/threshold | `docs/assumptions-register.md` | `config/` — tag as source_backed / derived / assumption / sensitivity_only / unvalidated |
| Add a test | `tests/` matching layer | additive only; never weaken an invariant |
| Touch the database | `migrations/` | new file only — never edit an applied migration |
| Add a dependency | `pyproject.toml` | justify in work order; prefer stdlib + pydantic |
| Generate narrative/context | out of scope until M7 | never from the simulation engine |

## Non-negotiables per task type

- **Simulation changes:** fixed seed recorded; replay determinism verified; invariants green.
- **Event/schema changes:** schema_version bump if breaking; provenance fields intact; contract tests updated.
- **Config changes:** every new numeric parameter enters the assumptions register with a tag.
