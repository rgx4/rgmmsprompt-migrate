---
name: workspace-context-research
description: Keep the parent context small by searching first, reading targeted ranges, and delegating broad exploration to isolated subagents that return concise path-based evidence.
argument-hint: "<question or scope>"
user-invocable: true
---

# Context-efficient research

Use this procedure when a task could require broad repository exploration, large files, or verbose logs.

1. Define the specific question before reading broadly.
2. Search for symbols, paths, references, tests, configuration, and documentation first.
3. Prefer targeted file ranges and nearby context over complete-file reads.
4. Delegate broad exploration to `workspace-context-reader` or another isolated exploration subagent when useful.
5. Ask subagents to return only:
   - findings relevant to the question;
   - exact paths and line ranges when available;
   - local guidance/skill names that matter;
   - contradictions and unknowns.
6. Do not bring complete files, giant logs, or unfiltered search output back into the parent context unless explicitly necessary.
7. Summarize before continuing to planning or implementation.

This is a behavioral optimization. No root hook or script mechanically blocks large reads.
