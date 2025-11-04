---
description: Analyze and optimize CLAUDE.md ruleset files with project-aware meta-learning, skills analysis, personal/project deduplication, and context efficiency optimization
---

# Optimize Ruleset Command

This command analyzes and optimizes CLAUDE.md ruleset files (project or personal) by:
1. Learning from chat history patterns (meta-learning with PROJECT-AWARE filtering)
2. Analyzing skills inventory and context efficiency
3. Detecting personal/project duplication to eliminate redundancy (NEW)
4. Detecting issues in current ruleset
5. Recommending skill extractions for context optimization
6. Providing prioritized recommendations with token savings metrics
7. Applying fixes to create optimized version

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
### Phase 2.5: Skills Inventory & Analysis (Context Efficiency)
### Phase 2.8: Personal/Project Deduplication (NEW - Project Mode Only)
### Phase 3: Ruleset Analysis
### Phase 3.5: Skill Extraction Recommendations (Context Efficiency)
### Phase 4: Unified Recommendations (Enhanced with Token Metrics)
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

## PHASE 2.5: Skills Inventory & Analysis (Context Efficiency Focus)

**Purpose**: Analyze existing skills to understand context usage and identify optimization opportunities.

Skills are the PRIMARY context optimization mechanism. They provide:
- Auto-activation based on project context
- Progressive disclosure (loaded only when needed)
- 30-70% context reduction when not active
- Cross-project reusability

### Step 2.5.1: Discover Skills

Scan for skills in both locations:

**Personal Skills** (cross-project):
```bash
if [ -d ~/.claude/skills ]; then
    echo "Personal skills found:"
    find ~/.claude/skills -name "SKILL.md" -type f 2>/dev/null
else
    echo "No personal skills directory"
fi
```

**Local Skills** (project-specific):
```bash
if [ -d .claude/skills ]; then
    echo "Local skills found:"
    find .claude/skills -name "SKILL.md" -type f 2>/dev/null
else
    echo "No local skills directory"
fi
```

Count:
```bash
personal_skill_count=$(find ~/.claude/skills -name "SKILL.md" 2>/dev/null | wc -l)
local_skill_count=$(find .claude/skills -name "SKILL.md" 2>/dev/null | wc -l)
echo "Total: $personal_skill_count personal, $local_skill_count local"
```

### Step 2.5.2: Analyze Each Skill

For each skill file found, extract:

**Parse frontmatter**:
```bash
# Extract name
skill_name=$(grep "^name:" $skill_file | cut -d':' -f2- | xargs)

# Extract description (may be multi-line, ends at ---)
skill_description=$(sed -n '/^description:/,/^---$/p' $skill_file | grep -v "^description:" | grep -v "^---$" | xargs)
```

**Count size**:
```bash
lines=$(wc -l < $skill_file)
words=$(wc -w < $skill_file)
# Estimate tokens: words * 1.3
tokens=$(echo "$words * 1.3" | bc | cut -d'.' -f1)
echo "$skill_name: $lines lines, $words words, ~$tokens tokens"
```

### Step 2.5.3: Determine Skill Activation for Project

For each personal skill, check if it would activate for this project:

**Activation triggers** to check (from description):
- File patterns: `.py`, `pyproject.toml`, `package.json`, `Dockerfile`, etc.
- Directory patterns: `.spec/`, `lessons/`, `src/`, etc.
- Keywords: "Python", "Node", "Docker", "git", "testing", etc.

**Check project match**:
```bash
# Example for python-workflow skill:
# Check if project has Python files
if ls *.py 2>/dev/null || ls pyproject.toml 2>/dev/null; then
    activation="ACTIVE ✅"
else
    activation="INACTIVE"
fi
```

**Activation matrix example**:
```
python-workflow: ACTIVE (pyproject.toml found)
git-workflow: ACTIVE (git repo detected)
multi-agent-ai-projects: ACTIVE (.spec/lessons/ found)
web-projects: INACTIVE (no package.json)
container-projects: INACTIVE (no Dockerfile)
```

### Step 2.5.4: Calculate Context Savings

**Active skills** (loaded for this project):
```bash
active_tokens=0
for skill in $active_skills; do
    tokens=$(get_skill_tokens $skill)
    active_tokens=$((active_tokens + tokens))
done
echo "Active skills: ~$active_tokens tokens"
```

**Inactive skills** (NOT loaded for this project):
```bash
inactive_tokens=0
for skill in $inactive_skills; do
    tokens=$(get_skill_tokens $skill)
    inactive_tokens=$((inactive_tokens + tokens))
done
echo "Saved by not loading: ~$inactive_tokens tokens"
```

**Total if all loaded**:
```bash
total_tokens=$((active_tokens + inactive_tokens))
savings_percent=$(echo "scale=0; $inactive_tokens * 100 / $total_tokens" | bc)
echo "Context savings: ~$savings_percent% ($inactive_tokens of $total_tokens tokens)"
```

### Step 2.5.5: Check for Skill Usage in History

Cross-reference skills with history:
- Count how many times `Skill tool` was invoked
- Which skills were activated?
- Are there skills that should activate but didn't?

**Detection pattern**:
```bash
# Check history for Skill tool usage
grep "Skill tool" /tmp/filtered_history.jsonl 2>/dev/null
# Note: This requires detailed history analysis
```

### Step 2.5.6: Identify Skill Issues

Check for these issues:

**Issue S1: Unused Skills (Never Invoked)**
- Skill exists but never appears in history
- Possible causes: Poor description, unclear activation triggers
- **Recommendation**: Improve description with trigger keywords

**Issue S2: Misplaced Skills**
- Personal skill that's only used in one project → Should be local
- Local skill that could help other projects → Should be personal

**Issue S3: Overlapping with CLAUDE.md**
- Skill content duplicates what's in CLAUDE.md
- **Recommendation**: Remove duplication, reference skill from CLAUDE.md

**Issue S4: Missing Skills**
- Procedural content in CLAUDE.md that should be a skill
- Criteria: >200 words, >10 steps, used in 50% of sessions
- **Recommendation**: Extract to skill (analyzed in Phase 3.5)

### Step 2.5.7: Output Skills Inventory Report

Present findings:

```markdown
## Skills Inventory

**Personal Skills** (~/.claude/skills/):
1. **python-workflow** (88 lines, ~600 tokens)
   - Status: ✅ ACTIVE (pyproject.toml detected)
   - Description: Python project workflow, uv/pip/poetry management
   - Last used: [Check history if available]

2. **git-workflow** (117 lines, ~757 tokens)
   - Status: ⚠️ INACTIVE (not needed this session)
   - Description: Git commit workflow, security scanning
   - Context savings: 757 tokens by not loading

3. **multi-agent-ai-projects** (85 lines, ~521 tokens)
   - Status: ✅ ACTIVE (.spec/lessons/ detected)
   - Description: AI learning projects, STATUS.md workflow
   - Last used: [Check history]

4. **web-projects** (99 lines, ~579 tokens)
   - Status: ⚠️ INACTIVE (no package.json)
   - Context savings: 579 tokens by not loading

5. **container-projects** (133 lines, ~700 tokens)
   - Status: ⚠️ INACTIVE (no Dockerfile)
   - Context savings: 700 tokens by not loading

**Local Skills** (.claude/skills/):
- [None found] or [List if present]

**Context Efficiency Summary**:
- Active skills: 2 (~1,121 tokens loaded)
- Inactive skills: 3 (~2,036 tokens saved)
- Total if all loaded: 5 (~3,157 tokens)
- **Savings: 64% context reduction** ✨

**Issues Detected**:
- ⚠️ [If any skills never invoked, unclear descriptions, etc.]
- ✅ [Skills working well]
```

**Key Insight**: Skills provide selective loading—only load what's needed for this project!

---

## PHASE 2.8: Personal/Project Deduplication Analysis

**Purpose**: Detect and eliminate content in project ruleset that duplicates personal ruleset, reducing redundant context.

**Applies to**: **Project mode only** (when optimizing `.claude/CLAUDE.md`). Personal mode skips this phase.

**Why this matters**:
- Personal ruleset = General policies (loaded always)
- Project ruleset = Project-specific context (loaded always)
- If both have same content = wasted tokens (loaded twice)
- Solution: Keep general in personal, specific in project, reference personal when needed

### Step 2.8.1: Check if Applicable

```bash
# Only run in project mode
if [ "$mode" != "project" ]; then
    echo "## Phase 2.8: Skipped (Personal mode - no deduplication needed)"
    return 0
fi

echo "## Phase 2.8: Personal/Project Deduplication Analysis"
```

### Step 2.8.2: Read Personal Ruleset

```bash
# Check if personal ruleset exists
if [ ! -f ~/.claude/CLAUDE.md ]; then
    echo "No personal ruleset found - skipping deduplication analysis"
    echo "Recommendation: Create personal ruleset for cross-project guidance"
    return 0
fi

echo "Reading personal ruleset for comparison..."

# Count personal ruleset size
personal_lines=$(wc -l < ~/.claude/CLAUDE.md)
personal_words=$(wc -w < ~/.claude/CLAUDE.md)
personal_tokens=$(echo "$personal_words * 1.3" | bc | cut -d'.' -f1)

echo "Personal ruleset: $personal_lines lines, $personal_words words, ~$personal_tokens tokens"
```

### Step 2.8.3: Extract Sections from Both Rulesets

```bash
# Extract section headers and line numbers from both files
# Format: line_number:header_text

# Personal ruleset sections
personal_sections=$(grep -n "^##" ~/.claude/CLAUDE.md | sed 's/:/ /' | while read line_num rest; do
    header=$(echo "$rest" | sed 's/^## //')
    echo "$line_num:$header"
done)

# Project ruleset sections
project_sections=$(grep -n "^##" .claude/CLAUDE.md | sed 's/:/ /' | while read line_num rest; do
    header=$(echo "$rest" | sed 's/^## //')
    echo "$line_num:$header"
done)

echo "Personal sections: $(echo "$personal_sections" | wc -l)"
echo "Project sections: $(echo "$project_sections" | wc -l)"
```

### Step 2.8.4: Section-Level Comparison

For each project section, check if personal ruleset has a similar section:

```bash
# Compare sections by header similarity
duplication_issues=()

while IFS=':' read -r proj_line proj_header; do
    # Look for similar headers in personal ruleset
    while IFS=':' read -r pers_line pers_header; do
        # Simple similarity: case-insensitive substring match
        proj_lower=$(echo "$proj_header" | tr '[:upper:]' '[:lower:]')
        pers_lower=$(echo "$pers_header" | tr '[:upper:]' '[:lower:]')

        # Check if headers are similar (contain same keywords)
        # Extract key words (4+ letters)
        proj_words=$(echo "$proj_lower" | grep -oE '\b[a-z]{4,}\b' | sort)
        pers_words=$(echo "$pers_lower" | grep -oE '\b[a-z]{4,}\b' | sort)

        # Count common words
        common_words=$(comm -12 <(echo "$proj_words") <(echo "$pers_words") | wc -l)

        if [ "$common_words" -ge 2 ]; then
            # Headers are similar - extract and compare content
            # Get next section line for boundaries
            proj_next=$(echo "$project_sections" | grep -A1 "^$proj_line:" | tail -1 | cut -d: -f1)
            if [ -z "$proj_next" ] || [ "$proj_next" = "$proj_line" ]; then
                proj_next=$(wc -l < .claude/CLAUDE.md)
            fi

            pers_next=$(echo "$personal_sections" | grep -A1 "^$pers_line:" | tail -1 | cut -d: -f1)
            if [ -z "$pers_next" ] || [ "$pers_next" = "$pers_line" ]; then
                pers_next=$(wc -l < ~/.claude/CLAUDE.md)
            fi

            # Extract section content
            proj_content=$(sed -n "${proj_line},${proj_next}p" .claude/CLAUDE.md)
            pers_content=$(sed -n "${pers_line},${pers_next}p" ~/.claude/CLAUDE.md)

            # Compare content similarity (keyword-based)
            proj_keywords=$(echo "$proj_content" | grep -oE '\b[a-z]{4,}\b' | sort | uniq)
            pers_keywords=$(echo "$pers_content" | grep -oE '\b[a-z]{4,}\b' | sort | uniq)

            common_kw=$(comm -12 <(echo "$proj_keywords") <(echo "$pers_keywords") | wc -l)
            total_kw=$(echo "$proj_keywords" "$pers_keywords" | tr ' ' '\n' | sort | uniq | wc -l)

            if [ "$total_kw" -gt 0 ]; then
                similarity=$((common_kw * 100 / total_kw))
            else
                similarity=0
            fi

            # Classify duplication based on similarity
            if [ "$similarity" -ge 80 ]; then
                # D1: Exact duplication
                issue_type="D1"
                issue_priority="HIGH"
            elif [ "$similarity" -ge 50 ]; then
                # D2: Hierarchical duplication
                issue_type="D2"
                issue_priority="HIGH"
            elif [ "$similarity" -ge 30 ]; then
                # D4: Redundant examples
                issue_type="D4"
                issue_priority="MEDIUM"
            else
                continue  # Not similar enough
            fi

            # Calculate section size
            section_words=$(echo "$proj_content" | wc -w)
            section_tokens=$(echo "$section_words * 1.3" | bc | cut -d'.' -f1)

            # Calculate savings based on issue type
            case "$issue_type" in
                D1) savings_pct=100 ;;
                D2) savings_pct=60 ;;
                D4) savings_pct=40 ;;
            esac
            savings=$((section_tokens * savings_pct / 100))

            # Record issue
            duplication_issues+=("$issue_type:$issue_priority:$proj_header:$proj_line:$similarity:$section_tokens:$savings")
        fi
    done <<< "$personal_sections"
done <<< "$project_sections"
```

### Step 2.8.5: Check for Skill Overlap (D3)

Cross-reference project sections with skills from Phase 2.5:

```bash
# Check if project sections duplicate skill content
# (Skills were already inventoried in Phase 2.5)

# For each project section, check if skill covers same topic
# Look for keywords that match skill descriptions

# Example: If project has "Git Workflow" section and git-workflow skill exists
# Flag as D3 issue

# Simple heuristic: Check section headers against skill names
for skill_name in $all_skill_names; do
    # Convert skill name to readable form (e.g., "git-workflow" → "git workflow")
    skill_readable=$(echo "$skill_name" | tr '-' ' ')

    # Check if any project section mentions this topic
    while IFS=':' read -r proj_line proj_header; do
        proj_lower=$(echo "$proj_header" | tr '[:upper:]' '[:lower:]')

        if echo "$proj_lower" | grep -q "$skill_readable"; then
            # Project section overlaps with skill topic
            issue_type="D3"
            issue_priority="MEDIUM"

            # Get section size
            proj_next=$(echo "$project_sections" | grep -A1 "^$proj_line:" | tail -1 | cut -d: -f1)
            if [ -z "$proj_next" ] || [ "$proj_next" = "$proj_line" ]; then
                proj_next=$(wc -l < .claude/CLAUDE.md)
            fi

            section_words=$(sed -n "${proj_line},${proj_next}p" .claude/CLAUDE.md | wc -w)
            section_tokens=$(echo "$section_words * 1.3" | bc | cut -d'.' -f1)
            savings=$((section_tokens * 80 / 100))  # 80% savings for skill extraction

            duplication_issues+=("$issue_type:$issue_priority:$proj_header:$proj_line:N/A:$section_tokens:$savings")
        fi
    done <<< "$project_sections"
done
```

### Step 2.8.6: Calculate Total Deduplication Savings

```bash
# Sum up all potential savings
total_dedup_savings=0
issue_count_high=0
issue_count_medium=0
issue_count_low=0

for issue in "${duplication_issues[@]}"; do
    IFS=':' read -r type priority header line sim tokens savings <<< "$issue"
    total_dedup_savings=$((total_dedup_savings + savings))

    case "$priority" in
        HIGH) issue_count_high=$((issue_count_high + 1)) ;;
        MEDIUM) issue_count_medium=$((issue_count_medium + 1)) ;;
        LOW) issue_count_low=$((issue_count_low + 1)) ;;
    esac
done

total_issue_count=$((issue_count_high + issue_count_medium + issue_count_low))
```

### Step 2.8.7: Output Deduplication Report

Present findings in markdown format:

```markdown
## Phase 2.8 Results: Personal/Project Deduplication

**Personal Ruleset**: ~/.claude/CLAUDE.md (~$personal_tokens tokens)
**Project Ruleset**: .claude/CLAUDE.md (~$project_tokens tokens)

**Duplication Issues Found**: $total_issue_count
- HIGH priority: $issue_count_high
- MEDIUM priority: $issue_count_medium
- LOW priority: $issue_count_low

**Potential Token Savings**: ~$total_dedup_savings tokens

### Duplication Issues Detected

[For each issue in duplication_issues array, output detailed report]

#### Issue D1: Exact Duplication - "[Header]"

**Lines**: [X-Y] ([N] lines, ~[M] tokens)
**Priority**: HIGH
**Similarity**: [P]%
**Token Savings**: ~[S] tokens

**Problem**:
Project section "[Header]" duplicates content from personal ruleset.

**Recommendation**:
Remove project section, content already in personal ruleset.

If project needs specific notes, replace with:
```markdown
## [Header]

See personal ruleset for [topic]. Project-specific notes:
- [Only project-specific details if any]
```

**Token Savings**: ~[S] tokens per session

---

[Repeat for each duplication issue]

### Deduplication Summary

**Recommendations**:
1. Remove [N] exact duplicates (HIGH): ~[X] tokens
2. Condense [M] hierarchical duplicates (HIGH): ~[Y] tokens
3. Reference [P] skills instead (MEDIUM): ~[Z] tokens
4. Simplify [Q] redundant examples (MEDIUM): ~[W] tokens

**Total Potential Savings**: ~$total_dedup_savings tokens ([P]% of project ruleset)

**Next Steps** (Phase 3):
- Ruleset analysis will consider these findings
- Unified recommendations (Phase 4) will include deduplication fixes
- Apply optimizations (Phase 5) can implement removals/consolidations
```

### Step 2.8.8: Store Results for Phase 4 Integration

```bash
# Store deduplication results for later use in Phase 4
DEDUP_ISSUE_COUNT=$total_issue_count
DEDUP_SAVINGS=$total_dedup_savings
DEDUP_ISSUES_ARRAY=("${duplication_issues[@]}")

# These will be referenced in Phase 4 unified recommendations
export DEDUP_ISSUE_COUNT DEDUP_SAVINGS
```

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

## PHASE 3.5: Skill Extraction Recommendations (Context Efficiency Focus)

**Purpose**: Identify opportunities to extract CLAUDE.md content into skills for improved context efficiency.

### Step 3.5.1: Analyze CLAUDE.md for Skill Candidates

Review the target CLAUDE.md for sections that match skill extraction criteria:

**Criteria for skill extraction**:
1. **Complexity**: >10 sequential steps, decision trees, multi-stage workflows
2. **Length**: >200 words of procedural content
3. **Repetition**: Same procedure mentioned 3+ times in CLAUDE.md
4. **Context cost**: >500 tokens estimated
5. **Frequency**: Used in ~50% of sessions or less (would benefit from selective loading)
6. **Procedural vs Policy**: Procedural ("how to") not policy ("what/why")

### Step 3.5.2: Identify CLAUDE.md Sections as Candidates

Check these common candidates:

**Candidate Type 1: Workflow Procedures**
- Example: "Running Lesson Code" section with bash commands and multi-step execution
- Example: "Deployment Workflow" with 15+ steps
- **Indicator**: Contains numbered steps, code blocks, conditional logic

**Candidate Type 2: Tool-Specific Guides**
- Example: "Git Workflow" procedures (commit, push, branching)
- Example: "Container Operations" (docker build, run, debug)
- **Indicator**: Mentions specific tools repeatedly

**Candidate Type 3: Environment Setup**
- Example: "Setting Up API Keys" across multiple services
- Example: "Configuring Development Environment"
- **Indicator**: One-time or occasional setup procedures

**Candidate Type 4: Debugging Guides**
- Example: "Common Errors and Solutions" with decision trees
- Example: "Troubleshooting Network Issues"
- **Indicator**: If-then logic, diagnostic steps

**Candidate Type 5: Project-Type Patterns**
- Example: Lesson-running procedures (if learning project)
- Example: Testing workflows specific to project type
- **Indicator**: Project-specific but reusable in similar projects

### Step 3.5.3: Cross-Reference with History Patterns

Match CLAUDE.md sections with history patterns from Phase 2:

**Pattern detected in history** + **Procedural content in CLAUDE.md** = **HIGH priority skill candidate**

Example:
- History: Manual .venv path usage (3 occurrences)
- CLAUDE.md: "Virtual Environment Handling" section (250 words)
- **Recommendation**: Extract to local skill "lesson-runner"

### Step 3.5.4: Check for Overlap with Existing Skills

Compare candidate sections with skills inventory from Phase 2.5:

**Scenario A: Content already covered by skill**
- CLAUDE.md has "Git Workflow" section (200 words)
- Skill "git-workflow" already exists (117 lines)
- **Recommendation**: Remove CLAUDE.md section, replace with skill reference

**Scenario B: Partial overlap**
- CLAUDE.md has generic Python advice
- Skill "python-workflow" has detailed Python patterns
- **Recommendation**: Keep high-level policy in CLAUDE.md, reference skill for details

**Scenario C: No overlap - new skill needed**
- CLAUDE.md has unique "Lesson Runner" procedures
- No existing skill covers this
- **Recommendation**: Extract to new local skill

### Step 3.5.5: Calculate Token Savings Per Candidate

For each skill extraction candidate:

**Current state** (inline in CLAUDE.md):
```
Section: "Running Lesson Code"
Lines: 27
Words: 240
Estimated tokens: 240 * 1.3 = 312 tokens
Loaded: 100% of sessions (always in CLAUDE.md)
Total cost per session: 312 tokens
```

**Optimized state** (extracted to skill):
```
CLAUDE.md reference: "See lesson-runner skill" (18 words, ~24 tokens)
Skill content: 240 words (~312 tokens when invoked)
Invocation rate: 50% of sessions (only loaded when running lessons)
Weighted cost per session: 24 + (312 * 0.5) = 24 + 156 = 180 tokens
Savings: 312 - 180 = 132 tokens per session
```

**Criteria for worthwhile extraction**:
- Saves >100 tokens per session (weighted average)
- OR invoked <30% of sessions (major baseline reduction)
- OR content is >500 tokens (large optimization potential)

### Step 3.5.6: Determine Skill Placement

For each recommended skill:

**Personal skill** (~/.claude/skills/):
- General-purpose across projects
- No project-specific references
- Example: "api-debugging", "git-advanced-workflow"

**Local skill** (.claude/skills/):
- Project-specific procedures
- References project directories/structure
- Example: "lesson-runner", "agent-spike-testing"

### Step 3.5.7: Draft Skill Templates

For each recommended skill extraction, provide a template:

```markdown
### Recommended Skill: lesson-runner

**Placement**: .claude/skills/lesson-runner.md (local skill)

**Rationale**:
- Complexity: 7 steps with conditional execution
- Size: 240 words (~312 tokens)
- Usage: ~50% of sessions (lesson work)
- Context savings: 132 tokens per session (weighted)
- Source: CLAUDE.md lines 173-200

**Skill Template**:

```yaml
---
name: lesson-runner
description: Run Python code in lesson context with proper virtual environment handling. Activate when user wants to run tests, demos, or CLI commands for lessons in .spec/lessons/. Handles uv run python, dependency management, and cross-directory execution.
---

# Lesson Runner Skill

Standard patterns for running lesson code with proper virtual environment and dependency management.

## When to Use

- User wants to run test scripts in lessons
- User wants to execute demos
- User wants to run lesson CLI commands
- User is working in .spec/lessons/ directories

## Running Lesson Code

[Extract content from CLAUDE.md lines 173-200]
\```bash
cd .spec/lessons/lesson-XXX
uv run python test_router.py
\```

[Additional procedures...]
\```
```

**CLAUDE.md Changes**:
Replace current section (lines 173-200) with:
```markdown
### Running Lesson Code

For detailed patterns on running lesson code, see the `lesson-runner` skill.

**Quick reference**: Always use `uv run python` from lesson directory.
\```
```

**Impact**:
- Baseline context: -288 tokens (removed from CLAUDE.md)
- Reference added: +24 tokens
- Skill loaded selectively: 312 tokens (50% of sessions)
- **Net savings: ~132 tokens per session**
```

### Step 3.5.8: Cross-Project Skill Recommendations

Check history for patterns that appear across MULTIPLE projects (Personal mode only):

**Pattern**: Appears in 3+ different projects
**Recommendation**: Create personal skill (benefits all projects)

Example:
```markdown
### Cross-Project Pattern: Docker Debugging

**Detected in**: agent-spike, web-app, api-service (3 projects)
**Frequency**: 5 occurrences total
**Content**: Docker container debugging procedures

**Recommendation**: Create personal skill "container-debugging"
- Placement: ~/.claude/skills/container-debugging/SKILL.md
- Activation: Dockerfile, docker-compose.yml, container mentions
- Content: Common docker debugging commands, log inspection, networking issues
- **Benefit**: Helps all 3 projects + future container projects
- **Token savings**: ~200 tokens baseline × 3 projects = 600 tokens total
```

### Step 3.5.9: Output Skill Extraction Report

Present findings:

```markdown
## Skill Extraction Recommendations

**Candidates Identified**: [N candidates from CLAUDE.md]
**Potential Savings**: [X tokens per session]

### High Priority Extractions (>200 token savings)

1. **lesson-runner** (Local Skill)
   - Source: CLAUDE.md lines 173-200
   - Size: 240 words (~312 tokens)
   - Usage: 50% of sessions
   - Savings: 132 tokens per session
   - Placement: .claude/skills/lesson-runner.md

[Repeat for each high-priority candidate]

### Medium Priority Extractions (100-200 token savings)

[List medium priority candidates]

### Overlap Opportunities (Consolidation)

**Overlap 1: Git Workflow**
- CLAUDE.md has "Git Usage" section (180 words, ~234 tokens)
- Skill "git-workflow" already exists (117 lines, ~757 tokens)
- **Recommendation**: Remove CLAUDE.md section, reference skill
- **Savings**: 234 tokens baseline (100% of sessions)

[Repeat for other overlaps]

### Cross-Project Skills (Personal Mode Only)

[List patterns detected across multiple projects]

### Total Potential Impact

**If all recommendations implemented**:
- Current CLAUDE.md: [X tokens]
- Optimized CLAUDE.md: [Y tokens] (baseline)
- Skills loaded selectively: [Z tokens] (weighted average)
- **Total savings: [W tokens] per session (~N% reduction)**
```

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

## Part 4: Context Efficiency Analysis 🌟

**PRIMARY FOCUS**: Token savings through skills and optimization

### Token Comparison (Before vs After)

**Current Context** (Before Optimization):

```
Personal Ruleset:
├─ ~/.claude/CLAUDE.md: [X] lines (~[Y] words, ~[Z] tokens)

Project Ruleset:
├─ .claude/CLAUDE.md: [A] lines (~[B] words, ~[C] tokens)

Skills (if all loaded):
├─ python-workflow: 88 lines (~600 tokens)
├─ git-workflow: 117 lines (~757 tokens)
├─ multi-agent-ai-projects: 85 lines (~521 tokens)
├─ web-projects: 99 lines (~579 tokens)
├─ container-projects: 133 lines (~700 tokens)
└─ Total skills: [N] (~[M] tokens)

TOTAL CONTEXT: ~[TOTAL] tokens (if all loaded)
```

**Optimized Context** (After Optimization):

```
Personal Ruleset:
├─ ~/.claude/CLAUDE.md: [X2] lines (~[Y2] words, ~[Z2] tokens)
├─ Change: -[N]% ([saved] tokens saved)

Project Ruleset:
├─ .claude/CLAUDE.md: [A2] lines (~[B2] words, ~[C2] tokens)
├─ Change: -[P]% ([saved2] tokens saved)

Skills (Project-Aware Loading):
├─ ACTIVE for this project:
│   ├─ python-workflow: 88 lines (~600 tokens) ✅
│   └─ multi-agent-ai-projects: 85 lines (~521 tokens) ✅
├─ INACTIVE (not loaded):
│   ├─ git-workflow: 117 lines (~757 tokens saved)
│   ├─ web-projects: 99 lines (~579 tokens saved)
│   └─ container-projects: 133 lines (~700 tokens saved)
└─ Context savings from skills: [N] tokens ([P]%)

OPTIMIZED BASELINE: ~[NEW_TOTAL] tokens
SAVINGS: ~[SAVINGS] tokens ([PERCENT]% reduction) ✨
```

### Skill-Based Optimization Impact

**Skills Inventory** (from Phase 2.5):
- Personal skills: [N] ([M] tokens total if all loaded)
- Active for project: [X] skills ([Y] tokens)
- Inactive: [Z] skills ([W] tokens saved by not loading)

**Skill Extraction Recommendations** (from Phase 3.5):
- High priority extractions: [N] candidates
- Potential additional savings: ~[M] tokens per session
- Overlap opportunities: [X] (consolidation with existing skills)

### Deduplication Impact (Project Mode Only)

**Personal/Project Overlap** (from Phase 2.8):
- Duplication issues detected: [N] (HIGH: [X], MEDIUM: [Y], LOW: [Z])
- Token savings from deduplication: ~[M] tokens

**Breakdown by Issue Type**:
```
D1 (Exact Duplicates): [N] sections (~[X] tokens)
├─ Remove from project, already in personal
└─ Savings: 100% of section content

D2 (Hierarchical Duplicates): [N] sections (~[Y] tokens)
├─ Keep project-specific details only
└─ Savings: ~60% of section content

D3 (Skill Overlap): [N] sections (~[Z] tokens)
├─ Reference skill instead of duplicating
└─ Savings: ~80% of section content (via extraction)

D4 (Redundant Examples): [N] sections (~[W] tokens)
├─ Simplify or reference personal
└─ Savings: ~40% of section content
```

**Impact**:
- Current project ruleset includes duplicated content: ~[M] tokens
- After deduplication: Project focuses only on project-specific context
- **Clearer separation**: General (personal) vs Specific (project)
- **Easier maintenance**: Update general rules once, not per-project

### Estimated Session Context

**Baseline Context** (loaded for every session):
```
Before: [X] tokens (CLAUDE.md + all skills if loaded)
After:  [Y] tokens (optimized CLAUDE.md + skill references)
Savings: [Z] tokens ([P]% reduction)
```

**Weighted Average** (accounting for skill invocation):
```
Typical session (no skill invocation): [A] tokens
With 1 skill invoked: [B] tokens
With 2 skills invoked: [C] tokens

Weighted average (based on usage patterns): ~[W] tokens
Savings vs. current: ~[S] tokens per session
```

### Cost Savings Estimate

**Token Economics**:
- Per-session savings: ~[N] tokens
- Sessions per week: ~[M] (estimated)
- Weekly savings: ~[N×M] tokens
- Monthly savings: ~[N×M×4] tokens

**Estimated Cost** (Claude Sonnet 4.5 pricing):
- Input: $3/million tokens
- Savings per month: ~$[COST] (at [N×M×4] tokens/month)
- Yearly savings: ~$[COST×12]

**Note**: Primary benefit is faster response times and more focused context, cost savings are secondary.

### Optimization Summary

**Structural Changes**:
- Current: [X lines, Y sections]
- Optimized: [~A lines, B sections]
- Removed: [N lines of redundant/outdated content]
- Added: [M lines of new rules from history]
- Reorganized: [P sections reordered for priority]

**Key Improvements**:
1. [Improvement 1 with token impact]
2. [Improvement 2 with token impact]
3. [Improvement 3 with token impact]
[...]

**Skills Recommendations**:
- Extract [N] sections to local skills: ~[M] tokens saved
- Consolidate [X] overlaps with existing skills: ~[Y] tokens saved
- Create [Z] cross-project skills (personal mode): benefits all projects

**Checkpoint Status**:
- Location: [.claude/CHECKPOINT | ~/.claude/CHECKPOINT]
- Previous: [timestamp | None]
- Updated: [new timestamp]
- Next run: Will analyze only NEW history since this timestamp

### Why This Matters

**Context Efficiency Benefits**:
1. **Faster Responses**: Smaller baseline context = faster Claude initialization
2. **More Focused**: Only relevant information loaded per project
3. **Better Reasoning**: Claude has more room for thinking with smaller baseline
4. **Scales Better**: As you add projects, skills prevent context explosion
5. **Self-Improving**: Each optimization compounds with future improvements

**Example Impact**:
```
Project A (Python learning):
└─ Loads: python-workflow + multi-agent-ai-projects skills
└─ Skips: web-projects + container-projects + git-workflow
└─ Savings: 2,036 tokens (64% skill context reduction)

Project B (Web app):
└─ Loads: web-projects + git-workflow skills
└─ Skips: python-workflow + multi-agent-ai-projects + container-projects
└─ Savings: 1,121 tokens (different skills, same efficiency)

Result: Each project gets tailored context, not everything!
```

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

### Implementation Strategy

**Recommended approach for file modifications:**

Use **Task tool with specialized agents** for complex operations:
- Multiple rulesets to update (personal + project)
- Home directory files (especially ~/.claude/ on Windows)
- Content with complex escaping needs (markdown with code blocks, quotes)
- Atomic multi-file coordination

**Direct tools work well for:**
- Backups: `cp file file.backup`
- Reading for analysis: `cat file` or Read tool
- Single project-local edits: Edit tool
- Simple verification: `wc -l`, `diff`, etc.

**Why Task tool for complex operations:**
- Abstracts away cross-platform path resolution issues
  - Windows: ~/.claude/ paths work in bash but may fail in Read/Edit tools
  - Python: Requires `os.path.expanduser('~/')`, not `/c/Users/...`
- Handles content escaping automatically (markdown, code blocks, nested quotes)
- Better error handling and validation
- Can read current state, generate complete optimized versions, and coordinate multiple related changes

**Python path handling (if used directly):**
- ALWAYS use `os.path.expanduser('~/.claude/...')` for home directory
- NEVER hardcode MSYS paths like `/c/Users/...` (breaks in Python's open())
- Use raw strings for Windows paths: `r'C:\Users\...'`

**Bash heredoc limitations:**
- Complex markdown with nested quotes/backticks is fragile
- Multiple levels of escaping cause syntax errors
- If content is complex, use Task tool or Python with proper string handling

**Note**: The Task tool approach is not a workaround—it's the architecturally correct pattern for complex multi-file operations. Simple operations can use direct tools.

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
