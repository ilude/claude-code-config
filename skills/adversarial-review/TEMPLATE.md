{BASE_TARGET}

Phase 1: Challenge Assumptions
- What assumptions does this make?
- Which assumptions are most likely wrong?
- What happens if each assumption fails?

Phase 2: Edge Case Mining
- Boundary conditions (empty, null, max, negative)
- Timing issues (race conditions, ordering)
- Environment variations (OS, versions, permissions)
- Data quality issues (malformed, missing, duplicate)

Phase 3: Failure Mode Analysis
- List 5 ways this could fail
- For each: Likelihood (H/M/L), Impact (1-10), Mitigation
- Which failures are catastrophic?

Phase 4: Hidden Dependencies
- Undocumented state assumptions
- External service dependencies
- Implicit ordering requirements
- Configuration assumptions

Phase 5: Attack Vectors & Blind Spots
- What did we not consider?
- What expertise are we missing?
- Where could malicious input cause issues?
- What would break this in production?

Be adversarial. If you don't find issues, you weren't critical enough.
