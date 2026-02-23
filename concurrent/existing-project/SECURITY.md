# Security Policy

## Supported Versions

This harness is early-stage and does not yet have formal long-term support guarantees. Security-related fixes will generally land on the latest main branch and on the most recent tagged release.

## Reporting a Vulnerability

If you believe you have found a security issue in the harness (for example, a pattern that could lead to prompt injection, data leakage, or unsafe use of external tools):

- **Do not** share sensitive details in public issues.
- Instead, open a minimal GitHub issue that:
  - Describes the area of concern (e.g., specific file, pattern, or script).
  - Includes a high-level description of the risk without exposing sensitive data.
- If a private contact method is listed in the repository description or on the maintainer profile, you can also reach out there with more detail.

## Scope

This project is a harness and prompt/template collection. It does **not** ship runtime infrastructure, hosting, or production deployment code. When using it in your own stack, you are responsible for:

- Secret management and environment configuration.
- Network and infrastructure security.
- Compliance with any regulatory requirements in your domain.

## Best Practices for Users

- Treat all external inputs (user text, third-party content) as untrusted and apply the prompt-injection and security skills where appropriate.
- Avoid checking real secrets or proprietary data into the same repository as this public harness.
- Review and adapt the `skills/security-policy.md` and `harness/permissions-matrix.md` for your own environment before production use.
