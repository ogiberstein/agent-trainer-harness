# Project Brief

## Project Name
<!-- A short, memorable name. Avoid generic names like "App" or "Platform". -->

## Goal
<!-- What outcome should be delivered? Focus on the user's problem, not features.
     Good: "Enable freelancers to invoice clients and get paid within 48 hours."
     Bad: "Build an invoicing app." -->

## Users
<!-- Who is this for? Be specific. Include primary persona and any secondary users.
     Example: "Solo freelancers (1-person business) doing <$100K/year revenue." -->

## Scope
- In scope:
  <!-- List concrete deliverables. Be ruthless — everything not listed here is out of scope. -->
  - [...]
- Out of scope:
  <!-- Explicitly state what will NOT be built. This prevents scope creep downstream. -->
  - [...]

## Constraints
- Tech stack: <!-- Mandated technologies, or "team's choice" if flexible -->
- Timeline: <!-- Hard deadline or target, e.g., "MVP in 2 weeks" -->
- Budget: <!-- Token/cost constraints, hosting limits, or "unconstrained" -->
- Compliance/security: <!-- GDPR, HIPAA, SOC2, or "standard web app security" -->

## Verification Map
Required only for unattended Full and Concurrent runs. Do not complete this for Lite or supervised small-task workflows.

Before implementation, add one row for each material code area and choose feedback loops that fit the run budget. As conditional design guidance, make impossible states unrepresentable where this simplifies correctness; this is not a mandate for extra type scaffolding.

During the existing pre-build review, Codex must challenge the map for missing coverage, weak oracles, and feedback loops that exceed the run budget. Resolve material findings before the run. The existing post-build code audit remains required; this preflight is not a new review lane.

- Run verification budget: [...]

| Material code area | Invariant | Fastest feedback loop | Expected runtime range | Oracle | Smallest real-boundary check |
|---|---|---|---|---|---|
| [...] | [...] | [...] | [...] | [...] | [...] |

## Success Criteria
<!-- How do you know this project succeeded? Use measurable outcomes where possible. -->
- [ ] <!-- e.g., "User can complete core flow end-to-end" -->
- [ ] <!-- e.g., "Page load under 2.5s on mobile" -->

## Prior Art and Context
<!-- Link or describe any existing systems, prototypes, competitor references,
     or user research that should inform this project. Delete section if none. -->

## Notes
<!-- Any additional context, preferences, or constraints from the requester. -->
