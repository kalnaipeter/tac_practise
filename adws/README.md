# AI Developer Workflow (ADW) System — tac_practise

ADW automates software development by integrating GitHub issues with Claude Code CLI to classify issues, generate plans, implement solutions, and create pull requests — all without you in the loop.

## The PETER Framework (and its ZTE evolution)

Every out-of-loop agentic system is built on four pillars:

| Pillar | What It Does | tac_practise Implementation |
|--------|-------------|---------------------------|
| **P — Prompt Input** | How work enters the system | GitHub Issues (`/chore`, `/bug`, `/feature`) |
| **E — Environment** | Safe execution space | Feature branch per issue; **isolated worktrees** for parallel agents |
| **T — Trigger** | What kicks off the agent | Webhook (`trigger_webhook.py`) or Cron (`trigger_cron.py`) |
| **R — Review** | How output is validated | Pull Request → human review → merge |

### Zero-Touch Engineering (ZTE)

ZTE is the evolution from PITER (2 touchpoints: prompt + review) to PITE (1 touchpoint: prompt only).

| Level | Framework | Touchpoints | Scripts |
|-------|-----------|-------------|---------|
| Out-Loop | PITER | Prompt + Review | `adw_sdlc.py`, `adw_sdlc_iso.py` |
| Zero-Touch | PITE | Prompt only | `adw_sdlc_zte_iso.py` (auto-merges) |

Issue format for ZTE: `/chore adw_sdlc_ZTE_iso update the background color`
CRITICAL: `ZTE` must be EXPLICITLY uppercased.

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

# Isolated SDLC (parallel-safe, worktree per agent)
uv run adw_sdlc_iso.py 123

# Zero-Touch Execution (auto-merges to main!)
uv run adw_sdlc_zte_iso.py 123

# Ship phase only (merge to main)
uv run adw_ship_iso.py 123 <adw-id>

# Run continuous monitoring (polls every 20 seconds)
uv run trigger_cron.py

# Start webhook server (for instant GitHub events)
uv run trigger_webhook.py
```

## Isolated Workflows (Zero-Touch Engineering)

All `_iso` scripts run in isolated git worktrees under `trees/<adw_id>/`:
- Each agent gets its own filesystem copy of the repo
- Dedicated port ranges (backend: 9100-9114, frontend: 9200-9214)
- Supports 15 concurrent agents
- State persists in `agents/<adw_id>/adw_state.json`

### Pipeline Overview

| Script | Phases | Ships To Main? |
|--------|--------|----------------|
| `adw_sdlc_iso.py` | Plan → Build → Test → Review → Document | No (creates PR) |
| `adw_sdlc_zte_iso.py` | Plan → Build → Test → Review → Document → Ship | Yes (auto-merge) |
| `adw_ship_iso.py` | Validate state → Merge to main | Yes |

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
├── adw_plan_build.py            # Core pipeline: Plan → Build → PR
├── adw_plan_build_test.py       # Plan → Build → Test (feedback loop) → PR
├── adw_plan_build_review.py     # Plan → Build → Review (spec verification)
├── adw_plan_build_document.py   # Plan → Build → Document
├── adw_plan_build_test_review.py # Plan → Build → Test → Review
├── adw_sdlc.py                  # Full SDLC: Plan → Build → Test → Review → Document
├── adw_test.py                  # Standalone test phase (feedback loop)
├── adw_review.py                # Standalone review phase (spec verification + screenshots)
├── adw_patch.py                 # Standalone patch phase (quick-fix from 'adw_patch' keyword)
├── adw_document.py              # Standalone document phase (docs + conditional_docs update)
├── trigger_webhook.py           # FastAPI webhook receiver for GitHub events
├── trigger_cron.py              # Polling-based trigger for GitHub issues
└── README.md                    # This file
```

## Choosing a Workflow

| Scenario | Workflow | Command |
|----------|----------|---------|
| Quick iteration, trust the code | Plan + Build | `uv run adw_plan_build.py 123` |
| Standard development | Plan + Build + Test | `uv run adw_plan_build_test.py 123` |
| Build + verify matches spec | Plan + Build + Review | `uv run adw_plan_build_review.py 123` |
| Build + auto-documentation | Plan + Build + Document | `uv run adw_plan_build_document.py 123` |
| Full validation + spec review | Plan + Build + Test + Review | `uv run adw_plan_build_test_review.py 123` |
| Production feature (everything) | Full SDLC | `uv run adw_sdlc.py 123` |
| Quick-fix from review/comment | Patch | `uv run adw_patch.py 123` |
| Document existing work | Document | `uv run adw_document.py 123 <adw-id>` |

## ADW Tracking

Every workflow run gets a unique 8-character ADW ID (e.g., `e5f6g7h8`).

- **Branch:** `feat-123-e5f6g7h8-add-search-filter`
- **State:** `agents/e5f6g7h8/adw_state.json` (tracks adw_id, issue_number, branch_name, plan_file, issue_class)
- **Logs:** `agents/e5f6g7h8/execution.log` (or `review_execution.log`, `patch_execution.log`, etc.)
- **Review screenshots:** `agents/e5f6g7h8/reviewer/review_img/`
- **Issue comments:** Prefixed with `e5f6g7h8_agent_name: ✅ status`

State is passed between phases via `adw_state.json`, making phases composable and resumable.

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
| `/review` | Review implementation against spec, capture screenshots |
| `/patch` | Create focused patch plan for specific issue |
| `/document` | Generate feature documentation + update conditional docs |

## One Agent, One Prompt, One Purpose

Each ADW phase uses a **dedicated agent with a focused prompt**. This keeps context windows clean and makes individual prompts improvable:

- **Planner** reads the issue + codebase structure → produces a plan
- **Builder** reads the plan → implements it
- **Tester** reads the validation spec → runs/resolves tests
- **Reviewer** reads the spec + diff + UI → verifies implementation
- **Patcher** reads the review issue → creates minimal fix
- **Documenter** reads the spec + diff + screenshots → generates docs

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
