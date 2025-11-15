---
description: Analyze skill activation patterns and suggest trigger improvements (project, gitignored)
model: haiku
---

# Skill Activation Analyzer

Analyze conversation history for skill activation patterns. Detect missed activations and suggest improvements to trigger criteria.

## Execution Workflow

### 1. Run Analyzer
Execute skill-analyzer.py script with checkpoint mode (analyzes only new messages since last run):

```bash
python ~/.claude/scripts/skill-analyzer.py --json ./tmp/analyze-skills-temp.json --checkpoint --verbose
```

**Checkpoint behavior:**
- First run: Analyzes all messages in history.jsonl
- Subsequent runs: Only analyzes new messages since last run
- Reset mode: Use `--reset` flag to re-analyze everything

If script doesn't exist, inform user and exit.

### 2. Read & Parse Results
Load JSON output from temp file. Extract:
- Statistics (total skills, activated, missed)
- Suggestions (missed activations with evidence)

### 3. Load Existing Skills
Read all SKILL.md files from `~/.claude/skills/` to show current activation patterns.

### 4. Present Missed Activations
Group suggestions by skill. For each missed activation, display:
- Skill name
- Evidence (file touched, import used, error encountered)
- Line number where activation should have occurred
- Current activation patterns
- Suggested new patterns
- Confidence level (high/medium/low)

Format:
```
## Missed Activations (N)

### [skill-name]
Evidence: [what triggered the detection]
Line: [message number]
Current triggers:
  - [existing pattern 1]
  - [existing pattern 2]
Suggested additions:
  - [new pattern suggestion]
Confidence: HIGH
```

### 5. Offer Update Options
Present 4 choices:
1. Update high-confidence suggestions only (confidence=high)
2. Update all suggestions
3. Select individually (ask for each skill)
4. Skip all updates

### 6. Update Skill Files
For each skill to update:
- Read SKILL.md file
- Find "**Auto-activates when**:" section
- Append new trigger patterns to the list
- Write back to file
- Create backup: SKILL.md.backup

If no "Auto-activates when" section exists:
- Add section after description
- Insert new patterns

### 7. Report & Cleanup
Display summary:
- Skills updated: N
- Patterns added: M
- Files modified: [list of SKILL.md files]

Remove temp JSON file.

Suggest re-running command after making changes to see if patterns improve.

## Pattern Categories

| Confidence | Criteria | Example |
|-----------|----------|---------|
| **HIGH** | Direct file match | Working with `tools/services/youtube/` |
| **MEDIUM** | Import pattern match | Importing from `tools.services.*` |
| **LOW** | Error pattern match | When proxy errors occur |

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Script not found | Analyzer missing | Verify ~/.claude/scripts/skill-analyzer.py exists |
| No history.jsonl | No conversation data | Claude Code needs to run to generate history |
| No suggestions | All skills activating correctly | Skills are working as expected |
| JSON parse error | Corrupted output | Check ./tmp/analyze-skills-temp.json |
| Skill file not writable | Permission issue | Verify write permissions on ~/.claude/skills/ |
| No skills loaded | Skills directory missing | Check ~/.claude/skills/ exists |

## Safety Notes

- Always create .backup files before modifying SKILL.md
- Only suggest patterns that appeared in actual conversation
- Don't suggest overly broad patterns (e.g., "*.py")
- Respect existing skill structure and formatting
- Skip system/builtin skills (only update user/project skills)

## Example Output

```
# Skill Activation Analysis

## Statistics
- Total skills: 15
- Skills activated: 8
- Missed activations: 4
- Messages analyzed: 234

## Missed Activations (4)

### agent-spike-project
Evidence: Created update_archives_with_timestamps.py
Line: 234
Current triggers:
  - Working with `tools/` directory
  - Importing from `tools.services.*`
Suggested additions:
  - Working with `projects/*/scripts/` directory
Confidence: HIGH

### python-workflow
Evidence: Discussed uv sync --all-groups
Line: 156
Current triggers:
  - Working with Python files (.py)
Suggested additions:
  - Discussing package management commands (uv, pip, poetry)
Confidence: MEDIUM

Options:
1. Update high-confidence suggestions (2 patterns)
2. Update all suggestions (4 patterns)
3. Select individually
4. Skip

Your choice (1-4):
```

## Notes

- Run periodically (weekly) to improve skill activation accuracy
- Checkpoint tracks what's been analyzed - only scans new messages on each run
- Use `--reset` flag to re-analyze all messages (ignores checkpoint)
- High-confidence patterns are usually safe to auto-apply
- Medium/low confidence should be reviewed before applying
- This is a meta-learning tool - skills improve based on real usage
- Checkpoint stored at `~/.claude/.checkpoints/skill-analyzer.json`
