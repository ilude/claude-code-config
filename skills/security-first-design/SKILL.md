# Security-First-Design Skill

**Auto-activate when:** User mentions authentication, authorization, API security, sensitive data, user input, secrets management, encryption, security review, or when working with `.env$` (actual env files, not examples), `credentials.json`, `secrets.yaml`, API keys, authentication systems, or security-critical features.

Systematically evaluate security implications before implementation.

## When to Activate

- Designing new authentication/authorization systems
- Building APIs that handle sensitive data
- Implementing user input handling
- Reviewing security concerns in existing code
- Planning features with security requirements

## Framework

Five-phase security analysis framework:

1. **Attack Surface Mapping** - Identify all external inputs, resource access, privileges, data handling, and authentication needs
2. **Threat Modeling** - Evaluate injection attacks, authentication bypass, authorization bypass, data exposure, and denial of service vectors
3. **Secret Management Audit** - Verify API keys, credentials, .gitignore rules, logging, and encryption
4. **Input Validation Design** - Establish whitelist validation, type/length/format checks, sanitization, and escaping
5. **Security Checklist** - Verify no secrets in code, input validation coverage, least privilege, safe error messages, dependency scanning, and documented risks

## Usage

Apply this framework when security is a primary design concern. Work through phases sequentially, documenting findings and mitigations at each stage.
