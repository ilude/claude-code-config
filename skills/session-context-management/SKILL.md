# Session Context Management

**Purpose**: Maintain "just enough" context across work sessions for resuming non-trivial development tasks

**Philosophy**: Document to resume work, not to create archives. Tokens aren't free. Err on side of less.

---

## When to Activate

Activate this skill when:
- Task estimated > 15 minutes
- Work involves multiple files/steps
- User might context-switch (meetings, interruptions, rabbit holes)
- Implementation scope could expand during work
- Future-you needs to remember "what/why"

**Default**: If in doubt, activate - overhead is minimal when done right.

---

## Core Principles

✅ **"Just Enough" > Complete** - Document to resume, not archive
✅ **Tokens Aren't Free** - Every line costs tokens to write/read
✅ **User Can Fill Gaps** - They remember context better than docs
✅ **Err on Side of Less** - Add detail only when painful without it
✅ **ADHD-Friendly** - Interruptions and rabbit holes are normal
✅ **Walk Away Anytime** - Never lose context mid-work

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

## CURRENT.md - Quick Resume

**Purpose**: Resume work in < 2 minutes
**Max Size**: ~100 lines (enforce brevity)
**Update**: After milestones (~1-2 hours work)

**Sections**:
```markdown
# Quick Resume
Last: [timestamp]

## Right Now
[One sentence]

## Last 5 Done
1-5. [Terse bullets]

## In Progress
- [Active items]

## Paused (if any)
- [Context switches]

## Tests
Pass/Fail + which failing

## Blockers
[Or "None"]

## Next 3
1-3. [Immediate actions]
```

**Rule**: If you can't resume from CURRENT.md alone, add detail. Otherwise, don't.

---

## STATUS.md - Terse Log

**Purpose**: Chronological breadcrumbs
**Size**: No limit, but keep entries SHORT
**Update**: After meaningful steps

**Format**:
```markdown
## [Date Time] - [What]
✅/❌ [Outcome]
Next: [Action]
[Only add Why/Blocker if non-obvious]
```

**Bad (too verbose)**:
```
## 2025-01-12 14:35 - Login Page Implementation
**What**: Created login page with certificate and credential auth
**Why**: Phase 2 requirement, foundation for all protected routes
...150 more tokens...
```

**Good (just enough)**:
```
## 2025-01-12 14:35 - Login page
✅ Cert & cred auth working
❌ Cookies broken in tests
Next: Fix playwright config
```

---

## LESSONS.md - Bullet Points

**Purpose**: Extract patterns that worked/didn't
**Update**: After completing features
**Format**: Bullets, not essays

```markdown
## [Feature/Category]

### Pattern: [Name]
- Context: [Why we needed this]
- Solution: [What worked] → [file:line]
- Gotcha: [What tripped us up]
- Use when: [Future scenarios]
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
   - Document why feature is complete in final STATUS.md entry

---

## Self-Evaluation

**Every 5-10 features**, review and ask:

1. **Did we document TOO MUCH?**
   - Walls of text nobody reads?
   - Sections never referenced?

2. **Did we document TOO LITTLE?**
   - Couldn't resume work?
   - Lost important "why"?

3. **Token efficiency?**
   - Documentation vs actual work ratio
   - Can we be more terse?

4. **What sections matter?**
   - Which parts of CURRENT.md actually used?
   - Which STATUS.md entries were valuable?

**Goal**: Continuous improvement toward "just enough"

**Command**: `/review-session-context` (future enhancement)

---

## Anti-Patterns

❌ **Complete audit trails** - Not an archive
❌ **Explaining obvious things** - User knows context
❌ **Upfront planning** - Document as you go
❌ **Perfect grammar** - Bullets > prose
❌ **Waiting for session end** - Update continuously
❌ **Rigid templates** - Adapt to needs

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

---

## Low Context Warning Protocol

**Automatic Monitoring**: Check token budget in `<system-reminder>` tags throughout conversation.

### When < 10% Remaining (~<20k tokens):
1. **Capture snapshot immediately** using CURRENT.md format
2. **Alert user**: "⚠️ Context usage at [X%] ([used]/[total] tokens). Recommend `/clear` soon to avoid interruption."
3. **Provide resume prompt**:
   ```
   Copy this to resume after /clear:

   Resume [feature-name]: [Right Now from CURRENT.md]
   Last done: [Last item from Done list]
   Next: [Next 3 #1]
   [Blockers if any]
   ```

### When < 5% Remaining (~<10k tokens):
1. **Urgent snapshot capture**
2. **Strong warning**: "🚨 Context critical - [remaining] tokens left. `/clear` now recommended to avoid interruption."
3. **Provide ready-to-use resume prompt** (same format as above)

**Why this approach:**
- No waiting for context compaction (can take 30+ seconds)
- Seamless continuation with provided resume prompt
- User control over when to clear
- Preserves work even if we hit limit unexpectedly

---

## Activation Instructions

When task meets criteria, Claude should:

1. **Create structure**: `.session/feature/[feature-name]/`
2. **Initialize files**: CURRENT.md, STATUS.md, LESSONS.md
3. **Tell user**: "Session context tracking active for [feature-name]"
4. **Update frequently**: After milestones, not sessions
5. **Stay terse**: "Just enough" principle always
6. **Monitor context**: Check token budget warnings and proactively warn user when low

---

## Templates

See `templates/` directory for:
- `CURRENT.md.template` - Quick resume format
- `STATUS.md.template` - Terse log format
- `LESSONS.md.template` - Bullet point format
