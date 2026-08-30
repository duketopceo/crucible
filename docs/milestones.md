# Milestones

| Milestone | Scope | Acceptance | Status |
|---|---|---|---|
| **M0 — repo control plane** | Structure, AGENTS.md, indexes, CI skeleton, config scaffold | Agent can start at REPO_INDEX.md, locate any file, see deps/break risk, run `make check` | **done** |
| **M2 — deterministic route** | Domain models, six stations, routing, genealogy, append-only events, invariants | Fixed-seed run completes; no illegal state transitions; complete part genealogy | todo |
| **M4 — industrial transport** | MQTT pub, ingest worker, OPC UA adapter, raw+modeled stores | Equipment event travels adapter → broker → stores with provenance intact | todo |
| **M6 — analytics + dashboard** | Production/WIP/quality/reliability marts; embedded dashboard; incident walkthrough | Reviewer follows one incident: degradation → excursion → affected serials → disposition → impact | todo |
| M3 — stochastic behavior (deferred) | Distributions, downtime, noise, batch effects, defect risk | Variation across seeds while preserving invariants; uncertainty intervals | deferred |
| M5 — external seed data (deferred) | C-MAPSS/UCI fetch scripts, checksums, licenses, isolated schemas | Clean env fetch or clearly report unavailability; no data mixing | deferred |
| M7 — OpenRouter layer (deferred) | Gateway, strict schemas, local validation | Runs with no key; malformed output rejected; no fact mutation | deferred |
| M8 — industrial comparison (deferred) | UMH/Sparkplug/Redpanda comparison docs | Explains gained capability vs added complexity | deferred |
