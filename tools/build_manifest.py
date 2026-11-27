"""Generate and verify the manifest for the public contract snapshot."""

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTRACTS = ROOT / "contracts"
MANIFEST = CONTRACTS / "manifest.json"
PUBLIC_CONTRACTS = {
    "event-time.json",
    "examples/chart-result.json",
    "schemas/api/chart-result.schema.json",
}
PUBLIC_REPOSITORY_FILES = {
    ".github/workflows/ci.yml",
    ".gitignore",
    "CHANGELOG.md",
    "CONTRIBUTING.md",
    "CONVENTIONS.md",
    "Cargo.toml",
    "LICENSE",
    "LICENSING.md",
    "README.md",
    "VERSION",
    "contracts/manifest.json",
    "pyproject.toml",
    "python/kefer_contracts/__init__.py",
    "src/lib.rs",
    "tests/__init__.py",
    "tests/test_contracts.py",
    "tools/build_manifest.py",
} | {f"contracts/{name}" for name in PUBLIC_CONTRACTS}


def require_exact_paths(label, actual, expected):
    missing = sorted(expected - actual)
    extra = sorted(actual - expected)
    if missing or extra:
        raise ValueError(f"{label}: missing={missing}, unexpected={extra}")


def build():
    files = {
        path.relative_to(CONTRACTS).as_posix()
        for path in CONTRACTS.rglob("*")
        if path != MANIFEST and (path.is_file() or path.is_symlink())
    }
    require_exact_paths("public contract files", files, PUBLIC_CONTRACTS)
    for path in [CONTRACTS / name for name in files] + [MANIFEST]:
        if path.is_symlink():
            raise ValueError(f"public contract paths cannot be symbolic links: {path}")
    document = {
        "name": "kefer-contracts",
        "version": (ROOT / "VERSION").read_text().strip(),
        "files": {
            name: hashlib.sha256((CONTRACTS / name).read_bytes()).hexdigest()
            for name in sorted(files)
        },
    }
    return json.dumps(document, indent=2) + "\n"


def check_tracked_files():
    tracked = subprocess.check_output(
        ["git", "ls-files", "--cached", "-z"], cwd=ROOT, text=True
    )
    require_exact_paths("tracked public files", set(tracked.rstrip("\0").split("\0")),
                        PUBLIC_REPOSITORY_FILES)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    try:
        content = build()
        if args.check:
            if not MANIFEST.is_file() or MANIFEST.read_text() != content:
                raise ValueError("public manifest is out of date")
            if (ROOT / ".git").exists():
                check_tracked_files()
        else:
            MANIFEST.write_text(content)
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        parser.exit(1, f"{error}\n")
    print("Public contract manifest verified" if args.check else "Public contract manifest updated")


if __name__ == "__main__":
    main()
