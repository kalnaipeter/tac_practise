# Lesson 04 — Stay Out The Loop

## Core Concepts

- **Out-of-loop > In-the-loop.** Stop prompting agents manually back and forth. Instead, build autonomous systems that execute entire developer workflows while you're AFK — your product builds itself.
- **The PETER Framework** — the four pillars of an out-of-loop agentic system:
  - **P — Prompt Input:** How work enters the system (GitHub issues, JIRA tickets, Slack messages). The issue *is* the prompt — e.g., `/chore document the adw directory`.
  - **E — (Execution) Environment:** A safe, dedicated environment where the agent runs (feature branch, sandbox, CI runner). Isolated so it can't break production.
  - **T — Trigger:** What kicks off the agent (webhook on issue creation, cron polling every N seconds, manual `adw` comment). The bridge between human intent and agent action.
  - **R — Review:** How the output gets validated (pull requests, automated tests, human review). The agent creates a PR — you review, not write.
- **AI Developer Workflows (ADWs)** — End-to-end automated pipelines that chain agent templates into a complete SDLC: classify issue → create branch → plan → implement → commit → PR.
- **The Agentic Layer** — A Python-based orchestration system (`adws/`) that sits between your issue tracker and your codebase, routing work through specialized agents:
  - `issue_classifier` → determines `/chore`, `/bug`, or `/feature`
  - `sdlc_planner` → generates a spec in `specs/*.md`
  - `sdlc_implementor` → executes the spec
  - `branch_generator`, `committer`, `pr_creator` → handle git operations
- **Two trigger modes:**
  - **Webhook (`trigger_webhook.py`):** Real-time — GitHub fires a webhook on issue events, FastAPI receives it, launches `adw_plan_build.py` in background
  - **Cron (`trigger_cron.py`):** Polling — checks GitHub every 20 seconds for new issues or `adw` comments, triggers the workflow

## Key Takeaways

1. **Your issue tracker becomes your prompt interface.** Creating a GitHub issue IS prompting your agent. The title and body are the `$ARGUMENTS`. Labels, commands (`/chore`, `/bug`, `/feature`) are the routing signals.
2. **The agent chain is: Classify → Branch → Plan → Commit → Implement → Commit → PR.** Each step uses a different slash command template from lesson 3, executed programmatically via `execute_template()`.
3. **Webhooks > Cron for real-time.** Webhooks give instant response (GitHub → FastAPI → background process). Cron is the fallback for environments where webhooks aren't possible.
4. **Every step comments on the issue.** The agent posts progress updates (`✅ Starting ADW workflow`, `✅ Issue classified as: /chore`, `✅ Plan file created`) — you can watch the entire workflow unfold asynchronously.
5. **The ADW ID is the tracking spine.** Every workflow run gets a unique 8-char UUID (`make_adw_id()`). All logs, comments, and branches carry this ID for traceability: `agents/{adw_id}/adw_plan_build/execution.log`.
6. **Health checks validate the system.** Before relying on the autonomous loop, `health_check.py` verifies env vars, git config, Claude CLI, and GitHub auth are all working.
7. **Separation of concerns in agent code:**
   - `data_types.py` — Pydantic models for GitHub issues, agent requests/responses
   - `github.py` — All GitHub operations (fetch issues, post comments, manage PRs)
   - `agent.py` — Claude Code CLI execution layer
   - `utils.py` — ADW ID generation, logging setup
   - `adw_plan_build.py` — The orchestrator that chains everything together

## The PETER Framework in Practice

```
Prompt Input:  GitHub Issue → "/chore document the adw directory"
Trigger:       Webhook (GitHub → FastAPI /gh-webhook endpoint)
               OR Cron (poll every 20s for new issues / "adw" comments)
Environment:   Feature branch (feat-123-a1b2c3d4-document-adw-directory)
               Agent runs in isolated branch, never touches main
Review:        Pull Request created automatically
               Human reviews diff, approves/rejects
```

## Applied Changes

- Created **`adws/`** directory in `tac_practise` with:
  - `README.md` — Documents the ADW system architecture, PETER framework, and how workflows are triggered and executed
  - `adw_plan_build.py` — The core orchestrator script adapted for tac_practise (React + TypeScript context)
  - `trigger_webhook.py` — FastAPI webhook receiver for GitHub issue events
  - `trigger_cron.py` — Polling-based trigger that monitors GitHub for new issues
- Updated **`CLAUDE.md`** to reference the ADW layer and the PETER framework

## Relation to TAC Goal

Lessons 1–3 built the foundation: stop coding (1), equip agents with context (2), encode workflows as templates (3). Lesson 4 is where the system becomes **autonomous**. By connecting an issue tracker → trigger → agent chain → PR, you have a complete "system that builds a system." You file an issue, walk away, and come back to a pull request. The human role shifts from *coder* to *reviewer*. This is the "stay out the loop" mindset — your engineering methodology, encoded in templates and orchestrated by ADWs, runs without you.
