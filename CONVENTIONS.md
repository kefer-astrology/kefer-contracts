# Calculation conventions (normative, v0.1.0)

Both implementations — the Rust app (`tauri-application`, JPL/ANISE) and the
Python sidecar (`function-wrapper`, Skyfield) — must follow these rules. Each
rule is backed by a fixture in `contracts/`.

## 1. Time

- Event times are RFC 3339 with offset, or the legacy forms
  `YYYY-MM-DD[ HH:MM[:SS]]` / `YYYY-MM-DDTHH:MM:SS` interpreted as UTC.
  Grammar: `event-time.json`. (Rust also accepts the leap second `:60`;
  Python cannot represent it.)
- UT1 is taken equal to UTC (no ΔUT1 data). TT is derived from UTC with
  leap seconds. Results disclose this with
  `ut1_approximated_from_utc` (Rust).

## 2. Positions

- **Geocentric.** Topocentric values are only `altitude`/`azimuth`.
- **Apparent** (light-time, gravitational deflection, aberration) by default;
  `position_mode: geometric` disables corrections.
- **Ecliptic of date, mean equinox of date.** Longitude = true-equinox
  apparent longitude − nutation in longitude (IAU 2000A). This is exact (the
  mean and true equinox lie on the same ecliptic of date).
- These rules are the convention **`kefer-positions/1`** (`conventions.json`),
  the default. Every chart result reports `calculation_convention`.
- **`kefer-positions/1-true-equinox`** (implemented by both):
  the same inputs plus IAU 2000A nutation — longitudes + Δψ, RAMC + equation
  of the equinoxes (GAST), obliquity + Δε. Selected per chart with the config
  field `calculation_convention`; it moves longitudes by Δψ (≤ ~17″) and the
  ASC by up to ~32″. Right ascension/declination stay on the mean equator.
  Changing the *default* remains open decision D-CONV-1.
- An unknown or unimplemented convention id is computed with the default and
  reported as `calculation_convention_unsupported: <id>; kefer-positions/1_used`
  — never silently. Results always report the convention actually used.
- Accuracy against JPL Horizons (`reference/`): `reference/tolerances.json`,
  for the bodies listed per implementation in `capabilities.json`
  (`ephemeris_grade_bodies`). Other bodies must carry a warning.
- **Hypothetical bodies** (Uranian points) use fixed Keplerian elements in the
  format `schemas/points/hypothetical-bodies.schema.json`. The element values
  are a separate data pack, shipped by the implementation with its own
  provenance notice and **not** part of this package. The pack's `model` id
  names the element set, so a different set needs a new id.

## 3. Axes and houses

- RAMC = GMST (classic UT-based IAU formula; ≤ 0.15″ from IAU 2006 `gmst06`)
  + east longitude. Obliquity = IAU 2006 mean obliquity.
- ASC lies on the eastern horizon; MC on the upper meridian.
- Native house systems: Placidus, Whole Sign, Campanus, Equal, Porphyry.
  `houses/cusps.json` pins both implementations to 1e-9°;
  `tests/test_house_definitions.py` verifies the fixture against each
  system's geometric definition, independently of either implementation.
- Koch, Regiomontanus, Vehlow, Alcabitius: **Whole Sign substitute** with
  warning `house_system_<id>_not_yet_supported: whole_sign_used`.
  Placidus at |latitude| ≥ 90° − ε falls back with a warning.

## 4. Aspects

- Catalog: `catalogs/aspects.json` (24 canonical ids; aliases
  `semisquare`→`octile`, `sesquiquadrate`→`trioctile` accepted on read,
  canonical ids written).
- Separation = shortest arc in [0°, 180°]. An aspect matches when
  |separation − angle| ≤ orb (inclusive). The **first match in catalog
  order** wins. Orb precedence: operation > chart > preset > workspace >
  model default, with aliases resolved per layer.
- Chart aspects exclude the structurally locked pairs asc–desc, ic–mc,
  north_node–south_node. Cross (transit) aspects compare every transiting
  body with every transited body.
- Fixture: `aspects/detection.json`.

## 5. No silent substitution

Whenever an engine, house system, zodiac or body cannot be honoured exactly,
the result carries a warning from `substitution-warnings.json` or the
documented per-body codes (`<id>_unavailable`, `<id>_position_unreliable`,
`<id>_two_body_approximation`).

## 6. Capabilities

`capabilities.json` declares, per implementation, the conventions, native
and substituted house systems, engines, zodiac support, ephemeris-grade
bodies and optional features (aspect dynamics, event search, tradition
presets). Each implementation has a test that its declaration matches its
code; anything not declared must be rejected or warned about.

## 7. API

`schemas/api/chart-result.schema.json` defines the fields both
implementations return for a computed chart.

## 8. Versioning

- Semantic versioning of this repository (`VERSION`). A fixture change that
  alters an expected value or rule is a **minor** bump before 1.0 and must be
  implemented by both consumers in the same release train.
- `contracts/manifest.json` lists the SHA-256 of every file. Consumers vendor
  `contracts/` and verify it against the manifest of the pinned version.

## 9. Known issues (tracked, disclosed at runtime)

| Id | Implementation | Issue |
|---|---|---|
| KC-1 | Rust | **Resolved before 0.1.0 within 1900–2100**: asteroids 1–20 come from verified Horizons Type-13 kernels (J2000). Outside that range the legacy `codes_300ast` segments (frame `ECLIPJ2000_DE405`, not rotated by ANISE, up to ~3° off) remain a fallback disclosed as `<id>_position_unreliable`. |
| KC-2 | Python | Ceres, Pallas, Juno, Vesta and Chiron use two-body MPC elements: < 1′ near the element epoch, degrees decades away. Disclosed beyond 5 years. |
| KC-3 | Python | `applying`/`separating` in aspects are always `false` (not computed). |
| KC-4 | Python | No event search (stations, exact aspect times); transits are sampled series only. |
| KC-5 | Python | No tradition (school) presets; Rust only. |
