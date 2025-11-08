---
name: prompt-engineering
description: Advanced prompting techniques for transforming basic prompts into structured, high-quality prompts. Provides 7 techniques with templates. Manually invoke via /optimize-prompt or /prompt-help commands.
---

# Prompt Engineering Skill

Advanced prompting techniques based on "The Mental Models of Master Prompters" - scaffolding reasoning processes, not magic words.

## Technique Selection Decision Tree

```
Prompt Pattern → Recommended Technique
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Analysis/evaluation ("analyze", "assess") → deep-analyze
Decision/choice ("choose", "vs", "which") → multi-perspective
Vague/unclear (<10 words, no specifics) → meta-prompting
Explanation ("explain", "how", "what") → deliberate-detail OR reasoning-scaffold
Improvement ("optimize", "better") → recursive-review
Design/create ("design", "build") → meta-prompting,reasoning-scaffold
Risk/security (security terms) → deep-analyze
Complex/multi-part (multiple "and") → reasoning-scaffold + context
Default/unsure → meta-prompting
```

## Token Cost Reference

| Technique | Multiplier | Worth It When |
|-----------|------------|---------------|
| meta-prompting | 1.5-2x | Need optimal prompt design |
| recursive-review | 1.5-2x | Building reusable templates |
| deep-analyze | 2-3x | High-stakes decisions |
| multi-perspective | 3-4x | Complex trade-offs |
| deliberate-detail | 2-3x | Learning/documentation |
| reasoning-scaffold | 1.5-2x | Need reproducible thinking |
| temperature-simulation | 2x | Confidence calibration critical |

## Technique Templates

### 1. meta-prompting
**Best for**: Unfamiliar domains, maximum quality, vague prompts

```
You're an expert prompt designer.

Task: {BASE_PROMPT}

Design the single most effective prompt to achieve this. Consider:
- What context is essential vs optional?
- What output format would be optimal?
- What reasoning steps should be explicit?
- What constraints prevent bad outputs?
- What examples would eliminate ambiguity?
- What verification steps ensure quality?

Then execute that designed prompt.
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
Provide thorough analysis of the topic.

Phase 2: Chain of Verification
Now verify your analysis systematically:

1. **Incompleteness Check**: Identify 3 specific ways your analysis might be incomplete or biased
   - What perspectives are missing?
   - What data sources weren't considered?
   - What assumptions are implicit?

2. **Challenging Evidence**: Cite specific evidence that challenges or contradicts your conclusions
   - Counter-examples
   - Alternative interpretations
   - Conflicting data

3. **Revised Findings**: Based on verification, revise your analysis
   - What changed?
   - What strengthened?
   - What new uncertainties emerged?

4. **Confidence Calibration**: Rate confidence (0-100%) with detailed justification
   - What would increase confidence?
   - What are the key uncertainties?

Phase 3: Adversarial Review
Attack your revised analysis:

1. **Identify 5 Failure Modes**: Specific ways your analysis could be wrong
   - For each: Likelihood (Low/Med/High) and Impact (1-10 scale)

2. **Prioritize Top 3 Vulnerabilities**: Which failures matter most?

3. **Mitigations**: How could you strengthen the analysis?

Phase 4: Final Synthesis
Provide:
- Core findings (with confidence levels)
- Key uncertainties (what we don't know)
- Recommended actions (given uncertainty)
- Follow-up questions (to improve confidence)

Be self-critical. If verification doesn't find problems, the analysis wasn't rigorous enough.
```

### 4. multi-perspective
**Best for**: Complex trade-offs, stakeholder alignment, exploring options

```
{BASE_PROMPT}

Approach through multi-persona debate with conflicting priorities.

Setup: Define 3 Expert Personas

Identify 3 experts with genuinely conflicting priorities:

**Persona 1**: [Name/Role]
- Primary Priority: [What they optimize for]
- Background: [Relevant expertise]

**Persona 2**: [Name/Role]
- Primary Priority: [MUST conflict with Persona 1]
- Background: [Relevant expertise]

**Persona 3**: [Name/Role]
- Primary Priority: [MUST conflict with 1 and 2]
- Background: [Relevant expertise]

Round 1: Opening Arguments
Each persona presents their perspective and proposed solution:
- **Persona 1**: [Why their priority matters most, recommended approach]
- **Persona 2**: [Why their priority matters most, recommended approach]
- **Persona 3**: [Why their priority matters most, recommended approach]

Round 2: Critiques
Each persona critiques the other two approaches:
- **Persona 1 Critiques**: Problems with Persona 2 and 3's approaches
- **Persona 2 Critiques**: Problems with Persona 1 and 3's approaches
- **Persona 3 Critiques**: Problems with Persona 1 and 2's approaches

Round 3: Refinement & Compromise
Each responds to critiques and identifies compromise:
- **Persona 1**: How critiques change their view, one area for compromise
- **Persona 2**: How critiques change their view, one area for compromise
- **Persona 3**: How critiques change their view, one area for compromise

Synthesis:
- Points of Agreement: [What all personas agree on]
- Irreconcilable Differences: [Where compromise isn't possible]
- Recommended Balanced Solution: [Integrated approach]
- Sensitivity Analysis: If X priority dominates, choose Y approach

Personas must have genuine tension. If they agree too quickly, they're not realistic.
```

### 5. deliberate-detail
**Best for**: Learning complex topics, comprehensive documentation

```
{BASE_PROMPT}

Do NOT summarize. Do NOT be concise.

For every point you make, provide:
- **Implementation details**: How exactly it works (step-by-step)
- **Edge cases**: Where it breaks or behaves unexpectedly
- **Failure modes**: What goes wrong and why
- **Historical context**: Why it exists, what problem it solved, what it replaced
- **Trade-offs**: What you sacrifice by choosing this approach
- **Alternatives**: What other approaches exist and why they weren't chosen

Prioritize completeness over brevity. Expand every concept fully.
I need exhaustive depth, not an executive summary.
```

### 6. reasoning-scaffold
**Best for**: Systematic decisions, reproducible analysis

```
{BASE_PROMPT}

Follow this structured reasoning approach:

Step 1: Core Question
What is the fundamental question being asked?
[Answer here]

Step 2: Key Components
What are the essential variables, entities, or components?
[List and define each]

Step 3: Relationships
What relationships or dependencies exist between components?
[Describe interactions]

Step 4: Possible Approaches
What are 3-5 possible approaches or solutions?
[For each: Description, Pros, Cons]

Step 5: Decision Criteria
What criteria should guide selection?
[Define criteria with relative weights/importance]

Step 6: Optimal Approach
Which approach is optimal and why?
[Justify selection against criteria from Step 5]

Step 7: Risk Analysis
What could go wrong?
[Identify risks and mitigation strategies]

Step 8: Final Recommendation
Clear recommendation with confidence level (0-100%)
[State recommendation, confidence %, justification]
```

### 7. temperature-simulation
**Best for**: Confidence calibration, catching mistakes

```
{BASE_PROMPT}

Provide two responses at different confidence levels, then synthesize:

Response 1 - Junior Analyst Perspective (Uncertain, Over-Explains)
Approach as someone less experienced would:
- Use hedged language and caveats
- Explain basic concepts step-by-step
- Be uncertain about conclusions
- Over-explain reasoning
[Junior's response]

Response 2 - Senior Expert Perspective (Confident, Direct)
Approach as a domain expert would:
- Bottom-line up front
- Assume domain knowledge
- State conclusions directly
- Be concise and telegraphic
[Expert's response]

Synthesis - Balanced Integration
Synthesize both perspectives:
- What does the junior catch that the expert glosses over?
- What does the expert see that the junior misses?
- What's the appropriately-calibrated answer?
[Integrated response with appropriate confidence]
```

## Technique Combinations

**Powerful combinations**:
- `meta-prompting,recursive-review` - Design optimal prompt, then refine
- `deep-analyze,multi-perspective` - Rigorous analysis from multiple angles
- `reasoning-scaffold,deliberate-detail` - Structured exploration with full detail
- `multi-perspective,reasoning-scaffold` - Multiple viewpoints with systematic comparison

**Apply in order**: meta-prompting → recursive-review → deep-analyze → multi-perspective

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| Over-engineering | deep-analyze for "syntax of X" | Match complexity to importance |
| Template rigidity | Following steps blindly | Adapt/skip irrelevant steps |
| Verification theater | Finding nothing wrong | Genuine critique required |
| Persona stereotyping | Generic "lawyer vs cowboy" | Specific realistic priorities |
| Missing synthesis | Just listing perspectives | Must integrate views |

## Effectiveness Indicators

✅ **Strong prompt transformation:**
- Analysis finds genuine problems/gaps
- Personas have real tension/conflict
- Confidence varies appropriately
- Verification changes conclusions
- Multiple approaches genuinely differ

❌ **Weak transformation:**
- Verification finds no issues
- All personas basically agree
- Junior/senior perspectives identical
- No real constraints added
- Going through motions without depth

## Integration Notes

**Command usage**:
- `/optimize-prompt [techniques] <prompt>` - Apply techniques
- `/prompt-help [technique]` - View documentation

**Auto-selection**: Command uses decision tree above when no techniques specified.

**Token awareness**: Each technique multiplies tokens. Balance value vs cost.

**Philosophy**: These techniques scaffold reasoning processes. They work by structuring how Claude thinks about problems, not through special keywords.