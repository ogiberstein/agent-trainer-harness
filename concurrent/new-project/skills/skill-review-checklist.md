# Skill Review Checklist

Use this checklist before moving any skill from `draft` to `reviewed` or `approved`.

## 1) Metadata and Scope
- [ ] Skill has valid frontmatter (`name`, `description`).
- [ ] Name is lowercase-hyphen format and unique.
- [ ] Description clearly states WHAT it does and WHEN to use it.
- [ ] Scope boundaries and "Do not use for" are explicit.

## 2) Safety and Security
- [ ] Instructions do not encourage bypassing policy or permissions.
- [ ] No secret handling anti-patterns (hardcoding, logging secrets, exfiltration).
- [ ] Untrusted input handling is explicit (sanitize, validate, or escalate).
- [ ] Destructive actions require confirmation or escalation.
- [ ] Skill aligns with `skills/security-policy.md`.

## 3) Quality and Practicality
- [ ] Workflow is step-by-step and executable.
- [ ] Output contract is explicit and testable.
- [ ] Terminology is consistent with repository standards.
- [ ] No placeholders left in final skill content.
- [ ] SKILL.md is concise and readable.

## 4) Integration and Governance
- [ ] Skill is registered in `skills/registry.md` with owner and review date.
- [ ] Version is set and follows semver intent.
- [ ] Pack membership is documented in `skills/packs.md` (if applicable).
- [ ] Project activation can be pinned via `profiles/active-skills.yaml`.

## 5) Validation Pass
- [ ] Dry run completed on at least one representative scenario.
- [ ] Output quality reviewed by human.
- [ ] Failure modes documented (what to do when uncertain or blocked).
- [ ] Any risks/limitations are documented in Notes.

## Review Decision
- **Skill:** [skill-name]
- **Version:** [x.y.z]
- **Reviewer:** [name]
- **Date:** [YYYY-MM-DD]
- **Decision:** `reviewed` | `approved` | `changes-required`
- **Notes:**
  - [note]
