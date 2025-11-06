---
name: ruleset-optimization
description: Guidelines for optimizing Claude rulesets and instruction files (CLAUDE.md, settings.json) using context efficiency principles. Includes strategies for skill extraction, progressive disclosure, token savings calculation, and deduplication. Manually invoke when optimizing rulesets, reducing context size, extracting content to skills, or improving ruleset organization.
---

# Ruleset Optimization Guidelines

This skill provides comprehensive guidelines for optimizing Claude rulesets and instruction files to minimize context usage while maximizing effectiveness.

## Context Efficiency Philosophy

**PRIMARY GOAL**: Minimize baseline context, maximize signal-to-noise ratio.

Context efficiency is THE most important optimization principle. Every token counts.

### Core Strategy

1. **Use skills for domain-specific rules** (git, python, web, containers)
   - Only loaded when relevant (file patterns, project structure)
   - 30-70% context reduction when inactive
   - Progressive disclosure of detailed procedures

2. **Keep CLAUDE.md minimal**
   - Project overview and purpose (essential context)
   - Quick start checklist
   - Project-specific patterns not covered by skills
   - References to skills for details

3. **Progressive disclosure wins**
   - Baseline = always-needed info only (~20% of content)
   - Details = loaded on-demand via skills (~80% of content)
   - Result: Faster responses, better reasoning

## When Optimizing Rulesets

### Prioritization Framework

1. **Calculate token savings from skill extraction**
   - Count tokens in section to be moved
   - Estimate how often section is needed (always/sometimes/rarely)
   - Calculate savings: tokens × (1 - usage_frequency)

2. **Prioritize moves that save >100 tokens**
   - High-impact: 500+ tokens, used <50% of time
   - Medium-impact: 200-500 tokens, used <30% of time
   - Low-impact: <200 tokens or used >70% of time

3. **Report context efficiency gains**
   - Before: X tokens baseline
   - After: Y tokens baseline, Z with skills (when needed)
   - Savings: (X - Y) tokens baseline (N% reduction)

### Content Classification

**Move to Skills (procedural "how-to"):**
- Step-by-step procedures
- Domain-specific workflows
- Tool usage patterns
- Complex decision trees
- Language/framework-specific rules
- Optional best practices

**Keep in CLAUDE.md (policy "what/why"):**
- Core values and principles
- Always-applicable preferences
- Security requirements
- File operation policies
- Communication style
- Project structure overview

### Deduplication Strategy

**Personal vs Project Rulesets:**
- Personal ruleset (~/.claude/CLAUDE.md): Universal defaults
- Project ruleset (.claude/CLAUDE.md): Project-specific overrides
- Never duplicate content between them
- Project ruleset always takes precedence

**Across Skills:**
- Each skill should have clear, non-overlapping scope
- Reference other skills rather than duplicating content
- Use skill dependencies when logical flow requires it

## Creating New Skills

### Skill Structure

```markdown
---
name: skill-name
description: Clear description of when to activate, what it contains, and manual/auto activation triggers.
---

# Skill Title

Brief introduction and purpose.

## Section 1: Core Content
...

## Section 2: Additional Details
...
```

### Activation Patterns

**Auto-activation (file/project patterns):**
- Git operations: git commit, push, version control
- Python projects: .py files, pyproject.toml, requirements.txt
- Web projects: package.json, React, Next.js
- Container projects: Dockerfile, docker-compose.yml

**Manual invocation (commands):**
- Slash commands: `/optimize-prompt`, `/commit`, `/analyze-permissions`
- Explicit requests: "optimize this ruleset", "help with prompting"

### Naming Conventions

- Use kebab-case for skill directories
- SKILL.md for the main file (consistent with existing skills)
- Include version/date in description if content is time-sensitive

## Optimization Workflow

### Step 1: Analyze Current State

1. Read the full CLAUDE.md or project ruleset
2. Identify distinct sections/topics
3. Count approximate tokens per section
4. Estimate usage frequency for each section

### Step 2: Identify Candidates

Look for sections that are:
- Domain-specific (git, python, docker, etc.)
- Procedural (step-by-step instructions)
- Large (>200 tokens)
- Conditionally needed (<70% of sessions)
- Duplicated between personal/project rulesets

### Step 3: Extract to Skills

1. Create skill directory: `~/.claude/skills/skill-name/`
2. Write SKILL.md with proper frontmatter
3. Include activation description in frontmatter
4. Move content from ruleset to skill
5. Test activation triggers

### Step 4: Update Ruleset References

Replace extracted section with:
```markdown
## Section Title

**Guidelines have been moved to a skill for context efficiency.**

The `skill-name` skill contains:
- Brief bullet list of what's included
- Quick highlights

**Activation:** [auto/manual] - when [trigger description]

**Quick reference:**
- Key point 1
- Key point 2

See `~/.claude/skills/skill-name/SKILL.md` for complete guidelines.
```

### Step 5: Verify and Document

1. Test that skill activates correctly
2. Ensure no broken references
3. Calculate token savings
4. Update CHANGELOG.md with optimization details

## Example Impact

**Before optimization:**
- CLAUDE.md: 6,000 tokens baseline
- All content loaded every session
- Slower responses, more context pollution

**After optimization:**
- CLAUDE.md: 4,000 tokens baseline (33% reduction)
- Skills: 1,500 tokens additional when activated
- Total with all skills: 5,500 tokens (still 8% savings)
- Most sessions: 4,000-4,500 tokens (25-33% savings)

**Compound benefits:**
- Optimization helps ALL projects using shared skills
- Clearer organization improves maintainability
- Faster context loading and better reasoning
- More room for project-specific context

## Common Optimization Patterns

### Pattern 1: Language/Framework Workflow
**Extract:** Python workflow, JavaScript/Node.js workflow, Docker workflow
**Keep:** General code quality preferences, file operation policies

### Pattern 2: Tool-Specific Guidelines
**Extract:** Git workflow, pytest usage, npm/yarn preferences
**Keep:** Security requirements, commit policies

### Pattern 3: Project Type Patterns
**Extract:** Multi-agent AI projects, web projects, container projects
**Keep:** Project structure overview, session management

### Pattern 4: Advanced Techniques
**Extract:** Prompt engineering, optimization strategies
**Keep:** Basic communication style, core preferences

## Anti-Patterns to Avoid

❌ **Over-extraction:**
- Don't create skills for tiny sections (<100 tokens)
- Don't split highly cohesive content
- Don't create skills for always-needed content

❌ **Under-referencing:**
- Don't remove section without adding reference
- Don't lose context about what skill contains
- Don't forget activation triggers in reference

❌ **Duplication:**
- Don't duplicate between personal/project rulesets
- Don't duplicate across multiple skills
- Don't duplicate between ruleset and skill reference

❌ **Poor organization:**
- Don't mix multiple domains in one skill
- Don't create overly broad skills
- Don't create overlapping activation triggers

## Maintenance

### Regular Review
- Quarterly review of token usage
- Check for new extraction opportunities
- Verify skill activation patterns work correctly
- Remove stale or unused skills

### Skill Evolution
- Update skill content as practices evolve
- Merge skills if scopes overlap
- Split skills if they grow too large (>1000 tokens)
- Archive deprecated skills with notes

### Documentation
- Keep CHANGELOG.md updated with optimizations
- Document token savings from each change
- Note lessons learned for future optimizations
- Share patterns across projects

---

**This skill is manually invoked when optimizing rulesets or organizing Claude instructions.**

For command usage, see:
- `/optimize-ruleset` - Analyze and optimize current ruleset
- `/analyze-permissions` - Review permission patterns
