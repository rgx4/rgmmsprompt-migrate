---
name: workspace-validation
description: Discover and run only the validation checks confirmed by each affected child repository before declaring a change complete.
argument-hint: "[changed repository or scope]"
user-invocable: true
---

# Validate changes

For each affected repository independently:

1. Discover applicable validation from local developer docs, project/package scripts, CI configuration, and local instructions.
2. Do not invent commands from ecosystem conventions.
3. Run the narrowest useful checks first, then broader checks required by the repository.
4. Include compile/typecheck/build/lint/test checks only when applicable and supported by repository evidence.
5. Distinguish failures caused by the current change from pre-existing failures when possible.
6. Do not modify tests/configuration merely to bypass a gate.
7. For cross-repository changes, validate the boundary/contract as well as each repository locally when such a check exists.
8. Report exact commands, outcomes, and checks that could not be run.

A passing check in one repository does not imply another affected repository is validated.
