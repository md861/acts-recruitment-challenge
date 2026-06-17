# Agent Handover

Last updated: 2026-06-18 00:00 BST (Europe/London)

## Current State

- Repo: `acts-recruitment-challenge`
- Branch: `main`
- Remote: `https://github.com/md861/acts-recruitment-challenge`
- Last pushed commit before this file: `03e9085 Record dependency setup and project protocols`
- Working protocol: do not commit or push unless the user explicitly asks, it is end-of-day, or it is a handover-to-new-agent prompt.

## Read First

- `CANDIDATE_INSTRUCTIONS.md`
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

Baseline checks passed with:

```bash
PATH="$PWD/.tools/go/bin:$PWD/.tools/node/bin:$PATH" ./scripts/test.sh
```

## Known Deferred Item

- `npm audit` reports Vite/esbuild dev-server vulnerabilities (`GHSA-67mh-4wv8-2f99`).
- Decision: defer for now; do not run `npm audit fix --force` blindly.
- Controlled Vite upgrade estimate: 30-60 minutes.

## Handover Routine

When asked to prepare for handover:

- Update this file with current branch, commit, verification status, known risks, and next suggested action.
- Add a timestamped entry to `project_lab-book.md`.
- Update `Changes.md` if files were created or modified.
- Commit and push only if the prompt is explicitly a handover-to-new-agent request or the user asks.

