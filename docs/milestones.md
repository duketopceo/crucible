# Milestones

Canonical milestone plan. Mirrors `ROADMAP.md`; this file is the status ledger. Critical path: **M0 → M1 → M2 → M3 → M4 → M6**. Deferrable: M5, M7, M8.

| Milestone | Scope | Acceptance | Status |
|---|---|---|---|
| **M0 — repository control plane** | Structure, AGENTS.md, indexes, CI skeleton, config scaffold | Agent can start at `REPO_INDEX.md`, locate any file, see deps/break risk, run `make check` | **done** |
| **M1 — research and factory specification** | Research ledger, process map, entity glossary, parameter register, assumptions register, external-data manifest, ADRs | Every modeled station has purpose, inputs, outputs, resources, state transitions, evidence, assumptions, open questions | **in progress** |
| **M2 — deterministic route** | Domain models, six stations, routing, genealogy, append-only events, invariant tests | Fixed-seed run completes; no illegal state transitions; complete part genealogy | todo |
| **M3 — stochastic process behavior** | Distributions, downtime, sensor noise, batch effects, defect risk, inspection outcomes, disposition | Multiple seeds vary while preserving invariants; metrics report uncertainty intervals | todo |
| **M4 — industrial transport** | MQTT publication, ingest worker, OPC UA adapter, raw+modeled stores | Equipment event travels adapter → broker → stores with provenance intact | todo |
| **M5 — external seed data** | C-MAPSS/UCI fetch scripts, checksums, licenses, isolated schemas | Clean-env fetch or clear unavailability report; no data mixing | deferred |
| **M6 — analytics + dashboard** | Production/WIP/quality/reliability marts; embedded dashboard; incident walkthrough | Reviewer follows one incident: degradation → excursion → affected serials → disposition → impact | todo |
| **M7 — OpenRouter layer** | Gateway, strict schemas, local validation | Runs with no key; malformed output rejected; no fact mutation | deferred |
| **M8 — industrial comparison** | UMH/Sparkplug/Redpanda comparison docs | Explains gained capability vs added complexity | deferred |

## Notes

- **M3 is critical path, not deferred.** A deterministic-only simulation produces identical output every run and contradicts the "realistic synthetic data" claim. Stochasticity is the product.
- M5, M7, M8 are enhancements. They do not block the portfolio demo (M6).
- Each milestone closes when its work orders (see `docs/work-orders.md`) meet acceptance criteria and `make check` is green.
