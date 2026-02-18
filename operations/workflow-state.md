# Workflow State

Use this file to make multi-step workflows resumable.

## Active Workflow
- Workflow ID: WF-001
- Name: <!-- feature or initiative name -->
- Status: running | blocked | completed
- Current step: <!-- step-id -->
- Last checkpoint: YYYY-MM-DD HH:MM UTC
- Owner: <!-- role -->

## Steps

| Step ID | Description | Owner | Status | Evidence | Next Action |
|---|---|---|---|---|---|
| STEP-001 | <!-- description --> | <!-- role --> | pending | | |

## Resume Rules
- Resume from the first non-completed step.
- Do not repeat completed steps unless dependencies changed.
- If a step fails, append failure evidence and spawn a linked fix step.
