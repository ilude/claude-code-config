---
name: prompt-engineering
description: Advanced prompting techniques for transforming basic prompts into structured, high-quality prompts. Provides 7 techniques with templates. Manually invoke via /optimize-prompt or /prompt-help commands.
---

# Prompt Engineering Skill

Advanced prompting techniques based on "The Mental Models of Master Prompters" - scaffolding reasoning processes, not magic words.

## Selection Guide

| Pattern | Technique | Token Cost |
|---------|-----------|------------|
| Analysis/evaluation | deep-analyze | 2-3x (high-stakes) |
| Decision/choice | multi-perspective | 3-4x (complex trade-offs) |
| Vague/unclear | meta-prompting | 1.5-2x (optimal design) |
| Explanation | deliberate-detail, reasoning-scaffold | 2-3x, 1.5-2x |
| Improvement | recursive-review | 1.5-2x (reusable templates) |
| Design/create | meta-prompting, reasoning-scaffold | 1.5-2x |
| Risk/security | deep-analyze | 2-3x |
| Complex/multi-part | reasoning-scaffold | 1.5-2x (reproducible) |
| Confidence calibration | temperature-simulation | 2x |

## Technique Templates

### 1. meta-prompting
**Best for**: Unfamiliar domains, maximum quality, vague prompts

```
You're an expert prompt designer.

Task: {BASE_PROMPT}

Design the optimal prompt considering:
- Essential context vs optional
- Optimal output format
- Explicit reasoning steps needed
- Constraints to prevent bad outputs
- Examples to eliminate ambiguity
- Quality verification steps

Execute the designed prompt.
```

### 2. recursive-review
**Best for**: Building reusable templates, debugging prompts

```
{BASE_PROMPT}

Then optimize this through 3 versions:

Version 1: Add missing constraints
- What assumptions are implicit?
- What edge cases aren't covered?
- What outputs are undesirable?
- Add constraints to prevent these.

Version 2: Resolve ambiguities
- What terms need clearer definition?
- What scope is unclear (too broad/narrow)?
- What priorities might conflict?
- Clarify all ambiguities.

Version 3: Enhance reasoning depth
- What reasoning should be made explicit?
- Where would examples help?
- What verification steps should be built in?
- What quality bar should be set?

After all versions, execute the final optimized version.
```

### 3. deep-analyze
**Best for**: High-stakes decisions, security analysis, confidence calibration

```
{BASE_PROMPT}

Phase 1: Initial Analysis
Provide thorough analysis.

Phase 2: Chain of Verification
1. **Incompleteness Check**: 3 ways analysis might be incomplete/biased
2. **Challenging Evidence**: Specific counter-examples, alternative interpretations, conflicting data
3. **Revised Findings**: What changed, strengthened, or introduced new uncertainties
4. **Confidence Calibration**: 0-100% with justification and key uncertainties

Phase 3: Adversarial Review
1. **5 Failure Modes**: Likelihood (L/M/H) and Impact (1-10) for each
2. **Top 3 Vulnerabilities**: Prioritize failures by importance
3. **Mitigations**: Strengthening strategies

Phase 4: Final Synthesis
- Core findings (with confidence levels)
- Key uncertainties
- Recommended actions
- Follow-up questions

Be self-critical. If verification doesn't find problems, analysis wasn't rigorous enough.
```

### 4. multi-perspective
**Best for**: Complex trade-offs, stakeholder alignment, exploring options

```
{BASE_PROMPT}

Define 3 Expert Personas with conflicting priorities:

**Persona 1**: [Name/Role] - Priority: [X] - Background: [Expertise]
**Persona 2**: [Name/Role] - Priority: [Y conflicts with X] - Background: [Expertise]
**Persona 3**: [Name/Role] - Priority: [Z conflicts with X,Y] - Background: [Expertise]

Round 1: Opening Arguments
- **Persona 1**: [Priority justification, recommended approach]
- **Persona 2**: [Priority justification, recommended approach]
- **Persona 3**: [Priority justification, recommended approach]

Round 2: Critiques
- **Persona 1**: [Problems with 2 and 3]
- **Persona 2**: [Problems with 1 and 3]
- **Persona 3**: [Problems with 1 and 2]

Round 3: Refinement
- **Persona 1**: [Response to critiques, compromise area]
- **Persona 2**: [Response to critiques, compromise area]
- **Persona 3**: [Response to critiques, compromise area]

Synthesis:
- Points of Agreement
- Irreconcilable Differences
- Recommended Balanced Solution
- Sensitivity Analysis: If X priority dominates → Y approach

Personas must have genuine tension.
```

### 5. deliberate-detail
**Best for**: Learning complex topics, comprehensive documentation

```
{BASE_PROMPT}

Do NOT summarize or be concise. Provide for every point:
- **Implementation details**: Step-by-step how it works
- **Edge cases**: Where it breaks/behaves unexpectedly
- **Failure modes**: What goes wrong and why
- **Historical context**: Why it exists, what it replaced
- **Trade-offs**: What you sacrifice
- **Alternatives**: Other approaches and why not chosen

Prioritize completeness over brevity.
```

### 6. reasoning-scaffold
**Best for**: Systematic decisions, reproducible analysis

```
{BASE_PROMPT}

Step 1: Core Question
[Fundamental question being asked]

Step 2: Key Components
[Essential variables, entities, components - define each]

Step 3: Relationships
[Dependencies and interactions between components]

Step 4: Possible Approaches
[3-5 approaches with Description, Pros, Cons]

Step 5: Decision Criteria
[Criteria with relative weights/importance]

Step 6: Optimal Approach
[Selection justified against Step 5 criteria]

Step 7: Risk Analysis
[Risks and mitigation strategies]

Step 8: Final Recommendation
[Recommendation, confidence 0-100%, justification]
```

### 7. temperature-simulation
**Best for**: Confidence calibration, catching mistakes

```
{BASE_PROMPT}

Response 1 - Junior Analyst (Uncertain, Over-Explains)
- Hedged language, caveats
- Step-by-step basic concepts
- Uncertain conclusions
[Junior's response]

Response 2 - Senior Expert (Confident, Direct)
- Bottom-line up front
- Assumes domain knowledge
- Concise, telegraphic
[Expert's response]

Synthesis - Balanced Integration
- What junior catches that expert glosses over
- What expert sees that junior misses
- Appropriately-calibrated answer
[Integrated response]
```

## Technique Combinations

- `meta-prompting,recursive-review` - Design then refine
- `deep-analyze,multi-perspective` - Rigorous multi-angle analysis
- `reasoning-scaffold,deliberate-detail` - Structured exploration with depth
- `multi-perspective,reasoning-scaffold` - Multiple viewpoints, systematic comparison
- **Order**: meta-prompting → recursive-review → deep-analyze → multi-perspective

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| Over-engineering | deep-analyze for "syntax of X" | Match complexity to importance |
| Template rigidity | Following steps blindly | Adapt/skip irrelevant steps |
| Verification theater | Finding nothing wrong | Genuine critique required |
| Persona stereotyping | Generic "lawyer vs cowboy" | Specific realistic priorities |
| Missing synthesis | Just listing perspectives | Must integrate views |

## Effectiveness Indicators

**Strong**: Analysis finds real problems, personas conflict, confidence varies, verification changes conclusions, approaches differ
**Weak**: No issues found, personas agree, perspectives identical, no constraints added, superficial application

## Integration Notes

- `/optimize-prompt [techniques] <prompt>` - Apply techniques
- `/prompt-help [technique]` - View documentation
- Auto-selection uses decision tree when techniques unspecified
- Balance token cost vs value
- These scaffold reasoning processes, not magic keywords