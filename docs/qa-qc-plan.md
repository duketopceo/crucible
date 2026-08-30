# QA/QC Plan

## Purpose

This plan defines how Crucible verifies a synthetic manufacturing system without overstating real-world validation. It applies to simulation, event contracts, adapters, storage, analytics, external seed-data use, and LLM-assisted artifacts.

## Terms

| Term | Meaning in Crucible |
|---|---|
| QA | Preventive engineering practices: requirements, reviews, versioning, tests, CI, provenance, and change control |
| QC | Inspection of produced outputs: schema checks, data-quality checks, invariant checks, replay checks, and scenario results |
| Verification | Evidence that code correctly implements the declared model |
| Validation | Evidence that a model represents a real system for a defined use; limited here because no factory measurements are available |
| UQ | Sensitivity and uncertainty analysis for assumed parameters and stochastic outputs |

Crucible may claim verification where tests pass. It may claim sensitivity analysis where assumptions have been varied and reported. It must not claim physical validation or production predictive accuracy without real data and subject-matter validation.

## Quality gates

| Gate | Required evidence | Blocks release? |
|---|---|---|
| Documentation | Index entries, architecture/assumption/provenance updates | Yes for high-risk changes |
| Schema | JSON/typed schema validation and compatibility check | Yes |
| Unit | Focused unit tests for changed domain logic | Yes |
| Invariants | Route, genealogy, capacity, status, inventory, event-order checks | Yes |
| Contract | Adapter-to-canonical-event compatibility | Yes |
| Integration | Compose/offline components exchange valid data | Yes for affected services |
| Replay | Same seed/config produces same canonical facts | Yes for simulation changes |
| Data quality | Null, uniqueness, relationship, range, unit, and duplicate checks | Yes |
| Security | Secret scan where available plus human review of changed configs | Yes |
| Review | Work-order acceptance criteria and changed-contract review | Yes |

## Invariants

The following are non-negotiable unless a versioned design decision explicitly changes them:

1. Each part serial is unique.
2. Each released part has complete required genealogy.
3. A part follows a legal route and cannot start a step before prerequisites complete.
4. A resource cannot process beyond its capacity.
5. An asset cannot complete production while unavailable, under maintenance, or failed.
6. Quarantined material cannot be consumed without documented release.
7. A scrapped part cannot be released, packed, or shipped.
8. A quality hold has a reason, scope, and pending/final disposition path.
9. Raw events are append-only and remain attributable to a source.
10. Every synthetic event identifies its run, generator/model version, seed, and parameter profile.
11. Every external source record identifies its source, license/terms, retrieval time, checksum where feasible, and transformation version.
12. Per-source event order is preserved or explicitly represented as out-of-order; ingestion does not silently rewrite time.
13. A repeated fixed-seed run with the same configuration produces the same canonical event stream.
14. Generated LLM output cannot directly mutate authoritative simulation facts.

## Test layers

### Unit tests

Test domain methods and pure functions: status transitions, identifier generation, route rules, capacity use, genealogy joins, quality-risk calculations, unit normalization, and schema parsing.

### Invariant tests

Generate small simulation runs and assert all required invariants. Prefer property-based tests where useful: vary seed, queue size, downtime timing, lot status, and scenario input while demanding legal state.

### Contract tests

Run each adapter against fixed fixtures. Verify that source messages normalize to the canonical event envelope and that unsupported fields remain raw/reviewable rather than becoming untyped facts.

### Integration tests

Run core Compose services: database, broker, simulator, OPC UA endpoint, ingestion worker, and API. Prove an event travels through the intended pipeline and is queryable with provenance.

### Replay tests

Persist a seed, parameter profile, configuration hash, and run manifest. Re-run the same simulation and compare canonical events and derived metrics according to a stable comparison policy.

### Data-quality tests

Check `not_null`, uniqueness, accepted values, foreign-key relationships, timestamp plausibility, unit validity, value range, duplicates, raw/normalized linkage, and metric reconciliation.

### Scenario tests

Keep golden scenarios with declared expected behavior rather than fake real-world targets.

| Scenario | Assertions |
|---|---|
| Baseline | Legal end-to-end route, complete genealogy, no unexplained holds |
| Furnace downtime | No production during downtime; queue/WIP grows; recovery is modeled |
| Vacuum excursion | Alarm/deviation, affected serials identified, quality hold and enhanced inspection path |
| Bad core lot | Correlated affected parts, containment blast radius, no unrelated lot contamination |
| NDT false negative | Latent defect and observed result can differ; outcome is labeled synthetic/assumed |
| Duplicate delivery | Raw evidence retained; normalized event remains idempotent |
| Adapter reconnect | Connection event logged; collection resumes without unmarked gap |
| Malformed LLM result | Rejected; authoritative state unchanged |
| Mapping/schema migration | Old data remains interpretable or migration explicitly fails |
| Fixed-seed replay | Canonical facts match the original run |

## Quality control for external data

External datasets are references, never silent factory truth. Each download requires:

```text
source_name
source_url
retrieved_at
license_or_terms
citation_or_doi
raw_sha256
source_schema_version
transformation_version
allowed_use
known_limitations
```

The pipeline must prevent direct insertion of external rows into simulation-fact tables. A transformation must label output `derived`, `sensitivity_only`, or other declared source status.

## Quality control for OpenRouter artifacts

LLM output is always untrusted before validation. Required checks:

- Valid structured response/schema where applicable
- Scenario type exists in configured fault catalog
- Referenced asset and work order exist
- Timing is within simulation-run bounds
- Parameter range is allowed by the scenario profile
- Proposed state transition is legal
- Artifact carries model, provider, prompt version, response hash, time, and synthetic label
- Rejection retains the output as an audit artifact but does not mutate simulation state

The core test suite must use an offline fake gateway. No test requires an API key or paid inference.

## Uncertainty policy

Synthetic parameters must be tagged `source_backed`, `derived`, `assumption`, `sensitivity_only`, or `unvalidated`. Metrics from stochastic scenarios should display distributional results—such as quantiles or intervals—rather than a single implied factual prediction.

High-sensitivity assumptions must be identified through scenario sweeps. Typical candidates are defect-risk coefficients, machine-failure behavior, repair duration, inspection sensitivity/specificity, buffer capacity, and cycle-time distributions.

## Review checklist

Before a PR merges, reviewers must confirm:

- Work-order acceptance criteria are met.
- Related index entries have been updated.
- Schema/model/event changes are versioned.
- Provenance and assumptions are updated.
- Tests cover changed behavior and failure cases.
- No real factory claims, proprietary details, or misleading accuracy language were introduced.
- No credentials, tokens, personally identifiable information, customer data, or unlicensed datasets were added.
- Dashboard metrics retain links to inputs and run metadata.

## Related files

- `docs/technical-research-foundation.md`
- `docs/machine-integration-map.md`
- `docs/seed-data-research.md`
- `docs/agent-navigation-and-indexing.md`
- Future: `tests/invariants/*`
- Future: `tests/contracts/*`
- Future: `scripts/validate_run.py`
