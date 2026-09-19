---
name: dotnet-runtime-analysis
description: Analyse collected .NET CPU traces by converting .nettrace artifacts to Speedscope and producing deterministic self/inclusive frame summaries. Use after trace collection, not as a substitute for end-to-end timing or wait analysis.
license: MIT
---

# .NET Runtime Analysis

Use this skill after a bounded trace has been collected for a known process and journey. It complements `dotnet-trace-collect`, which selects and captures diagnostics but does not analyse them.

## Supported path

- `.nettrace`: first use `dotnet-trace report <trace.nettrace> topN` and repeat with `--inclusive`; convert when a portable frame summary is useful with `dotnet-trace convert <trace.nettrace> --format Speedscope --output <output-file>`.
- `.speedscope.json`: summarise directly with the bundled script.
- `.nettrace` produced by the preview `collect-linux` verb: current `convert` and `report` support may be incomplete; use the latest PerfView when conversion fails and report the limitation.
- PerfView `.etl` or `.etl.zip`: analyse in PerfView; do not pretend the bundled script can parse ETW.
- Dumps: use the analysis tool recommended by `dump-collect`; this skill does not parse dumps.

Resolve the script relative to this `SKILL.md` installation:

```bash
python3 scripts/summarize_speedscope.py trace.speedscope.json --top 30
```

Use `--format json` when a machine-readable handoff is useful. Use `--profile <index>` to select one profile from a multi-profile file and `--match <regex>` to restrict frames.

## Workflow

1. Preserve the original artifact and record the collection command, PID, runtime, UTC interval, and workload.
2. Convert a copy to Speedscope when required.
3. Run the summariser and retain both self and inclusive tables.
4. Map significant frames to repository symbols and the measured request path.
5. Separate what the trace can establish from what it cannot:
   - sampled CPU weight identifies on-CPU hot paths;
   - it does not by itself quantify database time, network waits, lock waits, or total request wall-clock time;
   - missing symbols or sampling bias reduce confidence;
   - inclusive time can include callees and recursion.
6. Correlate with endpoint timings, ASP.NET events, EF/SQL telemetry, GC events, and browser timing before assigning end-to-end impact.

## Reporting

For each hot frame include profile name, unit, self weight, inclusive weight, percentage, symbol, file/line when present, and the trace limitation. Label a source-level optimisation as a hypothesis until a controlled benchmark demonstrates improvement.

Do not modify source code as part of trace analysis.
