"""Validate the public package without depending on implementation fixtures."""

import json
import subprocess
import sys
import tomllib
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def read_json(path):
    return json.loads((ROOT / "contracts" / path).read_text())


class PublicContractsTests(unittest.TestCase):
    def test_public_manifest_and_file_allowlist(self):
        subprocess.run(
            [sys.executable, str(ROOT / "tools/build_manifest.py"), "--check"],
            check=True,
        )

    def test_package_versions_match(self):
        version = (ROOT / "VERSION").read_text().strip()
        self.assertEqual(read_json("manifest.json")["version"], version)
        for name, section in (("Cargo.toml", "package"), ("pyproject.toml", "project")):
            metadata = tomllib.loads((ROOT / name).read_text())
            self.assertEqual(metadata[section]["version"], version)

    def test_chart_example_and_extension_compatibility(self):
        try:
            from jsonschema import Draft202012Validator, ValidationError
        except ImportError:
            self.skipTest("jsonschema unavailable")
        schema = read_json("schemas/api/chart-result.schema.json")
        Draft202012Validator.check_schema(schema)
        validate = Draft202012Validator(schema).validate
        example = read_json("examples/chart-result.json")
        validate(example)
        validate({**example, "extension": {"value": "synthetic"}})
        with self.assertRaisesRegex(ValidationError, "calculation_convention"):
            validate({key: value for key, value in example.items()
                      if key != "calculation_convention"})


if __name__ == "__main__":
    unittest.main()
