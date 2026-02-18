# Workflow State

Use this file to make multi-step workflows resumable.

## Active Workflow
- Workflow ID: WF-001
- Name: [feature or initiative]
- Status: running | blocked | completed
- Current step: [step-id]
- Last checkpoint: YYYY-MM-DD HH:MM UTC
- Owner: [role]

## Steps
| Step ID | Description | Owner | Status | Evidence | Next Action |
|---|---|---|---|---|---|
| STEP-001 | Requirements baseline | Product Manager | completed | `specs/requirements.md` | Move to design |
| STEP-002 | Design package | Designer | running | `specs/ui-spec.md`, `specs/architecture.md` | Complete gate checks |
| STEP-003 | Backend implementation | Fullstack Engineer | pending |  | Await STEP-002 |

## Resume Rules
- Resume from the first non-completed step.
- Do not repeat completed steps unless dependencies changed.
- If a step fails, append failure evidence and spawn a linked fix step.
