# Adaptation Plan — Multi-Repository Copilot Workspace Architecture

Date: 2026-09-13
Status: Completed
Source baseline: the previously generated `github-copilot-repository-template`

## 1. Objective

Adapt the current generic repository-oriented Copilot template into a workspace-oriented template for a parent/root directory that coordinates multiple well-documented child Git repositories.

The root layer must complement—not duplicate or replace—the `AGENTS.md`, instructions, custom agents, skills, documentation, and code already owned by each child repository.

The primary operating model is GitHub Copilot CLI started from the workspace root. Users should be able to:

- name a target repository explicitly;
- ask Copilot to determine repository ownership when the target is not known;
- coordinate work that spans more than one repository;
- keep the parent context small by delegating broad exploration to isolated subagents;
- use repository-local knowledge and skills once the relevant repository has been identified;
- avoid custom scripts, hook-based enforcement, workflow state machines, and environment-specific configuration in the root template.

## 2. Baseline assessment

### Keep

- Generic responsibility boundaries: research, bug investigation, planning, implementation, review.
- Read-only vs write-capable agent separation.
- Evidence-first behavior and the rule not to invent commands or architecture.
- Agent Skills for reusable task procedure.
- Current Copilot capability documentation and the practice of distinguishing official support from optional/preview features.
- A reusable prompt library.

### Change

- Change the unit of abstraction from **one application repository** to **one multi-repository workspace**.
- Replace `REPOSITORY-CONTEXT.md` with a concise `WORKSPACE.md` repository map.
- Replace repository bootstrap with workspace discovery and routing.
- Make repository-local `AGENTS.md`, `.github/instructions`, `.github/agents`, and `.github/skills` explicitly authoritative for repository-specific work.
- Add context-efficient delegation as a first-class architecture concern.
- Update documentation so the canonical usage starts Copilot from the parent/root directory.
- Document the important distinction between *file access* and *loading child-repository custom agents/skills*.

### Remove

- Root path-specific instructions for tests, docs, workflows, or languages. Those belong in child repositories.
- Root testing and documentation skills that duplicate repository-local procedures.
- Optional prompt-file dependency from the core architecture.
- GitHub Actions validation from the runtime workflow. The root architecture should remain script-free and should not require automation merely to coordinate local repositories.
- Any assumption that the root template owns application build/test/migration commands.

## 3. Current Copilot capabilities that drive the design

The implementation must reflect the official behavior verified on 2026-09-13:

1. Copilot CLI can run from a parent directory containing multiple child repositories and work across them.
2. `/add-dir` / `--add-dir` expands allowed directories and loads `.github/skills` and `.github/agents` from each added root as trusted configuration.
3. Project custom agents are discovered from the current working directory upward to the Git root; descendant child-repository agents are not assumed to be globally loaded merely because their files are reachable.
4. Skills are context-efficient: `SKILL.md` content is injected when invoked or selected as relevant. Added roots can contribute skills.
5. Custom agents run as subagents with separate context windows, which can keep broad exploration and diagnostics out of the main coordinating context.
6. Repository/agent instructions can be discovered in nested paths of files being worked on; path-specific instructions apply by `applyTo`.
7. Tool restrictions on custom agents are native and remain useful responsibility boundaries.

## 4. Target architecture

### Root responsibilities

The root owns only cross-repository process and workspace coordination:

- repository discovery;
- repository routing;
- context-efficient research;
- generic research/bug/planning/implementation/review workflow;
- cross-repository coordination;
- a concise workspace map;
- generic prompts and adoption guidance.

### Child repository responsibilities

Each child repository remains authoritative for:

- system/domain architecture;
- technology and framework conventions;
- build/test/lint/typecheck commands;
- migrations and databases;
- local agents and skills;
- local path-specific instructions;
- CI and release behavior;
- security/compliance requirements;
- implementation details.

### Agent set

Create six **workspace-namespaced** root agents with genuine responsibility/context boundaries. Namespacing avoids collisions with child repositories that already define agents with common names:

1. `workspace-context-reader` — read/search only; broad or large-file exploration; concise evidence return.
2. `workspace-researcher` — read/search only; current-state understanding and cross-repository mapping.
3. `workspace-bug-investigator` — read/search/execute; diagnostics without edits.
4. `workspace-planner` — read/search only; executable plan without implementation.
5. `workspace-implementer` — read/search/edit/execute; only generic write-capable role.
6. `workspace-reviewer` — read/search/execute; independent review without edits.

Do not pin provider-specific model IDs. Document optional user-level `/subagents` model tuning instead.

### Skill set

Create nine root skills, namespaced when a generic name would plausibly collide with repository-local skills:

1. `workspace-discovery`
2. `workspace-routing`
3. `workspace-context-research`
4. `workspace-research`
5. `workspace-bug-investigation`
6. `workspace-planning`
7. `workspace-implementation`
8. `workspace-validation`
9. `workspace-review`

All must stay technology-neutral and defer repository-specific technique to local guidance.

## 5. Session behavior

### Explicit repository

If the user names a repository, route there immediately, read local authority, and avoid expanding scope unless evidence shows another repository is involved.

### Repository unknown

Use `WORKSPACE.md`, targeted search, and local repository entry documentation to identify the smallest plausible repository set. Do not infer ownership from names alone.

### Repository-local agents and skills

Starting from the root provides file access to child repositories. To make a child repository's `.github/agents` and `.github/skills` available as trusted Copilot configuration in the root session, add the repository with `/add-dir <repo-path>` or start with repeated `--add-dir` arguments.

For two repositories that are regularly used together, the recommended session start is:

```text
copilot --add-dir repos/repository-a --add-dir repos/repository-b
```

Names in documentation remain neutral examples only.

### Context efficiency

Broad exploration should be delegated to `context-reader` or another isolated exploration subagent rather than returning raw files/logs into the parent context. Search before read, prefer targeted ranges, and return concise path/line evidence.

No hook or script will mechanically block large reads in this version. This remains a behavioral optimization, with optional future hook enforcement only if measured context usage justifies it.

## 6. File migration plan

### New/renamed concepts

- Add `WORKSPACE.md`.
- Add `.github/agents/workspace-context-reader.agent.md`.
- Namespace all root agents and generic skills with `workspace-` where collision is plausible.
- Add skills `workspace-discovery`, `workspace-routing`, and `workspace-context-research`.
- Rename repository-oriented docs and examples to workspace-oriented language.
- Add a dedicated multi-repository bootstrap prompt to `docs/PROMPTS.md` rather than relying on preview prompt files.
- Add `docs/REVIEW-REPORT.md` to record the required multi-pass review of this generated template.

### Remove from the previous package

- `.github/instructions/*`
- `.github/prompts/*`
- `.github/workflows/*`
- `.github/skills/repository-discovery`
- `.github/skills/testing`
- `.github/skills/documentation`
- `docs/REPOSITORY-CONTEXT.md`
- repository-template-specific PR/contribution scaffolding that does not help the root orchestration role unless independently justified.

## 7. Documentation updates

Rewrite:

- `README.md` — workspace-first quick start and two-repository examples.
- `AGENTS.md` — short canonical root behavior and local-authority rule.
- `.github/copilot-instructions.md` — very small repository-wide Copilot guidance.
- `docs/ARCHITECTURE.md` — root vs child authority, routing, subagent/context model, explicit `/add-dir` behavior.
- `docs/WORKFLOW.md` — explicit repo, unknown repo, cross-repo, bug, implementation, and review flows.
- `docs/ADOPTION.md` — installing as a workspace root and cloning child repositories under `repos/`.
- `docs/COPILOT-CAPABILITIES.md` — current official support used by this architecture.
- `docs/PROMPTS.md` — root-oriented reusable prompts.
- `docs/VALIDATION.md` — final validation evidence.

## 8. Review plan — minimum five passes

After implementation, run and document at least these five independent review passes:

1. **Architecture & authority review** — root/local ownership, duplication, routing, cross-repo semantics.
2. **Copilot compatibility review** — agent/skill frontmatter, supported discovery mechanisms, no invented product features.
3. **Context-efficiency review** — search-before-read, subagent isolation, concise handoffs, no accidental always-on bloat.
4. **Security & privacy review** — no identifiers, secrets, internal names/URLs, dangerous automation, or broad permissions.
5. **Consistency & packaging review** — links, referenced files, stale names, empty files, ZIP tree, hash comparison after extract.

A sixth **usability review** should be run if any issue is found in passes 1–5 or if the final README does not make the two-repository workflow obvious without external explanation.

## 9. Acceptance criteria

The adaptation is complete only when:

- The root can coordinate an arbitrary number of child repositories without knowing their implementation details.
- The user can explicitly name a repository or ask the root to route the task.
- Local `AGENTS.md`/instructions remain authoritative for local work.
- The documentation clearly explains when `/add-dir` is needed to load child custom agents/skills.
- Context-efficient delegation is built into the generic workflow without scripts/hooks.
- No environment-specific names, paths, companies, products, credentials, or model IDs exist.
- No packaged runtime script/hook/state machine is required.
- All generated agents and skills use currently supported frontmatter.
- At least five documented reviews pass.
- The final ZIP contains exactly the intended files, expands under a single root directory, and matches the reviewed uncompressed directory byte-for-byte.


## 10. Implementation outcome

Implemented as planned with one additional architecture refinement discovered during review: all root agents and generic workflow skills are namespaced with `workspace-` to reduce identifier collisions with child repositories. Documentation also warns that collisions can still occur between two child repositories loaded into the same session and recommends loading only the relevant repository or making local identifiers unique.
