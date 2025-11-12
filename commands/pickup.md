---
description: Resume work from a saved session
argument-hint: [feature-name]
---

Resume work on a session.

If feature-name is provided: $ARGUMENTS
If not provided, list available active sessions from .session/feature/ and ask which to resume.

Read the CURRENT.md file for the specified session and:
1. Summarize "Right Now" status
2. Show last completed item
3. Identify blockers (if any)
4. Start with "Next 3 #1" action

Resume format:
```
Resuming [feature-name]: [Right Now]
Last done: [Last item from Done list]
Next: [Next 3 #1]
[Blockers if any]
```

Only scan **active sessions** from .session/feature/ (not .session/completed/).
