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

## Open Questions

- None at the moment. Future entries should ask the user for clarification where human intent, rationale, or manual decision-making is unclear.

