# ACTS Recruitment Challenge

This repository contains a deliberately small proof-of-concept collective training simulation.

It is intended for take-home technical interviews across three role families:

- Modelling and Simulation Engineer
- Integration / Fullstack Software Engineer
- Platform Engineer

The demo has three parts:

- `model-python`: a simple Python population agent-based model.
- `api-go`: a Go integration API that talks to the model.
- `frontend-react`: a React UI that polls the API and renders agents on a 2D lattice.

The system is intentionally basic. It should run quickly, be easy to understand, and contain enough rough edges for candidates to improve in a focused one-day exercise.

## Quick Start

From the repository root:

```bash
./scripts/start.sh
```

Then open:

```text
http://localhost:5173
```

The script starts:

- Python model service on `http://localhost:8001`
- Go integration API on `http://localhost:18080`
- React frontend on `http://localhost:5173`

Press `Ctrl+C` in the terminal to stop all services.

## Requirements

The demo is intended to run on Linux, macOS, or Windows via WSL.

Use these versions or newer:

| Tool | Minimum | Notes |
| --- | ---: | --- |
| Python | 3.10 | The model uses only the Python standard library. |
| Go | 1.21 | The API uses only the Go standard library. |
| Node.js | 18 | Used by the React/Vite frontend. |
| npm | 9 | Installed with most Node.js distributions. |

The pack has been smoke-tested with Python 3.14 and Go 1.26. The frontend could not be smoke-tested on the author's machine because `npm` was not installed there, but it uses a standard Vite React setup.

Check your local versions:

```bash
python3 --version
go version
node --version
npm --version
```

## Installing Dependencies

### macOS

Install [Homebrew](https://brew.sh/) if you do not already have it, then run:

```bash
brew install python go node
```

### Ubuntu, Debian, or WSL

Install Python and basic tooling:

```bash
sudo apt update
sudo apt install -y python3 python3-venv curl ca-certificates
```

Install Go using either your package manager or the official Go packages. The package manager version may be older on some distributions:

```bash
sudo apt install -y golang-go
```

Install Node.js 20 LTS using NodeSource:

```bash
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs
```

### Other Linux Distributions

Use your distribution's package manager, or install from the official project pages:

- Python: <https://www.python.org/downloads/>
- Go: <https://go.dev/doc/install>
- Node.js: <https://nodejs.org/>

## Project Dependencies

The backend services do not need dependency installation beyond the tools above:

- `model-python` has no third-party Python packages.
- `api-go` has no third-party Go modules.

The frontend dependencies are declared in `frontend-react/package.json` and are installed automatically by `./scripts/start.sh` if `frontend-react/node_modules` is not present.

You can install them manually with:

```bash
cd frontend-react
npm install
```

## Useful Commands

Run all lightweight checks:

```bash
./scripts/test.sh
```

Create a source-only zip suitable for sending to a candidate:

```bash
./scripts/package-candidate.sh
```

This package excludes generated files and the internal assessment guide.

Create a local development zip of the full repository:

```bash
./scripts/package-challenge.sh
```

Create a zip of a completed candidate submission:

```bash
./scripts/package-submission.sh
```
