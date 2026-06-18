# Project Lab Book

This lab book records the development history for the ACTS recruitment challenge work. It is intended to be readable, transparent, and useful when preparing final `SOLUTION_NOTES.md`.

## Project Context

The repository is a small proof-of-concept collective training simulation with three services:

- Python population model in `model-python`.
- Go integration API in `api-go`.
- React/Vite frontend in `frontend-react`.

The candidate instructions ask for one focused, role-relevant improvement, with clear verification and written notes.

## Running Development Log

### Entry 1 - Initial orientation

Date/time: 2026-06-17, time not recorded (Europe/London)

What happened:

Codex inspected the workspace and confirmed that the active directory was `\\wsl.localhost\Ubuntu-22.04\home\mynk\Skyral_Tasks`.

Decision:

Proceed by inspecting the project before making changes.

Reasoning:

The challenge asks for good engineering judgement and preserving the working baseline. Understanding the system first reduces the risk of making a broad or misaligned change.

Problems or observations:

The workspace contains Windows `Zone.Identifier` metadata entries. These are not project source files and should be ignored.

### Entry 2 - Repository summary

Date/time: 2026-06-17, time not recorded (Europe/London)

What happened:

Codex read the main documentation, service entry points, tests, scripts, Dockerfiles, and templates.

Current understanding:

- The Python model uses a seeded random walk on a 2D lattice.
- The Go API proxies model endpoints and adds basic validation warnings.
- The React frontend polls snapshots and provides pause/resume, step, and reset controls.
- Docker Compose exists.
- Kubernetes support is only a starter README.

Decision:

No implementation track has been chosen yet. Keep the project baseline intact until a track and improvement are selected.

Problems or observations:

The project is intentionally simple, so a good submission should probably be narrow and testable rather than large.

### Entry 3 - GitHub and lab-book setup

Date/time: 2026-06-17, time not recorded (Europe/London)

What happened:

The user requested a private GitHub repository and two living lab books:

- `AI_USAGE_lab-book.md`
- `project_lab-book.md`

Decision:

Create both lab books at the repository root and start them with entries covering the work already done.

Reasoning:

This gives the project a transparent history from the beginning and makes the final AI usage and solution notes easier to prepare.

Problems or observations:

PowerShell did not have `git` or `gh` available. WSL access initially required sandbox approval. GitHub repo creation still needs Git/GitHub CLI availability and authentication to be confirmed.

Next steps:

- Initialize a local git repository if one does not already exist.
- Create a private GitHub repo if GitHub CLI/authentication is available.
- Add the lab books to the initial commit.

### Entry 4 - Local git repository initialized

Date/time: 2026-06-17, time not recorded (Europe/London)

What happened:

Codex initialized a local git repository in `acts-recruitment-challenge` and renamed the default branch to `main`.

Decision:

Add `*Zone.Identifier*` to `.gitignore`.

Reasoning:

The workspace contains Windows download metadata entries such as `README.md:Zone.Identifier`. These are not source files and should not be included in the project history or final submission.

Problems or observations:

Git is available inside WSL, but PowerShell does not currently expose `git`. GitHub CLI (`gh`) was not found in WSL, so publishing to GitHub requires another route.

Next steps:

- Stage the project files.
- Commit the initial repository state.
- Create or connect a private GitHub repo once credentials/tooling are available.

### Entry 5 - Initial commit created

Date/time: 2026-06-17, time not recorded (Europe/London)

What happened:

Codex staged the clean project tree and created the first local git commit on branch `main`.

Commit:

```text
2c2b960 Initial challenge setup
```

Decision:

Use a one-shot commit identity for the initial commit:

```text
user.name=Codex
user.email=codex@example.invalid
```

Reasoning:

WSL did not have a global git identity configured. Using a one-shot identity allowed the initial project snapshot to be recorded without changing the user's global git configuration.

Problems or observations:

GitHub CLI (`gh`) is not installed in WSL, so Codex could not create the private GitHub repository directly at this point.

Next steps:

- Either install/authenticate `gh` in WSL and run `gh repo create ... --private`.
- Or create an empty private GitHub repository manually and add it as the `origin` remote.
- Push branch `main` once the remote exists.

### Entry 6 - GitHub CLI installed locally

Date/time: 2026-06-17, time not recorded (Europe/London)

What happened:

Codex attempted a system package install, but `sudo` required a password. Instead, Codex installed GitHub CLI locally inside the project workspace.

Decision:

Install the official GitHub CLI release under `.tools/gh` and ignore `.tools/` in git.

Reasoning:

This makes `gh` available for repository creation without requiring system-level package installation or changes to the user's global environment.

Details:

- Release: `v2.95.0`.
- Asset: `gh_2.95.0_linux_amd64.tar.gz`.
- Checksum verification: passed.
- Installed binary: `.tools/gh/bin/gh`.

Problems or observations:

The local binary is intentionally not committed. It is a tool artifact, not part of the challenge solution.

Next steps:

- Check `gh auth status`.
- Authenticate if needed.
- Create a private GitHub repository and push `main`.

### Entry 7 - Compact changes summary added

Date/time: 2026-06-17, time not recorded (Europe/London)

What happened:

The user requested an extremely succinct `Changes.md` file listing created and modified files.

Decision:

Add `Changes.md` at the repository root with two short sections:

- Files created.
- Files modified.

Reasoning:

This gives a quick audit trail for setup changes without needing to read the longer lab books.

### Entry 8 - Working protocols for this project

Date/time: 2026-06-17, time not recorded (Europe/London)

What happened:

The user clarified how commits and pushes should be handled, and asked for learned project protocols to be captured for future agents.

Standing protocols:

- Treat `project_lab-book.md` as the default lab book when the user says "lab book", unless they explicitly name another file.
- Do not commit or push changes unless the user explicitly asks, the prompt is clearly an end-of-day wrap-up, or the prompt is clearly a handover-to-new-agent request.
- Keep `AI_USAGE_lab-book.md` as a running record of AI prompts, purpose, human judgement, accepted output, and verification.
- Keep `project_lab-book.md` as a readable project history covering decisions, changes, problems, and next steps.
- Ask the user questions when a lab-book entry needs human rationale or intent that Codex cannot infer confidently.
- Keep `Changes.md` extremely succinct, with the two-list format requested by the user: files created and files modified.
- Keep `.tools/` out of git; it contains local tooling such as the downloaded GitHub CLI binary, not challenge source.
- Ignore Windows `Zone.Identifier` metadata files; they are not part of the source or submission.

Decision:

Future agents should follow these protocols before making repository-history changes or updating project records.

Verification:

This entry was added locally only. Per the new protocol, it has not been committed or pushed.

### Entry 9 - Dependency check

Date/time: 2026-06-17, time not recorded (Europe/London)

What happened:

The user asked Codex to check whether the dependencies required to run and test the project are installed.

Findings:

- Python is available in WSL: `Python 3.10.12`.
- Go is not available in WSL: `go: command not found`.
- Native Node.js is not available in WSL: `node: command not found`.
- `npm` is available on PATH, but it resolves to the Windows installation at `/mnt/c/Program Files/nodejs/npm`, not a native WSL install.
- `frontend-react/package-lock.json` exists.
- `frontend-react/node_modules` is not installed.

Decision:

Do not attempt dependency installation yet. Report the current state first.

Reasoning:

The project README expects Python 3.10+, Go 1.21+, Node.js 18+, and npm 9+. The current environment does not satisfy the Go or native Node.js requirements, so `./scripts/test.sh` and `./scripts/start.sh` are not expected to work cleanly yet.

Next steps:

- Install Go inside WSL.
- Install native Node.js and npm inside WSL.
- Run `./scripts/test.sh` after dependencies are installed.

### Entry 10 - Dependencies fixed and tests verified

Date/time: 2026-06-17, time not recorded (Europe/London)

What happened:

The user asked Codex to fix the missing dependencies required to run and test the project.

Actions taken:

- Installed Go locally under `.tools/go`.
- Installed Node.js locally under `.tools/node`.
- Reused the existing `.tools/` convention, which is ignored by git.
- Verified both downloaded archives with SHA256 checksums before extraction.
- Fixed executable permissions on `scripts/*.sh`.
- Ran the project test script with a clean PATH pointing at the local Go and Node toolchains.

Installed versions:

- Go: `go1.26.4 linux/amd64`.
- Node.js: `v24.16.0`.
- npm: `11.13.0`.
- Python: `3.10.12` was already present.

Verification:

`./scripts/test.sh` passed with the local toolchain.

Observed output:

- Python tests passed: 2 tests.
- Go tests passed.
- Frontend TypeScript check passed.
- `npm install` installed 67 packages.
- `npm audit` reported 2 baseline vulnerabilities: 1 moderate and 1 high.

Problems or observations:

The project scripts initially failed with `Permission denied` because the shell scripts were not executable. `chmod +x scripts/*.sh` fixed this.

Next steps:

- Decide later whether to address the baseline npm audit findings as part of the chosen challenge track.
- Continue using the local toolchain by prepending `.tools/go/bin` and `.tools/node/bin` to `PATH`.

### Entry 11 - Vite/esbuild audit finding deferred

Date/time: 2026-06-17, time not recorded (Europe/London)

What happened:

After dependencies were installed, `npm audit` reported 2 frontend dependency vulnerabilities through Vite's esbuild dependency. The user asked what the issue was, how long a controlled Vite upgrade would take, and whether deferring it was a reasonable trade-off.

Finding:

- Affected package path: `vite -> esbuild <= 0.24.2`.
- Advisory: `GHSA-67mh-4wv8-2f99`.
- Summary: esbuild's development server behavior can allow a malicious website visited in the same browser to read responses from a local dev server because of permissive CORS behavior.
- Scope: development-server exposure, not the built static frontend by itself.
- Automated fix: `npm audit fix --force` would install `vite@8.0.16`, which is a breaking upgrade from the current Vite 5 setup.

Decision:

Defer the Vite/esbuild vulnerability fix for now and continue with the main project work.

Reasoning:

The issue does not block running or testing the project, the full project checks currently pass, and a controlled Vite upgrade could distract from the role-focused challenge improvement. The fix should be revisited if time allows, or if frontend/platform security becomes part of the chosen track.

Estimate recorded:

A controlled Vite upgrade is estimated at 30-60 minutes: update Vite/plugin versions, refresh `package-lock.json`, run frontend checks, run full project checks, and smoke-test the UI.

Next steps:

- Keep the audit finding visible as a known deferred hygiene/security item.
- Do not run `npm audit fix --force` blindly.
- Revisit only after the main challenge direction is chosen or if time remains.

### Entry 12 - Lab-book timestamp format

Date/time: 2026-06-17 23:38 BST (Europe/London)

What happened:

The user asked whether lab-book entries can record the time as well as the date, and clarified that the time should be registered next to the date for each entry.

Decision:

Use `Date/time:` for project lab-book entries going forward.

Protocol:

- Future `project_lab-book.md` entries should include the actual entry time next to the date.
- Use the local timezone explicitly: `Europe/London`.
- For previous entries where the exact time was not recorded, mark the time honestly as `time not recorded`.

Reasoning:

This improves traceability without inventing precision for earlier work.

### Entry 13 - Agent handover file and routine

Date/time: 2026-06-18 00:00 BST (Europe/London)

What happened:

The user asked for a separate succinct handover Markdown file that another AI agent can use and maintain to continue from the current state.

Decision:

Create `HANDOVER.md` at the repository root.

Handover protocol:

- `HANDOVER.md` should be updated as part of any "prepare for handover" routine.
- Keep it concise and agent-facing.
- Include current repo state, must-read files, local toolchain notes, verification status, known deferred risks, and next suggested action.
- Add a timestamped entry to `project_lab-book.md` whenever the handover file or routine is updated.
- Update `Changes.md` when the handover file is created or materially changed.
- Respect the existing commit/push protocol: only commit and push when explicitly asked, at end of day, or for a handover-to-new-agent prompt.

Reasoning:

The project lab book is comprehensive, but a future agent also needs a short operational summary to get oriented quickly without rereading the full history first.

### Entry 14 - Handover performed

Date/time: 2026-06-18 00:20 BST (Europe/London)

What happened:

The user asked Codex to perform the handover routine.

Actions taken:

- Read `HANDOVER.md` and the required context files listed there.
- Checked the current branch, remote, working tree status, and latest commit.
- Updated `HANDOVER.md` with the current remote, latest commit, current task status, and suggested next action.
- Recorded this handover in `project_lab-book.md`.
- Updated `AI_USAGE_lab-book.md` for the handover prompt.
- Kept `Changes.md` succinct while noting that the handover and lab-book files have been updated.

Current state:

- Branch: `main`.
- Remote: `https://github.com/md861/acts-recruitment-challenge.git`.
- Latest commit before this handover update: `2345836 Add agent handover notes`.
- Working tree was clean before the handover documentation edits.

Next steps:

- Commit and push the handover update, because this prompt is a handover-to-new-agent request.

Verification:

`./scripts/test.sh` passed with local Go and Node on `PATH`.

### Entry 15 - Model modularisation request scoped

Date/time: 2026-06-18 13:22 BST (Europe/London)

What happened:

The user proposed a Track A-style modelling refactor to make the Python model easier to unit test and integration test.

Requested module boundaries:

- Agent creation and agent behaviour.
- Movement selection routines that can support multiple movement strategies.
- Random walk routines with deterministic seeding, probability distributions, and skewed movement options.
- Terrain handling for cell properties such as fixed density, restricted traversal by agent id, and trespass penalties.
- Simulation metrics such as congestion, breach detection/handling, and cell density.

Decision:

Do not implement yet. First assess feasibility and provide a time estimate, as requested.

Current assessment:

The existing model is compact and concentrated in `model-python/population_model/model.py`, so this is manageable. The main risk is scope control: the architecture can support the requested concepts, but only a focused first implementation should be completed for the take-home challenge.

Next steps:

- Provide the user with a realistic estimate for a narrow, testable modular refactor.
- If approved, implement the refactor in small slices and expand tests around the new module boundaries.

### Entry 16 - Full model modularisation scope selected

Date/time: 2026-06-18 13:26 BST (Europe/London)

What happened:

The user chose to proceed with the full version of the requested Track A modelling modularisation and asked for an enumerated task breakdown focused on what will be modularized.

Decision:

Prepare a structured implementation plan before changing source code.

Planned focus:

- Separate domain state from orchestration.
- Introduce dedicated modules for agent creation/behaviour, movement strategy selection, random walk policy, terrain rules, and simulation metrics.
- Preserve the existing snapshot contract unless a documented additive metrics field is introduced.
- Add tests around each module boundary and the integrated model tick loop.

### Entry 17 - Model modularization blueprint created

Date/time: 2026-06-18 13:36 BST (Europe/London)

What happened:

The user asked for the modularisation breakdown to be saved as the main blueprint for the project so Codex and future AI agents can refer to it.

Decision:

Create a tracked root-level Markdown file named `MODEL_MODULARIZATION_BLUEPRINT.md`.

Reasoning:

A dedicated blueprint is easier for future agents to find than reconstructing the plan from chat history or lab-book entries. It also makes the chosen Track A scope visible in GitHub.

Implementation note:

The blueprint captures module boundaries, suggested implementation order, testing expectations, snapshot compatibility guardrails, and documentation responsibilities.

Next steps:

- Commit and push the blueprint and bookkeeping updates, as explicitly requested by the user.
