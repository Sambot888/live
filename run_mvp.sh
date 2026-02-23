#!/usr/bin/env bash
set -euo pipefail

MODE="${1:-free}"

if ! command -v python >/dev/null 2>&1; then
  echo "[ERROR] python not found in PATH"
  exit 1
fi

echo "[INFO] Running tests..."
python -m unittest discover -s tests

echo "[INFO] Starting bot in mode: ${MODE}"
python -m mvp_bot.main --mode "${MODE}"
