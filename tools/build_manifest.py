"""Write (or --check) contracts/manifest.json: version + SHA-256 of every contract file.

Consumers vendor the whole `contracts/` directory and verify it against this
manifest, so a vendored copy can never drift silently from a released version.
Standard library only.
"""

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTRACTS = ROOT / "contracts"
MANIFEST = CONTRACTS / "manifest.json"


def build() -> str:
    files = {}
    for path in sorted(p for p in CONTRACTS.rglob("*") if p.is_file() and p != MANIFEST):
        files[path.relative_to(CONTRACTS).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
    doc = {
        "name": "kefer-contracts",
        "version": (ROOT / "VERSION").read_text().strip(),
        "files": files,
    }
    return json.dumps(doc, indent=2) + "\n"


def main() -> int:
    content = build()
    if "--check" in sys.argv:
        if not MANIFEST.exists() or MANIFEST.read_text() != content:
            print("contracts/manifest.json is out of date; run python tools/build_manifest.py")
            return 1
        print("manifest up to date")
        return 0
    MANIFEST.write_text(content)
    print(f"wrote {MANIFEST} ({len(json.loads(content)['files'])} files)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
