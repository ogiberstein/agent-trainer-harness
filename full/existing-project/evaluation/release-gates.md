# Release Gates

A new agent/profile/adapter version can be promoted only if:

1. No critical regressions against last stable baseline
2. Scorecard thresholds met for all critical dimensions
3. Cost increase is within approved threshold
4. At least one failure-injection scenario passes
5. Security and permissions checks pass

## Security Gate (Project Release)

For production or high-risk changes, release also requires:

1. Security audit completed (`security-audit-adversarial-testing` workflow or equivalent)
2. No unresolved Critical/High security findings
3. Any accepted residual risk documented in `DECISIONS.md` with human approval

## Promotion Record
- Candidate version:
- Baseline version:
- Decision:
- Approver:
- Date:
