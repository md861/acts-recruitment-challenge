#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT_DIR="$ROOT_DIR/dist"
NAME="acts-recruitment-challenge"

mkdir -p "$OUT_DIR"

if command -v zip >/dev/null 2>&1; then
  (
    cd "$(dirname "$ROOT_DIR")"
    zip -qr "$OUT_DIR/$NAME.zip" "$NAME" \
      -x "$NAME/.git/*" \
      -x "$NAME/.run/*" \
      -x "$NAME/dist/*" \
      -x "$NAME/frontend-react/dist/*" \
      -x "$NAME/**/__pycache__/*" \
      -x "$NAME/.pytest_cache/*" \
      -x "$NAME/frontend-react/node_modules/*"
  )
  echo "Created $OUT_DIR/$NAME.zip"
else
  (
    cd "$(dirname "$ROOT_DIR")"
    tar \
      --exclude="$NAME/.git" \
      --exclude="$NAME/.run" \
      --exclude="$NAME/dist" \
      --exclude="$NAME/frontend-react/dist" \
      --exclude="$NAME/**/__pycache__" \
      --exclude="$NAME/.pytest_cache" \
      --exclude="$NAME/frontend-react/node_modules" \
      -czf "$OUT_DIR/$NAME.tar.gz" "$NAME"
  )
  echo "Created $OUT_DIR/$NAME.tar.gz"
fi
