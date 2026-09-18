---
name: workspace-research
description: Explain existing behavior within one or more child repositories using local authority and concrete evidence, without modifying files or drifting into implementation.
argument-hint: "<topic or scope>"
user-invocable: true
---

# Research existing behavior

1. Route the task to the correct repository set with `/workspace-routing` when ownership is unclear.
2. Load applicable local `AGENTS.md`, Copilot instructions, relevant local skills, and canonical documentation.
3. Locate entry points, main modules/types, tests, configuration, contracts, and integration boundaries relevant to the question.
4. Delegate broad exploration with `/workspace-context-research` when useful.
5. Trace the important execution/data flow.
6. Separate:
   - confirmed repository-local facts;
   - confirmed cross-repository relationships;
   - inference;
   - unresolved questions.
7. Cite concrete paths for material claims.
8. Do not edit files or propose changes until the current state is sufficiently clear.

Prefer a focused evidence map over a repository dump.
