# Solution Notes

## Summary

The Python population model was refactored from a single-file toy random walk into a set of focused, testable modules covering terrain handling, agent creation, role-based behaviour profiles, movement strategy selection, configurable random walk policies, simulation metrics, and analysis report generation. The Go API contract and React frontend were extended in a backward-compatible way to surface terrain metadata, compact metrics, and a canvas-rendered terrain visualization with agent overlays.

## Track

Modelling and Simulation Engineer

## What Changed

### New Python model modules ([`model-python/population_model/`](model-python/population_model/))

- [**`terrain.py`**](model-python/population_model/terrain.py) — PNG terrain map parser with a symbolic cell vocabulary (normal, black outer boundary, brown density-zero reflective boundary, red restricted, orange max-density gate, green exit/removal, blue Type 1 penalty, pink Type 2 penalty). Provides terrain query and validation APIs, role/id-based restricted-cell rules, and traversal classification (allowed, boundary, enclosure, restricted breach, gate congestion).
- [**`agents.py`**](model-python/population_model/agents.py) — Deterministic agent creation factory. Handles role assignment, behaviour profile lookup, and terrain-aware initial placement so agents are never initialized outside the black enclosure or on blocked boundary cells.
- [**`behaviour.py`**](model-python/population_model/behaviour.py) — Role-specific behaviour profiles (civilian, staff, patrol). Civilians avoid restricted and penalty cells when alternatives exist; staff prefer waiting or lower-cost moves; patrol agents may intentionally enter configured restricted cells. Provides deterministic, behaviour-aware movement selection from candidate moves.
- [**`movement.py`**](model-python/population_model/movement.py) — Movement strategy module. Evaluates terrain traversal for each candidate move, returns a `MovementDecision` with an allowed/blocked flag, reason metadata, cell type, and penalty preference cost so behaviour can prefer lower-cost moves.
- [**`random_walk.py`**](model-python/population_model/random_walk.py) — Configurable random walk policies: uniform, weighted, wait-probability, directional skew, and deterministic seeded choice. Kept independent of terrain and model orchestration so policies can be tested and changed without touching the model.
- [**`metrics.py`**](model-python/population_model/metrics.py) — Simulation metrics accumulator. Records cell density snapshots, cumulative heatmap visit counts, congestion counts and congested cells, boundary blocks, restricted breaches (handled and unresolved), gate congestion events, exit events, penalty traversals, and per-agent time spent by cell type.
- [**`analysis.py`**](model-python/population_model/analysis.py) — Dependency-free simulation analysis collector and HTML report generator. Produces terrain overlay heatmaps, role-specific terrain time summaries, congestion curves, exit curves, breach/penalty curves, and deterministic replay evidence across a configurable tick window.

### Refactored model orchestration

- [**`model.py`**](model-python/population_model/model.py) — Slimmed to delegate tick progression, per-agent advancement, movement application, metric recording, and density updates to focused helpers. Initialization and reset run through one deterministic lifecycle path. Snapshot shape, reset determinism, and API/frontend compatibility are preserved.
- [**`config.py`**](model-python/population_model/config.py) — Added terrain map path, restricted-cell agent ids, restricted-cell roles, gate capacity, exit agent ids, Type 1 penalty settings, GIF tick count, and analysis tick count. Fixed float environment variable parsing. Kept a Doxygen-compatible file header.
- [**`state.py`**](model-python/population_model/state.py) — Added additive agent behaviour profile identity field to the agent domain type.

### New test modules ([`model-python/tests/`](model-python/tests/))

Nine test modules covering all new modules plus expanded model integration:
[`test_terrain.py`](model-python/tests/test_terrain.py), [`test_agents.py`](model-python/tests/test_agents.py), [`test_behaviour.py`](model-python/tests/test_behaviour.py), [`test_movement.py`](model-python/tests/test_movement.py), [`test_random_walk.py`](model-python/tests/test_random_walk.py), [`test_metrics.py`](model-python/tests/test_metrics.py), [`test_config.py`](model-python/tests/test_config.py), [`test_analysis.py`](model-python/tests/test_analysis.py), [`test_model.py`](model-python/tests/test_model.py) (expanded).

### New scripts

- [**`scripts/render-terrain-gif.py`**](scripts/render-terrain-gif.py) — Renders a configurable terrain-backed simulation preview GIF with patterned cell fills and a legend using only the Python standard library.
- [**`scripts/render-analysis-plots.py`**](scripts/render-analysis-plots.py) — Renders the simulation analysis HTML report over a configurable tick window.

### Go API

- [**`api-go/internal/contracts/contracts.go`**](api-go/internal/contracts/contracts.go) — Passed terrain map metadata, simulation metrics (density, congestion, breaches, exits, penalty events), and agent behaviour profile metadata through the API contract in a backward-compatible way.

### React frontend

- [**`frontend-react/src/api/simulation.ts`**](frontend-react/src/api/simulation.ts) — Added types for terrain map metadata, typed simulation metrics, cumulative heatmap metrics, role metrics, and optional agent behaviour profile metadata.
- [**`frontend-react/src/components/LatticeView.tsx`**](frontend-react/src/components/LatticeView.tsx) — Replaced raw terrain image display with a canvas renderer that reads snapshot terrain metadata and applies the same color/stripe pattern language as the generated GIF. Agents are rendered above the patterned terrain canvas.
- [**`frontend-react/src/components/ControlPanel.tsx`**](frontend-react/src/components/ControlPanel.tsx) — Expanded terrain legend to cover all cell types and surfaced compact terrain metrics (congestion, breaches, exits, penalty traversals).
- [**`frontend-react/src/App.tsx`**](frontend-react/src/App.tsx) — Passed terrain map metadata and metrics into the view components.
- [**`frontend-react/src/styles.css`**](frontend-react/src/styles.css) — Styled the terrain viewport, canvas overlay, metrics panel, and expanded legend swatches.
- [**`frontend-react/public/terrain/Terrain1.png`**](frontend-react/public/terrain/Terrain1.png) — Frontend-served copy of the terrain map for the canvas renderer.

### Documentation and configuration

- [**`MODEL_MODULARIZATION_BLUEPRINT.md`**](MODEL_MODULARIZATION_BLUEPRINT.md) — Full implementation blueprint for Track A.
- [**`Changes.md`**](Changes.md) — Audit of all files created and modified by this project.
- [**`docs/doxygen/Doxyfile`**](docs/doxygen/Doxyfile) — Doxygen configuration for Python model source documentation.
- [**`.gitignore`**](.gitignore) — Extended to ignore Windows Zone.Identifier metadata, local `.tools/` toolchain, generated `artifacts/`, and Doxygen build output.
- [**`scripts/start.sh`**](scripts/start.sh) — Defaults `SIM_TERRAIN_MAP_PATH` to `Terrain maps/Terrain1.png`, generates terrain GIF and analysis report before starting services.

## Why

After an initial orientation pass through the codebase — including a quick literature review on Go and running `./scripts/start.sh` — it was clear the scope of all candidate suggestions (congestion, collision avoidance, terrain-based modelling, goal-directed movement, etc.) was too large for one day's work done properly. The goal narrowed to:

- Modularization of the model code
- Unit and integration test coverage
- A terrain map handler that uses a PNG file to drive cell-type definitions without hard-coding layouts
- Observable performance metrics (breach detection, gate congestion, per-agent cell-time)
- A runnable simulation example with collated analysis output

The original model was a single-file toy random walk in [`model-python/population_model/model.py`](model-python/population_model/model.py). Every agent moved identically, terrain information existed in the snapshot only as a list of cell coordinates with no behavioral effect, and there were no observable metrics beyond tick count and agent positions. This made it inadequate as a foundation for collective training simulation for two reasons:

1. **No meaningful agent differentiation.** Collective training scenarios require roles with distinct intent — civilians who avoid hazards, staff who wait or route carefully, patrol agents who have access to restricted areas. Without this, the simulation produces no behavioral signal worth observing or measuring.

2. **No terrain coupling.** The terrain map was parsed but ignored during movement. Collective training tools depend on spatial constraints: restricted zones, congestion at gates, penalty areas, exit/removal flows. Without terrain-aware movement the simulation cannot represent any recognizable scenario.

The modularization separates terrain rules, behaviour profiles, movement strategy, and metrics into independently testable units, making it straightforward to add new terrain maps, define new role profiles, or change movement policies without touching the orchestration layer. The simulation now produces observable metrics — congestion counts, breach events, per-agent cell-type time, exit events — that could support scenario assessment in a real training tool.

**Key issue encountered and resolved:** During terrain integration, agents were being initialized outside the intended simulation boundary. The fix was to introduce a black cell color as the explicit outer enclosure marker in the terrain parser ([`terrain.py`](model-python/population_model/terrain.py)), with the agent placement factory ([`agents.py`](model-python/population_model/agents.py)) then enforcing that no agent is initialized outside that enclosure.

## How to Run

Dependencies: Python 3.10+, Go 1.21+, Node 18+, npm 9+. Local project-scoped tooling is available under `.tools/` if system tooling is not installed (see [`README.md`](README.md) for install instructions).

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
| [`test_terrain.py`](model-python/tests/test_terrain.py) | 8 | Map loading, cell initialization, brown density-zero cells, role/id restrictions, traversal classification, outside-boundary validation, rule queries |
| [`test_behaviour.py`](model-python/tests/test_behaviour.py) | 9 | Profile intent, deterministic movement selection, behaviour-aware filtering, default-role fallback, invalid empty profile, all-blocked fallback |
| [`test_movement.py`](model-python/tests/test_movement.py) | 8 | Allowed moves, boundary blocks, enclosure blocks, restricted-cell permissions, gate congestion, penalty costs, large-dimension handling |
| [`test_random_walk.py`](model-python/tests/test_random_walk.py) | 7 | Determinism, uniform policy, weighted policy, wait probability, directional skew, invalid policy fallback |
| [`test_agents.py`](model-python/tests/test_agents.py) | 5 | Deterministic creation, role assignment, behaviour profile lookup, terrain-aware placement across cell types |
| [`test_model.py`](model-python/tests/test_model.py) | 7 | Terrain snapshot shape, agent behaviour profile metadata, movement strategy integration, restricted role/id respect, snapshot API compatibility, 100-tick metrics integration, reset determinism |
| [`test_metrics.py`](model-python/tests/test_metrics.py) | 3 | Density snapshots, congested cells, breach accounting, event counters, per-agent cell-type time |
| [`test_config.py`](model-python/tests/test_config.py) | 4 | Deterministic defaults, numeric environment parsing, comma-separated permission lists, invalid-value fallbacks |
| [`test_analysis.py`](model-python/tests/test_analysis.py) | 2 | Metric aggregation, replay evidence, HTML report generation |

### Artifact verification

```bash
# Verify GIF frame count matches tick count (should print 500)
python3 -c "from pathlib import Path; p=Path('artifacts/terrain1_first_500_ticks.gif'); data=p.read_bytes(); print(data.count(bytes([0x21,0xf9,0x04])))"

# Regenerate analysis report and confirm HTML artifact is produced
python3 scripts/render-analysis-plots.py
```

### Last recorded full test pass

2026-06-18 22:21 BST — all checks passed after adding simulation analysis plots and 500-tick artifact defaults.

## Some Ideas for Next Steps if Time Was Available

### Modelling

- **Variable domain size.** The simulation grid is currently sized from the terrain PNG dimensions. Supporting runtime-configurable or multi-resolution domains would allow scaling studies without replacing the map image.
- **Collision detection and avoidance between agents.** Agents currently share cells freely beyond gate capacity limits. Adding explicit collision or exclusion rules would make density metrics more physically meaningful.
- **Fully enforce cell-type behaviours.** For example, exit gate cells should remove trespassing agents from the simulation on entry; penalty cells should affect agent speed or movement likelihood rather than only recording a traversal event.
- **Defined patrol paths.** Patrol agents currently use a behaviour-weighted random walk within allowed cells. Giving them configurable waypoint routes would make patrol coverage measurable and testable.
- **Scenario-driven test cases.** For example:
  - Raise an alert when a breach is detected and automatically dispatch the nearest *x* patrol units and *n* staff agents to the breach location.
  - Measure response time as a function of civilian count, patrol capacity, and staff capacity, with named initialization presets for repeatable scenario comparisons.

### Performance

- **Parallelise agent advancement.** Each agent's next-cell calculation is independent of other agents' calculations within the same tick. These could be computed in parallel (e.g. via `concurrent.futures`) before the density update step, which would need to remain sequential. A tradeoff analysis (Amdahl's Law) against the overhead of process/thread creation would determine the worthwhile agent count threshold.
- **Domain decomposition with message passing.** For very large terrain maps, dividing the grid into *n* spatial partitions with message passing at partition boundaries to track agent flux could reduce per-tick work per partition, subject to the same Amdahl tradeoff.
- **Profiling and complexity analysis.** Run memory and time profiling across varying agent counts and agent-per-id ratios to identify bottlenecks before committing to a parallelisation strategy.

### Visualisation

- **Zoom and pan in the frontend.** The terrain canvas currently renders the full map at a fixed scale. A zoom/pan control would make individual cells and cell edges inspectable, which is especially useful for the large Terrain1 map (1213×839). See the [unfixed issues list](README.md#unfixed-issues) in the README.
- **Fix remaining known issues.** Individual cell grid edges are not yet visible in either the browser view or the generated GIF. The full list is maintained in the [README](README.md#unfixed-issues).
- **Resolve the deferred npm audit finding.** `npm audit` reports a Vite/esbuild dev-server vulnerability (`GHSA-67mh-4wv8-2f99`). A controlled Vite upgrade (estimated 30–60 minutes) would clear it without risking a blind `npm audit fix --force`.
