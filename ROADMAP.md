# Archify Foundry Twin — Final Research and Build Plan

## Executive decision

Archify Foundry Twin should be built as a **research-grounded synthetic manufacturing system**, not as a claim of a real SpaceX factory and not as an LLM-generated fake-data demo. The authoritative layer should be a deterministic, stochastic, discrete-event simulation that owns material genealogy, routing, station capacity, equipment state, telemetry, quality outcomes, and disposition. Small OpenRouter models should be optional assistants that generate constrained scenarios and human-readable artifacts—operator handoffs, maintenance notes, quality summaries—not authoritative process facts.

This distinction is important because a manufacturing digital twin is expected to be fit for purpose and synchronized with an observable manufacturing element; NIST research emphasizes verification, validation, uncertainty quantification, data fidelity, and traceability as prerequisites for trust. Because Archify has no physical factory and no proprietary operating data, the honest claim is **verified synthetic simulation with documented assumptions**, not validated prediction of real turbine-blade production.[1][2][3][4]

The portfolio target, Luke-the-duke.com, should display the result as a readable engineering case study and dashboard. The website should be the presentation layer; the repository must remain reproducible, inspectable, testable, and usable by agents without depending on the website.

## What Archify is

Archify is a simulation and data-platform reference implementation for a generic high-temperature investment-casting line producing blades, vanes, and test coupons. It maps public generic process knowledge into a versioned factory model, generates causally consistent synthetic events, transports selected events through industrial-style interfaces, stores raw and modeled data, and exposes operational decisions through BI.

The system should demonstrate these questions:

- Where is work-in-process, and how long has it waited?
- Which station or asset is constraining throughput?
- Which process excursions caused quality holds?
- Which parts, lots, and batches are affected by a deviation?
- What happens to yield, rework, scrap, and delivery when equipment health declines?
- Can every dashboard number be traced back to a source event, model version, simulation run, and assumption?

The system should **not** claim that its thresholds, defect rates, routes, or recipes represent SpaceX. SpaceX may be the motivating context, but the modeled factory must be called a generic reference line unless a public source supports a narrower claim.

## Recommended architecture

Use a staged architecture rather than deploying a complete industrial platform immediately:

```text
Research ledger and source claims
              |
              v
Versioned factory model + parameter profiles
              |
              v
Python discrete-event simulator
  routing, queues, resources, genealogy, failures, quality
              |
              +--> OPC UA equipment adapter / simulator
              |
              +--> MQTT or Sparkplug event publication
              |
              v
Raw event store and modeled operational database
              |
              +--> telemetry analytics
              +--> genealogy and traceability
              +--> quality and reliability marts
              |
              v
BI API and Luke-the-duke.com dashboard
              |
              +--> optional OpenRouter narrative/scenario services
```

SimPy is a suitable initial simulation engine because it is a process-based discrete-event framework with processes, events, and shared resources; it is designed for systems where queues and limited-capacity resources interact. FactorySimPy is worth evaluating as a reference or optional dependency because it provides canonical manufacturing components such as machines, combiners, buffers, and configurable processing delays on top of SimPy. OpenFactoryTwin is another useful architectural reference because it represents factory state, process executions, and event logs and explicitly targets simulation-based digital twins for production and logistics.[5][6][7][8]

The first implementation should be a plain Python package with a database and event adapter. Do not make the simulation dependent on an LLM, web application, or broker. It must be runnable in an offline mode with a fixed random seed.

## Factory model

Model a generic investment-casting reference line in enough detail to support genealogy, bottleneck analysis, quality containment, and maintenance scenarios:

| Area | Workstation | Main outputs |
|---|---|---|
| Materials | Receiving and quarantine | Material lots, certificates, release/hold status |
| Core | Ceramic-core forming/firing/inspection | Core lots and inspection results |
| Pattern | Wax-pattern injection and inspection | Pattern serials and dimensional results |
| Assembly | Cluster assembly | Mold/cluster genealogy |
| Shell | Ceramic-shell building and drying | Shell batches and mold readiness |
| Thermal | Dewax and shell preheat | Cycle records and shell release |
| Melt | Alloy charge and vacuum induction melting | Melt heats, chemistry, melt telemetry |
| Pour | Vacuum pour and controlled solidification | Cast part serials, process curves, alarms |
| Post-cast | Knockout and gate removal | Cast-part status and visual results |
| Thermal treatment | Heat treatment and HIP | Batch cycles, recipes, pressure/temperature records |
| Finishing | Machining and finishing | Tool usage, dimensions, rework records |
| NDT | Fluorescent penetrant, radiography/CT, or equivalent reference inspection | Inspection results and evidence links |
| Quality | Final inspection and disposition | Accept, rework, hold, scrap, conditional release |
| Logistics | Packing and shipment | Released serials and certificate package |

The MVP should implement six core workstations: shell building, preheat, vacuum melt/pour, controlled solidification, heat treatment, machining, and NDT/final disposition. Receiving, core, pattern, and shipment can initially be represented as upstream/downstream genealogy records rather than fully simulated queues.

The model should follow ISA-95 concepts without pretending to implement the standard completely. ISA-95 distinguishes physical process, sensing/actuation, supervisory control, manufacturing operations management, and business planning/logistics levels; Level 3 includes MES, SCADA, maintenance, quality, inventory movement, historians, recipe management, and product tracking. This maps cleanly to Archify's separation between simulated equipment, event transport, MES-like modeled records, and portfolio analytics.[9][10][11]

## Source of truth hierarchy

Every record must carry provenance. The system should maintain four separate categories:

| Category | Examples | Authority |
|---|---|---|
| Public reference | NASA C-MAPSS, UCI Steel Plates Faults, public standards, open-source project documentation | External evidence, not factory truth |
| Research claim | Generic process stage, protocol behavior, terminology | Design constraint with citation |
| Simulation fact | Serial, lot, timestamp, route state, sensor value, quality result | Authoritative only inside a simulation run |
| Generated context | Shift note, maintenance narrative, quality summary | Narrative or advisory only |

Use fields such as `synthetic`, `source_type`, `source_id`, `source_version`, `simulation_run_id`, `model_version`, `parameter_profile`, `random_seed`, `occurred_at`, and `ingested_at`. A data consumer should be able to answer: "Was this measured, imported, derived, or generated?" without reading application code.

## Seed data research

### NASA C-MAPSS

NASA's C-MAPSS dataset contains multivariate time series from simulated engine degradation. NASA describes engine-specific initial wear and manufacturing variation, sensor noise, changing operating conditions, degradation that grows toward failure in training trajectories, and remaining-useful-life targets. The NASA Prognostics Center of Excellence repository provides a public download and citation for the turbofan degradation simulation dataset. A NASA Open Data listing identifies the dataset as public domain, although the repository's current access situation should still be checked by the downloader at build time.[12][13][14]

Use C-MAPSS as a **behavioral reference for equipment-health modeling**, not as foundry data. Extract patterns such as normal operation, gradual drift, accelerated degradation, sensor noise, and run-to-failure behavior. Map those patterns to a generic vacuum pump, furnace subsystem, CNC spindle, or inspection asset through a documented transformation layer. Do not copy aircraft sensor labels into a furnace schema and do not claim physical equivalence.

The repo should download C-MAPSS through a reproducible script, record the URL, retrieval date, checksum, source citation, and transformation version, and retain the raw dataset separately from Archify-generated events.

### UCI Steel Plates Faults

The UCI Steel Plates Faults dataset contains 1,941 observations and seven fault classes and is licensed CC BY 4.0 with DOI `10.24432/C5J88N`. Use it as a compact, external reference for quality analytics, classification workflows, defect Pareto analysis, model evaluation, and explainability.[15]

Do not map its labels directly to turbine-blade defects. Keep it in an `external_quality_reference` domain and create a clearly labeled synthetic mapping only if needed for a demonstration. The important portfolio feature is not claiming cross-domain accuracy; it is showing correct separation between external reference data and the simulated factory's own defect model.

### Kaggle casting imagery

The Kaggle casting-product dataset is a useful optional seed for an inspection-cell demonstration. Search results describe 7,348 grayscale casting images labeled acceptable or defective. Its parts are not turbine blades, so it should only support an image-ingestion and human-review workflow, not a claim of aerospace NDT accuracy. The dataset's exact license and redistribution terms must be verified directly before bundling or redistributing it; the repository should provide a downloader and checksum rather than committing the full image set.[16][17]

### Optional references

N-CMAPSS is a later option for a stronger prognostics module. NASA-related research describes it as synthetic run-to-failure data generated under realistic flight conditions with multiple fault modes, but it is still not foundry data. It should not delay the first build.[18][19]

### Seed-data policy

External datasets should calibrate **shapes, behaviors, schemas, and ML workflow patterns**, not establish proprietary process limits. Numerical parameters for Archify must be tagged as one of:

- `source_backed`: directly supported by a public source;
- `derived`: a transparent transformation of a source-backed quantity;
- `assumption`: selected by the project to create a useful test case;
- `sensitivity_only`: intentionally varied to study model behavior;
- `unvalidated`: not checked against physical factory data.

## Deterministic simulation versus LLM generation

The authoritative process model should use deterministic logic plus stochastic distributions. Cycle durations may use triangular or lognormal distributions; failures may use a reliability distribution; sensor noise can be modeled explicitly; defects can be generated from causal risk functions; inspection can have sensitivity and specificity; and batch effects can create correlated outcomes across parts.

A process excursion should propagate causally:

```text
asset degradation
   -> vacuum or thermal excursion
   -> process-run deviation
   -> increased defect risk
   -> NDT result or quality hold
   -> rework/scrap/conditional release
   -> yield, WIP, cost, and delivery impact
```

Use hard rules for containment. For example, a simulated vacuum deviation during a defined pour window can place all affected serials on quality hold. It should not automatically mean scrap; the disposition route should be hold, additional inspection or review, then accept, rework, scrap, or conditional release.

OpenRouter is appropriate for structured scenario proposals and narrative documents. Its official documentation supports JSON Schema responses for compatible models and recommends strict schemas, descriptions, and endpoint checks; support is per provider endpoint, not guaranteed universally. Every response must still be validated locally for schema, semantics, asset existence, time validity, permitted ranges, and allowed state transitions.[20][21]

Good LLM roles include:

- propose a `vacuum_excursion` scenario within a declared fault catalog;
- write a shift handoff from validated events;
- write a maintenance work order from a validated downtime event;
- summarize a quality evidence packet without changing source facts;
- create a synthetic supplier certificate or inspection narrative labeled as synthetic.

Bad LLM roles include:

- inventing authoritative telemetry;
- deciding whether a furnace was available;
- creating the genealogy graph;
- selecting acceptance limits;
- assigning the final quality disposition;
- overwriting or repairing source events;
- claiming that a generated recipe represents SpaceX or an actual foundry.

## Repository plan

The repository should be designed for both humans and coding agents. The top-level index must be the first navigation point. Every meaningful directory and file should have a short index entry explaining purpose, dependencies, inputs, outputs, version, timestamp, and change risk.

Suggested structure:

```text
archify-foundry-twin/
├── AGENTS.md
├── README.md
├── REPO_INDEX.md
├── CHANGELOG.md
├── LICENSE
├── pyproject.toml
├── uv.lock
├── Makefile
├── compose.yaml
├── .env.example
├── .gitignore
├── docs/
│   ├── DOCS_INDEX.md
│   ├── architecture.md
│   ├── factory-process.md
│   ├── data-provenance.md
│   ├── assumptions-register.md
│   ├── event-contract.md
│   ├── qa-qc-plan.md
│   ├── work-orders.md
│   ├── milestones.md
│   └── adr/
├── index/
│   ├── FILE_INDEX.yaml
│   ├── SCHEMA_INDEX.yaml
│   ├── EVENT_INDEX.yaml
│   └── AGENT_NAVIGATION.md
├── config/
│   ├── factory.yaml
│   ├── recipes.yaml
│   ├── defect-model.yaml
│   ├── reliability-profiles.yaml
│   └── scenarios/
├── src/archify/
│   ├── domain/
│   ├── simulation/
│   ├── quality/
│   ├── reliability/
│   ├── genealogy/
│   ├── events/
│   ├── provenance/
│   └── adapters/
├── services/
│   ├── simulator/
│   ├── opcua_simulator/
│   ├── ingest/
│   ├── llm_gateway/
│   └── api/
├── schemas/
│   ├── json/
│   └── sql/
├── migrations/
├── dashboards/
├── notebooks/
├── tests/
│   ├── unit/
│   ├── invariants/
│   ├── contract/
│   ├── integration/
│   └── scenario/
├── scripts/
│   ├── fetch_external_data.py
│   ├── run_simulation.py
│   ├── validate_run.py
│   └── build_indexes.py
└── data/
    ├── external/.gitkeep
    ├── raw/.gitkeep
    └── README.md
```

The repository should not place a separate verbose index file beside every tiny file. That creates documentation noise and becomes stale. Use one generated `FILE_INDEX.yaml` with one entry per tracked file, plus local `README.md` files for directories with non-obvious behavior. The index generator should run in CI and fail when tracked files are missing from the index or stale beyond an allowed threshold.

Recommended file-index entry:

```yaml
- path: src/archify/simulation/engine.py
  purpose: Runs the discrete-event factory simulation and emits canonical events.
  version: v0.1.0
  last_reviewed: 2026-08-30T00:00:00Z
  inputs:
    - config/factory.yaml
    - config/recipes.yaml
    - config/defect-model.yaml
  outputs:
    - simulation events
    - run manifest
  depends_on:
    - src/archify/domain/models.py
    - simpy
  consumed_by:
    - services/simulator
    - tests/invariants
  change_risk: high
  breaks_if_changed:
    - event timestamps and genealogy contracts
    - downstream database loaders
    - scenario replay tests
  verification:
    - tests/unit/test_engine.py
    - tests/invariants/test_genealogy.py
```

The index should describe what would break, not merely what a file contains. Agents should begin at `REPO_INDEX.md`, follow the exact file path, read its dependencies and verification references, then modify the smallest possible surface area.

## AGENTS.md policy

`AGENTS.md` should define the operating rules for every coding agent:

- read `REPO_INDEX.md` before editing;
- read the target file's index entry and all high-risk dependencies;
- never invent a schema, event, threshold, or public source;
- label all synthetic data and generated documents;
- preserve backward compatibility or update the schema version;
- run focused tests before broad tests;
- update the index, changelog, assumptions register, and timestamp when behavior changes;
- do not add secrets or OpenRouter keys to the repository;
- do not commit external datasets unless the license permits redistribution;
- do not call generated output validated merely because it is JSON;
- report uncertainty and failed checks explicitly;
- use work orders with acceptance criteria and QA evidence;
- make no unrelated refactors.

Every agent-created change should include a short work-order ID in the commit or pull-request title, such as `WO-001 implement canonical event envelope`.

## Container build

Start with a small Docker Compose stack, not UMH:

```text
postgres or TimescaleDB  -> modeled records and telemetry
mosquitto                -> MQTT event transport
opcua-simulator          -> simulated equipment interface
factory-simulator        -> discrete-event engine
ingest                   -> event persistence and normalization
api                      -> read-only portfolio/query API
grafana                  -> optional development analytics
```

Eclipse Mosquitto is an open-source MQTT broker supporting MQTT 5.0, 3.1.1, and 3.1 and includes command-line publisher/subscriber utilities. The initial topic model can use plain MQTT with a versioned Archify envelope. Evaluate Sparkplug after the canonical event model is stable; Sparkplug adds an industrial MQTT topic namespace, payload structure, and session-state management for SCADA/IIoT integration.[22][23][24]

Use Docker Compose healthchecks and dependency conditions so the application does not race the database or broker. Compose supports `healthcheck` and `service_healthy`, and profiles can enable optional services only when needed.[25][26]

The first compose profile should be `core`: database, broker, simulator, ingest, and API. A `bi` profile can add Grafana. An `llm` profile can add the OpenRouter gateway. A later `industrial` profile can add UMH or Redpanda for comparison. Keep all OpenRouter access behind the gateway so the simulator remains runnable without a key.

## Open-source repositories to study

| Repository or project | Role in Archify | Recommendation |
|---|---|---|
| SimPy | Discrete-event simulation engine | Use directly for MVP; official docs support processes, events, and shared resources.[5] |
| FactorySimPy | Manufacturing DES components | Study or prototype against it; avoid adding it unless its fixed-structure assumptions fit.[8] |
| OpenFactoryTwin / OFacT | State and process-execution digital-twin concepts | Study its event-log and factory-state model.[7] |
| United Manufacturing Hub | Industrial ingestion, contextualization, storage, UMH Core, Redpanda | Use as Phase 2 architecture benchmark, not MVP dependency.[27] |
| node-opcua | TypeScript OPC UA client/server and gateway layer | Use for an optional OPC UA adapter or simulated equipment endpoint.[28][29] |
| Eclipse Mosquitto | Lightweight MQTT broker | Use in the core compose stack.[22] |
| OpenMES | MES concepts and self-hosted production tracking | Study for work orders, tracking, and traceability; do not make it the core domain model.[30] |
| Eclipse Sparkplug | Industrial MQTT interoperability | Evaluate after plain MQTT contracts work.[23][31] |

Do not fork multiple repos into the application. Prefer an `external/` research manifest and small adapter modules. The repository should explain what was borrowed, what was inspired, what license applies, and what is original.

## Data model and event contract

The core entities should include `material_lot`, `core_lot`, `wax_pattern`, `shell_batch`, `mold`, `melt_heat`, `work_order`, `process_run`, `equipment_asset`, `equipment_state`, `part_serial`, `inspection_result`, `nonconformance`, `maintenance_order`, `quality_hold`, `disposition`, and `simulation_run`.

Use a canonical envelope:

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
  "workstation_id": "vacuum-furnace-01",
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
    "simulation_run_id": "sim-2026-08-30-001",
    "generator": "archify-sim-v0.1.0",
    "random_seed": 42,
    "parameter_profile": "baseline-v1"
  }
}
```

Raw events should be append-only. Modeled tables should be rebuildable from raw events plus versioned reference data. BI marts should be derived and disposable. This supports replay, auditability, and agent-safe change management.

## QA, QC, and verification

Archify needs a written QA/QC plan before it has a dashboard. The key distinction is:

- **Verification:** did the implementation correctly execute the defined model?
- **Validation:** does the model represent the real system adequately for its intended purpose?
- **Uncertainty quantification:** how sensitive are the outputs to unknown or assumed parameters?

NIST and manufacturing digital-twin literature emphasize that these are distinct and recurring lifecycle activities; without real factory data, Archify can perform strong verification and sensitivity analysis but cannot claim full real-world validation.[2][3][32]

Required invariant tests:

- every part has a unique serial;
- every released part has complete required genealogy;
- no process starts before its prerequisites are complete;
- no machine produces while unavailable;
- resource capacity is never exceeded;
- quarantined material cannot be consumed;
- scrapped parts cannot ship;
- event timestamps are nondecreasing per source stream;
- each quality hold has a reason and disposition path;
- each simulated event points to a simulation run and model version;
- raw events are immutable;
- replaying the same seed and configuration produces the same canonical event stream.

Required QC checks should cover nulls, uniqueness, accepted status values, foreign-key relationships, units, timestamp validity, range checks, duplicate events, mass balance, and cross-table genealogy. dbt's standard tests include `unique`, `not_null`, `accepted_values`, and `relationships`, which are a useful minimum for modeled data. Great Expectations is an optional later layer for richer data-integrity expectations across tables and sources.[33][34]

Model-level QA should include golden scenarios:

| Scenario | Expected result |
|---|---|
| Baseline run | Normal route completion and complete genealogy |
| Furnace downtime | Queue growth, lost capacity, no production during downtime |
| Vacuum excursion | Alarm, affected process runs identified, serials placed on hold |
| Bad ceramic-core lot | Correlated downstream defect risk and containment blast radius |
| NDT false negative | Inspection result differs from latent defect state, clearly labeled |
| Replay | Same seed produces same facts and metrics |
| LLM malformed response | Response rejected without mutating simulation state |

## Work-order and milestone plan

### Milestone 0 — repository control plane

**Work orders:** initialize repo, create `AGENTS.md`, create top-level indexes, define versioning, add provenance policy, add CI skeleton.

**Acceptance:** an agent can start at `REPO_INDEX.md`, locate any source file, identify dependencies and break risk, and run a single validation command.

### Milestone 1 — research and factory specification

**Work orders:** create research ledger, process map, entity glossary, parameter register, assumption register, external-data manifest, and architecture decision records.

**Acceptance:** every modeled station has a purpose, inputs, outputs, resources, state transitions, evidence, assumptions, and open questions.

### Milestone 2 — deterministic route

**Work orders:** implement part/lot/work-order models, station resources, routing, genealogy, append-only events, and invariant tests.

**Acceptance:** one fixed-seed run completes with no illegal state transitions and a complete part genealogy.

### Milestone 3 — stochastic process behavior

**Work orders:** add cycle-time distributions, queues, machine downtime, sensor noise, batch effects, defect risk, inspection outcomes, and disposition logic.

**Acceptance:** multiple seeds create variation while preserving invariants; metrics include uncertainty intervals rather than a single asserted truth.

### Milestone 4 — industrial transport

**Work orders:** add MQTT publication, ingestion worker, OPC UA simulator/adapter, topic documentation, replay, and raw-event persistence.

**Acceptance:** a simulated equipment event can travel from source adapter through the broker into the raw and modeled stores with provenance intact.

### Milestone 5 — external seed-data pipelines

**Work orders:** add NASA, UCI, and optional Kaggle download scripts, checksums, license records, transformations, and isolated reference schemas.

**Acceptance:** a clean environment can fetch or clearly report unavailable data, reproduce transformations, and never mix external reference rows with simulation facts.

### Milestone 6 — analytics and BI

**Work orders:** create production, WIP, quality, reliability, genealogy, and containment marts; build non-decorative dashboard views; expose portfolio-safe read APIs.

**Acceptance:** a reviewer can follow one incident from asset degradation to process excursion to affected serials to disposition and business impact.

### Milestone 7 — OpenRouter layer

**Work orders:** add gateway, model configuration, strict JSON schemas, local semantic validation, cost/token logging, prompt versions, and synthetic-document storage.

**Acceptance:** the system operates with no API key; malformed or semantically invalid model output is rejected; generated text cannot mutate authoritative process facts.

### Milestone 8 — industrial comparison

**Work orders:** document UMH, Sparkplug, and optional Redpanda deployment; compare plain Compose against an industrial reference profile.

**Acceptance:** the comparison explains what additional capability is gained and what operational complexity is introduced; it is not merely a second pile of containers.

## README design

The README should open with the honest one-sentence description:

> Archify Foundry Twin is a research-grounded synthetic manufacturing data platform that simulates a generic investment-casting reference line, preserves material genealogy, emits industrial-style events, and demonstrates quality and reliability decisions without claiming access to real factory data.

It should then contain:

- portfolio demo link to Luke-the-duke.com;
- system diagram;
- quick start with Docker Compose;
- offline simulation command;
- optional OpenRouter setup;
- dashboard route;
- example incident walkthrough;
- data provenance and limitations;
- repository navigation instructions;
- architecture and event-contract links;
- test and validation commands;
- external-data licensing notice;
- roadmap and milestone status.

The README should not lead with animated factory graphics, decorative gauges, or a claim of prediction accuracy. Lead with a traceable operational question and show the evidence path.

## Portfolio presentation

Luke-the-duke.com should show a concise public case study with four views:

1. **Factory map:** stations, routes, queues, assets, and event boundaries.
2. **Operations:** throughput, WIP age, cycle time, bottleneck, downtime, and schedule impact.
3. **Quality and containment:** defect Pareto, first-pass yield, holds, rework/scrap, and affected-lot blast radius.
4. **Evidence and provenance:** simulation run, seed, model version, assumptions, source claims, and validation status.

A reviewer should be able to click from a quality incident to the affected process run, asset telemetry, material lots, serials, inspection records, and disposition. This is more credible than displaying live-looking numbers without traceability.

## Final build recommendation

Build the project in Python first, with SimPy, Pydantic or equivalent schema validation, PostgreSQL, Mosquitto, and a small API. Keep TypeScript limited initially to the OPC UA adapter or web presentation if that accelerates the portfolio. Add FactorySimPy or OpenFactoryTwin as studied references before adopting them as dependencies. Use NASA C-MAPSS for equipment-health behavior, UCI Steel Plates Faults for a separate quality-model reference, and Kaggle casting imagery only as an optional visual-inspection module after license verification.

The defining technical rule is: **simulation code owns truth; LLMs propose or explain; validators decide whether outputs are admissible.** The defining portfolio rule is: **every number is traceable to an event, model version, seed, parameter profile, and evidence status.** The defining research rule is: **public sources ground the architecture and behaviors, but no external dataset is presented as real turbine-foundry data.**

That scope is difficult but learnable because it separates the work into clear layers: process modeling, data contracts, simulation, transport, storage, analytics, QA/QC, and agent orchestration. It is also the strongest version of the idea that can be defended honestly without access to a real factory.
