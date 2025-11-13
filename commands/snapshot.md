---
description: Manually capture session state snapshot
argument-hint: [feature-name]
---

Capture a snapshot of the current session state.

## Context Inference (Feature Name)

**Priority order:**

1. **Explicit argument**: If `$ARGUMENTS` provided → use that (highest priority)
2. **Check existing sessions**: Find git root, check if `.session/feature/` exists
   - List all existing session directories: `ls .session/feature/`
   - If we're in a subdirectory (e.g., `projects/mentat/`), check if a session exists matching that subdirectory name
   - Example: Working in `projects/mentat/` → check if `.session/feature/mentat/` exists
3. **Infer from recent context**:
   - Recent `.session/feature/[name]/` file reads/writes in conversation
   - Active todo list mentioning feature names
   - Recent discussion about specific feature work
   - Current working directory/project name
4. **If single existing session matches** → use that automatically
5. **If multiple possibilities** → List them and ask: "Which session? [options] or create new?"
6. **If no existing sessions and unclear** → Suggest based on working directory, ask to confirm

**CRITICAL**: Prefer existing sessions over creating new ones. Never guess - always confirm if ambiguous.

---

## Execution

Once feature-name is determined:

1. **Verify .gitignore** includes `.session/` directory
   - If missing: Add it to prevent accidental commits

2. **Activate session-context-management skill** (if not already active)

3. **Follow skill instructions**: See "Snapshot Creation" section in skill for complete implementation:
   - Create/verify directory
   - Create CURRENT.md (capture current state + todos)
   - Append to STATUS.md (log entry)
   - Create/preserve LESSONS.md
   - Verify all files created
   - Report success to user

**All implementation details are in the session-context-management skill.**
