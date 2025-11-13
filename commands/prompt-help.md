---
description: Documentation for structured-analysis frameworks
argument-hint: [all|meta-prompting|recursive-review|deep-analyze|multi-perspective|deliberate-detail|reasoning-scaffold|temperature-simulation|adversarial-review|scope-boundary|idempotency-audit|zero-warning-verification|security-first-design|evidence-based-optimization]
model: haiku
---

# Structured Analysis Help

Display comprehensive documentation for structured-analysis frameworks that apply to ANY artifact.

Invoke the `structured-analysis` skill to access framework details and templates.

## Framework Structure

The skill contains **12 frameworks** organized in three tiers:

- **Tier 1: Core 4** - Most commonly used analysis frameworks
- **Tier 2: Auto-Invoke 3** - Applied automatically in relevant contexts
- **Tier 3: On-Demand 5** - Specialized frameworks for specific use cases

## Process

- **Parse ARG**: Determine if requesting all frameworks (empty, "all", "help") or specific framework
- **Invoke Skill**: Call structured-analysis skill to retrieve documentation
- **Display Content**: Show overview or framework details with templates, use cases, and examples

## Valid Framework Names

| Framework | Purpose | Tier |
|-----------|---------|------|
| `meta-prompting` | Reverse prompting: Claude designs the optimal artifact | Tier 1 |
| `recursive-review` | 3-pass iterative refinement for quality | Tier 1 |
| `deep-analyze` | Chain of verification for thorough evaluation | Tier 1 |
| `multi-perspective` | Multi-persona debate for decision-making | Tier 1 |
| `reasoning-scaffold` | Structured step-by-step template | Tier 2 |
| `temperature-simulation` | Multiple confidence levels for analysis | Tier 2 |
| `deliberate-detail` | Exhaustive detail with no summarization | Tier 2 |
| `adversarial-review` | Challenge assumptions and identify weaknesses | Tier 3 |
| `scope-boundary` | Define explicit scope and exclusions | Tier 3 |
| `idempotency-audit` | Verify artifact can be safely re-executed | Tier 3 |
| `zero-warning-verification` | Ensure no warnings or quality issues | Tier 3 |
| `security-first-design` | Identify and address security concerns | Tier 3 |
| `evidence-based-optimization` | Base improvements on concrete data | Tier 3 |

## Output Format

- **All frameworks** (`/optimize-prompt help`): Overview table by tier, selection guide, quick examples
- **Specific framework** (`/optimize-prompt deep-analyze`): Template, use cases, examples, combinations

## Related Commands
- `/optimize-prompt [frameworks] <artifact>` - Apply frameworks to analyze or transform any artifact
- `/optimize-prompt help` - Redirects here for documentation