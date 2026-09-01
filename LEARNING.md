# Learning Guide — Crucible / Archify Foundry Twin

A teaching scope for understanding this project from first principles. Hand it to any tutor, LLM, or study partner to get real understanding instead of just watching agents build.

## Audience

A software engineer who knows code well but is new to manufacturing, industrial automation, and quality systems. The gap is the **domain**, not the code — this guide assumes strong programming ability and zero factory-floor experience.

## The goal

After working through this, you should be able to explain the project from first principles — not just describe what the code does, but justify *why* each architectural choice exists and *why the honest-claims boundary matters*:

1. Explain what investment casting is and why turbine blades are made that way.
2. Explain why a discrete-event simulation (not ML, not a dashboard) is the right source of truth.
3. Explain determinism vs. stochasticity and the replay invariant.
4. Explain material genealogy and why containment ("blast radius") matters in aerospace.
5. Explain ISA-95 levels and where MES/SCADA/historian sit.
6. Explain MQTT, OPC UA, MTConnect, Sparkplug — and why they exist instead of just REST.
7. Explain verification vs. validation vs. uncertainty quantification — and why this project can only claim the first.
8. Explain provenance: "was this measured, imported, derived, or generated?"
9. Explain what a digital twin actually is (vs. a dashboard) per NIST.
10. Explain equipment degradation, RUL, and why C-MAPSS is a behavioral reference, not foundry data.

## Teaching principles

- **Concept first, code second.** The learner already knows how to write software. Teach the domain; map it to concepts they know (event sourcing, append-only logs, idempotency, rebuildable views).
- **Use software analogies.** "Raw events are an append-only event log." "Modeled tables are a materialized view you can rebuild." "Genealogy is a DAG." "A quality hold is a state-machine guard."
- **Challenge the learner.** After each module, ask them to defend a design choice. If the answer is weak, say so.
- **Keep it tight.** Short sentences, no filler.
- **Prioritize the core ideas and the "why."** Skip exhaustive protocol trivia unless asked.

## Curriculum (in order)

### Module 1 — Investment casting (the physical process)
The lost-wax process: wax pattern → ceramic shell → dewax → melt → pour → directional solidification → knockout → heat treatment/HIP → machining → NDT → disposition.
- Why turbine blades: single-crystal / directional solidification, internal cooling channels, high-temperature alloys.
- Key terms: shell, mold, melt heat, HIP, NDT (FPI/RT/CT).
- **Check:** walk the 14-step line and say what each step produces.

### Module 2 — Discrete-event simulation (DES)
What DES is: entities, events, resources, queues, clock. Why it's the right model for a factory (limited-capacity resources interacting over time).
- SimPy concepts: processes, events, shared resources.
- Why DES beats a continuous model or a pure ML model here.
- **Check:** explain why "the simulation owns truth" is defensible.

### Module 3 — Determinism vs. stochasticity
Fixed seed + deterministic logic = reproducible. Stochastic distributions = realistic variation. The replay invariant: same seed + config = identical event stream.
- Why both are needed, and why a deterministic-only sim looks fake.
- **Check:** explain the replay invariant and why it matters for testing.

### Module 4 — Genealogy and traceability
Material genealogy: lot → serial lineage. Why aerospace tracks every part's history. Containment: when a deviation happens, which parts/lots are affected (the "blast radius").
- **Check:** explain why "every released part has complete genealogy" is an invariant.

### Module 5 — ISA-95 and the automation pyramid
Levels 0–4: physical process, sensing/actuation, supervisory control, MOM (MES/SCADA/historian/quality), business planning.
- Where this project's pieces map: simulated equipment ≈ L1–2, ingest ≈ historian, modeled records ≈ L3, BI ≈ L4.
- **Check:** place MES, SCADA, and historian on the pyramid.

### Module 6 — Industrial protocols
MQTT (pub/sub, topics, broker), OPC UA (information model, nodes, browse), MTConnect (read-only machine-tool data), Sparkplug (MQTT for IIoT).
- Why these exist instead of REST: publish/subscribe, real-time, standard information models, read-only safety.
- **Check:** say when to use each and why the adapter is "replaceable."

### Module 7 — Verification vs. validation vs. UQ
Verification: did the code implement the model correctly? Validation: does the model match reality? UQ: how sensitive to assumptions?
- Why this project can verify but not validate (no real factory data). The honest-claims boundary.
- **Check:** explain why "verified synthetic simulation" is the defensible claim, not "validated prediction."

### Module 8 — Provenance and data lineage
"Was this measured, imported, derived, or generated?" Append-only raw events, rebuildable modeled tables, disposable marts.
- Map to event sourcing and materialized views.
- **Check:** explain why raw events are immutable and modeled tables rebuildable.

### Module 9 — Digital twin (what it actually is)
NIST's definition: a twin is synchronized with an observable physical element. A synthetic twin without a physical factory is "verified simulation," not a "validated twin."
- Why "digital twin" is often marketing for "dashboard."
- **Check:** explain the difference between a twin and a dashboard.

### Module 10 — Equipment health and prognostics
Degradation, remaining useful life (RUL), run-to-failure, Weibull distributions.
- Why C-MAPSS (turbofan engine data) is a *behavioral* reference for a vacuum pump/furnace, not foundry data. The transformation layer.
- **Check:** explain why you can't copy aircraft sensor labels into a furnace schema.

## What "done" looks like

You can explain the whole project in your own words: what it is, why the architecture is what it is, what the honest claim is, and where each number traces back to. That is the actual understanding agents can't give you.
