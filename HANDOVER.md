# Agent Handover

Last updated: 2026-06-18 21:21 BST (Europe/London)

## Current State

- Repo: `acts-recruitment-challenge`
- Branch: `main`
- Remote: `https://github.com/md861/acts-recruitment-challenge.git`
- Latest commit: `7bf9300 Complete behaviour movement and terrain rules`
- Working protocol: do not commit or push unless the user explicitly asks, it is end-of-day, or it is a handover-to-new-agent prompt.
- Current task status: Track A modelling work has been chosen. Terrain map handling, model metrics integration, frontend terrain visualization, agent creation/placement, agent behaviour profiles, movement strategy selection, configurable random walk policies, and terrain rule coverage have now been implemented and committed.

## Read First

- `CANDIDATE_INSTRUCTIONS.md`
- `README.md`
- `MODEL_MODULARIZATION_BLUEPRINT.md`
- `project_lab-book.md`
- `AI_USAGE_lab-book.md`
- `Changes.md`

## Tooling

Local tools live under ignored `.tools/`:

- Go: `.tools/go/bin/go` (`go1.26.4`)
- Node: `.tools/node/bin/node` (`v24.16.0`)
- npm: `.tools/node/bin/npm` (`11.13.0`)
- GitHub CLI: `.tools/gh/bin/gh` (`2.95.0`)

Use:

```bash
PATH="$PWD/.tools/go/bin:$PWD/.tools/node/bin:$PATH"
```

## Verification

Most recent baseline checks passed with:

```bash
PATH="$PWD/.tools/go/bin:$PWD/.tools/node/bin:$PATH" ./scripts/test.sh
```

Last recorded pass: 2026-06-18 21:21 BST after completing the remaining Step 8 terrain rule work.

There are no tracked local changes after the latest push. The `artifacts/` directory is intentionally ignored and should stay untracked unless the user explicitly asks to publish an artifact.

Untracked note: `Terrain maps/Terrain1_00.png` is present locally and has not been tracked or modified by Codex.

## Known Deferred Item

- `npm audit` reports Vite/esbuild dev-server vulnerabilities (`GHSA-67mh-4wv8-2f99`).
- Decision: defer for now; do not run `npm audit fix --force` blindly.
- Controlled Vite upgrade estimate: 30-60 minutes.

## Suggested Next Action

Continue from the main Track A blueprint after completing Step 8:

1. Reassess the next unfinished main-blueprint task by checking `MODEL_MODULARIZATION_BLUEPRINT.md` `Implementation Tasks`.
2. The next likely unfinished item is Step 9, metrics: explicit cell-density, congested-cell, and unresolved-breach metrics are still incomplete.
3. Prepare final solution notes and AI usage summary when implementation scope is complete.

Generated local artifact: `artifacts/terrain1_first_100_ticks.gif`.

Known GIF/visualization issues to revisit:

- Browser terrain visualization at `http://localhost:5173/` does not yet match the generated GIF's legend panel and patterned terrain fills.
- Individual cell edges are not yet visible in the browser simulation view or generated GIF.

Latest terrain semantics:

- Black cells define the outer simulation enclosure.
- Brown cells are density-zero reflective boundaries that reject all agents.
- The terrain handler reports validation issues for special cell definitions outside the black outer boundary.

The README now mirrors this at a higher level using Completed, Active, and Next roadmap states.

Runtime note:

- `scripts/start.sh` defaults `SIM_TERRAIN_MAP_PATH` to `Terrain maps/Terrain1.png`.
- Generated artifacts remain local and ignored by git.

## Handover Routine

When asked to prepare for handover:

- Before any commit/push or handover prep, update the relevant bookkeeping docs and check them for stale state, especially `HANDOVER.md`, `README.md`, `project_lab-book.md`, `AI_USAGE_lab-book.md`, and `Changes.md`.
- When adding a new module, add focused unit tests for that module and, if it affects orchestration or cross-module behaviour, add/update integration tests that prove the module is used correctly.
- Add and maintain Doxygen-compatible file headers for Python model modules using `## @file` and `@brief` comments.
- Update this file with current branch, commit, verification status, known risks, and next suggested action.
- Add a timestamped entry to `project_lab-book.md`.
- Update `Changes.md` if files were created or modified.
- Keep `Changes.md` as a two-list audit: `Files Created` contains files created by this project, while `Files Modified` contains only files that existed in the base project and were later modified.
- After updating `Changes.md`, sanity-check that no filename appears in both `Files Created` and `Files Modified`.
- Keep `artifacts/` untracked unless the user explicitly asks to publish generated artifacts.
- Commit and push only if the prompt is explicitly a handover-to-new-agent request or the user asks.
