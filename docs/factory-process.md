# Generic Investment-Casting Reference Line

M0 spec stub. Entity glossary and per-station detail land with M1/M2 work orders.

## Modeled areas (full reference line)

Materials receiving/quarantine → Core → Pattern (wax) → Cluster assembly → Shell building → Dewax/preheat → Vacuum melt/pour → Controlled solidification → Knockout/gate removal → Heat treatment & HIP → Machining/finishing → NDT (FPI/RT) → Final inspection & disposition → Packing/shipment.

## MVP scope (M2): six core workstations

1. **Shell building** — shell batches accumulate on patterns (batch effect source)
2. **Preheat** — shell preheat cycles
3. **Vacuum melt/pour** — alloy charge, vacuum induction melting, pour
4. **Controlled solidification** — directional solidification window; vacuum excursion sensitivity
5. **Heat treatment** — batch cycles (solution + aging; HIP optional)
6. **Machining + NDT/final disposition** — gate removal, dimensional, FPI, accept/rework/hold/scrap

Receiving, core, pattern, and shipment are represented as upstream/downstream genealogy records initially, not simulated queues.

## Causal excursion chain (M3+)

asset degradation → vacuum/thermal excursion → process-run deviation → increased defect risk → NDT result / quality hold → rework/scrap/conditional release → yield, WIP, cost, delivery impact.

## Claim discipline

This is a **generic reference line**. No station parameter represents SpaceX or any real foundry. All numeric parameters carry a tag: `source_backed` | `derived` | `assumption` | `sensitivity_only` | `unvalidated`.
