"""Placeholder validate_run script.

Real implementation lands with WO-005/WO-006 (M2): replays a run from its
manifest (same seed + config) and asserts the canonical event stream is
byte-identical, then runs invariant checks over the raw event log.
"""

from __future__ import annotations

import argparse


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate a simulation run (M2, not yet implemented)"
    )
    parser.add_argument("--replay-check", action="store_true")
    parser.parse_args()
    print("[stub] replay/invariant validation — implement in WO-005/WO-006 (M2)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
