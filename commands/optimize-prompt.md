---
description: Transform prompts using advanced prompting techniques
argument-hint: [help|meta-prompting|recursive-review|deep-analyze|multi-perspective|deliberate-detail|reasoning-scaffold|temperature-simulation] <prompt>
---

# Optimize Prompt

Transform a basic prompt into an enhanced prompt using advanced prompting techniques.

For techniques, templates, and philosophy, see the `structured-analysis` skill.

This command leverages a tiered framework of 12 prompting techniques organized into 3 tiers based on complexity and use case.

## Process
Parse → Select → Apply → Output

## Help Mode

If ARG starts with "help": Direct to `/prompt-help [technique]` and exit without optimization.

## Normal Optimization Mode

### Step 1: Invoke Skill
```
Use Skill tool: structured-analysis
```

### Step 2: Parse Input
**Input format**: `{ARG}`

Extract:
- Techniques (if specified before prompt)
- Base prompt (the actual prompt to enhance)

### Step 3: Select Techniques

| Prompt Type | Technique |
|--|--|
| Analysis/evaluation | deep-analyze |
| Decision/choice | multi-perspective |
| Vague/unclear | meta-prompting |
| Explanation | deliberate-detail, reasoning-scaffold |
| Improvement | recursive-review |
| Design/create | meta-prompting, reasoning-scaffold |
| Risk/security | deep-analyze |
| Default | meta-prompting |

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

If multiple techniques specified, apply in order:
1. meta-prompting
2. recursive-review
3. deep-analyze
4. multi-perspective

## Token Multipliers

| Technique | Cost |
|--|--|
| meta-prompting | 1.5-2x |
| recursive-review | 1.5-2x |
| deep-analyze | 2-3x |
| multi-perspective | 3-4x |
| deliberate-detail | 2-3x |
| reasoning-scaffold | 1.5-2x |
| temperature-simulation | 2x |