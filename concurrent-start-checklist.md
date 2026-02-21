# Concurrent Mode — Start Checklist

Step-by-step checklist for launching a fully autonomous, concurrent project run. Each step has a checkbox so you (or an agent) can track progress.

---

## Prerequisites

- [ ] Python 3.10+ installed (`python3 --version`)
- [ ] Claude Code CLI installed and authenticated (`claude --version`)
- [ ] Git installed; project is a git repo with at least one commit

## Setup (new project)

- [ ] Clone the harness: `git clone https://github.com/ogiberstein/agent-trainer-harness.git my-project && cd my-project`
- [ ] Fill in `BRIEF.md` — project scope, target users, constraints, success criteria
- [ ] Edit `profiles/project-profile.yaml` — tech stack, quality bars, naming conventions
- [ ] Edit `runtime/config.yaml`:
  - [ ] `model` — which Claude model workers use
  - [ ] `max_workers` — how many parallel workers (default: 3)
  - [ ] `notification_webhook` — Slack or Telegram webhook URL (see "Webhook Setup" below)
  - [ ] `project_name` — display name for notifications
  - [ ] `skip_phases` — list any phases to skip (e.g., `["growth"]`)
- [ ] Install Python deps: `pip install -r runtime/requirements.txt`

## Setup (existing project)

- [ ] Run `bash starter_kit_existing_projects/core/copy_core.sh --preset full /path/to/project` (or `--preset backend`)
- [ ] `cd /path/to/project`
- [ ] Fill in `BRIEF.md`, `profiles/project-profile.yaml`, `runtime/config.yaml` (same as above)
- [ ] Install Python deps: `pip install -r runtime/requirements.txt`
- [ ] Optionally run the alignment flow: paste `starter_kit_existing_projects/alignment/EXISTING_PROJECT_ALIGNMENT_PROMPT.md` into your IDE

## Launch

- [ ] Optional dry run: `python runtime/run.py --project . --dry-run`
- [ ] Start the orchestrator: `python runtime/run.py --project .`
- [ ] Wait for Requirements notification (webhook + terminal output)
- [ ] Review `specs/requirements.md` — edit if needed
- [ ] Resume: `python runtime/run.py --project . --resume`
- [ ] Walk away — phases 2-7 run autonomously

## While It Runs (optional monitoring)

- `python cli/harness_cli.py --project . status` — current phase + task counts
- `python cli/harness_cli.py --project . task list` — all tasks with status
- Watch `STATUS.md` for phase progression
- Watch `logs/runs.jsonl` for telemetry events
- Worker output: `.worktrees/<task-id>/.worker_output.txt`

## When It Finishes

- [ ] Receive "complete" notification via webhook
- [ ] Run `python cli/validate_harness.py --project .` to verify harness consistency
- [ ] Review deliverables: `specs/`, `src/`, `tests/`, `docs/`, `qa/`
- [ ] Review decisions: `DECISIONS.md`

## Stopping / Pausing

- Graceful pause: `touch runtime/.checkpoint` (workers finish current task, then orchestrator pauses)
- Resume after pause: `python runtime/run.py --project . --resume`
- Abort: kill the orchestrator process

---

## Webhook Setup

Notifications are optional but recommended — they tell you when the orchestrator needs you (requirements review) or has finished.

### Slack

1. Go to [api.slack.com/messaging/webhooks](https://api.slack.com/messaging/webhooks)
2. Create a new Slack app (or use an existing one)
3. Enable "Incoming Webhooks" and add a webhook to your channel
4. Copy the URL (looks like `https://hooks.slack.com/services/T.../B.../xxx`)
5. Paste into `runtime/config.yaml`:
   ```yaml
   notification_webhook: "https://hooks.slack.com/services/T.../B.../xxx"
   ```

The harness sends a JSON payload with a `text` field, which Slack renders natively.

### Telegram

1. Message [@BotFather](https://t.me/BotFather) on Telegram and create a new bot
2. Copy the bot token (looks like `123456:ABC-DEF1234...`)
3. Send any message to your bot, then get your chat ID:
   ```
   https://api.telegram.org/bot<TOKEN>/getUpdates
   ```
   Look for `"chat":{"id": 12345678}` in the response.
4. Your webhook URL is:
   ```
   https://api.telegram.org/bot<TOKEN>/sendMessage?chat_id=<CHAT_ID>
   ```
   **However**, the Telegram `sendMessage` API expects `text` in the body, which the harness already sends. Set it as:
   ```yaml
   notification_webhook: "https://api.telegram.org/bot<TOKEN>/sendMessage?chat_id=<CHAT_ID>"
   ```

### Generic webhook

Any service that accepts POST with a JSON body containing `text`, `project`, `level`, and `timestamp` fields will work. The harness uses `requests.post(url, json=payload)`.

### No webhook (local only)

Leave `notification_webhook: ""` in config. All notifications still print to the terminal where the orchestrator is running.
