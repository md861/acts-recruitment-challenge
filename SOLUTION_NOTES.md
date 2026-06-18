# Solution Notes

## Summary

The Python population model was refactored from a single-file toy random walk into a set of focused, testable modules covering terrain handling, agent creation, role-based behaviour profiles, movement strategy selection, configurable random walk policies, simulation metrics, and analysis report generation. The Go API contract and React frontend were extended in a backward-compatible way to surface terrain metadata, compact metrics, and a canvas-rendered terrain visualization with agent overlays.

## Track

Modelling and Simulation Engineer

## What Changed

### New Python model modules (`model-python/population_model/`)

- **`terrain.py`** — PNG terrain map parser with a symbolic cell vocabulary (normal, black outer boundary, brown density-zero reflective boundary, red restricted, orange max-density gate, green exit/removal, blue Type 1 penalty, pink Type 2 penalty). Provides terrain query and validation APIs, role/id-based restricted-cell rules, and traversal classification (allowed, boundary, enclosure, restricted breach, gate congestion).
- **`agents.py`** — Deterministic agent creation factory. Handles role assignment, behaviour profile lookup, and terrain-aware initial placement so agents are never initialized outside the black enclosure or on blocked boundary cells.
- **`behaviour.py`** — Role-specific behaviour profiles (civilian, staff, patrol). Civilians avoid restricted and penalty cells when alternatives exist; staff prefer waiting or lower-cost moves; patrol agents may intentionally enter configured restricted cells. Provides deterministic, behaviour-aware movement selection from candidate moves.
- **`movement.py`** — Movement strategy module. Evaluates terrain traversal for each candidate move, returns a `MovementDecision` with an allowed/blocked flag, reason metadata, cell type, and penalty preference cost so behaviour can prefer lower-cost moves.
- **`random_walk.py`** — Configurable random walk policies: uniform, weighted, wait-probability, directional skew, and deterministic seeded choice. Kept independent of terrain and model orchestration so policies can be tested and changed without touching the model.
- **`metrics.py`** — Simulation metrics accumulator. Records cell density snapshots, cumulative heatmap visit counts, congestion counts and congested cells, boundary blocks, restricted breaches (handled and unresolved), gate congestion events, exit events, penalty traversals, and per-agent time spent by cell type.
- **`analysis.py`** — Dependency-free simulation analysis collector and HTML report generator. Produces terrain overlay heatmaps, role-specific terrain time summaries, congestion curves, exit curves, breach/penalty curves, and deterministic replay evidence across a configurable tick window.

### Refactored model orchestration

- **`model.py`** — Slimmed to delegate tick progression, per-agent advancement, movement application, metric recording, and density updates to focused helpers. Initialization and reset run through one deterministic lifecycle path. Snapshot shape, reset determinism, and API/frontend compatibility are preserved.
- **`config.py`** — Added terrain map path, restricted-cell agent ids, restricted-cell roles, gate capacity, exit agent ids, Type 1 penalty settings, GIF tick count, and analysis tick count. Fixed float environment variable parsing. Kept a Doxygen-compatible file header.
- **`state.py`** — Added additive agent behaviour profile identity field to the agent domain type.

### New test modules (`model-python/tests/`)

Nine test modules covering all new modules plus expanded model integration:
`test_terrain.py`, `test_agents.py`, `test_behaviour.py`, `test_movement.py`, `test_random_walk.py`, `test_metrics.py`, `test_config.py`, `test_analysis.py`, `test_model.py` (expanded).

### New scripts

- **`scripts/render-terrain-gif.py`** — Renders a configurable terrain-backed simulation preview GIF with patterned cell fills and a legend using only the Python standard library.
- **`scripts/render-analysis-plots.py`** — Renders the simulation analysis HTML report over a configurable tick window.

### Go API

- **`api-go/internal/contracts/contracts.go`** — Passed terrain map metadata, simulation metrics (density, congestion, breaches, exits, penalty events), and agent behaviour profile metadata through the API contract in a backward-compatible way.

### React frontend

- **`frontend-react/src/api/simulation.ts`** — Added types for terrain map metadata, typed simulation metrics, cumulative heatmap metrics, role metrics, and optional agent behaviour profile metadata.
- **`frontend-react/src/components/LatticeView.tsx`** — Replaced raw terrain image display with a canvas renderer that reads snapshot terrain metadata and applies the same color/stripe pattern language as the generated GIF. Agents are rendered above the patterned terrain canvas.
- **`frontend-react/src/components/ControlPanel.tsx`** — Expanded terrain legend to cover all cell types and surfaced compact terrain metrics (congestion, breaches, exits, penalty traversals).
- **`frontend-react/src/App.tsx`** — Passed terrain map metadata and metrics into the view components.
- **`frontend-react/src/styles.css`** — Styled the terrain viewport, canvas overlay, metrics panel, and expanded legend swatches.
- **`frontend-react/public/terrain/Terrain1.png`** — Frontend-served copy of the terrain map for the canvas renderer.

### Documentation and configuration

- **`MODEL_MODULARIZATION_BLUEPRINT.md`** — Full implementation blueprint for Track A.
- **`HANDOVER.md`** — Agent-facing handover state, commit protocol, verification commands.
- **`project_lab-book.md`** — Running development history.
- **`AI_USAGE_lab-book.md`** — Running AI prompt and verification log.
- **`Changes.md`** — Audit of all files created and modified by this project.
- **`docs/doxygen/Doxyfile`** — Doxygen configuration for Python model source documentation.
- **`docs/doxygen/README.md`** — Local rebuild instructions.
- **`.gitignore`** — Extended to ignore Windows Zone.Identifier metadata, local `.tools/` toolchain, generated `artifacts/`, and Doxygen build output.
- **`scripts/start.sh`** — Defaults `SIM_TERRAIN_MAP_PATH` to `Terrain maps/Terrain1.png`, generates terrain GIF and analysis report before starting services.

## Why

The original model was a single-file toy random walk. Every agent moved identically, terrain information existed in the snapshot only as a list of cell coordinates with no behavioral effect, and there were no observable metrics beyond tick count and agent positions. This made it inadequate as a foundation for collective training simulation for two reasons:

1. **No meaningful agent differentiation.** Collective training scenarios require roles with distinct intent — civilians who avoid hazards, staff who wait or route carefully, patrol agents who have access to restricted areas. Without this, the simulation produces no behavioral signal worth observing or measuring.

2. **No terrain coupling.** The terrain map was parsed but ignored during movement. Collective training tools depend on spatial constraints: restricted zones, congestion at gates, penalty areas, exit/removal flows. Without terrain-aware movement the simulation cannot represent any recognizable scenario.

The modularization addresses both by separating terrain rules, behaviour profiles, movement strategy, and metrics into independently testable units. This makes it straightforward to add new terrain maps, define new role profiles, or change movement policies without touching the orchestration layer. The simulation now produces observable metrics — congestion counts, breach events, per-agent cell-type time, exit events — that could support scenario assessment in a real training tool.

## How to Run

Dependencies: Python 3.10+, Go 1.21+, Node 18+, npm 9+. Local project-scoped tooling is available under `.tools/` if system tooling is not installed.

```bash
# Start all three services (generates terrain GIF and analysis report first)
./scripts/start.sh

# Open the frontend
# http://localhost:5173
```

Environment variables to customize startup:

```bash
SIM_TERRAIN_MAP_PATH="Terrain maps/Terrain1.png"   # terrain input (default)
SIM_GIF_TICKS=500                                   # preview GIF length (default)
SIM_ANALYSIS_TICKS=500                              # analysis report window (default)
SIM_GENERATE_GIF=0                                  # set to skip GIF generation
SIM_GENERATE_ANALYSIS=0                             # set to skip analysis generation
```

Generate analysis artifacts independently:

```bash
python3 scripts/render-terrain-gif.py
python3 scripts/render-analysis-plots.py
```

Rebuild Doxygen source documentation (requires system Doxygen):

```bash
doxygen docs/doxygen/Doxyfile
# Output: docs/doxygen/build/html/index.html
```

## How You Tested It

### Automated tests

Run all lightweight checks with:

```bash
./scripts/test.sh
```

This covers Python unit and integration tests, Go build verification, and frontend type checking.

**Python test suite — 53 tests across 9 modules:**

| Module | Tests | Coverage |
|---|---:|---|
| `test_terrain.py` | 8 | Map loading, cell initialization, brown density-zero cells, role/id restrictions, traversal classification, outside-boundary validation, rule queries |
| `test_behaviour.py` | 9 | Profile intent, deterministic movement selection, behaviour-aware filtering, default-role fallback, invalid empty profile, all-blocked fallback |
| `test_movement.py` | 8 | Allowed moves, boundary blocks, enclosure blocks, restricted-cell permissions, gate congestion, penalty costs, large-dimension handling |
| `test_random_walk.py` | 7 | Determinism, uniform policy, weighted policy, wait probability, directional skew, invalid policy fallback |
| `test_agents.py` | 5 | Deterministic creation, role assignment, behaviour profile lookup, terrain-aware placement across cell types |
| `test_model.py` | 7 | Terrain snapshot shape, agent behaviour profile metadata, movement strategy integration, restricted role/id respect, snapshot API compatibility, 100-tick metrics integration, reset determinism |
| `test_metrics.py` | 3 | Density snapshots, congested cells, breach accounting, event counters, per-agent cell-type time |
| `test_config.py` | 4 | Deterministic defaults, numeric environment parsing, comma-separated permission lists, invalid-value fallbacks |
| `test_analysis.py` | 2 | Metric aggregation, replay evidence, HTML report generation |

### Artifact verification

```bash
# Verify GIF frame count matches tick count (should print 500)
python3 -c "from pathlib import Path; p=Path('artifacts/terrain1_first_500_ticks.gif'); data=p.read_bytes(); print(data.count(bytes([0x21,0xf9,0x04])))"

# Regenerate analysis report and confirm HTML artifact is produced
python3 scripts/render-analysis-plots.py
```

### Last recorded full test pass

2026-06-18 22:21 BST — all checks passed after adding simulation analysis plots and 500-tick artifact defaults.

## Trade-Offs and Next Steps

### What was not done

- **Goal-directed pathfinding.** Agents currently select from candidate moves using behaviour-weighted random walks rather than navigating toward explicit goals. Adding A\* or field-based pathfinding would produce more realistic collective movement but was out of scope for a one-day exercise.
- **Grouping and queuing.** Agents do not form groups or queue explicitly at gates; gate congestion is modeled as a capacity block. Real collective training scenarios often need explicit queue formation.
- **Individual cell edge rendering.** The terrain map is large (1213×839), so drawing every cell edge requires a careful zoom and canvas strategy. Edges are not yet visible in the browser view or generated GIF.
- **Frontend npm audit item.** `npm audit` reports a Vite/esbuild dev-server vulnerability (`GHSA-67mh-4wv8-2f99`). This was deferred to avoid a blind `npm audit fix --force` upgrade; a controlled Vite upgrade is estimated at 30–60 minutes.

### What would be improved next

1. Add goal-directed movement so agents navigate toward configured exit or waypoint cells rather than relying entirely on random walk policies.
2. Add explicit queue objects at gate cells so congestion produces observable agent line formation rather than just a blocked-move count.
3. Add zoom and pan to the frontend terrain canvas so individual cells and edges are inspectable at any map scale.
4. Perform the controlled Vite upgrade to clear the npm audit finding.
5. Add scenario configuration files so named training scenarios can be loaded without changing environment variables.
