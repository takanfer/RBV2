# Session Handoff Protocol

Defines how context is preserved between agent sessions so a new session can pick up exactly where the previous one left off, without re-discovering the project state from scratch.

---

## Problem

Each Cursor agent session starts with a blank context. Without a structured handoff, the new session must:
- Re-read all specification files to understand the project
- Figure out which tasks are done and which are next
- Discover any in-progress or blocked work
- Understand any decisions made in prior sessions

This wastes significant context window and time. The Session Handoff Protocol eliminates this by creating a structured summary that the next session reads first.

---

## Session Summary Location

After each session, write or update:

```
planning/session-handoff.md
```

This file is the FIRST thing a new session should read (after the execution protocol rule).

---

## Session Summary Format

```markdown
# Session Handoff

**Last Updated:** {date and time}
**Last Session By:** {agent model or human}
**Current Phase:** {N} — {Phase Name}

## Where We Are

{2-3 sentences describing current state. What phase are we in? What was the last task completed? What's next?}

## Tasks Completed This Session

| Task | Title | Commit |
|------|-------|--------|
| P{N}-T{NN} | {title} | `{hash}` |

## In-Progress Work

{Description of any partially completed work. Include:
- What was started
- What's done so far
- What remains
- Any files that were modified but not committed}

If nothing is in progress: "No in-progress work. Clean state."

## Blocked Tasks

{Any tasks that cannot proceed, with the reason and what's needed to unblock.}

If nothing is blocked: "No blocked tasks."

## Decisions Made

{Any design decisions, specification interpretations, or conflict resolutions made during this session. These are important for consistency across sessions.}

If no decisions: "No new decisions."

## Known Issues

{Any bugs, test failures, specification gaps, or concerns discovered.}

If none: "No known issues."

## Next Steps

1. {First task to pick up}
2. {Second task if applicable}
3. {Any preparatory reading needed}

## Files Modified (Not Yet Committed)

{List of files with uncommitted changes, if any. Ideally this is empty — sessions should end with a clean commit.}

## Validator Status

Last run: {timestamp}
Result: {N}/{N} checks passing, 0 errors
```

---

## Start-of-Session Protocol

When beginning a new session:

1. **Read** `.cursor/rules/execution-protocol.mdc`
2. **Read** `planning/session-handoff.md` (if it exists)
3. **Read** `planning/Implementation_Tasks.md` — verify the handoff matches actual task status
4. **Read** the phase rule for the current phase
5. **Run** `python codegen/validate_docs.py` to confirm documentation is clean
6. **Run** `git status` to check for uncommitted changes
7. If there is in-progress work from the prior session, complete or roll back before starting new tasks

---

## End-of-Session Protocol

Before ending a session:

1. **Commit** all changes (no uncommitted work should remain)
2. **Push** to remote
3. **Run** `python codegen/validate_docs.py` — confirm 0 errors
4. **Run** `pytest` — confirm all tests pass
5. **Update** `planning/session-handoff.md` with the session summary
6. **Update** `planning/Implementation_Tasks.md` with any task status changes
7. **Commit** the handoff and progress updates

---

## Multi-Agent Coordination

If multiple agents work on different phases or tasks concurrently:

- Each agent writes to its own section of the session handoff
- Task status in `Implementation_Tasks.md` is the single source of truth for "who is doing what"
- Agents must not modify files being actively edited by another agent
- Git merge conflicts in `Implementation_Tasks.md` should be resolved by preserving both agents' status updates

---

## Authoritative Sources

- `.cursor/rules/execution-protocol.mdc` — Task lifecycle rules
- `planning/Implementation_Tasks.md` — Task definitions and status
- `planning/Progress_Tracking_Format.md` — Status marker format
