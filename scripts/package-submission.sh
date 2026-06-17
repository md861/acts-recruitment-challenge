#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT_DIR="$ROOT_DIR/dist"
NAME="acts-recruitment-submission"

mkdir -p "$OUT_DIR"

if command -v zip >/dev/null 2>&1; then
  (
    cd "$ROOT_DIR"
    zip -qr "$OUT_DIR/$NAME.zip" . \
      -x ".git/*" \
      -x ".run/*" \
      -x "dist/*" \
      -x "frontend-react/dist/*" \
      -x "**/__pycache__/*" \
      -x ".pytest_cache/*" \
      -x "frontend-react/node_modules/*"
  )
  echo "Created $OUT_DIR/$NAME.zip"
else
  (
    cd "$ROOT_DIR"
    tar \
      --exclude=".git" \
      --exclude=".run" \
      --exclude="dist" \
      --exclude="frontend-react/dist" \
      --exclude="**/__pycache__" \
      --exclude=".pytest_cache" \
      --exclude="frontend-react/node_modules" \
      -czf "$OUT_DIR/$NAME.tar.gz" .
  )
  echo "Created $OUT_DIR/$NAME.tar.gz"
fi
