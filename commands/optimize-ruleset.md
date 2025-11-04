---
description: Analyze and optimize CLAUDE.md ruleset files with meta-learning from chat history
---

# Optimize Ruleset Command

This command analyzes and optimizes CLAUDE.md ruleset files (project or personal) by:
1. Learning from chat history patterns (meta-learning)
2. Detecting issues in current ruleset
3. Providing prioritized recommendations
4. Applying fixes to create optimized version

## Parameters

- **No parameter**: `/optimize-ruleset` → Optimize **project** ruleset at `.claude/CLAUDE.md`
- **"personal"**: `/optimize-ruleset personal` → Optimize **personal** ruleset at `~/.claude/CLAUDE.md`
- **"--no-history"**: Skip history analysis (just analyze ruleset)
- **"--history-only"**: Only analyze history, suggest rules (don't modify ruleset)

## Process Overview

You will execute these phases in order:

### Phase 1: Determine Target & Context
### Phase 2: History Analysis (Meta-Learning)
### Phase 3: Ruleset Analysis
### Phase 4: Unified Recommendations
### Phase 5: Apply Optimizations (if approved)

---

## PHASE 1: Determine Target & Context

### Step 1.1: Parse Parameters

Check the parameter provided:
- No parameter → Target: `.claude/CLAUDE.md` (project ruleset)
- "personal" → Target: `~/.claude/CLAUDE.md` (personal ruleset)
- Extract any flags: --no-history, --history-only

### Step 1.2: Verify Target Exists

Check if target file exists:
- **If exists**: Proceed to analysis
- **If doesn't exist**:
  - For project: Offer to create from template
  - For personal: Offer to create default personal ruleset
  - Ask user if they want to create it

### Step 1.3: Gather Project Context (if project ruleset)

If optimizing project ruleset, gather context by checking:

**Project structure**:
```bash
ls -la
find . -maxdepth 2 -type d | head -20
```

**Package managers**:
- Python: `ls pyproject.toml setup.py requirements.txt 2>/dev/null`
- Node: `ls package.json 2>/dev/null`
- Rust: `ls Cargo.toml 2>/dev/null`
- Go: `ls go.mod 2>/dev/null`

**Special directories**:
- Learning/experimental: `.spec/`, `lessons/`, `examples/`
- Source code: `src/`, `lib/`, `app/`
- Tests: `tests/`, `test/`, `__tests__/`
- Documentation: `docs/`, `documentation/`

**State tracking**:
- `ls STATUS.md TODO.md CHANGELOG.md README.md 2>/dev/null`

**Git status**:
```bash
git status --short 2>/dev/null || echo "Not a git repo"
git log --oneline -5 2>/dev/null
```

**Identify project type**:
- Python (learning/spike, production, library, etc.)
- Node/TypeScript
- Rust
- Go
- Multi-language
- State: Learning spike, Active development, Production, Archived

### Step 1.4: Output Context Summary

Display what you discovered:
```markdown
## Context Analysis

**Target**: [.claude/CLAUDE.md | ~/.claude/CLAUDE.md]
**Project Type**: [Python learning spike, Node production app, etc.]
**Package Manager**: [uv, npm, cargo, etc.]
**Key Directories**: [.spec/lessons/, src/, tests/, etc.]
**Git Status**: [Clean, X files modified, etc.]
**State Tracking**: [STATUS.md found, None, etc.]
```

---

## PHASE 2: History Analysis (Meta-Learning)

**Skip this phase if --no-history flag is present**

### Step 2.1: Read CHECKPOINT File

Try to read `~/.claude/CHECKPOINT`:
```bash
cat ~/.claude/CHECKPOINT 2>/dev/null
```

**If exists**: Parse the timestamp (ISO 8601 format: 2025-11-04T09:16:23Z)
**If doesn't exist**: Set checkpoint_timestamp = 0 (analyze all history)

### Step 2.2: Read History File

Read `~/.claude/history.jsonl`:
```bash
cat ~/.claude/history.jsonl
```

**Format**: JSON Lines (one JSON object per line)
**Fields**:
- `display`: User's command/input
- `timestamp`: Unix timestamp in milliseconds
- `project`: Working directory
- `sessionId`: Session identifier
- `pastedContents`: Any pasted content

### Step 2.3: Filter by Checkpoint

For each line in history.jsonl:
1. Parse JSON
2. Extract timestamp
3. If timestamp > checkpoint_timestamp: Include in analysis
4. If timestamp <= checkpoint_timestamp: Skip (already analyzed)

Count entries: `X entries since checkpoint` or `Y total entries (first run)`

### Step 2.4: Detect Issue Patterns

Analyze the filtered history entries for these patterns:

#### Pattern 1: Repeated Tool Usage Mistakes
Look for:
- Multiple attempts using bash commands when dedicated tools exist
- Example: `grep` in bash instead of Grep tool
- Example: `find` in bash instead of Glob tool
- Example: Manual .venv paths instead of `uv run python`

**Detection**: User input contains bash commands for file operations

**Suggested Rule**: "Use dedicated tools (Grep, Glob, Read) instead of bash commands"

#### Pattern 2: Manual Path References
Look for:
- Patterns like `../../../.venv/`, `../../node_modules/`
- Using explicit paths to virtual environments
- Platform-specific path separators

**Detection**: User input or your responses contain `../.venv` or similar

**Suggested Rule**: "Use package manager run commands (uv run, npm run) instead of manual paths"

#### Pattern 3: User Corrections
Look for:
- User says: "no", "actually", "that's wrong", "incorrect"
- User provides clarification after misunderstanding
- User redirects approach

**Detection**: User input starts with negations or corrections

**Suggested Rule**: Based on what was corrected (document the lesson)

#### Pattern 4: Missing Context Checks
Look for:
- Errors about files not found
- Assumptions that were wrong
- Documentation that didn't match reality

**Detection**: Error messages, user corrections about project state

**Suggested Rule**: "Verify project state before making assumptions"

#### Pattern 5: Forgotten Workflow Steps
Look for:
- User reminds to check STATUS.md
- User reminds to read README
- User asks to commit when work is done

**Detection**: User explicitly reminds about workflow steps

**Suggested Rule**: Add workflow step to appropriate checklist

#### Pattern 6: TODO List Management Issues
Look for:
- TODO lists created but not updated
- Tasks marked complete prematurely
- Multiple tasks in_progress simultaneously

**Detection**: TODO-related commands or corrections

**Suggested Rule**: Refine TODO list best practices

### Step 2.5: Generate Rules from Patterns

For each pattern detected, create a suggested rule:

```markdown
### Pattern: [Name]
- **Detected**: [X times in Y sessions]
- **Example**: [Quote from history]
- **Issue**: [What went wrong]
- **Suggested Rule**: [Specific guidance]
- **Priority**: [HIGH/MEDIUM/LOW]
- **Add to**: [Personal ruleset | Project ruleset | Both]
- **Section**: [Where in ruleset to add it]
```

### Step 2.6: Update CHECKPOINT

After analysis, write current timestamp to `~/.claude/CHECKPOINT`:
```bash
date -u +"%Y-%m-%dT%H:%M:%SZ" > ~/.claude/CHECKPOINT
```

**Format**: ISO 8601 UTC timestamp

---

## PHASE 3: Ruleset Analysis

### Step 3.1: Read Target Ruleset

Read the entire CLAUDE.md file (project or personal).

Count:
- Total lines
- Number of sections (## headers)
- Approximate length per section

### Step 3.2: Detect Ruleset Issues

Check for these common issues:

#### HIGH PRIORITY (Critical)

**Issue H1: Outdated/Inaccurate Project Description**
- Check: Does overview match project structure?
- Example: Says "production app" but has .spec/lessons/
- Example: Mentions technologies not in project
- Example: References non-existent directories

**Issue H2: Technical Inaccuracies**
- Check: Claims about .venv structure (verify with ls)
- Check: Claims about package manager (verify with ls)
- Check: Claimed Python version (check pyproject.toml)
- Check: Command examples (do they work?)

**Issue H3: Missing Critical Context**
- Check: Is project purpose clear in first 50 lines?
- Check: Is project type/state explained?
- Check: Are key directories identified?

**Issue H4: Contradictions**
- Check: Internal contradictions in file
- Check: Contradictions with project reality
- Check: Contradictions with STATUS.md

**Issue H5: References to Non-Existent Files**
- Check: Mentions src/ but doesn't exist
- Check: Mentions files that aren't present
- Check: Commands reference missing scripts

#### MEDIUM PRIORITY (Important)

**Issue M1: Poor Section Ordering**
- Check: Is most important info in top 30%?
- Check: Is rarely-used info (Docker, deployment) too prominent?
- Check: Should lessons/project-specific be first?

**Issue M2: Missing Quick Start**
- Check: Is there onboarding for new Claude sessions?
- Check: Are immediate actions listed?

**Issue M3: Unclear Doc Relationships**
- Check: Is relationship with STATUS.md explained?
- Check: Is relationship with README explained?
- Check: Is redundancy with other docs addressed?

**Issue M4: Unexplained Dual Structures**
- Check: pyproject.toml has both [project.optional-dependencies] and [dependency-groups]?
- Check: Are differences explained?
- Check: Is it clear which to use?

**Issue M5: Irrelevant Detail Overload**
- Check: Too much about containers when not used?
- Check: Too much about deployment for learning project?
- Check: Config details that rarely change?

#### LOW PRIORITY (Polish)

**Issue L1: Verbose Explanations**
- Check: Could sections be more concise?
- Check: Repetitive content?

**Issue L2: Missing Examples**
- Check: Complex commands lack examples?
- Check: Would code samples help?

**Issue L3: Inconsistent Formatting**
- Check: Heading styles consistent?
- Check: Code block formatting consistent?

**Issue L4: No Summary Section**
- Check: Is there a TL;DR for new sessions?
- Check: Is there a checklist?

**Issue L5: Missing Directory Structure**
- Check: Would a tree visualization help?

### Step 3.3: Prioritize Ruleset Issues

Group detected issues by priority (HIGH/MEDIUM/LOW).

For each issue:
- Describe the problem
- Explain why it matters (impact)
- Provide specific fix recommendation
- Show before/after if helpful
- Note line numbers if applicable

---

## PHASE 4: Unified Recommendations

### Step 4.1: Combine History + Ruleset Analysis

Merge findings:
- History-derived rules (from Phase 2)
- Ruleset issues (from Phase 3)

Look for overlap:
- Did history reveal same issue ruleset has?
- Example: History shows .venv confusion + Ruleset documents .venv wrong = HIGH priority

### Step 4.2: Final Prioritization

Re-prioritize based on:
- Frequency (issue appeared multiple times)
- Severity (blocks work, causes errors)
- Impact (affects many sessions)

**Priority Levels**:
- **CRITICAL**: Issue appeared in history AND ruleset, causes actual problems
- **HIGH**: Technical inaccuracies, missing critical info, history patterns with 3+ occurrences
- **MEDIUM**: Structural issues, missing onboarding, history patterns with 2 occurrences
- **LOW**: Polish, formatting, history patterns with 1 occurrence

### Step 4.3: Present Comprehensive Report

Output in this format:

```markdown
# Ruleset Optimization Analysis

**Target**: [Path to CLAUDE.md]
**Project Type**: [Detected type]
**Current State**: [X lines, Y sections]

---

## Part 1: Meta-Learning from History

**History Analyzed**: [X entries since checkpoint | Y total entries (first run)]
**Checkpoint**: [Previous: YYYY-MM-DD | None (first run)]
**Updated Checkpoint**: [Current timestamp]

### Patterns Detected

#### Pattern: [Name] (Priority: HIGH/MEDIUM/LOW)
- **Frequency**: [X occurrences across Y sessions]
- **Example from History**:
  ```
  [Quote or description]
  ```
- **Issue**: [What went wrong]
- **Lesson Learned**: [Key insight]
- **Suggested Rule**: [Specific guidance to add]
- **Add to**: [Personal/Project ruleset, which section]

[Repeat for each pattern]

### Recommended New Rules from History

1. **[Rule Title]** (from Pattern X)
   - **Add to**: [Ruleset location]
   - **Section**: [Which section]
   - **Text**:
     ```markdown
     [Exact text to add]
     ```

---

## Part 2: Current Ruleset Analysis

**Issues Detected**: [X critical, Y high, Z medium, W low]

### CRITICAL Issues (History + Ruleset)
[Issues that appeared in both]

### HIGH Priority Issues
[Issues from H1-H5]

### MEDIUM Priority Issues
[Issues from M1-M5]

### LOW Priority Issues
[Issues from L1-L5]

---

## Part 3: Unified Recommendations

**Total Recommendations**: [X critical, Y high, Z medium, W low]

### Proposed Changes

1. **[Change Description]** (Priority: CRITICAL/HIGH/MEDIUM/LOW)
   - **Current**: [What it is now]
   - **Problem**: [Why it's an issue]
   - **Fix**: [What to change]
   - **Source**: [History pattern + Ruleset issue | Ruleset only | History only]
   - **Impact**: [What improves]

[Repeat for each recommendation]

---

## Part 4: Optimization Summary

**Estimated Result**:
- Current: [X lines, Y sections]
- Optimized: [~A lines, B sections]
- Changes: [Structural reorganization, N new rules added, M sections rewritten]

**Structure Improvements**:
- Move [section X] before [section Y] (priority ordering)
- Add Quick Start section
- Condense [section Z]
- Add rules from history to [section W]

---

## What would you like me to do?

1. **Apply HIGH + CRITICAL only** - Fix most important issues
2. **Apply HIGH + MEDIUM + CRITICAL** - Comprehensive optimization (recommended)
3. **Apply ALL recommendations** - Complete optimization including polish
4. **Show me a draft first** - Write optimized version, let me review before applying
5. **Analysis only** - Don't change anything, just show me the report
6. **Add history rules only** - Just add the new rules from history analysis

Please respond with your choice (1-6) or ask questions about specific recommendations.
```

---

## PHASE 5: Apply Optimizations (if approved)

Based on user choice:

### Option 1-3: Apply Fixes

1. **Create backup**: Copy current CLAUDE.md to CLAUDE.md.backup
2. **Apply changes based on priority level chosen**
3. **Verify structure**: Ensure valid markdown
4. **Show diff summary**: List what changed
5. **Success message**

### Option 4: Show Draft

1. **Generate complete optimized version**
2. **Display in code block**
3. **Ask for approval**
4. **If approved**: Write to file
5. **If not**: Offer to revise

### Option 5: Analysis Only

- Report already shown
- No changes made
- Suggest user review and decide

### Option 6: Add Rules Only

1. **Read current ruleset**
2. **Find appropriate sections**
3. **Insert new rules from history**
4. **Preserve existing content**
5. **Show what was added**

---

## Recommended Ruleset Structure (Target State)

After optimization, CLAUDE.md should generally follow:

```markdown
# CLAUDE.md

**Terminology** (if relevant - personal vs project rulesets)

## Project Overview / Purpose
- What this project is
- Current state (learning, production, archived)
- Key technologies
- Directory structure

## Quick Start
- First time here?
- Resuming work?
- Working on [main thing]?

## [Core Project-Specific Sections] (70% of file)
- Most frequently needed information
- Development workflow
- Key commands by usage frequency
- Patterns and practices
- Rules learned from history

## Common Development Commands
- Most common (daily use)
- Less common (weekly use)
- Rarely needed (documented but de-emphasized)

## Configuration Details
- Language version, tools
- Only if relevant, not verbose

## Background / Infrastructure
- Rarely needed information
- Clearly marked as "Background"

## Summary for New Claude Sessions
- Checklist format
- Quick reference
```

---

## Example: Pattern Detection Logic

When analyzing history, use these heuristics:

### Detecting Manual .venv Paths

```javascript
// Pseudocode
if (entry.display.includes('.venv/Scripts/python') ||
    entry.display.includes('.venv/bin/python') ||
    entry.display.includes('../.venv/')) {

    pattern = "Manual virtual environment paths"
    issue = "Using explicit venv paths instead of tool commands"
    rule = "Always use `uv run python` / `poetry run` / etc."
    priority = HIGH if (occurrences >= 3) else MEDIUM
}
```

### Detecting User Corrections

```javascript
// Pseudocode
correction_keywords = ["no", "actually", "incorrect", "wrong", "that's not"]

if (entry.display.toLowerCase().startsWith(correction_keywords)) {
    pattern = "User correction - something was misunderstood"
    // Look at previous entry to see what was corrected
    lesson = analyze_what_was_corrected(entry, previous_entry)
    rule = "Verify [specific thing] before assuming"
    priority = depends on severity
}
```

### Detecting Forgotten Workflow Steps

```javascript
// Pseudocode
reminder_keywords = ["remember to", "don't forget", "make sure to", "you should"]

if (entry.display.includes(reminder_keywords)) {
    pattern = "User had to remind about workflow step"
    step = extract_workflow_step(entry.display)
    rule = "Add to workflow checklist: " + step
    priority = MEDIUM
}
```

---

## Edge Cases

### Case 1: CHECKPOINT very old (>30 days)
- Limit to most recent 1000 entries
- Note: "Analyzing recent 1000 entries (checkpoint very old)"

### Case 2: history.jsonl doesn't exist
- Skip history analysis
- Note: "History file not found, skipping meta-learning"
- Continue with ruleset analysis

### Case 3: history.jsonl format error
- Try to parse what's possible
- Note: "Some history entries could not be parsed"
- Continue with what was successfully parsed

### Case 4: Target ruleset doesn't exist
- Offer to create from template
- Use history analysis to inform initial ruleset
- Ask: "No ruleset found. Would you like me to create one incorporating lessons from your history?"

### Case 5: Target ruleset is excellent
- Congratulate!
- Report: "Ruleset is well-structured. Only minor polish suggestions."
- Still add rules from history if relevant

### Case 6: Command run multiple times quickly
- CHECKPOINT prevents re-analyzing same history
- Only new entries analyzed
- Report: "No new history since last run" if checkpoint is current

---

## Success Criteria

This command succeeds if:

1. ✅ Correctly determines target (project vs personal)
2. ✅ Parses history.jsonl and filters by checkpoint
3. ✅ Identifies real patterns (not false positives)
4. ✅ Generates specific, actionable rules from history
5. ✅ Detects ruleset issues accurately
6. ✅ Provides unified recommendations with clear priorities
7. ✅ Explains rationale (educational, not just "do this")
8. ✅ Updates CHECKPOINT correctly
9. ✅ Produces an optimized ruleset that's clearer and more accurate
10. ✅ Works incrementally (learns from each session)
11. ✅ Handles edge cases gracefully
12. ✅ Creates self-improving system over time

---

## Notes for Claude

- **Be thorough but not overwhelming** - Prioritize well
- **Explain WHY** - Help user understand the value of changes
- **Be specific** - "Add Quick Start section" is better than "Improve structure"
- **Use examples** - Show before/after, quote from history
- **Respect existing good content** - Don't change what works
- **Focus on patterns** - 1 occurrence may be random, 3+ is a pattern
- **Update CHECKPOINT** - Always write new timestamp after history analysis
- **Ask before major changes** - Draft first if unsure

Remember: This is meta-learning. You're teaching the system to improve itself based on real experience!
