---
name: growth-analytics-instrumentation
description: Defines analytics events, attribution assumptions, and measurement requirements for growth initiatives. Use when growth plans require engineering instrumentation and reliable experiment measurement.
---

# Growth Analytics Instrumentation

## Purpose
Ensure growth decisions are based on reliable tracking and comparable metrics.

## Use When
- Growth plans include experiments or funnel changes.
- Attribution and KPI definitions are inconsistent.

## Inputs Required
- `specs/growth-plan.md`
- `specs/architecture.md`
- Existing analytics schema/events (if available)

## Steps
1. Define core funnel events and canonical event naming.
2. Map each growth initiative to required events and properties.
3. Specify attribution assumptions and known blind spots.
4. Define dashboard/metric ownership and reporting frequency.
5. Create implementation-ready tracking requirements for engineering.

## Output Contract
- Instrumentation section in `specs/growth-plan.md`
- Tracking requirements in `handoffs/growth-to-engineering.md`

## Safety and Security
- Minimize collection of sensitive or unnecessary personal data.
- Align event design with compliance and retention policies.
