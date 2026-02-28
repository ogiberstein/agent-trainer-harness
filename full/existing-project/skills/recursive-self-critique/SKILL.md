---
name: recursive-self-critique
description: Adversarial self-testing loop that improves output quality by generating test cases against your own work, judging pass/fail, and iterating until robust. Use during requirements, architecture, gate decisions, and any high-stakes reasoning.
version: 0.1.0
reviewed_at: 2026-02-18
---

# Recursive Self-Critique

## Purpose
Produce higher-confidence outputs by forcing explicit separation between generation and critique. Instead of one-shot answers, iterate through adversarial self-testing until the output survives scrutiny.

## When to Use
- Drafting or finalizing requirements (Product Manager).
- Making architecture and design decisions (Designer).
- Evaluating gate advancement on complex phases (Orchestrator).
- Implementing architecturally significant changes where wrong abstractions are costly (Engineers, on-demand).

## Do Not Use For
- Routine implementation tasks with clear specs and low ambiguity.
- Documentation that restates existing code behavior.
- Tasks where speed matters more than depth (hotfixes, typo corrections).

## Inputs Required
- Your draft output (requirements doc, architecture spec, gate assessment, etc.)
- `BRIEF.md` — for grounding tests against project goals
- `DECISIONS.md` — for checking consistency with prior decisions
- `specs/requirements.md` — for checking alignment (when applicable)

## Steps

### 1. Generate
Produce your complete output as you normally would. Do not self-censor or hedge — commit to concrete decisions.

### 2. Adversarial Test Generation
PAUSE. Step out of the author mindset and into the critic mindset. Generate 3-5 test cases designed to find weaknesses:

- **Assumption test:** What assumption am I making that could be wrong? What if the opposite is true?
- **Edge-case test:** What edge case or failure mode would break this? What happens at the boundaries?
- **Skeptic test:** What would a skeptical senior reviewer challenge? What looks hand-wavy?
- **Completeness test:** What am I missing from the BRIEF or requirements that should be addressed here?
- **Consistency test:** Does this conflict with any prior decision in DECISIONS.md or any stated constraint?

Tailor the specific tests to your domain:
- **Requirements:** ambiguity, testability, scope creep, missing user segments, conflicting priorities
- **Architecture:** scalability, failure modes, single points of failure, dependency risks, migration paths
- **Gate decisions:** evidence quality, unchecked acceptance criteria, optimism bias

### 3. Judge
Evaluate your output against each test case. For each:
- **Pass** — the output handles this adequately (state why in one sentence)
- **Fail** — the output has a gap or weakness (state the specific problem)

Be honest. The value of this step is entirely dependent on intellectual honesty.

### 4. Revise
If any test case failed:
- Note the specific learning from each failure
- Revise your output to address the failures
- Do not just add caveats — make structural improvements

### 5. Iterate
Return to Step 2 with your revised output. Generate new test cases if the revision introduced new concerns. Maximum 3 iterations total.

### 6. Report
Append a self-critique summary to your output:

```markdown
## Self-Critique Summary
- **Iterations:** [N]
- **Tests passed:** [M/K]
- **Key revisions:**
  - [What changed and why, one line per revision]
```

## Output Contract
- Your original deliverable, improved through iteration
- Self-critique summary appended (as shown above)
- If a test case failed and could not be resolved, flag it as an open risk in the output

## Quality Bar
- At least 3 adversarial test cases generated per iteration
- All test cases pass by the final iteration, OR unresolved failures are explicitly flagged as risks
- Revisions are structural, not cosmetic — adding a disclaimer doesn't count as fixing a gap

## Safety and Security
- Do not use this process to rationalize away legitimate concerns. If a test reveals a real problem, escalate.
- Do not suppress failure results. Transparency about what was challenged and survived builds trust.
- If the recursive loop exceeds 3 iterations without convergence, stop and escalate to the orchestrator or human with a summary of what isn't resolving.
