---
name: development-philosophy
description: Personal development philosophy emphasizing experiment-driven, fail-fast approach. Activate when planning implementations, reviewing code architecture, making design decisions, or when user asks to apply development principles. Guides against over-engineering and towards solving real problems with simple solutions.
---

# Development Philosophy

## Core Approach: Experiment-Driven, Fail-Fast

**Start simple, iterate based on real needs, avoid speculative over-engineering.**

- Experiment in short cycles; expect to learn and pivot
- Build the simplest thing that works, then improve based on actual pain points
- Focus on real bottlenecks, not hypothetical problems (Theory of Constraints)
- Document learnings, not just code

**For learning projects specifically:**
- Lessons are experiments - focus on understanding, not production perfection
- STATUS.md tracks progress and learnings
- Each lesson can fail or succeed - both outcomes are valuable

---

## Technical Principles

### For Production Code

**SOLID Principles:**
- **Single Responsibility**: One class, one reason to change
- **Open/Closed**: Open for extension, closed for modification
- **Liskov Substitution**: Subtypes must be substitutable for base types
- **Interface Segregation**: Many specific interfaces > one general interface
- **Dependency Inversion**: Depend on abstractions, not concretions

**Key Patterns:**
- **DRY (Don't Repeat Yourself)**: Extract common patterns, but not prematurely
- **CQRS**: Separate reads from writes when complexity justifies it
- **Dependency Injection**: Pass dependencies in, don't create them internally
- **Inversion of Control**: Framework/container manages object lifecycle

**Test-First Development:**
- Write failing test first (defines behavior)
- Write minimal code to pass
- Refactor with tests as safety net
- Tests document intent and prevent regressions

### For Experimental/Lesson Code

**Apply selectively:**
- ✅ DRY when you notice actual repetition (not before)
- ✅ Test-first when exploring new patterns (helps clarify thinking)
- ✅ Dependency injection for agents (when framework encourages it)
- ⚠️ SOLID when it aids learning, not just for principle's sake
- ⚠️ CQRS probably overkill for simple lessons

**Priority:** Understanding > perfection. Messy code that teaches is better than pristine code you don't understand.

---

## When to Apply What

### Experiment Phase (Lessons/Prototypes)
1. **Start**: Write simplest code that demonstrates concept
2. **Notice pain**: When does duplication hurt? When do tests help?
3. **Extract patterns**: Move from concrete to reusable
4. **Document learnings**: What worked? What didn't?

### Productionize Phase (Moving to Production)
1. **Apply SOLID**: Refactor for maintainability
2. **Add comprehensive tests**: Not just happy path
3. **Inject dependencies**: Make components swappable
4. **Consider CQRS**: If read/write patterns differ significantly
5. **Enforce DRY**: Extract shared utilities

---

## Practical Guidelines

### Don't:
- ❌ Build abstractions before you have 3+ concrete cases
- ❌ Add dependency injection if simple imports work fine
- ❌ Write tests for trivial getters/setters
- ❌ Apply CQRS to simple CRUD operations
- ❌ Optimize before measuring (real bottlenecks only)

### Do:
- ✅ Write tests when behavior is non-obvious or critical
- ✅ Extract functions/classes when you see actual repetition
- ✅ Use dependency injection when testing requires mocking
- ✅ Apply SOLID when classes have unclear responsibilities
- ✅ Refactor when you understand the problem better

---

## How This Guides Development

**For AI assistants (Claude Code):**
- Challenge me when I'm over-engineering
- Ask "What's the simplest version that would work?"
- Suggest patterns when you see real pain (duplication, tight coupling, hard to test)
- Don't preach principles - show how they solve actual problems

**For code reviews:**
- Is this DRY violation actually painful or just aesthetic?
- Does this abstraction solve a real problem or add complexity?
- Are tests testing behavior or implementation details?
- Is this SOLID principle helping or just adding boilerplate?

**For architectural decisions:**
- What's the current bottleneck? (Theory of Constraints)
- What's the simplest way to prove this idea? (experiment-driven)
- Can we defer this decision until we know more? (fail-fast)
- Does this pattern solve a problem we actually have? (no speculation)

---

## Key Questions to Ask

**Before adding abstraction:**
- Do we have 3+ concrete examples that would benefit?
- Is the duplication actually causing pain?
- Will this make the code easier or harder to understand?

**Before adding complexity:**
- What problem are we solving?
- Is this problem real or hypothetical?
- What's the simplest solution?
- Can we prove it works with a small experiment first?

**During implementation:**
- Are we solving the real bottleneck?
- Could we defer this decision?
- What's the minimum viable implementation?
- How will we know if this works?

---

## References

- **Doc Norton**: Emergent design, organic architecture
- **Theory of Constraints**: Focus on bottlenecks, not broad optimization
- **SOLID Principles**: Robert C. Martin (Uncle Bob)
- **Test-Driven Development**: Kent Beck
- **DRY Principle**: Andy Hunt & Dave Thomas (Pragmatic Programmer)

---

## TL;DR

**Experiment fast, learn from failures, solve real problems.** Apply SOLID/DRY/CQRS/DI when they solve actual pain, not because they're "best practices." Tests should help, not hinder. Start simple, iterate based on evidence.
