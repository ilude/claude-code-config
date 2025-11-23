---
description: Brain dump mode - capture ideas quickly, make them actionable
argument-hint: [optional-slug]
---

# Brain Dump Mode

**Context**: User likely woke up with an idea they need to get out of their head. Priority is:
1. Capture the idea quickly
2. Make it actionable if possible
3. Get user back to what they were doing (sleeping, etc.)

## Workflow

### 1. Acknowledge Context
- Check time with `date` to understand urgency
- Be concise - user's brain is racing, don't add friction

### 2. Capture the Idea
Ask ONE question at a time to extract:
- **What** is the core idea? (let them dump it all out)
- **Why** does it matter? (what problem does it solve)
- **Scope** - what's the minimum viable version?

### 3. Create Idea Folder
```
.claude/ideas/<slug>/
├── YYYY-MM-DD-idea.md    # Main idea document
├── research/              # Any web research, references
├── decisions/             # Key decisions made
└── [other files as needed]
```

**Slug naming:**
- Start with date if no clear name: `2025-11-22/`
- Refine as idea clarifies: `2025-11-22/` → `voice-memo-ingest/`
- Ask user before renaming

### 4. Determine Path Forward

**If actionable:**
- Create concrete implementation plan
- Get user approval
- Execute with FREQUENT git commits (every meaningful change)
- Push often so progress is saved
- Continue capturing context in idea folder while working

**If needs more thought:**
- Save everything to idea folder
- Add to `.claude/STATUS.md` or `SUGGESTED_NEXT.md` for future reference
- Commit and push what we have

### 5. Git Discipline
- Commit after creating idea folder
- Commit after each phase of planning
- Commit after each implementation step
- Push after every 2-3 commits minimum
- User should be able to resume from any point

## Idea Document Template

```markdown
# [Idea Title]

**Date**: YYYY-MM-DD HH:MM
**Status**: [brainstorm|planning|in-progress|parked|completed]

## The Idea
[Raw brain dump - capture everything user says]

## Why It Matters
[Problem it solves, motivation]

## Minimum Viable Version
[Smallest useful implementation]

## Implementation Plan
[If actionable - concrete steps]

## Open Questions
[Things to figure out]

## Research & References
[Links, notes from web searches]

## Decision Log
| Date | Decision | Rationale |
|------|----------|-----------|
```

---

**Start now**: Ask the user "What's the idea?" and let them dump it all out.
