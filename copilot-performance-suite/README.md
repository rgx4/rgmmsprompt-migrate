# Copilot Performance Investigation Suite

Ready-to-install, read-only performance investigation workflow for GitHub Copilot CLI. It coordinates browser/React, ASP.NET/.NET runtime, EF Core, and SQL evidence without changing production code.

## Included agents

- `performance-orchestrator` — scopes journeys, delegates specialised work, correlates evidence, ranks findings, and stops before implementation.
- `frontend-performance-investigator` — Chrome DevTools, network, main thread, React, rendering, payload, and hub/refetch analysis.
- `dotnet-performance-investigator` — ASP.NET request paths, trace collection/analysis, waits, CPU, GC, allocations, serialization, and measured hot-path review.
- `sql-performance-investigator` — EF-generated SQL, query counts, plans, reads, cardinality, indexes, sargability, N+1, and over-fetching.

## Included skills

- `chrome-devtools` (GitHub Awesome Copilot)
- `sql-optimization` (GitHub Awesome Copilot)
- `analyzing-dotnet-performance` (Microsoft .NET)
- `dotnet-trace-collect` (Microsoft .NET)
- `dump-collect` (Microsoft .NET dependency used for hangs/memory cases)
- `vercel-react-best-practices` (Vercel)
- `dotnet-runtime-analysis` (suite skill with a deterministic Speedscope summariser)

The upstream skills are included in full, including their reference files and rule sets. Exact source revisions are recorded in `source-lock.json`.

## Requirements

- GitHub Copilot CLI with custom-agent and skill support
- Node.js LTS, npm, and current stable Chrome for Chrome DevTools MCP
- Python 3 for validation and the Speedscope summariser
- The relevant .NET diagnostic tools for backend tracing; the included collection skill provides environment-specific installation commands

Chrome DevTools MCP is configured inside the relevant agents and pinned to `chrome-devtools-mcp@1.9.0`. `npx` downloads it on first use. The configuration disables MCP usage statistics and CrUX URL lookups and redacts sensitive network headers.

## Install for your user

The shortest installation path is the Copilot CLI plugin command. Unzip the package, enter its parent directory, and run:

```bash
copilot plugin install ./copilot-performance-suite
```

Verify it with:

```bash
copilot plugin list
```

Inside an interactive session, use `/agent` and `/skills list` to confirm that the agents and skills loaded.

To install the files directly into your personal Copilot directories instead of the plugin cache:

macOS/Linux:

```bash
chmod +x install.sh
./install.sh --user
```

PowerShell:

```powershell
.\install.ps1 -Scope User
```

The scripts install agents and skills under `~/.copilot/`. Existing matching agents or skills are not overwritten unless `--force` or `-Force` is supplied.

## Install in one repository

macOS/Linux:

```bash
./install.sh --project /path/to/repository
```

PowerShell:

```powershell
.\install.ps1 -Scope Project -ProjectPath C:\path\to\repository
```

This installs the same payload under the repository's `.github/agents/` and `.github/skills/` directories.

Restart Copilot CLI after installation.

## Run the workflow

Interactive:

```text
/agent
```

Select `performance-orchestrator`, then provide a bounded objective, for example:

```text
Investigate the runtime performance of the Setups and Outings journeys. Use the existing architecture review as the initial hypothesis set. Focus on initial page load, setup value-change latency, and the Hub-driven Outings refresh path. Measure before recommending and do not implement changes.
```

Non-interactive:

```bash
copilot --agent performance-orchestrator --prompt "Investigate the Outings initial-load journey. Measure before recommending and do not implement changes."
```

For a smaller investigation, select a worker directly or narrow the orchestrator prompt to one endpoint, interaction, or architecture candidate.

## Behaviour and boundaries

- All agents intentionally omit the `edit` tool.
- Diagnostic artifacts may be created, but application code, tests, queries, indexes, schemas, and configuration are not modified.
- Production tracing, plans, load, or database execution requires explicit authorisation.
- Findings are classified as `CONFIRMED`, `SUPPORTED`, `HYPOTHESIS`, `NOT_OBSERVED`, or `BLOCKED`.
- The orchestrator stops after the evidence report. Implementation and before/after verification are separate, user-approved work.

If browser authentication is required, complete sign-in yourself; the agents are instructed not to request or handle credentials.

## Validate the package

```bash
python3 tools/verify_package.py .
```

The validator checks the complete agent/skill set, frontmatter, read-only tool restrictions, the MCP version pin, and the bundled Python helper.
