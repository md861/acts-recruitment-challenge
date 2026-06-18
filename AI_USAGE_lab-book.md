# AI Usage Lab Book

This lab book records how AI assistance is used during the ACTS recruitment challenge work. It follows the spirit of `docs/ai-usage-log-template.md`, but keeps a running, chronological record rather than only a final submission summary.

## Purpose

- Capture prompts and requests made to AI tools.
- Record why each prompt was asked.
- Record what was understood or accepted from the response.
- Record human input, judgement, corrections, and decisions.
- Record verification steps and any places where AI assistance was uncertain or unhelpful.

## Maintenance Protocol

- New entries should be appended in chronological order.
- New entries should use `Date/time:` with timezone where available.
- If an exact time was not recorded, use `Date/time: YYYY-MM-DD, time not recorded (Europe/London)`.
- Keep entry numbers unique and increasing.
- If a previous entry is corrected or reordered, add a maintenance entry explaining the correction.

## Running Log

### Entry 1 - Workspace orientation

Date/time: 2026-06-17, time not recorded (Europe/London)

Tool used: Codex

Prompt / request:

```text
do you see the pwd?
```

Purpose:

Confirm that Codex could see the expected working directory before inspecting or changing the project.

What was understood / accepted:

The active working directory was confirmed as `\\wsl.localhost\Ubuntu-22.04\home\mynk\Skyral_Tasks`.

Human input and judgement:

The user confirmed that this was the intended location.

Verification:

Codex ran `Get-Location` and reported the path.

### Entry 2 - Repository contents summary

Date/time: 2026-06-17, time not recorded (Europe/London)

Tool used: Codex

Prompt / request:

```text
ok great. read the contents and give me a summary about it
```

Purpose:

Understand the repository structure, challenge instructions, service layout, and likely improvement areas before beginning implementation work.

What was understood / accepted:

The project is a deliberately small ACTS take-home challenge containing a Python population model, Go integration API, React frontend, Docker Compose files, and starter Kubernetes notes.

Human input and judgement:

The user asked for a summary rather than changes, so no project files were modified.

Verification:

Codex read the challenge instructions, README, architecture notes, key Python/Go/React files, tests, scripts, Dockerfiles, and templates.

### Entry 3 - Candidate instructions confirmation

Date/time: 2026-06-17, time not recorded (Europe/London)

Tool used: Codex

Prompt / request:

```text
have you read the candidate instructions.md?
```

Purpose:

Confirm that the candidate instructions had actually been read before project setup began.

What was understood / accepted:

Both the root `CANDIDATE_INSTRUCTIONS.md` and the project copy at `acts-recruitment-challenge/CANDIDATE_INSTRUCTIONS.md` had been read and appeared to match.

Verification:

Codex had already read both files with `Get-Content -Raw`.

### Entry 4 - Lab-book and private GitHub repo request

Date/time: 2026-06-17, time not recorded (Europe/London)

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

What was understood / accepted:

Codex created `AI_USAGE_lab-book.md` and `project_lab-book.md`, initialized a local git repository, staged the clean source tree, and created the initial commit. GitHub CLI was not available in WSL at this point.

Human input and judgement:

The user specified the filenames and the kind of information to capture. Codex chose a chronological format.

Verification:

Codex confirmed `git version 2.34.1`, confirmed the folder was not already a git repository, and created commit `2c2b960 Initial challenge setup`.

### Entry 5 - GitHub CLI local install

Date/time: 2026-06-17, time not recorded (Europe/London)

Tool used: Codex

Prompt / request:

```text
install the github cli
```

Purpose:

Make GitHub CLI available so the private GitHub repository could be created and pushed from the WSL project environment.

What was understood / accepted:

System-wide installation through `apt` was blocked because `sudo` required a password. Codex installed GitHub CLI locally under ignored `.tools/`.

Verification:

Codex ran `.tools/gh/bin/gh --version`, which reported `gh version 2.95.0 (2026-06-17)`.

### Entry 6 - Changes summary file

Date/time: 2026-06-17, time not recorded (Europe/London)

Tool used: Codex

Prompt / request:

```text
please add another md file Changes.md, extremely succinct, that gives a list of all the changes made, essentially two lists - 1) files created 2) files modified, with a very brief description about each content of the list.
```

Purpose:

Create a compact project change summary that is easier to scan than the running lab books.

What was understood / accepted:

Codex created `Changes.md` with two sections: files created and files modified.

### Entry 7 - Dependency check and local tooling

Date/time: 2026-06-17, time not recorded (Europe/London)

Tool used: Codex

Prompt / request:

```text
ok good. now check if we have all the dependencies required to run/test the given project
```

Follow-up prompt:

```text
please fix the dependencies
```

Purpose:

Check whether the WSL environment could run and test the baseline project, then fix missing dependencies.

What was understood / accepted:

The environment had Python, but Go and native WSL Node.js were missing. Codex installed local, project-scoped Go and Node toolchains under `.tools/` rather than using system packages.

Verification:

`./scripts/test.sh` passed with local Go and Node on `PATH`. `npm install` reported baseline Vite/esbuild audit findings, which were not fixed in this step.

### Entry 8 - Vite/esbuild audit trade-off

Date/time: 2026-06-17, time not recorded (Europe/London)

Tool used: Codex

Prompt / request:

```text
what is this issue about. provide a summary please
```

Follow-up prompts:

```text
what is the estimate for running a controlled vite upgrade?
```

```text
since this issue would not obtrude our progress with the project, we would continue for now. If we take too much time in the project then we would come back to this vulnerability. does this sound as a reasonable trade-off?
```

Purpose:

Understand the npm audit finding before deciding whether to fix it immediately.

Human input and judgement:

The user decided to defer the Vite/esbuild vulnerability because it did not block the main challenge work.

What was accepted from AI:

Codex agreed that deferring was reasonable and estimated a controlled Vite upgrade at 30-60 minutes.

Verification:

No code changes were made for this vulnerability. The finding remains a documented deferred item.

### Entry 9 - Initial handover routine

Date/time: 2026-06-18, time not recorded (Europe/London)

Tool used: Codex

Prompt / request:

```text
perform handover
```

Purpose:

Prepare the repository for another agent to continue from the current state.

What was understood / accepted:

Codex updated the handover file and running logs with branch, remote, latest commit, verification state, deferred audit issue, and suggested next action.

Verification:

Codex checked `git status`, latest commit, branch, remote, and reran the baseline checks before committing.

### Entry 10 - Model modularisation scoping

Date/time: 2026-06-18, time not recorded (Europe/London)

Tool used: Codex

Prompt / request:

```text
Ok so, I want to:
1) modularize the code so that it becomes easier to implement unit tests and integration tests
2) I want to have a separate module for a) agent creation that also deals with agent behaviour, b) next movement routine that allows us to select from a range of different possibilities that are easy to implement and focus on and can be used by other modules/routines such as agent behaviour, c) random walk routine that can be used to model different kinds of random walks (i.e. seeded/deterministic, probability distribution, skewness, etc) d) Terrain handler that gives a bunch of different properties of cell (e.g. cells with fixed density, cells that can't be traversed i.e. restricted cells (based on agent's id), cells with penalty (depending on agent's id) for stresspassing, e) simulation metrics such as congestion, breach detected vs handled, cell density, etc 
read the above requirements and tell me if you can manage this. Along with and estimate on time required to do this. Make sure relevant prompts are documented in relevant book-keeping docs as expected. Thanks
```

Purpose:

Assess whether a Track A modelling refactor was manageable and estimate the time required before starting implementation.

What was understood / accepted:

Codex identified the requested module boundaries: agent creation/behaviour, movement selection, random walk policies, terrain/cell rules, and simulation metrics.

Verification:

Codex read the current Python model modules and existing Python tests before answering.

### Entry 11 - Full modularisation scope selected

Date/time: 2026-06-18, time not recorded (Europe/London)

Tool used: Codex

Prompt / request:

```text
ok good. let us go forward with the full version of every idea listed. Give me a breakdown of your tasks, essentially and enumerated list focusing on what we are modularizing
```

Purpose:

Confirm that the modelling track should proceed with the full requested modularisation scope and ask Codex to break the work into clear tasks.

Human input and judgement:

The user chose the larger implementation scope after reviewing the estimate.

What was accepted from AI:

Codex provided an implementation breakdown covering agents, movement, random walk, terrain, metrics, orchestration, configuration, snapshots, tests, and frontend terrain visualization.

### Entry 12 - Blueprint document request

Date/time: 2026-06-18, time not recorded (Europe/London)

Tool used: Codex

Prompt / request:

```text
ok good, can you save this as the main blueprint for what we want to implement in this project so that you and other ai agents can refer to in the future? make that file (perhaps an md file) tracked and visible in github. Make relevant entries in the lab books, and commit and push
```

Purpose:

Turn the modularisation breakdown into a tracked project blueprint and publish it to GitHub.

What was understood / accepted:

Codex created `MODEL_MODULARIZATION_BLUEPRINT.md`, updated the bookkeeping docs, committed, and pushed.

### Entry 13 - Terrain map legend and asset tracking

Date/time: 2026-06-18, time not recorded (Europe/London)

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

What was understood / accepted:

Codex documented the legend in `MODEL_MODULARIZATION_BLUEPRINT.md`, recorded the decision in bookkeeping docs, and tracked `Terrain maps/Terrain1.png`.

Verification:

Codex confirmed `Terrain maps/Terrain1.png` was a PNG image before committing.

### Entry 14 - Terrain map handler promoted to first implementation step

Date/time: 2026-06-18, time not recorded (Europe/London)

Tool used: Codex

Prompt / request:

```text
Ok great. Make this implementation of the map handler as the first next step. and then update the breakdown that you created before we talked about this map handler
```

Purpose:

Update the project blueprint so terrain-map handling became the first implementation slice.

What was understood / accepted:

Codex reordered the blueprint around PNG terrain handling, map initialization tests, terrain metrics, and later frontend visualization.

### Entry 15 - Handover refresh for future agents

Date/time: 2026-06-18, time not recorded (Europe/London)

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

Prepare the project for another AI agent to continue from the current planning state.

What was understood / accepted:

Codex updated `HANDOVER.md` to reference the blueprint, selected Track A modelling scope, and terrain-map-handler-first sequence, then committed and pushed.

Verification:

`./scripts/test.sh` passed with local Go and Node on `PATH`.

### Entry 16 - README roadmap and handover preparation

Date/time: 2026-06-18, time not recorded (Europe/London)

Tool used: Codex

Prompt / request:

```text
can we create a roadmap using these blueprints (including the next step breakdowns) with a completed, active, next state for them and maintain them in the readme for our github please? commit and push once done and then prep for handover
```

Purpose:

Make the project roadmap visible from the GitHub README and refresh handover state.

What was understood / accepted:

Codex added a `Roadmap` section to `README.md`, based on `MODEL_MODULARIZATION_BLUEPRINT.md`, and refreshed handover docs.

Verification:

`./scripts/test.sh` passed with local Go and Node on `PATH`.

### Entry 17 - Changes.md classification clarification

Date/time: 2026-06-18, time not recorded (Europe/London)

Tool used: Codex

Prompt / request:

```text
also, i can see that the changes.md should not have mentions of files that were created in the files modified list. Please can you make sure that we only include the files in the modified list if they were already present in the base code that we had not created ourselves but were modified? Do i make sense to you?
```

Purpose:

Clarify how `Changes.md` should classify files in its created and modified sections.

Human input and judgement:

The user identified the classification issue and clarified the desired rule.

What was accepted from AI:

Codex cleaned `Changes.md` to remove created files from the modified-files section and recorded the rule in the lab books.

### Entry 18 - Handover after Changes.md cleanup

Date/time: 2026-06-18, time not recorded (Europe/London)

Tool used: Codex

Prompt / request:

```text
good. prepare for handover. commit and push
```

Purpose:

Refresh the handover state after cleaning `Changes.md`, then commit and push documentation updates.

What was understood / accepted:

Codex updated `HANDOVER.md` with the latest state and the clarified `Changes.md` classification rule.

Verification:

`./scripts/test.sh` passed with local Go and Node on `PATH`.

### Entry 19 - Terrain map handler implementation

Date/time: 2026-06-18, time not recorded (Europe/London)

Tool used: Codex

Prompt / request:

```text
great. lets start with the first next step
```

Purpose:

Begin the active roadmap item: implementing the terrain map handler.

What was understood / accepted:

Codex added terrain cell vocabulary, terrain configuration fields, PNG map loading/parsing, color-to-cell mapping, and focused tests for `Terrain maps/Terrain1.png`.

Verification:

- `PYTHONPATH="$PWD/model-python" python3 -m unittest discover -s model-python/tests` passed.
- `PATH="$PWD/.tools/go/bin:$PWD/.tools/node/bin:$PATH" ./scripts/test.sh` passed.

### Entry 20 - Terrain map integration and metrics

Date/time: 2026-06-18, time not recorded (Europe/London)

Tool used: Codex

Prompt / request:

```text
ok. lets get on with the remaining tasks for this slice
```

Purpose:

Complete the remaining terrain-map-handler tasks: model snapshot metadata, integration tests, metrics hooks, and 100-tick terrain-map simulation coverage.

What was understood / accepted:

Codex integrated the terrain map into `PopulationModel`, added terrain-aware metrics, exposed additive snapshot metadata, and added deterministic model integration coverage.

Verification:

- `PYTHONPATH="$PWD/model-python" python3 -m unittest discover -s model-python/tests` passed.
- `PATH="$PWD/.tools/go/bin:$PWD/.tools/node/bin:$PATH" ./scripts/test.sh` passed.

### Entry 21 - Terrain visualization and GIF request

Date/time: 2026-06-18, time not recorded (Europe/London)

Tool used: Codex

Prompt / request:

```text
ok great. can we use the new map handler to create the cells as suggested by terrain 1 png file? and produce a gif of first 100 ticks of the simulation rendered by the visualization front end?
```

Purpose:

Use the terrain map handler as the source of terrain cell definitions, connect terrain metadata through API/frontend visualization, and produce a first-100-ticks GIF.

What was understood / accepted:

Codex updated the model, API contract, frontend terrain visualizer, and added a reproducible Python GIF renderer. Browser automation, ffmpeg, and ImageMagick were not available, so the GIF was generated through a project script rather than browser capture.

Verification:

- Generated `artifacts/terrain1_first_100_ticks.gif`.
- `file` reported the artifact as GIF89a, 640 x 443.
- The GIF decoded successfully through the local image viewer.
- `PATH="$PWD/.tools/go/bin:$PWD/.tools/node/bin:$PATH" ./scripts/test.sh` passed.

### Entry 22 - Artifact protocol and terrain boundary update

Date/time: 2026-06-18, time not recorded (Europe/London)

Tool used: Codex

Prompt / request:

```text
1) I would not like to unnecessarily populate the artifacts directory in github as the files may be too big and too many in the future. for now keep this dir untracked unless specified explicitly. add this in the handover notes as part of development protocol.
2) I have checked the gif in artifacts dir. It has issues following issues: a) The legends are not visible in the gif but are visible in the web browser. The cells seem to be indistinguishible from each other in the simulation domain, c) the cell shading should not be solid, instead should be as shown in the legend with lines and not solid fills. d) the agents are being initialized at the top left corner of the simulation, I want them to be within the main simulation block which is bounded by the black outlines. 
For now make a not of these issues that we will get back to, and as a next step, I want to add an extra color coding in the terrain map handler as follows:
1)  Define the black cells such that no agent is initialized outside the area enclosed by these black cells. These cells are only used to define the outer boundaries of the simulation block
2) Define brown cells to represent cells with cell density = 0, and treat them as a reflective boundary that does not allow agents to pass through them regardless of their ids
3) add a check in the handler to make sure that no cell definitions are outside of the black outer boundaries. If detected otherwise, generate an issue that the map is erroneous.
Can we do that for now?
```

Purpose:

Keep generated artifacts out of Git by default, record known GIF issues, and update terrain semantics for black and brown cells.

Human input and judgement:

The user reviewed the generated GIF, identified usability issues, and clarified new terrain semantics.

What was accepted from AI:

Codex added `artifacts/` to `.gitignore`, documented the protocol and known GIF issues, added brown density-zero terrain handling, added black-boundary enclosure checks, and added validation tests.

Verification:

- `PYTHONPATH="$PWD/model-python" python3 -m unittest discover -s model-python/tests` passed.
- `PATH="$PWD/.tools/go/bin:$PWD/.tools/node/bin:$PATH" ./scripts/test.sh` passed.

### Entry 23 - README unfixed issues list

Date/time: 2026-06-18, time not recorded (Europe/London)

Tool used: Codex

Prompt / request:

```text
ok for now keep it as an unfixed issue. I would like to maintain a list of these unfixed issues in the readme for github please? commit and push and prepare for handover
```

Purpose:

Record the browser visualizer parity gap as a known unfixed issue in the GitHub README and prepare handover.

What was understood / accepted:

Codex added an `Unfixed Issues` section to `README.md` and refreshed handover/bookkeeping docs.

Verification:

- `PYTHONPATH="$PWD/model-python" python3 -m unittest discover -s model-python/tests` passed.
- `PATH="$PWD/.tools/go/bin:$PWD/.tools/node/bin:$PATH" ./scripts/test.sh` passed.

### Entry 24 - Bookkeeping stale-state protocol and next-step check

Date/time: 2026-06-18, time not recorded (Europe/London)

Tool used: Codex

Prompt / request:

```text
ok great. 
1) make sure before we commit and push, or do a handover prep, we update relevant book-keeping docs, check for stale states in them. Add this as an entry under the dev protocol in handover doc. 
2) read the blueprint and tell me what is next.
```

Purpose:

Add a development protocol for bookkeeping freshness and identify the next implementation step from the blueprint.

Human input and judgement:

The user identified a recurring process risk around stale documentation.

What was accepted from AI:

Codex updated `HANDOVER.md` with the bookkeeping stale-state protocol and reread the blueprint/README roadmap before answering.

### Entry 25 - Agent creation and placement refactor

Date/time: 2026-06-18 15:15 BST (Europe/London)

Tool used: Codex

Prompt / request:

```text
ok great. commit and push. and then get on with the next steps. keep working until step 5 in your list that is "Add unit tests for deterministic creation and terrain-aware placement.". prompt before moving to step 6. thanks
```

Purpose:

Commit and push the bookkeeping protocol, then implement the next blueprint slice through unit tests for deterministic agent creation and terrain-aware placement.

What was understood / accepted:

Codex added `AgentFactory`, moved creation/placement out of `PopulationModel`, added terrain-aware placement tests, and updated bookkeeping docs.

Human input and judgement:

The user explicitly set the stopping point before step 6.

Verification:

- `PYTHONPATH="$PWD/model-python" python3 -m unittest discover -s model-python/tests` passed.
- `PATH="$PWD/.tools/go/bin:$PWD/.tools/node/bin:$PATH" ./scripts/test.sh` passed.

### Entry 26 - Agent factory commit and handover request

Date/time: 2026-06-18 15:16 BST (Europe/London)

Tool used: Codex

Prompt / request:

```text
ok good. commit and push and prep for handover.
```

Purpose:

Commit and push the agent creation/placement refactor and refresh handover state.

What was understood / accepted:

Codex reran checks, updated handover/bookkeeping docs, committed `bef3fee Refactor agent creation and placement`, and pushed it.

Verification:

- `PYTHONPATH="$PWD/model-python" python3 -m unittest discover -s model-python/tests` passed.
- `PATH="$PWD/.tools/go/bin:$PWD/.tools/node/bin:$PATH" ./scripts/test.sh` passed.

### Entry 27 - Last implemented and roadmap checks

Date/time: 2026-06-18, time not recorded (Europe/London)

Tool used: Codex

Prompt / request:

```text
check what was last implemented
```

Follow-up prompt:

```text
what's next on our roadmap
```

Purpose:

Confirm the most recent implementation and identify the next roadmap item before starting new work.

What was understood / accepted:

Codex checked git history, working tree state, `HANDOVER.md`, and the README roadmap. The latest committed implementation was agent creation/placement, and the next roadmap step was agent behaviour profiles.

Verification:

Codex inspected `git log`, `git status`, `HANDOVER.md`, `Changes.md`, and the relevant model/test files.

### Entry 28 - Agent behaviour profile implementation

Date/time: 2026-06-18 20:04 BST (Europe/London)

Tool used: Codex

Prompt / request:

```text
let's get on with step 6 then
```

Purpose:

Continue the Track A modelling roadmap by implementing agent behaviour profiles after the agent creation and placement refactor.

What was understood / accepted:

Codex added `population_model/behaviour.py`, wired `PopulationModel._next_movement` through default behaviour profiles, and added focused behaviour tests.

Human input and judgement:

The user selected the next roadmap step. Codex chose a minimal module boundary and kept the existing movement choices compatible with previous behaviour.

Verification:

- `PYTHONPATH=model-python python3 -m unittest discover -s model-python/tests` passed with 18 tests.
- `PATH="$PWD/.tools/go/bin:$PWD/.tools/node/bin:$PATH" ./scripts/test.sh` passed.

### Entry 29 - Agent behaviour profiles commit and push

Date/time: 2026-06-18 20:08 BST (Europe/London)

Tool used: Codex

Prompt / request:

```text
commit and push
```

Purpose:

Commit and push the completed step 6 behaviour-profile slice.

What was understood / accepted:

Codex staged only the behaviour-profile code, tests, and bookkeeping docs, excluded the unrelated untracked `Terrain maps/Terrain1_00.png`, committed `55798e2 Add agent behaviour profiles`, and pushed `main`.

Verification:

`git status --short` showed only the pre-existing untracked `Terrain maps/Terrain1_00.png` after the push.

### Entry 30 - AI usage log ordering and timestamp repair

Date/time: 2026-06-18 20:14 BST (Europe/London)

Tool used: Codex

Prompt / request:

```text
Why do we not see the last few important prompts (for the last two steps I believe step 5 and step 6) in the AI_USAGE labbook?
```

Follow-up prompt:

```text
yes fix the order please. and perhaps include a timestamp in this lab book as well when you are inserting the entries to help future maintainance and transparancy
```

Purpose:

Repair the AI usage lab book after duplicated/out-of-order entry numbers made recent prompts hard to find.

What was understood / accepted:

Codex reordered the AI usage entries into chronological sequence, made entry numbers unique, added this maintenance protocol, and switched entries to `Date/time:` fields. Exact timestamps were added where available from commits, handover records, or the current shell clock; older entries with no recorded time were marked as time not recorded.

Human input and judgement:

The user identified the transparency issue and requested a maintainable timestamp convention.

Verification:

Codex checked the entry list with `grep -n '^### Entry' AI_USAGE_lab-book.md`, reviewed the step 5 and step 6 entries in place, and checked the documentation-only diff/status.

### Entry 31 - Movement strategy module and test protocol

Date/time: 2026-06-18 20:22 BST (Europe/London)

Tool used: Codex

Prompt / request:

```text
good. lets keep moving
```

Follow-up prompt:

```text
make sure you are creating relevant unit and integration tests for each new module added. This should be part of the development protocol.
```

Purpose:

Continue the roadmap by implementing movement strategy selection and record the expectation that new modules need focused tests.

What was understood / accepted:

Codex added `population_model/movement.py`, moved terrain-aware allow/block movement decisions out of `PopulationModel`, added movement decision reason metadata, added focused unit tests for the movement module, and added a model-level integration test proving movement-strategy block reasons update metrics.

Human input and judgement:

The user clarified a development protocol: every new module should have relevant unit tests and, when it touches orchestration or cross-module behaviour, integration coverage as well.

Verification:

- `PYTHONPATH=model-python python3 -m unittest discover -s model-python/tests` passed with 25 tests.
- `PATH="$PWD/.tools/go/bin:$PWD/.tools/node/bin:$PATH" ./scripts/test.sh` passed.

### Entry 32 - Configurable random walk policies

Date/time: 2026-06-18 20:31 BST (Europe/London)

Tool used: Codex

Prompt / request:

```text
ok good. let's get on with the next step
```

Purpose:

Continue the Track A blueprint after movement strategy selection by implementing configurable random walk policies.

What was understood / accepted:

Codex added `population_model/random_walk.py`, introduced `RandomWalkPolicy`, and wired behaviour profiles through random walk policies rather than direct random choice. The implementation supports deterministic seeded choice, uniform policies, weighted policies, wait probability, and directional skew.

Human input and judgement:

The user approved continuing to the next blueprint item after the movement strategy slice.

Verification:

- `PYTHONPATH=model-python python3 -m unittest discover -s model-python/tests` passed with 32 tests.
- `PATH="$PWD/.tools/go/bin:$PWD/.tools/node/bin:$PATH" ./scripts/test.sh` passed.

### Entry 33 - Doxygen-compatible module headers

Date/time: 2026-06-18 20:31 BST (Europe/London)

Tool used: Codex

Prompt / request:

```text
Looking at the summary of coverage added for the random_walk that you have listed above, I feel like it would have been a great idea to create a doxygen compatible comment header at the beginning of each such module that we have added (and modified) so that we can compile them into a doxygen created documentation as an added readability to the code. Can we do that? is it possible to add this now and maintain/update as we go forward? if yes, then, for now just add the header for the modules and report back to me.
```

Purpose:

Add documentation headers that can later feed Doxygen-generated documentation and establish a maintenance convention for future module edits.

What was understood / accepted:

Codex added concise Doxygen-compatible file headers to the Python population model modules using `## @file` and `@brief` comments, and added the convention to the handover development protocol.

Human input and judgement:

The user identified a documentation quality improvement tied to the modules being added during the Track A work.

Verification:

`PYTHONPATH=model-python python3 -m unittest discover -s model-python/tests` passed with 32 tests.

### Entry 34 - Changes.md overlap protocol

Date/time: 2026-06-18 20:43 BST (Europe/London)

Tool used: Codex

Prompt / request:

```text
good. put this sanity check as part of protocol docs for future. then tell me what is next
```

Purpose:

Record the `Changes.md` no-overlap sanity check as a future protocol and identify the next roadmap item.

What was understood / accepted:

Codex added a handover protocol rule requiring future agents to check that no filename appears in both the created and modified lists after updating `Changes.md`.

Human input and judgement:

The user wants the classification rule to be mechanically maintained, not just remembered conversationally.

Verification:

Before adding the protocol rule, Codex confirmed `Changes.md` had `NO_OVERLAP`, with 18 created entries and 13 modified entries.

### Entry 35 - Remaining Step 4 agent creation work

Date/time: 2026-06-18 20:55 BST (Europe/London)

Tool used: Codex

Prompt / request:

```text
ok let's get on with the remaining tasks for this step.
```

Purpose:

Complete the unfinished parts of main blueprint Step 4, `Add an agent creation module`.

What was understood / accepted:

Codex completed behaviour profile lookup inside `AgentFactory`, added optional `behaviour_profile` metadata to agents, passed that metadata through the model snapshot, Go API contract, and frontend type, and added tests for configured profile lookup plus placement across allowed non-black terrain cell types.

Human input and judgement:

The user asked to finish the first unfinished main-blueprint step after explicitly clarifying that future `what's next` answers should refer to the main blueprint task list.

Verification:

- `PYTHONPATH=model-python python3 -m unittest discover -s model-python/tests` passed with 34 tests.
- `PATH="$PWD/.tools/go/bin:$PWD/.tools/node/bin:$PATH" ./scripts/test.sh` passed.

### Entry 36 - Remaining Step 5 agent behaviour work

Date/time: 2026-06-18 21:07 BST (Europe/London)

Tool used: Codex

Prompt / request:

```text
looks good. let's get on with it
```

Follow-up prompt:

```text
please add these description notes as doxygen comments as well. thanks
```

Purpose:

Complete the unfinished parts of main blueprint Step 5 by making behaviour profiles actively influence movement and documenting the new selector behaviour.

What was understood / accepted:

Codex added `BehaviourMoveSelector`, wired `PopulationModel` to select movement through behaviour profiles and movement strategy, added Doxygen-style comments to the new behaviour/random-walk helpers, and added tests for civilian avoidance, staff waiting preference, patrol restricted-cell intent, and all-blocked fallback.

Human input and judgement:

The user approved the implementation plan and requested that the descriptive notes be preserved as Doxygen-compatible comments.

Verification:

- `PYTHONPATH=model-python python3 -m unittest discover -s model-python/tests` passed with 38 tests.
- `PATH="$PWD/.tools/go/bin:$PWD/.tools/node/bin:$PATH" ./scripts/test.sh` passed.

### Entry 37 - Remaining Step 6 movement strategy work

Date/time: 2026-06-18 21:13 BST (Europe/London)

Tool used: Codex

Prompt / request:

```text
perfect. let's keep moving
```

Purpose:

Complete the unfinished parts of main blueprint Step 6 by applying terrain costs/preferences in movement decisions.

What was understood / accepted:

Codex added movement decision penalty metadata and preference costs, implemented Type 1 directional and Type 2 all-direction penalty costing, updated behaviour selection to prefer lower-cost allowed moves, and added focused movement/behaviour tests.

Human input and judgement:

The user asked to continue through the main blueprint's next unfinished step.

Verification:

- `PYTHONPATH=model-python python3 -m unittest discover -s model-python/tests` passed with 41 tests.
- `PATH="$PWD/.tools/go/bin:$PWD/.tools/node/bin:$PATH" ./scripts/test.sh` passed.

### Entry 38 - Remaining Step 8 terrain module work

Date/time: 2026-06-18 21:21 BST (Europe/London)

Tool used: Codex

Prompt / request:

```text
good what's next
```

Follow-up prompt:

```text
explain what you suggest for each remaining test. Then get on with the tasks and capture the suggestions in doxygen comments as before. Once done, commit and push and prep for handover. thanks
```

Purpose:

Identify the next unfinished main-blueprint task and complete the remaining terrain-module work.

What was understood / accepted:

Codex identified Step 8 as the next unfinished main-blueprint task, proposed role-based restrictions, terrain traversal classification, terrain effect metadata, and focused tests, then implemented role/id restricted-cell rules, traversal classification, movement-strategy consumption of terrain classifications, and relevant terrain/movement/behaviour tests.

Human input and judgement:

The user asked for the proposed test/task breakdown before implementation and requested Doxygen comments for the design notes.

Verification:

- `PYTHONPATH=model-python python3 -m unittest discover -s model-python/tests` passed with 42 tests.
- `PATH="$PWD/.tools/go/bin:$PWD/.tools/node/bin:$PATH" ./scripts/test.sh` passed.

### Entry 39 - Step 9 metrics module work

Date/time: 2026-06-18 21:33 BST (Europe/London)

Tool used: Codex

Prompt / request:

```text
so the next step now is step 9 correct? if so, let us keep moving
```

Purpose:

Confirm that main blueprint Step 9, `Add a metrics module`, was the next unfinished item and continue implementation.

What was understood / accepted:

Codex expanded `TerrainMetrics` with cell density snapshots, congestion counts, congested cells, unresolved breach accounting, event counters, and per-agent time spent by terrain cell type. Codex wired model initialization/reset/tick progression to refresh density metrics, carried breach handling metadata through movement decisions, and added focused metrics unit tests plus snapshot-level model assertions.

Human input and judgement:

The user confirmed the next step from the main blueprint and asked Codex to proceed.

Verification:

- `PYTHONPATH="$PWD/model-python" python3 -m unittest discover -s model-python/tests` passed with 45 tests.
- `./scripts/test.sh` passed across Python, Go, and frontend typecheck.

### Entry 40 - Step 10 model orchestration refactor

Date/time: 2026-06-18 21:41 BST (Europe/London)

Tool used: Codex

Prompt / request:

```text
good. keep moving
```

Purpose:

Continue from the main blueprint after Step 9 and complete Step 10, `Refactor model orchestration`.

What was understood / accepted:

Codex refactored `PopulationModel` so initialization/reset share a deterministic runtime setup path and `step()` delegates tick progression, per-agent advancement, movement application, metric recording, and density updates to focused helpers. Snapshot shape and movement behaviour were preserved.

Human input and judgement:

The user approved continuing to the next unfinished main-blueprint item.

Verification:

- `PYTHONPATH="$PWD/model-python" python3 -m unittest model-python/tests/test_model.py` passed with 5 tests.
- `./scripts/test.sh` passed across Python, Go, and frontend typecheck.

### Entry 41 - Steps 13 and 14 test coverage

Date/time: 2026-06-18 21:46 BST (Europe/London)

Tool used: Codex

Prompt / request:

```text
ok get on with steps 13 and 14 and then report back
```

Purpose:

Complete main blueprint Step 13, `Add module-level unit tests`, and Step 14, `Add model-level integration tests`.

What was understood / accepted:

Codex reviewed the existing test inventory, added focused configuration parsing unit tests, fixed a discovered float environment parsing bug, and added model integration tests for configured restricted-cell access by agent id and role plus API-compatible snapshot shape.

Human input and judgement:

The user directed Codex to proceed with both test-focused blueprint steps and report back once complete.

Verification:

- `PYTHONPATH="$PWD/model-python" python3 -m unittest discover -s model-python/tests` passed with 51 tests.
- `./scripts/test.sh` passed across Python, Go, and frontend typecheck.

### Entry 42 - Step 15 frontend terrain visualization

Date/time: 2026-06-18 21:56 BST (Europe/London)

Tool used: Codex

Prompt / request:

```text
ok good. get on with the tasks for this step. also make sure that by default we always create a 100 tick gif whenever we run the simulation. The number of ticks is configurable but default is 100. Add doxygen compatible comments for this step as well.
```

Purpose:

Complete main blueprint Step 15, `Add frontend terrain visualization`, and make terrain GIF preview generation part of the default simulation startup flow.

What was understood / accepted:

Codex replaced the raw terrain image view with a browser canvas that reads the snapshot-provided terrain asset and applies the GIF-style terrain color/stripe markings, kept agents overlaid on top, added compact terrain metrics to the control panel, made GIF tick count/output configurable with a 100-tick default, and added Doxygen-compatible comments to the touched frontend and script files.

Human input and judgement:

The user requested that GIF generation become a default part of running the simulation while keeping the tick count configurable.

Verification:

- `SIM_GIF_TICKS=2 python3 scripts/render-terrain-gif.py --ticks 2 --output artifacts/test_step15_preview.gif` generated a smoke-test GIF.
- `npm --prefix frontend-react run test` passed.
- `PYTHONPATH="$PWD/model-python" python3 -m unittest discover -s model-python/tests` passed with 51 tests.
- `bash -n scripts/start.sh scripts/test.sh` passed.
- `./scripts/test.sh` passed across Python, Go, and frontend typecheck.

### Entry 43 - Step 15 issue fixes and commit request

Date/time: 2026-06-18 22:04 BST (Europe/London)

Tool used: Codex

Prompt / request:

```text
good. commit and push.
one issue detected - the blue cell has mixed coloring style in the frontend, i.e. it has both solid and striped cells. please fix the issue.
anothe issue detected - the sample giff generated is only 2 steps long while expected is 100 ticks. please review and fix.
report after finishing
```

Purpose:

Fix the reported Step 15 visualization/GIF issues, then commit and push the completed work.

What was understood / accepted:

Codex fixed the frontend Type 1 blue terrain stripe calculation by using positive modulo semantics that match the Python GIF renderer. Codex also regenerated the default GIF artifact and verified it contains 100 frames.

Human input and judgement:

The user identified the visual inconsistency and clarified that the generated sample GIF should be 100 ticks by default.

Verification:

- `python3 scripts/render-terrain-gif.py` regenerated `artifacts/terrain1_first_100_ticks.gif`.
- Frame check reported `frames=100`.
- `npm --prefix frontend-react run test` passed.
- `./scripts/test.sh` passed across Python, Go, and frontend typecheck.

### Entry 44 - Simulation analysis plots and 500-tick defaults

Date/time: 2026-06-18 22:21 BST (Europe/London)

Tool used: Codex

Prompt / request:

```text
now that we have a decent working repo, i want to create simulation analysis plots, heatmaps etc that I would need for my report. Here is a list of metrics I want in the analysis: terrain overlay heatmaps, role-specific metrics, congestion plots, exit curves, and deterministic replay evidence

Check what metrics we already have. implement the remaining ones. And then create a module to plot that has these metrics in one place. Then make sure this plot is created for every instance we run start.sh. Make the default tick count for the gif and for these analysis plots to be 500. Complete these tasks and report
```

Follow-up prompt:

```text
add a doxygen compatible comment next to these new implemented metrics as well please
```

Purpose:

Add report-ready simulation analysis metrics and artifacts, update artifact defaults to 500 ticks, and document the new metric fields.

What was understood / accepted:

Codex added cumulative terrain heatmap and role-specific metrics, implemented a dependency-free analysis module and CLI report renderer, wired default analysis generation into `start.sh`, updated GIF defaults to 500 ticks, and added Doxygen-compatible comments next to the new metrics.

Human input and judgement:

The user specified the required analysis outputs and requested explicit Doxygen-compatible comments for newly implemented metrics.

Verification:

- `python3 scripts/render-terrain-gif.py` generated `artifacts/terrain1_first_500_ticks.gif`.
- GIF frame check reported `frames=500`.
- `python3 scripts/render-analysis-plots.py` generated `artifacts/simulation_analysis_500_ticks.html`.
- `./scripts/test.sh` passed with 53 Python tests, Go tests, and frontend typecheck.

### Entry 45 - Doxygen documentation setup

Date/time: 2026-06-18 22:49 BST (Europe/London)

Tool used: Codex

Prompt / request:

```text
create a dir for doxygen documentation. compile the documentation with standard doxygen cofig and commit and push
```

Purpose:

Add a Doxygen documentation directory and standard configuration for compiling source documentation.

What was understood / accepted:

Codex added `docs/doxygen/Doxyfile`, `docs/doxygen/README.md`, and ignored `docs/doxygen/build/`. The config targets Python model sources/tests, scripts, frontend source, Go internal contracts, README, and the modularization blueprint.

Human input and judgement:

The user explicitly requested documentation setup, compilation, commit, and push.

Verification / limitation:

- `doxygen docs/doxygen/Doxyfile` was attempted but failed because `doxygen` is not installed.
- Installing Doxygen was blocked because passwordless `sudo` is unavailable in the WSL environment.
- `git diff --check` passed.
