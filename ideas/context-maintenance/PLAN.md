# Context Maintenance System - Comprehensive Plan

**Created**: 2025-01-24
**Problem**: Claude doesn't check existing context (STATUS.md, CLAUDE.md, skills) before acting, leading to pattern violations and out-of-date documentation
**Solution**: Three-tier approach combining hooks, git automation, and plan mode integration

---

## Problem Analysis

Based on user feedback and exploration:

1. **STATUS.md gets stale** - Updated manually after work, often forgotten during rapid iteration
2. **CLAUDE.md doesn't reflect new patterns** - Project conventions change but aren't documented
3. **Skills don't auto-update** - Patterns emerge from code but aren't extracted to skills
4. **Claude ignores context** - Jumps to solutions without reading existing docs (15% check rate)
5. **Plans don't include context updates** - Not treated as deliverables, so they don't happen

**Result**: Violated patterns, duplicate work, wrong priorities, stale documentation

---

## Recommended Solution: Multi-Tier Integration

### Tier 1: Hook-Based Context Prompting (Behavioral)
**Goal**: Force Claude to see context before acting

### Tier 2: Git-Based Automation (Maintenance)
**Goal**: Auto-maintain STATUS.md/CLAUDE.md from actual commits

### Tier 3: Plan Mode Integration (Process)
**Goal**: Make context updates explicit deliverables in every plan

---

## Tier 1: Hook-Based Context Prompting

### Overview
Use `UserPromptSubmit` hooks to inject context summaries before Claude sees the prompt. Creates "speed bump" that makes context impossible to miss.

### Architecture

**Hook File**: `~/.claude/hooks/inject-context.py`

**Trigger**: Every prompt in projects with `.claude/` directory

**Execution Time**: <100ms (parses first 100 lines of STATUS.md, first 5KB of CLAUDE.md)

### What Gets Injected

**Tier 1 (Universal - ~150 tokens)**:
```
═══ CONTEXT CHECKPOINT ═══
Project: agent-spike | Updated: 2025-11-24
Phase: Personal AI Research Assistant

📋 STATUS.md exists - Current state, blockers, next steps
📖 CLAUDE.md exists - Project patterns, architecture rules
🎯 VISION.md exists - Long-term roadmap

⚠️ REQUIRED BEFORE CHANGES:
  1. Check STATUS.md for current phase
  2. Check CLAUDE.md for existing patterns
  3. State findings in response
═══════════════════════════
```

**Tier 2 (Intent-Specific - additional 150-250 tokens)**:

- **Code modification** detected (keywords: implement, add, create, modify, fix):
  ```
  🔨 CODE MODIFICATION DETECTED
  Check STATUS.md (current phase, blockers, recent completions)
  Check CLAUDE.md (service patterns, file locations, architecture)
  RESPOND: "Checked [file] - [finding]" before proposing code.
  ```

- **Planning** detected (keywords: design, plan, architect, approach):
  ```
  📐 PLANNING DETECTED
  Review VISION.md + STATUS.md (design decisions made) + active skills
  RESPOND: "Reviewed [context] - following [pattern]" before design.
  ```

- **Debugging** detected (keywords: why, error, failing, broken, debug):
  ```
  🐛 DEBUGGING DETECTED
  Check STATUS.md "Known Issues" + git log + existing error patterns
  RESPOND: "Checked [source] - [finding]" before fix.
  ```

- **Git operations** detected (keywords: commit, push, git):
  ```
  🔀 GIT OPERATION DETECTED
  Security scan + STATUS.md alignment + git-workflow skill active
  ```

### Intent Classification

Simple keyword matching:
```python
def classify_intent(prompt: str) -> list[str]:
    p = prompt.lower()
    intents = []

    if any(kw in p for kw in ['commit', 'push', 'git']):
        intents.append('git')
    if any(kw in p for kw in ['implement', 'add', 'create', 'modify', 'fix']):
        intents.append('code')
    if any(kw in p for kw in ['design', 'plan', 'architect', 'approach']):
        intents.append('planning')
    if any(kw in p for kw in ['why', 'error', 'failing', 'broken', 'debug']):
        intents.append('debug')

    return intents or ['default']
```

### Realistic Expectations

**Baseline** (no hooks):
- Claude checks context: ~15% of time
- Pattern violations: 8-10/week
- User corrections: 10-12/week

**With hooks** (after 2-3 weeks):
- Claude checks context: ~60-70% of time (4x improvement)
- Pattern violations: 2-3/week (70% reduction)
- User corrections: 3-4/week (65% reduction)

**Never reaches 100%**: Claude is probabilistic. Will occasionally skip context despite prompting.

### Implementation Files

1. **`~/.claude/hooks/inject-context.py`** (new)
   - Intent classification
   - STATUS.md/CLAUDE.md parsing
   - Context injection formatting

2. **`~/.claude/hooks/hooks.json`** (modify)
   - Register inject-context hook
   - No matchers = runs on all prompts

3. **`~/.claude/CLAUDE.md`** (modify)
   - Add "Context Verification Protocol" section
   - Explicit instruction to read hook summaries first

4. **`.claude/CLAUDE.md`** (modify)
   - Add "Required Reading" section
   - Link to hook behavior

### Trade-offs

**Advantages**:
- ✅ Zero user overhead (automatic)
- ✅ Consistent application (every prompt)
- ✅ Intent-aware (different warnings for different tasks)
- ✅ Fast iteration (update hook → affects all projects)

**Disadvantages**:
- ❌ Token cost (~150-400 per prompt = $0.0001 each)
- ❌ No guarantee (Claude can still ignore)
- ❌ Notification fatigue (brain tunes out repetition)
- ❌ False positives (intent misclassification)

**Mitigation**:
- Vary wording to prevent tuning out
- Keep summaries compact (<350 tokens avg)
- Tune keywords based on usage
- Combine with explicit ruleset instructions

---

## Tier 2: Git-Based Automation

### Overview
Use git hooks (post-commit, post-merge) to automatically update STATUS.md and draft CLAUDE.md/skill updates based on actual commits.

### Architecture

**Hooks**:
- **post-commit**: Immediate updates (Git State section, <5 seconds)
- **post-merge**: Batch processing (Recent Completions, design decisions, <10 seconds)

### Commit Analysis Engine

**File**: `.githooks/lib/commit_analyzer.py`

**Extracts**:
```python
@dataclass
class CommitAnalysis:
    sha: str
    type: str  # feat, fix, refactor, docs, test, chore
    scope: str | None
    subject: str
    files_changed: list[str]

    # Detected patterns
    new_services: list[str]
    new_protocols: list[str]
    migrations: list[str]

    # Significance flags
    is_design_decision: bool
    is_new_pattern: bool
    affects_skills: list[str]
    completion_summary: str | None
```

**Pattern Detection**:
- New protocols: `grep 'class.*Protocol:' diff`
- New services: New files in `compose/services/*/`
- Design decisions: Commit body >100 chars with rationale
- Migrations: Message contains "migrate", diffs show old→new
- Completions: Message contains "complete", tests passing
- Skill relevance: File paths match skill activation patterns

### STATUS.md Updates

#### A. Git State Section (AUTO-UPDATE)

**Always safe, fast update**:
```markdown
## Git State
- Branch: main
- Recent commits (2025-11-24):
  - 5418aaa - docs: add proactive memory system design
  - 65ca4b8 - feat: add archive-to-MinIO migration script
- Status: Clean working tree
```

**Updates**: Every post-commit (<200ms)
**Safety**: Backed up before update, changes staged for next commit

#### B. Recent Completions (DRAFT MODE)

**Completion detection**:
1. Multiple commits with same scope
2. Final commit contains "complete" or "tests passing"
3. No new commits in scope for 2+ hours

**Output**: Draft at `.claude/context-updates/YYYYMMDD-completion.md`

**Example auto-generated**:
```markdown
**URL Pattern Analytics SurrealDB Migration** ✅ COMPLETE (2025-11-24)
- Added AsyncPatternTracker protocol and SurrealDB models
- Extracted pattern matching logic to pure functions
- Implemented SurrealDB repository for analytics
- Created TDD test suite (27 tests)
- 6 commits, all tests passing
```

**User workflow**: Review draft → manually add to STATUS.md → delete draft

#### C. Lesson Progress (AUTO-DETECT)

**Detects**:
- COMPLETE.md file created in `lessons/lesson-XXX/`
- Commit message: "complete lesson X"
- Tests passing in lesson directory

**Auto-updates**:
- Increment lesson count
- Add to "Completed Lessons" section

### CLAUDE.md Updates

#### Pattern Detection

**File**: `.githooks/lib/pattern_detector.py`

**Detects**:

1. **Design Decisions** (commit body >100 chars):
   ```python
   DesignDecision(
       title="Optimize git hooks for performance",
       rationale="Pre-commit scanning 1,633 files took 75 seconds",
       solution="Only scan staged files (1-5 files typically)",
       suggested_section="## Git Hooks",
       draft_file=".claude/context-updates/20251124-claude-githooks.md"
   )
   ```

2. **Conventions** (3+ commits with pattern):
   ```python
   Convention(
       pattern="Async* prefix for async protocols",
       occurrences=5,
       examples=["AsyncPatternTracker", "AsyncCacheManager"],
       suggested_update="Add to Python Workflow section"
   )
   ```

**Output**: Always drafts for user review, never auto-commits to CLAUDE.md

### Skill Updates

**File**: `.githooks/lib/skill_matcher.py`

**Maps file changes to skills**:
```python
SKILL_PATTERNS = {
    "agent-spike-project": {
        "paths": ["compose/services/**", "compose/cli/**"],
        "keywords": ["service", "protocol", "archive"]
    },
    "python-workflow": {
        "paths": ["**/*.py", "pyproject.toml"],
        "keywords": ["uv", "pytest", "protocol"]
    }
}
```

**When patterns emerge** (3+ uses in different contexts):
- Generates draft at `.claude/context-updates/YYYYMMDD-skill-NAME.md`
- Includes suggested text with examples
- User reviews → applies → deletes draft

### Safety Mechanisms

**Backups**:
```python
def backup_file(filepath: Path) -> Path:
    """Create timestamped backup before EVERY update."""
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup = filepath.parent / f"{filepath.name}.bak.{timestamp}"
    shutil.copy(filepath, backup)
    return backup  # Keep last 5 backups
```

**Auto-stage, NOT auto-commit**:
```bash
# Update + stage, user commits when ready
git add .claude/STATUS.md
echo "[post-commit] STATUS.md updated and staged"
# No git commit = user retains control
```

**Loop prevention**:
```python
# Skip automation for doc-only commits
if commit_msg.startswith("docs: auto-update"):
    exit(0)
```

### Performance Budget

- Pre-commit: <2 sec (blocks user)
- Post-commit: <5 sec (user waits)
- Post-merge: <10 sec (batch OK)

**Optimizations**:
- Skip commits with no relevant files
- Background processing (non-blocking)
- Incremental (only new commits)
- Caching (reuse analysis results)

### Implementation Files

1. **`.githooks/post-commit`** (new) - Main automation trigger
2. **`.githooks/lib/commit_analyzer.py`** (new) - Core analysis engine
3. **`.githooks/lib/status_updater.py`** (new) - STATUS.md automation
4. **`.githooks/lib/pattern_detector.py`** (new) - CLAUDE.md intelligence
5. **`.githooks/lib/skill_matcher.py`** (new) - Skill synchronization
6. **`.githooks/config.json`** (new) - User control settings

### Trade-offs

**Advantages**:
- ✅ STATUS.md always current (Git State auto-updated)
- ✅ Zero manual overhead (runs on every commit)
- ✅ Patterns captured (design decisions, conventions)
- ✅ Historical accuracy (derived from git, not memory)

**Disadvantages**:
- ❌ Heuristics not perfect (may miss patterns)
- ❌ Requires review (drafts, not auto-commits)
- ❌ Performance cost (5 seconds per commit)
- ❌ Maintenance (tune heuristics over time)

**Automation Levels**:
- **Conservative**: Git State only auto-updated
- **Balanced** (RECOMMENDED): Git State auto, everything else drafted
- **Aggressive**: Everything auto-committed (not recommended)

---

## Tier 3: Plan Mode Integration

### Overview
Make every plan explicitly include STATUS.md/CLAUDE.md updates as deliverables and specify commit boundaries throughout work.

### Enhanced Plan Template

**Location**: `~/.claude/plan-templates/default.md` (new)

**Structure**:
```markdown
# [Feature Name] - Implementation Plan

## Context Baseline
**STATUS.md current state**: [One-line summary]
**CLAUDE.md patterns**: [Relevant existing patterns]
**Active session**: [.session/feature/X if exists]

## Implementation Phases

### Phase 1: [Name] (est. Xm)
**What**: [Implementation work]
**Commit point**: YES/NO + message if yes
**Context update**: NONE | STATUS | CLAUDE | BOTH
  - If STATUS: What to document
  - If CLAUDE: What pattern to capture

[Repeat for each phase]

## Context Deliverables (REQUIRED)

### STATUS.md Updates
**When**: After phases [X, Y]
**What to document**:
- Completion entry with date
- Key decisions
- Next steps

### CLAUDE.md Updates
**Trigger**: IF new patterns emerged
**Patterns to consider**: [List]
**Action**: Add to [section] OR extract to skill

### Skills Review
**Check if**: Work creates reusable patterns (≥3 uses)
**Candidate patterns**: [List if any]
**Action**: Extract OR document in CLAUDE.md

## Commit Boundaries (DISTRIBUTED)

| After Phase | Type | Message | Push |
|-------------|------|---------|------|
| Phase 1 | feat | Add X service | NO |
| Phase 3 | test | Add tests | NO |
| Phase 4 | docs | Update STATUS.md | YES |

## Verification Checklist
- [ ] All phases implemented
- [ ] STATUS.md updated
- [ ] CLAUDE.md updated (if needed)
- [ ] Skills extracted (if ≥3 patterns)
- [ ] Commits at boundaries
- [ ] Working tree clean
```

### When to Update What

**STATUS.md** - Update when:
- Feature/lesson completes (completion entry)
- Major phase completes (progress entry)
- Blocked on something (blocker entry)
- Multi-day work resumes

**CLAUDE.md** - Update when:
- New project-wide pattern emerges
- Architecture decision made
- Development workflow changes
- Anti-pattern discovered

**Skills** - Extract when:
- Pattern used ≥3 times across different contexts
- Generic enough for other projects
- Non-trivial enough to forget

### Example: Before vs After

**BEFORE**:
```
## Implementation
1. Backend service (30m)
2. Frontend UI (30m)

## Commits
1. feat(backend): add service
2. feat(frontend): add UI
```

**AFTER**:
```
## Phase 1: Backend (30m)
Commit: YES - feat(backend): add service
Context: NONE

## Phase 2: Frontend (30m)
Commit: YES - feat(frontend): add UI
Context: NONE

## Phase 3: Finalize (15m)
Commit: YES - docs: update STATUS.md
Context: STATUS (completion entry)

## Context Deliverables
- STATUS.md: Add completion after Phase 3
- CLAUDE.md: Check if storage pattern novel
- Skills: Review if ≥3 uses

## Verification Checklist
- [ ] All phases done
- [ ] STATUS.md updated
- [ ] 3 commits created
```

**Result**: Logical commits throughout, STATUS.md stays current, patterns captured

### Implementation Files

1. **`~/.claude/plan-templates/default.md`** (new) - Enhanced template
2. **`~/.claude/commands/review-skills-from-plan.md`** (new) - Skill extraction automation
3. **`~/.claude/CLAUDE.md`** (modify) - Document pattern as default
4. **Plan mode system prompt** (optional, high risk) - Enforce context sections

### Trade-offs

**Advantages**:
- ✅ Completeness (all work in plan)
- ✅ Better git history (logical commits)
- ✅ Pattern discoverability (documented)
- ✅ Future resumability (context current)

**Disadvantages**:
- ❌ Slightly more verbose plans
- ❌ More upfront planning overhead
- ❌ Requires discipline

**Mitigation**: Keep terse (bullets not prose), becomes automatic after 2-3 uses, verification checklist enforces

---

## Implementation Roadmap

### Phase 1: Hook-Based Context (Week 1)
**Priority**: HIGH - Immediate behavior improvement

**Tasks**:
1. Create `~/.claude/hooks/inject-context.py`
   - Intent classification (code, planning, debug, git)
   - STATUS.md parsing (first 100 lines)
   - CLAUDE.md parsing (first 5KB)
   - Context injection (Tier 1 + Tier 2)

2. Update `~/.claude/hooks/hooks.json`
   - Register inject-context hook
   - Test doesn't conflict with inject-sessions

3. Update rulesets
   - `~/.claude/CLAUDE.md`: Add "Context Verification Protocol"
   - `.claude/CLAUDE.md`: Add "Required Reading"

4. Test & tune
   - Run on 10 prompts across intents
   - Verify execution time <100ms
   - Tune keywords based on false positives

**Success Criteria**:
- Hook runs on every prompt without errors
- Context visible at top of responses
- Claude mentions checking context in >40% responses (week 1 baseline)

**Estimated Time**: 4-6 hours

---

### Phase 2: Git Automation - STATUS.md (Week 2)
**Priority**: MEDIUM - Maintenance automation

**Tasks**:
1. Create commit analyzer
   - `.githooks/lib/commit_analyzer.py`
   - Pattern detection (protocols, services, migrations)
   - Significance classification

2. Create STATUS updater
   - `.githooks/lib/status_updater.py`
   - Git State auto-update
   - Recent Completions draft generation
   - Versioned backups

3. Create post-commit hook
   - `.githooks/post-commit`
   - Orchestrate automation
   - Background processing
   - Loop prevention

4. Test with last 10 commits
   - Git State updates correctly
   - Completions drafted appropriately
   - No infinite loops
   - Performance <5 seconds

**Success Criteria**:
- Git State section always current
- Completion drafts generated for multi-commit sequences
- No accidental overwrites (backups working)
- User approves draft quality

**Estimated Time**: 6-8 hours

---

### Phase 3: Git Automation - CLAUDE.md & Skills (Week 3)
**Priority**: LOW - Nice to have

**Tasks**:
1. Create pattern detector
   - `.githooks/lib/pattern_detector.py`
   - Design decision extraction (body >100 chars)
   - Convention detection (3+ occurrences)
   - CLAUDE.md draft generation

2. Create skill matcher
   - `.githooks/lib/skill_matcher.py`
   - File path → skill mapping
   - Pattern relevance detection
   - Skill update draft generation

3. Integration
   - Update post-commit to call detectors
   - Create `.claude/context-updates/` directory
   - Test draft quality

**Success Criteria**:
- Design decisions drafted when body >100 chars
- Conventions detected after 3+ commits
- Skill update drafts include examples
- User finds drafts valuable

**Estimated Time**: 6-8 hours

---

### Phase 4: Plan Mode Integration (Week 4)
**Priority**: MEDIUM - Process improvement

**Tasks**:
1. Create plan template
   - `~/.claude/plan-templates/default.md`
   - Context Baseline section
   - Commit Boundaries table
   - Verification Checklist

2. Trial run
   - Use on 2-3 small features
   - Gather friction points
   - Refine sections

3. Optional automation
   - `/review-skills-from-plan` command
   - Post-plan verification hook

4. Document pattern
   - Update `~/.claude/CLAUDE.md`
   - Make default for future plans

**Success Criteria**:
- Plans include context deliverables
- Commits at logical boundaries
- STATUS.md updated consistently
- Zero manual reminders

**Estimated Time**: 4-6 hours

---

## Expected Outcomes

### Week 1 (Hooks)
- Claude checks context: 15% → 40%
- Pattern violations: 8-10/week → 5-6/week
- User corrections: 10-12/week → 6-8/week

### Week 2 (Git Automation - STATUS)
- STATUS.md updated within: 1 week → 1 day
- Git State accuracy: Manual → Always current
- Completion entries: Missing → Drafted

### Week 3 (Git Automation - CLAUDE & Skills)
- CLAUDE.md growth: 0-1/month → 2-3/week
- Skills extracted: 0/month → 1-2/month
- Pattern documentation: Ad-hoc → Systematic

### Week 4 (Plan Mode)
- Context updates in plans: 0% → 100%
- Commits per feature: 1-2 → 3-5
- Manual reminders: 5-10/week → 0/week

### After 4 Weeks (Combined)
- Claude checks context: 15% → 60-70% (4x improvement)
- Pattern violations: 8-10/week → 2-3/week (70% reduction)
- User corrections: 10-12/week → 3-4/week (65% reduction)
- STATUS.md staleness: 1 week → <1 day (7x improvement)
- Context documentation: Manual → Mostly automated

---

## Critical Files Summary

### Tier 1 (Hooks)
1. `~/.claude/hooks/inject-context.py` - Context injection engine
2. `~/.claude/hooks/hooks.json` - Hook registration
3. `~/.claude/CLAUDE.md` - Personal ruleset enhancement
4. `.claude/CLAUDE.md` - Project ruleset enhancement

### Tier 2 (Git Automation)
5. `.githooks/post-commit` - Main trigger
6. `.githooks/lib/commit_analyzer.py` - Analysis engine
7. `.githooks/lib/status_updater.py` - STATUS.md automation
8. `.githooks/lib/pattern_detector.py` - CLAUDE.md intelligence
9. `.githooks/lib/skill_matcher.py` - Skill synchronization
10. `.githooks/config.json` - Configuration

### Tier 3 (Plan Mode)
11. `~/.claude/plan-templates/default.md` - Enhanced template
12. `~/.claude/commands/review-skills-from-plan.md` - Skill extraction

---

## Additional Research Item

**Video reviewed**: https://www.youtube.com/watch?v=JdJE6_OU3YA
- Topic: AI memory systems architecture
- Speaker's thesis: "AI systems are stateless by design but useful intelligence requires state"
- **Status**: ✅ Reviewed (2025-01-24)
- **Verdict**: Strongly validates our 3-tier approach, adds critical enhancements

---

## Research Validation: Memory Systems Video Insights

### The 8 Principles of Memory Architecture (Applied to Our Design)

**Video source**: [YouTube](https://www.youtube.com/watch?v=JdJE6_OU3YA)

The speaker outlines why AI memory is "the biggest unsolved problem in AI" and provides 8 principles for solving it. Here's how they validate and enhance our design:

#### 1. Memory is Architecture, Not a Feature
**Their principle**: "Don't wait for vendors to solve this - you need to design it yourself"
**Our implementation**: ✅ 3-tier system (hooks + git + plan mode) is architectural, not waiting for Claude Code features

#### 2. Separate by Lifecycle, Not Convenience
**Their principle**: "Personal preferences (permanent) ≠ project facts (temporary) ≠ session state (ephemeral)"
**Our implementation**: ✅ Already separated:
- `~/.claude/CLAUDE.md` (personal-permanent)
- `.claude/STATUS.md` (project-temporary)
- `.session/feature/*` (ephemeral)

#### 3. Match Storage to Query Pattern
**Their principle**: "Different questions need different retrieval - key-value, structured, semantic, event logs"
**Our implementation**: ✅ Multiple stores:
- CLAUDE.md rules (key-value)
- STATUS.md sections (structured)
- Skills (semantic patterns)
- Git history (event logs)

#### 4. Mode-Aware Context Beats Volume
**Their principle**: "Planning needs breadth, execution needs precision - retrieval must match task type"
**Our implementation**: ✅ Hook intent detection (planning/code/debug/git) injects mode-specific context

#### 5. Build Portable First
**Their principle**: "Memory must survive vendor/tool/model changes"
**Our implementation**: ✅ Markdown + git = portable across any AI system

#### 6. Compression is Curation
**Their principle**: "Do not upload 40 pages hoping AI extracts what matters - you do the compression work"
**Our implementation**: ✅ Hooks inject summaries (first 100 lines), not full files; git automation drafts for human curation

#### 7. Retrieval Needs Verification
**Their principle**: "Semantic search recalls well but fails on specifics - pair fuzzy retrieval with exact verification"
**Our implementation**: ⚠️ Partial - hooks recall (inject summaries), Claude verifies (reads files), but not explicit

#### 8. Memory Compounds Through Structure
**Their principle**: "Random accumulation creates noise - structured memory compounds without degradation"
**Our implementation**: ✅ Structured: STATUS.md (chronological), CLAUDE.md (principles), skills (patterns)

---

## Enhancements from Video Insights

### Enhancement 1: State Delta Awareness (NEW)

**Problem**: "What changed since last time" is crucial for relevance but not surfaced
**Video insight**: "Relevance changes based on state delta - what's new since you last talked"

**Implementation**: Add to Tier 1 hooks

**Updated injection** (Tier 1):
```
═══ CONTEXT CHECKPOINT ═══
Project: agent-spike | Updated: 2025-11-24
Phase: Personal AI Research Assistant

Since last session (2025-01-23):
├─ 12 commits (feat: 8, fix: 2, docs: 2)
├─ New: SurrealDB PatternTracker complete
├─ Changed: URL filtering migrated to async
└─ Active: 2 sessions (mentat, message-bus)

📋 STATUS.md - Current state, blockers, next steps
📖 CLAUDE.md - Project patterns, architecture
🎯 VISION.md - Long-term roadmap

⚠️ CHECK BEFORE CHANGES: What's changed?
═══════════════════════════
```

**Code changes**:
```python
def get_state_delta(status_md: Path, git_dir: Path) -> dict:
    """Extract what changed since last Claude session."""

    # Read last session timestamp from cache
    cache = git_dir / ".claude" / ".last-session"
    last_session = read_timestamp(cache) if cache.exists() else "1 day ago"

    # Git commits since then
    commits = git("log", f"--since={last_session}", "--oneline", "--format=%s")
    commit_count = len(commits.split('\n'))

    # Categorize commits
    feat_count = len([c for c in commits if c.startswith('feat')])
    fix_count = len([c for c in commits if c.startswith('fix')])
    docs_count = len([c for c in commits if c.startswith('docs')])

    # Parse STATUS.md for recent completions
    recent = extract_recent_completion(status_md)

    # Active sessions
    sessions = list((git_dir / ".session" / "feature").iterdir())

    return {
        "commit_count": commit_count,
        "feat": feat_count,
        "fix": fix_count,
        "docs": docs_count,
        "recent_completion": recent,
        "active_sessions": [s.name for s in sessions]
    }
```

**Update cache after each session**:
```python
# In inject-context.py, after generating context
cache_file = Path(cwd) / ".claude" / ".last-session"
cache_file.write_text(datetime.now().isoformat())
```

---

### Enhancement 2: Forgetting as Technology (NEW)

**Problem**: STATUS.md accumulates indefinitely, older entries become noise
**Video insight**: "Human memory uses forgetting as technology - lossy compression with importance weighting"

**Solution**: Automatic archival of old STATUS.md entries

**Implementation**: Add to Tier 2 git automation

**New file**: `.githooks/lib/status_archiver.py`

```python
def archive_old_entries(status_md: Path, archive_md: Path, age_threshold_days: int = 90):
    """
    Move STATUS.md entries older than threshold to archive.

    Keeps STATUS.md focused on recent work (last 3 months).
    Archived entries still retrievable if needed.
    """

    # Parse STATUS.md into dated sections
    sections = parse_dated_sections(status_md)

    cutoff = datetime.now() - timedelta(days=age_threshold_days)

    # Separate recent from old
    recent = [s for s in sections if s.date > cutoff]
    old = [s for s in sections if s.date <= cutoff]

    if not old:
        return  # Nothing to archive

    # Backup before modifying
    backup_file(status_md)

    # Write recent to STATUS.md
    with open(status_md, 'w') as f:
        f.write(format_sections(recent))
        f.write(f"\n---\n\n**Older entries**: See STATUS_ARCHIVE.md\n")

    # Append old to STATUS_ARCHIVE.md
    with open(archive_md, 'a') as f:
        f.write(f"\n## Archived {datetime.now().strftime('%Y-%m')}\n\n")
        f.write(format_sections(old))

    # Stage changes
    git("add", str(status_md), str(archive_md))
```

**Trigger**: Monthly cron job or manual command

```bash
# Add to Makefile
archive-status:
	uv run python .githooks/lib/status_archiver.py

# Or git hook: post-commit (runs monthly check)
```

**Lifecycle metadata** (add to STATUS.md sections):

```markdown
## Recent Completions (Lifecycle: temporary, archive: 3 months)

**URL Pattern Analytics** ✅ COMPLETE (2025-01-24)
- [details]
```

---

### Enhancement 3: Explicit Two-Stage Retrieval (IMPROVED)

**Problem**: Hooks inject summaries but don't force verification step
**Video insight**: "Recall candidates, then verify against ground truth"

**Solution**: Make verification explicit in hook output

**Updated Tier 1 injection**:

```
🔨 CODE MODIFICATION DETECTED

Found 3 relevant context entries:
├─ STATUS.md line 45: Current phase (SurrealDB migration)
├─ CLAUDE.md line 120: Service pattern (protocol-first)
└─ git log: Last 5 commits touch this area

⚠️ VERIFICATION REQUIRED:
1. Read STATUS.md lines 45-60 for phase details
2. Read CLAUDE.md lines 120-150 for service pattern
3. Review git diff for recent changes

RESPOND: "Verified [file:line] - [specific finding]" before code.
```

**Force specificity**:
- Not "Checked STATUS.md" (vague)
- But "Verified STATUS.md:45 - Phase 4 complete, Phase 5 starting" (specific)

---

### Enhancement 4: Lifecycle Metadata (NEW)

**Problem**: No explicit markers for how long context should persist
**Video insight**: "Separate by lifecycle - permanent vs temporary vs ephemeral"

**Solution**: Add lifecycle metadata to sections

**Format**:
```markdown
## Section Name
**Lifecycle**: permanent | temporary | ephemeral
**Review**: quarterly | monthly | after-completion
**Archive**: never | 3-months | 1-year
```

**Examples**:

```markdown
## Development Philosophy
**Lifecycle**: permanent (applies to all projects)
**Review**: quarterly
**Archive**: never

---

## Current Phase: SurrealDB Migration
**Lifecycle**: temporary (project-specific)
**Review**: weekly
**Archive**: 3-months after completion

---

## Active Session: mentat
**Lifecycle**: ephemeral (single feature)
**Review**: per-session
**Archive**: after merge
```

**Git automation enhancement**: Detect lifecycle and auto-archive accordingly

---

### Enhancement 5: Memory Compounding Metrics (NEW)

**Problem**: No way to measure if memory is actually compounding
**Video insight**: "Memory compounds through structure - measure the accumulation"

**Metrics to track**:

```markdown
## Memory Health (Auto-generated monthly)

**Status as of 2025-01-24**:

Structure metrics:
├─ STATUS.md entries: 24 (last 3 months)
├─ CLAUDE.md patterns: 18 documented
├─ Skills: 3 project, 15 personal
└─ Archived entries: 47 (still retrievable)

Compounding metrics:
├─ Patterns reused: 12 (referenced 3+ times)
├─ Decisions stable: 15 (unchanged 6+ months)
├─ Lessons applied: 8 (prevented duplicate work)
└─ Context check rate: 64% (up from 15% baseline)

Quality indicators:
├─ Pattern violations: 2/week (was 10/week)
├─ User corrections: 3/week (was 12/week)
├─ Stale context: <1 day (was 1 week)
└─ Coverage: 94% (work has context)
```

**Generate monthly with**:
```bash
make memory-health
```

---

## Updated Implementation Roadmap

### Phase 1: Hook-Based Context (Week 1) - ENHANCED
**Priority**: HIGH - Immediate behavior improvement

**Tasks**:
1. Create `~/.claude/hooks/inject-context.py`
   - Intent classification (code, planning, debug, git)
   - STATUS.md parsing (first 100 lines)
   - CLAUDE.md parsing (first 5KB)
   - **NEW**: State delta calculation (commits since last session)
   - **NEW**: Explicit two-stage retrieval prompts
   - Context injection (Tier 1 + Tier 2)

2. Update `~/.claude/hooks/hooks.json`
   - Register inject-context hook
   - Test doesn't conflict with inject-sessions

3. **NEW**: Session timestamp tracking
   - `.claude/.last-session` file updated after each interaction
   - Used to calculate "since last session" delta

4. Update rulesets
   - `~/.claude/CLAUDE.md`: Add "Context Verification Protocol"
   - `.claude/CLAUDE.md`: Add "Required Reading"

5. Test & tune
   - Run on 10 prompts across intents
   - Verify execution time <100ms
   - Tune keywords based on false positives
   - **NEW**: Verify state delta accuracy

**Success Criteria**:
- Hook runs on every prompt without errors
- Context visible at top of responses
- **NEW**: State delta shows relevant changes
- **NEW**: Claude verifies specific lines (not vague "checked file")
- Claude mentions checking context in >40% responses (week 1 baseline)

**Estimated Time**: 6-8 hours (was 4-6, added 2 hours for enhancements)

---

### Phase 2: Git Automation - STATUS.md (Week 2) - ENHANCED
**Priority**: MEDIUM - Maintenance automation

**Tasks**:
1. Create commit analyzer
   - `.githooks/lib/commit_analyzer.py`
   - Pattern detection (protocols, services, migrations)
   - Significance classification

2. Create STATUS updater
   - `.githooks/lib/status_updater.py`
   - Git State auto-update
   - Recent Completions draft generation
   - Versioned backups
   - **NEW**: Lifecycle metadata preservation

3. **NEW**: Create STATUS archiver
   - `.githooks/lib/status_archiver.py`
   - Archive entries older than 3 months
   - Move to STATUS_ARCHIVE.md
   - Keep STATUS.md focused on recent work

4. Create post-commit hook
   - `.githooks/post-commit`
   - Orchestrate automation
   - Background processing
   - Loop prevention

5. **NEW**: Monthly archival task
   - Add to cron or manual `make archive-status`
   - Run archiver on STATUS.md

6. Test with last 10 commits
   - Git State updates correctly
   - Completions drafted appropriately
   - No infinite loops
   - Performance <5 seconds
   - **NEW**: Archival doesn't lose context

**Success Criteria**:
- Git State section always current
- Completion drafts generated for multi-commit sequences
- No accidental overwrites (backups working)
- User approves draft quality
- **NEW**: STATUS.md stays under 500 lines (archived rest)

**Estimated Time**: 8-10 hours (was 6-8, added 2 hours for archival)

---

### Phase 3: Git Automation - CLAUDE.md & Skills (Week 3) - SAME

No changes from original plan.

**Estimated Time**: 6-8 hours

---

### Phase 4: Plan Mode Integration (Week 4) - ENHANCED
**Priority**: MEDIUM - Process improvement

**Tasks**:
1. Create plan template
   - `~/.claude/plan-templates/default.md`
   - Context Baseline section
   - **NEW**: State delta section (what changed since last plan)
   - Commit Boundaries table
   - Verification Checklist

2. **NEW**: Add lifecycle metadata to templates
   - Prompts for lifecycle classification
   - Archive triggers

3. Trial run
   - Use on 2-3 small features
   - Gather friction points
   - Refine sections

4. Optional automation
   - `/review-skills-from-plan` command
   - Post-plan verification hook

5. Document pattern
   - Update `~/.claude/CLAUDE.md`
   - Make default for future plans

**Success Criteria**:
- Plans include context deliverables
- Commits at logical boundaries
- STATUS.md updated consistently
- **NEW**: Lifecycle metadata included
- Zero manual reminders

**Estimated Time**: 5-7 hours (was 4-6, added 1 hour for lifecycle metadata)

---

### Phase 5: Memory Health Tracking (NEW - Week 5)
**Priority**: LOW - Measurement

**Tasks**:
1. Create memory health analyzer
   - `.githooks/lib/memory_health.py`
   - Parse STATUS.md, CLAUDE.md, skills
   - Calculate metrics (structure, compounding, quality)

2. Generate monthly report
   - Add to Makefile: `make memory-health`
   - Output to `.claude/MEMORY_HEALTH.md`

3. Track baseline and improvements
   - Week 1: Baseline metrics
   - Monthly: Updated metrics
   - Quarterly: Trend analysis

**Success Criteria**:
- Monthly report generated automatically
- Shows compounding (patterns reused, lessons applied)
- Tracks quality improvements (violations down, check rate up)

**Estimated Time**: 3-4 hours

---

## Updated Expected Outcomes

### Week 1 (Hooks + State Delta)
- Claude checks context: 15% → 45% (better than 40% due to state delta)
- Pattern violations: 8-10/week → 4-6/week (better than 5-6 due to verification)
- User corrections: 10-12/week → 5-7/week (better than 6-8)
- **NEW**: State awareness: "What changed" mentioned in 70% of responses

### Week 2 (Git Automation - STATUS + Archival)
- STATUS.md updated within: 1 week → 1 day
- Git State accuracy: Manual → Always current
- Completion entries: Missing → Drafted
- **NEW**: STATUS.md length: 500+ lines → <500 lines (rest archived)
- **NEW**: Context focus: All time → Last 3 months

### Week 3 (Git Automation - CLAUDE & Skills)
- CLAUDE.md growth: 0-1/month → 2-3/week
- Skills extracted: 0/month → 1-2/month
- Pattern documentation: Ad-hoc → Systematic

### Week 4 (Plan Mode + Lifecycle)
- Context updates in plans: 0% → 100%
- Commits per feature: 1-2 → 3-5
- Manual reminders: 5-10/week → 0/week
- **NEW**: Lifecycle clarity: Unknown → Explicit in all sections

### Week 5 (Memory Health)
- **NEW**: Memory health tracked monthly
- **NEW**: Compounding measured (patterns reused, lessons applied)
- **NEW**: Quality trends visible

### After 5 Weeks (Combined)
- Claude checks context: 15% → 65-75% (was 60-70%, improved by enhancements)
- Pattern violations: 8-10/week → 1-2/week (was 2-3, improved by verification)
- User corrections: 10-12/week → 2-3/week (was 3-4, improved by state delta)
- STATUS.md staleness: 1 week → <1 day
- STATUS.md focus: All time → Last 3 months (rest archived, retrievable)
- Context documentation: Manual → Mostly automated
- **NEW**: Memory compounding: Measurable monthly
- **NEW**: Portability: Markdown + git = vendor-independent

---

## Updated Critical Files Summary

### Tier 1 (Hooks) - ENHANCED
1. `~/.claude/hooks/inject-context.py` - Context injection engine + state delta
2. `~/.claude/hooks/hooks.json` - Hook registration
3. `~/.claude/CLAUDE.md` - Personal ruleset enhancement
4. `.claude/CLAUDE.md` - Project ruleset enhancement
5. **NEW**: `.claude/.last-session` - Session timestamp tracking

### Tier 2 (Git Automation) - ENHANCED
6. `.githooks/post-commit` - Main trigger
7. `.githooks/lib/commit_analyzer.py` - Analysis engine
8. `.githooks/lib/status_updater.py` - STATUS.md automation
9. **NEW**: `.githooks/lib/status_archiver.py` - Archival automation
10. `.githooks/lib/pattern_detector.py` - CLAUDE.md intelligence
11. `.githooks/lib/skill_matcher.py` - Skill synchronization
12. `.githooks/config.json` - Configuration
13. **NEW**: `.claude/STATUS_ARCHIVE.md` - Archived entries

### Tier 3 (Plan Mode) - ENHANCED
14. `~/.claude/plan-templates/default.md` - Enhanced template + lifecycle metadata
15. `~/.claude/commands/review-skills-from-plan.md` - Skill extraction

### Tier 4 (Memory Health) - NEW
16. **NEW**: `.githooks/lib/memory_health.py` - Health analyzer
17. **NEW**: `.claude/MEMORY_HEALTH.md` - Monthly reports

---

## Key Insights from Memory Systems Research

**Most important validation**: Our 3-tier approach aligns with the 8 principles of memory architecture from active research.

**Most important addition**: State delta tracking ("what changed since last time") dramatically improves relevance.

**Most important technique**: "Forgetting as technology" via archival keeps STATUS.md focused on recent work.

**Speaker's challenge**: "If you solve memory now, you have an agentic AI edge. Memory compounds through structure."

**Our answer**: We're building exactly that - structured, portable, mode-aware memory that compounds without degradation.

---

## Final Assessment

**Will this work?** Yes, with realistic expectations.

**What it solves**:
- Stale STATUS.md → Automated updates from git
- Stale CLAUDE.md → Automated pattern detection
- Claude ignoring context → Forced visibility via hooks
- Missing patterns → Systematic extraction
- Plans without context → Template enforcement

**What it doesn't solve**:
- 100% compliance (Claude is probabilistic)
- Zero manual review (drafts need approval)
- Perfect pattern detection (heuristics have limits)

**Success depends on**:
1. Hook implementation quality (fast, accurate)
2. STATUS.md maintenance (kept current)
3. User reinforcement (correct Claude when it skips)
4. Iteration (tune based on data)

**Recommendation**: Build in phases, measure each, proceed if valuable.

**Total Estimated Time**: 20-28 hours over 4 weeks

---

**End of Plan**
