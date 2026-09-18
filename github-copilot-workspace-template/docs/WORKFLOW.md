# Workflow

## Default operating mode

Start Copilot CLI from the workspace root.

```text
cd workspace-root
copilot
```

If a session needs child repository custom agents/skills, add those repository roots explicitly with `/add-dir` or `--add-dir`.

## 1. Explicit repository task

When the user names the repository:

```text
User: In repos/repository-a, investigate <issue>.
```

Flow:

```text
named repository
  ↓
load local guidance
  ↓
research / investigate
  ↓
plan if needed
  ↓
implement
  ↓
local validation
  ↓
independent review
```

Do not perform workspace-wide routing unless evidence shows another repository is involved.

## 2. Unknown repository task

When the user describes a behavior without naming ownership:

```text
request
  ↓
/workspace-routing
  ↓
WORKSPACE.md + targeted search
  ↓
smallest plausible repository set
  ↓
show routing evidence
  ↓
continue or ask clarification
```

Implementation must not start while ownership is materially ambiguous.

## 3. Unfamiliar-area research

Use `workspace-researcher` and `/workspace-research`.

When the exploration is broad or files are large, delegate search/reading to `workspace-context-reader` with `/workspace-context-research` so the main context receives concise evidence.

Research output should separate:

- repository-local facts;
- cross-repository relationships;
- inference;
- unknowns.

## 4. Bug flow

```text
symptom
  ↓
route ownership
  ↓
workspace-bug-investigator
  ↓
hypotheses + repository-confirmed diagnostics
  ↓
root cause / remaining uncertainty
  ↓
workspace-implementer
  ↓
validation
  ↓
workspace-reviewer
```

Investigation does not fix the bug.

## 5. Feature flow

For a small, well-understood local change:

```text
local guidance → implement → validate → review
```

For a non-trivial or cross-repository change:

```text
research → plan → implement in dependency order → validate per repository → cross-boundary review
```

Do not force research/planning ceremony onto trivial work when requirements and scope are already clear.

## 6. Cross-repository change

A cross-repository plan should explicitly state:

1. repositories in scope;
2. boundary/contract between them;
3. execution order;
4. local tests and validation per repository;
5. compatibility validation across the boundary;
6. rollout/coordination risk if relevant;
7. out-of-scope repositories.

Each repository remains responsible for its own local commands and conventions.

## 7. Validation

Use `/workspace-validation`.

Validation is evidence-driven and repository-specific. A root workflow must not invent commands such as `npm test`, `dotnet test`, or `make` unless the target repository actually defines them.

For multi-repository changes, report validation separately for each repository.

## 8. Review

Use `workspace-reviewer` and `/workspace-review`.

Review begins from the actual diff. It remains independent from implementation and includes cross-repository contract compatibility when applicable.

The reviewer reports findings; it does not edit the code to fix them.

## 9. Resume work

This root template does not impose a workflow state machine. Resume from:

- the current Git diff;
- existing issue/PR/task context;
- repository-local planning artifacts if that repository uses them;
- `WORKSPACE.md` for routing context.

Do not create a second persistent state system unless the adopting team has a concrete cross-session requirement.
