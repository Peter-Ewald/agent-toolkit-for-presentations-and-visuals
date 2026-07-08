#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

uv sync
uv run playwright install chromium

echo "Setup complete: uv sync + Chromium installed for diagram-excalidraw."
