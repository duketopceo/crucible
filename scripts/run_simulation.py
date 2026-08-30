"""Placeholder run_simulation script.

Real implementation lands with WO-006 (M2): loads config profiles, runs the
SimPy engine with a fixed seed, writes run manifest + canonical events.
"""

from __future__ import annotations

import argparse


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run a Crucible simulation (M2, not yet implemented)"
    )
    parser.add_argument("--profile", default="baseline-v1")
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    print(f"[stub] simulation profile={args.profile} seed={args.seed} — implement in WO-006 (M2)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
