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

1. **Activate session-context-management skill** (if not already active)

2. **Check/Create Feature Overview** (first snapshot only or when scope changed):

   **On first snapshot** (CURRENT.md doesn't exist):
   - Analyze conversation context for feature overview information
   - Extract: Goal, requirements, user stories, design decisions
   - If insufficient context in conversation, prompt user **ONE question at a time**:
     1. "What is the goal of this feature?"
     2. "Any critical requirements or constraints?"
     3. "Key user scenarios driving this feature?"
     4. "Any architectural or design decisions already made?"
   - Create Feature Overview section at top of CURRENT.md

   **On subsequent snapshots** (CURRENT.md exists with Feature Overview):
   - Read existing Feature Overview section
   - Check if feature scope/understanding has changed in conversation
   - If changed: Update relevant parts of Feature Overview (goals, requirements, decisions)
   - If unchanged: Preserve as-is (Feature Overview is slower-changing than task state)

3. **Follow skill instructions**: See "Multi-Instance Support" section in skill for complete implementation:
   - Create/verify directory: `.session/feature/[feature-name]/`
   - **CURRENT.md**:
     - Ensure Feature Overview section exists at top (shared across all instances)
     - Update or create instance section with `## [$TAG] Title` header below overview
     - If section exists: Update it
     - If new: Append section with separator `---`
     - Preserve other instance sections
   - **STATUS.md**:
     - Extract user request from recent conversation (summarize intent)
     - Identify key discussion points (decisions, alternatives, trade-offs)
     - Prepend entry with enhanced format:
       ```
       ## [$TAG] timestamp - Description
       **User Request**: [Summarized intent]
       **Discussion**: [Key decisions - omit if routine work]
       **Outcomes**:
       ✅/❌ [Results]
       **Next**: [Action]
       ```
   - **LESSONS.MD**: Create if missing (never modify if exists - human-curated)
   - Verify all files created
   - Report success: `Snapshot saved: [$TAG] in .session/feature/[feature-name]/`

**All multi-instance formatting details are in the session-context-management skill.**

**Feature Overview Philosophy**:
- **50,000-foot view**: High-level context, not implementation details
- **Slower-changing**: Only update when feature scope/understanding evolves
- **Conversation-first**: Infer from context before prompting user
- **One question at a time**: Never bundle multiple questions
- **Backward compatible**: Sessions without overview still work
