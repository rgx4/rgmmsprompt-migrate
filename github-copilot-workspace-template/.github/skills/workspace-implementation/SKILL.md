---
name: workspace-implementation
description: Implement a well-understood change across one or more child repositories using local agents/skills/instructions, minimal scope, behavior-relevant tests, and repository-confirmed validation.
argument-hint: "<change or plan>"
user-invocable: true
---

# Implement a scoped change

Use `workspace-implementer` when available.

1. Confirm the repository set and intended outcome.
2. Load local repository guidance and more specific local skills before editing.
3. Inspect the exact code and nearby patterns.
4. Follow the planned dependency order for cross-repository changes.
5. Keep changes limited to the requested behavior; do not bundle unrelated cleanup.
6. Add or update behavior-relevant tests according to local conventions.
7. Never remove, skip, invert, or weaken assertions simply to obtain a pass.
8. If work unexpectedly requires another repository, migration, public-contract change, destructive operation, or materially broader scope, stop and surface it.
9. Use `/workspace-validation` before completion.
10. Report changed repositories/files, validation actually performed, limitations, and separate follow-up.

Repository-local implementation skills are more specific than this generic procedure and should be used when available.
