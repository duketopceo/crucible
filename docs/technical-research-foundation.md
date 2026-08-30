# Crucible: Technical Research Foundation

## Scope and claim boundary

Crucible is a research-grounded synthetic industrial-data platform. Its first reference model, **Archify Foundry Twin**, models a generic high-temperature investment-casting line for blades, vanes, and test coupons.

It is **not** a representation of SpaceX’s proprietary factory, processes, equipment configuration, material specifications, quality limits, suppliers, or production data. It must not claim prediction accuracy for a real foundry.

The defensible claim is:

> A verified synthetic manufacturing simulation with documented public references, declared assumptions, deterministic replay, and uncertainty-aware analytics.

## Architecture decision

The authoritative source of truth is a deterministic, stochastic discrete-event simulation:

```text
Research ledger + assumptions register
                 |
                 v
Versioned factory model / parameter profiles
                 |
                 v
Python simulation core
  routing · queues · resources · genealogy · failures · quality
                 |
       +---------+----------+
       |                    |
       v                    v
OPC UA equipment       MQTT event transport
simulator/adapter      (optional Sparkplug later)
       |                    |
       +---------+----------+
                 v
Raw append-only event store
                 |
                 v
Modeled operational / genealogy / quality tables
                 |
                 v
Analytics marts + read-only portfolio API + dashboard
                 |
                 v
Optional OpenRouter gateway for bounded scenarios and narratives
```

The simulation core owns canonical facts: timestamps, machine state, route state, capacity, lot and serial genealogy, sensor values, latent defect state, inspection observations, holds, and disposition. It must run offline with a fixed random seed.

OpenRouter models are optional and untrusted. They may propose bounded scenario JSON or create synthetic operator handoffs, maintenance notes, and quality summaries. They never create authoritative telemetry, acceptance limits, genealogy, or dispositions.

## Factory reference line

The documented generic route is:

```text
Receiving/quarantine
-> ceramic core
-> wax pattern
-> cluster assembly
-> shell build/dry
-> dewax/preheat
-> VIM melt/pour
-> controlled solidification
-> knockout/gate removal
-> heat treatment/HIP
-> machining
-> NDT
-> final disposition
-> shipment
```

MVP scope begins at shell preparation and ends at final disposition. Upstream materials and downstream shipping exist as genealogy/status records until the core flow is verified.

### Data boundaries by machine class

| Machine/system class | Important data | Real integration path | MVP substitute |
|---|---|---|---|
| Wax injector | Cycle, recipe, temperature, pressure, tooling ID, alarms | PLC/OPC UA | OPC UA simulator |
| Shell line | Slurry condition, layer, dip/dry times, humidity, shell ID | PLC/SCADA/manual QC | Process-run simulator |
| Preheat furnace | Zone temperature, setpoint, cycle/load, alarms | OPC UA/historian | Furnace state model |
| VIM furnace | Vacuum, temperature, power, gas, heat ID, cycle state | OPC UA/historian | OPC UA + MQTT |
| Solidification furnace | Temperature, withdrawal/cooling profile, mold ID | OPC UA/historian | Telemetry curve generator |
| HIP / heat-treat furnace | Temperature, pressure, load, recipe, soak, qualification evidence | OPC UA/historian/record export | Batch-process model |
| CNC cell | State, job, program, tool, spindle/axis data, alarms | MTConnect, OPC UA, CNC API | MTConnect-like read adapter |
| CMM | Feature, nominal/actual, tolerance, program, serial | CMM/QMS export/API | CSV/API quality adapter |
| X-ray/CT/FPI | Scan/report, indication, serial, reviewer, disposition | Vendor API, file drop, QMS | Structured inspection event |
| MES/QMS/CMMS | Orders, route, genealogy, holds, NCR, maintenance | REST/database/message bus | Domain services |

## Protocol choices

- **OPC UA** is the primary model for equipment integration. The OPC UA Machine Tools companion specification offers a technology-neutral model for monitoring and job data across equipment and higher-level MES, SCADA, ERP, and analytics systems.
- **MTConnect** is the preferred read-only machine-tool data path for CNC-style assets. Preserve device metadata, data-item IDs, sequence IDs, sample timestamps, units, conditions, and events.
- **MQTT** is the initial broker transport. Keep the canonical event envelope broker-independent. Consider Sparkplug only after topics and semantic contracts are stable.
- **ISA-95 concepts** guide the boundary between control/equipment, manufacturing operations, and business systems. Crucible does not claim standard conformance.

## Storage layers

| Layer | Purpose | Primary write behavior |
|---|---|---|
| Raw | Original event payloads, external downloads, adapter metadata | Append-only |
| Operational | Assets, work orders, lots, serials, process runs, inspections, holds | Validated domain writes |
| Telemetry | Long-form time series and quality/status codes | Append-only, deduplicated |
| Analytics | Yield, WIP, downtime, quality, genealogy, containment marts | Rebuildable derived data |
| Evidence | Reports, images, generated notes, prompt/output records | Immutable artifacts |
| Catalog | Sources, assumptions, parameter profiles, schema/model versions | Versioned metadata |

MVP storage: PostgreSQL first, with TimescaleDB only if telemetry query volume warrants it. The logical layers remain separate regardless of physical database choice.

## Canonical event envelope

```json
{
  "event_id": "evt_01J...",
  "event_type": "process.telemetry.recorded",
  "schema_version": "1.0",
  "occurred_at": "2026-08-30T19:12:04.218Z",
  "ingested_at": "2026-08-30T19:12:04.431Z",
  "source_system": "furnace-plc-01",
  "site_id": "archify-reference-01",
  "area_id": "casting",
  "workstation_id": "vim-01",
  "work_order_id": "WO-26-00421",
  "part_serial": "BLADE-26-00421-07",
  "melt_lot_id": "HEAT-26-081",
  "payload": {
    "tag": "vacuum_pressure",
    "value": 0.028,
    "unit": "mbar",
    "quality": "good"
  },
  "provenance": {
    "synthetic": true,
    "simulation_run_id": "sim-20260830-001",
    "generator": "crucible-sim-v0.1.0",
    "random_seed": 42,
    "parameter_profile": "baseline-v1"
  }
}
```

Raw events are immutable. Modeled state is rebuildable from raw events plus versioned reference/configuration data. Analytics marts are disposable/rebuildable.

## Seed-data policy

| Source | Approved use | Explicit limitation |
|---|---|---|
| NASA C-MAPSS | Reference patterns for asset degradation, sensor drift/noise, run-to-failure workflows | Turbofan simulation; not foundry equipment or failure rates |
| UCI Steel Plates Faults | Generic quality-classification, evaluation, and explainability workflow | Steel-plate faults; not blade-defect labels or probabilities |
| Kaggle casting imagery | Optional image-ingestion and synthetic inspection-review workflow | Verify license; cast-part imagery is not aerospace blade NDT |

External data belongs in an isolated reference-data domain. It does not silently become simulation fact. Every download records URL, retrieval date, license/terms, checksum, source schema, transformation version, permitted use, and known limitations.

Parameter statuses:

- `source_backed`: direct public support
- `derived`: documented transformation from a public source
- `assumption`: intentionally selected project parameter
- `sensitivity_only`: varied to test response
- `unvalidated`: not calibrated against a physical factory

## Simulation and quality logic

Use hard constraints for routing, capacity, material availability, quarantine, legal state transitions, holds, and shipment release. Use stochastic distributions for cycle duration, queues, repair duration, sensor noise, batch effects, degradation, latent defects, and inspection uncertainty.

An incident must propagate causally:

```text
asset degradation
-> process excursion
-> deviation/alarm
-> elevated latent defect risk
-> quality hold / enhanced inspection
-> accept, rework, scrap, or conditional release
-> yield, WIP, throughput, and delivery impact
```

Do not make every excursion automatic scrap. A quality hold and review path is the default model behavior. Automatic scrap requires an explicitly documented synthetic rule.

## QA, QC, and verification

Required invariants:

- Every serial is unique.
- Released parts have complete required genealogy.
- No station starts before route prerequisites complete.
- No asset produces during planned or unplanned downtime.
- Capacity is never exceeded.
- Quarantined material is never consumed without release.
- Scrapped parts never ship.
- Source event order and sequence rules hold per source stream.
- Every event includes source/provenance fields.
- Raw events remain immutable.
- Same seed + configuration produces the same canonical event stream.

Golden scenarios:

- Baseline route
- Furnace downtime
- Vacuum excursion
- Bad ceramic-core lot
- NDT false negative
- Duplicate delivery / reconnection
- Malformed LLM response
- Schema version migration
- Deterministic replay

The project can verify implementation and perform sensitivity analysis. It cannot claim validation against a real factory without real production measurements and subject-matter review.

## Machine adapter contract

Every physical/simulated adapter must normalize into the canonical event envelope and preserve source fidelity.

### OPC UA adapter

1. Connect with explicit endpoint, credentials, and security policy.
2. Discover/configure namespace and persist node metadata.
3. Subscribe to critical telemetry, state, alarms, recipe/job, and quality nodes.
4. Preserve node ID, browse path, data type, unit, status code, source timestamp, and ingest timestamp.
5. Reconnect with bounded backoff and emit connection-state events.
6. Send unmapped/malformed messages to a dead-letter path.

### MTConnect adapter

1. Read `/probe` and persist the device model.
2. Read `/current` for initial state.
3. Read `/sample` incrementally using sequence state.
4. Preserve data-item ID, sequence, timestamp, unit, condition/event/sample category, and raw observation.
5. Detect unknown data items, duplicates, gaps, unit conflicts, and source resets.
6. Emit canonical normalized events only after raw persistence.

### File/API quality adapter

1. Detect a new CMM, X-ray/CT, FPI, or QMS result.
2. Persist the unmodified report/image/document reference first.
3. Validate serial, inspection method, timestamp, program/recipe, reviewer, and disposition fields.
4. Emit a typed inspection event.
5. Route nonconforming or incomplete records to review, not automatic acceptance.

## Agent rules

All coding agents must:

1. Read `REPO_INDEX.md` before editing.
2. Read the target file’s `FILE_INDEX.yaml` entry and listed high-risk dependencies.
3. Make the smallest change required by the work order.
4. Never invent sources, limits, machine capabilities, event schemas, or data provenance.
5. Run focused tests, then required broader tests.
6. Update index, changelog, assumptions register, and provenance information whenever behavior changes.
7. Preserve compatibility or increment schema/model version deliberately.
8. Never commit datasets unless redistribution is permitted.
9. Never commit credentials, tokens, API keys, or real customer/manufacturing data.
10. Clearly label synthetic and generated data.

## Recommended initial container stack

```text
core profile:
  PostgreSQL
  Mosquitto
  factory simulator
  OPC UA simulator
  ingestion worker
  read-only API

bi profile:
  Grafana

llm profile:
  OpenRouter gateway

later industrial profile:
  Redpanda/UMH comparison deployment
  Sparkplug bridge, only if justified
```

The core simulator must work without Docker and without any LLM key. Compose services require health checks and should start only after critical dependencies are healthy.

## Documentation map

- `ROADMAP.md` — the build plan: milestones, work orders, build order, portfolio presentation.
- `docs/technical-research-foundation.md` — this technical baseline (research, architecture, envelope, protocols).
- `docs/factory-process.md` — the generic reference line and six-station MVP spec.
- `docs/machine-integration-map.md` — machine, data, protocol, and adapter matrix.
- `docs/qa-qc-plan.md` — test strategy, invariants, acceptance evidence, and known limits.
- `docs/agent-navigation-and-indexing.md` — file-index contract and agent workflow.
- `docs/seed-data-research.md` — permitted seed-data uses, acquisition controls, and gaps.

Each implementation issue references its owning document section and includes acceptance criteria, test evidence, affected contracts, data-provenance impact, and required index changes.
