# kefer-contracts

Versioned public chart-result interface for Kefer Astrology. The draft
`0.1.0` package contains the [chart-result schema](contracts/schemas/api/chart-result.schema.json),
a [synthetic chart](contracts/examples/chart-result.json), [event-time examples](contracts/event-time.json)
and a [SHA-256 manifest](contracts/manifest.json).
[Conventions](CONVENTIONS.md) explains the units and coordinate frames.

Clients may read the JSON directly, use the embedded Rust constants, or load
files through the Python package. This package describes results and event
times. The desktop's native commands and workspace storage are versioned
with the application.

## Compatibility

This is the initial public interface for this repository. Clients can rely
on the documented chart-result fields and their units. Additional fields may
appear. Kefer's numerical verification is maintained separately.

## Checks

```sh
python -m unittest discover -s tests
python tools/build_manifest.py --check
cargo test
```

The full schema test requires the optional Python `test` extra. The license is
[MIT](LICENSE). See [licensing](LICENSING.md) for scope.
