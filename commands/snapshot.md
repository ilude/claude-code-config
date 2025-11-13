---
description: Manually capture session state snapshot
argument-hint: [feature-name]
---

Capture a snapshot of the current session state.

## Context Inference (Feature Name)

**Priority order:**

1. **Explicit argument**: If `$ARGUMENTS` provided → use that (highest priority)
2. **Infer from context**: Check conversation for:
   - Recent `.session/feature/[name]/` file reads/writes
   - Active todo list mentioning feature names
   - Recent discussion about specific feature work
3. **If clear from context** → use inferred name automatically
4. **If ambiguous or unclear** → List available sessions and prompt user: "Which feature should I snapshot?"

**CRITICAL**: If unable to infer feature-name, MUST prompt user explicitly. Never guess or skip this step.

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
