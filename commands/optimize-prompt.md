# Optimize Prompt

Transform a basic prompt into an enhanced prompt using advanced prompting techniques.

**Action**: Invoke the `prompt-engineering` skill to access technique templates.

---

## Instructions

**Input format**: `{ARG}`

The input can be:
- `[techniques] <prompt>` - Specific techniques requested (comma-separated)
- `<prompt>` - No techniques specified (you'll select intelligently)

**Your task:**

1. **Invoke the skill**:
   - Use the Skill tool: `prompt-engineering`
   - This loads all technique templates and selection guidelines

2. **Parse the input**:
   - Extract techniques (if specified) and base prompt
   - If no techniques: Use skill's selection guidelines to choose appropriate technique(s)

3. **Apply technique(s)**:
   - Use the templates from the skill
   - Construct the enhanced prompt following the template structure

4. **Provide output** in this format:

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

---

## Examples

**Example 1**: `deep-analyze "Evaluate JWT security"`
→ Apply deep-analyze template from skill

**Example 2**: `"Choose between PostgreSQL and MongoDB"`
→ Identify as decision prompt, select multi-perspective, apply template

**Example 3**: `meta-prompting,reasoning-scaffold "Design a cache"`
→ Apply both templates in sequence

---

**Key difference from basic prompting**: These techniques add structure (verification, perspectives, reasoning scaffolds) that dramatically improves output quality, at the cost of 1.5-4x more tokens.
