# Repository Index

Start here. Read top-to-bottom before editing anything.

## Reading order for agents

1. `AGENTS.md` — operating rules.
2. `index/FILE_INDEX.yaml` — find your target file's entry, dependencies, break risk.
3. `index/AGENT_NAVIGATION.md` — task-type → path routing.
4. This file for the map below.

## Directory map

| Path | Purpose | Change risk |
|---|---|---|
| `AGENTS.md` | Agent operating rules | low |
| `README.md` | Project overview, honest claims policy | low |
| `ROADMAP.md` | Build plan: milestones, work orders, portfolio presentation | low |
| `index/` | Generated file index, schema index, event index, agent navigation | medium (generated) |
| `docs/` | Architecture, process, provenance, assumptions, work orders, ADRs | low |
| `config/` | Versioned factory model, recipes, defect model, reliability profiles | **high** — parameters drive simulation output |
| `src/crucible/domain/` | Core entities: lots, serials, work orders, assets, holds | **high** |
| `src/crucible/simulation/` | SimPy engine: routing, queues, resources, genealogy | **high** |
| `src/crucible/quality/` | Defect risk, inspection, disposition logic | **high** |
| `src/crucible/reliability/` | Equipment health, degradation, failure sampling | **high** |
| `src/crucible/genealogy/` | Lot/serial lineage graph and containment | **high** |
| `src/crucible/events/` | Canonical envelope, event types, append-only log | **high** |
| `src/crucible/provenance/` | Provenance fields, run manifest, source registry | **high** |
| `src/crucible/adapters/` | MQTT/OPC UA adapters (M4+) | medium |
| `services/` | Deployable services: simulator runner, ingest, API | medium |
| `schemas/` | JSON event schemas, SQL DDL | **high** |
| `migrations/` | Append-only DB migrations | **high** — never edit applied migrations |
| `dashboards/` | Embedded BI views (M6+) | low |
| `tests/` | unit / invariants / contract / integration / scenario | low (additive) |
| `scripts/` | fetch_external_data, run_simulation, validate_run, build_indexes | medium |
| `data/` | external/ (downloaded, not committed), raw/ (run outputs), README | low |

## Key invariants (enforced by tests, M2+)

- Unique part serials; complete genealogy for every released part.
- No process starts before prerequisites; no production while equipment unavailable.
- Quarantined material cannot be consumed; scrapped parts cannot ship.
- Per-stream event timestamps nondecreasing; raw events immutable.
- Same seed + config → identical canonical event stream.

## Validation commands

```bash
make check          # lint + unit + index freshness
make test           # full test suite
make simulate       # offline fixed-seed run (M2+)
make replay-check   # determinism check (M2+)
make indexes        # regenerate index/FILE_INDEX.yaml
```

## Source-of-truth hierarchy (enforced in code)

| Category | Authority |
|---|---|
| Public reference (NASA C-MAPSS, UCI Steel Plates) | external evidence only, never factory truth |
| Research claim | design constraint with citation |
| Simulation fact | authoritative inside a run only |
| Generated context (LLM narratives) | advisory only, never mutates facts |

## Milestones

- **M0 — repo control plane** (done)
- **M1 — research and factory specification** (in progress)
- **M2 — deterministic route + genealogy + invariants**
- **M3 — stochastic process behavior** (critical path)
- **M4 — MQTT transport + Postgres ingest + provenance**
- **M6 — embedded dashboard + incident walkthrough**
- Deferred: external seed data (M5), OpenRouter layer (M7), industrial comparison (M8)
