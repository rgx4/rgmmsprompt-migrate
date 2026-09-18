# GitHub Copilot Capabilities Used by This Architecture

Research date: **2026-09-13**

Official GitHub documentation is the source of truth for capability claims in this template. Re-check these links before changing the architecture because Copilot CLI evolves quickly.

## Supported capabilities relied upon

### Multi-repository CLI from a parent directory

GitHub's Copilot CLI best-practices documentation explicitly describes running Copilot from a parent directory containing multiple repositories so the CLI can access and work across child repositories.

Source:

- https://docs.github.com/en/copilot/how-tos/copilot-cli/cli-best-practices

### `/add-dir` / `--add-dir`

The current CLI command reference states that adding a directory:

- allows file access to that directory; and
- loads `.github/skills` and `.github/agents` from the added root as trusted configuration.

This is the recommended mechanism for making child repository custom agents/skills explicitly available in a root session.

Source:

- https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-command-reference

### Custom instruction discovery

Copilot CLI supports:

- `AGENTS.md`;
- `.github/copilot-instructions.md`;
- `.github/instructions/**/*.instructions.md`;
- additional instruction directories.

Current documentation says repository and agent instruction files can be discovered from repository root/current working directory and in nested paths of files Copilot is working on. Multiple applicable instruction files are combined; GitHub does not define a universal precedence order, so conflicting instructions should be avoided.

Source:

- https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-custom-instructions

### Agent Skills

Agent Skills are officially supported. Skills use `SKILL.md` with required `name` and `description` fields. Copilot injects a skill's contents when the skill is invoked or selected as relevant.

Current CLI documentation also supports inherited parent skills and skills contributed by added roots.

Sources:

- https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-skills
- https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-command-reference

### Custom agents and isolated subagents

Custom agents use Markdown agent profiles with YAML frontmatter and can restrict tools. GitHub currently documents that custom-agent work runs in temporary subagents with their own context windows, allowing focused work to be offloaded without filling the main agent's context window.

This is the basis for `workspace-context-reader`.

Sources:

- https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/create-custom-agents-for-cli
- https://docs.github.com/en/copilot/concepts/agents/copilot-cli/about-custom-agents
- https://docs.github.com/en/copilot/reference/custom-agents-configuration

### Custom-agent discovery

Current CLI documentation says project custom agents are discovered by walking upward from the current working directory to the Git root. Added roots can also contribute `.github/agents`.

This is why this architecture does not assume that every descendant child repository's agents are globally loaded merely because the root session can read that repository's files.

Source:

- https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-command-reference

### Tool permissions and restrictions

Copilot CLI distinguishes read-only operations from potentially destructive operations and supports allow/deny permission controls. Custom agents can also restrict the tools exposed to them.

Sources:

- https://docs.github.com/en/copilot/how-tos/copilot-cli/use-copilot-cli/allowing-tools
- https://docs.github.com/en/copilot/reference/custom-agents-configuration

## Useful current capabilities not required by the template

### Built-in exploration/review agents

Copilot CLI includes built-in agents such as `explore`, `code-review`, `security-review`, and command/task agents. These may complement the custom workspace agents, but the template does not depend on a particular built-in agent remaining unchanged.

Source:

- https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-command-reference

### Per-agent/subagent models

Current CLI configuration supports per-agent/subagent model selection and reasoning-effort configuration. This template deliberately does not commit model IDs. Teams may tune `workspace-context-reader` locally if their account/policy supports the desired model.

Source:

- https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-command-reference

### Hooks

Hooks are an official mechanism on supported Copilot surfaces and `preToolUse` can deny tool calls. They could enforce rules such as read-size limits, but this template does not use them because the requested root layer is intentionally script-free and the value should be demonstrated before adding that operational complexity.

Sources:

- https://docs.github.com/en/copilot/concepts/agents/hooks
- https://docs.github.com/en/copilot/reference/hooks-reference

### MCP

Custom agents can use MCP tools where configured. This expands the trust boundary into external systems. No MCP server is configured because the generic root has no confirmed external integration requirement.

Source:

- https://docs.github.com/en/copilot/reference/custom-agents-configuration

### Prompt files and Agentic Workflows

These can be useful in some Copilot surfaces, but neither is required for the root coordination architecture. Reusable prompts live in `docs/PROMPTS.md` so the core workflow is not dependent on a surface-specific prompt-file feature.

## Architectural conclusions from current support

1. Working from the parent/root directory is a supported multi-repository pattern.
2. Child code can be accessible without child custom agents/skills being globally active; `/add-dir` makes that trust/configuration boundary explicit.
3. Root and child customizations should use distinct names to avoid name-based collisions.
4. Skills are a better home than always-on instructions for procedural detail.
5. Separate-context custom agents are a native way to reduce main-context pollution.
6. Tool restrictions are useful native boundaries, but natural-language scope is not deterministic enforcement.
7. Hooks/MCP/automation should be added only for concrete needs, not for architectural symmetry.
