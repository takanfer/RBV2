# Progress Tracking Format

Defines the machine-parseable format for tracking implementation progress, completion status, and phase reports.

---

## Task Status Format

In `planning/Implementation_Tasks.md`, each task follows this format:

```
- [ ] **P{N}-T{NN}: {Title}**
```

Status markers:

| Marker | Meaning |
|--------|---------|
| `[ ]` | Not started |
| `[~]` | In progress (current session) |
| `[x]` | Complete — commit hash follows the title after ` — ` |
| `[!]` | Blocked — reason documented below |

Complete format example:
```
- [x] **P0-T01: Project skeleton and Python tooling** — `a1b2c3d`
```

Blocked format example:
```
- [!] **P0-T09: Raw evidence layer migration**
  - BLOCKED: P0-T08 migration has failing downgrade. See issue #12.
```

---

## Phase Progress Summary

At the top of each phase section in `planning/Implementation_Tasks.md`, maintain a summary line:

```
> Phase 0: 14/18 tasks complete, 1 in progress, 1 blocked, 2 not started
```

Update this line whenever a task status changes.

---

## Session Progress File

After each session, create or update a progress file at `planning/progress.md`:

```markdown
# Implementation Progress

## Current Phase: 0 — Foundations

### Status: IN PROGRESS

| Metric | Value |
|--------|-------|
| Tasks Complete | 14/18 |
| Tasks In Progress | 1 (P0-T15) |
| Tasks Blocked | 0 |
| Tests Passing | 42/42 |
| Validator Checks | 1620/1620 |
| Last Commit | `abc1234` |
| Last Session | 2026-04-16 |

### Completed Tasks
| Task | Title | Commit | Date |
|------|-------|--------|------|
| P0-T01 | Project skeleton | `a1b2c3d` | 2026-04-14 |
| P0-T02 | Docker Compose | `e4f5g6h` | 2026-04-14 |

### Blocked Tasks
(none)

### Next Task
P0-T15: CI workflow and Phase 0 tests
```

---

## Phase Gate Report Format

See `Phase_Gate_Specifications.md` for the full gate report template. The progress file should reference the gate report when a phase is complete:

```markdown
## Phase 0: COMPLETE
Gate Report: planning/gate-reports/phase-0-gate.md
Approved: 2026-04-20
```

---

## Commit Tracking

Every implementation commit must include the task ID. The progress tracking system relies on being able to trace commits to tasks.

Commit message format:
```
P{N}-T{NN}: {short description}
```

To verify all tasks have commits:
```bash
git log --oneline | grep "P0-T"
```
