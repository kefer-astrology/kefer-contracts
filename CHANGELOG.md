# Changelog

## 0.1.0 — first official release (unreleased)

First published version. It consolidates the internal development
iterations recorded in Git history as "0.1.0", "0.2.0" and "0.3.0"; none of
them was tagged, published or consumed outside the project's own branches.

Contract versions that are independent of the package version are
unchanged: every file `schema_version` 1, aspect catalog `catalog_version`
1.0.0, convention ids `kefer-positions/1` and
`kefer-positions/1-true-equinox`.

### Behavioural contracts
- Event-time grammar, settings resolution, workspace YAML v1, substitution
  warnings (including `calculation_convention_unsupported`).
- Canonical aspect catalog 1.0.0 (24 aspects, Rust ids and default orbs,
  aliases `semisquare`/`sesquiquadrate`) and an aspect detection fixture
  (chart and cross cases, inclusive orb boundary, structurally locked pairs).

### Calculation conventions
- `conventions.json`: versioned conventions. `kefer-positions/1` (geocentric,
  apparent, ecliptic and mean equinox of date) is the default;
  `kefer-positions/1-true-equinox` (IAU 2000A nutation: longitudes + Δψ,
  RAMC + equation of the equinoxes, obliquity + Δε) is opt-in per chart.
  Both are implemented by Rust and Python. Chart results must report
  `calculation_convention`.
- `capabilities.json`: per-implementation declaration (conventions, houses,
  engines, zodiac, ephemeris-grade bodies, optional features).

### Fixtures and independent references
- House parity fixtures for the mean (9 systems × 4 sites) and true-equinox
  (9 systems × 2 sites × 6 epochs) conventions, each also verified against
  the system's geometric definition and ERFA GAST / obliquity.
- JPL Horizons apparent true-equinox positions for 31 bodies (Sun, Moon,
  planets, Pluto, Chiron, numbered asteroids 1–20) × 6 epochs 1950–2049
  (mean-equinox values follow by subtracting Δψ); ERFA earth orientation;
  USNO 2024 new/full moons; measured tolerances.
- JSON Schemas including the chart-result API; SHA-256 manifest; Rust crate
  and Python package for pinned consumption.

### Measured (arcsec vs JPL Horizons, mean equinox)
- Rust ≤ 1.5 for all 31 bodies; Python ≤ 0.8 for planets (Moon 6.7 in
  1950); axes ≤ 0.14 vs ERFA. True-equinox results meet the tolerances declared in
  `reference/tolerances.json`.

### Licensing
- Code and contract files MIT, except `contracts/points/` third-party data
  (see `LICENSING.md`).
- Hypothetical-body (Uranian) element values are **not included**. Their
  provenance is unresolved. The format is specified by
  `schemas/points/hypothetical-bodies.schema.json`, and implementations ship
  their own data pack. Support for hypothetical bodies is unchanged in the
  implementations.
