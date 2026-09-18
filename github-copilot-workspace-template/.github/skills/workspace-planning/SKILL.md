---
name: workspace-planning
description: Create an executable implementation plan for one or more child repositories using confirmed local evidence, dependency order, local tests, validation, risks, and explicit out-of-scope work.
argument-hint: "<requirement or confirmed research>"
user-invocable: true
---

# Plan a change

1. Confirm repository ownership. Use `/workspace-routing` if needed.
2. Consume existing confirmed research instead of redoing it unless stale or contradictory.
3. Load local repository guidance for every affected repository.
4. Identify exact affected surfaces and likely files only when supported by evidence.
5. For cross-repository work, identify contracts/dependencies and execution order.
6. Break work into the smallest coherent phases.
7. For each phase, state:
   - repository;
   - intended behavior/change;
   - files or surfaces to inspect/modify;
   - tests expected;
   - repository-confirmed validation;
   - dependencies/pause points.
8. Call out risks, unknowns, and explicit out-of-scope work.
9. Do not implement while planning.

If a plan still requires guessing about a material requirement, contract, migration, or owner, stop and return to research.
