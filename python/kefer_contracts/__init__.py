"""Shared contracts for the Kefer Astrology calculation implementations.

`contracts_dir()` returns the directory holding the versioned contract files.
Files under `points/` are third-party-derived data and are not MIT-licensed;
see `points/NOTICE.md`.
"""

import json
from importlib import resources
from pathlib import Path

__version__ = "0.1.0"


def contracts_dir() -> Path:
    return Path(str(resources.files("kefer_contracts") / "data"))


def load(relative_path: str):
    return json.loads((contracts_dir() / relative_path).read_text(encoding="utf-8"))
