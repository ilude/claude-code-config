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

## Instance Detection

**Detect current instance and session IDs for multi-instance support:**

```bash
# Instance ID (which IDE window)
INSTANCE_ID=$(cat ~/.claude/ide/$CLAUDE_CODE_SSE_PORT.lock 2>/dev/null | python -c "import json, sys; print(json.load(sys.stdin)['authToken'][:8])" 2>/dev/null || echo "unknown")

# Session ID (which conversation)
SESSION_ID=$(ls -lt ~/.claude/debug/*.txt 2>/dev/null | head -1 | awk '{print $9}' | xargs basename 2>/dev/null | cut -d. -f1 | cut -c1-8 || echo "unknown")

# Combined tag
TAG="[$INSTANCE_ID:$SESSION_ID]"
```

**Show detected IDs to user**: `Snapshot for [$INSTANCE_ID:$SESSION_ID]`

---

## Execution

Once feature-name and instance IDs are determined:

1. **Verify .gitignore** includes `.session/` directory
   - If missing: Add it to prevent accidental commits

2. **Activate session-context-management skill** (if not already active)

3. **Follow skill instructions**: See "Multi-Instance Support" section in skill for complete implementation:
   - Create/verify directory: `.session/feature/[feature-name]/`
   - **CURRENT.md**: Update or create section with `## [$TAG] Title` header
     - If section exists: Update it
     - If new: Append section with separator `---`
     - Preserve other instance sections
   - **STATUS.md**: Prepend entry with `## [$TAG] timestamp - Description`
   - **LESSONS.MD**: Update (no tags, shared)
   - Verify all files created
   - Report success: `Snapshot saved: [$TAG] in .session/feature/[feature-name]/`

**All multi-instance formatting details are in the session-context-management skill.**
