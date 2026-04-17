# Phase Execution Prompts

Ready-to-use prompts for starting each implementation phase. Copy the relevant prompt into Cursor to begin a phase.

---

## How to Use

1. Start a new Cursor agent session.
2. Copy the prompt for the target phase below.
3. Paste it as the first message.
4. The agent will read all referenced files, identify the first task, and begin work.
5. After each task, review the output and approve continuation.
6. At the end of the phase, the agent will produce a Phase Gate Report.

---

## Phase 0 Prompt — Foundations

```
You are implementing Phase 0 (Foundations) of the RBv2 Multifamily Property Assessment Platform.

BEFORE WRITING ANY CODE, read these files in this order:
1. .cursor/rules/agent-behavior.mdc
2. .cursor/rules/execution-protocol.mdc
3. .cursor/rules/phase-0-foundations.mdc
4. .cursor/rules/rbv2-project.mdc
5. specs/patterns/Code_Patterns_Specification.md
6. specs/patterns/API_Design_Specification.md
7. specs/auth/Authentication_Middleware_Specification.md
8. specs/auth/Authorization_Model_Specification.md
9. specs/patterns/Infrastructure_Specification.md
10. specs/patterns/Development_Environment_Specification.md
11. specs/patterns/Observability_Specification.md
12. specs/platform/Project_Skeleton_Specification.md
13. specs/platform/Database_Schema_Specification.md (Layer A raw evidence + tenancy/identity + Domain 2 partial + Domain 10 partial)
14. specs/platform/Service_Interface_Contracts.md (§1 AuthZ, §2 Engagement)
15. planning/Implementation_Tasks.md (Phase 0 section)
16. planning/Deployment_Roadmap.md (Phase 0 section, DDL Scope Per Phase)

After reading all files, identify the first incomplete task (P0-T01 or the first task not marked [x]) and begin implementation following the Execution Protocol.

Work through tasks sequentially: P0-T01, P0-T02, ..., P0-T09, P0-T09a, P0-T09b, P0-T10, ..., P0-T18, then P0-CK1, P0-CK2, P0-CK3.

After completing all tasks and checkpoints, produce a Phase 0 Gate Report per specs/patterns/Phase_Gate_Specifications.md and present it for approval.
```

---

## Phase 1 Prompt — Canonical Core

```
You are implementing Phase 1 (Canonical Core) of the RBv2 platform.

PREREQUISITE: Phase 0 must be complete. Verify by checking that P0-T01 through P0-T18 (including P0-T09a and P0-T09b) and P0-CK1 through P0-CK3 are all marked [x] in planning/Implementation_Tasks.md.

BEFORE WRITING ANY CODE, read these files:
1. .cursor/rules/agent-behavior.mdc
2. .cursor/rules/execution-protocol.mdc
3. .cursor/rules/phase-1-canonical-core.mdc
4. .cursor/rules/rbv2-project.mdc
5. specs/patterns/Code_Patterns_Specification.md
6. specs/platform/Database_Schema_Specification.md (all PostgreSQL domains)
7. specs/platform/Shared_Type_Definitions.md
8. specs/platform/Service_Interface_Contracts.md (§3 Import & Mapping, §4 Entity Resolution)
9. specs/data/Data_Onramp_Specification.md
10. specs/data/Complete_Data_Inventory.md
11. planning/Implementation_Tasks.md (Phase 1 section)

Begin with the first incomplete Phase 1 task. Work sequentially through P1-T01 to P1-T20.

After completing all tasks, produce a Phase 1 Gate Report.
```

---

## Phase 2 Prompt — Temporal Spine

```
You are implementing Phase 2 (Temporal Unit Spine) of the RBv2 platform.

PREREQUISITE: Phase 1 gate passed and approved.

BEFORE WRITING ANY CODE, read these files:
1. .cursor/rules/agent-behavior.mdc
2. .cursor/rules/execution-protocol.mdc
3. .cursor/rules/phase-2-temporal-spine.mdc
4. .cursor/rules/rbv2-project.mdc
5. specs/patterns/Code_Patterns_Specification.md
6. specs/platform/Database_Schema_Specification.md (temporal tables + ClickHouse fact tables)
7. specs/platform/Service_Interface_Contracts.md (§5 Temporal State Builder)
8. specs/engine/Basic_Analytic_Data_Set.md (all 124 KPIs)
9. specs/engine/BADS_Edge_Case_Rules.md
10. planning/Implementation_Tasks.md (Phase 2 section)

Begin with the first incomplete Phase 2 task. Work sequentially through P2-T01 to P2-T12.

After completing all tasks, produce a Phase 2 Gate Report.
```

---

## Phase 3 Prompt — Core Diagnostics

```
You are implementing Phase 3 (Core Diagnostics) of the RBv2 platform.

PREREQUISITE: Phase 2 gate passed and approved.

BEFORE WRITING ANY CODE, read these files:
1. .cursor/rules/agent-behavior.mdc
2. .cursor/rules/execution-protocol.mdc
3. .cursor/rules/phase-3-core-diagnostics.mdc
4. .cursor/rules/rbv2-project.mdc
5. specs/patterns/Code_Patterns_Specification.md
6. specs/scoring/Scoring_Algorithm_Specification.md
7. specs/scoring/Scoring_Model_Specification.md
8. specs/scoring/Scoring_Thresholds_Calibration.md
9. config/scoring_config.json
10. config/Scoring_Weights_Final_Update.json
11. specs/engine/Analytical_Engine_Specification.md
12. specs/engine/Analytical_Engine_Algorithm_Specifications.md
13. specs/engine/Analytical_Question_Inventory.md
14. specs/platform/Service_Interface_Contracts.md (§6 Metric Engine, §7 Scoring Engine, §8 Finding Compiler, §9 Impact Engine)
15. planning/Implementation_Tasks.md (Phase 3 section)

Begin with the first incomplete Phase 3 task. Work sequentially through P3-T01 to P3-T25.

After completing all tasks, produce a Phase 3 Gate Report.
```

---

## Phase 4 Prompt — Workspace & Reporting

```
You are implementing Phase 4 (Workspace & Reporting) of the RBv2 platform.

PREREQUISITE: Phase 3 gate passed and approved.

BEFORE WRITING ANY CODE, read these files:
1. .cursor/rules/agent-behavior.mdc
2. .cursor/rules/execution-protocol.mdc
3. .cursor/rules/phase-4-workspace-reporting.mdc
4. .cursor/rules/rbv2-project.mdc
5. specs/patterns/Code_Patterns_Specification.md
6. specs/ui/UI_UX_Specification.md
7. specs/ui/Report_Template_Specification.md
8. specs/platform/Service_Interface_Contracts.md (§10 Study & Snapshot, §11 Report Rendering)
9. planning/Implementation_Tasks.md (Phase 4 section)

Begin with the first incomplete Phase 4 task.

After completing all tasks, produce a Phase 4 Gate Report.
```

---

## Phase 5 Prompt — Client Portal & Longitudinal Tracking

```
You are implementing Phase 5 (Client Portal and Longitudinal Tracking) of the RBv2 platform.

PREREQUISITE: Phase 4 gate passed and approved.

BEFORE WRITING ANY CODE, read these files:
1. .cursor/rules/agent-behavior.mdc
2. .cursor/rules/execution-protocol.mdc
3. .cursor/rules/phase-5-client-portal.mdc
4. .cursor/rules/rbv2-project.mdc
5. specs/patterns/Code_Patterns_Specification.md
6. specs/ui/UI_UX_Specification.md
7. specs/platform/Service_Interface_Contracts.md (§12 Client Portal Service, §13 Trend & Trajectory Service)
8. specs/platform/Database_Schema_Specification.md (trend-ready ClickHouse tables, recommendation table)
9. planning/Implementation_Tasks.md (Phase 5 section)

Begin with the first incomplete Phase 5 task. Work sequentially through P5-T01 to P5-T15.

After completing all tasks, produce a Phase 5 Gate Report.
```

---

## Phase 6 Prompt — Door Opener & Extensibility

```
You are implementing Phase 6 (Door Opener and Extensibility) of the RBv2 platform.

PREREQUISITE: Phase 5 gate passed and approved.

BEFORE WRITING ANY CODE, read these files:
1. .cursor/rules/agent-behavior.mdc
2. .cursor/rules/execution-protocol.mdc
3. .cursor/rules/phase-6-door-opener.mdc
4. .cursor/rules/rbv2-project.mdc
5. specs/patterns/Code_Patterns_Specification.md
6. specs/scoring/Door_Opener_Applicability_Matrix.md
7. specs/platform/Service_Interface_Contracts.md (§14 Door Opener Service, §15 Extension SDK)
8. specs/data/Data_Onramp_Specification.md
9. specs/data/Audit_Workbook_Specification.md
10. specs/ui/Report_Template_Specification.md
11. specs/platform/Database_Schema_Specification.md (door opener columns in assessment/scorecard/report tables)
12. planning/Implementation_Tasks.md (Phase 6 section)

Begin with the first incomplete Phase 6 task. Work sequentially through P6-T01 to P6-T12.

After completing all tasks, produce a Phase 6 Gate Report.
```
