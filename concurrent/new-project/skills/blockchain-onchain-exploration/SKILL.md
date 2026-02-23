---
name: blockchain-onchain-exploration
description: Explores and interprets blockchain data including transactions, logs, balances, contract interactions, and event flows. Use when users need onchain investigation, protocol behavior analysis, or wallet/contract activity interpretation.
---

# Blockchain Onchain Exploration

## Purpose
Provide accurate, traceable interpretation of onchain behavior.

## Use When
- Investigating wallet or contract activity.
- Explaining transaction flows, event logs, and token movements.
- Analyzing protocol mechanics from onchain evidence.

## Required Inputs
- Chain/network (for example, Ethereum mainnet, Arbitrum, Solana)
- Target identifiers (address, tx hash, block range, token contract)
- Time window and question scope
- Required output depth (quick summary vs detailed trace)

## Workflow
1. Confirm chain and identifiers to avoid cross-network confusion.
2. Pull transaction/event context and normalize key fields.
3. Reconstruct causal flow (caller, callee, value transfer, emitted events).
4. Interpret outcomes (success/failure/revert reason if available).
5. Highlight uncertainty (missing traces, reorg risk, indexing lag).
6. Summarize with references to exact identifiers.

## Output Format
```markdown
## Onchain Exploration Report
- Network:
- Scope:
- Key artifacts:
  - tx/address/block:
- Findings:
  - [finding]
- Flow summary:
  1. ...
  2. ...
- Risks/uncertainty:
- Next queries:
```

## Guardrails
- Never infer intent without evidence.
- Distinguish confirmed onchain facts from interpretation.
- Call out chain reorg/finality caveats where relevant.
