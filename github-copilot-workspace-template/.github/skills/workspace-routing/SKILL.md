---
name: workspace-routing
description: Determine which child repository or smallest repository set owns a task before substantive work begins. Use when the user does not name the target repository or cross-repository scope is uncertain.
argument-hint: "<task or issue>"
user-invocable: true
---

# Workspace routing

Route the task before implementation.

## If the user names a repository

1. Start with that repository.
2. Read its local guidance before material work.
3. Expand scope only when concrete evidence shows another repository is involved.

## If the repository is not named

1. Read `WORKSPACE.md`.
2. Search for relevant domain terms, symbols, APIs, contracts, components, or entry points across plausible child repositories.
3. Inspect the smallest amount of local high-level guidance needed to confirm ownership.
4. Select the smallest repository set supported by evidence.
5. State the routing decision and evidence before edits.

## Cross-repository work

When more than one repository is involved:

- identify each repository's responsibility independently;
- identify the boundary/contract/dependency between them;
- distinguish producer, consumer, orchestration, and shared-contract roles when supported by evidence;
- route research to each side before planning changes.

Never infer ownership from a repository name alone. If evidence remains ambiguous, ask before implementation.
