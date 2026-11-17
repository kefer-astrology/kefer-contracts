# kefer-contracts

Shared, language-neutral contracts for the Kefer Astrology calculation
implementations:

- **tauri-application** — Rust (JPL/ANISE), MIT
- **function-wrapper** — Python (Skyfield), independent implementation

Both implementations must reproduce the fixtures in `contracts/` within the
tolerances in `contracts/reference/tolerances.json`.

## Contents

| Path | What |
|---|---|
| `CONVENTIONS.md` | Normative calculation conventions (time, frames, houses, aspects, warnings) |
| `contracts/conventions.json` | Versioned calculation conventions (default `kefer-positions/1`) |
| `contracts/capabilities.json` | What each implementation supports (tested by each implementation) |
| `contracts/catalogs/` | Canonical catalogs (aspects, with aliases) |
| `contracts/houses/`, `contracts/aspects/` | Parity fixtures (exact expected outputs), incl. `houses/cusps-true-equinox.json` |
| `contracts/reference/` | Independent references: JPL Horizons positions, ERFA earth orientation, USNO moon phases, tolerances |
| `contracts/event-time.json`, `settings-resolution.json`, `substitution-warnings.json`, `workspace-v1/` | Behavioural contracts |
| `contracts/schemas/` | JSON Schemas (Draft 2020-12), incl. the chart-result API and the hypothetical-body data-pack format |
| `contracts/points/` | Third-party-derived data — **not MIT**, see its `NOTICE.md` |
| `contracts/manifest.json` | Version + SHA-256 of every file |
| `tools/` | Manifest builder, aspect-fixture generator, reference fetcher |

## Consuming a pinned version

Both consumers keep their own pinned copy so builds stay offline:

- **Rust**: `tauri-application/contracts/` is a verified copy of this
  repository's `contracts/` at the version in `contracts/manifest.json`; a
  Rust test checks every file hash. Alternatively depend on the crate in this
  repository (`Cargo.toml`, files exposed via `include_str!`).
- **Python**: `function-wrapper` tests read `KEFER_CONTRACTS_DIR` (CI checks
  out this repository at the tag pinned in `kefer-contracts.lock`) and verify
  the manifest. Alternatively install the `kefer-contracts` Python package
  (`pyproject.toml`).

## Development

```bash
python -m unittest discover -s tests      # integrity + independent house checks
python tools/build_manifest.py            # after changing anything in contracts/
python tools/generate_aspect_fixture.py   # after changing the catalog or rule
python tools/fetch_references.py contracts/reference-fetch  # needs network + pyerfa
```

## License

MIT for project-owned material; see `LICENSING.md` for the exceptions.
