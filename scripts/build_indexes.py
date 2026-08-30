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

# Files that never need index entries: package markers, generated lockfiles,
# and OS artifacts. Everything else must have an entry.
EXCLUDED = {
    ".gitkeep",
    ".DS_Store",
    "__init__.py",
    "uv.lock",
}

# GitHub UI metadata is not project content and is not hand-indexed.
EXCLUDED_PATHS = {
    ".github/PULL_REQUEST_TEMPLATE.md",
}
EXCLUDED_PREFIXES = (".github/ISSUE_TEMPLATE/",)


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
    missing = []
    for p in tracked_files():
        rel = str(p.relative_to(REPO_ROOT))
        if p.name in EXCLUDED:
            continue
        if rel in EXCLUDED_PATHS or rel.startswith(EXCLUDED_PREFIXES):
            continue
        if rel not in indexed:
            missing.append(rel)

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
