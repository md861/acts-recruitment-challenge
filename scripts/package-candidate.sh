#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT_DIR="$ROOT_DIR/dist"
PACKAGE_NAME="acts-recruitment-challenge"
OUTPUT="$OUT_DIR/$PACKAGE_NAME-candidate.zip"

mkdir -p "$OUT_DIR"

if ! command -v git >/dev/null 2>&1; then
  echo "Missing required command: git"
  exit 1
fi

if ! git -C "$ROOT_DIR" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "This script must be run from a git checkout of the challenge repository."
  exit 1
fi

git -C "$ROOT_DIR" archive \
  --format=zip \
  --output="$OUTPUT" \
  --prefix="$PACKAGE_NAME/" \
  HEAD \
  -- . ":(exclude)ASSESSMENT_GUIDE.md"

echo "Created $OUTPUT"

