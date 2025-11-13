---
name: session-context-management
description: Maintain "just enough" context across work sessions using CURRENT.md, STATUS.md, and LESSONS.md files. Activate when tasks take >15 minutes, touch 3+ files, interruptions likely, or scope uncertain. Includes /snapshot and /pickup commands for saving and resuming work. ADHD-friendly, token-efficient approach.
---

# Session Context Management

**Purpose**: Maintain "just enough" context across work sessions for resuming non-trivial development tasks

**Philosophy**: Document to resume work, not to create archives. Tokens aren't free. Err on side of less.

---

## When to Activate

**Activate this skill when ANY of these are true:**

1. **Task duration**: Work will take more than 15 minutes
2. **Multiple files/steps**: Work touches 3+ files OR has 3+ distinct steps
3. **Interruptions likely**: Meeting soon, end of day approaching, or working on unfamiliar code
4. **Scope might expand**: Starting with "just a quick fix" on complex code
5. **User explicitly invokes `/snapshot` or `/pickup` commands**

**Default rule**: If unsure whether to activate → activate (overhead is minimal).

**Do NOT activate for**: Single file edits under 10 minutes, trivial tasks, purely informational requests.

---

## Core Principles & Anti-Patterns

**✅ Do:**
- "Just Enough" > Complete - Document to resume, not archive
- Tokens Aren't Free - Every line costs tokens
- User Can Fill Gaps - They remember context better than docs
- Err on Side of Less - Add detail only when painful without it
- ADHD-Friendly - Interruptions and rabbit holes are normal
- Walk Away Anytime - Never lose context mid-work

**❌ Don't:**
- Complete audit trails - Not an archive
- Explaining obvious things - User knows context
- Upfront planning - Document as you go
- Perfect grammar - Bullets > prose
- Waiting for session end - Update continuously
- Rigid templates - Adapt to needs

---

## Security Rules (BLOCKING)

**CRITICAL: Validate content before writing session files**

Before writing to CURRENT.md, STATUS.md, or LESSONS.md, scan content for sensitive data. If detected, REFUSE to write and warn user.

### Prohibited Patterns (BLOCK & REFUSE):
- API keys: API_KEY=, sk-ant-, sk-proj-, ANTHROPIC_API_KEY=
- Passwords: PASSWORD=, pwd=, passwd=, password:
- Tokens: TOKEN=, Bearer, token:, access_token=
- Private keys: -----BEGIN PRIVATE KEY-----, -----BEGIN RSA
- Credentials: connection strings with passwords, username/password pairs
- PII: SSN, credit cards, personal email addresses in creds
- CUI: classified info, proprietary secrets

### Safe Content (ALLOW):
- Timestamps: 2025-01-13 14:30
- Task descriptions: "Implement login", "Fix auth bug"
- Test results: "3 pass, 1 fail", "Coverage 85%"
- Status: "Blocked on API", "Waiting for review"
- Patterns: "Use uv run python", "Prefer Edit over Write"
- Paths: src/auth/login.py

### Validation Process:
1. Review entire content block before writing
2. Check for prohibited patterns
3. If found: STOP, show detected content, refuse to write
4. If clean: Proceed with write

---

## Low Context Warning Protocol

**Automatic Monitoring**: Check token budget in `<system-reminder>` tags throughout conversation.

**When < 10% Remaining (~<20k tokens):**
1. Capture snapshot immediately using CURRENT.md format
2. Alert user: "⚠️ Context usage at [X%] ([used]/[total] tokens). Recommend `/clear` soon to avoid interruption."
3. Provide resume prompt:
   ```
   Copy this to resume after /clear:

   Resume [feature-name]: [Right Now from CURRENT.md]
   Last done: [Last item from Done list]
   Next: [Next 3 #1]
   [Blockers if any]
   ```

**When < 5% Remaining (~<10k tokens):**
1. Urgent snapshot capture
2. Strong warning: "🚨 Context critical - [remaining] tokens left. `/clear` now recommended to avoid interruption."
3. Provide ready-to-use resume prompt

**Why this approach**: No waiting for context compaction, seamless continuation, user control, preserves work.

---

## File Structure

```
project-root/
└── .session/feature/[feature-name]/
    ├── CURRENT.md    # 🚀 READ FIRST - Quick resume (~100 lines max)
    ├── STATUS.md     # 📋 Terse log - Chronological entries
    └── LESSONS.md    # 💡 Bullet points - What worked/didn't
```

**Why `.session/`**: Add to `.gitignore` - this is working memory, not documentation

**Why `feature/[feature-name]/`**: Separate contexts for different work streams

---

## File Format Templates

### CURRENT.md - Quick Resume
**Purpose**: Resume work in < 2 minutes | **Max Size**: ~100 lines | **Update**: After milestones (~1-2 hours work)

```markdown
# Quick Resume

Last: YYYY-MM-DD HH:MM

## Right Now
[One sentence describing what you're doing RIGHT NOW]

## Last 5 Done
1. ✅ [Most recent completed task]
2. ✅ [Previous completed task]
3. ✅ [Earlier completed task]
4. ✅ [Earlier completed task]
5. ✅ [Earliest completed task]

## In Progress
[If TodoWrite active: Copy active todos here]
[If no TodoWrite: List what's being worked on from context]
- [Active item 1]
- [Active item 2]

## Paused
[Leave empty UNLESS you context-switched to different feature]
[If paused items exist: "- [Feature name] - [Why paused]"]

## Tests
[If tests were run, show results. If not run yet, write "Not run yet"]
**[Framework name]**: X pass / Y fail
- ❌ [failing-test-name] - [why it's failing]

## Blockers
[List specific blockers OR write "None"]

## Next 3
1. [The immediate next action - be specific]
2. [Then do this]
3. [After that]

---
Details → STATUS.md
```

### STATUS.md - Terse Log
**Purpose**: Chronological breadcrumbs | **Size**: No limit, but keep entries SHORT | **Update**: After meaningful steps

```markdown
# Status Log

[Append-only log - oldest to newest]

---

## YYYY-MM-DD HH:MM - [What we did]
✅/❌ [Outcome]
Next: [Action]
[Why/Blocker only if non-obvious]

---

[Keep entries SHORT - this is breadcrumbs, not a diary]
```

**Good example:**
```
## 2025-01-12 14:35 - Login page
✅ Cert & cred auth working
❌ Cookies broken in tests
Next: Fix playwright config
```

### LESSONS.md - Bullet Points
**Purpose**: Extract patterns that worked/didn't | **Update**: After completing features | **Format**: Bullets, not essays

```markdown
# Lessons Learned

[Organized by category, not chronologically]

---

## [Feature/Category]

### Pattern: [Name]
- Context: [Why we needed this]
- Solution: [What worked] → [file:line]
- Gotcha: [What tripped us up]
- Use when: [Future scenarios]

---

[KEEP IT BULLETS - No essays. Only write what you'll reference again.]
```

**Rule**: If you won't reference it again, don't write it.

---

## Workflow

### Session Start (Claude):
1. Read CURRENT.md (< 1 min)
2. Say: "Resuming: [Right Now]. Next: [Next 3 #1]"
3. Mention blockers if any
4. Start work

### During Work (Claude):
1. Work on task
2. Update CURRENT.md after milestones
3. Append to STATUS.md (terse!)
4. User can walk away anytime

### Context Switch (Rabbit Hole):
1. Move current work to "Paused"
2. Update "Right Now" with new focus
3. Work on new thing
4. Resume later from CURRENT.md

### Feature Complete:
1. Mark in CURRENT.md
2. Final STATUS.md entry
3. Extract bullets to LESSONS.md
4. Update "Next 3"
5. **Archive session**: Auto-suggest moving to `.session/completed/[feature-name]`
   - Offer to execute: `mv .session/feature/[name] .session/completed/[name]`
   - Ask for confirmation before archiving

---

## Snapshot Creation (Manual `/snapshot` Command)

**Purpose**: Manual failsafe for capturing state before interruptions, reboots, context switches, or risky work.

**When to Snapshot**: Before system reboots, meetings/interruptions, context switches, risky refactoring, end of work day, or any time user requests `/snapshot`

### High-Level Process:

1. **Verify .gitignore includes `.session/`** (see Activation Instructions)
2. **Validate feature-name** - No `/`, `\`, or special chars. Sanitize if needed, ask user to confirm.
3. **Create directory**: `mkdir -p ".session/feature/<feature-name>"`
4. **Create/Overwrite CURRENT.md** with exact template structure above (populate with current state)
5. **Append to STATUS.md** with timestamp and outcome (create if missing with header)
6. **Create LESSONS.md if missing** (never modify if exists - human-curated only)
7. **Verify all 3 files exist**: `test -f` each file
8. **Show confirmation**: `ls -lh` directory and report sizes

**Fill CURRENT.md with:**
- Timestamp (YYYY-MM-DD HH:MM)
- Right Now: One sentence what you're doing
- Last 5 Done: From conversation/TodoWrite
- In Progress: Copy active todos or current work items
- Paused: Only if context-switched
- Tests: Results if run, else "Not run yet"
- Blockers: Specific blockers or "None"
- Next 3: Immediate next actions

**Append to STATUS.md:**
- Timestamp + brief description
- ✅ What succeeded
- ❌ What failed/incomplete
- Next: What should happen next

### Error Handling:
- **mkdir fails**: Report error, check permissions
- **Feature name invalid**: Sanitize, ask user to confirm
- **.session is file not directory**: Report error, ask user to resolve
- **Verification fails**: Attempt recreate, report which files succeeded/failed
- **Never claim success without verification**

---

## Pickup/Resume (Manual `/pickup` Command)

**Purpose**: Resume work from a saved session.

### High-Level Process:

1. **Verify .gitignore** (same as snapshot)
2. **Read CURRENT.md** - Extract: "Right Now", "Last 5 Done" #1, "Blockers", "Next 3" #1
   - If missing: List available sessions, ask which to resume, STOP
3. **Read STATUS.md** - Show last 2-3 entries (timestamp + outcome)
   - If missing: Skip (no error)
4. **Check LESSONS.md** - If STATUS entries ≥5 and LESSONS empty/missing, remind user to document patterns
5. **Display resume format:**
   ```
   Resuming [feature-name]: [Right Now]

   Last done: [Item #1 from Last 5 Done]

   [If STATUS.md exists:]
   Recent work:
   - [Timestamp] [Outcome summary]
   - [Timestamp] [Outcome summary]

   Next: [Item #1 from Next 3]

   [If blockers:]
   ⚠️ Blockers: [Blockers]

   [If LESSONS reminder needed:]
   💡 Consider documenting patterns in LESSONS.md
   ```
6. **Begin work immediately** - Execute "Next 3 #1" action, don't ask what to do

### Error Handling:
- **Session directory doesn't exist**: List available, ask which to resume
- **CURRENT.md missing**: Report error, offer to create new or pick different session
- **CURRENT.md malformed**: Read what's available, warn about missing sections

---

## Activation Instructions

When task meets criteria OR `/snapshot`/`/pickup` invoked:

1. **Verify .gitignore** (MUST do before creating session files):
   - Check if `.gitignore` exists: `test -f .gitignore`
   - If exists: Read and check for `.session/` line. Add if missing under "Session-specific directories" section.
   - If missing: Create with minimum content:
     ```
     # Session-specific directories
     .session/
     ```
   - **Why**: Prevents accidental commits of session working memory

2. **Create structure**: `.session/feature/[feature-name]/`

3. **Initialize files**: CURRENT.md, STATUS.md, LESSONS.md (see templates above)

4. **Tell user**: "Session context tracking active for [feature-name]"

5. **Update frequently**: After milestones, stay terse, monitor token budget

---

## Self-Evaluation

**Every 5-10 features**, review and ask:

1. **Did we document TOO MUCH?** - Walls of text nobody reads? Sections never referenced?
2. **Did we document TOO LITTLE?** - Couldn't resume work? Lost important "why"?
3. **Token efficiency?** - Documentation vs actual work ratio. Can we be more terse?
4. **What sections matter?** - Which parts actually used?

**Goal**: Continuous improvement toward "just enough"

---

## Success Criteria

✅ Resume work in < 2 minutes from cold start
✅ CURRENT.md stays under ~100 lines
✅ STATUS.md entries are terse (< 50 words)
✅ Can walk away anytime without loss
✅ Find "why" in < 3 minutes when needed
✅ Token usage is efficient
✅ Self-evaluation shows we err on "less"

---

## Integration with Other Skills

Works alongside:
- `testing-workflow` - Test results in CURRENT.md
- `git-workflow` - Commit SHAs in STATUS.md if relevant
- `python-workflow` / `web-projects` - Same context system

This skill provides working memory. Other skills provide domain knowledge.
