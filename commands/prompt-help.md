---
description: Documentation for prompt engineering techniques
argument-hint: [all|meta-prompting|recursive-review|deep-analyze|multi-perspective|deliberate-detail|reasoning-scaffold|temperature-simulation]
model: haiku
---

# Prompt Engineering Help

Display comprehensive documentation for advanced prompting techniques.

Invoke the `prompt-engineering` skill to access technique details and templates.

## Process

- **Parse ARG**: Determine if requesting all techniques (empty, "all", "help") or specific technique
- **Invoke Skill**: Call prompt-engineering skill to retrieve documentation
- **Display Content**: Show overview or technique details with templates, use cases, and examples

## Valid Technique Names

| Technique | Purpose |
|-----------|---------|
| `meta-prompting` | Reverse prompting: Claude designs the optimal prompt |
| `recursive-review` | 3-pass iterative refinement for quality |
| `deep-analyze` | Chain of verification + adversarial review for evaluation |
| `multi-perspective` | Multi-persona debate for decision-making |
| `deliberate-detail` | Exhaustive detail with no summarization |
| `reasoning-scaffold` | Structured step-by-step template |
| `temperature-simulation` | Multiple confidence levels for analysis |

## Output Format

- **All techniques** (`/optimize-prompt help`): Overview table, selection guide, quick examples
- **Specific technique** (`/optimize-prompt deep-analyze`): Template, use cases, examples, combinations

## Related Commands
- `/optimize-prompt [techniques] <prompt>` - Apply techniques to transform prompts
- `/optimize-prompt help` - Redirects here for documentation