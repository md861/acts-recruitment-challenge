# Model Modularization Blueprint

This document is the implementation blueprint for the Track A modelling work. It is intended for Codex and future AI agents to use as the shared reference before changing the Python model.

## Goal

Refactor the Python population model into clear, testable modules while adding richer modelling concepts: agent behaviour, configurable movement strategies, random walk policies, terrain rules, and simulation metrics.

The work should preserve the existing API/frontend snapshot contract unless new fields are added in a backward-compatible way.

## Implementation Tasks

1. Preserve the baseline contract.
   - Confirm the current snapshot shape, reset behaviour, seed determinism, and bounds handling before refactoring.
   - Keep the Go API and React frontend working while Python internals change.

2. Modularize domain state.
   - Keep/refine `population_model/state.py` as the shared model vocabulary.
   - Continue using `Position`, `Heading`, and `Agent`.
   - Add small domain types only where they improve clarity, such as `Cell`, `CellProperty`, `MovementDecision`, or `TerrainEffect`.

3. Add an agent creation module.
   - Add `population_model/agents.py`.
   - Handle deterministic agent creation, role assignment, initial placement, and behaviour profile lookup.
   - Keep placement logic testable independently from the full model tick loop.

4. Add an agent behaviour module.
   - Add `population_model/behaviour.py`, or keep behaviour profiles in `agents.py` if the implementation remains small.
   - Represent role-specific intent, for example:
     - civilians mostly random-walk and avoid restricted or penalty cells;
     - staff may wait more often or prefer lower-cost movement;
     - patrol agents may enter some restricted cells and handle breach events.

5. Add a movement strategy module.
   - Add `population_model/movement.py`.
   - Provide the shared "next movement" routine.
   - Select candidate moves, filter illegal moves, apply terrain costs/preferences, and return a movement decision with status/reason metadata.

6. Add a random walk module.
   - Add `population_model/random_walk.py`.
   - Support deterministic seeded choices.
   - Support uniform random walks, weighted/probability-based movement, skewed movement, and wait probability.
   - Keep random walk policy tests independent from terrain and model orchestration.

7. Add a terrain module.
   - Add `population_model/terrain.py`.
   - Own cell-level rules:
     - bounded grid checks;
     - restricted cells;
     - restriction by agent id and/or role;
     - fixed density or capacity cells;
     - traversal penalties;
     - breach/trespass classification.

8. Add a metrics module.
   - Add `population_model/metrics.py`.
   - Compute simulation observations such as:
     - cell density;
     - congestion count and congested cells;
     - attempted breaches;
     - handled breaches;
     - unresolved breaches;
     - terrain penalty events.

9. Refactor model orchestration.
   - Slim down `population_model/model.py`.
   - Keep it responsible for initialization, tick progression, collaborator calls, state updates, and snapshot construction.
   - Avoid embedding policy decisions directly in the orchestration layer.

10. Extend scenario configuration carefully.
    - Update `population_model/config.py` only where runtime configuration is genuinely needed.
    - Prefer deterministic defaults.
    - Avoid making environment configuration noisy or hard to explain.

11. Add snapshot fields backward-compatibly.
    - Preserve existing `simulation`, `terrain`, and `agents` fields.
    - Add richer fields only additively, for example `simulation.metrics`, richer terrain cell metadata, or movement status reasons.
    - Keep downstream API/frontend compatibility in mind.

12. Add module-level unit tests.
    - Test agent creation determinism.
    - Test random walk determinism, weighting, skew, and wait probability.
    - Test terrain restrictions, capacity/density rules, and traversal penalties.
    - Test movement filtering and selection.
    - Test metrics calculations.

13. Add model-level integration tests.
    - Run several ticks and verify agents remain in bounds.
    - Verify restricted cells are respected according to role/id.
    - Verify breach metrics are recorded.
    - Verify reset remains repeatable.
    - Verify the snapshot remains API-compatible.

14. Keep documentation and bookkeeping current.
    - Update `project_lab-book.md` as decisions and implementation slices are completed.
    - Update `AI_USAGE_lab-book.md` for meaningful AI prompts and accepted output.
    - Update `Changes.md` whenever tracked files are created or modified.
    - Prepare final `SOLUTION_NOTES.md` and `AI_USAGE.md` near submission time.

## Suggested Implementation Order

1. Extract existing logic into modules without changing behaviour.
2. Add tests around the extracted module boundaries.
3. Introduce terrain-aware movement and role-specific behaviour.
4. Add configurable random walk policies.
5. Add breach, congestion, and density metrics.
6. Add integration tests around the full model tick loop.
7. Update final documentation and run the full test script.

## Scope Guardrails

- Prefer small, explicit policies over a generic framework.
- Keep the public snapshot stable unless adding documented fields.
- Make deterministic behaviour easy to test.
- Avoid frontend or Go API changes unless Python snapshot additions require them.
- Do not address the deferred Vite/esbuild audit item as part of this modelling track unless time remains after the main work.
