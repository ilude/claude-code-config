---
description: Analyze and optimize CLAUDE.md ruleset files with project-aware meta-learning from chat history
---

# Optimize Ruleset Command

This command analyzes and optimizes CLAUDE.md ruleset files (project or personal) by:
1. Learning from chat history patterns (meta-learning with PROJECT-AWARE filtering)
2. Detecting issues in current ruleset
3. Providing prioritized recommendations
4. Applying fixes to create optimized version

## Parameters

- **No parameter**: `/optimize-ruleset` → Optimize **project** ruleset at `.claude/CLAUDE.md`
  - Analyzes history FOR THIS PROJECT ONLY
  - Checkpoint: `.claude/CHECKPOINT` (project-specific)

- **"personal"**: `/optimize-ruleset personal` → Optimize **personal** ruleset at `~/.claude/CLAUDE.md`
  - Analyzes history ACROSS ALL PROJECTS
  - Checkpoint: `~/.claude/CHECKPOINT` (global)

- **"--no-history"**: Skip history analysis (just analyze ruleset)
- **"--history-only"**: Only analyze history, suggest rules (don't modify ruleset)

## Checkpoint System

**Multi-line format** supporting multiple checkpoint types:
```
optimize-ruleset: 2025-11-04T14:47:09Z
commit-command: 2025-11-03T10:00:00Z
other-command: 2025-11-02T15:30:00Z
```

**Location**:
- Project checkpoints: `<project>/.claude/CHECKPOINT`
- Personal checkpoint: `~/.claude/CHECKPOINT`

**Why project-specific?**
- Each project tracks its own optimization history
- No re-analysis of unrelated project history
- Patterns detected are specific to project context

## Process Overview

You will execute these phases in order:

### Phase 1: Determine Target & Context
### Phase 2: History Analysis (Meta-Learning with Project Filtering)
### Phase 3: Ruleset Analysis
### Phase 4: Unified Recommendations
### Phase 5: Apply Optimizations (if approved)

---

## PHASE 1: Determine Target & Context

### Step 1.1: Parse Parameters

Check the parameter provided:
- No parameter → **Project mode**: Target `.claude/CLAUDE.md`, Checkpoint `.claude/CHECKPOINT`
- "personal" → **Personal mode**: Target `~/.claude/CLAUDE.md`, Checkpoint `~/.claude/CHECKPOINT`
- Extract any flags: --no-history, --history-only

### Step 1.2: Get Current Working Directory (Project Mode Only)

**If project mode**, get and normalize the current directory:

```bash
# Get current directory
current_dir=$(pwd)
echo "Current directory: $current_dir"

# Output example: /c/Projects/Personal/agent-spike
```

**Path normalization** (for Windows compatibility):
- `C:\Projects\...` → `/c/Projects/...`
- Forward slashes only
- Store as: `current_project_path`

### Step 1.3: Determine Checkpoint Path

Based on mode:
- **Project mode**: `checkpoint_path=".claude/CHECKPOINT"`
- **Personal mode**: `checkpoint_path="~/.claude/CHECKPOINT"`

Create `.claude` directory if needed:
```bash
mkdir -p .claude  # For project mode
```

### Step 1.4: Verify Target Exists

Check if target file exists:
- **Project mode**: `ls .claude/CLAUDE.md`
- **Personal mode**: `ls ~/.claude/CLAUDE.md`

**If doesn't exist**:
- Offer to create from template
- Ask user if they want to create it
- Skip if user declines

### Step 1.5: Gather Project Context (if project ruleset)

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

### Step 1.6: Output Context Summary

Display what you discovered:
```markdown
## Context Analysis

**Mode**: [Project | Personal]
**Target**: [.claude/CLAUDE.md | ~/.claude/CLAUDE.md]
**Checkpoint**: [.claude/CHECKPOINT | ~/.claude/CHECKPOINT]
**Current Directory**: [/c/Projects/Personal/agent-spike] (project mode only)
**Project Type**: [Python learning spike, Node production app, etc.]
**Package Manager**: [uv, npm, cargo, etc.]
**Key Directories**: [.spec/lessons/, src/, tests/, etc.]
**Git Status**: [Clean, X files modified, etc.]
**State Tracking**: [STATUS.md found, None, etc.]
```

---

## PHASE 2: History Analysis (Meta-Learning with Project Filtering)

**Skip this phase if --no-history flag is present**

### Step 2.1: Read CHECKPOINT File

Try to read the checkpoint file:
```bash
cat $checkpoint_path 2>/dev/null
```

Example content:
```
optimize-ruleset: 2025-11-04T14:47:09Z
commit-command: 2025-11-03T10:00:00Z
```

### Step 2.2: Parse optimize-ruleset Checkpoint

Extract the `optimize-ruleset:` line:
```bash
checkpoint_timestamp=$(grep "^optimize-ruleset:" $checkpoint_path 2>/dev/null | cut -d' ' -f2)

# If no checkpoint found:
if [ -z "$checkpoint_timestamp" ]; then
    checkpoint_timestamp="1970-01-01T00:00:00Z"  # Unix epoch (analyze all history)
    echo "No checkpoint found - analyzing all history"
else
    echo "Checkpoint found: $checkpoint_timestamp"
fi
```

Convert to Unix timestamp in milliseconds (history.jsonl uses ms):
```bash
# Convert ISO 8601 to Unix timestamp (seconds)
checkpoint_seconds=$(date -d "$checkpoint_timestamp" +%s 2>/dev/null)

# Convert to milliseconds
checkpoint_ms=$((checkpoint_seconds * 1000))
```

### Step 2.3: Read and Filter History

**history.jsonl structure**:
```json
{
  "display": "user command text",
  "timestamp": 1762266888953,
  "project": "C:\\Projects\\Personal\\agent-spike",
  "sessionId": "uuid"
}
```

**Filtering logic**:

#### For Project Mode:
```bash
# Filter by: timestamp > checkpoint AND project == current_project_path
# Only analyze history entries from THIS project

while IFS= read -r line; do
    # Parse JSON fields (use python or jq if available)
    entry_timestamp=$(echo "$line" | python -c "import sys,json; print(json.load(sys.stdin)['timestamp'])" 2>/dev/null)
    entry_project=$(echo "$line" | python -c "import sys,json; print(json.load(sys.stdin).get('project', ''))" 2>/dev/null)

    # Normalize entry_project path (Windows to Unix format)
    entry_project=$(echo "$entry_project" | sed 's|\\|/|g' | sed 's|^C:|/c|' | sed 's|^D:|/d|')

    # Check conditions
    if [ "$entry_timestamp" -gt "$checkpoint_ms" ] && [ "$entry_project" == "$current_project_path" ]; then
        # Include this entry in analysis
        echo "$line" >> /tmp/filtered_history.jsonl
    fi
done < ~/.claude/history.jsonl
```

#### For Personal Mode:
```bash
# Filter by: timestamp > checkpoint ONLY
# Analyze history from ALL projects

while IFS= read -r line; do
    entry_timestamp=$(echo "$line" | python -c "import sys,json; print(json.load(sys.stdin)['timestamp'])" 2>/dev/null)

    if [ "$entry_timestamp" -gt "$checkpoint_ms" ]; then
        # Include this entry (any project)
        echo "$line" >> /tmp/filtered_history.jsonl
    fi
done < ~/.claude/history.jsonl
```

Count entries:
```bash
entry_count=$(wc -l < /tmp/filtered_history.jsonl 2>/dev/null || echo "0")
echo "Entries to analyze: $entry_count"
```

**Report**:
- Project mode: "Analyzing X entries from this project since [checkpoint]"
- Personal mode: "Analyzing X entries from all projects since [checkpoint]"
- First run: "Analyzing all history (no checkpoint found)"

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
- **Project Context**: [This project | All projects]
- **Example**: [Quote from history]
- **Issue**: [What went wrong]
- **Suggested Rule**: [Specific guidance]
- **Priority**: [HIGH/MEDIUM/LOW]
- **Add to**: [Personal ruleset | Project ruleset | Both]
- **Section**: [Where in ruleset to add it]
```

### Step 2.6: Update CHECKPOINT

After analysis, update the checkpoint file with the current timestamp.

**Read existing checkpoint**:
```bash
current_content=$(cat $checkpoint_path 2>/dev/null)
```

**Update optimize-ruleset line**:
```bash
# Generate new timestamp
new_timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# Remove old optimize-ruleset line (if exists)
other_lines=$(echo "$current_content" | grep -v "^optimize-ruleset:" 2>/dev/null)

# Create new content
{
    echo "$other_lines"
    echo "optimize-ruleset: $new_timestamp"
} > $checkpoint_path

# Ensure proper formatting (remove empty lines at start)
sed -i '/^$/d' $checkpoint_path 2>/dev/null || true
```

**Verify**:
```bash
echo "Updated checkpoint:"
cat $checkpoint_path
```

**Result**:
- Project mode: `.claude/CHECKPOINT` updated for this project only
- Personal mode: `~/.claude/CHECKPOINT` updated globally

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
- History-derived rules (from Phase 2, filtered by project)
- Ruleset issues (from Phase 3)

Look for overlap:
- Did history reveal same issue ruleset has?
- Example: History shows .venv confusion + Ruleset documents .venv wrong = CRITICAL priority

### Step 4.2: Final Prioritization

Re-prioritize based on:
- Frequency (issue appeared multiple times)
- Severity (blocks work, causes errors)
- Impact (affects many sessions)
- Context (project-specific patterns more relevant for project ruleset)

**Priority Levels**:
- **CRITICAL**: Issue appeared in history AND ruleset, causes actual problems
- **HIGH**: Technical inaccuracies, missing critical info, history patterns with 3+ occurrences in this project
- **MEDIUM**: Structural issues, missing onboarding, history patterns with 2 occurrences
- **LOW**: Polish, formatting, history patterns with 1 occurrence

### Step 4.3: Present Comprehensive Report

Output in this format:

```markdown
# Ruleset Optimization Analysis

**Mode**: [Project | Personal]
**Target**: [Path to CLAUDE.md]
**Checkpoint**: [Path to CHECKPOINT]
**Current Directory**: [PWD] (project mode only)

---

## Part 1: Meta-Learning from History

**History Scope**:
- **Project mode**: Only entries from this project
- **Personal mode**: Entries from all projects

**History Analyzed**: [X entries since checkpoint | Y total entries (first run)]
**Checkpoint**: [Previous: YYYY-MM-DD | None (first run)]
**Updated Checkpoint**: [Current timestamp]
**Projects Included**: [Current project only | All projects]

### Patterns Detected

#### Pattern: [Name] (Priority: HIGH/MEDIUM/LOW)
- **Frequency**: [X occurrences across Y sessions]
- **Project Context**: [This project | All projects]
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

**Checkpoint Status**:
- Location: [.claude/CHECKPOINT | ~/.claude/CHECKPOINT]
- Previous: [timestamp | None]
- Updated: [new timestamp]
- Next run will analyze only NEW history since this timestamp

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

## Path Normalization

**Windows Path Handling**:
```bash
# Convert Windows paths to Unix format for comparison
normalize_path() {
    local path="$1"
    # Convert backslashes to forward slashes
    path=$(echo "$path" | sed 's|\\|/|g')
    # Convert drive letters: C: → /c
    path=$(echo "$path" | sed 's|^C:|/c|I' | sed 's|^D:|/d|I')
    echo "$path"
}

# Usage:
entry_project=$(normalize_path "$entry_project")
current_project=$(normalize_path "$current_project")

# Now compare
if [ "$entry_project" == "$current_project" ]; then
    # Match!
fi
```

---

## Edge Cases

### Case 1: Project has no .claude directory
- Command creates it: `mkdir -p .claude`
- Creates CHECKPOINT in new directory
- Creates CLAUDE.md from template

### Case 2: history.jsonl has no project field
- Older entries might not have this field
- Treat as "unknown project"
- For project mode: Skip these entries
- For personal mode: Include these entries

### Case 3: Path normalization issues
- Windows: `C:\Projects\...` vs `/c/Projects/...`
- Solution: Normalize all paths before comparison
- Case insensitive on Windows

### Case 4: Moving project directory
- Checkpoint is project-relative: `.claude/CHECKPOINT`
- Moves with project
- History entries have old path
- No matches until new work generates new history with new path
- **Solution**: Old history not analyzed, only new history with new path

### Case 5: Multiple checkpoint types
- optimize-ruleset has its checkpoint
- commit-command (future) has its checkpoint
- Both coexist in same CHECKPOINT file
- Each command reads/updates only its line

### Case 6: CHECKPOINT in wrong location (migration)
- If `~/.claude/CHECKPOINT` exists but should be project-specific
- Warn user: "Found global checkpoint, expected project checkpoint"
- Suggest: "Delete ~/.claude/CHECKPOINT if it was created by mistake"

### Case 7: Very old checkpoint (>30 days)
- Might have thousands of entries
- Limit to most recent 1000 entries
- Note: "Checkpoint very old, analyzing recent 1000 entries"

### Case 8: No history entries for project
- Project mode: "No history found for this project"
- Skip history analysis
- Continue with ruleset analysis

---

## Success Criteria

This command succeeds if:

1. ✅ Correctly determines target (project vs personal)
2. ✅ Uses project-specific checkpoint for project mode
3. ✅ Filters history by project path in project mode
4. ✅ Filters history globally in personal mode
5. ✅ Parses multi-line checkpoint format
6. ✅ Updates checkpoint preserving other entries
7. ✅ Identifies real patterns (not false positives)
8. ✅ Generates specific, actionable rules from history
9. ✅ Detects ruleset issues accurately
10. ✅ Provides unified recommendations with clear priorities
11. ✅ Explains rationale (educational, not just "do this")
12. ✅ Produces an optimized ruleset that's clearer and more accurate
13. ✅ Works incrementally (learns from each session)
14. ✅ Handles edge cases gracefully
15. ✅ Creates self-improving system per-project

---

## Notes for Claude

- **Be thorough but not overwhelming** - Prioritize well
- **Explain WHY** - Help user understand the value of changes
- **Be specific** - "Add Quick Start section" is better than "Improve structure"
- **Use examples** - Show before/after, quote from history
- **Respect existing good content** - Don't change what works
- **Focus on patterns** - 1 occurrence may be random, 3+ is a pattern in this project
- **Update CHECKPOINT** - Always write new timestamp after history analysis
- **Preserve other checkpoints** - Don't overwrite commit-command or other entries
- **Project context matters** - Patterns from THIS project are more relevant than global patterns
- **Ask before major changes** - Draft first if unsure

Remember: This is meta-learning with PROJECT AWARENESS. Each project improves independently based on its own history!
