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

Date: 2026-06-17

What happened:

Codex inspected the workspace and confirmed that the active directory was `\\wsl.localhost\Ubuntu-22.04\home\mynk\Skyral_Tasks`.

Decision:

Proceed by inspecting the project before making changes.

Reasoning:

The challenge asks for good engineering judgement and preserving the working baseline. Understanding the system first reduces the risk of making a broad or misaligned change.

Problems or observations:

The workspace contains Windows `Zone.Identifier` metadata entries. These are not project source files and should be ignored.

### Entry 2 - Repository summary

Date: 2026-06-17

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

Date: 2026-06-17

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

Date: 2026-06-17

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
