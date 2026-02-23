---
name: security-audit-adversarial-testing
description: Performs adversarial security audits of code and system design, including threat modeling, abuse-case testing, and exploitability assessment. Use when users request security reviews, stress testing, or hardening guidance.
---

# Security Audit Adversarial Testing

## Purpose
Find exploitable weaknesses before release by testing from an attacker mindset.

## Use When
- Reviewing code for security before QA/release.
- Investigating auth, permissions, input handling, secrets, and data exposure.
- Stress testing trust boundaries and abuse cases.

## Required Inputs
- Relevant code and architecture artifacts
- Deployment assumptions and trust boundaries
- Authentication/authorization model
- Threat tolerance and compliance constraints

## Workflow
1. Build a concise threat model (assets, actors, attack surfaces).
2. Enumerate abuse cases by entry point.
3. Check common classes: injection, auth bypass, privilege escalation, SSRF, deserialization, secret leakage, insecure defaults.
4. Assess exploitability and blast radius.
5. Recommend prioritized fixes and compensating controls.

## Severity Scale
- Critical: likely exploitable, high impact, immediate fix required.
- High: significant exploit path with strong impact potential.
- Medium: exploitable with constraints or moderate impact.
- Low: hard-to-exploit or limited impact issue.

## Output Format
```markdown
## Security Audit Findings
- Threat model summary:
- Findings:
  - [severity] [title]
    - Vector:
    - Impact:
    - Evidence:
    - Fix:
- Residual risk:
- Retest plan:
```

## Guardrails
- Do not run destructive actions against real production systems.
- Prioritize reproducible evidence over theoretical concerns.
- Map each finding to concrete remediation steps.
