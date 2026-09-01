# Agent Navigation and Indexing Contract

## Purpose

Crucible is intended to be maintainable by humans and coding agents. An agent must be able to start at the repository index, locate the exact relevant file, understand why it exists, determine what depends on it, identify the risk of change, and run the verification that proves the modification is safe.

Documentation must improve navigation, not become duplicate prose that immediately goes stale.

## Required navigation path

Before editing any file, an agent must:

1. Read `REPO_INDEX.md`.
2. Identify the responsible domain and the target file.
3. Find the target’s entry in `index/FILE_INDEX.yaml`.
4. Read its `depends_on`, `consumed_by`, `breaks_if_changed`, and `verification` fields.
5. Read linked schemas, configuration, and high-risk neighboring files.
6. Read the active work order and its acceptance criteria.
7. Make the smallest change needed.
8. Run focused verification before broader validation.
9. Update index metadata, changelog, assumptions, and provenance if behavior changed.

## FILE_INDEX contract

`index/FILE_INDEX.yaml` is the machine-readable catalog for every tracked source, configuration, schema, migration, script, workflow, and meaningful documentation file. Generated/dependency directories are excluded by policy.

Minimum entry:

```yaml
- path: src/crucible/simulation/engine.py
  purpose: Executes the discrete-event factory model and emits canonical facts.
  version: v0.1.0
  last_reviewed: 2026-08-30T00:00:00Z
  owner_domain: simulation
  inputs:
    - config/factory.yaml
    - config/recipes.yaml
  outputs:
    - canonical simulation events
    - run manifest
  depends_on:
    - src/crucible/domain/models.py
    - simpy
  consumed_by:
    - services/simulator
    - tests/invariants/test_genealogy.py
  change_risk: high
  breaks_if_changed:
    - event ordering
    - lot and serial genealogy
    - fixed-seed replay
  verification:
    - pytest tests/unit/test_engine.py
    - pytest tests/invariants/test_genealogy.py
  status: planned
```

### Required fields

| Field | Meaning |
|---|---|
| `path` | Repository-relative path; unique key |
| `purpose` | Why the file exists, not merely what language it uses |
| `version` | File or contract version; update deliberately when behavior changes |
| `last_reviewed` | ISO 8601 UTC timestamp |
| `owner_domain` | Domain responsible for the file, such as simulation, events, quality, adapters, or docs |
| `inputs` | Configurations, schemas, data, or interfaces it reads |
| `outputs` | Artifacts, events, tables, files, or interfaces it writes/exposes |
| `depends_on` | Code, schemas, packages, or contracts required by the file |
| `consumed_by` | Known readers/callers/dependent artifacts |
| `change_risk` | `low`, `medium`, `high`, or `critical` |
| `breaks_if_changed` | Concrete affected behavior and contracts |
| `verification` | Exact tests, commands, or review evidence |
| `status` | `planned`, `active`, `deprecated`, or `generated` |

### Risk classification

| Risk | Examples | Required action |
|---|---|---|
| Low | Narrative documentation, isolated display copy | Focused lint/link check |
| Medium | Local helper, non-authoritative dashboard component | Unit test plus affected integration check |
| High | Domain rule, adapter mapping, configuration, metric definition | Contract/invariant tests, updated docs, peer review |
| Critical | Event schema, database migration, genealogy, disposition rule, raw-event retention | Versioning/migration plan, replay tests, full relevant suite, explicit review |

## Index maintenance

- A script, `scripts/build_indexes.py`, will check tracked files against `FILE_INDEX.yaml`.
- CI will fail when a tracked, indexable file has no entry or when an entry points to a missing file.
- CI will warn or fail when a high-risk file’s `last_reviewed` timestamp is stale under a configured policy.
- Generated files are not hand-indexed unless they are reviewed deliverables.
- Directory-level `README.md` files are used only where the local subsystem needs an explanation beyond index metadata.

## Contract registries

Use dedicated registries for high-impact contracts:

- `index/SCHEMA_INDEX.yaml` — JSON, SQL, event, and API schemas
- `index/EVENT_INDEX.yaml` — event types, producer/consumer ownership, version, payload schema
- `docs/assumptions-register.md` — uncertain or synthetic parameter decisions
- `docs/data-provenance.md` — external datasets, transformations, and license/terms records
- `docs/technical-research-foundation.md` and `docs/adr/` — architectural decisions and rationale

An event, schema, or metric change is incomplete unless the relevant registry changes in the same PR.

## Agent behavioral rules

Agents must not:

- Invent an event field, machine capability, source citation, numerical process limit, or data provenance.
- Treat LLM output as authoritative manufacturing data.
- Modify raw event history to make downstream tests pass.
- Combine external reference records with simulation facts without a transformation/provenance label.
- Add a dependency or container only to appear more production-like.
- Commit credentials, access tokens, private endpoints, certificates, or downloaded datasets without confirmed redistribution rights.
- Refactor unrelated areas while completing a focused work order.

Agents must:

- State uncertainty and unresolved requirements.
- Keep tests deterministic where expected.
- Add negative/failure tests for high-risk paths.
- Use existing contracts or deliberately version them.
- Record any new parameter in the assumptions register.
- Update the `last_reviewed` timestamp and version for changed indexed files.

## Change template

Every PR or agent handoff should state:

```text
Work order:
Scope:
Files changed:
Contracts changed:
Assumptions added/changed:
Provenance impact:
Known risks:
Tests run:
Expected failures or gaps:
Index updates:
```

## Related files

- `REPO_INDEX.md`
- `AGENTS.md`
- `CHANGELOG.md`
- `docs/technical-research-foundation.md`
- `docs/qa-qc-plan.md`
- Future: `index/FILE_INDEX.yaml`
- Future: `scripts/build_indexes.py`
