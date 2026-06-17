# ACTS Take-Home Technical Challenge

Thank you for taking the time to complete this exercise.

This challenge is designed to resemble the kind of work we do when building collective training tools: composing models, integration services, user interfaces, and deployment infrastructure into something that can be run, inspected, improved, and trusted.

It is intentionally small. We do not expect production polish everywhere. We are interested in how you understand the system, choose a sensible improvement, use your time, verify your changes, and explain trade-offs.

Please spend no more than one working day on this challenge.

## Scenario

You have inherited a simple proof-of-concept training simulation.

The system contains:

- A Python population model.
- A Go integration API.
- A React frontend.

The Python model simulates a small number of agents moving around a 2D lattice. The Go API reads snapshots from the model and exposes them to the frontend. The frontend displays the current state and provides a few controls.

The system works, but it is deliberately simplistic. Your task is to improve it in a way that fits your role specialism.

## Getting Started

Run the demo:

```bash
./scripts/start.sh
```

Open:

```text
http://localhost:5173
```

You should see agents moving around a simple lattice.

Run the lightweight checks:

```bash
./scripts/test.sh
```

If something does not work on your machine, please document what happened and how you worked around it.

## Choose One Track

Please complete the track that matches the role you are interviewing for.

### Track A: Modelling and Simulation Engineer

Focus on improving the Python model.

The current model is a toy random walk. It has no meaningful intent, limited environmental interaction, and only basic state. Improve it so that it is still simple, but more representative of something that could support collective training.

Possible directions:

- Add goal-directed movement.
- Add terrain, restricted areas, or routes.
- Add agent roles and behaviours.
- Add congestion, collision avoidance, grouping, or queues.
- Add deterministic scenario configuration and repeatable tests.
- Add model-level validation or simple behavioural metrics.

Example issue:

> The model currently includes restricted cells in the snapshot, but agents do not make intelligent use of them. A useful improvement would make agent movement respond to terrain or scenario intent in a clear and testable way.

### Track B: Integration / Fullstack Software Engineer

Focus on the Go API, data contracts, and/or React UI.

The current integration is intentionally thin. The frontend polls snapshots and assumes the shape and timing of the model data are fine. Improve the system so it behaves more like a usable integration layer for a training tool.

Possible directions:

- Add clearer API contracts and validation.
- Improve error handling when the model is unavailable or returns bad data.
- Add pause, reset, step, speed, or scenario controls.
- Add server-sent events or another better update mechanism.
- Improve the UI so simulation state is easier to understand.
- Add tests around model-to-API mapping.

Example issue:

> The API currently acts mostly as a pass-through. A useful improvement would make it more robust against model failures, bad snapshots, timing issues, or frontend misuse.

### Track C: Platform Engineer

Focus on packaging and running the system in a local Kubernetes-style environment.

The current system runs as local processes. Improve its deployment shape so another engineer can run it predictably on k3d, Kubernetes, or a similar local environment.

Possible directions:

- Add Dockerfiles or improve the supplied ones.
- Add Kubernetes manifests or a small Helm chart.
- Add health and readiness probes.
- Add ConfigMaps for runtime configuration.
- Add a short k3d runbook.
- Add logs, metrics, or operational checks.
- Make startup order, ports, and failure modes clearer.

Example issue:

> The PoC has services, ports, and config, but no reliable platform story. A useful improvement would make the system easy to deploy, inspect, and restart locally.

## AI Tooling

You are encouraged to use AI tools such as Claude, Codex, ChatGPT, or Copilot.

We care about how you use them.

Please include an `AI_USAGE.md` file in your submission. Use [docs/ai-usage-log-template.md](./docs/ai-usage-log-template.md) as a starting point.

We would like to understand:

- What prompts you wrote.
- How you broke down the problem.
- What AI-generated code or advice you accepted.
- What you changed manually.
- How you verified the output.
- Where the AI tool was unhelpful or wrong.

Using AI well is a strength. Submitting unverified AI output is not.

## What to Submit

Please send back a zip file containing:

- Your modified repository.
- A `SOLUTION_NOTES.md` file explaining what you changed and why.
- An `AI_USAGE.md` file.
- Any tests, scripts, manifests, or docs needed to run your solution.

Your solution should be runnable locally. Please keep setup simple and document anything unusual.

You can use [docs/solution-notes-template.md](./docs/solution-notes-template.md) if helpful.

## What We Are Looking For

We are not looking for the largest possible change.

We are looking for:

- A working baseline preserved or improved.
- A clear, role-relevant improvement.
- Evidence that you understood the existing system.
- Sensible tests or verification.
- Good engineering judgement and trade-offs.
- Clear communication.

Small, coherent, well-tested improvements are better than ambitious unfinished rewrites.
