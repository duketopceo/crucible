# Data Provenance Policy

Every record answers: **was this measured, imported, derived, or generated?** — without reading application code.

## Mandatory fields

| Field | Meaning |
|---|---|
| `synthetic` | always `true` in this repo — all data is simulation output |
| `source_type` | `simulation` \| `external_reference` \| `research_claim` \| `generated_context` |
| `source_id` / `source_version` | origin identifier and version (e.g. dataset DOI, config file version) |
| `simulation_run_id` | run that produced the record |
| `model_version` | crucible package version that generated it |
| `parameter_profile` | named profile in `config/` (e.g. `baseline-v1`) |
| `random_seed` | seed for the producing run |
| `occurred_at` / `ingested_at` | simulated event time vs real ingestion time |

## Rules

1. Raw events: append-only, immutable, never edited or deleted.
2. Modeled tables: rebuildable from raw events + versioned reference data. Disposable marts are derived.
3. External datasets (M5): downloaded via script with URL, retrieval date, checksum, license, and citation recorded. Raw external data never mixes with simulation facts — separate schemas.
4. Generated documents (M7, deferred): labeled `generated: true`, stored separately, never authoritative.

## Data categories

- **Public reference** — NASA C-MAPSS (equipment-health behavior patterns), UCI Steel Plates Faults (quality analytics reference). Shapes/behaviors only; no cross-domain accuracy claims.
- **Research claim** — terminology and process structure from public standards/literature, cited in the assumptions register.
- **Simulation fact** — authoritative only inside a run identified by run id + seed + profile.
- **Generated context** — advisory narrative, never mutates facts.
