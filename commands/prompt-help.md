# Prompt Engineering Help

This command provides help on advanced prompting techniques and the `/optimize-prompt` command.

**Skill activation**: Reference the `prompt-engineering` skill for detailed information.

**Argument**: `{ARG}` (optional - specific technique name for detailed help)

---

## Mode Selection

**If ARG is empty or general**: Show overview of all techniques and usage examples

**If ARG is a technique name**: Show detailed information about that specific technique

Valid technique names:
- `meta-prompting`
- `recursive-review`
- `deep-analyze`
- `multi-perspective`
- `deliberate-detail`
- `reasoning-scaffold`
- `temperature-simulation`

---

## General Help (No Specific Technique)

### Overview

The `/optimize-prompt` command transforms basic prompts into advanced prompts using sophisticated techniques from prompt engineering research.

**Basic usage**:
```bash
# Let Claude choose the best techniques
/optimize-prompt "your prompt here"

# Specify specific technique(s)
/optimize-prompt technique-name "your prompt here"
/optimize-prompt technique1,technique2 "your prompt here"
```

---

### Available Techniques

#### 1. **meta-prompting**
- **Purpose**: Reverse prompting - Claude designs the optimal prompt, then executes it
- **Best for**: Vague prompts, unfamiliar domains, maximum quality
- **Cost**: ~1.5-2x tokens
- **Example**: `/optimize-prompt meta-prompting "Write unit tests"`

#### 2. **recursive-review**
- **Purpose**: Iteratively refine through 3 optimization passes
- **Best for**: Building reusable templates, debugging prompts
- **Cost**: ~1.5-2x tokens
- **Example**: `/optimize-prompt recursive-review "Analyze code quality"`

#### 3. **deep-analyze**
- **Purpose**: Chain of verification + adversarial review
- **Best for**: High-stakes decisions, rigorous analysis, confidence calibration
- **Cost**: ~2-3x tokens
- **Example**: `/optimize-prompt deep-analyze "Evaluate JWT security"`

#### 4. **multi-perspective**
- **Purpose**: Multi-persona debate with conflicting priorities
- **Best for**: Complex trade-off decisions, exploring options
- **Cost**: ~3-4x tokens
- **Example**: `/optimize-prompt multi-perspective "Choose database for microservice"`

#### 5. **deliberate-detail**
- **Purpose**: Exhaustive detail with no summarization
- **Best for**: Learning complex topics, comprehensive documentation
- **Cost**: ~2-3x tokens
- **Example**: `/optimize-prompt deliberate-detail "Explain distributed consensus"`

#### 6. **reasoning-scaffold**
- **Purpose**: Structured step-by-step reasoning template
- **Best for**: Systematic decisions, reproducible analysis
- **Cost**: ~1.5-2x tokens
- **Example**: `/optimize-prompt reasoning-scaffold "Design API architecture"`

#### 7. **temperature-simulation**
- **Purpose**: Multiple confidence levels (uncertain vs confident) then synthesize
- **Best for**: Confidence calibration, catching mistakes
- **Cost**: ~2x tokens
- **Example**: `/optimize-prompt temperature-simulation "Estimate project timeline"`

---

### Quick Selection Guide

**Need verification of analysis?** → `deep-analyze`

**Making a choice/decision?** → `multi-perspective`

**Prompt is vague or unclear?** → `meta-prompting`

**Want structured thinking?** → `reasoning-scaffold`

**Need exhaustive detail?** → `deliberate-detail`

**Refining existing prompt?** → `recursive-review`

**Calibrating confidence?** → `temperature-simulation`

**Not sure?** → Just provide the prompt, Claude will select techniques intelligently

---

### Example Workflows

#### Workflow 1: High-Stakes Technical Decision

```bash
# Start with multi-perspective to explore options
/optimize-prompt multi-perspective "Choose between monorepo and polyrepo"

# Then deep-analyze the recommended approach
/optimize-prompt deep-analyze "Migration path to monorepo strategy"
```

#### Workflow 2: Building Reusable Prompts

```bash
# Optimize a basic prompt
/optimize-prompt meta-prompting "Review code for security issues"

# Refine it further
/optimize-prompt recursive-review "Design API endpoint documentation"

# Save the enhanced prompt as a template
```

#### Workflow 3: Learning Complex Topic

```bash
# Get exhaustive detail
/optimize-prompt deliberate-detail "Explain Raft consensus algorithm"

# Then make a decision with that knowledge
/optimize-prompt multi-perspective "Choose between Raft and Paxos for our use case"
```

---

### Combining Techniques

You can combine multiple techniques for maximum effect:

**Excellent combinations**:
- `meta-prompting,recursive-review` - Design optimal prompt, then refine it
- `deep-analyze,multi-perspective` - Rigorous analysis from multiple angles
- `reasoning-scaffold,deliberate-detail` - Structured exploration with full detail
- `multi-perspective,reasoning-scaffold` - Multiple viewpoints with systematic comparison

**Example**:
```bash
/optimize-prompt deep-analyze,multi-perspective "Migrate to Kubernetes"
```

---

### Token Cost Awareness

These techniques make prompts more powerful but use more tokens:

| Technique | Cost Multiplier | Worth It When... |
|-----------|----------------|------------------|
| meta-prompting | 1.5-2x | Need optimal prompt design |
| recursive-review | 1.5-2x | Building reusable templates |
| deep-analyze | 2-3x | High-stakes decisions |
| multi-perspective | 3-4x | Complex trade-offs |
| deliberate-detail | 2-3x | Learning/documentation |
| reasoning-scaffold | 1.5-2x | Need reproducible thinking |
| temperature-simulation | 2x | Confidence calibration critical |

**Rule of thumb**: Reserve complex techniques for important problems where the token cost is justified by better outcomes.

---

### Getting More Details

For detailed information about a specific technique:
```bash
/prompt-help meta-prompting
/prompt-help deep-analyze
/prompt-help multi-perspective
# etc.
```

For the complete reference:
```bash
# Read the full skill documentation
~/.claude/skills/prompt-engineering/SKILL.md
```

---

## Technique-Specific Help

**If ARG specifies a technique name, provide detailed help for that technique:**

### Help for: {ARG}

**From the prompt-engineering skill, extract and display:**

1. **Purpose**: What this technique does
2. **Category**: Which family it belongs to
3. **Token Cost**: Expected multiplier
4. **Best For**: When to use this technique
5. **Template Preview**: Show the template structure
6. **When to Suggest**: Indicators that suggest this technique
7. **Example Usage**: Concrete example with input/output
8. **Combinations**: What other techniques work well with this
9. **Anti-Patterns**: What to avoid when using this

---

### Example: /prompt-help deep-analyze

```markdown
## Technique: deep-analyze

**Category**: Self-Correction Systems
**Purpose**: Chain of verification + adversarial review for rigorous analysis

**Token Cost**: ~2-3x standard prompt

**Best For**:
- High-stakes decisions requiring confidence
- Fact-heavy topics prone to errors
- Security, risk, or compliance analysis
- When you need explicit uncertainty quantification

**How It Works**:
1. **Phase 1**: Initial thorough analysis
2. **Phase 2**: Chain of Verification
   - Find 3 ways analysis might be incomplete
   - Cite challenging evidence
   - Revise findings
   - Calibrate confidence
3. **Phase 3**: Adversarial Review
   - Identify 5 failure modes
   - Assess likelihood and impact
   - Recommend mitigations
4. **Phase 4**: Synthesis with confidence levels

**Example Usage**:
```bash
/optimize-prompt deep-analyze "Evaluate the security implications of using JWT tokens"
```

**Enhanced Prompt Output**:
The command will produce a prompt with all 4 phases explicitly structured, forcing systematic verification and adversarial thinking.

**Combines Well With**:
- `multi-perspective` - For rigorous multi-angle analysis
- `reasoning-scaffold` - For structured deep analysis

**Anti-Patterns to Avoid**:
- Don't use for simple factual questions
- Verification must find real issues (not theater)
- Don't skip the adversarial phase

**When Claude Suggests This**:
- You use words like "analyze", "evaluate", "assess", "review"
- Security or risk topics
- High-stakes technical decisions

**Learn More**: See `~/.claude/skills/prompt-engineering/SKILL.md` for full template and examples.
```

---

### Example: /prompt-help multi-perspective

```markdown
## Technique: multi-perspective

**Category**: Perspective Engineering
**Purpose**: Multi-persona debate with conflicting priorities

**Token Cost**: ~3-4x standard prompt (highest cost, highest value for complex decisions)

**Best For**:
- Complex trade-off decisions
- Stakeholder alignment challenges
- Exploring solution space thoroughly
- When "right answer" depends on priorities

**How It Works**:
1. **Setup**: Define 3 expert personas with conflicting priorities
2. **Round 1**: Each persona argues their perspective
3. **Round 2**: Each critiques the other two
4. **Round 3**: Each responds and identifies compromise
5. **Synthesis**: Integrated balanced recommendation

**Example Usage**:
```bash
/optimize-prompt multi-perspective "Choose between PostgreSQL and MongoDB"
```

**Enhanced Prompt Output**:
Creates structured debate with 3 experts (e.g., Performance Engineer, Maintainability Architect, Operations Engineer) who have genuinely conflicting priorities.

**Combines Well With**:
- `deep-analyze` - Multi-angle + rigorous verification
- `reasoning-scaffold` - Structured multi-perspective comparison

**Anti-Patterns to Avoid**:
- Personas must have REAL tension (not superficial)
- Don't skip synthesis step
- Avoid stereotype personas ("cautious lawyer" - be specific)

**When Claude Suggests This**:
- You use words like "choose", "decide", "which", "vs", "or"
- Architecture or design decisions
- Process or policy choices
- "Should we..." questions

**Learn More**: See `~/.claude/skills/prompt-engineering/SKILL.md` for full template and examples.
```

---

## Additional Resources

### Full Documentation
**Skill file**: `~/.claude/skills/prompt-engineering/SKILL.md`
- Complete templates for all techniques
- Combination strategies
- Anti-patterns to avoid
- Measuring effectiveness

### Related Commands
**`/optimize-prompt [techniques] <prompt>`**: Transform prompts using these techniques

### Source
These techniques are based on **"The Mental Models of Master Prompters: 10 Techniques for Advanced Prompting"** - a comprehensive guide to advanced prompt engineering.

### Feedback & Questions

These tools are designed to help you get higher-quality outputs from Claude. If you have:
- **Questions**: Ask about specific techniques or use cases
- **Issues**: Report if techniques don't work as expected
- **Ideas**: Suggest new techniques or improvements

---

## Summary

**To optimize a prompt**:
```bash
/optimize-prompt "your prompt"                    # Claude selects techniques
/optimize-prompt technique-name "your prompt"     # You specify technique
/optimize-prompt tech1,tech2 "your prompt"        # Multiple techniques
```

**To learn about techniques**:
```bash
/prompt-help                      # This overview
/prompt-help technique-name       # Specific technique details
```

**To see full reference**:
```bash
# Read: ~/.claude/skills/prompt-engineering/SKILL.md
```

---

**Ready to optimize your prompts? Try `/optimize-prompt` with any prompt you want to enhance!**
