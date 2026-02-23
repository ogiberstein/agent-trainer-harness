# Private Skills Library

This directory is for internal, vetted skills only.

## Structure
- `skills/_TEMPLATE/SKILL.md` - starter template for new skills
- `skills/registry.md` - inventory and ownership
- `skills/security-policy.md` - trust and review requirements
- `skills/packs.md` - optional grouped activations by use case

## Authoring Workflow
1. Copy `_TEMPLATE/SKILL.md` into a new skill folder.
2. Fill purpose, usage rules, and concrete steps.
3. Add owner, version, and review date to `skills/registry.md`.
4. Run an internal review before enabling in production harnesses.

## Activation
- Select a pack from `skills/packs.md` or define custom selections.
- Pin enabled skills in `profiles/active-skills.yaml` per project.
