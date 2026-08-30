# Crucible — Architecture

M0 stub. Full architecture document lands with M2 (deterministic route).

## Layered model (staged, not all built yet)

```
Versioned factory model + parameter profiles   (config/, M0-M2)
            |
Discrete-event simulator (SimPy)               (src/archify/simulation/, M2)
  routing, queues, resources, genealogy, quality, failures
            |
            +--> MQTT event publication         (src/archify/adapters/, M4)
            |
Append-only raw event store                    (Postgres, M4)
            |
Modeled operational tables (rebuildable)       (migrations/, M4)
            |
BI views + read-only API                       (dashboards/, services/api/, M6)
```

## Defining rules

1. **Simulation code owns truth.** LLMs (deferred, M7) may propose scenarios or write narratives; validators decide admissibility; nothing generated mutates authoritative facts.
2. **Every number traceable.** Each dashboard figure links to event → simulation run → model version → seed → parameter profile → evidence status.
3. **Raw events immutable; modeled tables rebuildable** from raw events + versioned reference data.

## Source-of-truth hierarchy

| Category | Examples | Authority |
|---|---|---|
| Public reference | NASA C-MAPSS, UCI Steel Plates Faults (deferred, M5) | external evidence, not factory truth |
| Research claim | generic process stage behavior, terminology | design constraint with citation |
| Simulation fact | serial, lot, timestamp, sensor value, quality result | authoritative inside a run |
| Generated context | shift note, maintenance narrative | advisory only |

## Provenance fields (mandatory on every event)

`synthetic`, `source_type`, `source_id`, `source_version`, `simulation_run_id`, `model_version`, `parameter_profile`, `random_seed`, `occurred_at`, `ingested_at`.

## ISA-95 alignment (conceptual)

Simulated equipment ≈ Level 1-2; event transport + ingest ≈ historian; modeled records (work orders, genealogy, holds, disposition) ≈ Level 3 MES-like; BI/API ≈ Level 4 consumption. No claim of full standard compliance.
