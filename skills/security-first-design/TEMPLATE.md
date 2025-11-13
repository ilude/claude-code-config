{BASE_TARGET}

Phase 1: Attack Surface Mapping
- What external inputs exist?
- What resources are accessed?
- What privileges are required?
- What data is stored/transmitted?
- What authentication is needed?

Phase 2: Threat Modeling
- **Injection attacks**: SQL, command, XSS, path traversal
- **Authentication bypass**: Default credentials, weak tokens
- **Authorization bypass**: IDOR, privilege escalation
- **Data exposure**: Secrets in logs, error messages, commits
- **Denial of service**: Resource exhaustion, infinite loops

Phase 3: Secret Management Audit
- Are API keys in environment variables?
- Are credentials hardcoded anywhere?
- Is .env in .gitignore?
- Are secrets logged accidentally?
- Is sensitive data encrypted at rest?

Phase 4: Input Validation Design
- Whitelist valid inputs (not blacklist)
- Validate types, lengths, formats
- Sanitize before use in commands/queries
- Escape before rendering in UI
- Reject malformed data early

Phase 5: Security Checklist
- ✅ No secrets in code/commits
- ✅ Input validation on all external data
- ✅ Principle of least privilege applied
- ✅ Error messages don't leak info
- ✅ Dependencies scanned for vulnerabilities
- ✅ Authentication/authorization correct
- ⚠️ Remaining risks documented with mitigations
