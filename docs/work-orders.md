# Work Orders

Format: id, title, milestone, scope, acceptance criteria, status. Commit titles reference the WO id (e.g. `WO-003: implement canonical event envelope`). Each work order maps to a GitHub issue tagged `work-order`.

## M2 — deterministic route

### WO-001 — Domain models: lot, serial, work order, asset, hold, disposition
**Scope:** Implement core entities in `src/crucible/domain/`: `material_lot`, `part_serial`, `work_order`, `equipment_asset`, `equipment_state`, `quality_hold`, `disposition`. Pydantic models with validation.
**Acceptance:**
- Each entity has required fields and a `schema_version`.
- Serial identifiers are unique and immutable once created.
- Disposition enum is exactly `accept | rework | hold | scrap | conditional_release`.
- Unit tests cover construction, validation failures, and equality.
**Status:** todo

### WO-002 — Station resources + routing (six core workstations)
**Scope:** Implement the six stations from `config/factory.yaml` (shell-building, preheat, vacuum-melt-pour, controlled-solidification, heat-treatment, machining-ndt-disposition) as SimPy resources with capacity and a legal route graph.
**Acceptance:**
- A part follows the legal route; no station starts before prerequisites complete.
- Capacity is never exceeded (invariant-tested).
- Upstream/downstream genealogy records (receiving, core, pattern, cluster, packing, shipment) exist but are not simulated queues.
**Status:** todo

### WO-003 — Canonical event envelope + append-only event log
**Scope:** Implement the canonical event envelope and an append-only event log in `src/crucible/events/`.
**Acceptance:**
- Every event carries `event_id`, `event_type`, `schema_version`, `occurred_at`, `ingested_at`, source fields, `payload`, and `provenance` (including `synthetic`, `simulation_run_id`, `generator`, `random_seed`, `parameter_profile`).
- Raw events are append-only; no update or delete path exists.
- Contract tests validate the envelope against a JSON schema.
**Status:** todo

### WO-004 — Genealogy graph + containment queries
**Scope:** Implement lot/serial lineage in `src/crucible/genealogy/` and containment queries (which parts/lots are affected by a deviation).
**Acceptance:**
- Every released part has complete required genealogy.
- A containment query returns the affected serials/lots for a given excursion or bad lot.
- Invariant: no orphan released parts.
**Status:** todo

### WO-005 — Invariant test suite + replay determinism check
**Scope:** Implement `tests/invariants/` covering all invariants in `docs/qa-qc-plan.md`, plus a replay check.
**Acceptance:**
- All invariants pass on small fixed-seed runs.
- Same seed + config produces the same canonical event stream (replay check green).
- A failing invariant blocks merge (enforced in CI).
**Status:** todo

### WO-006 — Run manifest + `scripts/run_simulation.py`
**Scope:** Implement the run manifest (seed, profile, model version, config hash) and a working `scripts/run_simulation.py` entry point.
**Acceptance:**
- `make simulate` runs an offline fixed-seed simulation and writes a run manifest.
- The manifest records seed, parameter profile, model version, and config hash.
- The run is reproducible from the manifest.
**Status:** todo

## M3 — stochastic process behavior

### WO-007 — Stochastic distributions + downtime + sensor noise
**Scope:** Add cycle-time distributions (triangular/lognormal), machine downtime, repair duration, and sensor noise to the simulation.
**Acceptance:**
- Multiple seeds produce variation while preserving all invariants.
- Metrics report uncertainty intervals (quantiles), not a single asserted value.
- Downtime never allows production during the down window.
**Status:** todo

### WO-008 — Defect risk + inspection + disposition logic
**Scope:** Add causal defect risk, inspection sensitivity/specificity, batch effects, and the disposition workflow (hold → review → accept/rework/scrap/conditional release).
**Acceptance:**
- A vacuum/thermal excursion causally raises defect risk for affected serials.
- An excursion does not automatically scrap; hold + review is the default path.
- Golden scenarios (vacuum excursion, bad core lot, NDT false negative) pass.
**Status:** todo

## M4 — industrial transport

### WO-010 — MQTT publication + topic contract
**Scope:** Publish selected events over MQTT with a versioned topic contract.
**Acceptance:**
- A simulated event publishes to a documented topic with the canonical envelope.
- The simulator runs offline without a broker (publication is optional/graceful).
**Status:** todo

### WO-011 — Ingest worker → raw store → modeled tables
**Scope:** Implement the ingestion worker that persists raw events and rebuilds modeled tables.
**Acceptance:**
- An event travels broker → raw store → modeled tables with provenance intact.
- Modeled tables are rebuildable from raw events + reference data.
- Duplicate delivery is idempotent; raw evidence retained.
**Status:** todo

### WO-012 — OPC UA equipment simulator adapter
**Scope:** Implement the OPC UA simulator (`services/opcua_simulator`) and adapter contract from `docs/machine-integration-map.md`.
**Acceptance:**
- A simulated OPC UA VIM tag reaches raw, normalized, and analytics stores with timestamps intact.
- Unknown nodes are retained raw, not mapped into the domain model.
- Reconnect emits connection-state events; no unmarked gap.
**Status:** todo

## M6 — analytics + dashboard

### WO-020 — BI marts + embedded dashboard + incident walkthrough
**Scope:** Build production/WIP/quality/reliability/genealogy/containment marts and a non-decorative dashboard; wire the incident walkthrough.
**Acceptance:**
- A reviewer follows one incident from degradation → excursion → affected serials → disposition → business impact.
- Every dashboard figure links to its source event, run, seed, model version, and assumption.
- No decorative gauges or fake-looking numbers.
**Status:** todo

## Definition of done (every WO)

- Acceptance criteria met and demonstrated by tests.
- `make check` green; invariants green; replay check green (simulation changes).
- File index entry added/updated; CHANGELOG entry; assumptions register touched if parameters changed.
- No unrelated refactors; conventional commit with WO id.
