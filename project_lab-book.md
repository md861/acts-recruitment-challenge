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

### Entry 22 - Terrain map implementation, visualization, and handover

Date/time: 2026-06-18 14:57 BST (Europe/London)

What happened:

The user asked to start the terrain map handler, complete the remaining terrain-handler slice, produce a 100-tick GIF, update terrain semantics, keep generated artifacts untracked by default, set `Terrain1.png` as the default map for `scripts/start.sh`, fix the GIF issues, then commit/push and prepare handover.

Implementation:

- Added `model-python/population_model/terrain.py` for PNG terrain parsing, cell vocabulary, map validation, query APIs, and black/brown boundary semantics.
- Added `model-python/population_model/metrics.py` for terrain-aware metrics.
- Updated `ModelConfig` with terrain map, permission, gate, exit, and penalty settings.
- Integrated terrain metadata and terrain-aware metrics into the Python model snapshot.
- Updated the Go API contract to pass through additive terrain map metadata and metrics.
- Updated the React frontend to render the terrain image with agent overlays and an expanded terrain legend.
- Added a frontend-served copy of `Terrain1.png`.
- Added `scripts/render-terrain-gif.py` and generated a local ignored `artifacts/terrain1_first_100_ticks.gif`.
- Added `artifacts/` to `.gitignore`.
- Updated `scripts/start.sh` so it defaults to `Terrain maps/Terrain1.png`, while still allowing `SIM_TERRAIN_MAP_PATH` overrides.
- Updated the GIF renderer to include a legend panel and stripe/pattern fills for special cell categories.
- Recorded visible cell edges as a future visualization issue.

Verification:

- Visually checked the regenerated GIF: legend, patterned cells, and agents inside the main simulation block are visible.
- Python unit tests passed: `PYTHONPATH="$PWD/model-python" python3 -m unittest discover -s model-python/tests`.
- Full checks passed: `PATH="$PWD/.tools/go/bin:$PWD/.tools/node/bin:$PATH" ./scripts/test.sh`.

Known follow-up:

- Individual cell edges are not yet visible in the browser simulation view or generated GIF.
- `Terrain maps/Terrain1_00.png` exists locally as an untracked file and was left untouched.

Next steps:

- Commit and push the implementation and documentation updates.
- Continue broader modularization: agent creation/behaviour, movement strategy selection, and configurable random walk policies.

### Entry 23 - README unfixed issues list added

Date/time: 2026-06-18 15:04 BST (Europe/London)

What happened:

The user liked the generated GIF but noted that the browser visualizer at `http://localhost:5173/` does not yet reflect the same legend and patterned terrain rendering.

Decision:

Keep browser/GIF visual parity as an unfixed issue for now and maintain a dedicated `Unfixed Issues` section in `README.md`.

Issues recorded:

- Browser terrain visualization does not yet match the generated GIF's legend panel and patterned fills.
- Individual cell edges are not yet visible in the simulation view.

Next steps:

- Commit and push the documentation update.
- Prepare handover.

Verification:

- Python unit tests passed: `PYTHONPATH="$PWD/model-python" python3 -m unittest discover -s model-python/tests`.
- Full checks passed: `PATH="$PWD/.tools/go/bin:$PWD/.tools/node/bin:$PATH" ./scripts/test.sh`.

### Entry 24 - Bookkeeping stale-state protocol clarified

Date/time: 2026-06-18 15:08 BST (Europe/London)

What happened:

The user asked to make sure relevant bookkeeping docs are updated and checked for stale states before commit/push or handover prep.

Decision:

Add this as a development protocol in `HANDOVER.md`.

Protocol:

Before any commit/push or handover preparation, update the relevant bookkeeping docs and check them for stale state, especially `HANDOVER.md`, `README.md`, `project_lab-book.md`, `AI_USAGE_lab-book.md`, and `Changes.md`.

Current next step from the blueprint:

Continue broader Track A modularization by refactoring agent creation/placement and agent behaviour out of `population_model/model.py`.

### Entry 25 - Agent creation and terrain-aware placement refactored

Date/time: 2026-06-18 15:12 BST (Europe/London)

What happened:

The user asked to continue with the next blueprint steps through unit tests for deterministic creation and terrain-aware placement, and to prompt before moving on to behaviour profiles.

Implementation:

- Added `model-python/population_model/agents.py`.
- Introduced `AgentFactory` for deterministic agent creation, role assignment, and initial placement.
- Moved agent creation and placement out of `PopulationModel`.
- Kept initial placement terrain-aware: agents are not initialized outside the black terrain enclosure or on boundary/density-zero cells.
- Added `model-python/tests/test_agents.py`.
- Added unit tests for deterministic creation, role assignment, terrain-aware placement, and legacy restricted-cell avoidance.
- Updated the README roadmap and `Changes.md`.

Verification:

- Python unit tests passed: `PYTHONPATH="$PWD/model-python" python3 -m unittest discover -s model-python/tests`.
- Full checks passed: `PATH="$PWD/.tools/go/bin:$PWD/.tools/node/bin:$PATH" ./scripts/test.sh`.

Next step:

Prompt the user before starting step 6: agent behaviour profiles.

### Entry 26 - Handover prepared for agent factory commit

Date/time: 2026-06-18 15:15 BST (Europe/London)

What happened:

The user asked to commit and push the agent creation/placement refactor and prepare for handover.

Decision:

Refresh the handover state, rerun checks, and commit the agent factory slice.

Verification:

- Python unit tests passed: `PYTHONPATH="$PWD/model-python" python3 -m unittest discover -s model-python/tests`.
- Full checks passed: `PATH="$PWD/.tools/go/bin:$PWD/.tools/node/bin:$PATH" ./scripts/test.sh`.

### Entry 24 - Terrain map handler first slice implemented

Date/time: 2026-06-18 14:12 BST (Europe/London)

What happened:

The user asked to start the first next step: implementing the terrain map handler.

Implementation:

- Added `model-python/population_model/terrain.py`.
- Added symbolic terrain cell types for normal, boundary, restricted, gate, exit, Type 1 penalty, and Type 2 penalty cells.
- Added a standard-library PNG loader/parser for non-interlaced 8-bit RGB/RGBA PNG terrain maps.
- Added exact palette mapping for `Terrain maps/Terrain1.png`.
- Added terrain query APIs for cell lookup, traversability, exit checks, penalties, summary, and serialization.
- Extended `ModelConfig` with terrain map path, restricted ids, exit ids, gate max density, and Type 1 penalty settings.
- Added `model-python/tests/test_terrain.py` covering map selection, real cell counts from `Terrain1.png`, representative cell initialization, traversability/capacity/exit/penalty rules, and serialization for future snapshots.
- Updated the README roadmap so the core terrain map handler is now completed and model integration/metrics are active.

Verification:

- Python unit tests passed: `PYTHONPATH="$PWD/model-python" python3 -m unittest discover -s model-python/tests`.
- Full checks passed: `PATH="$PWD/.tools/go/bin:$PWD/.tools/node/bin:$PATH" ./scripts/test.sh`.

Next steps:

- Integrate parsed terrain metadata into the model snapshot without breaking the existing API/frontend contract.
- Add terrain-aware metrics, including breach detection and time spent in each cell type per agent id.

### Entry 25 - Terrain map snapshot integration and metrics implemented

Date/time: 2026-06-18 14:20 BST (Europe/London)

What happened:

The user asked to continue with the remaining tasks for the terrain map handler slice.

Implementation:

- Added `model-python/population_model/metrics.py`.
- Integrated `TerrainMap` loading into `PopulationModel`.
- Added `simulation.metrics` to the Python model snapshot.
- Added `terrain.map` metadata to the Python model snapshot while preserving existing terrain fields.
- Added terrain-aware movement checks for hard boundary cells, unauthorized restricted cells, and over-capacity gate cells.
- Added metrics for restricted breaches detected/handled, boundary blocks, gate congestion, exit events, penalty-cell traversals, and time spent in each cell type per agent id.
- Added model-level tests for terrain metadata in snapshots.
- Added a deterministic 100-tick terrain-map-backed integration test that exercises breach, boundary, gate, exit, penalty, and normal cell metrics.
- Updated the README roadmap so terrain handler integration and metrics are marked completed.

Verification:

- Python unit tests passed: `PYTHONPATH="$PWD/model-python" python3 -m unittest discover -s model-python/tests`.
- Full checks passed: `PATH="$PWD/.tools/go/bin:$PWD/.tools/node/bin:$PATH" ./scripts/test.sh`.

Next steps:

- Continue broader modularization: agent creation/behaviour, movement strategy selection, and configurable random walk policies.
- Later, update the Go API contract and React frontend to pass through and visualize terrain metadata.

### Entry 26 - Terrain map visualization and GIF generated

Date/time: 2026-06-18 14:30 BST (Europe/London)

What happened:

The user asked whether the new map handler could create cells from `Terrain1.png` and produce a GIF of the first 100 simulation ticks rendered by the visualization frontend.

Implementation:

- Updated the Python model to use terrain-map dimensions for default terrain-backed runs.
- Added `asset_path` to terrain map snapshot metadata.
- Updated the Go API contract to pass through additive terrain map metadata and metrics.
- Added a Vite-served frontend terrain asset at `frontend-react/public/terrain/Terrain1.png`.
- Updated frontend snapshot types for terrain metadata and optional metrics.
- Updated `LatticeView` to render the terrain PNG efficiently with agent overlays.
- Expanded the frontend legend for normal, boundary, restricted, gate, exit, Type 1 penalty, and Type 2 penalty cells.
- Added `scripts/render-terrain-gif.py`, a standard-library renderer that uses the model and terrain handler to produce the first 100 ticks.
- Generated `artifacts/terrain1_first_100_ticks.gif`.

Notes:

The environment did not expose a browser automation, ffmpeg, or ImageMagick tool. The GIF is therefore generated by a reproducible Python renderer using the same terrain map handler and simulation state, while the React frontend now has the corresponding terrain-map visualization path.

Verification:

- `file artifacts/terrain1_first_100_ticks.gif` reports a GIF89a image, 640 x 443.
- The GIF decoded successfully through the local image viewer.
- Full checks passed: `PATH="$PWD/.tools/go/bin:$PWD/.tools/node/bin:$PATH" ./scripts/test.sh`.

Next steps:

- Refine the frontend terrain rendering with stripe-line markings for special cells.
- Surface terrain metrics in the frontend control panel.
- Continue broader modelling modularization.

### Entry 27 - Artifact protocol and terrain boundary semantics updated

Date/time: 2026-06-18 14:41 BST (Europe/London)

What happened:

The user reviewed the generated GIF and clarified two things:

- Generated artifacts should not be tracked in GitHub by default because they may become large and numerous.
- The terrain map handler should distinguish black outer-boundary cells from brown density-zero reflective boundary cells.

Known GIF issues recorded:

- The GIF does not include the legend, although the browser UI does.
- Cell categories are hard to distinguish in the GIF.
- Special-cell shading should use line/stripe patterns rather than solid fills.
- Agents should initialize inside the main black-bounded simulation block.

Implementation:

- Added `artifacts/` to `.gitignore`.
- Recorded the artifact protocol in `HANDOVER.md`.
- Added brown terrain cells as `density_zero`.
- Treated brown cells as reflective/non-traversable for all agents.
- Treated black cells as defining the enclosed simulation area.
- Added map validation issues for special cell definitions outside the black outer boundary.
- Added tests for brown density-zero cells and outside-boundary validation issues.

Verification:

- Python unit tests passed: `PYTHONPATH="$PWD/model-python" python3 -m unittest discover -s model-python/tests`.
- Full checks passed: `PATH="$PWD/.tools/go/bin:$PWD/.tools/node/bin:$PATH" ./scripts/test.sh`.

Observation:

`Terrain maps/Terrain1_00.png` is present locally as an untracked file. It was left untouched.

Next steps:

- Keep the current generated GIF local unless the user explicitly asks to publish it.
- Later refine the GIF/frontend visualization to include a legend, striped cell patterns, and clearer cell categories.

### Entry 22 - Changes.md two-list rule clarified

Date/time: 2026-06-18 14:05 BST (Europe/London)

What happened:

The user noticed that `Changes.md` listed files created during this project again under the modified-files section.

Decision:

Keep `Changes.md` as a compact two-list audit:

- `Files Created` should include files created by this work.
- `Files Modified` should include only files that already existed in the base project and were then modified.

Action taken:

Cleaned `Changes.md` so created project bookkeeping files remain only under `Files Created`, while `Files Modified` now lists only base-project files that were changed.

Reasoning:

This keeps the file aligned with the user's original intent: a succinct created-vs-modified summary rather than a chronological event log.

### Entry 23 - Handover prepared after Changes.md cleanup

Date/time: 2026-06-18 14:06 BST (Europe/London)

What happened:

The user asked to prepare for handover and explicitly asked to commit and push.

Decision:

Refresh `HANDOVER.md` with the latest commit state and the clarified `Changes.md` rule.

Current state:

- No implementation code has changed yet.
- Track A modelling work remains selected.
- The next implementation step is still the terrain map handler.
- `Changes.md` now follows the two-list rule: files created by this project are not repeated under files modified.

Next steps:

- Run the baseline checks.
- Commit and push the documentation cleanup and handover refresh.

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

### Entry 18 - Terrain map input folder and legend recorded

Date/time: 2026-06-18 13:44 BST (Europe/London)

What happened:

The user clarified that the project now has a `Terrain maps/` folder containing PNG terrain-map inputs and provided the color legend for different cell types.

Asset noted:

- `Terrain maps/Terrain1.png` - PNG terrain map image.

Terrain legend:

- Black: hard boundary cells that can never contain agents, regardless of id; treat as reflective hard Dirichlet-style boundaries.
- Red: restricted cells that only configurable allowed agent ids may enter.
- Orange: configurable maximum-density cells, used as gate-like passage cells in examples.
- Green: removal or exit cells where configurable agent ids are taken out of the active simulation.
- Blue: Type 1 penalty cells with configurable directional movement effects.
- Pink: Type 2 penalty cells with preset movement reduction in all directions.

Decision:

Record the terrain-map convention in `MODEL_MODULARIZATION_BLUEPRINT.md` and track the PNG asset in git.

Reasoning:

The terrain image and legend are now part of the intended model input contract, so future implementation should parse the image into symbolic cell properties rather than hard-coding the current four restricted cells.

### Entry 19 - Terrain map handler made first implementation step

Date/time: 2026-06-18 13:54 BST (Europe/London)

What happened:

The user asked to make the terrain map handler the first next implementation step and to update the earlier modularisation breakdown accordingly.

Decision:

Revise `MODEL_MODULARIZATION_BLUEPRINT.md` so implementation starts with:

- selecting and parsing a PNG terrain map;
- treating white cells as normal cells;
- initializing symbolic terrain cells from map colors;
- testing that initialization matches map specifications;
- integrating terrain-map metrics such as breach detection and time spent per cell type per agent id;
- adding a later frontend visualization slice with color-coded stripe markings and a legend.

Reasoning:

The terrain map defines the model environment, so implementing it first gives later agent behaviour, movement policy, random walk, and metrics work a concrete shared input.

### Entry 20 - Handover refreshed for terrain-map-handler implementation

Date/time: 2026-06-18 13:59 BST (Europe/London)

What happened:

The user asked for the handover docs to be updated so any future agent can pick up from the current state, and then explicitly asked to commit and push afterward.

Decision:

Refresh `HANDOVER.md` to point future agents at the chosen Track A scope and the new first implementation step: the terrain map handler.

Current state for future agents:

- Track A modelling work is selected.
- The terrain-map-handler-first plan is captured in `MODEL_MODULARIZATION_BLUEPRINT.md`.
- `Terrain maps/Terrain1.png` is tracked and documented as the current terrain input asset.
- No implementation code has been changed yet.
- The next coding step is to implement and test the terrain map handler.

Verification:

`./scripts/test.sh` passed with local Go and Node on `PATH`.

Next steps:

- Commit and push the documentation updates, as explicitly requested.

### Entry 21 - README roadmap added and handover prepared

Date/time: 2026-06-18 14:01 BST (Europe/London)

What happened:

The user asked for a roadmap based on the blueprints and next-step breakdowns, maintained in the GitHub README with completed, active, and next states. The user also asked to commit and push once done and then prepare for handover.

Decision:

Add a `Roadmap` section to `README.md` that points to `MODEL_MODULARIZATION_BLUEPRINT.md` and summarizes:

- completed setup, bookkeeping, blueprint, and terrain-map documentation;
- active terrain map handler implementation and tests;
- next model integration, metrics, 100-tick terrain-map integration test, broader modularisation, and frontend visualization work.

Reasoning:

The README is the most visible GitHub entry point. Keeping the roadmap there makes the current project state legible to reviewers and future agents without requiring them to read the entire lab book first.

Next steps:

- Refresh `HANDOVER.md` so future agents read the README roadmap.
- Commit and push the documentation updates.

Verification:

`./scripts/test.sh` passed with local Go and Node on `PATH`.

### Entry 22 - Agent behaviour profiles implemented

Date/time: 2026-06-18 20:04 BST (Europe/London)

What happened:

The user asked to continue with step 6 from the roadmap: agent behaviour profiles.

Decision:

Add a small `population_model/behaviour.py` module rather than expanding `PopulationModel`.

Reasoning:

Role-specific movement choices were still embedded inside the orchestration class. Moving them into behaviour profiles keeps the tick loop simple and creates a testable place to capture later intent, terrain preferences, and movement strategy selection.

Implementation:

- Added `BehaviourProfile` and `BehaviourProfileSet`.
- Added default civilian, staff, and patrol profiles.
- Kept seeded movement selection deterministic by passing the model's existing `random.Random` instance into the profile selector.
- Updated `PopulationModel._next_movement` to delegate to the behaviour profiles.
- Added unit tests for role-specific intent metadata, deterministic selection, default-role fallback, and invalid empty profiles.

Verification:

`PYTHONPATH=model-python python3 -m unittest discover -s model-python/tests` passed with 18 tests.

Next steps:

- Add a movement strategy module that filters candidate moves against terrain and returns movement decisions with status/reason metadata.
- Add configurable random walk policies after the movement strategy module is in place.

### Entry 23 - AI usage lab book chronology repaired

Date/time: 2026-06-18 20:17 BST (Europe/London)

What happened:

The user noticed that the recent step 5 and step 6 prompts were difficult to find in `AI_USAGE_lab-book.md`.

Decision:

Reorder `AI_USAGE_lab-book.md` into a clean chronological sequence with unique entry numbers and add a maintenance protocol requiring `Date/time:` fields with timezone where possible.

Reasoning:

The prompts were present, but duplicated/out-of-order entry numbers made the log less transparent. A timestamp convention should make future maintenance easier and reduce ambiguity during handover or review.

Verification:

Codex checked the reordered entry list and confirmed that step 5, step 6, the step 6 commit/push, and the chronology repair entries are now easy to find.

### Entry 24 - Movement strategy module implemented

Date/time: 2026-06-18 20:22 BST (Europe/London)

What happened:

The user asked to keep moving after the roadmap showed movement strategy selection as the next active Track A item.

Decision:

Add `population_model/movement.py` with a `MovementStrategy` and `MovementDecision` instead of keeping terrain-entry checks inside `PopulationModel`.

Reasoning:

The model orchestration loop should ask for a movement decision and then apply state/metrics updates. Keeping allow/block decisions in a module makes movement filtering testable independently and prepares the next random-walk-policy slice.

Implementation:

- Added movement decisions with target coordinates, allowed/blocked status, reason metadata, and terrain cell type.
- Moved boundary, enclosure, restricted-cell, and gate-congestion entry checks into `MovementStrategy`.
- Kept metrics recording in `PopulationModel`, driven by movement decision reasons.
- Added focused unit tests for the movement strategy.
- Added a model-level integration test proving blocked movement reasons update metrics through the orchestration loop.

Protocol update:

The user clarified that every new module should have relevant unit tests and, where appropriate, integration tests. This was added to the handover development protocol.

Verification:

- `PYTHONPATH=model-python python3 -m unittest discover -s model-python/tests` passed with 25 tests.
- `PATH="$PWD/.tools/go/bin:$PWD/.tools/node/bin:$PATH" ./scripts/test.sh` passed.

### Entry 25 - Configurable random walk policies implemented

Date/time: 2026-06-18 20:31 BST (Europe/London)

What happened:

The user asked to continue with the next Track A blueprint step after movement strategy selection.

Decision:

Add a dedicated `population_model/random_walk.py` module and wire behaviour profiles through random walk policy objects.

Reasoning:

Random walk selection should be independently testable and configurable before adding more sophisticated terrain preference filtering. Keeping policy selection separate from behaviour profiles lets roles choose different movement policies without embedding random choice details in the model orchestration loop.

Implementation:

- Added `RandomWalkPolicy` with deterministic seeded selection.
- Added uniform and weighted policy constructors.
- Added wait probability support for policies without an explicit wait move.
- Added directional skew support through a multiplier for a chosen move.
- Updated behaviour profiles to use random walk policies.
- Added independent random-walk unit tests covering determinism, weighting, wait probability, skew, and invalid policy validation.

Verification:

- `PYTHONPATH=model-python python3 -m unittest discover -s model-python/tests` passed with 32 tests.
- `PATH="$PWD/.tools/go/bin:$PWD/.tools/node/bin:$PATH" ./scripts/test.sh` passed.

### Entry 26 - Doxygen-compatible module headers added

Date/time: 2026-06-18 20:31 BST (Europe/London)

What happened:

The user suggested adding Doxygen-compatible comment headers to the Python modules that have been added or modified, so generated documentation can be produced later.

Decision:

Add concise `## @file` and `@brief` headers to the population model modules and record a protocol to maintain these headers as modules evolve.

Reasoning:

The headers improve readability now and make a future Doxygen documentation pass easier without changing runtime behaviour.

Verification:

`PYTHONPATH=model-python python3 -m unittest discover -s model-python/tests` passed with 32 tests.

### Entry 27 - Changes.md overlap check added to protocol

Date/time: 2026-06-18 20:43 BST (Europe/London)

What happened:

The user asked to make the `Changes.md` no-overlap sanity check part of the future development protocol.

Decision:

Add an explicit handover protocol rule requiring future agents to check that no filename appears in both `Files Created` and `Files Modified` after updating `Changes.md`.

Reasoning:

This preserves the user's intended two-list audit format and prevents created files from being repeated as modified files.

Verification:

Codex had just checked `Changes.md` and confirmed `NO_OVERLAP`, with 18 created entries and 13 modified entries.

### Entry 28 - Remaining Step 4 agent creation work completed

Date/time: 2026-06-18 20:55 BST (Europe/London)

What happened:

The user asked to complete the remaining work for main blueprint Step 4, `Add an agent creation module`.

Decision:

Finish Step 4 by making behaviour profile lookup part of `AgentFactory`, exposing the selected behaviour profile identity additively on agents, and adding placement coverage across allowed non-black terrain cell types.

Reasoning:

The factory already handled deterministic creation, role assignment, and terrain-aware placement. The missing pieces were the behaviour-profile lookup responsibility and a stronger test that placement can seed agents across the relevant terrain categories used by the selected map semantics.

Implementation:

- Added optional `behaviour_profile` metadata to `Agent`.
- Updated `AgentFactory` to accept a `BehaviourProfileSet` and record the profile identity for each created agent.
- Passed model behaviour profiles into `AgentFactory`.
- Passed `behaviour_profile` through the Go API contract and frontend snapshot type.
- Added agent factory tests for configured behaviour profile lookup and placement across normal, restricted, gate, exit, Type 1 penalty, and Type 2 penalty cells.
- Added a model-level assertion that snapshots include the additive behaviour profile field.

Verification:

- `PYTHONPATH=model-python python3 -m unittest discover -s model-python/tests` passed with 34 tests.
- `PATH="$PWD/.tools/go/bin:$PWD/.tools/node/bin:$PATH" ./scripts/test.sh` passed.

### Entry 29 - Remaining Step 5 agent behaviour work completed

Date/time: 2026-06-18 21:07 BST (Europe/London)

What happened:

The user approved the proposed plan for completing main blueprint Step 5, `Add an agent behaviour module`, and asked to proceed.

Decision:

Add a behaviour-aware movement selector that evaluates profile candidate moves through the movement strategy before selecting one.

Reasoning:

Behaviour profiles previously described role intent but did not actively influence movement choices. The selector makes that intent operational while keeping movement legality in `MovementStrategy` and preserving deterministic seeded selection.

Implementation:

- Added `BehaviourMoveSelector`.
- Civilians avoid restricted and penalty cells when a normal allowed move is available.
- Staff prefer waiting/lower-cost moves and avoid penalty cells when possible.
- Patrol profiles can intentionally keep allowed restricted-cell moves.
- Added deterministic fallback when every candidate move is blocked.
- Wired `PopulationModel` through the behaviour selector while preserving the existing `_next_movement` override hook used by integration tests.
- Added Doxygen-style descriptions to the new behaviour selector and random-walk helper methods.
- Added unit tests covering civilian, staff, patrol, and all-blocked fallback behaviour.

Verification:

- `PYTHONPATH=model-python python3 -m unittest discover -s model-python/tests` passed with 38 tests.
- `PATH="$PWD/.tools/go/bin:$PWD/.tools/node/bin:$PATH" ./scripts/test.sh` passed.

### Entry 30 - Remaining Step 6 movement strategy work completed

Date/time: 2026-06-18 21:13 BST (Europe/London)

What happened:

The user asked to continue with the next unfinished main-blueprint step, Step 6 `Add a movement strategy module`.

Decision:

Finish Step 6 by making movement decisions carry terrain penalty metadata and preference costs, then letting behaviour-aware selection prefer lower-cost allowed moves.

Reasoning:

The movement module already handled legality and blocked reasons. The remaining blueprint gap was applying terrain costs/preferences, especially Type 1 and Type 2 penalty cells, before behaviour selection chooses a final move.

Implementation:

- Added `preference_cost` and optional `penalty` metadata to `MovementDecision`.
- Added terrain penalty lookup to `MovementStrategy`.
- Added Type 1 directional penalty costing.
- Added Type 2 all-direction penalty costing.
- Updated behaviour selection to prefer the lowest-cost allowed decisions after filtering avoided terrain.
- Added Doxygen-style comments for the new movement decision/strategy helpers.
- Added movement tests for Type 1 and Type 2 penalty costs.
- Added behaviour tests proving lower-cost allowed moves are preferred.

Verification:

- `PYTHONPATH=model-python python3 -m unittest discover -s model-python/tests` passed with 41 tests.
- `PATH="$PWD/.tools/go/bin:$PWD/.tools/node/bin:$PATH" ./scripts/test.sh` passed.

### Entry 31 - Remaining Step 8 terrain module work completed

Date/time: 2026-06-18 21:21 BST (Europe/London)

What happened:

The user asked to continue from the main blueprint after Step 6. The next unfinished task was Step 8, `Add a terrain module`.

Decision:

Finish Step 8 by adding role-based restricted-cell permissions and terrain-level traversal classification.

Reasoning:

The terrain module already parsed maps and exposed terrain rules, but restricted cells only considered configured agent ids and callers inferred breach/congestion reasons from boolean traversal results. Terrain should own these cell-level rule classifications so movement and metrics use consistent reason metadata.

Implementation:

- Added `restricted_cell_roles` to `ModelConfig`.
- Added `allowed_roles` to `TerrainCell`.
- Added `TerrainTraversal` to classify traversal attempts.
- Added `TerrainMap.classify_traversal`.
- Kept `is_traversable` as a compatibility wrapper around `classify_traversal`.
- Updated movement strategy to consume terrain traversal classification for restricted and gate decisions.
- Added Doxygen-style comments describing the traversal classification behaviour.
- Added terrain tests for role-based restricted access and traversal reasons.

Verification:

- `PYTHONPATH=model-python python3 -m unittest discover -s model-python/tests` passed with 42 tests.
- `PATH="$PWD/.tools/go/bin:$PWD/.tools/node/bin:$PATH" ./scripts/test.sh` passed.

### Entry 32 - Step 9 metrics module completed

Date/time: 2026-06-18 21:33 BST (Europe/London)

What happened:

The user confirmed that the next unfinished main-blueprint item was Step 9, `Add a metrics module`, and asked to continue.

Decision:

Complete the metrics module by adding the remaining blueprint observations directly to `TerrainMetrics`, while keeping policy decisions in movement/terrain modules.

Reasoning:

Metrics should be a reusable accumulator rather than hidden orchestration logic. The model can report density snapshots and movement outcomes, and the metrics module can derive serializable cell density, congestion, and breach summaries from those inputs.

Implementation:

- Added latest cell-density snapshots to `TerrainMetrics`.
- Added congestion count and congested-cell summaries.
- Added unresolved breach accounting.
- Preserved handled breach, boundary block, gate congestion, exit, penalty traversal, and per-agent cell-type time metrics.
- Carried breach-handling metadata through `MovementDecision`.
- Refreshed model metrics on initialization, reset, and after each tick.
- Added focused `test_metrics.py` unit coverage.
- Added model-level assertions that public snapshots expose density and congestion metrics.

Verification:

- `PYTHONPATH="$PWD/model-python" python3 -m unittest discover -s model-python/tests` passed with 45 tests.
- `./scripts/test.sh` passed across Python, Go, and frontend typecheck.

### Entry 33 - Step 10 model orchestration refactored

Date/time: 2026-06-18 21:41 BST (Europe/London)

What happened:

The user asked to keep moving after Step 9, making main blueprint Step 10, `Refactor model orchestration`, the next active task.

Decision:

Refactor `PopulationModel` without changing public snapshots or movement behaviour.

Reasoning:

`PopulationModel` already delegated terrain, agent creation, behaviour selection, movement decisions, and metrics to collaborators, but the tick loop still mixed multiple responsibilities inline. Splitting the loop into small lifecycle and per-agent helpers makes the orchestration layer easier to read and keeps policy decisions outside the top-level loop.

Implementation:

- Consolidated initialization and reset runtime setup in `_reset_runtime_state`.
- Slimmed `step()` so it delegates each tick to `_advance_tick`.
- Split per-agent work into `_advance_agent`, `_apply_movement_decision`, and `_apply_allowed_movement`.
- Moved allowed/blocked movement metric recording into focused helpers.
- Moved density publication and density mutation into focused helpers.
- Removed an unused terrain-enclosure helper from `PopulationModel`.
- Added a reset regression assertion proving density metrics are refreshed with the rebuilt runtime state.

Verification:

- `PYTHONPATH="$PWD/model-python" python3 -m unittest model-python/tests/test_model.py` passed with 5 tests.
- `./scripts/test.sh` passed across Python, Go, and frontend typecheck.

### Entry 34 - Steps 13 and 14 test coverage completed

Date/time: 2026-06-18 21:46 BST (Europe/London)

What happened:

The user asked to complete main blueprint Steps 13 and 14 and report back.

Decision:

Close the remaining module-level and model-level test gaps without expanding the production feature surface.

Reasoning:

Most module-level tests already existed after the modularization work, but configuration parsing had no focused coverage. Model-level integration also needed explicit checks for role/id restricted-cell behaviour and snapshot compatibility.

Implementation:

- Added `test_config.py` for deterministic defaults, numeric environment parsing, comma-separated permission lists, empty-list fallbacks, and invalid-number fallbacks.
- Fixed `_env_float` so configured float environment values are parsed instead of becoming `None`.
- Added a model integration test proving restricted cells block ordinary agents but allow configured agent ids and configured roles.
- Added a snapshot compatibility integration test for expected top-level and nested fields with additive metrics/terrain metadata.
- Kept existing module-level tests for agents, behaviour, movement, random walk, terrain, and metrics intact.

Verification:

- `PYTHONPATH="$PWD/model-python" python3 -m unittest discover -s model-python/tests` passed with 51 tests.
- `./scripts/test.sh` passed across Python, Go, and frontend typecheck.

### Entry 35 - Step 15 frontend terrain visualization completed

Date/time: 2026-06-18 21:56 BST (Europe/London)

What happened:

The user asked to complete main blueprint Step 15 and additionally requested that running the simulation creates a 100-tick GIF by default, with the tick count configurable.

Decision:

Finish the browser visualization by mirroring the generated GIF pattern language in a canvas renderer, surface compact terrain metrics, and make startup generate the deterministic preview GIF by default.

Reasoning:

The previous frontend displayed the raw PNG as a backdrop, which did not match the patterned GIF artifact. A canvas renderer can use the snapshot-provided terrain asset path and summary dimensions to classify map pixels client-side and apply the same stripe/color language without expanding the snapshot payload.

Implementation:

- Replaced raw terrain image display with a patterned terrain canvas in `LatticeView`.
- Kept agents overlaid above the terrain canvas.
- Added Doxygen-compatible comments to the frontend terrain/API/control surfaces touched by this step.
- Added typed terrain metrics to the frontend API types.
- Surfaced compact congestion, breach, gate-block, and penalty metrics in `ControlPanel`.
- Made `scripts/render-terrain-gif.py` accept `--ticks`, `--output`, `SIM_GIF_TICKS`, and `SIM_GIF_OUTPUT`, defaulting to 100 ticks.
- Made `scripts/start.sh` generate the terrain GIF preview by default before starting services; `SIM_GENERATE_GIF=0` disables it.
- Added Doxygen-compatible comments to the GIF/startup scripts.

Verification:

- `SIM_GIF_TICKS=2 python3 scripts/render-terrain-gif.py --ticks 2 --output artifacts/test_step15_preview.gif` generated a smoke-test GIF.
- `npm --prefix frontend-react run test` passed.
- `PYTHONPATH="$PWD/model-python" python3 -m unittest discover -s model-python/tests` passed with 51 tests.
- `bash -n scripts/start.sh scripts/test.sh` passed.
- `./scripts/test.sh` passed across Python, Go, and frontend typecheck.

### Entry 36 - Step 15 issue fixes before commit

Date/time: 2026-06-18 22:04 BST (Europe/London)

What happened:

The user asked to commit and push, but first reported two Step 15 issues: blue Type 1 terrain cells looked inconsistently solid/striped in the frontend, and the sample GIF appeared to be only 2 ticks long instead of the expected 100.

Decision:

Fix the frontend Type 1 stripe calculation and regenerate the default GIF artifact before committing.

Reasoning:

JavaScript keeps negative remainders negative, unlike Python. The Type 1 diagonal stripe calculation used `(x - y) % 10`, so parts of the blue terrain rendered with inconsistent stripe density compared with the GIF renderer. The 2-tick GIF was only a smoke-test artifact; the default renderer/startup path should produce `terrain1_first_100_ticks.gif`.

Implementation:

- Added a positive modulo helper for Type 1 frontend stripe rendering.
- Regenerated `artifacts/terrain1_first_100_ticks.gif` with the default GIF renderer.
- Verified the regenerated GIF contains 100 frame-control blocks.

Verification:

- `python3 scripts/render-terrain-gif.py` regenerated the default GIF.
- Frame check reported `frames=100`.
- `npm --prefix frontend-react run test` passed.
- `./scripts/test.sh` passed across Python, Go, and frontend typecheck.

### Entry 37 - Simulation analysis plots and 500-tick artifacts

Date/time: 2026-06-18 22:21 BST (Europe/London)

What happened:

The user requested report-ready simulation analysis plots: terrain overlay heatmaps, role-specific metrics, congestion plots, exit curves, and deterministic replay evidence. The user also asked that both GIF and analysis plot defaults use 500 ticks and be generated whenever `start.sh` runs.

Decision:

Add cumulative analysis metrics to the model metrics layer, then create a dedicated dependency-free analysis/report renderer for report artifacts.

Reasoning:

Live snapshots already exposed current density, congestion, exits, breaches, penalties, and per-agent terrain time. Report generation needs longitudinal metrics and plots, so a separate analysis module can run deterministic windows and render one artifact without adding plotting dependencies or bloating every live snapshot.

Implementation:

- Added cumulative cell visits for terrain heatmaps.
- Added role-specific terrain cell-time metrics.
- Added `population_model/analysis.py` for analysis collection, replay hashing, and HTML plot rendering.
- Added `scripts/render-analysis-plots.py`.
- Added analysis tests for metric collection, replay evidence, and report HTML generation.
- Updated frontend metric types for cumulative heatmap and role metrics.
- Changed default GIF tick count to 500.
- Added default 500-tick analysis report generation to `scripts/start.sh`.

Verification:

- `python3 scripts/render-terrain-gif.py` generated `artifacts/terrain1_first_500_ticks.gif`.
- GIF frame check reported `frames=500`.
- `python3 scripts/render-analysis-plots.py` generated `artifacts/simulation_analysis_500_ticks.html`.
- `./scripts/test.sh` passed with 53 Python tests, Go tests, and frontend typecheck.

### Entry 38 - Doxygen documentation setup

Date/time: 2026-06-18 22:49 BST (Europe/London)

What happened:

The user requested a directory for Doxygen documentation, compilation with a standard Doxygen config, and a commit/push.

Decision:

Add a reproducible Doxygen documentation setup under `docs/doxygen/` and ignore generated build output.

Reasoning:

The repository now contains Doxygen-compatible comments across model modules and recent frontend/script surfaces. A tracked config lets future agents or maintainers regenerate docs consistently without committing generated HTML churn.

Implementation:

- Added `docs/doxygen/Doxyfile`.
- Added `docs/doxygen/README.md`.
- Configured Doxygen input across Python model sources/tests, scripts, frontend source, Go internal contracts, README, and blueprint.
- Set generated output to `docs/doxygen/build/html`.
- Added `docs/doxygen/build/` to `.gitignore`.

Problems or observations:

- `doxygen` is not installed in the WSL environment.
- Passwordless `sudo` is not available, so Codex could not install Doxygen through `apt`.
- Non-sudo `apt-get install doxygen` failed because package installation requires root.

Verification:

- `doxygen docs/doxygen/Doxyfile` was attempted and failed with `doxygen: command not found`.
- `sudo -n true` reported that a password is required.
- `git diff --check` passed.

### Entry 39 - Doxygen documentation compiled after install

Date/time: 2026-06-18 22:57 BST (Europe/London)

What happened:

The user installed Doxygen and asked Codex to retry the documentation limitation.

Decision:

Use the system Doxygen installation instead of a local binary.

Implementation:

- Confirmed `/usr/bin/doxygen` is available.
- Confirmed Doxygen version `1.9.1`.
- Rebuilt the documentation with `doxygen docs/doxygen/Doxyfile`.
- Removed two config tags that produced Doxygen 1.9.1 warnings: `SHOW_HEADERFILE` and `COLS_IN_ALPHA_INDEX`.
- Rebuilt again and confirmed generated HTML exists.

Verification:

- `doxygen docs/doxygen/Doxyfile` completed successfully.
- `docs/doxygen/build/html/index.html` exists.
- Generated HTML size is about 4.3 MB.

### Entry 40 - Handover preparation

Date/time: 2026-06-18 23:07 BST (Europe/London)

What happened:

The user requested handover preparation, commit, and push.

Decision:

Refresh `HANDOVER.md` so the next agent can resume from the latest pushed state without replaying stale Step 8/Step 15 context.

Implementation:

- Updated the handover timestamp.
- Updated the latest-work marker for the upcoming handover commit.
- Clarified the most recent full test pass and the later Doxygen documentation pass.
- Confirmed the only remaining untracked file is the local `Terrain maps/Terrain1_00.png` copy.

Verification:

- `git status --short` was checked before the handover edit.
