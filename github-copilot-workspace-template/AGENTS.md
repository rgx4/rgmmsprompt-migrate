# Workspace Agent Guidance

This repository is a **workspace coordination layer**. It does not own the implementation details of child repositories.

## Authority

1. The user's current request defines the immediate task.
2. For repository-specific work, the target repository's own `AGENTS.md`, Copilot instructions, skills, documentation, tests, CI configuration, and source code are authoritative for that repository.
3. This root guidance defines only shared workflow and cross-repository coordination behavior.
4. `WORKSPACE.md` is a routing map, not a replacement for child-repository documentation.

When root and child guidance appear to conflict, do not silently choose. Follow the more local rule for local implementation when it is clearly applicable, and surface material conflicts.

## Routing

- If the user names a repository, start there.
- If the repository is not named, use `WORKSPACE.md` and evidence-based search to identify the smallest plausible repository set.
- Do not infer ownership from a repository name alone.
- Expand to another repository only when code, documentation, contracts, or runtime relationships support doing so.
- For cross-repository changes, research each repository's side of the boundary before planning edits.

## Local context

Before making a material claim or edit inside a child repository:

- read the applicable local `AGENTS.md` and Copilot instructions;
- discover relevant local skills and agents when they are available to the session;
- inspect actual code/configuration before asserting paths, commands, architecture, or behavior;
- never invent build, test, lint, migration, deployment, or release commands.

## Context efficiency

- Search before broad reading.
- Prefer targeted files and ranges over whole-repository dumps.
- Delegate broad exploration or large-file analysis to `workspace-context-reader` when useful.
- Ask subagents to return concise findings with paths/line ranges rather than raw source or full logs.
- Keep the main coordinating context focused on decisions, evidence, scope, and unresolved questions.

## Responsibility boundaries

- Research does not modify production code.
- Bug investigation may run confirmed diagnostics but does not fix the bug.
- Planning does not implement.
- `workspace-implementer` is the only root custom agent intended to edit application files.
- Review is independent from implementation and does not fix findings itself.
- Repository-local agents may have narrower or stronger rules; respect them.

## Safety

- Do not expose or persist secrets, credentials, private keys, tokens, customer data, or unnecessary proprietary detail.
- Do not run destructive, deployment, publication, migration, history-rewrite, or data-mutation commands unless the user explicitly requests them and local repository guidance permits them.
- Treat natural-language scope as a workflow constraint, not a security boundary.
- Validate changes using commands confirmed by the target repository before declaring work complete.
