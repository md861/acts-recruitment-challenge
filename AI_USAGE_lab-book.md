# AI Usage Lab Book

This lab book records how AI assistance is used during the ACTS recruitment challenge work. It follows the spirit of `docs/ai-usage-log-template.md`, but keeps a running, chronological record rather than only a final submission summary.

## Purpose

- Capture prompts and requests made to AI tools.
- Record why each prompt was asked.
- Record what was understood or accepted from the response.
- Record human input, judgement, corrections, and decisions.
- Record verification steps and any places where AI assistance was uncertain or unhelpful.

## Running Log

### Entry 1 - Workspace orientation

Date: 2026-06-17

Tool used: Codex

Prompt / request:

```text
do you see the pwd?
```

Purpose:

Confirm that Codex could see the expected working directory before inspecting or changing the project.

What was understood from the response:

The active working directory was confirmed as `\\wsl.localhost\Ubuntu-22.04\home\mynk\Skyral_Tasks`.

Human input and judgement:

The user confirmed that this was the intended location.

What was accepted from AI:

Only the environment confirmation.

Verification:

Codex ran `Get-Location` and reported the path.

### Entry 2 - Repository contents summary

Date: 2026-06-17

Tool used: Codex

Prompt / request:

```text
ok great. read the contents and give me a summary about it
```

Purpose:

Understand the repository structure, challenge instructions, service layout, and likely improvement areas before beginning implementation work.

What was understood from the response:

The project is a deliberately small ACTS take-home challenge containing a Python population model, Go integration API, React frontend, Docker Compose files, and starter Kubernetes notes. It asks the candidate to choose one role-specific track and make a focused, tested improvement.

Human input and judgement:

The user asked for a summary rather than changes, so no project files were modified.

What was accepted from AI:

The architectural summary and identification of likely tracks: modelling, integration/fullstack, or platform.

Verification:

Codex read the challenge instructions, README, architecture notes, key Python/Go/React files, tests, scripts, Dockerfiles, and templates.

### Entry 3 - Candidate instructions confirmation

Date: 2026-06-17

Tool used: Codex

Prompt / request:

```text
have you read the candidate instructions.md?
```

Purpose:

Confirm that the candidate instructions had actually been read before project setup began.

What was understood from the response:

Both the root `CANDIDATE_INSTRUCTIONS.md` and the project copy at `acts-recruitment-challenge/CANDIDATE_INSTRUCTIONS.md` had been read and appeared to match.

Human input and judgement:

The user accepted this confirmation and moved on to project setup.

What was accepted from AI:

The confirmation that the instructions were read.

Verification:

Codex had already read both files with `Get-Content -Raw`.

### Entry 4 - Lab-book and private GitHub repo request

Date: 2026-06-17

Tool used: Codex

Prompt / request:

```text
ok good. I would like to start a private github repo for this please. Also, please make sure:
1) we create a lab book (named AI_USAGE_lab-book.md) that we maintain, in the style of AI_Usage.md that captures everything this md files suggests we need to capture (e.g. prompts, purpose of the prompt, what I understood from the prompt, and what was my input, etc), This should be maintained as we build on our work, and please remember to ask me questions if any of the entries in this lab_book are not clear for you.
2) Another lab book (named project_lab-book.md) to capture the history of developing this project, including things like (but not limited) to changes we make, decisions we take, problems we face, etc. Make it very readable and transparent please.
Please do this and report back to me
```

Purpose:

Create durable records for AI usage and project development history, and initialize a private GitHub repository for the work.

What was understood from the response:

The lab books should be living documents. `AI_USAGE_lab-book.md` should record AI prompts and how the output was used. `project_lab-book.md` should record development history, decisions, changes, and problems encountered.

Human input and judgement:

The user specified the filenames and the kind of information to capture. Codex chose a chronological format to keep the records readable and transparent.

What was accepted from AI:

Creation of the two lab-book files and an initial record of the work so far.

Verification:

Pending: files are being created now. Private GitHub repo creation depends on local Git/GitHub CLI availability and network/authentication.

Follow-up:

Codex created `AI_USAGE_lab-book.md` and `project_lab-book.md`, initialized a local git repository, staged the clean source tree, and created the initial commit. GitHub CLI was not available in WSL, so creating the private GitHub repository could not be completed from the available tooling in this step.

What changed manually / by Codex:

- Added this running AI usage lab book.
- Added `project_lab-book.md`.
- Added `*Zone.Identifier*` to `.gitignore` so Windows metadata streams are not committed.
- Initialized git and committed the initial repository state.

Verification:

Codex confirmed `git version 2.34.1` was available in WSL, confirmed the folder was not previously a git repository, then created commit `2c2b960` with message `Initial challenge setup`.

## Open Questions

- Which GitHub publishing route should be used next: install/authenticate GitHub CLI in WSL, or have the user create an empty private repository and provide the remote URL?

### Entry 5 - GitHub CLI local install

Date: 2026-06-17

Tool used: Codex

Prompt / request:

```text
install the github cli
```

Purpose:

Make GitHub CLI available so the private GitHub repository can be created and pushed from the WSL project environment.

What was understood from the response:

System-wide installation through `apt` was blocked because `sudo` requires a password. A local project install was a workable alternative.

Human input and judgement:

The user requested installation of GitHub CLI. Codex selected a local install because it avoided changing system packages without sudo access.

What was accepted from AI:

Download and use the official GitHub CLI Linux amd64 tarball for the current latest release.

What changed manually / by Codex:

- Downloaded GitHub CLI `v2.95.0` into `.tools/`.
- Downloaded the official checksum file.
- Verified the tarball checksum.
- Extracted the binary under `.tools/gh`.
- Added `.tools/` to `.gitignore`.

Verification:

Codex ran `.tools/gh/bin/gh --version`, which reported `gh version 2.95.0 (2026-06-17)`.

Open question:

GitHub authentication still needs to be checked or completed before creating the private repository.

### Entry 6 - Changes summary file

Date: 2026-06-17

Tool used: Codex

Prompt / request:

```text
please add another md file Changes.md, extremely succinct, that gives a list of all the changes made, essentially two lists - 1) files created 2) files modified, with a very brief description about each content of the list.
```

Purpose:

Create a compact project change summary that is easier to scan than the running lab books.

What was accepted from AI:

Creation of `Changes.md` with two sections: files created and files modified.

Verification:

Pending commit.

### Entry 7 - Dependency check and clearance

Date: 2026-06-17

Tool used: Codex

Prompt / request:

```text
ok good. now check if we have all the dependencies required to run/test the given project
```

Purpose:

Check whether the local WSL environment satisfied the project README requirements for running and testing the baseline system.

What was understood from the response:

The environment had Python, but Go and native WSL Node.js were missing. `npm` existed only via the Windows Node installation, and `frontend-react/node_modules` was not installed.

Human input and judgement:

The user then asked Codex to fix the dependencies.

Prompt / request:

```text
please fix the dependencies
```

Purpose:

Make the project runnable and testable in the current WSL workspace.

What was accepted from AI:

Codex installed local, project-scoped toolchains under `.tools/` instead of using system package installation, because `sudo` required a password.

What changed manually / by Codex:

- Installed Go `1.26.4` under `.tools/go`.
- Installed Node.js `v24.16.0` and npm `11.13.0` under `.tools/node`.
- Verified downloaded archives with SHA256 checksums before extraction.
- Fixed executable permissions on `scripts/*.sh`.
- Ran `./scripts/test.sh` with local Go and Node on `PATH`.

Verification:

`./scripts/test.sh` passed. Python tests, Go tests, and frontend TypeScript checks all completed successfully. `npm install` reported 2 baseline vulnerabilities, 1 moderate and 1 high, but the project checks passed.

What AI was uncertain about or could not do:

Codex did not address the npm audit findings yet because that may or may not fit the chosen challenge track.

### Entry 8 - Vite/esbuild audit trade-off

Date: 2026-06-17

Tool used: Codex

Prompt / request:

```text
what is this issue about. provide a summary please
```

Purpose:

Understand the npm audit finding before deciding whether to fix it immediately.

What was understood from the response:

The audit finding concerns Vite's dependency on a vulnerable esbuild version. The vulnerability affects local development server exposure through permissive CORS behavior and could allow a malicious web page to read responses from a local dev server.

Prompt / request:

```text
what is the estimate for running a controlled vite upgrade?
```

Purpose:

Estimate whether fixing the issue now would be a good use of challenge time.

What was accepted from AI:

A controlled Vite upgrade was estimated at 30-60 minutes, including dependency updates, lockfile refresh, frontend typecheck, full project checks, and UI smoke testing.

Prompt / request:

```text
since this issue would not obtrude our progress with the project, we would continue for now. If we take too much time in the project then we would come back to this vulnerability. does this sound as a reasonable trade-off?
```

Purpose:

Validate a decision to defer the audit fix and focus on the main challenge work.

Human input and judgement:

The user decided to continue with the project and revisit the vulnerability only if time allows.

What was accepted from AI:

Codex agreed that deferring was reasonable because the issue does not block tests or core simulation work, and the automated fix may require a breaking Vite upgrade.

Verification:

No code changes were made for this vulnerability. The finding remains a documented deferred item.

What AI was uncertain about or could not do:

Codex did not perform a Vite migration or smoke-test an upgraded frontend because the user chose to defer it.

### Entry 9 - Handover routine

Date: 2026-06-18

Tool used: Codex

Prompt / request:

```text
perform handover
```

Purpose:

Prepare the repository for another agent to continue from the current state.

What was understood from the response:

This is a handover-to-new-agent request, so the standing project protocol allows a commit and push after updating the handover records.

Human input and judgement:

The user explicitly requested the handover routine.

What was accepted from AI:

Codex updated the handover file and running logs to capture the current branch, remote, latest commit, verification state, deferred audit issue, and suggested next action.

Verification:

Codex checked `git status`, latest commit, branch, remote, and reran the baseline project checks before committing.

### Entry 10 - Model modularisation scoping

Date: 2026-06-18

Tool used: Codex

Prompt / request:

```text
Ok so, I want to:
1) modularize the code so that it becomes easier to implement unit tests and integration tests
2) I want to have a separate module for a) agent creation that also deals with agent behaviour, b) next movement routine that allows us to select from a range of different possibilities that are easy to implement and focus on and can be used by other modules/routines such as agent behaviour, c) random walk routine that can be used to model different kinds of random walks (i.e. seeded/deterministic, probability distribution, skewness, etc) d) Terrain handler that gives a bunch of different properties of cell (e.g. cells with fixed density, cells that can't be traversed i.e. restricted cells (based on agent's id), cells with penalty (depending on agent's id) for stresspassing, e) simulation metrics such as congestion, breach detected vs handled, cell density, etc 
read the above requirements and tell me if you can manage this. Along with and estimate on time required to do this. Make sure relevant prompts are documented in relevant book-keeping docs as expected. Thanks
```

Purpose:

Assess whether a Track A modelling refactor is manageable and estimate the time required before starting implementation.

What was understood from the response:

The user wants a modular Python model architecture that separates agent creation/behaviour, movement selection, random walk policies, terrain/cell rules, and simulation metrics, while making future unit and integration tests easier to write.

Human input and judgement:

The user provided the desired module boundaries and asked for feasibility and timing rather than immediate code changes.

What was accepted from AI:

Pending: Codex is inspecting the current model and tests before providing an estimate.

Verification:

Codex read the current Python model modules and existing Python tests before answering.

### Entry 11 - Full modularisation scope selected

Date: 2026-06-18

Tool used: Codex

Prompt / request:

```text
ok good. let us go forward with the full version of every idea listed. Give me a breakdown of your tasks, essentially and enumerated list focusing on what we are modularizing
```

Purpose:

Confirm that the modelling track should proceed with the full requested modularisation scope, and ask Codex to break the work into clear tasks before implementation.

What was understood from the response:

The user wants to proceed with the broader Track A implementation: separated modules for agents, movement, random walks, terrain, and metrics, plus tests that exercise those boundaries.

Human input and judgement:

The user chose the larger implementation scope after reviewing the estimate.

What was accepted from AI:

Pending: Codex will provide an enumerated implementation breakdown before source changes begin.

### Entry 12 - Blueprint document request

Date: 2026-06-18

Tool used: Codex

Prompt / request:

```text
ok good, can you save this as the main blueprint for what we want to implement in this project so that you and other ai agents can refer to in the future? make that file (perhaps an md file) tracked and visible in github. Make relevant entries in the lab books, and commit and push
```

Purpose:

Turn the modularisation breakdown into a tracked project blueprint and publish it to the GitHub repository.

What was understood from the response:

The user wants a durable Markdown file that future AI agents can treat as the implementation reference for the Track A modelling refactor.

Human input and judgement:

The user explicitly asked for the file to be tracked, committed, and pushed.

What was accepted from AI:

Codex created `MODEL_MODULARIZATION_BLUEPRINT.md` from the agreed task breakdown and updated the bookkeeping docs.

Verification:

Pending: commit and push will be checked with `git status` and `git log`.

### Entry 13 - Terrain map legend and asset tracking

Date: 2026-06-18

Tool used: Codex

Prompt / request:

```text
also add the fact that now we have a folder Terrain maps that should contain a png file of what the terrain should look like with specifics of different cell types. the legend being
1) Black == boundaries or cells that can never have any agents regardless of their ids. Think of it as a hard dirichlet condition that is reflective
2) Red == Restricted cells i.e. only specid agent ids are allowed in these cells. these ids are configurable as a parameter in the simulation
3) Orange == Cells with a maximum agent density configured as a parameter in the simulation. For our examples, these cells should be treated as a "gate" through which agents can pass through. 
4) Green == Cells where agents with a given (configurable ids) are taken out of the simulation. These could be used for example as exit gates at a plane terminal through which passengers can board the plane
5) Blue == cells with Type 1 penalty for agents traversing it. penalty would be configurable, such as decreased/increased movement in a specific direction. 
6) Pink == cells with Type 2 penalty for agents traversing it. penalty would be preset, i.e. always decreases movement in all directions. 

update these things in relevant books and commit and push
```

Purpose:

Record the terrain-map asset folder and its color legend as part of the modelling blueprint, then publish the tracked PNG and documentation changes.

What was understood from the response:

The user wants `Terrain maps/` to be a tracked project input folder containing PNG terrain layouts. The terrain module should eventually parse the PNG color legend into cell semantics.

Human input and judgement:

The user supplied the cell-type legend and explicitly asked for commit and push.

What was accepted from AI:

Codex documented the legend in `MODEL_MODULARIZATION_BLUEPRINT.md`, recorded the decision in bookkeeping docs, and prepared to track `Terrain maps/Terrain1.png`.

Verification:

Codex confirmed `Terrain maps/Terrain1.png` is a PNG image before committing.

### Entry 14 - Terrain map handler promoted to first implementation step

Date: 2026-06-18

Tool used: Codex

Prompt / request:

```text
Ok great. Make this implementation of the map handler as the first next step. and then update the breakdown that you created before we talked about this map handler
```

Purpose:

Update the project blueprint so terrain-map handling is the first implementation slice, reflecting the newly clarified PNG map input and frontend visualization requirements.

What was understood from the response:

The user wants the terrain map handler, map initialization tests, simulation metrics, and later frontend terrain visualization to lead the implementation plan.

Human input and judgement:

The user chose the terrain map handler as the first next step before the broader agent, movement, and random-walk refactor work.

What was accepted from AI:

Codex updated `MODEL_MODULARIZATION_BLUEPRINT.md` to reorder the implementation tasks and suggested implementation order around terrain map handling first.

### Entry 15 - Handover refresh for future agents

Date: 2026-06-18

Tool used: Codex

Prompt / request:

```text
good. update the handover docs so that any agent can pick it up from here
```

Follow-up prompt:

```text
commit and push after
```

Purpose:

Prepare the project for another AI agent to continue from the current planning state, with the terrain map handler clearly identified as the next implementation step.

What was understood from the response:

The user wants `HANDOVER.md` refreshed and wants the resulting documentation changes committed and pushed.

Human input and judgement:

The user explicitly authorized commit and push for this handover update.

What was accepted from AI:

Codex updated the handover instructions to reference `MODEL_MODULARIZATION_BLUEPRINT.md`, the selected Track A modelling scope, and the terrain-map-handler-first implementation sequence.

Verification:

Codex ran `./scripts/test.sh` with the local Go and Node toolchains on `PATH`; the command completed successfully.

### Entry 16 - README roadmap and handover preparation

Date: 2026-06-18

Tool used: Codex

Prompt / request:

```text
can we create a roadmap using these blueprints (including the next step breakdowns) with a completed, active, next state for them and maintain them in the readme for our github please? commit and push once done and then prep for handover
```

Purpose:

Make the project roadmap visible from the GitHub README and then refresh the handover state for future agents.

What was understood from the response:

The user wants a README roadmap that summarizes completed work, the active terrain map handler step, and next planned implementation slices.

Human input and judgement:

The user explicitly requested commit and push after the README roadmap update, followed by handover preparation.

What was accepted from AI:

Codex added a `Roadmap` section to `README.md`, based on `MODEL_MODULARIZATION_BLUEPRINT.md` and the terrain map handler breakdown.

Verification:

Codex ran `./scripts/test.sh` with the local Go and Node toolchains on `PATH`; the command completed successfully. Documentation commit and push will be checked with git status and log.

### Entry 17 - Changes.md classification clarification

Date: 2026-06-18

Tool used: Codex

Prompt / request:

```text
also, i can see that the changes.md should not have mentions of files that were created in the files modified list. Please can you make sure that we only include the files in the modified list if they were already present in the base code that we had not created ourselves but were modified? Do i make sense to you?
```

Purpose:

Clarify how `Changes.md` should classify files in its created and modified sections.

What was understood from the response:

The user wants `Changes.md` to remain a succinct audit of project-created files versus pre-existing base files modified during the work. Files created by this project should not be repeated under `Files Modified`.

Human input and judgement:

The user identified the classification issue and clarified the desired rule.

What was accepted from AI:

Codex cleaned `Changes.md` to remove created files from the modified-files section and recorded the rule in the lab books.

### Entry 18 - Handover after Changes.md cleanup

Date: 2026-06-18

Tool used: Codex

Prompt / request:

```text
good. prepare for handover. commit and push
```

Purpose:

Refresh the handover state after cleaning `Changes.md`, then commit and push the documentation updates.

What was understood from the response:

The user explicitly requested a handover preparation routine and authorized commit and push.

Human input and judgement:

The user confirmed the `Changes.md` cleanup and asked for the handover to be prepared.

What was accepted from AI:

Codex updated `HANDOVER.md` to include the latest state and the clarified `Changes.md` classification rule.

Verification:

Codex ran `./scripts/test.sh` with the local Go and Node toolchains on `PATH`; the command completed successfully.
