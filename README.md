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

## Roadmap

Track A modelling work has been selected for this repository. The detailed implementation reference is [MODEL_MODULARIZATION_BLUEPRINT.md](./MODEL_MODULARIZATION_BLUEPRINT.md); this section keeps the current roadmap visible from the GitHub README.

### Completed

1. Baseline project orientation and verification.
   - The existing Python model, Go API, React frontend, scripts, and tests have been inspected.
   - Local project-scoped Go and Node tooling is available under ignored `.tools/`.
   - The baseline check script has passed with the local toolchain.

2. Project bookkeeping and handover setup.
   - `project_lab-book.md`, `AI_USAGE_lab-book.md`, `Changes.md`, and `HANDOVER.md` are maintained as running project records.
   - Commit/push protocol is documented in the handover file.

3. Track A blueprint created.
   - `MODEL_MODULARIZATION_BLUEPRINT.md` captures the target modular architecture.
   - The selected scope includes terrain handling, agent creation/behaviour, movement strategy selection, random walk policies, metrics, and frontend terrain visualization.

4. Terrain map asset and legend documented.
   - `Terrain maps/Terrain1.png` is tracked as the current terrain input asset.
   - The terrain legend is documented: white normal, black hard boundary, red restricted, orange max-density gate, green exit/removal, blue Type 1 penalty, and pink Type 2 penalty.

### Active

1. Implement the terrain map handler.
   - Add symbolic terrain cell vocabulary.
   - Add configuration for selected terrain map, restricted ids, exit ids, gate capacity, and Type 1 penalty settings.
   - Load/select `Terrain maps/Terrain1.png`.
   - Parse white, black, red, orange, green, blue, and pink cells into terrain definitions.
   - Treat white cells as normal cells with no special restrictions or penalties.
   - Provide terrain query and summary APIs for simulation use.

2. Add terrain map handler tests.
   - Verify the selected map can be loaded.
   - Verify parsed initialization matches the map legend.
   - Verify normal, boundary, restricted, gate, exit, Type 1 penalty, and Type 2 penalty cells are initialized correctly.
   - Verify traversability, capacity, exit, and penalty rules.

### Next

1. Integrate parsed terrain with the model snapshot.
   - Preserve existing snapshot fields.
   - Add terrain metadata in a backward-compatible way.

2. Add terrain-aware metrics.
   - Record breach detection/handling.
   - Record blocked boundary attempts.
   - Record time spent in each cell type per agent id.
   - Record gate congestion, exit events, and penalty-cell traversals.

3. Add a 100-tick terrain-map integration test.
   - Initialize a terrain-map-backed model.
   - Include all configured agent categories/ids.
   - Exercise the map and verify metrics are populated.

4. Continue the broader modularization.
   - Refactor agent creation and behaviour.
   - Add movement strategy selection.
   - Add configurable random walk policies.
   - Keep reset determinism and API/frontend compatibility intact.

5. Add frontend terrain visualization.
   - Render terrain cells from snapshot metadata.
   - Use the terrain color coding with stripe-line markings for special cells.
   - Show a compact legend explaining each color and stripe pattern.
