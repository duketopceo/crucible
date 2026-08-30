# Crucible — Roadmap and Build Plan

> Crucible is a research-grounded synthetic industrial-data platform. Its first reference model, **Archify Foundry Twin**, simulates a generic high-temperature investment-casting line and demonstrates quality and reliability decisions without claiming access to real factory data.

This file is the build plan: what gets built, in what order, and what "done" means at each step. Deep design rationale and citations live in `docs/technical-research-foundation.md`; this file only summarizes and points to them.

## Naming

Two names, one meaning each:

| Term | Meaning |
|---|---|
| **Crucible** | The platform and Python package (`crucible`). The forge where synthetic industrial data is produced and tested. |
| **Archify Foundry Twin** | The first reference model built on Crucible — a generic investment-casting line. Its `site_id` is `archify-reference-01`. |

Do not use the two interchangeably. Code and packages are `crucible`; the modeled factory is the Archify reference line.

## Executive decision

Archify Foundry Twin is a **verified synthetic simulation**, not a claim about a real factory and not an LLM fake-data demo. A deterministic, stochastic discrete-event simulation owns all process truth: material genealogy, routing, station capacity, equipment state, telemetry, quality outcomes, and disposition. Optional small LLM models (deferred, M7) only propose constrained scenarios and write human-readable artifacts — operator handoffs, maintenance notes, quality summaries. They never produce authoritative process facts.

The honest claim is **verified synthetic simulation with documented assumptions**, not validated prediction of real turbine-blade production. SpaceX is motivating context only; the modeled line is a generic reference and never claims to represent SpaceX or any real foundry.

## What it demonstrates

A reviewer should be able to answer, with every number traceable to an event:

- Where is work-in-process, and how long has it waited?
- Which station is constraining throughput?
- Which process excursion caused a quality hold?
- Which parts, lots, and batches are affected by a deviation?
- What happens to yield, rework, scrap, and delivery as equipment health declines?
- Can every dashboard figure be traced to a source event, model version, run, seed, and assumption?

## Architecture

```text
Research ledger + assumptions register
              |
              v
Versioned factory model + parameter profiles   (config/)
              |
              v
Python discrete-event simulator (SimPy)        (src/crucible/simulation/)
  routing · queues · resources · genealogy · failures · quality
              |
      +-------+--------+
      |                |
      v                v
OPC UA simulator   MQTT event transport        (src/crucible/adapters/, M4)
      |                |
      +-------+--------+
              v
Raw append-only event store                    (Postgres, M4)
              |
              v
Modeled operational / genealogy / quality tables
              |
              v
Analytics marts + read-only API + dashboard     (M6)
              |
              v
Optional OpenRouter gateway                     (M7, deferred)
```

Three defining rules (see `docs/technical-research-foundation.md`):

1. **Simulation code owns truth.** LLMs propose or explain; validators decide admissibility.
2. **Every number is traceable** to an event, model version, seed, parameter profile, and evidence status.
3. **Raw events are immutable; modeled tables are rebuildable** from raw events + versioned reference data.

## Factory model

The full reference line has fourteen areas. The MVP simulates **six core workstations**; upstream (receiving, core, pattern, cluster assembly) and downstream (packing, shipment) are recorded as genealogy records, not simulated queues, until the core flow is verified.

| # | Workstation | Area | Key outputs |
|---|---|---|---|
| 1 | Shell building | Shell | Shell batches, mold readiness |
| 2 | Preheat | Thermal | Preheat cycle records, shell release |
| 3 | Vacuum melt/pour | Melt | Melt heats, chemistry, cast part serials |
| 4 | Controlled solidification | Melt | Solidified serials, process curves, alarms |
| 5 | Heat treatment | Thermal treatment | Batch cycles, recipe records |
| 6 | Machining + NDT/final disposition | Finishing | Dimensions, inspection results, accept/rework/hold/scrap |

The full fourteen-area reference line (receiving → core → pattern → cluster assembly → shell → dewax/preheat → melt/pour → solidification → knockout → heat treatment/HIP → machining → NDT → final disposition → shipment) is documented in `docs/factory-process.md` and `config/factory.yaml`.

## Source-of-truth hierarchy

| Category | Examples | Authority |
|---|---|---|
| Public reference | NASA C-MAPSS, UCI Steel Plates Faults | External evidence, never factory truth |
| Research claim | Generic process stage, protocol, terminology | Design constraint with citation |
| Simulation fact | Serial, lot, timestamp, route state, sensor value, quality result | Authoritative inside a run only |
| Generated context | Shift note, maintenance narrative, quality summary | Advisory only |

Every record carries `synthetic`, `source_type`, `source_id`, `source_version`, `simulation_run_id`, `model_version`, `parameter_profile`, `random_seed`, `occurred_at`, `ingested_at`.

## Milestones

Critical path: **M0 → M1 → M2 → M3 → M4 → M6**. Deferrable: **M5, M7, M8**.

| Milestone | Scope | Acceptance | Status |
|---|---|---|---|
| **M0 — repository control plane** | Structure, AGENTS.md, indexes, CI skeleton, config scaffold | An agent starts at `REPO_INDEX.md`, locates any file, sees deps/break risk, runs `make check` | **done** |
| **M1 — research and factory specification** | Research ledger, process map, entity glossary, parameter register, assumptions register, external-data manifest, ADRs | Every modeled station has purpose, inputs, outputs, resources, state transitions, evidence, assumptions, open questions | **in progress** |
| **M2 — deterministic route** | Domain models, six stations, routing, genealogy, append-only events, invariant tests | Fixed-seed run completes; no illegal state transitions; complete part genealogy | todo |
| **M3 — stochastic process behavior** | Distributions, downtime, sensor noise, batch effects, defect risk, inspection outcomes, disposition | Multiple seeds vary while preserving invariants; metrics report uncertainty intervals | todo |
| **M4 — industrial transport** | MQTT publication, ingest worker, OPC UA adapter, raw+modeled stores | An equipment event travels adapter → broker → stores with provenance intact | todo |
| **M5 — external seed data** *(deferred)* | C-MAPSS/UCI fetch scripts, checksums, licenses, isolated schemas | Clean-env fetch or clear unavailability report; no data mixing | deferred |
| **M6 — analytics + dashboard** | Production/WIP/quality/reliability marts; embedded dashboard; incident walkthrough | Reviewer follows one incident: degradation → excursion → affected serials → disposition → impact | todo |
| **M7 — OpenRouter layer** *(deferred)* | Gateway, strict schemas, local validation | Runs with no key; malformed output rejected; no fact mutation | deferred |
| **M8 — industrial comparison** *(deferred)* | UMH/Sparkplug/Redpanda comparison docs | Explains gained capability vs added complexity | deferred |

**Why M3 is on the critical path, not deferred.** A purely deterministic simulation produces identical output every run, which looks fake and contradicts the "realistic synthetic data" claim. Stochasticity — variation across seeds while preserving invariants — is the product, not an enhancement. M3 immediately follows M2; only M5, M7, and M8 are genuinely optional.

## Work orders

Full work orders with acceptance criteria live in `docs/work-orders.md`. Each maps to a milestone and a GitHub issue tagged `work-order`.

| WO | Title | Milestone |
|---|---|---|
| WO-000 | Repository control plane | M0 (done) |
| WO-001 | Domain models: lot, serial, work order, asset, hold, disposition | M2 |
| WO-002 | Station resources + routing (six core workstations) | M2 |
| WO-003 | Canonical event envelope + append-only event log | M2 |
| WO-004 | Genealogy graph + containment queries | M2 |
| WO-005 | Invariant test suite + replay determinism check | M2 |
| WO-006 | Run manifest + `scripts/run_simulation.py` | M2 |
| WO-007 | Stochastic distributions + downtime + noise | M3 |
| WO-008 | Defect risk + inspection + disposition logic | M3 |
| WO-010 | MQTT publication + topic contract | M4 |
| WO-011 | Ingest worker → raw store → modeled tables | M4 |
| WO-012 | OPC UA equipment simulator adapter | M4 |
| WO-020 | BI marts + embedded dashboard + incident walkthrough | M6 |

## Portfolio presentation

`luke-the-duke.com` shows a public case study with four views:

1. **Factory map** — stations, routes, queues, assets, event boundaries.
2. **Operations** — throughput, WIP age, cycle time, bottleneck, downtime, schedule impact.
3. **Quality and containment** — defect Pareto, first-pass yield, holds, rework/scrap, affected-lot blast radius.
4. **Evidence and provenance** — run, seed, model version, assumptions, source claims, validation status.

A reviewer clicks from a quality incident to the affected process run, asset telemetry, material lots, serials, inspection records, and disposition. Traceability beats decorative gauges.

## Final build recommendation

Build in Python first: SimPy, Pydantic, PostgreSQL, Mosquitto, a small read-only API. Keep TypeScript limited to the OPC UA adapter or web presentation if it accelerates the portfolio. Add FactorySimPy or OpenFactoryTwin only as studied references before adopting them as dependencies.

The three defining rules, restated:

- **Technical:** simulation code owns truth; LLMs propose or explain; validators decide admissibility.
- **Portfolio:** every number is traceable to an event, model version, seed, parameter profile, and evidence status.
- **Research:** public sources ground architecture and behaviors; no external dataset is presented as real turbine-foundry data.
