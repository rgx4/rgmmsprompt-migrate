# Adoption Guide

## Recommended layout

Use the template as a small Git repository at the workspace root and keep independent application repositories under `repos/`.

```text
workspace-root/
├── .git/
├── .github/
├── AGENTS.md
├── WORKSPACE.md
├── docs/
└── repos/
    ├── repository-a/.git/
    └── repository-b/.git/
```

The root `.gitignore` ignores `repos/*`, so child repositories remain independent.

## Existing workspace

If you already have a parent directory containing repositories, you can either:

1. move/adapt the child repositories under this template's `repos/` directory; or
2. copy the root customization files into your existing parent workspace and adjust paths in `WORKSPACE.md`.

Do not copy root process files into every child repository. They are meant to remain shared.

## First-time bootstrap

1. Clone or create the root workspace repository.
2. Clone the child repositories.
3. Start Copilot CLI from the root.
4. Run `/workspace-discovery`.
5. Review `WORKSPACE.md` for accuracy.
6. Add the repositories whose custom agents/skills should participate in the current session.

Example:

```text
/add-dir repos/repository-a
/add-dir repos/repository-b
```

7. Use `/skills list` and `/agent` if you want to confirm which customizations are available.
8. Use `/instructions` to inspect instruction files discovered by the current CLI session.

## What discovery should write

`WORKSPACE.md` should contain only:

- repository path;
- high-level purpose/responsibility;
- local guidance entry points;
- confirmed cross-repository relationships;
- genuinely shared workspace conventions;
- unresolved unknowns.

It should not become a catalog of local framework or domain rules.

## What must remain local

Do not promote these into the workspace root merely for convenience:

- repository build/test commands;
- database/migration details;
- local architecture;
- service-specific domain rules;
- local code style;
- local release/deployment procedure;
- repository-specific agent prompts.

## Naming local customizations

The root uses `workspace-*` names to minimize collisions. Child repositories do not need to rename their existing agents/skills unless they collide with each other in the same loaded session and the collision causes ambiguity.

When adding new root customizations, keep the `workspace-` namespace.

## Session patterns

### Focused repository session

Start at root, add one repository:

```text
copilot --add-dir repos/repository-a
```

### Two-repository coordination

```text
copilot --add-dir repos/repository-a --add-dir repos/repository-b
```

### Many-repository workspace

Start at root without loading every repository customization. Use `/workspace-routing`, then `/add-dir` only the repositories needed for the task.

This keeps the available customization set easier to reason about.

If two child repositories expose identically named agents or skills, avoid loading both until the collision is resolved or verified. Prefer repository-specific names for local customizations that are commonly loaded together.

## Customization after adoption

### Mandatory

- populate `WORKSPACE.md` from evidence;
- confirm child repositories' local guidance is current;
- decide which repositories normally need `/add-dir` together.

### Optional

- adjust root prompts for your team's vocabulary without adding proprietary information to a public template;
- add a workspace-specific skill only for a genuinely cross-repository repeated procedure;
- configure user-level subagent models;
- add hooks later for a demonstrated enforcement need.
