"""Public chart-result contracts for Kefer Astrology.

`contracts_dir()` returns the directory holding the versioned contract files.
"""

import json
from importlib import resources
from pathlib import Path

__version__ = "0.1.0"


def contracts_dir() -> Path:
    return Path(str(resources.files("kefer_contracts") / "data"))


def load(relative_path: str):
    return json.loads((contracts_dir() / relative_path).read_text(encoding="utf-8"))
