# Machine Integration Map

## Purpose

This document maps generic investment-casting machine classes to practical acquisition paths. It is a design reference for **replaceable adapters**: the same Crucible pipeline must accept simulated, OPC UA, MTConnect, REST, database-export, or file-drop sources without changing the canonical event or genealogy model.

This is not an equipment specification and does not identify a particular company’s machines.

## Acquisition principles

1. Capture raw source payloads before normalization.
2. Preserve source ID, source timestamp, ingestion timestamp, data quality/status, units, and mapping version.
3. Treat controller values as observations, not inferred business truth.
4. Do not send control commands from the portfolio collector.
5. Use read-only integrations by default.
6. Never publish credentials, endpoint addresses, certificates, or customer machine data.
7. Emit normalized events only after schema and semantic checks.
8. Route unmapped, malformed, duplicate, or suspicious data to a dead-letter/review path.

## Machine and data matrix

| Area | Machine class | Observations to capture | Preferred real integration | Simulated integration | Risks and validation |
|---|---|---|---|---|---|
| Pattern | Wax injector | Asset state, cycle start/end, recipe, injection pressure/temperature, tooling/mold ID, count, alarm | PLC via OPC UA | OPC UA server | Confirm units, cycle ordering, tooling revision, state transitions |
| Assembly | Robotic tree/cluster cell | Program, robot state, cycle, gripper/interlock state, pattern IDs, fault | Robot/PLC OPC UA or vendor API | MQTT event producer | Avoid assigning one pattern to two trees; require operation completion |
| Shell | Dip/stucco/dry line | Shell ID, layer, slurry lot, temperature/viscosity, dip time, drying time, humidity, alarms | PLC/SCADA plus manual QC | Process-run simulator | Enforce layer order; identify which values are instrumented versus operator-entered |
| Preheat | Dewax/preheat furnace | Zone/control/load temperature, setpoint, recipe, cycle phase, load ID, pressure, alarm | OPC UA/historian/chart export | OPC UA furnace model | Validate time ordering, calibration status, required temperature records |
| Melt/pour | VIM furnace | Heat ID, charge lot, vacuum, melt temperature, power, gas/atmosphere, cycle, pour window, alarms | OPC UA/historian + quality system | OPC UA + MQTT | Prevent production during downtime; validate heat/part links and recipe state |
| Solidification | Directional/controlled solidification furnace | Mold ID, furnace state, thermal zones, withdrawal/cooling profile, cycle timing, alarm | OPC UA/historian | Curve generator | Validate profile phases, monotonic/allowed transitions, duration bounds |
| Post-cast | Knockout/gate removal | Cell state, cycle, work order, part IDs, operator, visual result, rework | PLC/OPC UA plus terminal | Process event producer | Require valid cast status; preserve operator-entered evidence distinctly |
| Thermal | Heat-treat furnace | Setpoint, control/load thermocouples, actual temperatures, recipe, soak, quench, load ID, alarms | OPC UA/historian/record export | Batch-process model | Preserve calibration and survey records separately; do not fabricate aerospace compliance |
| Thermal | HIP system | Batch/load ID, pressure, temperature, cycle phase, hold duration, alarms | OPC UA/historian | Batch-process model | Confirm recipe/load linkage; distinguish pressure units and source quality |
| Finish | CNC machine | Execution state, job, part count, active program, tool ID/life, spindle/axis values, alarms | MTConnect preferred; OPC UA/CNC API alternative | MTConnect-like source | Preserve MTConnect sequence; detect reset, gap, duplicate, and unit changes |
| Metrology | CMM | Serial, program, feature ID, nominal, actual, tolerance, pass/fail, probe, operator | CMM/QMS API, export, file watcher | CSV/API adapter | Validate serial, tolerance direction, units, program revision, reviewer |
| NDT | X-ray/CT | Scan ID, serial, inspection recipe, image/report URI, indication, result, reviewer | Vendor API/file drop/QMS | Inspection event | Persist source evidence first; do not turn a classifier score into final disposition alone |
| NDT | FPI/surface inspection | Method, serial, operator, indication location/type, result, report, disposition | QMS/manual terminal/API | Inspection event | Require method and reviewer; distinguish finding from disposition |
| Quality | QMS | NCR, hold, reason, disposition, approval, evidence links | REST/API/database export | Domain service | Holds must block release; approval workflow must be attributable |
| Maintenance | CMMS | Asset, downtime start/end, failure code, work order, technician, repair action, spares, root cause | REST/API/export | Maintenance service | Do not infer repair completion from prose; use timestamps and status |
| Operations | MES | Work order, route, resource, lot/serial, queue state, completion, genealogy | REST/API/database/message bus | Domain service | Maintain legal route and one current location/status per serial |

## OPC UA implementation path

### Phase 1: simulator

- Implement `services/opcua_simulator` with a small node tree for VIM and heat-treat assets.
- Expose asset metadata, machine state, current work order, recipe ID, alarm state, and telemetry tags.
- Publish updates using deterministic simulator time with explicit source timestamps.
- Use a local development endpoint only; never hard-code a production endpoint.

### Phase 2: adapter contract

The OPC UA client adapter must:

1. Load endpoint and mapping from configuration/environment only.
2. Establish explicit authentication/security mode in production deployments.
3. Persist source namespace, node ID, browse path, data type, engineering unit, status code, and timestamps.
4. Subscribe to state, alarms, job/recipe, and critical measurement nodes.
5. Emit `connection.opened`, `connection.degraded`, `connection.closed`, and `telemetry.recorded` events.
6. Use bounded retry/backoff and make reconnect behavior testable.
7. Retain unknown/unmapped node values in raw storage without treating them as modeled fields.

### Minimum node families

```text
Objects/Crucible
  Assets/VIM-01
    Metadata/AssetId
    Metadata/Manufacturer
    State/MachineState
    State/Availability
    Job/WorkOrderId
    Job/RecipeId
    Process/HeatId
    Process/VacuumPressure
    Process/MeltTemperature
    Process/Power
    Alarms/Active
  Assets/HT-01
    Metadata/AssetId
    State/MachineState
    Job/BatchId
    Job/RecipeId
    Process/Setpoint
    Process/ControlTemperature
    Process/LoadTemperature
    Process/CyclePhase
    Alarms/Active
```

## MTConnect implementation path

MTConnect is the preferred portfolio representation for CNC-style data because it is a read-only, standard vocabulary for machine-tool observations. The adapter must preserve raw device semantics instead of pretending all data is generic telemetry.

1. Fetch `/probe` and store the device model plus discovery timestamp.
2. Fetch `/current` to establish initial machine state.
3. Fetch `/sample` incrementally with persistent sequence state.
4. Store the raw response and each data item’s ID, category, type, subtype, timestamp, sequence, value, and unit if available.
5. Detect agent resets, duplicate sequence IDs, gaps, unknown data items, and conflicting units.
6. Map only reviewed data items into canonical tags.
7. Treat collection as read-only. Commands, programs, or controller writes are out of scope.

### Useful CNC fields

```text
availability
execution / controller mode
program / job identifier
part count
tool identifier and tool life
spindle speed/load
axis position
feed rate
alarm / condition
operator message
```

## File/API inspection path

CMM, NDT, and QMS systems may expose REST APIs, databases, CSV/XML/JSON exports, or network-file drops. The adapter must preserve the original artifact first, then validate it.

```text
source report/image
  -> immutable evidence record
  -> serial/method/timestamp/program validation
  -> typed inspection event
  -> quality review or model update
```

A classifier confidence score is an observation, not a release decision. Final disposition must remain a modeled quality workflow with a reason and, where configured, reviewer/approval attribution.

## Canonical normalized data requirements

Every normalized machine event includes:

```text
event_id
schema_version
event_type
source_system
source_record_id or source_sequence
asset_id
workstation_id
occurred_at
ingested_at
payload
raw_payload_reference
mapping_version
provenance.synthetic
provenance.simulation_run_id when synthetic
```

For numeric telemetry, preserve `value`, `unit`, `quality_code`, `source_timestamp`, and measurement/tag identity. Never use a dashboard-calculated metric as raw telemetry.

## Acceptance tests

- A simulated OPC UA VIM tag reaches raw storage, normalized storage, and an analytics query with timestamps intact.
- An unknown OPC UA node is retained raw and not mapped into the domain model.
- An MTConnect sequence gap creates a data-quality event.
- A duplicate MTConnect observation is deduplicated without erasing raw evidence.
- An inspection artifact with an unknown serial routes to review and cannot release a part.
- A machine in `unavailable` status cannot produce a valid completion event.
- Changing a mapping version preserves old mappings and makes the change visible in event provenance.

## Related files

- `docs/technical-research-foundation.md`
- `docs/qa-qc-plan.md`
- `docs/seed-data-research.md`
- `docs/agent-navigation-and-indexing.md`
- Future: `schemas/json/canonical-event.schema.json`
- Future: `config/machine-mappings/*.yaml`
- Future: `src/crucible/adapters/*`
