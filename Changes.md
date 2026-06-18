# Changes

## Files Created

1. `AI_USAGE_lab-book.md` - Running AI usage log with prompts, purpose, judgement, and verification.
2. `project_lab-book.md` - Running project history with decisions, changes, problems, and next steps.
3. `HANDOVER.md` - Concise agent-facing state and handover routine.
4. `MODEL_MODULARIZATION_BLUEPRINT.md` - Main Track A implementation blueprint for future agents, including updated black/brown terrain semantics.
5. `Terrain maps/Terrain1.png` - Example PNG terrain map input asset for future terrain parsing.
6. `model-python/population_model/terrain.py` - Terrain map handler, PNG parser, cell vocabulary, black/brown boundary semantics, validation, role/id restricted-cell rules, traversal classification, and terrain query APIs.
7. `model-python/population_model/metrics.py` - Terrain-aware simulation metrics accumulator.
8. `model-python/population_model/agents.py` - Deterministic agent creation, behaviour profile lookup, and terrain-aware placement factory.
9. `model-python/population_model/behaviour.py` - Role-specific behaviour profiles, behaviour-aware movement filtering, and deterministic movement selection.
10. `model-python/population_model/movement.py` - Movement strategy decisions with terrain traversal classification, allow/block reasons, and penalty preference costs.
11. `model-python/population_model/random_walk.py` - Configurable random walk policies for uniform, weighted, wait-probability, and skewed movement.
12. `model-python/tests/test_terrain.py` - Unit tests for terrain map loading, cell initialization, brown density-zero cells, role/id restrictions, traversal classification, outside-boundary validation, and rule queries.
13. `model-python/tests/test_agents.py` - Unit tests for deterministic agent creation, behaviour profile lookup, and terrain-aware placement.
14. `model-python/tests/test_behaviour.py` - Unit tests for behaviour profile intent, deterministic movement selection, movement filtering, and fallback behaviour.
15. `model-python/tests/test_movement.py` - Unit tests for movement strategy decisions, terrain block reasons, and penalty preference costs.
16. `model-python/tests/test_random_walk.py` - Unit tests for deterministic and configurable random walk policies.
17. `frontend-react/public/terrain/Terrain1.png` - Frontend-served copy of the terrain map image.
18. `scripts/render-terrain-gif.py` - Standard-library renderer for the first 100 terrain-backed simulation ticks with legend and patterned cell fills.

## Files Modified

1. `.gitignore` - Ignored Windows `Zone.Identifier` metadata, local `.tools/` install artifacts, and generated `artifacts/`.
2. `scripts/*.sh` - Restored executable permissions and made `start.sh` default to `Terrain maps/Terrain1.png`.
3. `README.md` - Added a GitHub-visible roadmap and unfixed issues list.
4. `api-go/internal/contracts/contracts.go` - Passed additive terrain map metadata, simulation metrics, and agent behaviour profile metadata through the API contract.
5. `frontend-react/src/App.tsx` - Passed terrain map metadata into the lattice visualizer.
6. `frontend-react/src/api/simulation.ts` - Added frontend types for terrain map metadata, optional metrics, and optional agent behaviour profile metadata.
7. `frontend-react/src/components/ControlPanel.tsx` - Expanded the legend for terrain map cell types.
8. `frontend-react/src/components/LatticeView.tsx` - Added terrain image rendering with agent overlays.
9. `frontend-react/src/styles.css` - Styled the terrain map viewport, overlays, and expanded legend swatches.
10. `model-python/population_model/config.py` - Added terrain map, permission, restricted-role, gate, exit, and penalty configuration fields plus a Doxygen-compatible file header.
11. `model-python/population_model/model.py` - Integrated terrain map metadata, behaviour-aware movement selection, terrain-aware movement strategy decisions, map-enclosure checks, and metrics into the model snapshot; added a Doxygen-compatible file header.
12. `model-python/population_model/state.py` - Added additive agent behaviour profile metadata and a Doxygen-compatible file header for shared domain state types.
13. `model-python/tests/test_model.py` - Added model-level terrain snapshot, agent behaviour profile metadata, movement strategy, and 100-tick metrics integration tests.
