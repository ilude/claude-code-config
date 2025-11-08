---
name: ruleset-optimization
description: Guidelines for optimizing Claude rulesets and instruction files (CLAUDE.md, settings.json) using context efficiency principles. Includes strategies for skill extraction, progressive disclosure, token savings calculation, and deduplication. Manually invoke when optimizing rulesets, reducing context size, extracting content to skills, or improving ruleset organization.
---

# Ruleset Optimization Guidelines

This skill provides comprehensive guidelines for optimizing Claude rulesets to minimize context usage while maximizing effectiveness.

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

## Prioritization Framework

### Token Savings Calculation

1. **Calculate extraction value**
   - Count tokens in section to be moved
   - Estimate usage frequency (always/sometimes/rarely)
   - Calculate savings: tokens × (1 - usage_frequency)

2. **Priority thresholds**
   - High-impact: 500+ tokens, used <50% of time
   - Medium-impact: 200-500 tokens, used <30% of time
   - Low-impact: <200 tokens or used >70% of time

3. **Report efficiency gains**
   - Before: X tokens baseline
   - After: Y tokens baseline, Z with skills (when needed)
   - Savings: (X - Y) tokens baseline (N% reduction)

## Content Classification

### Move to Skills (Procedural "How-To")
- Step-by-step procedures
- Domain-specific workflows
- Tool usage patterns
- Complex decision trees
- Language/framework-specific rules
- Optional best practices

### Keep in CLAUDE.md (Policy "What/Why")
- Core values and principles
- Always-applicable preferences
- Security requirements
- File operation policies
- Communication style
- Project structure overview

## Deduplication Strategy

### Personal vs Project Rulesets
- **Personal** (~/.claude/CLAUDE.md): Universal defaults
- **Project** (.claude/CLAUDE.md): Project-specific overrides
- Never duplicate content between them
- Project ruleset always takes precedence

### Across Skills
- Each skill should have clear, non-overlapping scope
- Reference other skills rather than duplicating content
- Use skill dependencies when logical flow requires it

## Creating Effective Skills

### Structure Template
```markdown
---
name: skill-name
description: Clear description of when to activate and what it contains.
---

# Skill Title

Brief introduction and purpose.

## Core Content
[Domain-specific guidance]
```

### Activation Patterns
**Auto-activation triggers:**
- File patterns: .py, package.json, Dockerfile
- Git operations: commit, push, version control
- Project structure: directories, files present

**Manual invocation:**
- Slash commands: /optimize-prompt, /commit
- Explicit requests: "optimize this ruleset"

## Extraction Decision Tree

```
Is content >200 tokens?
├─ No → Keep in CLAUDE.md
└─ Yes → Is it procedural?
    ├─ No → Keep in CLAUDE.md (policy)
    └─ Yes → Is it used <70% of sessions?
        ├─ No → Keep in CLAUDE.md (always needed)
        └─ Yes → Extract to skill (saves tokens)
```

## Anti-Patterns to Avoid

❌ **Over-extraction:** Don't create skills for tiny sections (<100 tokens)
❌ **Under-referencing:** Always add reference when removing content
❌ **Duplication:** Never duplicate between personal/project or across skills
❌ **Poor organization:** Don't mix multiple domains in one skill

## Optimization Impact Examples

**Before:** 6,000 tokens baseline (all loaded)
**After:** 4,000 tokens baseline + 1,500 tokens in skills (selective)
**Result:** 33% baseline reduction, 25-33% typical session savings

**Compound benefits:**
- Optimization helps ALL projects using shared skills
- Clearer organization improves maintainability
- Faster context loading and better reasoning
- More room for project-specific context

## Maintenance Guidelines

### Regular Review
- Quarterly token usage review
- Check for new extraction opportunities
- Verify skill activation patterns
- Remove stale or unused skills

### Skill Evolution
- Update content as practices evolve
- Merge overlapping skills
- Split skills >1000 tokens
- Archive deprecated skills with notes

---

**This skill is manually invoked when optimizing rulesets or organizing Claude instructions.**

For command usage, see:
- `/optimize-ruleset` - Analyze and optimize current ruleset
- `/analyze-permissions` - Review permission patterns