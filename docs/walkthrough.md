# End-to-End Walkthrough: Todo API

This walkthrough traces a small project through the full harness lifecycle so you can see how the pieces fit together. The example is a simple "Todo API with auth" — small enough to follow, large enough to exercise every phase.

## Step 0: Fill in the Brief

Edit `BRIEF.md`:

```markdown
# Project Brief

## Project Name
Todo API

## Goal
Let authenticated users create, read, update, and delete personal todo items via a REST API.

## Users
Individual developers who want a reference API with auth, CRUD, and tests.

## Scope
- In scope:
  - User registration and login (JWT)
  - CRUD endpoints for todos (scoped per user)
  - Input validation and error handling
  - Automated tests
- Out of scope:
  - Frontend/UI
  - Team/sharing features
  - Deployment/CI pipeline

## Constraints
- Tech stack: Node.js + Express + PostgreSQL
- Timeline: 1 week
- Budget: unconstrained
- Compliance/security: standard web app security, no PII beyond email

## Success Criteria
- [ ] User can register, log in, and receive a JWT
- [ ] Authenticated user can CRUD their own todos
- [ ] Unauthenticated requests are rejected with 401
- [ ] All endpoints have input validation and meaningful error responses
- [ ] Test suite covers happy path and key error cases
```

## Step 1: Run Setup (`/harness-start`)

Paste the Day 0 prompt from `day-0-start.md`. The agent will:

1. Read `BRIEF.md` and profiles.
2. Run the Setup Engineer flow → produces `profiles/merged-profile.yaml` and generated agent prompts in `harness/generated-agents/`.
3. Set `STATUS.md` to `phase: requirements`.
4. Log setup decisions in `DECISIONS.md` (e.g., "Skipping Growth Strategist — no acquisition goal").

## Step 2: Requirements Phase

The agent switches to the Product Manager role and produces:

**`specs/requirements.md`** (excerpt):
```markdown
### FR-001: User Registration
- **Priority:** Must
- **User Story:** As a developer, I want to register with email/password so that I have an account.
- **Acceptance Criteria:**
  - [ ] POST /auth/register with valid email+password returns 201 and user object
  - [ ] Duplicate email returns 409
- **Edge Cases:**
  - What if password is too short? → 400 with validation message
- **Out of Scope:**
  - OAuth/social login
```

**`handoffs/product-to-design.md`** summarizing deliverables and open questions.

**Gate check:** Every FR has user story + ≥2 ACs, edge cases listed, out-of-scope explicit → **PASS**. Human approves.

## Step 3: Design Phase

The agent switches to the Designer role and produces:

- **`specs/architecture.md`**: data model (users, todos tables), API endpoint inventory, tech stack rationale, folder structure.
- **`specs/ui-spec.md`**: marked as "N/A — API-only project" (a valid output for non-UI projects).
- **`handoffs/design-to-engineering.md`**: summarizes API contract and data model.
- **`DECISIONS.md`** entry: "DEC-001: Using bcrypt for password hashing, JWT with 24h expiry."

**Gate check:** Architecture includes data model + API design, tech choices justified → **PASS**. Human approves.

## Step 4: Implementation Phase

The agent switches to Fullstack Engineer and builds:

- `src/` — Express app with auth routes, todo routes, middleware, DB migrations.
- `tests/` — registration, login, CRUD, auth guard tests.
- `handoffs/engineering-to-qa.md` — what was built, how to run tests, known limitations.

**Gate check:** Core FRs implemented, tests present and passing → **PASS**.

## Step 5: QA Phase

The agent switches to QA Engineer and produces:

- **`qa/test-plan.md`**: test matrix mapping each FR/AC to a test case.
- **`qa/issues.md`**: e.g., "ISS-001: Missing rate limiting on /auth/login — Severity: Minor."
- **`qa/audit-report.md`**: "Ship with known issues. 1 Minor issue (rate limiting). All FRs pass."
- **`handoffs/qa-to-engineering.md`**: issues to fix if desired.

**Gate check:** No Critical/Major open, recommendation is "Ship with known issues" → **PASS**.

## Step 6: Documentation Phase

The agent switches to Documentation Writer and produces:

- **`docs/README.md`**: what it is, quick start, API overview.
- **`docs/SETUP.md`**: prerequisites, install steps, env config, verification command.
- **`docs/API.md`**: every endpoint with method, path, request/response examples.

**Gate check:** No placeholders, setup guide has concrete commands → **PASS**.

## Step 7: Final Review

The Orchestrator compiles:

```markdown
## Delivery Summary
- **Built:** REST API with JWT auth and CRUD todos
- **Deferred:** Rate limiting (Minor), OAuth (out of scope)
- **Risks:** No rate limiting on auth endpoints
- **Recommended next iteration:** Add rate limiting, consider refresh tokens
```

`STATUS.md` updated to `phase: complete`.

## Key Takeaways

1. **The brief drives everything.** A weak brief produces weak requirements produces weak code. Invest time here.
2. **Gates prevent compounding errors.** Catching a missing AC in Phase 1 is cheaper than discovering it in Phase 4.
3. **Handoffs preserve context.** Without them, each phase starts from scratch and re-reads everything.
4. **Lite mode would skip Phases 2, 6, and the detailed QA artifacts** — fine for a project this simple, but the full flow demonstrates the structure.
5. **The `/retrospective` command after delivery** captures what worked and what didn't, feeding improvements back into the harness.
