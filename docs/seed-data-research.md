# Seed Data Research and Provenance Policy

## Purpose

This document defines approved seed-data sources and limits for Crucible. Public datasets can inform data shapes, simulation behavior, and ML workflow demonstrations. They cannot establish proprietary foundry parameters or validate real turbine-blade manufacturing predictions.

## Approved sources

| Source | What it contains | Approved use | Not approved for |
|---|---|---|---|
| NASA C-MAPSS | Synthetic turbofan degradation time series with operational settings, sensor noise, variation, and run-to-failure trajectories | Asset-health/degradation pattern references, sensor trend experiments, maintenance analytics workflow | Foundry failure rates, furnace sensor limits, blade-quality predictions |
| UCI Steel Plates Faults | 1,941 steel-plate observations across seven fault classes; DOI `10.24432/C5J88N`; CC BY 4.0 | Generic classification, evaluation, feature pipeline, confusion matrix, explainability demonstration | Turbine-blade defect labeling, actual NDT accuracy, foundry yield claims |
| Kaggle casting product image data | Public casting-product images labeled acceptable/defective | Optional image ingestion, classifier integration, human-review queue demonstration | Aerospace blade NDT claim; redistribution without license review |

## NASA C-MAPSS handling

NASA C-MAPSS is a useful behavioral reference because it contains multiple multivariate degradation trajectories with normal initial variation, operating-condition effects, sensor noise, faults that grow toward failure in training data, and remaining-useful-life targets.

Use it to create a **derived asset-health profile** only. Example targets in Crucible may include a simulated vacuum-pump health score, furnace-subsystem degradation score, CNC spindle-health score, or inspection-asset availability trend.

The transformation must not copy turbofan sensor names into foundry telemetry or imply physical equivalence. Store the raw dataset separately and document the mapping:

```text
NASA C-MAPSS sequence
-> normalized generic degradation curve
-> derived health-state profile
-> simulated fault probability / sensor drift behavior
-> reference-factory asset scenario
```

The transformed profile is `derived` or `sensitivity_only`, never `source_backed` as a foundry fact.

## UCI Steel Plates Faults handling

Use the UCI data as an isolated `external_quality_reference` domain. A baseline model may demonstrate cleaning, split strategy, classification, calibration, confusion matrix, error review, and feature attribution.

Do not rename source labels into turbine-blade defect labels. If a portfolio display needs a crosswalk, present it as a synthetic UI/category mapping and preserve the original label in the source table.

## Kaggle casting imagery handling

This is optional and should wait until the core factory route, genealogy, and quality workflow are working. It may enrich a simulated inspection cell:

```text
part arrives at inspection
-> image/artifact stored
-> model returns score + class
-> result is a quality observation
-> low confidence or defect opens review/hold
-> final disposition remains a modeled quality workflow
```

Before use, confirm the dataset creator’s license, terms, required attribution, access restrictions, and redistribution rights. Prefer a download script plus checksum over committing the image corpus into Git.

## Acquisition controls

Every external download must generate a manifest entry with:

```yaml
source_name: ""
source_url: ""
retrieved_at: ""
license_or_terms: ""
citation_or_doi: ""
raw_sha256: ""
source_schema_version: ""
transformation_version: ""
allowed_use: ""
known_limitations: ""
local_path: ""
```

Recommended storage layout:

```text
data/
  external/        # untracked raw downloads unless license permits inclusion
  manifests/       # tracked metadata, checksums, citations, acquisition instructions
  derived/         # reproducible generated reference artifacts; default untracked if large
  fixtures/        # small, license-reviewed test fixtures only
```

The repository should track scripts, manifests, transformations, small reviewed fixtures, and documentation. It should not automatically track archives, full image datasets, or unreviewed third-party files.

## Provenance requirements

Every dataset-derived record must retain:

```text
source_type: external_reference | derived_reference | simulation | generated_context
source_name
source_record_id
source_version
transformation_version
license_or_terms_reference
synthetic flag
simulation_run_id, if applicable
```

Do not insert external records directly into tables whose meaning is authoritative simulation history. A documented transformation is mandatory.

## Known data gaps

| Gap | Consequence | Mitigation |
|---|---|---|
| No real foundry telemetry | Cannot calibrate sensor distributions or degradation rates | Use assumptions, sensitivity profiles, and clear labels |
| No real recipes/material limits | Cannot declare safe or actual acceptance thresholds | Use abstract recipe IDs and synthetic constraints only |
| No real NDT performance records | Cannot establish sensitivity/specificity | Make inspection performance an assumption and sweep it |
| Sparse public investment-casting time series | Weak direct calibration of process/defect links | Model causal structure; do not claim empirical rate accuracy |
| Licensing differences | Dataset copying may be prohibited | Store manifests and download scripts; verify terms before redistribution |
| Dataset drift/unavailability | Reproduction can fail | Capture retrieval date/checksum, fail clearly, cache only when permitted |

## Parameter labeling

Every parameter used in the simulator must have one status:

- `source_backed` — directly supported by cited public material
- `derived` — calculated or transformed from a source-backed input
- `assumption` — selected deliberately for the reference simulation
- `sensitivity_only` — varied to expose model behavior, not asserted as factual
- `unvalidated` — not compared with a physical factory or expert assessment

A dashboard or API response must be able to expose the active parameter profile and status. No output should visually imply that assumptions are measurements.

## Related files

- `docs/data-provenance.md`
- `docs/assumptions-register.md`
- `docs/technical-research-foundation.md`
- `docs/qa-qc-plan.md`
- Future: `scripts/fetch_external_data.py`
- Future: `data/manifests/*.yaml`
- Future: `src/crucible/provenance/*`
