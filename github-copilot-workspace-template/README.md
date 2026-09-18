# GitHub Copilot Multi-Repository Workspace Template

A small, reusable GitHub repository for coordinating GitHub Copilot CLI across multiple well-documented child repositories without duplicating their local agents, skills, instructions, or architecture knowledge.

This template is designed for a workspace like:

```text
workspace-root/
├── .github/                 # shared Copilot agents and skills
├── AGENTS.md                # generic workspace behavior
├── WORKSPACE.md             # routing map generated from evidence
├── docs/                    # workflow and adoption documentation
└── repos/
    ├── repository-a/        # its own .git, AGENTS.md, skills, agents, docs
    └── repository-b/        # its own .git, AGENTS.md, skills, agents, docs
```

The root answers **how to work across repositories**. Each child repository answers **how that repository works**.

## Why this architecture

A multi-repository workspace has two different kinds of knowledge:

- shared process: routing, research, planning, context management, cross-repository coordination;
- local engineering knowledge: architecture, domain rules, commands, tests, migrations, framework conventions, CI, security constraints.

Mixing both into one large root instruction file creates stale duplication and wastes context. This template keeps the root intentionally small and lets local repository guidance remain authoritative.

## What is included

- six workspace-namespaced custom agents with clear tool/responsibility boundaries;
- nine workspace-namespaced Agent Skills for routing and reusable engineering procedure;
- a `WORKSPACE.md` routing index populated by discovery rather than assumptions;
- current GitHub Copilot capability documentation;
- reusable root-oriented prompts;
- no runtime scripts, hooks, state machine, MCP configuration, or model IDs.

## Requirements

The primary runtime is **GitHub Copilot CLI**, because current GitHub documentation explicitly supports working from a parent directory containing multiple child repositories.

The architecture also uses currently supported Copilot concepts such as custom agents, Agent Skills, `AGENTS.md`, and repository custom instructions. Surface-specific support varies; see [docs/COPILOT-CAPABILITIES.md](docs/COPILOT-CAPABILITIES.md).

## Create the workspace

### 1. Create a repository from this template

Publish this directory as a GitHub template repository, then create or clone a new workspace repository from it.

### 2. Clone child repositories under `repos/`

For example:

```text
workspace-root/
└── repos/
    ├── repository-a/
    └── repository-b/
```

`repos/*` is ignored by the root Git repository so child repositories remain independent Git repositories.

You can use another layout, but update `WORKSPACE.md` and examples accordingly.

### 3. Start Copilot from the workspace root

```text
cd workspace-root
copilot
```

GitHub documents running Copilot CLI from a parent directory as a supported multi-repository workflow.

### 4. Bootstrap the workspace map

Run:

```text
/workspace-discovery
```

Or use this prompt:

```text
Use the /workspace-discovery skill. Inspect the child Git repositories in this workspace, read only their high-level local guidance and documentation needed to understand ownership, and update WORKSPACE.md with confirmed repository purpose, local guidance entry points, and documented cross-repository relationships. Do not copy implementation details or invent unknown facts.
```

Review the resulting `WORKSPACE.md` before relying on it for routing.

### 5. Load child-repository custom agents and skills when needed

Starting from the parent gives Copilot access to child repository files. That does **not** mean every descendant repository's custom agents and skills should be assumed to be globally loaded.

For a session that should use local agents/skills from specific repositories, explicitly add those repository roots:

```text
/add-dir repos/repository-a
/add-dir repos/repository-b
```

Equivalent startup form:

```text
copilot --add-dir repos/repository-a --add-dir repos/repository-b
```

`/add-dir` is a trust decision: GitHub documents that it loads `.github/agents` and `.github/skills` from the added root as trusted configuration.

With many repositories, add only the repositories relevant to the current task instead of loading everything.

If two loaded child repositories define custom agents or skills with the same identifier, do not assume which one will be selected. Prefer loading only the repository needed for the task, or rename local customizations so their identifiers are unambiguous. Use `/skills info`, `/skills list`, and `/agent` to verify what the session actually loaded.

## Daily use

### When you know the target repository

```text
In repos/repository-a, investigate <issue>. Do not modify code yet. Use the repository's local guidance and skills where applicable.
```

The root does not need to rediscover ownership.

### When you do not know the target repository

```text
Use /workspace-routing to determine which repository or smallest repository set owns <issue>. Show the evidence for the routing decision before editing anything.
```

### Cross-repository work

```text
This change may affect repository-a and repository-b. Research each side of the boundary first, identify the contract or dependency between them, then create an ordered implementation plan. Do not implement until the cross-repository scope is clear.
```

### Context-heavy investigation

```text
Delegate broad repository exploration to workspace-context-reader. Return only relevant findings, paths/line ranges, and unresolved questions to the main context.
```

This uses Copilot custom agents as isolated subagents so large exploration results do not need to remain in the parent context.

## Root agents

| Agent | Tools | Purpose |
|---|---|---|
| `workspace-context-reader` | read, search | Isolated broad/large-file exploration with concise evidence return |
| `workspace-researcher` | read, search | Current-state and cross-repository research |
| `workspace-bug-investigator` | read, search, execute | Diagnostic investigation without edits |
| `workspace-planner` | read, search | Planning without implementation |
| `workspace-implementer` | read, search, edit, execute | Scoped implementation; only root role intended to edit application files |
| `workspace-reviewer` | read, search, execute | Independent review without fixes |

The names are deliberately prefixed with `workspace-` to reduce collisions with agents already defined by child repositories.

## Root skills

- `/workspace-discovery`
- `/workspace-routing`
- `/workspace-context-research`
- `/workspace-research`
- `/workspace-bug-investigation`
- `/workspace-planning`
- `/workspace-implementation`
- `/workspace-validation`
- `/workspace-review`

The root skills describe process. Child repository skills should remain the source of truth for framework-, service-, domain-, test-, migration-, or deployment-specific procedure.

## Authority model

The practical hierarchy is:

```text
current user request
        ↓
workspace routing/process guidance
        ↓
child repository local guidance
        ↓
actual repository evidence
```

For implementation details, the child repository's local guidance is more specific and therefore more relevant. Root guidance must not overwrite it or copy it into `WORKSPACE.md`.

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

## Context efficiency

This template incorporates the useful part of context-budget architectures without requiring custom hooks or scripts:

1. search before broad reads;
2. prefer targeted ranges/files;
3. delegate large exploration to a separate-context agent;
4. return concise evidence to the main coordinator;
5. load skills on demand;
6. avoid injecting child-repository implementation knowledge into root instructions.

A future team may add `preToolUse` hooks to enforce read-size limits, but this template intentionally does not. That optimization should be added only after measuring a real context-cost problem.

## What stays local to child repositories

Do **not** move these into the root unless they genuinely apply across repositories:

- build/test/lint/type-check commands;
- framework rules;
- database/migration procedure;
- local architecture and domain rules;
- generated-code rules;
- CI/release/deployment behavior;
- local security/compliance requirements;
- repository-specific agents and skills.

## Model selection

The template pins no model IDs. Copilot CLI currently supports per-agent/subagent model configuration, but availability can vary by account and policy. If desired, configure a lower-cost/faster model for `workspace-context-reader` at user/session level rather than committing provider-specific model names into the workspace.

## No custom runtime scripts

The runtime architecture intentionally contains no:

- scope-manifest scripts;
- hook scripts;
- workflow-state files;
- custom model router;
- MCP server configuration;
- generated agent configuration.

The template relies on native Copilot composition, tool restrictions, local repository authority, Git/CI controls, and human review.

## Documentation

- [Adaptation plan](docs/ADAPTATION-PLAN.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Workflow](docs/WORKFLOW.md)
- [Adoption](docs/ADOPTION.md)
- [Copilot capabilities](docs/COPILOT-CAPABILITIES.md)
- [Prompt library](docs/PROMPTS.md)
- [Review report](docs/REVIEW-REPORT.md)
- [Validation report](docs/VALIDATION.md)

## Limitations

- Natural-language scope is not deterministic enforcement.
- Child repository agents/skills should be explicitly loaded with `/add-dir` when you want them available in a root session.
- A root session can route incorrectly if `WORKSPACE.md` is stale or the repository evidence is ambiguous; implementation should stop rather than guess.
- The context-efficiency rules are behavioral in this version; no hook blocks large reads mechanically.
- Copilot product capabilities evolve. Re-check the official links in `docs/COPILOT-CAPABILITIES.md` before changing the architecture.
