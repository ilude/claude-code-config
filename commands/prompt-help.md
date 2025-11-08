---
description: Documentation for prompt engineering techniques
argument-hint: [all|meta-prompting|recursive-review|deep-analyze|multi-perspective|deliberate-detail|reasoning-scaffold|temperature-simulation]
model: haiku
---

# Prompt Engineering Help

Display comprehensive documentation for advanced prompting techniques.

Invoke the `prompt-engineering` skill to access technique details and templates.

## Process

### Step 1: Parse ARG
Determine if user wants:
- All techniques overview (empty, "all", or "help")
- Specific technique documentation (technique name)

### Step 2: Invoke Skill
```
Use Skill tool: prompt-engineering
```

### Step 3: Display Requested Content

#### If ARG is empty, "all", or "help"
Display from skill:
1. Overview of all 7 techniques
2. Selection decision tree
3. Token cost comparison table
4. Combination recommendations
5. Quick command examples

#### If ARG is specific technique
Display from skill:
1. Technique name and category
2. Purpose and best use cases
3. Token cost multiplier
4. Full template with placeholders
5. When Claude auto-selects this technique
6. Example usage
7. Good combinations with other techniques
8. Anti-patterns to avoid

## Valid Technique Names
- `meta-prompting` - Reverse prompting (Claude designs optimal prompt)
- `recursive-review` - 3-pass iterative refinement
- `deep-analyze` - Chain of verification + adversarial review
- `multi-perspective` - Multi-persona debate
- `deliberate-detail` - Exhaustive detail, no summarization
- `reasoning-scaffold` - Structured step-by-step template
- `temperature-simulation` - Multiple confidence levels

## Output Format Examples

### All Techniques Overview
```
PROMPT ENGINEERING TECHNIQUES

1. meta-prompting (1.5-2x tokens)
   Best for: Vague prompts, unfamiliar domains

2. recursive-review (1.5-2x tokens)
   Best for: Building reusable templates

[Continue for all 7...]

SELECTION GUIDE
- Analysis/evaluation → deep-analyze
- Decision/choice → multi-perspective
[...]

USAGE
/optimize-prompt "your prompt"
/optimize-prompt deep-analyze "your prompt"
```

### Specific Technique
```
TECHNIQUE: deep-analyze

Category: Self-Correction Systems
Token Cost: ~2-3x standard prompt
Best For:
- High-stakes decisions
- Security analysis
- Confidence calibration

TEMPLATE
[Show full template from skill]

WHEN TO USE
Claude auto-selects when prompt contains:
- "analyze", "evaluate", "assess"
- Security or risk topics
- High-stakes decisions

EXAMPLE
/optimize-prompt deep-analyze "Evaluate JWT security"
```

## Related Commands
- `/optimize-prompt [techniques] <prompt>` - Apply techniques to transform prompts
- `/optimize-prompt help` - Redirects here for documentation