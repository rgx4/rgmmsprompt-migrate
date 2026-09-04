You are performing a READ-ONLY migration analysis.

Your task is NOT to implement a migration yet.

Your task is to study the real GitHub Copilot environment in which you are currently running, compare it with the reference workflow model described below, determine what is actually applicable, and propose a target architecture and incremental migration plan.

The reference model below was exported from an existing ChatGPT + Claude Code working system. It describes how I work today and which behaviors I would like to preserve where they still make sense.

CRITICAL PRINCIPLE:

"The exported ChatGPT/Claude workflow is a reference model, not a technical specification that must be reproduced literally."

Do not force the current repository, workspace, GitHub environment, editor, or Copilot installation to imitate Claude Code.

Instead:

1. understand the reference model;
2. investigate the real environment;
3. verify what capabilities actually exist;
4. compare them;
5. preserve useful behavioral properties;
6. adapt them to native Copilot mechanisms where possible;
7. simplify where appropriate;
8. explicitly reject concepts that do not translate well;
9. identify capability or permission gaps honestly;
10. propose an architecture and migration plan;
11. do not implement anything during this first execution.

Respond in Brazilian Portuguese. Keep exact filenames, commands, feature names, technical identifiers, and configuration keys in their original form when appropriate.


======================================================================
PART A — PRIMARY OBJECTIVE
======================================================================

I want to transport as much as is useful from my current AI-assisted development system into GitHub Copilot.

The desired result is NOT necessarily a one-to-one migration.

I want a Copilot-native architecture that preserves useful properties such as:

- task routing;
- specialized roles;
- separation of responsibilities;
- durable context;
- repository-specific context;
- workflow-specific context;
- evidence-driven analysis;
- explicit planning before implementation where appropriate;
- controlled implementation;
- verification gates;
- review loops;
- independent testing workflows;
- documentation maintenance;
- reusable lessons;
- human confirmation gates;
- scope control;
- minimal context duplication;
- protection against instruction conflicts;
- explicit handling of uncertainty;
- traceability between phases;
- safe cross-project coordination;
- the ability to use a lightweight path for trivial work without bypassing important safety rules.

You must determine how much of that is sensible and technically possible in the actual Copilot environment.


======================================================================
PART B — REFERENCE MODEL: WHAT EXISTS TODAY
======================================================================

The following describes the important parts of my current working model.

Treat these as behavioral requirements or design intentions to evaluate, not as implementation requirements.


----------------------------------------------------------------------
B1. Overall purpose of the current ChatGPT project
----------------------------------------------------------------------

The current ChatGPT project acts primarily as a prompt router for a Claude Code development ecosystem.

Its normal job is not to write production code directly.

Instead, when I describe a development task, it tries to:

1. identify the task type;
2. identify the repositories/projects/surfaces involved;
3. determine whether the task is single-project or cross-project;
4. inspect the relevant active artifact/workflow state;
5. choose the smallest valid route;
6. generate the appropriate Claude Code skill invocation or task-specific agent prompt.

The design preference is:

- route work through a user-facing skill when possible;
- use the smallest agent set that can correctly perform the task;
- avoid chaining multiple roles when one is enough;
- preserve human control over phase transitions;
- avoid turning the main chat into a generic coding agent.

The prompt router normally distinguishes:

- research;
- defect investigation;
- planning;
- implementation;
- review;
- independent test-only work;
- test-convention discovery;
- documentation repair;
- lesson recording;
- explicit multi-phase workflows.

A task-specific agent prompt contains only facts that are specific to that task, rather than duplicating the entire governance system.


----------------------------------------------------------------------
B2. Authority and context hierarchy
----------------------------------------------------------------------

The current root workspace has historically been under:

C:\Code

Do NOT assume the target Copilot workspace uses this path. Discover the actual workspace root.

The current reference model uses this authority order:

1. root `C:\Code\CLAUDE.md`
2. root `.claude/docs/`
3. per-project `<project>/CLAUDE.md`
4. per-project `<project>/.claude/`
5. `aiInstructions/`
6. archives/tombstones/historical artifacts

Important semantics:

- higher authority overrides lower authority;
- root rules are meta/workspace-level;
- project-specific stack, tooling, patterns and exceptions belong at project level;
- indexes/registries are pointers, not places where behavioral rules should be hidden;
- `aiInstructions/` is transitional project/domain knowledge rather than the preferred long-term governance source;
- archives and tombstones are historical evidence only;
- missing facts must not be invented;
- project rules must not silently contradict root rules.

One migration question for you is whether Copilot has useful equivalents for this layered context/authority model, and whether the same layering should be retained, simplified, or redesigned.


----------------------------------------------------------------------
B3. Core workflow
----------------------------------------------------------------------

The conceptual flow is:

Research
  ->
Plan
  ->
Implement
  ->
Review
  ->
Record durable learning when applicable

The phases have separate responsibilities.

Simple tasks may legitimately skip phases, but phases should not be reordered arbitrarily.

For example:

- a trivial docs correction may not need research and planning;
- a defect normally begins with bug investigation rather than generic research;
- an active, already-valid artifact may allow entering a later phase directly;
- full workflow coordination is opt-in rather than automatic.

The system prefers deliberate phase boundaries over a single agent that researches, decides, edits, approves its own work, and records its own conclusions without independent checks.


----------------------------------------------------------------------
B4. Routing modes
----------------------------------------------------------------------

The current routing model conceptually supports these modes:

### clarify

Use when genuinely required input is absent.

Ask one focused question.

Do not fabricate missing scope, IDs, paths, branch names, intended behavior, approvals, artifact state, or other required values.

### direct-agent

One complete role can perform the requested phase.

This is the normal mode.

### dispatch

The task contains dependent phases, but I did not explicitly authorize automatic coordination.

Only the next runnable phase is selected.

The handoff to the following phase is informational/manual.

### fleet

Reserved for genuinely independent tasks that can run safely in parallel without shared mutable state.

This is uncommon.

Do not use parallelism merely because the task is large.

### explicit-chain

Used only when I explicitly ask to run a complete multi-phase sequence.

The current Claude ecosystem uses an opt-in workflow coordinator for this.

Even then, lifecycle gates, pause gates, locks, review limits, and human confirmation requirements remain valid.

Agents themselves do not dispatch agents.


----------------------------------------------------------------------
B5. Canonical task routes
----------------------------------------------------------------------

The current user-facing conceptual routes are approximately:

Understand existing behavior or architecture:
`/research`

Investigate a defect/root cause:
`/bug-investigate`

Convert known scope or research into execution phases:
`/plan`

Apply an active research/plan/review artifact:
`/implement`

Review a branch/diff/PR/commit/files:
`/review`

Perform independent test-only work:
`/write-tests`

Discover missing test conventions:
`/analyze-conventions`

Repair documentation/reference drift:
`/update-docs`

Record a completed, traceable learning:
`/record-lesson`

Explicitly coordinate a complete workflow:
`/workflow-start ...`

The workflow system also has status/resume/cancel-style operations for persisted workflow state.

Do NOT assume Copilot needs slash commands with these exact names.

Determine whether the appropriate Copilot equivalent is:

- reusable prompts;
- custom agents;
- skills;
- instructions;
- CLI commands;
- chat modes;
- another mechanism;
- or no separate mechanism at all.


----------------------------------------------------------------------
B6. Specialized roles
----------------------------------------------------------------------

There are eight current role boundaries worth evaluating.


### 1. researcher

Purpose:
Document what currently exists.

Typical trigger:
I want to understand existing behavior, architecture, data flow, integrations, or code before deciding what to change.

Responsibilities:

- locate relevant files/projects;
- describe current implementation;
- trace entry points and data flows;
- identify observed patterns and constraints;
- identify integration points;
- record open questions;
- cite concrete `path:line` evidence for substantive codebase claims.

Important restriction:

The researcher does NOT recommend changes.

It should not become a critic, planner or implementer.

Its output answers "what exists?" rather than "what should we change?"

Historically it produces a durable research artifact.


### 2. bug-investigator

Purpose:
Investigate a reported defect and establish evidence-backed root cause.

Typical trigger:
A symptom, error, failing scenario, production problem, smoke-test failure, regression, etc.

Responsibilities:

- reproduce/trace the symptom when feasible;
- inspect code and relevant tests;
- maintain hypotheses;
- eliminate unsupported hypotheses;
- identify a confirmed root cause;
- describe the likely fix;
- collect validation evidence.

Restrictions:

- no production source edits;
- no test edits intended to implement the fix;
- the fix is described, not applied;
- if the correct fix scope becomes broader than a simple directly authorized repair, it should route toward planning.

This role is deliberately different from generic research because it may reach a diagnostic conclusion and describe the fix.


### 3. planner

Purpose:
Turn known evidence/scope into an executable implementation plan.

Inputs may include:

- research artifact;
- bug investigation;
- explicit user scope;
- existing project evidence.

Responsibilities:

- state the problem;
- define in-scope and out-of-scope work;
- identify exact impacted areas/files where evidence allows;
- split work into deterministic phases;
- define automated verification;
- define manual verification;
- identify risks and mitigations;
- define pause/handoff gates;
- handle cross-project ordering when required.

Restrictions:

- no production source edits;
- no execution of plan phases;
- do not fabricate missing intent;
- cross-project work uses orchestration planning rather than pretending it is one repository-local operation.


### 4. implementer

Purpose:
Be the only production-source editing role.

Important constraint:
Implementation requires a valid active input artifact.

Accepted conceptual inputs include:

- active research/bug artifact when direct implementation is authorized;
- active implementation plan;
- active review artifact with explicitly authorized finding IDs.

Responsibilities:

- edit production source only within authorized scope;
- own tests that are part of the feature/fix itself;
- use Red-Green or equivalent implementation verification;
- execute phase-specific validation;
- update artifact progress where the workflow requires it;
- stop on failing mandatory validation;
- hand off to review when implementation is complete.

Restrictions:

- no inventing scope;
- no research artifact creation;
- no plan creation;
- no self-review;
- no editing the review artifact;
- in fix-review mode, it may fix ONLY finding IDs explicitly authorized by the latest review round.


### 5. reviewer

Purpose:
Independently evaluate changes.

Review surfaces can include:

- .NET/backend;
- React/JavaScript/TypeScript;
- shared contracts;
- database migrations;
- cross-project integration;
- other project-specific surfaces.

Responsibilities:

- inspect source/diff/branch/PR scope;
- identify correctness issues;
- identify regression risk;
- evaluate architecture/convention fit;
- distinguish blockers from lesser findings;
- verify prior fixes using evidence;
- give a final recommendation.

Restrictions:

- never edit production source;
- do not approve with an unresolved blocker;
- do not mark findings resolved without verification evidence;
- do not create duplicate active review artifacts for the same feature.

For external review comments, PR comments, or static-analysis findings, a useful current analysis format is:

1. verdict:
   `correct | partially-correct | incorrect`
2. impact:
   `cleanup | semantic | regression | style`
3. action:
   `accept | reject | partial | narrower-fix`
4. reviewer-ready reply
5. follow-up verification

This is meant to prevent blindly accepting reviewer or analyzer feedback.


### 6. unit-test-writer

Purpose:
Independent test-only work where production code is NOT being changed.

This role is deliberately NOT used for feature/bug tests tied to implementation; those belong to `implementer`.

Supported conceptual modes currently include:

- `characterization`
- `coverage`
- `test-debt`
- `additional-scenarios`
- `test-contract`

The invocation is deliberately narrow:

- exactly one mode;
- exactly one surface;
- exactly one service/project;
- explicit mode-specific inputs.

The system avoids guessing test paths or silently using generic conventions.

If project test conventions have not been captured, the workflow first uses a separate conventions-analysis path.

`test-contract` is special because it produces a persistent contract/artifact rather than directly editing tests.


### 7. doc-updater

Purpose:
Documentation/reference maintenance only.

Typical uses:

- files moved or renamed;
- paths became stale;
- cross-references broke;
- documentation drift needs repair.

Current behavior separates:

1. discovery/read-only pass;
2. exact proposed file list;
3. approval where required;
4. tightly scoped write pass.

Important concepts:

- application source is out of scope;
- high-authority governance files are protected;
- some higher-tier files require file-by-file human approval;
- exact discovered paths are preferred over broad directory write access;
- unresolved references must be reported rather than invented.


### 8. lesson-recorder

Purpose:
Record durable operational knowledge after real completed work.

A lesson is NOT:

- a generic session note;
- speculation;
- a changelog dump;
- an unverified idea.

Typical eligible sources:

- a completed non-trivial task;
- a confirmed bug;
- a recurring gotcha;
- a verified pattern;
- an architectural decision.

Current flow:

1. collect traceable origin;
2. choose scope;
3. check for duplicate/similar lessons;
4. draft;
5. show the draft to the human;
6. save only after explicit confirmation.

Lessons are append-oriented and traceable.

Scope concepts currently include:

- project;
- cross-project;
- workspace.


----------------------------------------------------------------------
B7. Durable artifacts and lifecycle
----------------------------------------------------------------------

The current system relies heavily on durable artifacts rather than keeping important state only inside chat history.

Common artifact families include:

Research:
`thoughts/research/...`

Bug research:
`thoughts/research/...bug...`

Plans:
`thoughts/plans/...`

Cross-project plans:
an orchestration-style plan under `thoughts/plans/...`

Reviews:
`thoughts/reviews/...`

Independent test contracts:
`thoughts/test-contracts/...`

Workflow state:
persistent coordinator state when an explicit multi-phase workflow is active.

The exact folder design is Claude-specific and is NOT automatically a migration requirement.

The behavior to evaluate is durable, inspectable, version-conscious context between phases.


### Artifact lifecycle

Current canonical status concepts are:

- `draft`
- `active`
- `superseded`
- `completed`

Important semantics:

- downstream work generally requires an `active` artifact;
- old/historical statuses are not accepted as active execution input;
- an artifact has a stable `feature_key` or equivalent correlation identity;
- before starting duplicate research/planning, active artifacts for the same feature area should be discovered and consumed;
- replacing a plan should supersede the prior plan rather than leave multiple conflicting active plans;
- closed artifacts should not silently reopen;
- historical artifacts remain useful evidence but not current authority.


### Artifact-first writing

For research/planning/review work, the current model prefers creating the artifact skeleton early and filling it incrementally.

The reason is resilience:

- durable partial work survives context rotation;
- scope becomes explicit early;
- handoffs have an inspectable source.

This behavior should be evaluated for Copilot.

Do NOT create such artifacts during this migration analysis.


----------------------------------------------------------------------
B8. Plan pause gates
----------------------------------------------------------------------

Implementation plans may contain multiple phases.

A phase can require:

- automated verification;
- manual verification;
- an explicit pause before the next phase.

A workflow coordinator is not allowed to bypass a plan's pause gate merely because the next phase is known.

The underlying design principle is:

"automation cannot silently replace a human validation gate."

Determine whether Copilot has a natural way to model this, or whether a simpler manual protocol would be more reliable.


----------------------------------------------------------------------
B9. Persistent review/fix loop
----------------------------------------------------------------------

The review process is intentionally persistent.

Conceptually:

Implementer completes change
  ->
Reviewer creates Review Round 1
  ->
Reviewer identifies findings
  ->
Reviewer explicitly lists "Authorized for fix"
  ->
Implementer fixes ONLY those authorized finding IDs
  ->
Reviewer appends Round 2 to the SAME review record
  ->
Reviewer verifies evidence
  ->
If necessary, another controlled Round 3
  ->
Approval or explicit human intervention

Important current rules:

- one persistent review artifact per `feature_key`;
- do not create a second active review record for the same feature;
- review findings have stable IDs;
- only the latest round's authorized IDs are editable in fix-review mode;
- reviewer verifies fixes rather than implementer self-closing them;
- blocker findings prevent approval;
- findings cannot close without evidence;
- an approval can become stale when the reviewed commit changes;
- only Rounds 2 and 3 are automatic fix-review rounds;
- Round 4+ requires explicit human override.

Do not assume Copilot should reproduce the exact round count.

Evaluate whether the underlying control principle is useful and how it could be represented natively.


----------------------------------------------------------------------
B10. Test ownership boundary
----------------------------------------------------------------------

This distinction is important:

Tests belonging to a production feature or bug fix:
owned by the implementer as part of the same Red-Green implementation lifecycle.

Independent test-only work:
owned by the specialized test role.

The system deliberately avoids handing feature tests to a separate test writer because that would split responsibility for the implementation's correctness.

Evaluate whether this boundary remains useful in Copilot.


----------------------------------------------------------------------
B11. Cross-project coordination
----------------------------------------------------------------------

The workspace can contain multiple related repositories/projects.

Cross-project work is treated differently from a single-project change.

The planning layer is expected to identify:

- projects in scope;
- execution order;
- integration points;
- contracts;
- handoffs;
- risks;
- validation across boundaries;
- rollback implications when relevant.

The current preferred coordination mode is planner/orchestration rather than blindly chaining independent implementers.

The system must not invent repository names or service relationships.

This is especially important because my real work frequently involves related backend/frontend/services, release branches, migrations, PRs, smoke tests and cross-repository behavior.


----------------------------------------------------------------------
B12. Explicit workflow coordinator
----------------------------------------------------------------------

The normal workflow does NOT automatically chain agents.

Explicit full-sequence coordination exists only when requested.

The current coordinator maintains concepts such as:

- `feature_key`;
- task type;
- objective;
- project list;
- ordered phase list;
- current phase;
- workflow status;
- completed phases;
- artifact paths;
- pause state;
- open review findings;
- locks or equivalent concurrency protection.

Coordinator principles:

- preserve stored workflow order;
- do not silently clear locks;
- do not resume paused work without required confirmation;
- do not bypass artifact validation;
- do not bypass manual verification;
- do not bypass review round limits;
- cancellation must not erase historical artifacts;
- agents themselves do not spawn other agents.

Determine whether Copilot has any native equivalent for this.

It is perfectly acceptable to conclude that a simpler architecture is preferable.


----------------------------------------------------------------------
B13. Evidence and ambiguity discipline
----------------------------------------------------------------------

A core rule is:

Never fabricate required values.

Examples:

- branch;
- commit;
- PBI/bug/task IDs;
- user-facing behavior;
- project/service name;
- file path;
- threshold;
- command;
- validation;
- artifact state;
- human approval;
- review round;
- workflow state.

Current role-specific inference behavior is:

Roles whose purpose inherently involves reaching conclusions from code evidence:

- researcher;
- bug-investigator;
- reviewer.

They may draw role-appropriate conclusions only when evidence supports them, and important claims should cite `path:line` or equivalent concrete evidence.

Roles that execute declared intent rather than discover intent:

- planner;
- implementer;
- unit-test-writer;
- doc-updater;
- lesson-recorder.

They should not fill genuinely missing required intent by guessing.

No role may infer past:

- a human confirmation gate;
- a pause gate;
- an artifact lifecycle gate;
- a review-round gate;
- an approval gate.

The old concept of an `infer:` metadata flag was retired because unsupported/decorative metadata is worse than explicit behavioral rules.

This is a useful migration principle:

Do not design Copilot configuration around fields or mechanisms unless you can verify that the installed environment actually enforces them.


----------------------------------------------------------------------
B14. Mechanical enforcement
----------------------------------------------------------------------

The Claude environment does not rely entirely on prose instructions.

Some important controls are mechanically enforced through scripts/hooks/validators.

Examples of current design concepts include:

- artifact validators;
- exact-path write scope manifests;
- scope guards;
- command guards;
- stop gates;
- read-only/build-test/metadata/implementation command profiles;
- restrictions on dangerous Git/deployment operations;
- review-area write protection;
- SQL mutation protection;
- root-governance consistency audits.

The exact current Claude implementation includes mechanisms with names similar to:

- `validate-artifact.ps1`
- `scope-manifest-guard.ps1`
- `bash-command-guard.ps1`
- stop/scope hooks

Do NOT attempt to reproduce these exact scripts.

Instead, determine:

1. which protections are behaviorally valuable;
2. which Copilot mechanisms can enforce them;
3. which can only be advisory in Copilot;
4. whether editor permissions, CLI permissions, hooks, MCP policy, repository permissions, GitHub protections, or some other layer should own them;
5. where exact enforcement is impossible.

A critical migration goal is distinguishing:

"we told the AI not to do it"

from:

"the environment actually prevents it."


----------------------------------------------------------------------
B15. Fast path
----------------------------------------------------------------------

The current workflow has a narrow fast path for trivial, obvious, low-risk changes.

The principle is not "always Research -> Plan -> Implement -> Review".

That would be unnecessarily expensive.

However, the fast path should only apply when clearly eligible.

If uncertain, the normal controlled flow wins.

Changes to root workflow/governance infrastructure still require a consistency audit even when otherwise small.

Evaluate whether a comparable lightweight path is useful in Copilot and how it can avoid becoming a loophole.


----------------------------------------------------------------------
B16. Definition of Done principles
----------------------------------------------------------------------

A task is not considered complete merely because code was edited.

Important current completion concepts include:

- files are in canonical locations;
- no accidental knowledge loss;
- changed references resolve;
- artifacts reflect final lifecycle state;
- indexes remain pointers rather than hidden behavior stores;
- uncertainties/deferred work are explicitly recorded;
- relevant automated verification passes;
- required human verification is confirmed;
- reviews produce a final recommendation;
- lesson recording requires confirmation;
- no out-of-scope files were modified.

Treat this as a quality model to evaluate, not a mandatory template.


----------------------------------------------------------------------
B17. Documentation architecture
----------------------------------------------------------------------

The current model deliberately separates:

### Workspace/meta governance

Root instructions and workflow rules.

### Project-specific instructions

Technology stack, commands, conventions, anti-patterns and repository-specific behavior.

### Transitional/domain knowledge

`aiInstructions/`, historically organized by service/project with:

- architecture analysis;
- inventories;
- integration/service connection notes;
- PBIs/tasks;
- lessons;
- stable docs.

A useful historical pattern inside `aiInstructions` is "read only what you need":

- do not load entire trees indiscriminately;
- choose the 1-3 most relevant documents for the current task;
- use indexes for discovery, not behavior;
- load lessons when relevant or when repeated mistakes occur.

This is intended to control context size and reduce conflicting/stale context.

Historical/archive content must not override current evidence.


----------------------------------------------------------------------
B18. Persistent operational knowledge
----------------------------------------------------------------------

The system has an Operational Knowledge System / lesson concept.

Durable lessons should be:

- traceable to real work;
- scoped appropriately;
- checked for duplication;
- concise and reusable;
- confirmed before persistence;
- marked with `[NEEDS REVIEW]` where evidence is incomplete rather than filled with guesses.

Determine whether Copilot has a better native mechanism for this, or whether repository/workspace files remain appropriate.


----------------------------------------------------------------------
B19. Model resolution
----------------------------------------------------------------------

The current system does not choose models casually.

Some roles have fixed model tiers.

For more reasoning-sensitive roles such as:

- researcher;
- bug-investigator;
- planner;
- reviewer;

the dispatching skill may use a documented trigger vocabulary and resolver to select the model for that invocation.

The important principle is:

"Model Resolution is policy-driven, not intuition-driven."

Do not assume Copilot exposes equivalent model routing.

Investigate whether model choice can actually be controlled:

- globally;
- per agent;
- per prompt;
- per session;
- manually only;
- not at all.

If no equivalent exists, state that clearly instead of inventing one.


----------------------------------------------------------------------
B20. Prompt construction discipline
----------------------------------------------------------------------

When the current router generates a runnable development prompt, it tries not to repeat the whole governance system.

The generated task-specific prompt normally contains only facts such as:

- objective;
- success condition;
- confirmed repository/project/surface;
- branch when confirmed;
- active artifact/review/workflow path;
- `feature_key`;
- bug/PBI/PR identifiers;
- exact files/diff when known;
- customer scenario;
- prior evidence;
- exceptional constraints;
- confirmed validation;
- exact stop condition.

General behavior remains in reusable agent/skill/governance contracts.

This reduces token duplication and instruction drift.

Evaluate how this pattern maps to Copilot reusable prompts, instructions and agents.


----------------------------------------------------------------------
B21. Root vs project specificity
----------------------------------------------------------------------

The current root governance intentionally avoids encoding every project's:

- stack;
- service list;
- lint rules;
- test framework;
- implementation conventions.

Those belong closer to each project.

The desired design property is:

"global context contains stable global behavior; local context contains local technical rules."

I do not want a highly specialized workflow to contaminate every Copilot conversation unnecessarily.

This is a major migration criterion.


----------------------------------------------------------------------
B22. Human control
----------------------------------------------------------------------

Important user-controlled gates include:

- missing intent;
- manual verification;
- protected documentation changes;
- lesson persistence;
- review continuation after configured automatic rounds;
- destructive/privileged operations;
- explicit full-workflow coordination.

The system should automate repeated mechanical steps without silently taking decisions that belong to the human.


======================================================================
PART C — IMPORTANT SOURCE QUALITY NOTE
======================================================================

The reference model above is curated from:

- current project instructions;
- current `.claude` governance snapshots;
- observed workflows;
- historical/transitional `aiInstructions`;
- real examples of how tasks have been routed.

There may be historical remnants in the real workspace.

For example, older files may describe:

- legacy agent rosters;
- `.github/agents` experiments;
- old `AGENTS.md` orchestration;
- old authority documents;
- retired `infer:` fields;
- older artifact schemas;
- obsolete session-memory ideas;
- archived dispatch maps.

When you inspect the real environment:

DO NOT assume that every AI-related file you find is current.

Classify evidence as something like:

- current/canonical;
- current but project-specific;
- transitional;
- legacy;
- tombstone;
- archived;
- uncertain.

Prefer active, referenced sources over old snapshots or archived files.


======================================================================
PART D — FIRST EXECUTION RESTRICTIONS
======================================================================

THIS FIRST EXECUTION IS ANALYSIS ONLY.

You MUST NOT:

- edit source code;
- edit documentation;
- create final configuration files;
- create Copilot instruction files;
- create agents;
- create skills;
- create reusable prompt files;
- change editor settings;
- change GitHub settings;
- change repository settings;
- change MCP configuration;
- change CI/CD;
- change hooks;
- modify workflow files;
- perform the migration;
- create migration scaffolding;
- commit;
- push;
- open a PR;
- merge;
- rebase;
- reset branches;
- run deployments;
- run database migrations;
- execute destructive commands;
- execute privileged administrative operations.

You may perform safe READ-ONLY discovery needed for the study, such as:

- listing directories;
- reading files;
- searching text;
- checking Git status/log/branch metadata;
- inspecting configuration;
- inspecting installed tool/extension/CLI versions;
- using help/version/status commands that do not mutate state;
- inspecting available MCP/tools/integrations;
- inspecting repository metadata available read-only.

Avoid commands that create generated outputs/caches or mutate the working tree unless absolutely necessary for discovery.

If a capability cannot be verified without changing configuration or requesting an administrator action, classify it accordingly instead of attempting the change.

The deliverable from this execution must be:

STUDY + PROPOSED ARCHITECTURE + MIGRATION PLAN

Nothing more.


======================================================================
PART E — DISCOVERY PHASE: INVESTIGATE THE REAL ENVIRONMENT
======================================================================

Before proposing anything, inspect the actual environment you are running in.

Do not start from assumptions about what GitHub Copilot "normally supports".

Investigate what THIS environment actually has.


----------------------------------------------------------------------
E1. Workspace and repository topology
----------------------------------------------------------------------

Determine, as far as accessible:

- actual workspace root;
- whether this is one repository or a multi-repository workspace;
- repository roots;
- Git branches;
- relevant remotes;
- monorepo vs multiple repos;
- workspace files;
- major project/service directories;
- source/test/doc organization;
- shared root folders;
- existing AI-related directories;
- whether a root orchestration repository exists.


----------------------------------------------------------------------
E2. Existing instruction/context system
----------------------------------------------------------------------

Search for current instruction sources.

Do not assume filenames.

Investigate things such as:

- repository instruction files;
- personal/global instruction configuration;
- path-scoped instructions;
- workspace-scoped instructions;
- README/CONTRIBUTING/development instructions;
- AGENTS-like files;
- CLAUDE-like files;
- Copilot-specific instruction files;
- editor workspace settings;
- repository metadata that influences Copilot;
- existing reusable prompts;
- existing custom agents;
- existing skills or equivalent abstractions;
- prompt catalogs;
- task definitions;
- automation configuration.

For each one found, determine:

- exact path;
- whether it appears active;
- scope;
- precedence if known;
- whether it is version controlled;
- who is expected to maintain it;
- whether it already overlaps the reference model.


----------------------------------------------------------------------
E3. GitHub Copilot capabilities actually available
----------------------------------------------------------------------

Identify the actual Copilot surface you are running within, for example:

- VS Code;
- Visual Studio;
- JetBrains;
- CLI;
- GitHub.com;
- agent mode;
- another environment.

Identify installed/accessible Copilot-related capabilities.

Potential mechanisms to investigate include, but are not limited to:

- global/personal instructions;
- repository instructions;
- path-specific instructions;
- reusable prompt files;
- skills;
- custom agents;
- agent mode;
- chats;
- sessions;
- Spaces;
- editor mechanisms;
- Copilot CLI;
- GitHub integrations;
- MCP;
- tool access;
- terminal access;
- GitHub API access;
- repository/PR integration;
- code-review features;
- memory/persistence features;
- model selection;
- hooks;
- command/permission controls;
- organization policies.

THIS LIST IS NOT A REQUIRED TARGET ARCHITECTURE.

It is a discovery checklist.

If the installed version provides a help command, built-in documentation, schemas or example configuration, inspect those where useful.

Prefer evidence from the installed environment.

If you consult generic external product documentation, explicitly distinguish:

"GitHub documents this feature"

from:

"This feature is verified as available and usable in the current environment."


----------------------------------------------------------------------
E4. Capability availability classification
----------------------------------------------------------------------

For each Copilot capability relevant to this migration, classify availability as:

- VERIFIED AVAILABLE
- PROBABLY AVAILABLE
- REQUIRES CONFIGURATION
- REQUIRES ADMIN/ORG PERMISSION
- NOT AVAILABLE
- COULD NOT DETERMINE

Give evidence for the classification.

Do not claim support because you remember that Copilot supported something in another version/editor.


----------------------------------------------------------------------
E5. Existing development workflow
----------------------------------------------------------------------

Inspect current repository conventions:

- build;
- tests;
- lint;
- formatting;
- CI;
- PR process;
- code owners;
- branch protections when visible;
- GitHub Actions or other CI/CD;
- Azure DevOps-related configuration if present;
- local scripts;
- test organization;
- release/version conventions;
- documentation conventions;
- project-specific instructions.

Do not run the full development lifecycle merely to discover it.

Read definitions and configuration first.


----------------------------------------------------------------------
E6. Existing automation and guardrails
----------------------------------------------------------------------

Look for:

- hooks;
- scripts;
- pre-commit checks;
- CI policies;
- repository protections;
- local permission configuration;
- MCP restrictions;
- shell/tool allowlists;
- validators;
- generated manifests;
- agent permissions;
- review gates;
- safety scripts.

Determine whether anything already solves requirements from the reference model.


----------------------------------------------------------------------
E7. Existing `.claude` / `aiInstructions` system
----------------------------------------------------------------------

If the current workspace still contains the Claude system described above, inspect it as migration source evidence.

Use the source authority order where it is applicable:

1. current root governance;
2. current `.claude/docs`;
3. current project instructions;
4. current project `.claude`;
5. transitional `aiInstructions`;
6. archives last.

Do not automatically decide that these files should remain after migration.

Your task is to understand what behavior they encode and decide what should be migrated, adapted, retired or retained.


======================================================================
PART F — MAP THE REFERENCE MODEL TO COPILOT
======================================================================

For every major component listed below, analyze:

1. What does the component do in the reference system?
2. What problem does it solve?
3. Is there a direct Copilot equivalent?
4. Is there only a partial equivalent?
5. Would it have to be rebuilt?
6. Could it be simplified?
7. Is migration unnecessary?
8. Where should it live if migrated?
9. What should its scope be?
10. How should duplicate context be avoided?
11. How should conflicting instructions be prevented?
12. How should it be maintained?
13. Can the behavior be mechanically enforced or only instructed?
14. What permissions or product features does it depend on?


Components to map:

- root/global governance;
- project-specific governance;
- task router;
- routing modes;
- user-facing task commands;
- researcher role;
- bug-investigator role;
- planner role;
- implementer role;
- reviewer role;
- unit-test-writer role;
- test-conventions discovery;
- doc-updater role;
- lesson-recorder role;
- artifact contracts;
- artifact lifecycle;
- artifact-first persistence;
- `feature_key` correlation;
- plan pause gates;
- review/fix rounds;
- test ownership boundary;
- cross-project orchestration;
- explicit workflow coordinator;
- persistent workflow state;
- locks/concurrency protections;
- human approval gates;
- scope/write protection;
- command safety rules;
- validation rules;
- Definition of Done;
- operational lessons/knowledge;
- model resolution;
- reusable prompt construction;
- prompt-router behavior;
- external PR/review-comment analysis;
- MCP/tool integration;
- fast path;
- root post-change audit;
- transitional `aiInstructions`;
- archive/tombstone handling.


======================================================================
PART G — TARGET SCOPE CLASSIFICATION
======================================================================

For each recommended target component, classify where it belongs.

Possible scopes include:

### Personal

Behavior that is specifically about how I prefer to work and should follow me across unrelated repositories.

### Global/workspace

Behavior shared across related repositories in this development workspace.

### Workflow-specific

Behavior that should load only when a workflow such as research, bug investigation, planning, implementation or review is selected.

### Project-specific

Technical behavior shared by one project.

### Repository-specific

Rules that belong to one repository and should normally be versioned there.

### Path-specific

Rules applicable only to certain source areas.

### Task-specific

Facts that should be passed only for one invocation and should never become global instructions.

Do not choose global scope merely because it is convenient.

One explicit goal is to prevent specialized instructions from contaminating unrelated Copilot chats.


======================================================================
PART H — VIABILITY CLASSIFICATION
======================================================================

Be critical.

For every material migration idea, classify it as one of:

- VIABLE DIRECTLY
- VIABLE WITH SMALL ADAPTATIONS
- VIABLE WITH RECONSTRUCTION
- PARTIALLY VIABLE
- NOT RECOMMENDED
- NOT POSSIBLE IN CURRENT ENVIRONMENT
- REQUIRES ADDITIONAL INVESTIGATION

Explain the reason.

Do NOT conclude that everything can be migrated.


======================================================================
PART I — DESIGN PRINCIPLES FOR THE PROPOSED ARCHITECTURE
======================================================================

Your proposed architecture should emerge only after discovery.

Do not design it before examining the environment.

Optimize for:

- native Copilot mechanisms;
- low duplication;
- understandable maintenance;
- small global context;
- project-local technical rules;
- workflow-specific instructions loaded on demand;
- narrow task prompts;
- durable evidence where persistence has real value;
- human-visible state;
- reliable handoffs;
- clear role boundaries;
- minimum number of abstractions;
- enforceable safety where possible;
- explicit distinction between enforced policy and advisory prompt text;
- compatibility with multi-repository work if the workspace requires it.

Avoid recreating complexity merely because Claude currently has it.

For example:

- if one Copilot feature replaces three Claude abstractions cleanly, prefer the simpler Copilot design;
- if Copilot has no safe way to emulate an agent permission boundary, do not pretend that an instruction gives the same security;
- if persistent artifact files are still the best cross-session mechanism, say so;
- if Copilot has a stronger native persistence mechanism, evaluate replacing artifacts;
- if custom agents would duplicate path-specific instructions, eliminate the duplication.


======================================================================
PART J — MIGRATION PLAN REQUIREMENTS
======================================================================

After proposing the architecture, create an incremental migration plan.

Do NOT recommend migrating everything at once.

Use stages similar to:

1. discovery completion;
2. minimal proof of concept;
3. validation;
4. gradual migration;
5. workflow integration;
6. guardrails;
7. persistence/knowledge migration;
8. cleanup/retirement;
9. ongoing maintenance.

Each phase should explain:

- objective;
- components involved;
- likely files/settings/features;
- prerequisites;
- risk;
- validation;
- rollback/reversibility;
- user/admin decisions required.


======================================================================
PART K — PROOF OF CONCEPT
======================================================================

Recommend ONE small, reversible first proof of concept.

Choose something that is:

- representative of the larger system;
- low risk;
- easy to remove;
- quick to validate;
- capable of testing important Copilot capabilities.

Do not automatically choose a particular component before discovery.

Possible examples could include:

- one reusable research workflow;
- one repository instruction hierarchy;
- one custom read-only research agent;
- one reusable prompt with project instructions;
- another mechanism discovered locally.

For the selected POC explain:

1. why it is the best first experiment;
2. exactly which capability it tests;
3. which target files/configuration/features would probably be involved;
4. what would NOT be migrated yet;
5. how success would be validated;
6. how failure would be recognized;
7. how to revert it;
8. what we learn regardless of outcome.

Do not implement the POC during this execution.


======================================================================
PART L — EVIDENCE QUALITY
======================================================================

Ground environment claims in evidence.

Where practical, cite:

- exact file paths;
- relevant line ranges;
- configuration keys;
- installed versions;
- command/help output;
- repository structure;
- Git metadata;
- tool listings;
- official local schemas/docs.

Clearly distinguish:

### Verified fact

Directly supported by current environment evidence.

### Observed pattern

Repeated structure seen in the repository/workspace.

### Inference

Reasonable conclusion from evidence, but not explicitly declared.

### Unknown

Could not be established.

Do not silently convert an inference into a fact.


======================================================================
PART M — REQUIRED OUTPUT
======================================================================

Return the report using this structure.


## 1. Entendimento do sistema que quero reproduzir

Summarize the reference system in your own words.

Cover:

- primary goals;
- routing philosophy;
- role separation;
- workflow phases;
- artifact/persistence philosophy;
- safety/validation philosophy;
- context layering;
- human-control philosophy.

Do not merely repeat this prompt.


## 2. Descobertas no ambiente atual

Describe the actual environment.

Include:

- workspace/repository topology;
- Copilot surface/editor/CLI;
- existing instructions;
- existing prompts;
- existing agents/skills if any;
- MCP/tool integrations;
- existing automation;
- CI/CD;
- relevant safety controls;
- project/repository conventions.

Include a capability table with:

| Capability | Status | Evidence | Scope | Permission/config dependency | Notes |

Use the required availability statuses:

- VERIFIED AVAILABLE
- PROBABLY AVAILABLE
- REQUIRES CONFIGURATION
- REQUIRES ADMIN/ORG PERMISSION
- NOT AVAILABLE
- COULD NOT DETERMINE


## 3. Diferenças entre o modelo de referência e o ambiente real

Explain:

- direct matches;
- partial matches;
- important conceptual mismatches;
- Claude-specific concepts with no direct equivalent;
- Copilot-native opportunities that could simplify the system;
- mechanisms already present that make migration unnecessary.


## 4. Mapeamento dos componentes

Create a detailed table.

Suggested columns:

| Reference component | Current purpose | Need being solved | Copilot target mechanism | Target scope | Viability | Adaptation | Enforcement level | Limitations |

Cover every materially relevant component from Part F.


## 5. O que vale a pena migrar

Organize recommendations into:

### Migrar diretamente

### Adaptar

### Reconstruir

### Simplificar

### Não migrar

For each decision, give the reason.


## 6. Arquitetura recomendada

Propose the target architecture based on evidence.

Show:

- component hierarchy;
- where each component lives;
- personal vs shared/versioned content;
- repository vs workspace content;
- on-demand workflow context;
- relationship between instructions/prompts/agents/tools/artifacts;
- how task routing works;
- how a new task begins;
- how a workflow is selected;
- how specialized context is prevented from contaminating unrelated chats;
- how cross-project work operates;
- how human gates work;
- how persistent state works, if retained;
- what is mechanically enforced vs advisory.

A small text diagram is welcome if useful.


## 7. Lacunas e limitações

Be explicit.

List:

- capabilities from the reference model that cannot be reproduced;
- capabilities not verified;
- product limitations;
- editor limitations;
- organization-policy limitations;
- permission dependencies;
- places where enforcement would become prompt-only;
- any uncertainty about feature availability.


## 8. Perguntas ou verificações necessárias

Only include questions that truly require:

- my decision;
- administrator action;
- organization permissions;
- account/product information unavailable to you;
- a capability that cannot be verified locally.

Do NOT ask me questions that the repository or installed environment can answer.


## 9. Plano de migração

Provide incremental phases.

For each phase include:

- objective;
- change category;
- target components;
- prerequisites;
- likely target files/settings/features;
- validation;
- rollback/reversibility;
- risk;
- required human decision.

Do not attempt implementation.


## 10. Prova de conceito recomendada

Choose one small first migration.

Explain:

- what;
- why this one;
- exact behavior being tested;
- likely files/settings/features involved;
- expected interaction;
- validation criteria;
- rollback;
- what the result will teach us.

Again: DO NOT create it yet.


## 11. Próximo passo recomendado

Give me one concrete next action.

For example, the next step may be:

- authorize the POC implementation;
- obtain an admin permission;
- inspect one unresolved environment capability;
- choose between two target architectures.

Do not provide multiple vague next steps.

Choose the single most useful action based on your findings.


======================================================================
PART N — FINAL CONSTRAINTS
======================================================================

Before finishing, verify that you have NOT:

- modified files;
- created migration artifacts;
- created Copilot agents;
- created Copilot prompts;
- created skills;
- changed settings;
- changed GitHub configuration;
- edited `.claude`;
- edited `aiInstructions`;
- edited source;
- committed;
- pushed;
- opened a PR;
- performed a migration.

If you discover that some command or tool caused an unexpected write during discovery, report it immediately and do not hide it.

Your job in this run is to answer:

"What is the best evidence-based way to adapt my existing AI development workflow to the GitHub Copilot ecosystem that is ACTUALLY available in this workspace?"

The exported Claude/ChatGPT workflow tells you what I value.

The real Copilot environment tells you what is possible.

The proposed migration architecture must be derived from both.
