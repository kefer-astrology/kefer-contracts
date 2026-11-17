# Contributing

## Rules for contract changes

1. Every rule in `CONVENTIONS.md` must be backed by a fixture, and every
   fixture by a test in this repository.
2. A change to an expected value is a contract change: bump `VERSION`
   (minor before 1.0), add a `CHANGELOG.md` entry, run
   `python tools/build_manifest.py`, and land matching changes in both
   implementations before they pin the new version.
3. Reference data (`contracts/reference/`) is regenerated only with
   `tools/fetch_references.py`; record the retrieval date.
4. Parity fixtures (e.g. `houses/cusps.json`) must also be verified by an
   independent check (definition-based test or external reference).

## Licensing of contributions

- Contributions are accepted under the MIT License (inbound = outbound).
- Sign off every commit (`git commit -s`) to certify the
  [Developer Certificate of Origin](https://developercertificate.org/).
- Do not add third-party code or data without recording its source and
  license in `LICENSING.md` / a `NOTICE.md`. Never add GPL/AGPL material,
  Swiss Ephemeris code or data, or texts without redistribution rights.
- Disclose AI-generated material in the commit message
  (`Co-authored-by:` trailer).
- A contributor agreement for the Kefer Astrology nonprofit is being drafted
  (`governance/CONTRIBUTOR-AGREEMENT-DRAFT.md`); it is **not in effect** yet.
