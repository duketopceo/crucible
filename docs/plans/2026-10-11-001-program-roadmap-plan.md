---
title: Crucible program roadmap
type: program
date: 2026-10-11
status: active
---

# Crucible program roadmap (2026-10-11)

Written directly following the ce-plan program format (Now/Next/Later, U-IDs, status, evidence, dependencies, verification); the ce-plan skill was not run because this is a docs-stage repo. Milestone detail stays in `ROADMAP.md` and `docs/work-orders.md`.

State: M0 done, M1 in progress. `src/crucible/*` is empty packages; `tests/unit/test_sanity.py` is the only test. All local checks pass (see PR).

## Now

### U1. Close M1: fill the parameter register
- Status: in progress. Evidence: `docs/assumptions-register.md` is 22 lines; `config/factory.yaml` has `parameters: {}`.
- Depends on: none. Verify: every number in `config/factory.yaml` has a tagged register row.
- Difficulty: easy. Mostly writing and tagging.
- Feasibility: no public foundry data; values stay `assumption`/`sensitivity_only`.
- Simpler alternative: register only parameters M2 actually reads; defer M3 distributions.

### U2. Canonical event envelope (WO-003)
- Status: todo. Evidence: provenance fields listed in ROADMAP, no `events/` code.
- Depends on: U1. Verify: Pydantic model + contract test round-trips every required field.
- Difficulty: easy. One schema, no I/O.
- Feasibility: none external.
- Simpler alternative: JSONL file log first; skip the broker (M4).

### U3. Deterministic six-station route (WO-001/002/005/006, M2)
- Status: todo. Evidence: stubs in `scripts/run_simulation.py`, `scripts/validate_run.py`.
- Depends on: U1, U2. Verify: fixed-seed run is byte-identical on replay; no illegal transitions.
- Difficulty: medium. SimPy resources and genealogy are simple; replay determinism needs discipline.
- Feasibility: SimPy is the only new dependency (already an extra).
- Simpler alternative: plain SimPy processes, not ManPy; genealogy as a dict of parent ids, no graph library.

## Next

### U4. Stochastic behaviour (M3, WO-007/008)
- Status: todo. Difficulty: medium. Seed variation, downtime, defects, uncertainty intervals.
- Feasibility: parameters are assumptions; report sensitivity, not truth.
- Simpler alternative: three distributions and one defect model before the full profile set.
- Depends on: U3. Verify: multi-seed runs vary, invariants hold.

### U5. CI for the real suite
- Status: todo. Evidence: CI runs only `tests/unit`; `make test` and `replay-check` are not in CI.
- Difficulty: easy. Feasibility: public repo, hosted runners fine.
- Simpler alternative: add `replay-check` to the existing job rather than a new workflow.
- Depends on: U3. Verify: CI red on a deliberately broken replay.

### U6. MQTT publish + ingest (M4)
- Status: todo. Difficulty: hard. Broker, topic contract, ingest worker, Postgres raw/modeled stores.
- Feasibility: needs Docker services; the README Quick start is not runnable until then.
- Simpler alternative: write SQLite/Parquet first and publish MQTT as an optional sink; skip OPC UA until a consumer exists.
- Depends on: U3. Verify: event travels adapter to store with provenance intact.

## Later

### U7. Incident walkthrough dashboard (M6)
- Difficulty: hard. Marts, read-only API, UI per `DESIGN.md`. Feasibility: depends on U4 and U6 data volume.
- Simpler alternative: a static HTML report generated from one run before any API or server.
- Depends on: U4, U6. Verify: reviewer follows degradation to disposition.

### U8. External seed data, LLM layer, industrial comparison (M5/M7/M8)
- Difficulty: medium. Feasibility: C-MAPSS/UCI licences and availability; OpenRouter spend must go through the `orch` wrapper.
- Simpler alternative: cut M7 until a concrete narrative need exists; fold M8 into one doc.
- Depends on: U3. Verify: per milestone acceptance in ROADMAP.

## Simplification candidates (no code changed here)
- `INDEX.md`, `REPO_INDEX.md`, `index/AGENT_NAVIGATION.md`, `index/FILE_INDEX.yaml`, `docs/agent-navigation-and-indexing.md` and `scripts/luke-index-watcher.py` (310 lines) form an indexing layer bigger than the codebase. Consolidating to one index plus `build_indexes.py` would remove the most maintenance.
- `docs/milestones.md` duplicates the ROADMAP milestones table.
