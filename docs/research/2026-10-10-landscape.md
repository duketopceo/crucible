# Landscape: synthetic manufacturing data and factory twins

Method: README, ROADMAP and `docs/technical-research-foundation.md` read first; web search on 2026-10-11. Only claims a source supports are made. Gaps are marked.

## Who else is nearby

| Project | What it is | Source |
|---|---|---|
| SimPy | Python discrete-event simulation library; Crucible's planned engine (`pyproject.toml` extra `sim`). Described as more customisable than AnyLogic or Simul8 because it is open source. | [UTCluj paper](https://atna-mam.utcluj.ro/index.php/Acta/article/download/2837/2236) |
| ManPy | Open-source layer of manufacturing objects (machines, queues, buffers) on SimPy. | [UL Pure](https://pure.ul.ie/en/publications/manpy-an-open-source-layer-of-des-manufacturing-objects-implement/) |
| SimPyManufacturing | SimPy tool for multi-stage process industries (biomanufacturing), under active development per its docs. | [docs](https://simpymanufacturing-documentation.readthedocs.io) |
| OFacT (OpenFactoryTwin) | Python simulation-based digital twin for material flow; Apache-2.0; the 0.1.0 release (2024-09) held only the data model. | [Zenodo](https://zenodo.org/records/13734527), [ecosyste.ms](https://science.ecosyste.ms/projects/36315) |
| United Manufacturing Hub | Kubernetes Helm chart (Node-RED, MQTT, Kafka, TimescaleDB, Grafana) with a Sparkplug B input plugin; 0.x. | [UMH docs](https://docs.umh.app/benthos-umh/input/sparkplug-b-input), [about](https://www.umh.app/about) |
| Chalmers DES + Python pipeline | Paper on an API pipeline that runs new DES scenarios without rebuilding the model; pump-manufacturing case, no OPC UA or MQTT. | [Chalmers](https://research.chalmers.se/publication/553222) |

## What they do better

- ManPy and SimPyManufacturing already ship reusable station/queue objects. Crucible's six stations could be built on or compared against them rather than hand-rolled.
- UMH is a working, deployed IT/OT stack with Sparkplug B ingest. Crucible's M4 transport work duplicates part of it; M8 already plans a comparison.
- OFacT has a published data model for production state; worth reading before finalising WO-001 domain models.

## What users expect

A simulator that reviewers can trust: fixed-seed replay, invariant tests, and a clear statement of what is modelled. The search found no SimPy project that publishes OPC UA or MQTT event streams with provenance (search negative, not proof of absence).

## What is unique here

1. Provenance per record: `synthetic`, `source_type`, `model_version`, `parameter_profile`, `random_seed` on every event (README, ROADMAP).
2. An explicit honest-claims policy: verification yes, validation not claimed.
3. Genealogy-first design with event-to-decision traceability, aimed at a quality-containment walkthrough rather than a throughput dashboard.

## Gaps and risks

- No code exists yet beyond stubs (`src/crucible/*/__init__.py`, `scripts/run_simulation.py`); every comparison above is against plans, not behaviour.
- NASA C-MAPSS and UCI seed data (M5) were not re-verified in this pass; see `docs/seed-data-research.md`.
