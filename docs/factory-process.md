# Generic Investment-Casting Reference Line

The modeled factory is a **generic high-temperature investment-casting reference line** producing blades, vanes, and test coupons. It is not SpaceX and not any real foundry. All numeric parameters carry a tag (`source_backed | derived | assumption | sensitivity_only | unvalidated`) registered in `docs/assumptions-register.md`.

## Full reference line (fourteen areas)

```text
Receiving/quarantine
-> ceramic core
-> wax pattern
-> cluster assembly
-> shell building
-> dewax/preheat
-> vacuum melt/pour
-> controlled solidification
-> knockout/gate removal
-> heat treatment/HIP
-> machining/finishing
-> NDT (FPI/RT/CT)
-> final inspection & disposition
-> packing/shipment
```

## MVP scope (M2): six core workstations

Upstream (receiving, core, pattern, cluster assembly) and downstream (packing, shipment) are recorded as genealogy records, not simulated queues, until the core flow is verified.

| # | Workstation | Area | Capacity (config) | Outputs |
|---|---|---|---|---|
| 1 | Shell building | Shell | 4 | Shell batches on patterns (batch-effect source) |
| 2 | Preheat | Thermal | 2 | Preheat cycle records, mold readiness |
| 3 | Vacuum melt/pour | Melt | 1 | Melt heats, chemistry, cast part serials |
| 4 | Controlled solidification | Melt | 2 | Solidified serials, process curves, alarms |
| 5 | Heat treatment | Thermal treatment | 3 | Batch cycles (solution + aging; HIP optional) |
| 6 | Machining + NDT/final disposition | Finishing | 2 | Dimensions, inspection results, accept/rework/hold/scrap |

Capacities are `assumption` values pending M2 register entries.

## Causal excursion chain (M3+)

```text
asset degradation
-> vacuum/thermal excursion
-> process-run deviation
-> increased defect risk
-> NDT result / quality hold
-> rework/scrap/conditional release
-> yield, WIP, cost, delivery impact
```

A hold + review path is the default; automatic scrap requires an explicit documented synthetic rule.

## Claim discipline

- Generic reference line. No station parameter represents SpaceX or any real foundry.
- Every numeric parameter carries a source tag.
- The six stations and genealogy edges are versioned in `config/factory.yaml`; keep the two in sync.
