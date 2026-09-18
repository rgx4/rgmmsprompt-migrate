---
name: workspace-review
description: Independently review a change across one or more child repositories for material correctness, regression, security, contract, testing, and validation issues without applying fixes.
argument-hint: "<diff or scope>"
user-invocable: true
---

# Review changes

1. Identify the changed repository set and actual diff.
2. Load each repository's local review/testing/architecture guidance.
3. Review changed behavior before style.
4. Inspect surrounding code only as needed to understand risk.
5. For cross-repository work, explicitly review the shared boundary or contract.
6. Prioritize findings involving:
   - correctness;
   - regression risk;
   - security/privacy;
   - data or API compatibility;
   - concurrency/state handling;
   - error handling;
   - architecture-boundary violations;
   - missing or misleading tests;
   - missing required validation.
7. Avoid low-value style findings unless local rules make them correctness-relevant.
8. Do not edit or fix findings during review.
9. Report evidence, impact, and recommended correction for each material finding.

If repository-local reviewer agents/skills exist, prefer them for local details while keeping cross-repository compatibility review at the workspace level.
