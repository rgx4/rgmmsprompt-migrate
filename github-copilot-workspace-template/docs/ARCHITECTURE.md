# Architecture

## Purpose

This repository is a **workspace orchestration layer** for GitHub Copilot CLI. It is intended to sit above multiple independent Git repositories that already have useful local documentation, instructions, agents, and skills.

The root coordinates work. Child repositories own their implementation knowledge.

## Core design

```text
                         user
                          │
                          ▼
                  Copilot at root
                          │
                 workspace process
                          │
              ┌───────────┴───────────┐
              │                       │
              ▼                       ▼
       child repository A      child repository B
       local authority          local authority
       local agents/skills      local agents/skills
       code/tests/docs          code/tests/docs
              │                       │
              └───────────┬───────────┘
                          │
                  cross-repo boundary
```

The root should know **how to discover and coordinate** the child repositories, not **how each application is implemented**.

## Authority

### Workspace layer owns

- repository discovery and routing;
- cross-repository research and planning;
- responsibility boundaries between research, investigation, implementation, and review;
- context-efficiency practices;
- the workspace routing map (`WORKSPACE.md`);
- generic prompts and adoption guidance.

### Child repository owns

- architecture and domain rules;
- technology/framework conventions;
- build, test, lint, type-check, migration, deployment, and release commands;
- local CI behavior;
- repository-specific security/compliance rules;
- local agents and skills;
- path-specific instructions;
- actual code and tests.

`WORKSPACE.md` must never become a second copy of these local details.

## Working from the root

GitHub's current Copilot CLI best-practices documentation explicitly supports running from a parent directory that contains multiple child repositories. This is the canonical operating model for this template.

Starting from the root provides access to files in child repositories under the workspace. It does not justify assuming that every descendant repository's custom agents/skills are globally loaded.

### Loading child custom agents and skills

Current Copilot CLI documentation states that `/add-dir` and `--add-dir` both:

- allow file access to the added root; and
- load its `.github/skills` and `.github/agents` as trusted configuration.

Therefore:

```text
copilot --add-dir repos/repository-a --add-dir repos/repository-b
```

is the preferred startup when both repositories' local customizations should participate in the session.

For a focused task, add only the relevant repository.

This distinction matters because project-scoped custom-agent discovery walks **upward** from the current working directory to the Git root. Descendant custom agents should not be treated as globally loaded merely because the parent session can read their files.

## Instructions vs agents vs skills

### `AGENTS.md`

The root `AGENTS.md` contains durable workspace behavior: authority, routing, local-context discipline, context efficiency, and safety.

Child `AGENTS.md` files provide more specific local behavior when work enters those repositories.

### `.github/copilot-instructions.md`

This file is intentionally tiny. It reinforces the workspace/local separation for Copilot surfaces that use repository custom instructions.

### Custom agents

Agents exist only where a real tool/context responsibility boundary is useful.

| Agent | Why it exists |
|---|---|
| `workspace-context-reader` | Separate context window for broad exploration; read/search only |
| `workspace-researcher` | Read-only current-state and cross-repository research |
| `workspace-bug-investigator` | Can execute confirmed diagnostics but cannot edit |
| `workspace-planner` | Read-only planning boundary |
| `workspace-implementer` | Generic write-capable execution role |
| `workspace-reviewer` | Independent review; no edits |

All root names are prefixed `workspace-` to reduce collisions with child repository agents.

### Agent Skills

Skills hold reusable procedures and are loaded on demand. The root skills are also namespaced to avoid collision with local project skills.

This is intentionally more context-efficient than putting every procedure into `AGENTS.md`.

## Context-efficiency architecture

Current Copilot CLI custom agents run as subagents with separate context windows. The root uses this capability to keep the main session focused.

```text
main coordinator
      │
      ├── workspace-context-reader → broad search / large-file analysis
      │                                  │
      │                                  └── concise path/line evidence
      │
      ├── workspace-researcher → current-state synthesis
      ├── workspace-planner → implementation plan
      └── workspace-reviewer → independent review
```

The intended pattern is:

1. search before reading;
2. read targeted files/ranges;
3. delegate broad exploration;
4. summarize evidence before continuing;
5. keep raw logs and large source dumps out of the parent context;
6. load procedural skills only when relevant.

This template does **not** claim a fixed token saving percentage. Any optimization should be measured using the tooling available in the actual Copilot CLI version.

## Routing

Routing has two modes.

### Explicit target

If the user says "work in repository A," the workspace starts there and expands only with evidence.

### Unknown target

If the repository is not known:

```text
request
  ↓
WORKSPACE.md
  ↓
targeted workspace search
  ↓
local high-level guidance
  ↓
smallest evidence-backed repository set
```

If ownership remains ambiguous, implementation stops for clarification.

## Cross-repository work

A cross-repository change is not treated as one giant codebase. Research and validation remain repository-aware.

A plan should identify:

- repository responsibility;
- boundary/contract;
- producer/consumer order when applicable;
- local tests and validation per repository;
- cross-boundary validation when available;
- safe sequencing and pause points.

## Local customization precedence and collisions

The root intentionally uses `workspace-` names because current Copilot CLI skill and agent discovery uses name-based deduplication/priority. Common generic names such as `implementation` or `review` are likely to exist in child repositories.

Namespacing makes the intent explicit:

- `/workspace-planning` = cross-repository generic procedure;
- a child `/planning` or `/service-planning` skill = local procedure.

When both are useful, use both rather than forcing one to replace the other.

The same problem can occur between two child repositories loaded with `/add-dir`. This template does not invent a precedence rule for that case. If identifiers collide, load only the repository needed for the task or make the child identifiers unique, then verify the active source with Copilot CLI discovery commands.

## Why there are no hooks or runtime scripts

The previous design explored mechanical scope guards and hook-based enforcement. This version deliberately removes them because the target scenario already has mature repository-local guidance and the root should remain a small complement.

The following are behavioral rather than mechanically enforced:

- stay within the named repository/scope;
- prefer targeted reads;
- use local commands only;
- keep review independent.

Tool restrictions on custom agents still provide a native boundary (for example, read-only Researcher vs write-capable Implementer).

Hooks remain a future option if a measured failure justifies them, such as repeated destructive tool use or demonstrably excessive context ingestion.

## Model configuration

No model IDs are committed. Current Copilot CLI supports per-agent/subagent model configuration and reasoning effort, but availability varies by account and policy.

A team may configure a faster/lower-cost model for `workspace-context-reader` through the CLI's user/session subagent settings. The workspace architecture should not depend on a particular vendor model being available.

## Deliberately omitted

- MCP servers without a confirmed integration requirement;
- Agentic Workflows for interactive orchestration;
- prompt files as a runtime dependency;
- path-specific root instructions for application code;
- mandatory research/plan/review artifact schemas;
- scope manifests and workflow locks;
- model routers;
- custom read-size hooks/scripts;
- application CI/build/test assumptions.
