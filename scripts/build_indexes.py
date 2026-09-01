#!/usr/bin/env python3
"""Build/verify index/FILE_INDEX.yaml freshness.

M0: verifies every tracked file has an index entry and prints missing ones.
The full generator (auto-writing entries) lands with a later WO; until then
entries are maintained by hand and this script acts as the CI gate.

Usage:
    python scripts/build_indexes.py           # report missing entries
    python scripts/build_indexes.py --verify  # exit 1 if any file lacks an entry
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
INDEX_PATH = REPO_ROOT / "index" / "FILE_INDEX.yaml"

# Files that never need index entries: VCS metadata, empty package markers,
# lockfiles, and other regenerated artifacts.
EXCLUDED_NAMES = {
    ".gitkeep",
    ".DS_Store",
    "__init__.py",
    "uv.lock",
}
EXCLUDED_PREFIXES = (
    ".github/",
)


def tracked_files() -> list[Path]:
    out = subprocess.run(
        ["git", "ls-files"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    return [REPO_ROOT / line for line in out.stdout.splitlines() if line.strip()]


def indexed_paths() -> set[str]:
    with INDEX_PATH.open() as f:
        data = yaml.safe_load(f)
    return {entry["path"] for entry in data.get("entries", [])}


def main() -> int:
    verify = "--verify" in sys.argv

    if not INDEX_PATH.exists():
        print(f"FAIL: {INDEX_PATH} missing")
        return 1

    indexed = indexed_paths()
    missing = [
        str(p.relative_to(REPO_ROOT))
        for p in tracked_files()
        if p.name not in EXCLUDED_NAMES
        and not str(p.relative_to(REPO_ROOT)).startswith(EXCLUDED_PREFIXES)
        and str(p.relative_to(REPO_ROOT)) not in indexed
    ]

    if missing:
        print(f"Missing index entries ({len(missing)}):")
        for path in sorted(missing):
            print(f"  - {path}")
        if verify:
            return 1
    else:
        print("OK: all tracked files indexed")

    return 0


if __name__ == "__main__":
    sys.exit(main())
