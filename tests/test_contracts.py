"""Integrity tests for the kefer-contracts package (standard library + optional jsonschema)."""

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTRACTS = ROOT / "contracts"
SCHEMA_FOR = {
    "catalogs/aspects.json": "catalogs/aspects.schema.json",
    "houses/cusps.json": "houses/cusps.schema.json",
    "houses/cusps-true-equinox.json": "houses/cusps.schema.json",
    "aspects/detection.json": "aspects/detection.schema.json",
    "event-time.json": "event-time.schema.json",
    "substitution-warnings.json": "substitution-warnings.schema.json",
    "reference/positions-horizons.json": "reference/positions-horizons.schema.json",
    "reference/tolerances.json": "reference/tolerances.schema.json",
    "conventions.json": "conventions.schema.json",
    "capabilities.json": "capabilities.schema.json",
}

try:
    import jsonschema  # optional; CI installs it
except ImportError:  # pragma: no cover
    jsonschema = None


def load(rel):
    return json.loads((CONTRACTS / rel).read_text(encoding="utf-8"))


class ContractIntegrityTests(unittest.TestCase):
    def test_every_json_file_parses(self):
        for path in CONTRACTS.rglob("*.json"):
            with self.subTest(path=path.relative_to(ROOT)):
                json.loads(path.read_text(encoding="utf-8"))

    def test_fixtures_match_their_schemas(self):
        for data_rel, schema_rel in SCHEMA_FOR.items():
            with self.subTest(fixture=data_rel):
                data, schema = load(data_rel), load(f"schemas/{schema_rel}")
                if jsonschema is not None:
                    jsonschema.Draft202012Validator(schema).validate(data)
                else:
                    for key in schema.get("required", []):
                        self.assertIn(key, data)

    def test_aspect_catalog_integrity(self):
        catalog = load("catalogs/aspects.json")
        ids = [a["id"] for a in catalog["aspects"]]
        self.assertEqual(len(ids), len(set(ids)))
        for aspect in catalog["aspects"]:
            if "angle_expression" in aspect:
                # Expressions are plain arithmetic such as "360.0 / 11.0".
                self.assertEqual(eval(aspect["angle_expression"], {"__builtins__": {}}), aspect["angle"])
        for alias, target in catalog["aliases"].items():
            self.assertNotIn(alias, ids)
            self.assertIn(target, ids)

    def test_aspect_detection_fixture_is_reproducible(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / "tools/generate_aspect_fixture.py")],
            capture_output=True, text=True, cwd=ROOT,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        diff = subprocess.run(["git", "diff", "--exit-code", "--", "contracts/aspects/detection.json"],
                              cwd=ROOT, capture_output=True, text=True)
        if diff.returncode not in (0, 1):  # not a git checkout: nothing to compare
            self.skipTest("not a git checkout")
        self.assertEqual(diff.returncode, 0, "detection.json changed when regenerated:\n" + diff.stdout[:2000])

    def test_manifest_is_current(self):
        result = subprocess.run([sys.executable, str(ROOT / "tools/build_manifest.py"), "--check"],
                                capture_output=True, text=True, cwd=ROOT)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_reference_fixtures_are_aligned(self):
        horizons = load("reference/positions-horizons.json")
        erfa = load("reference/earth-orientation-erfa.json")["epochs"]
        self.assertEqual([e["utc"] for e in erfa], horizons["epochs_utc"])
        for body, rows in horizons["positions"].items():
            self.assertEqual(len(rows), len(horizons["epochs_utc"]), body)
        capabilities = load("capabilities.json")
        for name, impl in capabilities["implementations"].items():
            for body in impl["ephemeris_grade_bodies"]:
                self.assertIn(body, horizons["positions"], f"{name}: {body} has no reference")

    def test_conventions_and_capabilities_are_consistent(self):
        conventions = load("conventions.json")
        self.assertIn(conventions["default"], conventions["conventions"])
        implemented = {cid for cid, c in conventions["conventions"].items() if c["status"] == "implemented"}
        for name, impl in load("capabilities.json")["implementations"].items():
            for cid in impl["conventions"]:
                self.assertIn(cid, implemented, name)
                self.assertIn(name, conventions["conventions"][cid]["implemented_by"])
            houses = load("houses/cusps.json")["cases"][0]["systems"]
            self.assertEqual(set(impl["house_systems_native"]) | set(impl["house_systems_substituted"]), set(houses), name)

    def test_third_party_data_carries_a_notice(self):
        notice = (CONTRACTS / "points/NOTICE.md").read_text(encoding="utf-8")
        for name in ("fixed-stars.json", "arabic-lots.json"):
            self.assertIn(name, notice)
        for path in (CONTRACTS / "points").glob("*.json"):
            self.assertIn(path.name, notice, "every third-party data file needs a notice row")
        self.assertIn("reference/", (ROOT / "LICENSING.md").read_text(encoding="utf-8"))


class HypotheticalBodyFormatTests(unittest.TestCase):
    """The element format is a contract; the element values are not shipped here."""

    SYNTHETIC = {  # invented values: tests the format only
        "schema_version": 1, "source": "synthetic test data", "source_url": "",
        "model": "synthetic-test-v1",
        "bodies": [{"id": "testbody", "name": "Test body", "epoch_jd": 2451545.0,
                    "equinox_jd": 2451545.0, "mean_anomaly_deg": 10.0, "semimajor_axis_au": 42.0,
                    "eccentricity": 0.01, "argument_perihelion_deg": 20.0,
                    "ascending_node_deg": 30.0, "inclination_deg": 1.0}],
    }

    def test_element_values_are_not_distributed(self):
        self.assertFalse((CONTRACTS / "points/hypothetical-bodies.json").exists())

    def test_schema_accepts_a_valid_pack_and_rejects_invalid_ones(self):
        schema = load("schemas/points/hypothetical-bodies.schema.json")
        if jsonschema is None:
            self.skipTest("jsonschema not installed")
        validator = jsonschema.Draft202012Validator(schema)
        validator.validate(self.SYNTHETIC)
        bad = json.loads(json.dumps(self.SYNTHETIC))
        bad["bodies"][0]["eccentricity"] = 1.0
        self.assertFalse(validator.is_valid(bad))
        bad = json.loads(json.dumps(self.SYNTHETIC))
        bad["bodies"][0]["unknown_field"] = 1
        self.assertFalse(validator.is_valid(bad))


if __name__ == "__main__":
    unittest.main()
