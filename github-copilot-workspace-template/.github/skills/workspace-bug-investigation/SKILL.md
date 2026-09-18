---
name: workspace-bug-investigation
description: Trace an observed defect to an evidence-backed root cause across the smallest relevant repository set without applying the fix.
argument-hint: "<symptom or issue>"
user-invocable: true
---

# Bug investigation

1. State the observed symptom and expected behavior.
2. Route the issue to the smallest plausible repository set.
3. Load local debugging/testing guidance for each repository examined.
4. Trace from user-visible or runtime symptom toward the failing execution path.
5. Build a small hypothesis list.
6. Validate hypotheses against code, tests, configuration, logs, or repository-confirmed diagnostic commands.
7. Reject unsupported hypotheses explicitly.
8. Identify the confirmed or best-supported root cause only when evidence justifies it.
9. Identify likely fix area and regression-test need without editing files.
10. If ownership crosses repositories, explain the causal chain across the boundary.

Do not invent commands. Do not mutate data, deploy, publish, migrate, rewrite history, or fix the bug during investigation.
