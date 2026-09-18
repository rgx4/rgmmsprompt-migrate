This repository coordinates work across child repositories. Keep root-level behavior generic and defer repository-specific implementation rules to each child repository's local guidance and evidence.

When a repository is named, work there first. When it is not named, route the task using `WORKSPACE.md` plus repository evidence. Never invent repository ownership, paths, commands, architecture, or validation steps.

Prefer search and focused reads. Use isolated subagents for broad exploration when useful so the main context receives concise evidence rather than large source dumps.

Do not duplicate child-repository domain or technical documentation into the root. Update `WORKSPACE.md` only with stable workspace-level routing facts.
