---
name: quant-statistics-probability
description: Performs quantitative statistics and probability analysis for market and trading use cases, including distributions, hypothesis tests, risk metrics, and scenario calculations. Use when users request quant math, strategy metrics, or probability-driven decisions.
---

# Quant Statistics Probability

## Purpose
Provide rigorous, transparent quantitative analysis for trading and market workflows.

## Use When
- Computing expected value, variance, Sharpe-like metrics, drawdown risk.
- Running probability calculations for strategy outcomes.
- Evaluating assumptions in backtests and market models.

## Required Inputs
- Data source description and timeframe
- Variable definitions and units
- Assumptions (distribution, stationarity, independence, fees/slippage)
- Desired outputs (metrics, confidence level, decision threshold)

## Workflow
1. Restate objective and assumptions explicitly.
2. Validate data quality, sample size, and missing value policy.
3. Choose methods (descriptive stats, test, model) with rationale.
4. Compute metrics with intermediate formulas shown.
5. Run sensitivity checks (best/base/worst assumptions).
6. Report limitations and model risk.

## Output Format
```markdown
## Quant Analysis
- Objective:
- Inputs and assumptions:
- Method:
- Results:
  - metric: value
- Sensitivity:
  - scenario -> result
- Limitations:
- Decision guidance (non-financial-advice framing):
```

## Guardrails
- Do not present uncertain estimates as certainties.
- Always disclose assumption risk and data limitations.
- Include transaction costs/slippage assumptions when relevant.
- Treat outputs as analytical support, not financial advice.
