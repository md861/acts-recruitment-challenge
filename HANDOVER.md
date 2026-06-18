# Agent Handover

Last updated: 2026-06-18 22:04 BST (Europe/London)

## Current State

- Repo: `acts-recruitment-challenge`
- Branch: `main`
- Remote: `https://github.com/md861/acts-recruitment-challenge.git`
- Latest committed work: `Complete metrics tests and terrain visualization` (use `git log -1 --oneline` for the exact hash).
- Working protocol: do not commit or push unless the user explicitly asks, it is end-of-day, or it is a handover-to-new-agent prompt.
- Current task status: Track A modelling work has been chosen. Main blueprint Steps 1-15 are implemented. Step 16, final documentation/bookkeeping, is the remaining main-blueprint item.

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

Last recorded pass: 2026-06-18 22:04 BST after completing Step 15 frontend terrain visualization and issue fixes.

Additional Step 15 verification:

```bash
python3 scripts/render-terrain-gif.py
python3 -c "from pathlib import Path; p=Path('artifacts/terrain1_first_100_ticks.gif'); data=p.read_bytes(); print(data.count(bytes([0x21,0xf9,0x04])))"
```

The regenerated default GIF reported `100` frame-control blocks.

There are no tracked local changes after the latest push. The `artifacts/` directory is intentionally ignored and should stay untracked unless the user explicitly asks to publish an artifact.

Untracked note: `Terrain maps/Terrain1_00.png` is present locally and has not been tracked or modified by Codex.

## Known Deferred Item

- `npm audit` reports Vite/esbuild dev-server vulnerabilities (`GHSA-67mh-4wv8-2f99`).
- Decision: defer for now; do not run `npm audit fix --force` blindly.
- Controlled Vite upgrade estimate: 30-60 minutes.

## Suggested Next Action

Continue from the main Track A blueprint after completing Step 15:

1. Complete Step 16 documentation and bookkeeping.
2. Prepare final `SOLUTION_NOTES.md`.
3. Prepare final `AI_USAGE.md`.
4. Run final full verification and package/submission checks if requested.

Generated local artifact: `artifacts/terrain1_first_100_ticks.gif`.

Known visualization issue to revisit:

- Individual cell edges are not yet visible in the browser simulation view or generated GIF.

Latest terrain semantics:

- Black cells define the outer simulation enclosure.
- Brown cells are density-zero reflective boundaries that reject all agents.
- The terrain handler reports validation issues for special cell definitions outside the black outer boundary.

The README now mirrors this at a higher level using Completed, Active, and Next roadmap states.

Runtime note:

- `scripts/start.sh` defaults `SIM_TERRAIN_MAP_PATH` to `Terrain maps/Terrain1.png`.
- `scripts/start.sh` generates `artifacts/terrain1_first_100_ticks.gif` by default before starting services.
- Set `SIM_GIF_TICKS` to change the preview length; default is `100`.
- Set `SIM_GENERATE_GIF=0` to skip preview generation.
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
