---
description: Resume work from a saved session
argument-hint: [feature-name]
---

Resume work on a session.

## Session Selection (Multi-Instance Aware)

**Parse all available sessions with instance tags:**

1. **Scan `.session/feature/*/CURRENT.md` files**
2. **Extract all `## [instance:session]` sections** from each CURRENT.md
3. **Parse "Right Now" content** for each instance

**Display format:**
```
Available sessions:
1. feature-name [5d72a497:888cf413] - "Frontend queue multiple questions"
2. feature-name [a08428d4:3e5380bd] - "Transcripts timestamps support"
3. other-feature [5d72a497:abc12345] - "API endpoints"
```

**Selection:**
- **If `$ARGUMENTS` provided**: Use that feature-name, show all instances for that feature
- **If not provided**: Show all instances for all features
- User selects by number
- Resume from selected `[instance:session]` section

**CRITICAL**: Show ALL instances to allow resuming work from any Claude instance, not just current one.

---

## Execution

Once feature-name and instance:session are determined:

1. **Verify .gitignore** includes `.session/` directory
   - If missing: Add it to prevent accidental commits

2. **Activate session-context-management skill** (if not already active)

3. **Follow skill instructions**: See "Multi-Instance Support" section in skill for complete implementation:
   - Read CURRENT.md **specific `## [instance:session]` section**
   - Show last 2-3 STATUS.md entries **for that instance:session tag**
   - Check LESSONS.md (shared, no filtering needed)
   - Display resume format:
     ```
     Resuming [feature-name] from [instance:session]: [Right Now content]
     Last done: [Last item from Done list]
     Next: [Next 3 #1]
     ```
   - Begin with "Next 3 #1" action from that instance's context

**All multi-instance parsing details are in the session-context-management skill.**
