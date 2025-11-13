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
1. Determine target (project vs personal) and gather project context
2. Analyze git history for workflow patterns (if checkpoint outdated)
3. Inventory skills and calculate context efficiency gains
4. Detect personal/project duplication (project mode only)
5. Analyze ruleset for issues and outdated content
6. Recommend skill extractions based on token savings
7. Present unified report with priorities and token impact
8. Apply optimizations if user approves

## PHASE 1: Target & Context

Parse parameters (`personal` flag, `--no-history`, `--history-only`) to determine target ruleset path and mode. Create `.claude` directory if needed (project mode). Verify target exists; gather project context via directory listing, package manager detection (pyproject.toml, package.json, Cargo.toml, go.mod), and git status.

## PHASE 2: History Analysis

Skip if `--no-history` flag present.

Read checkpoint timestamp for optimize-ruleset. Filter history by timestamp (personal mode) or timestamp + project path (project mode). Scan filtered entries for workflow antipatterns.

| Pattern | Description |
|---------|-------------|
| Tool misuse | Using bash (grep, find, cat) instead of Read/Glob/Grep tools |
| Path hardcoding | Manual `.venv/` or absolute paths instead of relative/dynamic |
| Correction loops | Repeated corrections ("no", "actually") indicate unclear rules |
| Missing preconditions | File not found errors suggest rule skips verification steps |
| Forgotten workflows | STATUS.md, checkpoint updates, or test reminders |
| Todo misuse | Not updating lists, multiple in_progress tasks |

For each pattern: count occurrences, provide example, suggest rule addition, set priority based on frequency.

Update checkpoint with current timestamp after analysis.

## PHASE 2.5: Skills Inventory

Discover skills in `~/.claude/skills/` and `./.claude/skills/`. For each skill: extract name, count lines/words, estimate tokens (1.3 tokens/word).

Determine activation by checking project indicators (e.g., `pyproject.toml` → python-workflow, `.git` → git-workflow, `package.json` → web-projects). Calculate token savings: sum active (always loaded) vs inactive (conditional) tokens. Output inventory with activation status and context efficiency gains.

## PHASE 2.8: Personal/Project Deduplication

Skip in personal mode. Compare project ruleset sections with personal ruleset (exit if personal not found). Extract headers, calculate similarity %, classify duplication type.

| Type | Similarity | Priority | Savings |
|------|-----------|----------|---------|
| D1 - Exact duplication | >80% | HIGH | 100% of section |
| D2 - Hierarchical overlap | 50-80% | HIGH | 60% of section |
| D3 - Skill overlap | Partial | MEDIUM | 80% of section |
| D4 - Redundant examples | 30-50% | MEDIUM | 40% of section |

Output deduplication report with total potential savings.

## PHASE 3: Ruleset Analysis

Read target ruleset; count lines, sections, estimate tokens. Detect issues by priority.

| Priority | Issue | Description |
|----------|-------|-------------|
| HIGH | H1 | Outdated project description |
| HIGH | H2 | Technical inaccuracies |
| HIGH | H3 | Missing critical context |
| HIGH | H4 | Contradictions |
| HIGH | H5 | References to non-existent files |
| MEDIUM | M1 | Poor section ordering |
| MEDIUM | M2 | Missing quick start or critical intro |
| MEDIUM | M3 | Unclear documentation relationships |
| MEDIUM | M4 | Unexplained dual structures |
| MEDIUM | M5 | Irrelevant detail overload |
| LOW | L1 | Verbose explanations (convertible to bullets) |
| LOW | L2 | Missing examples |
| LOW | L3 | Inconsistent formatting |
| LOW | L4 | No summary section |
| LOW | L5 | Missing directory structure |

For each issue: note location, description, and severity.

## PHASE 3.5: Skill Extraction

Identify candidates: >200 words procedural content, >10 sequential steps, <70% session usage, domain-specific (git, python, docker).

Calculate savings: Current tokens (always loaded) vs As skill (reference tokens + skill tokens × usage frequency). Compare with existing skills: if overlap exists, reference existing skill; if new, extract. Output recommendations with token savings.

## PHASE 4: Unified Recommendations

Merge all findings: history patterns, skills inventory, deduplication issues, ruleset issues, extraction candidates.

Prioritize: CRITICAL (both history + ruleset), HIGH (3+ occurrences or technical), MEDIUM (2 occurrences or structural), LOW (1 occurrence or polish).

Present report with mode, target, history sample size, issue counts, token impact (current → optimized → savings %), and recommendations. Offer user choices: apply HIGH+CRITICAL, HIGH+MEDIUM+CRITICAL (recommended), ALL, show draft, analysis only, or add history rules only.

## PHASE 5: Apply Optimizations

**Option 1-3: Apply Fixes** - Create backup, apply changes by priority level, verify markdown validity, show diff.

**Option 4: Show Draft** - Generate complete optimized version for review.

**Option 5: Analysis Only** - Report complete; no changes.

**Option 6: Add Rules Only** - Insert new history-based rules into appropriate sections.

## Edge Cases

1. No `.claude` directory → Create it
2. No project field in history → Skip for project mode, include for personal
3. Path normalization → Convert Windows paths (C:\...) to POSIX (/c/...)
4. Multiple checkpoint types → Each command updates only its line
5. No history for project → Skip history analysis, continue with ruleset

## Success Criteria

- Correctly determines target (project vs personal)
- Uses project-specific checkpoint in project mode
- Filters history by project path in project mode
- Identifies real workflow patterns from history
- Generates actionable, testable rules
- Detects ruleset issues accurately
- Provides clear prioritization
- Updates checkpoint after analysis
- Handles edge cases gracefully