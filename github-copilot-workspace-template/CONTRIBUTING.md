# Contributing

This repository is a generic workspace coordination template. Contributions should improve cross-repository Copilot behavior without introducing assumptions about any specific company, product, stack, or child repository.

## Principles

- Keep root instructions small.
- Put reusable procedure in Agent Skills.
- Create a custom agent only when a responsibility, tool, or context boundary justifies it.
- Do not add framework-specific guidance to the root.
- Do not introduce model IDs, credentials, private URLs, internal names, or environment-specific paths.
- Prefer official GitHub documentation when changing claims about Copilot capabilities.
- Treat preview features as optional unless the template explicitly changes its compatibility target.

## Changing agents or skills

Before changing an agent or skill:

1. identify the failure or workflow need it addresses;
2. check whether a child repository should own the rule instead;
3. avoid duplicate canonical guidance;
4. update `README.md`, `docs/ARCHITECTURE.md`, and `docs/COPILOT-CAPABILITIES.md` when behavior/support changes materially;
5. review name collisions with likely child-repository customizations.

## Validation

Use the checklist in [docs/VALIDATION.md](docs/VALIDATION.md). Do not add a runtime validation script solely for this template unless there is a demonstrated maintenance need.
