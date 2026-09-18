# Validation Report

Validation date: **2026-09-13**

This report records validation of the generated workspace template itself. It does not validate application repositories cloned beneath it.

## Structure

Expected core components:

- root `AGENTS.md`;
- root `.github/copilot-instructions.md`;
- root `WORKSPACE.md`;
- six custom workspace agents;
- nine workspace Agent Skills;
- adoption, architecture, workflow, capability, prompt, plan, review, and validation documentation;
- ignored `repos/` container for independent child repositories.

No runtime scripts, hooks, MCP configuration, GitHub Actions workflow, or workflow-state machinery is required by the package.

## Copilot configuration validation

Validated:

- custom agent YAML frontmatter parses;
- agent descriptions are present;
- agent tool aliases are limited to `read`, `search`, `edit`, and `execute`;
- skill YAML frontmatter parses;
- every skill has required `name` and `description`;
- skill identifiers match directory names and valid CLI identifier shape;
- root customizations use the `workspace-` namespace where collision is plausible.

## Documentation validation

Validated:

- all internal Markdown links resolve;
- all documented workspace skill names exist;
- all documented workspace agent names exist;
- `/add-dir` examples use relative neutral repository paths;
- `WORKSPACE.md` remains a routing template and contains no fabricated repository facts.

## Security and privacy validation

Validated:

- no source-company, product, project, system, or person identifiers;
- no credentials, keys, tokens, secrets, or email addresses;
- no internal/private URLs or domains;
- no machine-specific absolute paths;
- no provider-specific model IDs;
- no destructive automation or broad GitHub token permissions;
- no third-party runtime dependency.

The only external URLs are official GitHub documentation links used for capability traceability.

## Context-efficiency validation

Validated:

- always-on instructions remain small;
- procedural detail lives in on-demand skills;
- broad exploration has a separate read-only agent;
- root agents/skills do not contain child-repository implementation knowledge;
- no claimed fixed token-reduction percentage;
- no large-read hook/script is required.

## Packaging validation

The final ZIP is validated after source review by:

1. enumerating source files;
2. creating a ZIP with one top-level directory;
3. extracting the ZIP into a clean directory;
4. comparing relative file lists;
5. comparing SHA-256 hashes of every file;
6. checking for unexpected cache/generated files;
7. confirming no empty functional file exists.

The delivery response reports the result of this final package-integrity check and the ZIP SHA-256.
