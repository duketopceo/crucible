# Crucible (Archify Foundry Twin)

> Crucible is a research-grounded synthetic manufacturing data platform that simulates a generic investment-casting reference line, preserves material genealogy, emits industrial-style events, and demonstrates quality and reliability decisions without claiming access to real factory data.

**Status:** Milestone 0 — repository control plane.

## Why this exists

Portfolio demonstration of industrial IT, data-pipeline, and quality-systems competence: discrete-event simulation, ISA-95-aligned modeling, material genealogy/traceability, industrial transport (MQTT), provenance-preserving ingestion, and BI with full event-to-decision traceability.

The motivating context is turbine-blade investment casting (SpaceX is building a foundry), but the modeled factory is a **generic reference line**. No output represents SpaceX or any real foundry.

## Architecture (one paragraph)

A deterministic, stochastic discrete-event simulation (SimPy, Python) owns all process truth: routing, queues, station capacity, equipment state, telemetry, quality outcomes, and disposition. Selected events are published over MQTT, ingested into an append-only raw store, and modeled into rebuildable operational tables. BI views answer: where is WIP, what is constraining throughput, what caused quality holds, which lots are affected by a deviation — every number traceable to a simulation run, model version, seed, and parameter profile.

## Quick start (M4+, not yet active)

```bash
cp .env.example .env
docker compose --profile core up
make simulate   # offline, fixed seed, no services required
```

## Navigation

- `REPO_INDEX.md` — start here; maps every directory and key file.
- `index/FILE_INDEX.yaml` — machine-readable per-file index (purpose, deps, break risk).
- `docs/` — architecture, factory process, provenance policy, assumptions register, work orders.
- `config/` — versioned factory model, recipes, defect model, reliability profiles.
- `src/archify/` — the Python package (domain, simulation, events, provenance, adapters).
- `tests/` — unit, invariants, contract, integration, scenario.

## Honest claims policy

- **Verification** (did the code execute the defined model?) — yes, via invariant + golden-scenario tests.
- **Validation** (does the model match a real factory?) — **not claimed.** No real factory data exists here.
- **Uncertainty** — parameter profiles vary assumptions; metrics report sensitivity, not asserted truth.

## License

MIT — see `LICENSE`.
