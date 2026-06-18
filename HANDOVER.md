# Agent Handover

Last updated: 2026-06-18 13:59 BST (Europe/London)

## Current State

- Repo: `acts-recruitment-challenge`
- Branch: `main`
- Remote: `https://github.com/md861/acts-recruitment-challenge.git`
- Latest commit before this handover update: `6acb2c0 Document terrain map legend`
- Working protocol: do not commit or push unless the user explicitly asks, it is end-of-day, or it is a handover-to-new-agent prompt.
- Current task status: Track A modelling work has been chosen. No implementation code has been changed yet. The next implementation step is the terrain map handler.

## Read First

- `CANDIDATE_INSTRUCTIONS.md`
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

Last recorded pass: 2026-06-18 13:59 BST during this handover update.

No implementation code has changed yet. Current changes in this handover update are documentation/planning only.

## Known Deferred Item

- `npm audit` reports Vite/esbuild dev-server vulnerabilities (`GHSA-67mh-4wv8-2f99`).
- Decision: defer for now; do not run `npm audit fix --force` blindly.
- Controlled Vite upgrade estimate: 30-60 minutes.

## Suggested Next Action

Implement the terrain map handler as the first Track A slice. Follow the updated order in `MODEL_MODULARIZATION_BLUEPRINT.md`:

1. Add symbolic terrain cell vocabulary and map configuration.
2. Load/select `Terrain maps/Terrain1.png`.
3. Parse white, black, red, orange, green, blue, and pink cells into terrain definitions.
4. Add unit tests that verify initialization matches the PNG legend.
5. Integrate parsed terrain metadata into the model snapshot without breaking the current API/frontend contract.
6. Add initial metrics hooks, especially breach detection and time spent in each cell type per agent id.
7. Add a 100-tick terrain-map integration test after the parser and terrain API are stable.

Frontend follow-on: render terrain cells with the same color coding, stripe-line markings for special cells, and a compact legend explaining each color/pattern.

## Handover Routine

When asked to prepare for handover:

- Update this file with current branch, commit, verification status, known risks, and next suggested action.
- Add a timestamped entry to `project_lab-book.md`.
- Update `Changes.md` if files were created or modified.
- Commit and push only if the prompt is explicitly a handover-to-new-agent request or the user asks.
