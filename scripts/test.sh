#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
RUN_DIR="$ROOT_DIR/.run"
GO_CACHE_DIR="$RUN_DIR/go-build-cache"

mkdir -p "$GO_CACHE_DIR"

require_command() {
  if ! command -v "$1" >/dev/null 2>&1; then
    echo "Missing required command: $1"
    echo
    echo "Install dependencies first. See README.md for macOS, Linux, and WSL instructions."
    exit 1
  fi
}

require_command python3
require_command go
require_command npm

echo "Running Python tests..."
(
  cd "$ROOT_DIR"
  PYTHONPATH="$ROOT_DIR/model-python" python3 -m unittest discover -s model-python/tests
)

echo "Running Go tests..."
(
  cd "$ROOT_DIR/api-go"
  GOCACHE="$GO_CACHE_DIR" go test ./...
)

echo "Running frontend typecheck..."
(
  cd "$ROOT_DIR/frontend-react"
  if [ ! -d node_modules ]; then
    npm install
  fi
  npm run test
)

echo "All checks passed."
