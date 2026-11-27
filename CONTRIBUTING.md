# Contributing

Keep changes within the public chart-result and event-time interface.
Include synthetic examples where they clarify consumer behavior. Keep
implementation sources, internal fixtures and third-party datasets outside
the public package. A new public file requires an explicit review and an
update to the allowlist in `tools/build_manifest.py`.

Describe compatibility impact in `CHANGELOG.md`. Version changes require
matching package metadata and a regenerated manifest.

Contributions are accepted under MIT. Use `git commit -s` to certify the
[Developer Certificate of Origin](https://developercertificate.org/).
Disclose AI-generated material in the commit message with a
`Co-authored-by:` trailer.
