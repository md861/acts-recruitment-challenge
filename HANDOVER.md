# Agent Handover

Last updated: 2026-06-18 15:04 BST (Europe/London)

## Current State

- Repo: `acts-recruitment-challenge`
- Branch: `main`
- Remote: `https://github.com/md861/acts-recruitment-challenge.git`
- Latest commit before this handover update: `3914336 Implement terrain map handler and visualization`
- Working protocol: do not commit or push unless the user explicitly asks, it is end-of-day, or it is a handover-to-new-agent prompt.
- Current task status: Track A modelling work has been chosen. The terrain map handler, model snapshot metadata, terrain metrics, terrain-map integration tests, frontend terrain map visualization path, Terrain1 startup default, and local 100-tick GIF renderer are implemented locally.

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

Last recorded pass: 2026-06-18 15:04 BST during this handover update.

Current local changes are documentation-only: README unfixed issue list plus handover/lab-book updates. The `artifacts/` directory is intentionally ignored and should stay untracked unless the user explicitly asks to publish an artifact.

Untracked note: `Terrain maps/Terrain1_00.png` is present locally and has not been tracked or modified by Codex.

## Known Deferred Item

- `npm audit` reports Vite/esbuild dev-server vulnerabilities (`GHSA-67mh-4wv8-2f99`).
- Decision: defer for now; do not run `npm audit fix --force` blindly.
- Controlled Vite upgrade estimate: 30-60 minutes.

## Suggested Next Action

Continue the broader Track A modularization after the terrain map handler slice:

1. Refactor agent creation into a dedicated module.
2. Add agent behaviour profiles.
3. Add movement strategy selection.
4. Add configurable random walk policies.
5. Refine frontend terrain rendering with stripe-line markings for special cells and terrain metrics in the control panel.
6. Make individual cell edges visible in the browser simulation view and generated GIF.

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
- Update this file with current branch, commit, verification status, known risks, and next suggested action.
- Add a timestamped entry to `project_lab-book.md`.
- Update `Changes.md` if files were created or modified.
- Keep `Changes.md` as a two-list audit: `Files Created` contains files created by this project, while `Files Modified` contains only files that existed in the base project and were later modified.
- Keep `artifacts/` untracked unless the user explicitly asks to publish generated artifacts.
- Commit and push only if the prompt is explicitly a handover-to-new-agent request or the user asks.
