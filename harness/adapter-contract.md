# Harness Adapter Contract

This contract defines the minimum interface every framework adapter must implement.

## Required Operations

```text
register_agents(agent_specs) -> adapter_agent_ids
start_run(run_context) -> run_id
dispatch_task(run_id, task_envelope) -> task_id
poll_task(task_id) -> status, partial_output, metrics
cancel_task(task_id) -> cancelled
read_memory(query) -> memory_records
write_memory(memory_records) -> ack
emit_handoff(handoff_envelope) -> handoff_id
request_human_decision(decision_payload) -> decision_result
finalize_run(run_id) -> final_report
```

## Canonical Envelopes

- `task_envelope`
  - `task_id`, `phase`, `source_agent`, `target_agent`, `inputs`, `acceptance_criteria`, `deadline`, `retry_count`
- `handoff_envelope`
  - `handoff_id`, `source_agent`, `target_agent`, `status`, `deliverables`, `open_questions`, `constraints`
- `memory_record`
  - `record_id`, `type`, `source`, `timestamp`, `ttl`, `tags`, `content_hash`, `content_ref`
- `execution_metrics`
  - `latency_ms`, `tokens_in`, `tokens_out`, `tool_calls`, `estimated_cost_usd`, `retry_count`

## Reliability Rules

- All operations should be idempotent where possible.
- `dispatch_task` and `emit_handoff` must support dedupe via stable ids.
- Adapter must return machine-readable error categories:
  - `transient_error`
  - `validation_error`
  - `permission_error`
  - `dependency_error`
  - `unknown_error`
