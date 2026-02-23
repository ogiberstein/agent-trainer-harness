# Skills Security Policy

## Trust Model
- Only internal skills in this repository are trusted by default.
- External skills must be imported into this repo and reviewed before use.

## Review Requirements
- Validate every instruction step for safety and relevance.
- Confirm no hidden network exfiltration or secret disclosure behavior.
- Assign owner and review date for each skill.

## Operational Rules
- Pin skill versions in harness configs.
- Keep an audit trail of skill updates in `operations/changelog.md`.
- Disable any skill immediately if suspicious behavior is detected.
