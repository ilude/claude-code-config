# Personal Commands Quick Start

**Created**: 2025-11-04
**Updated**: 2025-11-04 (Added project-aware checkpoints)

## What Was Set Up

✅ Personal ruleset: `~/.claude/CLAUDE.md` (231 lines)
✅ Personal commands directory: `~/.claude/commands/`
✅ Optimization command: `/optimize-ruleset` (829 lines) ⭐ **NOW PROJECT-AWARE**
✅ Checkpoint system: **Multi-line format** supporting multiple command types
✅ Documentation: `~/.claude/commands/README.md`

---

## 🎉 NEW: Project-Aware Checkpoint System!

### What Changed

**Before**:
- Single global checkpoint: `~/.claude/CHECKPOINT`
- Analyzed ALL history regardless of project
- Re-analyzed same history for different projects

**After**:
- **Project checkpoints**: `.claude/CHECKPOINT` in each project
- **Personal checkpoint**: `~/.claude/CHECKPOINT` for personal ruleset
- **Multi-line format**: Supports multiple command types
- **Project filtering**: Only analyzes history for current project

### Why This Matters

```
Project A Work:
└─ Checkpoint: agent-spike/.claude/CHECKPOINT
└─ Analyzes: Only history from agent-spike
└─ Learns: Patterns specific to this project

Project B Work:
└─ Checkpoint: other-project/.claude/CHECKPOINT
└─ Analyzes: Only history from other-project
└─ Learns: Patterns specific to that project

Personal Ruleset:
└─ Checkpoint: ~/.claude/CHECKPOINT
└─ Analyzes: History from ALL projects
└─ Learns: Cross-project patterns
```

**Result**: No redundant analysis, faster runs, more relevant patterns!

---

## 🚀 Try It Now!

### Test the /optimize-ruleset Command

**In your current project** (agent-spike):
```bash
/optimize-ruleset
```

**What happens**:
1. Creates `.claude/CHECKPOINT` in this project (if doesn't exist)
2. Analyzes history entries where `project == /c/Projects/Personal/agent-spike`
3. Detects patterns from THIS project only
4. Examines `.claude/CLAUDE.md` in this project
5. Provides recommendations
6. Updates `.claude/CHECKPOINT` with current timestamp

**Optimize personal ruleset**:
```bash
/optimize-ruleset personal
```

**What happens**:
1. Uses `~/.claude/CHECKPOINT` (global)
2. Analyzes history from ALL projects
3. Detects cross-project patterns
4. Examines `~/.claude/CLAUDE.md`
5. Updates `~/.claude/CHECKPOINT`

---

## 📚 Available Commands

### `/optimize-ruleset [personal]`

**Most Powerful Command** - Self-improving meta-learning system with project awareness

**No parameter**: Optimize project ruleset (PROJECT-SPECIFIC ANALYSIS)
```bash
/optimize-ruleset
```
- Target: `.claude/CLAUDE.md` (this project)
- Checkpoint: `.claude/CHECKPOINT` (this project)
- History filter: Only entries from this project

**"personal"**: Optimize personal ruleset (ALL PROJECTS)
```bash
/optimize-ruleset personal
```
- Target: `~/.claude/CLAUDE.md`
- Checkpoint: `~/.claude/CHECKPOINT`
- History filter: All entries from all projects

**Flags**:
- `--no-history`: Skip history analysis
- `--history-only`: Only analyze history, don't modify ruleset

---

## 🎯 Checkpoint System Deep Dive

### Multi-Line Format

**File structure** (supports multiple commands):
```
optimize-ruleset: 2025-11-04T14:47:09Z
commit-command: 2025-11-03T10:00:00Z
other-command: 2025-11-02T15:30:00Z
```

Each command maintains its own checkpoint line. No conflicts!

### File Locations

```
~/.claude/
├── CHECKPOINT                    # For personal ruleset only
│   Content: optimize-ruleset: 2025-11-04T14:47:09Z
└── CLAUDE.md                     # Personal ruleset

/c/Projects/Personal/agent-spike/
├── .claude/
│   ├── CHECKPOINT                # For THIS project (NEW!)
│   │   Content: optimize-ruleset: 2025-11-04T14:47:09Z
│   └── CLAUDE.md                 # Project ruleset

/c/Projects/OtherProject/
├── .claude/
│   ├── CHECKPOINT                # Separate checkpoint!
│   └── CLAUDE.md                 # Different project
```

### History Filtering

**history.jsonl structure**:
```json
{
  "display": "user command",
  "timestamp": 1762266888953,
  "project": "C:\\Projects\\Personal\\agent-spike",
  "sessionId": "..."
}
```

**Project mode filtering**:
```
For entry in history.jsonl:
  IF timestamp > checkpoint
  AND project == current_project_path:
    Include in analysis
```

**Personal mode filtering**:
```
For entry in history.jsonl:
  IF timestamp > checkpoint:
    Include in analysis (any project)
```

---

## 🔄 How the Improvement Loop Works

### Per-Project Learning

```
Monday - Work on agent-spike:
├─ Run: /optimize-ruleset
├─ Analyzes: Only agent-spike history
├─ Learns: uv patterns, lesson structure, etc.
├─ Updates: agent-spike/.claude/CHECKPOINT
└─ Improves: agent-spike/.claude/CLAUDE.md

Tuesday - Work on web-app:
├─ Run: /optimize-ruleset
├─ Analyzes: Only web-app history (independent!)
├─ Learns: npm patterns, React patterns, etc.
├─ Updates: web-app/.claude/CHECKPOINT
└─ Improves: web-app/.claude/CLAUDE.md

Wednesday - Optimize personal ruleset:
├─ Run: /optimize-ruleset personal
├─ Analyzes: History from BOTH projects
├─ Learns: Cross-project patterns
├─ Updates: ~/.claude/CHECKPOINT
└─ Improves: ~/.claude/CLAUDE.md
```

**Result**: Each project evolves independently based on its own work!

---

## 💡 Example: What Gets Learned

### From agent-spike Project

**Pattern 1: Manual .venv Paths** (Project-specific)
```
History shows: Used ../../../.venv/Scripts/python.exe in agent-spike
Context: Project uses uv package manager
Lesson: Use `uv run python` instead
→ Adds rule to agent-spike/.claude/CLAUDE.md (Python section)
```

**Pattern 2: Lesson Structure** (Project-specific)
```
History shows: Work in .spec/lessons/ directories
Context: Learning spike with progressive lessons
Lesson: Always check STATUS.md before starting
→ Adds rule to agent-spike/.claude/CLAUDE.md (Workflow)
```

### From web-app Project

**Pattern 3: npm Scripts** (Different project, different patterns!)
```
History shows: Using npm commands in web-app
Context: Node.js project with package.json
Lesson: Use `npm run` for all scripts
→ Adds rule to web-app/.claude/CLAUDE.md (NOT agent-spike!)
```

### Cross-Project Patterns

**Pattern 4: Git Workflow** (Applies everywhere)
```
History shows: Forgetting to check git status in multiple projects
Context: Occurs across all projects
Lesson: Always check git status before starting work
→ Adds rule to ~/.claude/CLAUDE.md (Personal > Git Workflow)
```

---

## 📁 File Locations

```
~/.claude/                              # Your personal Claude directory
├── CLAUDE.md                          # Personal ruleset (231 lines)
├── CHECKPOINT                         # Personal checkpoint (multi-line)
│   Content: optimize-ruleset: 2025-11-04T14:47:09Z
├── COMMANDS-QUICKSTART.md             # This file
├── history.jsonl                      # Your chat history (~19KB)
└── commands/
    ├── optimize-ruleset.md            # The command (829 lines, updated!)
    ├── commit.md                      # Commit command
    └── README.md                      # Documentation

/c/Projects/Personal/agent-spike/
└── .claude/
    ├── CHECKPOINT                     # Project checkpoint (NEW!)
    │   Content: (will be created on first run)
    └── CLAUDE.md                      # Project ruleset (354 lines)
```

---

## 🔍 What the Command Analyzes

### From History (Meta-Learning with Project Filter)

**Project Mode** (`/optimize-ruleset`):
- ✅ Only analyzes entries where `project == current_directory`
- ✅ Patterns specific to this project
- ✅ Faster (fewer entries to process)
- ✅ More relevant learnings

**Personal Mode** (`/optimize-ruleset personal`):
- ✅ Analyzes entries from all projects
- ✅ Cross-project patterns
- ✅ General best practices
- ✅ Comprehensive insights

**Pattern Detection** (same as before):
- Repeated tool usage mistakes
- Manual path references
- User corrections
- Missing context checks
- Forgotten workflow steps
- TODO list management issues

---

## 🎓 When to Run /optimize-ruleset

**Recommended Frequency**:

### Project Ruleset (`/optimize-ruleset`)
- ✅ After completing a lesson/milestone
- ✅ After frustrating sessions (turn pain into rules!)
- ✅ When discovering project structure
- ✅ Weekly for active projects
- ✅ Before major refactorings

### Personal Ruleset (`/optimize-ruleset personal`)
- ✅ Bi-weekly or monthly
- ✅ When you notice repeated patterns across projects
- ✅ After working on new types of projects
- ✅ To consolidate learnings from multiple projects

---

## 🚦 Usage Examples

### Example 1: First Run on agent-spike
```bash
cd /c/Projects/Personal/agent-spike
/optimize-ruleset

Output:
- No checkpoint found - analyzing ALL history for this project
- Found 47 entries from agent-spike
- Detected: Manual .venv paths, missing Quick Start, etc.
- Created: .claude/CHECKPOINT with timestamp
- Next run will only analyze NEW history
```

### Example 2: Second Run on agent-spike
```bash
cd /c/Projects/Personal/agent-spike
/optimize-ruleset

Output:
- Checkpoint found: 2025-11-04T10:00:00Z
- Analyzing 12 NEW entries since checkpoint
- Detected: 1 new pattern (forgot STATUS.md check)
- Updated: .claude/CHECKPOINT with new timestamp
- Incremental improvement!
```

### Example 3: Different Project
```bash
cd /c/Projects/OtherProject
/optimize-ruleset

Output:
- No checkpoint found (first run for THIS project)
- Analyzing ALL history for other-project
- Independent from agent-spike checkpoint!
- Creates: other-project/.claude/CHECKPOINT
- Learns patterns specific to this project
```

### Example 4: Personal Ruleset
```bash
# From any project
/optimize-ruleset personal

Output:
- Checkpoint: ~/.claude/CHECKPOINT
- Analyzing history from ALL projects
- Found patterns that occur across projects
- Updates personal best practices
```

---

## 🎁 What You Get

### Project-Specific Learning
- Each project learns from its own history
- No redundant analysis of other projects
- Faster, more relevant insights
- Patterns stay contextual

### Cross-Project Learning
- Personal ruleset captures universal patterns
- Best practices that apply everywhere
- Consistent behavior across projects

### Incremental Improvement
- Checkpoint prevents re-analyzing same history
- Each session adds only new insights
- Builds on previous learnings
- Gets smarter over time

---

## 📋 Quick Command Reference

```bash
# Optimize current project (most common)
/optimize-ruleset

# Optimize personal ruleset
/optimize-ruleset personal

# Skip history (faster, just analyze ruleset)
/optimize-ruleset --no-history

# Only analyze history (no changes)
/optimize-ruleset --history-only

# Check project checkpoint
cat .claude/CHECKPOINT

# Check personal checkpoint
cat ~/.claude/CHECKPOINT

# View command details
cat ~/.claude/commands/README.md

# List all commands
ls ~/.claude/commands/
```

---

## 🎯 Try It Now!

**Recommended First Action**:

```bash
# Run on current project
/optimize-ruleset
```

This will:
1. Create `.claude/CHECKPOINT` for this project
2. Analyze history entries from this project only
3. Detect patterns from agent-spike work
4. Show what it learned
5. Update checkpoint for next time

**Expected findings**:
- Manual .venv path usage (we discussed this!)
- Documentation accuracy issues (we fixed these!)
- Missing Quick Start (we added it!)
- Other patterns from today's work

---

## 🔄 Migration Note

**Old checkpoint**: `~/.claude/CHECKPOINT` (single-line format)
**New format**: Multi-line format

The global checkpoint has been converted to multi-line format:
```
Before: 2025-11-04T14:47:09Z
After:  optimize-ruleset: 2025-11-04T14:47:09Z
```

**For project work**: Future runs of `/optimize-ruleset` (no parameter) will create project-specific checkpoints in `.claude/CHECKPOINT`.

**For personal work**: `/optimize-ruleset personal` continues to use `~/.claude/CHECKPOINT`.

---

## ✨ Summary

### Key Improvements

1. **Project-Aware**: Each project tracks its own optimization history
2. **No Redundancy**: Don't re-analyze other projects' history
3. **Faster**: Fewer entries to process per run
4. **More Relevant**: Patterns are project-specific
5. **Extensible**: Multi-line format supports future commands
6. **Independent**: Projects improve independently

### The Power of Project Awareness

```
Without project awareness:
└─ One global checkpoint
└─ Analyzes ALL history every time
└─ Patterns mixed across projects
└─ Slower, less relevant

With project awareness:
└─ Per-project checkpoints
└─ Analyzes only project history
└─ Patterns contextual
└─ Faster, more relevant
```

---

**Questions?** Check:
- `~/.claude/commands/README.md` - Full documentation
- `~/.claude/commands/optimize-ruleset.md` - Complete command logic (829 lines!)
- `~/.claude/CLAUDE.md` - Your personal ruleset

**Happy optimizing!** 🚀

---

**Note**: This is a **meta-learning** system with **project awareness**. Each project learns from its own work and improves independently. The more you use it, the smarter each project becomes!
