# Optimize Prompt

You are transforming a basic prompt into an enhanced prompt using advanced prompting techniques.

**Skill activation**: Invoke the `prompt-engineering` skill for template reference.

**Input**: `{ARG}`

---

## Step 1: Parse Input

The input format is either:
- `[techniques] <prompt>` - User specifies which techniques to apply
- `<prompt>` - No techniques specified, you'll select intelligently

Parse the input to determine:
- **Techniques requested**: (comma-separated list or empty)
- **Base prompt**: The prompt to enhance

Available techniques:
- `meta-prompting` - Reverse prompting (design optimal prompt)
- `recursive-review` - 3-pass iterative refinement
- `deep-analyze` - Chain of verification + adversarial review
- `multi-perspective` - Multi-persona debate
- `deliberate-detail` - Exhaustive detail (no summarization)
- `reasoning-scaffold` - Structured step-by-step template
- `temperature-simulation` - Multiple confidence levels

**Parsing logic**:
- If input contains known technique names before the main text → extract techniques
- Otherwise → no techniques specified, proceed to intelligent selection

---

## Step 2: Intelligent Technique Selection (if needed)

If no techniques were specified, analyze the base prompt and select appropriate technique(s).

**Analysis questions**:
1. What is the user trying to accomplish?
2. What type of prompt is this? (analysis, decision, explanation, creation, evaluation)
3. What indicators suggest specific techniques?
4. How complex is the task?

**Selection guidelines** (from prompt-engineering skill):

### Analysis/Evaluation Prompts
Indicators: "analyze", "evaluate", "assess", "review", "examine"
→ Recommend: `deep-analyze`

### Decision/Choice Prompts
Indicators: "choose", "select", "decide", "which", "should we", "vs", "or"
→ Recommend: `multi-perspective` or `multi-perspective,reasoning-scaffold`

### Vague/Underspecified Prompts
Indicators: Very short (<10 words), no specifics, unclear goal
→ Recommend: `meta-prompting`

### Explanation/Understanding Prompts
Indicators: "explain", "how does", "what is", "describe", "learn about"
→ Recommend: `deliberate-detail` (complex) or `reasoning-scaffold` (systematic)

### Improvement/Optimization Prompts
Indicators: "improve", "optimize", "better", "enhance"
→ Recommend: `recursive-review`

### Creative/Design Prompts
Indicators: "design", "create", "build", "generate"
→ Recommend: `meta-prompting,reasoning-scaffold`

### Risk/Security Prompts
Indicators: "security", "risk", "vulnerability", "attack", "safe"
→ Recommend: `deep-analyze`

### Complex Multi-Faceted Prompts
Indicators: Multiple questions, "and", compound requirements
→ Recommend: `reasoning-scaffold` + appropriate domain technique

### Default Fallback
If no clear indicators → `meta-prompting` (safest default)

**Output of this step**: List of technique(s) to apply

**Explain your selection**: "I've analyzed your prompt and selected [techniques] because [reasoning]."

---

## Step 3: Apply Technique Templates

For each selected technique, incorporate its template from the prompt-engineering skill.

### Template: meta-prompting

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

---

### Template: recursive-review

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

---

### Template: deep-analyze

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

---

### Template: multi-perspective

```
{BASE_PROMPT}

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

---

### Template: deliberate-detail

```
{BASE_PROMPT}

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

---

### Template: reasoning-scaffold

```
{BASE_PROMPT}

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

---

### Template: temperature-simulation

```
{BASE_PROMPT}

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

---

## Step 4: Construct Enhanced Prompt

Combine the base prompt with the selected technique template(s).

**Integration rules**:
- If multiple techniques: Apply in logical order (see skill for combinations)
- Preserve the core intent of the base prompt
- Make the enhanced prompt self-contained and ready to use
- Format clearly with sections/phases if multiple techniques

---

## Step 5: Output

Provide the enhanced prompt in this format:

```markdown
## Enhanced Prompt

**Original**: {BASE_PROMPT}

**Techniques Applied**: {TECHNIQUE_LIST}

**Why These Techniques**: {BRIEF_EXPLANATION}

---

### Ready-to-Use Enhanced Prompt

```
{COMPLETE_ENHANCED_PROMPT}
```

---

**Usage Notes**:
- Token cost: ~{MULTIPLIER}x compared to basic prompt
- Best used for: {USE_CASE}
- You can copy this prompt and use it directly, or I can execute it now if you'd like.
```

---

## Examples

### Example 1: User Specifies Techniques

**Input**: `deep-analyze "Evaluate the security of JWT tokens"`

**Output**:
```markdown
## Enhanced Prompt

**Original**: Evaluate the security of JWT tokens

**Techniques Applied**: deep-analyze

**Why These Techniques**: You requested deep-analyze for rigorous verification and adversarial review of security topics.

---

### Ready-to-Use Enhanced Prompt

```
Evaluate the security of JWT tokens.

Phase 1: Initial Analysis
Provide thorough analysis of JWT token security.

Phase 2: Chain of Verification
[... full template ...]
```

---

### Example 2: Intelligent Selection

**Input**: `"Choose between PostgreSQL and MongoDB for our new service"`

**Analysis**: This is a decision/choice prompt with "choose between" indicator.

**Selected**: `multi-perspective` (decision-making with trade-offs)

**Output**: Enhanced prompt with multi-persona debate template

---

### Example 3: Multiple Techniques

**Input**: `deep-analyze,multi-perspective "Migrate to microservices architecture"`

**Output**: Enhanced prompt combining both techniques in logical order

---

## Important Notes

1. **Token Cost**: Enhanced prompts use 1.5-4x more tokens. This is intentional - you're getting higher quality reasoning.

2. **Don't Over-Optimize Simple Prompts**: If the base prompt is "What's the capital of France?", don't apply complex techniques. Use judgment.

3. **Test and Iterate**: After using an enhanced prompt, you can run `/optimize-prompt` again with feedback.

4. **Save Reusable Prompts**: Enhanced prompts can be saved as templates for repeated use.

5. **Execute Option**: After seeing the enhanced prompt, you can ask me to execute it immediately: "Execute this enhanced prompt now"
