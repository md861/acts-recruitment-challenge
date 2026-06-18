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
   - The terrain legend is documented: white normal, black outer boundary, brown density-zero reflective boundary, red restricted, orange max-density gate, green exit/removal, blue Type 1 penalty, and pink Type 2 penalty.

5. Core terrain map handler and unit tests implemented.
   - Add symbolic terrain cell vocabulary.
   - Add configuration for selected terrain map, restricted ids, exit ids, gate capacity, and Type 1 penalty settings.
   - Load/select `Terrain maps/Terrain1.png`.
   - Parse white, black, red, orange, green, blue, and pink cells into terrain definitions.
   - Treat white cells as normal cells with no special restrictions or penalties.
   - Provide terrain query and summary APIs for simulation use.
   - Verify the selected map can be loaded.
   - Verify parsed initialization matches the map legend.
   - Verify normal, boundary, restricted, gate, exit, Type 1 penalty, and Type 2 penalty cells are initialized correctly.
   - Verify traversability, capacity, exit, and penalty rules.

6. Terrain map model integration and metrics implemented.
   - Preserve existing snapshot fields.
   - Add terrain metadata in a backward-compatible way.
   - Record breach detection/handling.
   - Record blocked boundary attempts.
   - Record time spent in each cell type per agent id.
   - Record gate congestion, exit events, and penalty-cell traversals.
   - Initialize a terrain-map-backed model.
   - Include all configured agent categories/ids.
   - Exercise the map and verify metrics are populated.

7. Frontend terrain visualization and GIF artifact added.
   - Pass terrain metadata and metrics through the Go API contract.
   - Render the terrain PNG as the frontend map background.
   - Overlay agents on the terrain map.
   - Show the terrain color legend in the frontend.
   - Generate local ignored `artifacts/terrain1_first_100_ticks.gif` from the first 100 terrain-backed simulation ticks.
   - Include a legend panel and stripe/pattern styling in the generated GIF.

8. Terrain boundary semantics extended.
   - Black cells define the outer simulation enclosure.
   - Brown cells represent density-zero reflective boundaries.
   - The terrain handler reports validation issues for special cell definitions outside the black outer boundary.

9. Terrain1 startup default set.
   - `scripts/start.sh` defaults `SIM_TERRAIN_MAP_PATH` to `Terrain maps/Terrain1.png`.
   - The default can still be overridden by setting `SIM_TERRAIN_MAP_PATH`.

10. Agent creation and terrain-aware placement refactored.
   - Added a dedicated agent creation module.
   - Moved deterministic role assignment and initial placement out of `PopulationModel`.
   - Kept placement terrain-aware: agents are not initialized outside the black enclosure or on blocked boundary/density-zero cells.
   - Added unit tests for deterministic creation and terrain-aware placement.

11. Agent behaviour profiles added.
   - Added a dedicated behaviour profile module.
   - Moved role-specific candidate movement choices out of `PopulationModel`.
   - Captured civilian, staff, and patrol intent metadata for later terrain-aware movement filtering.
   - Added unit tests for profile intent, deterministic movement selection, default-role fallback, and invalid empty profiles.

12. Movement strategy selection added.
   - Added a dedicated movement strategy module.
   - Moved terrain-entry decisions and blocked-movement reason metadata out of `PopulationModel`.
   - Added unit tests for allowed moves, boundary blocks, enclosure blocks, restricted-cell permissions, gate congestion, and dimensions larger than the terrain map.
   - Added a model-level integration test proving movement-strategy block reasons update simulation metrics.

13. Configurable random walk policies added.
   - Added a dedicated random walk module.
   - Supports deterministic seeded choice, uniform policies, weighted policies, wait probability, and directional skew.
   - Behaviour profiles now select movement through random walk policies.
   - Added independent random-walk unit tests for determinism, weighting, waiting, skew, and invalid policies.

### Active

1. Continue the broader modularization.
   - Refine frontend terrain visualization.
   - Surface terrain metrics in the control panel.
   - Keep reset determinism and API/frontend compatibility intact.

### Next

1. Final documentation and full verification.
   - Prepare final solution notes.
   - Prepare final AI usage summary.
   - Run the full test script before submission.

## Unfixed Issues

These are known issues that are intentionally left for later work.

1. Browser terrain visualization does not yet match the generated GIF.
   - The GIF renderer now shows a legend panel and stripe/pattern fills for terrain cell categories.
   - The browser visualizer at `http://localhost:5173/` still renders the terrain mostly from the raw PNG image and does not yet apply the same canvas-style patterned rendering.
   - Suggested fix: replace or augment the browser terrain view with a canvas renderer that mirrors `scripts/render-terrain-gif.py`.

2. Individual cell edges are not yet visible.
   - The current terrain map is large, so drawing every cell edge needs a careful zoom/canvas strategy.
   - This affects both the browser simulation view and generated GIF readability.
