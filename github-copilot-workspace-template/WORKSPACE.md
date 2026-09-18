# Workspace Map

> This file is intentionally generic at first. Run the `/workspace-discovery` skill after cloning child repositories, then replace `Unknown` only with facts supported by repository evidence.
>
> Keep implementation details in the child repository that owns them. This file is a routing index, not a second architecture handbook.

Last reviewed: Unknown

## Repository map

| Repository path | Purpose / responsibility | Local guidance entry points | Relationships | Status |
|---|---|---|---|---|
| Unknown | Unknown | Unknown | Unknown | Undiscovered |

## Cross-repository relationships

Unknown.

Record only relationships supported by documentation, contracts, code references, CI configuration, or another concrete source.

## Shared workspace conventions

Unknown.

Only record conventions that genuinely apply across multiple repositories. Do not copy local build/test/framework rules here.

## Recommended Copilot CLI session loading

The parent/root session can access child repositories when they are under this workspace. Child repository custom agents and skills are not assumed to be globally loaded merely because their files are reachable.

For repositories whose local agents/skills should participate in the current session, add them explicitly:

```text
/add-dir repos/repository-a
/add-dir repos/repository-b
```

Or start the session with repeated `--add-dir` arguments.

Use only paths that actually exist in this workspace.

## Unknowns

- Repository inventory has not been discovered yet.
- Cross-repository ownership and relationships have not been confirmed yet.
