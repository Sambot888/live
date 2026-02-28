#!/usr/bin/env python3
"""Configure GitHub remote for this repo and print next push command.

Usage:
  python setup_github_remote.py
  python setup_github_remote.py --username Sambot888 --repo live --branch work
  python setup_github_remote.py --branch main --set-main
"""

from __future__ import annotations

import argparse
import subprocess
import sys


def run(cmd: list[str]) -> int:
    print("[INFO] $", " ".join(cmd))
    return subprocess.call(cmd)


def git_output(cmd: list[str]) -> str:
    return subprocess.check_output(cmd, text=True).strip()


def main() -> int:
    parser = argparse.ArgumentParser(description="Setup GitHub origin remote")
    parser.add_argument("--username", default="Sambot888")
    parser.add_argument("--repo", default="live")
    parser.add_argument("--branch", default="work")
    parser.add_argument("--set-main", action="store_true", help="Rename current branch to main before push")
    args = parser.parse_args()

    remote_url = f"https://github.com/{args.username}/{args.repo}.git"

    remotes = git_output(["git", "remote"]).splitlines()
    if "origin" in remotes:
        code = run(["git", "remote", "set-url", "origin", remote_url])
    else:
        code = run(["git", "remote", "add", "origin", remote_url])
    if code != 0:
        return code

    branch = args.branch
    if args.set_main:
        code = run(["git", "branch", "-M", "main"])
        if code != 0:
            return code
        branch = "main"

    print("[DONE] Remote configured:", remote_url)
    print("[NEXT] Push with:")
    print(f"git push -u origin {branch}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
