# Release Gates

## Phase Gate Checklists

Each phase has explicit pass criteria. Record PASS/FAIL/SKIPPED in the STATUS.md Gate Log before advancing. Different agents should arrive at the same gate verdict given the same artifacts.

### Phase 1 — Requirements Gate
- [ ] Every FR has a user story with at least 2 acceptance criteria
- [ ] Every FR has at least 1 edge case documented
- [ ] Out-of-scope section is explicit (not empty)
- [ ] Risks, Assumptions, and Concerns section is filled (not empty)
- [ ] Open questions are listed or explicitly "none"
- [ ] MoSCoW priority assigned to all FRs
- [ ] Cross-references consistent (BRIEF.md scope matches requirements scope)
- [ ] Handoff to design is complete with deliverables and context

### Phase 2 — Design Gate
- [ ] Every specified component defines default/loading/empty/error states
- [ ] Design tokens are concrete values (not placeholders)
- [ ] Responsive breakpoints specified
- [ ] Accessibility requirements documented
- [ ] Architecture includes data model, API shape, and state strategy
- [ ] Architecture is feasible given project constraints (timeline, stack)
- [ ] Cross-references consistent (API shape matches FRs, components cover ACs)
- [ ] Handoff to engineering is complete

### Phase 3 — Implementation Gate
- [ ] All "Must" FRs implemented
- [ ] All specified API endpoints have input validation
- [ ] Error handling returns appropriate status codes
- [ ] No hardcoded secrets
- [ ] Unit and integration tests present and passing
- [ ] Frontend components implement all specified state variants
- [ ] Semantic HTML and keyboard accessibility verified (if frontend exists)
- [ ] Handoff to QA includes test hints and known gaps

### Phase 4 — QA Gate
- [ ] Every acceptance criterion maps to at least 1 test case
- [ ] All tests executed with pass/fail evidence
- [ ] No open Critical issues
- [ ] No open Major issues (unless human-approved exception with rationale in DECISIONS.md)
- [ ] Issues include severity, reproduction steps, and expected vs actual
- [ ] Ship recommendation is explicit (Ship / Ship-with-known-issues / No-ship)

### Phase 5 — Documentation Gate
- [ ] No placeholder text in final docs
- [ ] Setup steps are verified and runnable
- [ ] API docs match implemented endpoints (not spec-only)
- [ ] Known issues from QA reflected
- [ ] Terminology consistent with codebase and UI

### Phase 6 — Growth Gate (if activated)
- [ ] Every recommendation includes expected impact and measurement method
- [ ] SEO/GEO strategy has concrete targets
- [ ] Experiment backlog has hypothesis, metric, and guardrails per item
- [ ] Analytics event taxonomy defined
- [ ] All proposals grounded in implemented capabilities

---

## Release Gate (Final)

For production or high-risk changes, final release also requires:

1. Security audit completed (if applicable)
2. No unresolved Critical/High security findings
3. Any accepted residual risk documented in `DECISIONS.md` with human approval

## Promotion Record
- Candidate version:
- Baseline version:
- Decision:
- Approver:
- Date:
