# Changes

## Files Created

- `AI_USAGE_lab-book.md` - Running AI usage log with prompts, purpose, judgement, and verification.
- `project_lab-book.md` - Running project history with decisions, changes, problems, and next steps.
- `HANDOVER.md` - Concise agent-facing state and handover routine.
- `MODEL_MODULARIZATION_BLUEPRINT.md` - Main Track A implementation blueprint for future agents, including updated black/brown terrain semantics.
- `Terrain maps/Terrain1.png` - Example PNG terrain map input asset for future terrain parsing.
- `model-python/population_model/terrain.py` - Terrain map handler, PNG parser, cell vocabulary, black/brown boundary semantics, validation, and terrain query APIs.
- `model-python/population_model/metrics.py` - Terrain-aware simulation metrics accumulator.
- `model-python/population_model/agents.py` - Deterministic agent creation and terrain-aware placement factory.
- `model-python/population_model/behaviour.py` - Role-specific behaviour profiles and deterministic movement selection.
- `model-python/tests/test_terrain.py` - Unit tests for terrain map loading, cell initialization, brown density-zero cells, outside-boundary validation, and rule queries.
- `model-python/tests/test_agents.py` - Unit tests for deterministic agent creation and terrain-aware placement.
- `model-python/tests/test_behaviour.py` - Unit tests for behaviour profile intent and deterministic movement selection.
- `frontend-react/public/terrain/Terrain1.png` - Frontend-served copy of the terrain map image.
- `scripts/render-terrain-gif.py` - Standard-library renderer for the first 100 terrain-backed simulation ticks with legend and patterned cell fills.

## Files Modified

- `.gitignore` - Ignored Windows `Zone.Identifier` metadata, local `.tools/` install artifacts, and generated `artifacts/`.
- `scripts/*.sh` - Restored executable permissions and made `start.sh` default to `Terrain maps/Terrain1.png`.
- `README.md` - Added a GitHub-visible roadmap and unfixed issues list.
- `api-go/internal/contracts/contracts.go` - Passed additive terrain map metadata and simulation metrics through the API contract.
- `frontend-react/src/App.tsx` - Passed terrain map metadata into the lattice visualizer.
- `frontend-react/src/api/simulation.ts` - Added frontend types for terrain map metadata and optional metrics.
- `frontend-react/src/components/ControlPanel.tsx` - Expanded the legend for terrain map cell types.
- `frontend-react/src/components/LatticeView.tsx` - Added terrain image rendering with agent overlays.
- `frontend-react/src/styles.css` - Styled the terrain map viewport, overlays, and expanded legend swatches.
- `model-python/population_model/config.py` - Added terrain map, permission, gate, exit, and penalty configuration fields.
- `model-python/population_model/model.py` - Integrated terrain map metadata, terrain-aware movement blocking, map-enclosure checks, and metrics into the model snapshot.
- `model-python/tests/test_model.py` - Added model-level terrain snapshot and 100-tick metrics integration tests.
