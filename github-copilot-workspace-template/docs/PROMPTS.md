# Prompt Library

These prompts assume Copilot CLI is running from the workspace root. Replace `<...>` values with the actual task. Repository names below are neutral examples.

## 1. Bootstrap the workspace

```text
Use /workspace-discovery.

Inspect the child Git repositories in this workspace. For each repository, determine only its documented high-level purpose, local Copilot/agent guidance entry points, and confirmed relationships to other repositories.

Update WORKSPACE.md with confirmed routing facts only. Do not copy implementation details, build/test commands, framework rules, migrations, or domain documentation into the root. Mark unresolved information as Unknown.

At the end, tell me which child repositories contain .github/agents or .github/skills and show the exact relative /add-dir commands I can run if I want those customizations loaded in this session.
```

## 2. Work in a known repository

```text
Work in <repository-path>.

First load that repository's local AGENTS.md, Copilot instructions, and relevant local skills. Then <task>.

Do not expand to another repository unless evidence shows it is involved. If you need to expand scope, explain why first.
```

## 3. Determine repository ownership

```text
Use /workspace-routing for <issue-or-requirement>.

Do not implement anything. Use WORKSPACE.md plus targeted search to identify the smallest repository set that owns the behavior. Show the evidence for the routing decision and any remaining ambiguity.
```

## 4. Research an unfamiliar area efficiently

```text
Use /workspace-research and /workspace-context-research to understand <topic>.

Delegate broad exploration or large-file analysis to workspace-context-reader. Keep the main response focused on confirmed behavior, important paths/line ranges, repository boundaries, and unresolved questions. Do not return large source dumps.
```

## 5. Investigate a bug

```text
Use workspace-bug-investigator with /workspace-bug-investigation for <symptom>.

Determine repository ownership first if needed. Trace the symptom to an evidence-backed root cause. You may run only diagnostic commands confirmed by local repository evidence. Do not edit files or apply the fix.
```

## 6. Plan a local feature

```text
Use workspace-planner and /workspace-planning to plan <feature> in <repository-path>.

Use existing local research and guidance. Produce ordered implementation phases, expected tests, repository-confirmed validation, risks, and out-of-scope work. Do not implement.
```

## 7. Plan a cross-repository feature

```text
Use /workspace-routing and workspace-planner for <requirement>.

Research each affected repository's side of the boundary before planning. Identify the contract/dependency, execution order, per-repository files/surfaces, local tests, validation, cross-boundary checks, risks, and pause points. Do not implement.
```

## 8. Implement an approved plan

```text
Use workspace-implementer with /workspace-implementation to execute this approved plan: <plan>.

Load repository-local guidance and skills before editing. Keep changes to the planned repository/file scope. Validate each affected repository using only commands confirmed by that repository. Stop if scope unexpectedly expands or a destructive/unplanned migration/public-contract change becomes necessary.
```

## 9. Validate before completion

```text
Use /workspace-validation for the current changes.

For each affected repository, discover the applicable validation commands from local documentation, project scripts, or CI. Run the narrowest useful checks first, then any broader required checks. Report exact commands, outcomes, and anything that could not be validated.
```

## 10. Review a local change

```text
Use workspace-reviewer with /workspace-review to review the current diff in <repository-path>.

Apply local review/testing/architecture guidance. Focus on material correctness, regression, security/privacy, error handling, architecture boundaries, tests, and missing validation. Do not edit files.
```

## 11. Review a cross-repository change

```text
Review the current coordinated change across <repository-a> and <repository-b>.

Review each repository locally and also verify compatibility at their shared boundary/contract. Separate findings by repository and cross-repository finding. Do not apply fixes.
```

## 12. Reduce context use during a long task

```text
Use /workspace-context-research for the next investigation.

Search before reading. Delegate broad exploration to workspace-context-reader. Ask subagents to return concise path/line evidence and unknowns, not whole files or full logs. Keep the parent context focused on decisions and the current task state.
```

## 13. Refresh a stale workspace map

```text
Use /workspace-discovery to refresh WORKSPACE.md.

Compare the current repository inventory and high-level documentation with the existing map. Update only facts that are supported by current evidence. Preserve unknowns where the repositories do not establish an answer. Do not rewrite child-repository documentation.
```
