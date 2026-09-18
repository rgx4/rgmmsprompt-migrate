Design and implement a repository-native Performance Engineering agent and its supporting skills for this RVG codebase.

First inspect the repository thoroughly:
- existing agents, skills, instructions and conventions
- React frontend architecture
- .NET/API architecture
- EF Core/data-access patterns
- SQL Server usage
- existing k6 performance-test setup
- existing observability, logging, tracing or profiling capabilities

Do not assume agent/skill paths or formats. Follow the conventions already used by this repository and reuse existing skills/instructions where appropriate instead of duplicating them.

Create a main Performance Engineer agent responsible for end-to-end performance investigations.

Its required workflow should be:

symptom
→ reproduce
→ establish baseline
→ measure
→ isolate the slow layer
→ form evidence-based hypotheses
→ select the appropriate specialist skill
→ make the smallest justified change
→ rerun the same measurement
→ compare before/after
→ report evidence and remaining uncertainty

The agent must never optimise purely from code inspection or assume that a slow page means a slow API/database.

It must distinguish, where applicable:
- React rendering/browser work
- HTTP/network/request waterfalls
- API/application code
- EF Core
- SQL Server
- external dependencies
- serialization/payload size
- caching
- concurrency/contention
- infrastructure

Create focused skills for at least:

performance-investigation
General investigation methodology, baselines, hypotheses, experiments, before/after validation and root-cause reasoning.

react-performance
React Profiler, browser Performance/Network tools, request waterfalls, sequential/duplicate requests, expensive renders, re-renders, state/context effects, large lists, client-side processing and page-load analysis.

api-performance
HTTP/API latency, request fan-out, payload size, pagination, serialization, over-fetching, retries, timeouts, dependency calls and endpoint-level bottlenecks.

dotnet-efcore-performance
.NET runtime and EF Core performance, generated SQL, N+1, Includes, projections, tracking, materialisation, allocations, GC, async/thread-pool issues and connection usage.

sql-server-performance
Execution plans, actual vs estimated rows, logical reads, STATISTICS IO/TIME, scans/seeks, joins, indexes, SARGability, statistics, cardinality, parameter sensitivity, memory grants, spills, blocking and query tuning.
Do not recommend indexes blindly from missing-index suggestions.

k6-performance-testing
Use and extend the k6 setup already present in this repository.
Cover discovery, baseline, load, stress, spike and soak testing.
Include warm-up, safe local testing, realistic test data, per-endpoint metrics and correct interpretation of p50/p90/p95/p99/max/error rate/throughput.
Local results must not be treated as production SLOs.

observability-profiling
Use available traces, metrics, logs and profilers to break request latency down across application, SQL, dependencies, serialization, CPU, memory, GC and other relevant components.

The Performance Engineer should choose skills dynamically based on evidence rather than running every skill for every problem.

For a slow RVG page such as Outings or Parts, the expected investigation flow should be approximately:

slow page
→ inspect browser/network behaviour
→ determine frontend time vs API time
→ identify expensive requests or frontend work
→ if frontend: React investigation
→ if backend: API investigation
→ if EF/SQL is involved: inspect generated SQL and database execution
→ reproduce with k6 where useful
→ validate the root cause
→ optimise only after evidence exists
→ rerun the same workload
→ compare before/after

Add strong guardrails:
- never claim an optimisation worked without before/after measurement
- do not confuse average latency with tail latency
- do not treat isolated cold-start/JIT/cache effects as sustained bottlenecks without evidence
- do not confuse correlation with root cause
- do not create caches, indexes, parallelism or architectural changes without evidence
- prefer the smallest change that addresses the measured bottleneck
- preserve correctness and existing behaviour
- do not modify application code as part of creating these agents/skills

Also create a lightweight Performance Finding format that investigations can use, containing:
area/page
environment
symptom
baseline
evidence
suspected layer
hypothesis
experiment
root cause
change
before
after
validation status
remaining risks/questions

Keep the agent orchestration concise and put detailed domain knowledge inside skills rather than creating one huge agent file.

After implementing:
1. show the final agent/skill architecture
2. list every file created or changed
3. explain why each skill boundary was chosen
4. show how the Performance Engineer decides which skill to use
5. verify that the new agent and skills are valid and discoverable using the repository's existing conventions
6. run any relevant repository validation/checks
7. provide 3 example prompts:
   - investigate the slow Outings page
   - investigate the slow Parts page
   - investigate a specific slow SQL/API endpoint

Do not modify RVG production code during this task. This task is only to build and validate the reusable Performance Engineering agent/skill system.