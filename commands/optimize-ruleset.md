---
description: Analyze and optimize CLAUDE.md ruleset files with project-aware meta-learning, skills analysis, personal/project deduplication, and context efficiency optimization
---

# Optimize Ruleset Command

For optimization philosophy and principles, see the `ruleset-optimization` skill.

## Parameters
- No parameter: `/optimize-ruleset` → Optimize project ruleset at `.claude/CLAUDE.md`
- `personal`: `/optimize-ruleset personal` → Optimize personal ruleset at `~/.claude/CLAUDE.md`
- `--no-history`: Skip history analysis
- `--history-only`: Only analyze history, don't modify ruleset

## Process Overview
1. Determine target and context
2. Analyze history for patterns (if checkpoint older than last run)
3. Inventory skills and calculate context efficiency
4. Detect personal/project duplication (project mode only)
5. Analyze ruleset issues
6. Recommend skill extractions
7. Present unified recommendations with token metrics
8. Apply optimizations if approved

## PHASE 1: Determine Target & Context

### Step 1.1: Parse Parameters
```bash
# Check parameter
if [ "$1" = "personal" ]; then
    mode="personal"
    target="~/.claude/CLAUDE.md"
    checkpoint_path="~/.claude/CHECKPOINT"
else
    mode="project"
    target=".claude/CLAUDE.md"
    checkpoint_path=".claude/CHECKPOINT"
fi

# Check flags
no_history=$(echo "$@" | grep -q "\-\-no-history" && echo "true" || echo "false")
history_only=$(echo "$@" | grep -q "\-\-history-only" && echo "true" || echo "false")
```

### Step 1.2: Get Current Directory (Project Mode Only)
```bash
if [ "$mode" = "project" ]; then
    current_dir=$(pwd)
    # Normalize path: C:\Projects\... → /c/Projects/...
    current_project_path=$(echo "$current_dir" | sed 's|\\|/|g' | sed 's|^C:|/c|I' | sed 's|^D:|/d|I')
fi
```

### Step 1.3: Create Directory and Verify Target
```bash
# Create .claude directory if needed
if [ "$mode" = "project" ]; then
    mkdir -p .claude
fi

# Check target exists
if [ ! -f "$target" ]; then
    echo "No ruleset found at $target"
    echo "Would you like to create one? (y/n)"
    # Exit if user declines
fi
```

### Step 1.4: Gather Project Context (Project Mode Only)
```bash
if [ "$mode" = "project" ]; then
    # Check structure
    ls -la
    find . -maxdepth 2 -type d | head -20

    # Check package managers
    ls pyproject.toml setup.py requirements.txt package.json Cargo.toml go.mod 2>/dev/null

    # Check git
    git status --short 2>/dev/null || echo "Not a git repo"
fi
```

Output context summary with mode, target, checkpoint, and project type.

## PHASE 2: History Analysis

Skip if `--no-history` flag present.

### Step 2.1: Read Checkpoint
```bash
checkpoint_timestamp=$(grep "^optimize-ruleset:" "$checkpoint_path" 2>/dev/null | cut -d' ' -f2)
if [ -z "$checkpoint_timestamp" ]; then
    checkpoint_timestamp="1970-01-01T00:00:00Z"
fi

# Convert to milliseconds
checkpoint_seconds=$(date -d "$checkpoint_timestamp" +%s 2>/dev/null)
checkpoint_ms=$((checkpoint_seconds * 1000))
```

### Step 2.2: Filter History

For project mode:
```bash
# Filter by timestamp AND project path
while IFS= read -r line; do
    entry_timestamp=$(echo "$line" | python -c "import sys,json; print(json.load(sys.stdin)['timestamp'])" 2>/dev/null)
    entry_project=$(echo "$line" | python -c "import sys,json; print(json.load(sys.stdin).get('project', ''))" 2>/dev/null)
    entry_project=$(echo "$entry_project" | sed 's|\\|/|g' | sed 's|^C:|/c|I')

    if [ "$entry_timestamp" -gt "$checkpoint_ms" ] && [ "$entry_project" = "$current_project_path" ]; then
        echo "$line" >> /tmp/filtered_history.jsonl
    fi
done < ~/.claude/history.jsonl
```

For personal mode: Filter by timestamp only (include all projects).

### Step 2.3: Detect Patterns

Check for these patterns in filtered history:
1. **Bash commands instead of tools** (grep, find, cat)
2. **Manual virtual env paths** (../.venv/)
3. **User corrections** ("no", "actually", "incorrect")
4. **Missing context checks** (file not found errors)
5. **Forgotten workflow steps** (reminders about STATUS.md)
6. **TODO list issues** (not updating, multiple in_progress)

For each pattern found, record:
- Frequency (occurrences)
- Example from history
- Suggested rule
- Priority (HIGH/MEDIUM/LOW based on frequency)

### Step 2.4: Update Checkpoint
```bash
new_timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
other_lines=$(grep -v "^optimize-ruleset:" "$checkpoint_path" 2>/dev/null)
{
    echo "$other_lines"
    echo "optimize-ruleset: $new_timestamp"
} > "$checkpoint_path"
```

## PHASE 2.5: Skills Inventory

### Step 2.5.1: Discover Skills
```bash
personal_skills=$(find ~/.claude/skills -name "SKILL.md" 2>/dev/null)
local_skills=$(find .claude/skills -name "SKILL.md" 2>/dev/null)
```

### Step 2.5.2: Analyze Each Skill
For each skill:
```bash
skill_name=$(grep "^name:" "$skill_file" | cut -d':' -f2- | xargs)
lines=$(wc -l < "$skill_file")
words=$(wc -w < "$skill_file")
tokens=$((words * 13 / 10))  # Estimate 1.3 tokens per word
```

### Step 2.5.3: Determine Activation
Check if project has files/directories that would activate each skill:
- python-workflow: Check for .py, pyproject.toml
- git-workflow: Check for .git directory
- web-projects: Check for package.json
- container-projects: Check for Dockerfile

### Step 2.5.4: Calculate Context Savings
```bash
active_tokens=0
inactive_tokens=0
# Sum tokens for active/inactive skills
# Calculate savings percentage
```

Output skills inventory with activation status and token savings.

## PHASE 2.8: Personal/Project Deduplication (Project Mode Only)

Skip in personal mode.

### Step 2.8.1: Read Personal Ruleset
```bash
if [ ! -f ~/.claude/CLAUDE.md ]; then
    echo "No personal ruleset for deduplication comparison"
    return 0
fi
```

### Step 2.8.2: Compare Sections
Extract section headers from both rulesets. For similar headers:
- Calculate content similarity percentage
- Classify duplication type:
  - D1: Exact (>80% similar) - HIGH priority
  - D2: Hierarchical (50-80%) - HIGH priority
  - D3: Skill overlap - MEDIUM priority
  - D4: Redundant examples (30-50%) - MEDIUM priority

### Step 2.8.3: Calculate Savings
For each duplication issue, calculate token savings based on type:
- D1: 100% of section
- D2: 60% of section
- D3: 80% of section
- D4: 40% of section

Output deduplication report with total potential savings.

## PHASE 3: Ruleset Analysis

### Step 3.1: Read Target Ruleset
Count lines, sections, approximate tokens.

### Step 3.2: Detect Issues

**HIGH Priority:**
- H1: Outdated project description
- H2: Technical inaccuracies
- H3: Missing critical context
- H4: Contradictions
- H5: References to non-existent files

**MEDIUM Priority:**
- M1: Poor section ordering
- M2: Missing quick start
- M3: Unclear doc relationships
- M4: Unexplained dual structures
- M5: Irrelevant detail overload

**LOW Priority:**
- L1: Verbose explanations
- L2: Missing examples
- L3: Inconsistent formatting
- L4: No summary section
- L5: Missing directory structure

For each issue found, note location and specific problem.

## PHASE 3.5: Skill Extraction Recommendations

### Step 3.5.1: Identify Candidates
Look for sections that are:
- >200 words of procedural content
- >10 sequential steps
- Used in <70% of sessions
- Domain-specific (git, python, docker)

### Step 3.5.2: Calculate Token Savings
For each candidate:
```
Current: [tokens] (always loaded)
As skill: [ref_tokens] + ([skill_tokens] * usage_freq)
Savings: current - as_skill
```

### Step 3.5.3: Check Overlap
Compare candidates with existing skills:
- Already covered → Remove from CLAUDE.md, reference skill
- Partial overlap → Keep policy in CLAUDE.md, reference skill for details
- No overlap → Create new skill

Output extraction recommendations with token savings.

## PHASE 4: Unified Recommendations

### Step 4.1: Combine Findings
Merge:
- History patterns (Phase 2)
- Skills inventory (Phase 2.5)
- Deduplication issues (Phase 2.8)
- Ruleset issues (Phase 3)
- Extraction candidates (Phase 3.5)

### Step 4.2: Prioritize
- CRITICAL: Issues in both history and ruleset
- HIGH: Technical inaccuracies, 3+ occurrences
- MEDIUM: Structural issues, 2 occurrences
- LOW: Polish, 1 occurrence

### Step 4.3: Present Report

```markdown
# Ruleset Optimization Analysis

**Mode**: [Project/Personal]
**Target**: [Path]
**History Analyzed**: [X entries since checkpoint]

## Issues Found
- CRITICAL: [count]
- HIGH: [count]
- MEDIUM: [count]
- LOW: [count]

## Token Impact
Current: [X] tokens
Optimized: [Y] tokens
Savings: [Z] tokens ([P]% reduction)

## Recommendations

[List each recommendation with priority, problem, fix, and impact]

## What would you like me to do?
1. Apply HIGH + CRITICAL only
2. Apply HIGH + MEDIUM + CRITICAL (recommended)
3. Apply ALL recommendations
4. Show draft first
5. Analysis only
6. Add history rules only
```

## PHASE 5: Apply Optimizations

Based on user choice:

### Option 1-3: Apply Fixes
1. Create backup: `cp $target $target.backup`
2. Apply changes based on priority level
3. Verify valid markdown
4. Show diff summary

### Option 4: Show Draft
Generate complete optimized version for review.

### Option 5: Analysis Only
Report already shown, no changes.

### Option 6: Add Rules Only
Insert new rules from history into appropriate sections.

## Path Normalization Function
```bash
normalize_path() {
    local path="$1"
    echo "$path" | sed 's|\\|/|g' | sed 's|^C:|/c|I' | sed 's|^D:|/d|I'
}
```

## Edge Cases
1. No .claude directory → Create it
2. No project field in history → Skip for project mode, include for personal
3. Path normalization → Normalize before comparison
4. Multiple checkpoint types → Each command updates only its line
5. No history for project → Skip history analysis, continue with ruleset

## Success Criteria
- Correctly determines target (project vs personal)
- Uses project-specific checkpoint
- Filters history by project in project mode
- Identifies real patterns
- Generates actionable rules
- Detects ruleset issues accurately
- Provides clear priorities
- Updates checkpoint properly
- Handles edge cases gracefully