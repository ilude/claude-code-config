---
description: Transform prompts using advanced prompting techniques
argument-hint: [help|meta-prompting|recursive-review|deep-analyze|multi-perspective|deliberate-detail|reasoning-scaffold|temperature-simulation] <prompt>
---

# Optimize Prompt

Transform a basic prompt into an enhanced prompt using advanced prompting techniques.

For techniques, templates, and philosophy, see the `prompt-engineering` skill.

## Process Overview
1. Parse input to extract techniques and base prompt
2. Invoke prompt-engineering skill for templates
3. Select technique(s) if not specified
4. Apply template(s) to base prompt
5. Output enhanced prompt with usage notes

## Help Mode

If ARG starts with "help":
1. Direct user to `/prompt-help` command
2. If ARG is "help [technique]", suggest `/prompt-help [technique]`
3. EXIT without optimization

Example response:
```
For comprehensive documentation on prompt engineering techniques, use:
- `/prompt-help` - View all techniques overview
- `/prompt-help deep-analyze` - View specific technique details

Or specify techniques directly:
- `/optimize-prompt meta-prompting "your prompt"`
```

## Normal Optimization Mode

### Step 1: Invoke Skill
```
Use Skill tool: prompt-engineering
```

### Step 2: Parse Input
**Input format**: `{ARG}`

Extract:
- Techniques (if specified before prompt)
- Base prompt (the actual prompt to enhance)

### Step 3: Select Techniques
If no techniques specified, use skill's decision tree:
- Analysis/evaluation → deep-analyze
- Decision/choice → multi-perspective
- Vague/unclear → meta-prompting
- Explanation → deliberate-detail or reasoning-scaffold
- Improvement → recursive-review
- Design/create → meta-prompting,reasoning-scaffold
- Risk/security → deep-analyze
- Default → meta-prompting

### Step 4: Apply Template(s)
1. Get template(s) from skill
2. Replace `{BASE_PROMPT}` placeholder with user's prompt
3. If multiple techniques, apply in logical order

### Step 5: Output Format

```markdown
## Enhanced Prompt

**Original**: {base_prompt}
**Techniques Applied**: {technique_list}
**Why These Techniques**: {brief_explanation}

---

### Ready-to-Use Enhanced Prompt

```
{complete_enhanced_prompt_with_template_applied}
```

---

**Usage Notes**:
- Estimated token cost: ~{multiplier}x original
- Best for: {use_case}
- Would you like me to execute this enhanced prompt now?
```

## Technique Combinations

If multiple techniques specified:
- Apply in order: meta-prompting → recursive-review → deep-analyze → multi-perspective
- Ensure templates don't conflict
- Combine outputs logically

## Token Multipliers

Reference skill for detailed costs. Quick reference:
- meta-prompting: 1.5-2x
- recursive-review: 1.5-2x
- deep-analyze: 2-3x
- multi-perspective: 3-4x
- deliberate-detail: 2-3x
- reasoning-scaffold: 1.5-2x
- temperature-simulation: 2x