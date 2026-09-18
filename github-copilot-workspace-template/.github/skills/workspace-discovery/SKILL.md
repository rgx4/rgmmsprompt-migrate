---
name: workspace-discovery
description: Discover child Git repositories, their documented responsibilities, local Copilot guidance, and cross-repository relationships, then update the root WORKSPACE.md with confirmed routing facts only.
argument-hint: "[optional workspace scope]"
user-invocable: true
---

# Workspace discovery

Build or refresh the root `WORKSPACE.md` as a routing index.

## Procedure

1. Identify child Git repositories within the requested workspace scope.
2. For each repository, read only enough high-level material to determine:
   - purpose or primary responsibility;
   - local guidance entry points such as `AGENTS.md`, `.github/copilot-instructions.md`, `.github/instructions/`, `.github/agents/`, and `.github/skills/`;
   - documented relationships to other repositories.
3. Use repository README/docs, manifests, contracts, CI references, or source references only when needed to confirm ownership or relationships.
4. Record each important item as either confirmed or unknown.
5. Surface contradictions instead of silently reconciling them.
6. When the user asks to bootstrap or refresh the workspace, update only `WORKSPACE.md` unless another file is explicitly requested.

## Do not copy into the root

Do not duplicate:

- build/test/lint/typecheck commands;
- framework-specific rules;
- detailed architecture;
- database/migration procedures;
- local domain rules;
- child repository agents/skills content.

Those remain owned by the child repository.

## Session loading guidance

If a child repository contains custom agents or skills that should be available to the current root Copilot CLI session, include the exact relative `/add-dir <repository-path>` command in your report. Do not claim the local agents/skills are loaded until the repository has actually been added or the CLI reports them as available.
