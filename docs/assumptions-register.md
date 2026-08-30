# Assumptions Register

Every numeric parameter in `config/` must appear here with a tag:

| Tag | Meaning |
|---|---|
| `source_backed` | directly supported by a cited public source |
| `derived` | transparent transformation of a source-backed quantity |
| `assumption` | selected by the project to create a useful test case |
| `sensitivity_only` | intentionally varied to study model behavior |
| `unvalidated` | not checked against any physical factory data |

## Register

| ID | Parameter | Value | Tag | Rationale / citation | Set in |
|---|---|---|---|---|---|
| — | (none yet — populated in M2 when `config/factory.yaml` gains numeric parameters) | | | | |

## Open questions

- Which reliability distribution (Weibull shape) best represents gradual pump degradation for the M3 health model? (C-MAPSS-derived, M5.)
- Batch-effect magnitude for shell building — needs a `sensitivity_only` sweep definition.
