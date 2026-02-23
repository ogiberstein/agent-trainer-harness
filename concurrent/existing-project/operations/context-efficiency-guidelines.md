# Context Efficiency Guidelines

Use this guide to keep runs efficient without hard token caps.

## 1) Minimal Active Set
- Activate only required roles and skills for the current project.
- Use `profiles/active-skills.yaml` to pin the smallest viable set.

## 2) Phase-Scoped Context
- Load only files needed for the current phase (typically 3-6 files).
- Avoid passing unrelated specs, docs, or historical artifacts.

## 3) Reference, Do Not Re-Paste
- Treat large policy docs as reference artifacts.
- Do not repeatedly paste long framework text into prompts.

## 4) Summary-First Handoffs
- Prefer short, structured handoffs over narrative recaps.
- Include only: deliverables, open questions, constraints, acceptance criteria.

## 5) Rolling Summaries
- After each phase, write a concise summary and use it downstream.
- Prefer `memory/summaries/` artifacts over full-history replay.

## 6) Narrow Rework
- On gate failure, rerun only the failed portion with targeted feedback.
- Do not restart whole phases unless dependencies changed.

## 7) Concise Output Default
- Ask agents for short status outputs with file paths and decisions.
- Avoid long prose unless deep analysis is explicitly needed.

## 8) Separate Setup from Delivery
- Reuse scaffold/policies as stable baseline.
- For new projects, customize profile and brief; avoid regenerating unrelated artifacts.

## 9) Isolate Parallel Work
- When parallel coding is necessary, isolate tasks by branch/worktree and file scope.
- Do not let multiple active tasks edit overlapping paths without explicit orchestration.

## Quick Operating Check (Before Any Phase)
1. Which files are strictly required right now?
2. Can a summary replace raw history?
3. Are we loading optional agents/skills that are not needed?
