# Crucible design direction: "Heat Log"

Status: proposal; the owner signs off. Crucible has no UI yet. This direction governs the README, docs, the future M6 dashboard and CLI output.

## Reference lock and decision ledger
The refero-design skill was not run (docs-stage repo; no live reference tooling used). Decisions are reasoned from the product instead:

| Decision | Reason |
|---|---|
| Warm bone paper, ink text, one ember accent | Investment-casting heat and a printed traveller/lab-notebook feel; avoids generic blue SaaS. |
| Monospace for ids, serials, seeds, timestamps | Traceability is the product; identifiers must align and be copyable. |
| One accent colour, used only for "heat" (melt, active, selected) | Colour carries state, not decoration. |
| Provenance chip on every figure | Rule 2: every number traceable to event, model version and seed. |

## Tokens (WCAG AA checked, ratios computed)

| Token | Light | Dark | Contrast |
|---|---|---|---|
| surface | `#F6F1EA` | `#16120F` | |
| ink | `#1C1917` | `#F6F1EA` | 15.6 / 16.6 |
| muted | `#5C5249` | `#B8A99A` | 6.8 / 8.1 |
| ember (accent, text) | `#B8410A` | `#FF8A4C` | 4.9 / 8.0 |
| on-ember | `#FFFFFF` | `#16120F` | 5.5 / 8.0 |
| chill (secondary, links) | `#2F6F8F` | `#6FB6D6` | 4.9 / 8.3 |

Ratios are against the surface. Ember on light is 4.9, so use it for text of 14 px and up only.

## Type
- Display and data: system monospace stack (`ui-monospace, "JetBrains Mono", "Liberation Mono", monospace`), weight 700 for headings, 400 for data.
- Prose: system sans, 16 px/1.6, measure 70 characters.
- Scale: 12, 14, 16, 20, 28, 40.

## Glyphs and motion
- Glyphs: 24 px grid, filled geometric shapes, 2 px minimum feature, no outlines or gradients; same construction as the mark.
- Motion: only to show a state change (a record being appended, a serial being traced). 150 ms ease-out, no looping or decorative animation, none under `prefers-reduced-motion`.

## Surfaces
- README and docs: logo at top, tokens via GitHub's light/dark `<picture>`.
- CLI (`make simulate`, `validate_run`): plain text, ids in monospace columns, ember only for failures of invariants, no emoji.
- M6 dashboard (planned): the four views in ROADMAP (factory map, operations, quality and containment, evidence and provenance); click-through from incident to serial; keyboard-reachable drill-down; visible 2 px ember focus ring.
- Empty/error states: say what is missing and which milestone produces it.

## Logo
See `assets/brand/README.md`. Proposal, owner signs off.
