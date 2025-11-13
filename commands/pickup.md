---
description: Resume work from a saved session
argument-hint: [feature-name]
---

Resume work on a session.

## Feature Name Selection

1. **If `$ARGUMENTS` provided**: Use that feature-name
2. **If not provided**:
   - List available active sessions from `.session/feature/`
   - Prompt user: "Which session would you like to resume?"
   - Only show **active sessions** (not `.session/completed/`)

**CRITICAL**: Never assume which session to resume. Always confirm with user if not explicitly specified.

---

## Execution

Once feature-name is determined:

1. **Verify .gitignore** includes `.session/` directory
   - If missing: Add it to prevent accidental commits

2. **Activate session-context-management skill** (if not already active)

3. **Follow skill instructions**: See "Pickup/Resume" section in skill for complete implementation:
   - Read CURRENT.md
   - Show last 2-3 STATUS.md entries
   - Check LESSONS.md (remind if empty after 5+ entries)
   - Display resume format to user
   - Begin with "Next 3 #1" action

**All implementation details are in the session-context-management skill.**
