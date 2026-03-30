# AI Developer Workflow (ADW) System — tac_practise

ADW automates software development by integrating GitHub issues with Claude Code CLI to classify issues, generate plans, implement solutions, and create pull requests — all without you in the loop.

## The PETER Framework

Every out-of-loop agentic system is built on four pillars:

| Pillar | What It Does | tac_practise Implementation |
|--------|-------------|---------------------------|
| **P — Prompt Input** | How work enters the system | GitHub Issues (`/chore`, `/bug`, `/feature`) |
| **E — Environment** | Safe execution space | Feature branch per issue, isolated from `main` |
| **T — Trigger** | What kicks off the agent | Webhook (`trigger_webhook.py`) or Cron (`trigger_cron.py`) |
| **R — Review** | How output is validated | Pull Request → human review → merge |

## How It Works

```
┌──────────────┐     ┌──────────────┐     ┌──────────────────────────────┐     ┌────────────┐
│ GitHub Issue  │────▶│   Trigger    │────▶│     adw_plan_build.py        │────▶│ Pull Request│
│ /chore ...    │     │ webhook/cron │     │ classify→branch→plan→build→PR│     │ for review  │
└──────────────┘     └──────────────┘     └──────────────────────────────┘     └────────────┘
```

### The ADW Pipeline (adw_plan_build.py)

1. **Fetch Issue** — Reads the GitHub issue details via `gh` CLI
2. **Classify** — Determines issue type: `/chore`, `/bug`, or `/feature`
3. **Branch** — Creates a feature branch: `feat-123-a1b2c3d4-add-dark-mode`
4. **Plan** — Generates an implementation plan in `specs/*.md` using the appropriate template
5. **Commit Plan** — Commits the spec file
6. **Implement** — Executes the plan against the codebase
7. **Commit Implementation** — Commits all changes
8. **Create PR** — Opens a pull request linking back to the issue

Every step posts a status comment on the issue so you can watch progress asynchronously.

## Quick Start

### Prerequisites

- Python 3.10+ with [uv](https://docs.astral.sh/uv/)
- [GitHub CLI](https://cli.github.com/) (`gh auth login`)
- Claude Code CLI
- Anthropic API key

### 1. Set Environment Variables

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
export CLAUDE_CODE_PATH="claude"           # or full path from `which claude`
export GITHUB_PAT="ghp_..."               # Optional: only if different account than gh auth
```

### 2. Run ADW

```bash
cd adws/

# Process a single issue manually
uv run adw_plan_build.py 123

# Run continuous monitoring (polls every 20 seconds)
uv run trigger_cron.py

# Start webhook server (for instant GitHub events)
uv run trigger_webhook.py
```

## Trigger Modes

### Webhook (Real-time)

`trigger_webhook.py` runs a FastAPI server that receives GitHub webhook events:

- **Endpoint:** `POST /gh-webhook`
- **Health:** `GET /health`
- **Default port:** 8001

**Setup in GitHub:** Repository → Settings → Webhooks → Add webhook
- Payload URL: `https://your-server/gh-webhook`
- Content type: `application/json`
- Events: Issues, Issue comments

Triggers when:
- A new issue is **opened**
- Someone comments **"adw"** on any issue

### Cron (Polling)

`trigger_cron.py` polls GitHub every 20 seconds:

- Finds issues with **no comments** (new issues)
- Finds issues where the **latest comment is "adw"**
- Launches `adw_plan_build.py` for each qualifying issue

Best for environments where webhooks can't be exposed publicly.

## File Structure

```
adws/
├── adw_plan_build.py      # Core orchestrator — chains the full pipeline
├── trigger_webhook.py     # FastAPI webhook receiver for GitHub events
├── trigger_cron.py        # Polling-based trigger for GitHub issues
├── agent.py               # Claude Code CLI execution layer
├── github.py              # GitHub operations (fetch issues, post comments, PRs)
├── data_types.py          # Pydantic models for issues, requests, responses
├── utils.py               # ADW ID generation, logging setup
├── health_check.py        # System health validation
└── README.md              # This file
```

## ADW Tracking

Every workflow run gets a unique 8-character ADW ID (e.g., `e5f6g7h8`).

- **Branch:** `feat-123-e5f6g7h8-add-search-filter`
- **Logs:** `agents/e5f6g7h8/adw_plan_build/execution.log`
- **Issue comments:** Prefixed with `e5f6g7h8_agent_name: ✅ status`

## Agent Templates Used

The ADW system invokes these slash command templates (from `.github/prompts/`):

| Template | Purpose |
|----------|---------|
| `/classify_issue` | Determine if issue is `/chore`, `/bug`, or `/feature` |
| `/chore` | Generate a chore plan in `specs/*.md` |
| `/bug` | Generate a bug fix plan with root cause analysis |
| `/feature` | Generate a feature plan with user story and phases |
| `/implement` | Execute a plan from `specs/*.md` |
| `/generate_branch_name` | Create semantic branch name |
| `/commit` | Stage and commit with formatted message |
| `/pull_request` | Push branch and create PR via `gh` |

## Example Flow

```
You: Create issue → "/chore add loading spinner to country table"

Agent:
  ✅ Starting ADW workflow (ID: a1b2c3d4)
  ✅ Issue classified as: /chore
  ✅ Working on branch: chore-42-a1b2c3d4-add-loading-spinner
  ✅ Building implementation plan
  ✅ Plan file created: specs/add-loading-spinner-plan.md
  ✅ Committing plan
  ✅ Implementing solution
  ✅ Solution implemented
  ✅ Committing implementation
  ✅ Pull request created: https://github.com/owner/repo/pull/43
  ✅ ADW workflow completed successfully

You: Review the PR, approve, merge. Done.
```
