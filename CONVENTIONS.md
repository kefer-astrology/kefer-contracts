# Interpreting Kefer chart results

Chart times are absolute instants. New clients should send RFC 3339
timestamps with an explicit offset or `Z`, including whole seconds.
Older inputs using `YYYY-MM-DD`, `YYYY-MM-DD HH:MM[:SS]` or
`YYYY-MM-DDTHH:MM:SS` without an offset are interpreted as UTC. See the
[event-time examples](contracts/event-time.json).

## Coordinates and units

- `positions` contains geocentric ecliptic longitudes by body identifier,
  expressed in degrees. A position can be a number or an object with
  a `longitude` field.
- `calculation_convention` identifies the coordinate convention used.
  `kefer-positions/1` uses the ecliptic and mean equinox of date.
  `kefer-positions/1-true-equinox` uses the ecliptic and true equinox of date.
  Handle unknown convention IDs explicitly before comparing coordinates.
- The standard chart uses apparent positions. A chart explicitly requested
  in geometric mode uses geometric positions. Compare only results from
  the same mode and convention.
- `motion` contains longitude speed in degrees per day and a retrograde flag.
- `axes`, `house_cusps`, and the aspect fields `angle`, `orb` and
  `exact_angle` use degrees. House cusps are in house order when supplied.
- Body IDs identify the same points across positions, motion and aspects.
  Accept new IDs and treat missing positions as unavailable.
- `fallback_used` and `warnings` are result diagnostics. Accept unfamiliar
  warning codes. Additional response fields are outside this public contract.

These conventions describe how to consume a result. Numerical conformance
fixtures and implementation parameters are maintained separately.
