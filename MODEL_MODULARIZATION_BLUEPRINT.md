# Model Modularization Blueprint

This document is the implementation blueprint for the Track A modelling work. It is intended for Codex and future AI agents to use as the shared reference before changing the Python model.

## Goal

Refactor the Python population model into clear, testable modules while adding richer modelling concepts: agent behaviour, configurable movement strategies, random walk policies, terrain rules, and simulation metrics.

The work should preserve the existing API/frontend snapshot contract unless new fields are added in a backward-compatible way.

## Implementation Tasks

1. Implement the terrain map handler as the first implementation slice.
   - Add a handler/parser that selects a PNG terrain map from `Terrain maps/`.
   - Treat white cells as normal cells with no special restrictions or penalties.
   - Convert map colors into symbolic terrain cell definitions.
   - Initialize terrain state from the selected map before agent placement and model ticks.
   - Add focused tests proving parsed cell definitions match the PNG legend.

2. Preserve the baseline contract.
   - Confirm the current snapshot shape, reset behaviour, seed determinism, and bounds handling before refactoring.
   - Keep the Go API and React frontend working while Python internals change.

3. Modularize domain state.
   - Keep/refine `population_model/state.py` as the shared model vocabulary.
   - Continue using `Position`, `Heading`, and `Agent`.
   - Add small domain types only where they improve clarity, such as `Cell`, `CellProperty`, `MovementDecision`, or `TerrainEffect`.

4. Add an agent creation module.
   - Add `population_model/agents.py`.
   - Handle deterministic agent creation, role assignment, initial placement, and behaviour profile lookup.
   - Keep placement logic testable independently from the full model tick loop.
   - Ensure test scenarios can place at least one configured agent against each non-black terrain cell type present in the selected map.

5. Add an agent behaviour module.
   - Add `population_model/behaviour.py`, or keep behaviour profiles in `agents.py` if the implementation remains small.
   - Represent role-specific intent, for example:
     - civilians mostly random-walk and avoid restricted or penalty cells;
     - staff may wait more often or prefer lower-cost movement;
     - patrol agents may enter some restricted cells and handle breach events.

6. Add a movement strategy module.
   - Add `population_model/movement.py`.
   - Provide the shared "next movement" routine.
   - Select candidate moves, filter illegal moves, apply terrain costs/preferences, and return a movement decision with status/reason metadata.

7. Add a random walk module.
   - Add `population_model/random_walk.py`.
   - Support deterministic seeded choices.
   - Support uniform random walks, weighted/probability-based movement, skewed movement, and wait probability.
   - Keep random walk policy tests independent from terrain and model orchestration.

8. Add a terrain module.
   - Add `population_model/terrain.py`.
   - Own cell-level rules:
     - bounded grid checks;
     - restricted cells;
     - restriction by agent id and/or role;
     - fixed density or capacity cells;
     - traversal penalties;
     - breach/trespass classification.
   - Support terrain maps from PNG inputs in `Terrain maps/`.

9. Add a metrics module.
   - Add `population_model/metrics.py`.
   - Compute simulation observations such as:
     - cell density;
     - congestion count and congested cells;
     - attempted breaches;
     - handled breaches;
     - unresolved breaches;
     - terrain penalty events.
     - time spent in each cell type per agent id.

10. Refactor model orchestration.
   - Slim down `population_model/model.py`.
   - Keep it responsible for initialization, tick progression, collaborator calls, state updates, and snapshot construction.
   - Avoid embedding policy decisions directly in the orchestration layer.

11. Extend scenario configuration carefully.
    - Update `population_model/config.py` only where runtime configuration is genuinely needed.
    - Prefer deterministic defaults.
    - Avoid making environment configuration noisy or hard to explain.
    - Include selected terrain map, restricted-cell agent ids, exit-cell agent ids, gate capacities, and Type 1 penalty settings.

12. Add snapshot fields backward-compatibly.
    - Preserve existing `simulation`, `terrain`, and `agents` fields.
    - Add richer fields only additively, for example `simulation.metrics`, richer terrain cell metadata, or movement status reasons.
    - Keep downstream API/frontend compatibility in mind.

13. Add module-level unit tests.
    - Test agent creation determinism.
    - Test random walk determinism, weighting, skew, and wait probability.
    - Test terrain restrictions, capacity/density rules, and traversal penalties.
    - Test selected PNG map parsing, including white normal cells and every configured special cell color.
    - Test that initialized terrain definitions match the selected map specification.
    - Test movement filtering and selection.
    - Test metrics calculations.

14. Add model-level integration tests.
    - Run several ticks and verify agents remain in bounds.
    - Verify restricted cells are respected according to role/id.
    - Verify breach metrics are recorded.
    - Run a terrain-map scenario for around 100 ticks with all configured agent categories/ids.
    - Verify time spent per cell type per agent id is populated.
    - Verify reset remains repeatable.
    - Verify the snapshot remains API-compatible.

15. Add frontend terrain visualization.
    - Render terrain cells from snapshot metadata.
    - Use the terrain-map color coding and stripe-line markings for colored/special cells.
    - Display a compact legend explaining each color and stripe pattern.
    - Keep agents visible on top of terrain markings.
    - Update frontend types and checks when terrain metadata is exposed through the API.

16. Keep documentation and bookkeeping current.
    - Update `project_lab-book.md` as decisions and implementation slices are completed.
    - Update `AI_USAGE_lab-book.md` for meaningful AI prompts and accepted output.
    - Update `Changes.md` whenever tracked files are created or modified.
    - Prepare final `SOLUTION_NOTES.md` and `AI_USAGE.md` near submission time.

## Suggested Implementation Order

1. Implement the terrain map handler and terrain-map unit tests.
2. Add terrain map configuration, including selected PNG, permission ids, exit ids, gate capacities, and Type 1 penalty settings.
3. Expose parsed terrain definitions in the model snapshot in a backward-compatible way.
4. Add baseline terrain metrics for breach detection and time spent in each cell type per agent id.
5. Add model integration coverage that runs the selected terrain map for around 100 ticks with all configured agent categories/ids.
6. Refactor agent creation and placement so map-aware tests can seed agents across non-black terrain cell types.
7. Add terrain-aware movement and role-specific behaviour.
8. Add configurable random walk policies.
9. Add frontend terrain visualization with color-coded stripe markings and a legend.
10. Update final documentation and run the full test script.

## Scope Guardrails

- Prefer small, explicit policies over a generic framework.
- Keep the public snapshot stable unless adding documented fields.
- Make deterministic behaviour easy to test.
- Avoid frontend or Go API changes unless Python snapshot additions require them.
- Do not address the deferred Vite/esbuild audit item as part of this modelling track unless time remains after the main work.

## Terrain Map Inputs

Terrain map images live in the tracked `Terrain maps/` folder. Each PNG should represent a terrain layout whose cell colors are converted into simulation cell properties by the terrain module.

The current terrain map asset is:

- `Terrain maps/Terrain1.png` - Example terrain map image, currently 1213 x 839 RGBA.

The terrain parser should use the following color legend:

1. Black cells are hard boundaries.
   - These cells can never contain agents, regardless of agent id.
   - Treat them as reflective hard Dirichlet-style boundaries: agents should not enter them, and attempted movement into them should be blocked or reflected by the movement routine.

2. Red cells are restricted cells.
   - Only specific agent ids may enter these cells.
   - The allowed ids must be configurable simulation parameters.
   - Unauthorized attempts should be represented as breach or trespass events.

3. Orange cells are maximum-density cells.
   - These cells have a configurable maximum agent density or capacity.
   - For example scenarios, treat them as gates through which agents can pass only when capacity allows.
   - Attempts to enter over-capacity gate cells should be blocked, delayed, or counted as congestion depending on the movement policy.

4. Green cells are removal or exit cells.
   - Agents with configurable ids are taken out of the simulation when they enter these cells.
   - Example use: plane-terminal boarding gates where selected passengers leave the active lattice after boarding.

5. Blue cells apply Type 1 traversal penalties.
   - The penalty is configurable.
   - Example penalties include decreasing or increasing movement likelihood in a specific direction.
   - The terrain module should expose the penalty, while movement/random-walk policies decide how to apply it.

6. Pink cells apply Type 2 traversal penalties.
   - The penalty is preset rather than scenario-configurable.
   - The default behaviour is to decrease movement in all directions.
   - This should be modelled separately from Type 1 penalties so tests can verify both behaviours.

Implementation notes:

- The terrain parser should map colors to symbolic cell types rather than scattering RGB checks throughout the model.
- Color matching should tolerate exact palette colors first; any tolerance or anti-aliasing support should be explicit and tested.
- Configuration should control agent-id permissions, capacities, and Type 1 penalty details.
- Metrics should record blocked boundary attempts, restricted-cell breaches, handled breaches, congestion at orange gate cells, exits through green cells, and penalty-cell traversals.
