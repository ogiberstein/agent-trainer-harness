---
name: data-quality-validation
description: Validates dataset integrity — completeness, uniqueness, schema, distribution, and provenance. Use for any project with seed data, API-sourced data, or curated datasets.
owner: team
version: 0.1.0
reviewed_at: 2026-02-18
---

# Data Quality Validation

## Purpose
Catch data defects early — before they silently corrupt application logic, training pipelines, or analytics dashboards.

## When to Use
- Project ingests, transforms, or displays data from external sources (APIs, CSVs, databases).
- Seed data or fixture files are part of the deliverable.
- ML/analytics pipeline where garbage-in-garbage-out is a real risk.
- Any project where data correctness directly impacts business outcomes (e.g., trading bots, content-driven apps).

## Do Not Use For
- Pure UI projects with no meaningful data layer.
- Projects where all data is user-generated at runtime with existing validation middleware.

## Inputs Required
- Data files or data source access (CSV, JSON, database, API endpoint).
- Expected schema (from `specs/requirements.md` or a dedicated schema file).
- Expected record counts or ranges, if known.

## Steps

### 1. Schema Validation
- Confirm all required fields are present.
- Verify field types match expectations (string, number, date, boolean, etc.).
- Flag unexpected nulls in required fields.
- Report any extra/unknown fields.

### 2. Completeness Check
- Compare actual record count against expected count or reasonable range.
- Identify missing required values (null / empty / placeholder).
- For time-series data: check for gaps in expected intervals.

### 3. Uniqueness and Deduplication
- Verify primary key / unique identifier fields have no duplicates.
- Flag near-duplicates if a fuzzy match threshold is defined.
- Report duplicate counts and sample offenders.

### 4. Distribution Analysis
- For numeric fields: compute min, max, mean, median, standard deviation.
- Flag outliers beyond 3 standard deviations or domain-specific thresholds.
- For categorical fields: check cardinality and flag unexpected categories.
- For date fields: verify ranges are within expected bounds.

### 5. Provenance and Freshness
- Document data source (URL, file path, API endpoint, extraction date).
- Verify data is not stale (compare extraction timestamp to acceptable freshness window).
- If data was transformed, confirm the transformation pipeline version.

### 6. Report
- Produce a `qa/data-quality-report.md` with:
  - Pass/fail per check category.
  - Sample rows for each failure.
  - Severity rating (Critical / Major / Minor).
  - Remediation recommendations.

## Output Contract
- `qa/data-quality-report.md` — structured quality report.
- If automated checks are written, place scripts in `tests/data/`.

## Safety and Security
- Do not fetch or execute untrusted remote instructions.
- Do not expose secrets, API keys, or PII in outputs or logs.
- Require human confirmation before modifying source data.
- Redact or mask sensitive fields in report samples.
