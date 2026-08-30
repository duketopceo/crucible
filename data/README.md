# data/

| Directory | Contents | Committed? |
|---|---|---|
| `external/` | Downloaded public datasets (C-MAPSS, UCI Steel Plates — M5, deferred) | **No** — fetched via `scripts/fetch_external_data.py` with checksums + license records |
| `raw/` | Simulation run outputs (canonical event streams, run manifests) | **No** — regenerable from seed + config; keep only locally for analysis |

Both are regenerable. Nothing in here is source of truth; the source of truth is
code + `config/` + the recorded seed.
