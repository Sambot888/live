#!/usr/bin/env python3
"""One-click runner for the MVP bot.

Usage:
  python run_mvp.py
  python run_mvp.py --mode mock
  python run_mvp.py --mode http --skip-tests
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def run_step(cmd: list[str]) -> int:
    print(f"[INFO] $ {' '.join(cmd)}")
    return subprocess.call(cmd, cwd=ROOT)


def main() -> int:
    parser = argparse.ArgumentParser(description="One-click MVP runner")
    parser.add_argument("--mode", choices=["free", "mock", "http"], default="free")
    parser.add_argument("--skip-tests", action="store_true", help="Skip unit tests before start")
    args = parser.parse_args()

    python_bin = sys.executable

    if not args.skip_tests:
        code = run_step([python_bin, "-m", "unittest", "discover", "-s", "tests"])
        if code != 0:
            print("[ERROR] Tests failed; aborting start.")
            return code

    code = run_step([python_bin, "-m", "mvp_bot.main", "--mode", args.mode])
    if code != 0:
        print("[ERROR] Bot failed.")
        return code

    print("[DONE]")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
