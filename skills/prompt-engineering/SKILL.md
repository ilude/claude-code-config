# Prompt Engineering Skill

**Purpose**: Advanced prompting techniques for transforming basic prompts into high-quality, structured prompts
**Type**: Reference skill (invoked by `/optimize-prompt` and `/prompt-help` commands)
**Owner**: mglenn
**Created**: 2025-11-05
**Source**: "The Mental Models of Master Prompters: 10 Techniques for Advanced Prompting" (YouTube)

---

## Overview

This skill provides templates and patterns for enhancing prompts using advanced techniques. It is designed to work with the `/optimize-prompt` command, which transforms basic prompts by incorporating these techniques.

**Key principle**: These techniques structure how LLMs reason, verify, and evolve - they're not about "magic words" but about scaffolding the reasoning process.

---

## Available Techniques

### 1. meta-prompting
**Category**: Meta-Prompting
**Purpose**: Reverse prompting - ask the model to design the optimal prompt, then execute it
**Token cost**: ~1.5-2x
**Best for**: Unfamiliar domains, maximum quality output, learning prompt patterns

**Template**:
```
You're an expert prompt designer.

Task: {ORIGINAL_PROMPT}

Design the single most effective prompt to achieve this. Consider:
- What context is essential vs optional?
- What output format would be optimal?
- What reasoning steps should be explicit?
- What constraints prevent bad outputs?
- What examples would eliminate ambiguity?
- What verification steps ensure quality?

Then execute that designed prompt.
```

**When to suggest**:
- Vague or underspecified prompts
- User asking "how do I prompt for X?"
- Need maximum quality with unknown domain

---

### 2. recursive-review
**Category**: Meta-Prompting
**Purpose**: Iteratively refine prompt through 3 focused optimization passes
**Token cost**: ~1.5-2x
**Best for**: Refining complex prompts, debugging poor outputs, building reusable templates

**Template**:
```
{ORIGINAL_PROMPT}

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

**When to suggest**:
- Prompt produces inconsistent results
- Need to build a reusable template
- Prompt has known issues but unclear how to fix

---

### 3. deep-analyze
**Category**: Self-Correction
**Purpose**: Chain of verification + adversarial review for rigorous analysis
**Token cost**: ~2-3x
**Best for**: High-stakes decisions, fact-heavy topics, need confidence calibration

**Template**:
```
{ORIGINAL_PROMPT}

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
Attack your revised analysis aggressively:

1. **Identify 5 Failure Modes**: Specific ways your analysis could be wrong or mislead
   - For each: Likelihood (Low/Med/High) and Impact (1-10 scale)

2. **Prioritize Top 3 Vulnerabilities**: Which failures matter most?

3. **Mitigations**: How could you strengthen the analysis or hedge against failures?

Phase 4: Final Synthesis
Provide:
- Core findings (with confidence levels)
- Key uncertainties (what we don't know)
- Recommended actions (given uncertainty)
- Follow-up questions (to improve confidence)

CRITICAL: Be genuinely self-critical. If verification doesn't find problems, the analysis wasn't rigorous enough.
```

**When to suggest**:
- Analysis or evaluation prompts
- Security, risk, or compliance topics
- High-stakes technical decisions
- User asks for "thorough" or "rigorous" analysis

---

### 4. multi-perspective
**Category**: Perspective Engineering
**Purpose**: Multi-persona debate with conflicting priorities to explore solution space
**Token cost**: ~3-4x
**Best for**: Complex trade-off decisions, stakeholder alignment, exploring options

**Template**:
```
{ORIGINAL_PROMPT}

Approach this through a multi-persona debate with conflicting priorities.

Setup: Define 3 Expert Personas

Identify 3 experts with genuinely conflicting priorities for this problem:

**Persona 1**: [Name/Role]
- Primary Priority: [What they optimize for]
- Background: [Relevant expertise]

**Persona 2**: [Name/Role]
- Primary Priority: [What they optimize for - MUST conflict with Persona 1]
- Background: [Relevant expertise]

**Persona 3**: [Name/Role]
- Primary Priority: [What they optimize for - MUST conflict with 1 and 2]
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
Each persona responds to critiques and identifies potential compromise:
- **Persona 1**: How critiques change their view, one area for compromise
- **Persona 2**: How critiques change their view, one area for compromise
- **Persona 3**: How critiques change their view, one area for compromise

Synthesis:
- Points of Agreement: [What all personas agree on]
- Irreconcilable Differences: [Where compromise isn't possible]
- Recommended Balanced Solution: [Integrated approach addressing key concerns]
- Sensitivity Analysis: If X priority dominates, choose Y approach

CRITICAL: Personas must have genuine tension. If they agree too quickly, they're not realistic.
```

**When to suggest**:
- Decision-making prompts (choose between X and Y)
- "Should we..." questions
- Architecture or design choices
- Process or policy decisions

---

### 5. deliberate-detail
**Category**: Reasoning Scaffolds
**Purpose**: Fight premature compression - demand exhaustive detail
**Token cost**: ~2-3x
**Best for**: Learning complex topics, comprehensive documentation, exploring edge cases

**Template**:
```
{ORIGINAL_PROMPT}

CRITICAL INSTRUCTIONS - Do NOT summarize. Do NOT be concise.

For every point you make, provide:
- **Implementation details**: How exactly it works (step-by-step)
- **Edge cases**: Where it breaks or behaves unexpectedly
- **Failure modes**: What goes wrong and why
- **Historical context**: Why it exists, what problem it solved, what it replaced
- **Trade-offs**: What you sacrifice by choosing this approach
- **Alternatives**: What other approaches exist and why they weren't chosen

Prioritize completeness over brevity. Expand every concept fully.
I need exhaustive depth here, not an executive summary.
```

**When to suggest**:
- User explicitly asks for "detailed" or "comprehensive"
- Learning/educational prompts
- Documentation generation
- Understanding complex systems

---

### 6. reasoning-scaffold
**Category**: Reasoning Scaffolds
**Purpose**: Provide explicit structured template for step-by-step reasoning
**Token cost**: ~1.5-2x
**Best for**: Complex decisions, reproducible reasoning, systematic analysis

**Template**:
```
{ORIGINAL_PROMPT}

Follow this structured reasoning approach:

Step 1: Core Question
What is the fundamental question being asked?
[Answer here]

Step 2: Key Components
What are the essential variables, entities, or components involved?
[List and define each]

Step 3: Relationships
What relationships or dependencies exist between components?
[Describe interactions]

Step 4: Possible Approaches
What are 3-5 possible approaches or solutions?
[For each: Description, Pros, Cons]

Step 5: Decision Criteria
What criteria should guide the selection?
[Define criteria with relative weights/importance]

Step 6: Optimal Approach
Which approach is optimal and why?
[Justify selection against criteria from Step 5]

Step 7: Risk Analysis
What could go wrong with this approach?
[Identify risks and mitigation strategies]

Step 8: Final Recommendation
Clear recommendation with confidence level (0-100%)
[State recommendation, confidence %, justification]
```

**When to suggest**:
- Complex decision-making prompts
- Comparison prompts (X vs Y vs Z)
- Need systematic, reproducible thinking
- Architectural or design decisions

---

### 7. temperature-simulation
**Category**: Perspective Engineering
**Purpose**: Simulate different confidence levels (uncertain vs confident) then synthesize
**Token cost**: ~2x
**Best for**: Calibrating confidence appropriately, catching obvious mistakes, avoiding overconfidence

**Template**:
```
{ORIGINAL_PROMPT}

Provide two different responses at different confidence levels, then synthesize:

Response 1 - Junior Analyst Perspective (Uncertain, Over-Explains)
Approach this topic as someone less experienced would:
- Use hedged language and caveats
- Explain basic concepts step-by-step
- Be uncertain about conclusions
- Over-explain reasoning
[Junior's response]

Response 2 - Senior Expert Perspective (Confident, Direct)
Approach this as a domain expert would:
- Bottom-line up front
- Assume domain knowledge
- State conclusions directly
- Be concise and telegraphic
[Expert's response]

Synthesis - Balanced Integration
Now synthesize both perspectives:
- What does the junior catch that the expert glosses over?
- What does the expert see that the junior misses?
- What's the appropriately-calibrated answer?
[Integrated response with appropriate confidence]
```

**When to suggest**:
- User seems overconfident or underconfident
- Need to check for obvious mistakes
- Calibrating certainty is important
- Novel or unfamiliar domain

---

## Technique Selection Guide

When user provides a prompt without specifying techniques, analyze the prompt and select appropriate technique(s) based on these indicators:

### Analysis/Evaluation Prompts
**Indicators**: "analyze", "evaluate", "assess", "review", "examine"
**Recommend**: `deep-analyze` (always) or `deep-analyze,multi-perspective` (if decision involved)

### Decision/Choice Prompts
**Indicators**: "choose", "select", "decide", "which", "should we", "vs", "or"
**Recommend**: `multi-perspective` (always) or `multi-perspective,reasoning-scaffold` (if complex)

### Vague/Underspecified Prompts
**Indicators**: Very short (< 10 words), no specifics, unclear goal
**Recommend**: `meta-prompting` (let model design better prompt)

### Explanation/Understanding Prompts
**Indicators**: "explain", "how does", "what is", "describe", "learn about"
**Recommend**: `deliberate-detail` (if complex topic) or `reasoning-scaffold` (if systematic)

### Improvement/Optimization Prompts
**Indicators**: "improve", "optimize", "better", "enhance"
**Recommend**: `recursive-review`

### Creative/Design Prompts
**Indicators**: "design", "create", "build", "generate"
**Recommend**: `meta-prompting,reasoning-scaffold`

### Risk/Security Prompts
**Indicators**: "security", "risk", "vulnerability", "attack", "safe"
**Recommend**: `deep-analyze` (always include adversarial review)

### Complex Multi-Faceted Prompts
**Indicators**: Multiple questions, "and", compound requirements
**Recommend**: `reasoning-scaffold` (structure) + domain-appropriate technique

### Default Fallback
**If no clear indicators**: `meta-prompting` (safest - lets model figure it out)

---

## Technique Combinations

Some techniques work well together:

### Excellent Combinations ✅

| Combination | Use Case | Effect |
|-------------|----------|--------|
| `meta-prompting,recursive-review` | Building optimal prompt | Design from scratch, then refine iteratively |
| `deep-analyze,multi-perspective` | High-stakes decision | Rigorous analysis from multiple angles |
| `reasoning-scaffold,deliberate-detail` | Learning complex topic | Structured exploration with exhaustive detail |
| `multi-perspective,reasoning-scaffold` | Complex choice | Multiple viewpoints with systematic comparison |

### Redundant Combinations ⚠️

| Combination | Issue | Better Alternative |
|-------------|-------|-------------------|
| `recursive-review,deep-analyze` | Both do verification | Choose one based on use case |
| `meta-prompting,reasoning-scaffold` | Both provide structure | `meta-prompting` alone (will add structure) |
| `deliberate-detail,temperature-simulation` | Conflicting verbosity | Choose one |

---

## Anti-Patterns to Avoid

1. **Over-Engineering Simple Questions**
   - Don't use `deep-analyze` for "What's the syntax for X?"
   - Match technique complexity to problem importance

2. **Template Rigidity**
   - Adapt templates to context
   - Skip irrelevant steps explicitly if needed

3. **Verification Theater**
   - Verification must be genuine, not performative
   - If verification finds nothing, that's suspicious

4. **Persona Stereotyping**
   - Give personas specific, realistic priorities
   - Avoid caricatures (e.g., "cautious lawyer" vs "cowboy developer")

5. **Ignoring Synthesis**
   - Multi-perspective techniques require synthesis
   - Don't just present multiple views - integrate them

---

## Measuring Effectiveness

**Indicators these techniques are working:**
- ✅ Output includes explicit uncertainty quantification
- ✅ Multiple perspectives are genuinely in tension
- ✅ Verification finds actual problems (not just confirms)
- ✅ Reasoning chains are clear and reproducible
- ✅ Edge cases and failure modes are identified

**Indicators of poor application:**
- ❌ Verification confirms everything (suspicious)
- ❌ Personas agree too quickly (not realistic)
- ❌ Reasoning is still compressed/surface-level
- ❌ No new insights vs simpler prompt
- ❌ Excessive tokens for marginal quality gain

---

## Token Cost Guidelines

All techniques increase token usage. Use appropriately:

| Technique | Cost Multiplier | When to Accept Cost |
|-----------|----------------|---------------------|
| meta-prompting | 1.5-2x | Unfamiliar domain, need quality |
| recursive-review | 1.5-2x | Building reusable template |
| deep-analyze | 2-3x | High-stakes decision |
| multi-perspective | 3-4x | Complex trade-offs |
| deliberate-detail | 2-3x | Learning/documentation |
| reasoning-scaffold | 1.5-2x | Need reproducibility |
| temperature-simulation | 2x | Confidence calibration critical |

**Rule of thumb**: Reserve multi-technique combinations for highest-value problems.

---

## Quick Reference

**Need verification?** → `deep-analyze`
**Making a choice?** → `multi-perspective`
**Prompt unclear?** → `meta-prompting`
**Want structure?** → `reasoning-scaffold`
**Need detail?** → `deliberate-detail`
**Calibrate confidence?** → `temperature-simulation`
**Refining prompt?** → `recursive-review`

---

## Integration with Commands

This skill is designed to work with:

- `/optimize-prompt [techniques] <prompt>` - Transform basic prompt using techniques
- `/prompt-help [technique]` - Documentation and examples

---

## Updates

**2025-11-05**: Initial creation
- Core techniques from "Mental Models of Master Prompters"
- Templates for each technique
- Intelligent technique selection guide
- Combination recommendations
- Anti-patterns and measurement guidance
