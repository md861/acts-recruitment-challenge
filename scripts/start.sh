#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
RUN_DIR="$ROOT_DIR/.run"
GO_CACHE_DIR="$RUN_DIR/go-build-cache"
CLEANED_UP=0

mkdir -p "$RUN_DIR"

require_command() {
  if ! command -v "$1" >/dev/null 2>&1; then
    echo "Missing required command: $1"
    echo
    echo "Install the required tools, then run ./scripts/start.sh again."
    echo
    echo "macOS:"
    echo "  brew install python go node"
    echo
    echo "Ubuntu/Debian/WSL:"
    echo "  sudo apt update"
    echo "  sudo apt install -y python3 python3-venv curl ca-certificates golang-go"
    echo "  curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -"
    echo "  sudo apt install -y nodejs"
    echo
    echo "Check versions with:"
    echo "  python3 --version"
    echo "  go version"
    echo "  node --version"
    echo "  npm --version"
    exit 1
  fi
}

wait_for_url() {
  local name="$1"
  local url="$2"
  local attempts=40
  local count=0

  until python3 - "$url" >/dev/null 2>&1 <<'PY'
import sys
from urllib.request import urlopen

with urlopen(sys.argv[1], timeout=1) as response:
    if response.status >= 400:
        raise SystemExit(1)
PY
  do
    count=$((count + 1))
    if [ "$count" -ge "$attempts" ]; then
      echo "$name did not become ready at $url"
      echo "Logs are in $RUN_DIR"
      exit 1
    fi
    sleep 0.25
  done
}

check_port_free() {
  local name="$1"
  local port="$2"

  if ! python3 - "$port" >/dev/null 2>&1 <<'PY'
import socket
import sys

port = int(sys.argv[1])
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("127.0.0.1", port))
PY
  then
    echo "$name cannot start because port $port is already in use."
    echo
    echo "Stop the process using that port, then run ./scripts/start.sh again."
    echo "On macOS/Linux/WSL you can inspect listeners with:"
    echo "  lsof -nP -iTCP:$port -sTCP:LISTEN"
    exit 1
  fi
}

cleanup() {
  if [ "$CLEANED_UP" -eq 1 ]; then
    return
  fi
  CLEANED_UP=1

  echo
  echo "Stopping services..."
  stop_service "$RUN_DIR/frontend.pid"
  stop_service "$RUN_DIR/api.pid"
  stop_service "$RUN_DIR/model.pid"
  rm -f "$RUN_DIR/frontend.pid" "$RUN_DIR/api.pid" "$RUN_DIR/model.pid"
}

stop_service() {
  local pid_file="$1"
  if [ ! -f "$pid_file" ]; then
    return
  fi

  local pid
  pid="$(cat "$pid_file")"
  if [ -z "$pid" ]; then
    return
  fi

  kill_tree "$pid" TERM
  sleep 0.5
  if kill -0 "$pid" >/dev/null 2>&1; then
    kill_tree "$pid" KILL
  fi
}

kill_tree() {
  local pid="$1"
  local signal="$2"

  if command -v pgrep >/dev/null 2>&1; then
    local child
    for child in $(pgrep -P "$pid" 2>/dev/null || true); do
      kill_tree "$child" "$signal"
    done
  fi

  kill "-$signal" "$pid" >/dev/null 2>&1 || true
}

trap cleanup EXIT
trap 'cleanup; exit 130' INT
trap 'cleanup; exit 143' TERM

require_command python3
require_command go
require_command npm

check_port_free "Python model" 8001
check_port_free "Go API" 18080
check_port_free "React frontend" 5173

echo "Starting Python model..."
(
  cd "$ROOT_DIR/model-python"
  exec env SIM_TERRAIN_MAP_PATH="${SIM_TERRAIN_MAP_PATH:-Terrain maps/Terrain1.png}" python3 main.py >"$RUN_DIR/model.log" 2>&1
) &
echo $! > "$RUN_DIR/model.pid"
wait_for_url "Python model" "http://127.0.0.1:8001/health"

echo "Building Go API..."
(
  cd "$ROOT_DIR/api-go"
  GOCACHE="$GO_CACHE_DIR" go build -o "$RUN_DIR/acts-api" .
)

echo "Starting Go API..."
(
  exec env API_ADDR="127.0.0.1:18080" MODEL_BASE_URL="http://127.0.0.1:8001" "$RUN_DIR/acts-api" >"$RUN_DIR/api.log" 2>&1
) &
echo $! > "$RUN_DIR/api.pid"
wait_for_url "Go API" "http://127.0.0.1:18080/api/health"

echo "Preparing React frontend..."
(
  cd "$ROOT_DIR/frontend-react"
  if [ ! -d node_modules ]; then
    npm install
  fi
  exec ./node_modules/.bin/vite --host 127.0.0.1 --port 5173 >"$RUN_DIR/frontend.log" 2>&1
) &
echo $! > "$RUN_DIR/frontend.pid"
wait_for_url "React frontend" "http://127.0.0.1:5173"

echo
echo "Demo is running."
echo "Frontend: http://127.0.0.1:5173"
echo "API:      http://127.0.0.1:18080/api/snapshot"
echo "Model:    http://127.0.0.1:8001/snapshot"
echo
echo "Logs are in $RUN_DIR"
echo "Press Ctrl+C to stop."

while true; do
  sleep 1
  for pid_file in "$RUN_DIR/model.pid" "$RUN_DIR/api.pid" "$RUN_DIR/frontend.pid"; do
    pid="$(cat "$pid_file")"
    if ! kill -0 "$pid" >/dev/null 2>&1; then
      echo "A service exited unexpectedly. Logs are in $RUN_DIR"
      exit 1
    fi
  done
done
