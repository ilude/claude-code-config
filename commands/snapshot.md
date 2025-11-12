---
description: Manually capture session state snapshot
argument-hint: [feature-name]
---

Capture a snapshot of the current session state.

**Context inference priority:**
1. If explicit feature-name provided via $ARGUMENTS → use that (highest priority)
2. If no argument, check conversation context to infer active feature:
   - Recent `.session/feature/[name]/` file reads/writes (CURRENT.md, STATUS.md, LESSONS.md)
   - Active todo list mentioning feature names
   - Recent discussion about specific feature work
3. If active feature is CLEAR from context → snapshot automatically without asking
4. If ambiguous or NO clear feature → list available sessions and ask which to snapshot

Create or update the CURRENT.md file with:
- Timestamp
- Right Now (one sentence current state)
- Last 5 Done (terse bullets)
- In Progress items
- Paused items (if any)
- Test status
- Blockers
- Next 3 actions

This is a manual failsafe for capturing state before:
- System reboots
- Meetings/interruptions
- Context switches
- Risky refactoring
- End of day

Format using the session-context-management skill's CURRENT.md template.
