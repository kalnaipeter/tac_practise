# Agentic Layer Guide

> The ring around your codebase where you template your engineering.

## The Most Important Question

**Am I working on the agentic layer or the application layer?**

If you're editing React components, fixing CSS, or adding data — you're on the application layer. If you're writing prompts, improving specs, building ADWs, or refining agent context — you're on the agentic layer.

**Target: 50%+ of engineering time on the agentic layer.**

## The 12 Leverage Points

These are the levers that make agents more capable. Ordered from most direct to most systemic:

| # | Leverage Point | Location | Impact |
|---|---------------|----------|--------|
| 1 | Context | `CLAUDE.md`, `ai_docs/` | Agent understands the project |
| 2 | Model | Model selection per phase | Capability ceiling |
| 3 | Prompt | `.github/prompts/`, `.claude/commands/` | Instruction quality determines output quality |
| 4 | Tools | MCP servers, CLI tools | What agents can do |
| 5 | Standard Output | JSON/JSONL, structured reports | Composable results between phases |
| 6 | Types | TypeScript interfaces, Pydantic models | Constraint enforcement |
| 7 | Docs | `ai_docs/`, `app_docs/` | Agent reference material |
| 8 | Tests | Test-fix loops, validation commands | Prove correctness |
| 9 | Architecture | Component patterns, service layers | Structural clarity for agents |
| 10 | Plans | `specs/` | Two-phase: plan then execute |
| 11 | Templates | Prompt templates, plan formats | Reusable across problem instances |
| 12 | AI Developer Workflows | `adws/` | Full pipeline orchestration |

## Agentic Layer Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     AGENTIC LAYER                           │
│                                                             │
│  Triggers          ADWs              Prompts/Commands       │
│  ┌──────────┐     ┌──────────────┐   ┌──────────────────┐  │
│  │ webhook  │────▶│ adw_sdlc.py  │──▶│ /feature         │  │
│  │ cron     │     │ adw_test.py  │   │ /implement       │  │
│  │ tasks.md │     │ adw_review   │   │ /test            │  │
│  │ AEA      │     │ ...          │   │ /review          │  │
│  └──────────┘     └──────────────┘   └──────────────────┘  │
│                          │                    │              │
│                    Plans/Specs          Context/Docs         │
│                   ┌──────────┐       ┌──────────────────┐   │
│                   │ specs/   │       │ CLAUDE.md        │   │
│                   │ *.md     │       │ ai_docs/         │   │
│                   └──────────┘       │ app_docs/        │   │
│                                      └──────────────────┘   │
├─────────────────────────────────────────────────────────────┤
│                   APPLICATION LAYER                          │
│  src/components/  src/services/  src/types/  index.html     │
└─────────────────────────────────────────────────────────────┘
```

## Minimum Viable Agentic Layer

To get started, you need only three things:

1. **Prompts** — Templates for `/chore`, `/feature`, `/bug`, `/implement`
2. **Plans** — Specs in `specs/` that guide agent execution
3. **ADWs** — Workflow scripts that chain prompts into pipelines

This project already has all three. The path forward is improving and expanding them.

## Composable Pipeline Progression

Build from small to large:

```
Prompt          →  Single instruction (e.g., /feature)
Plan            →  Structured spec from a prompt
ADW (2-phase)   →  Plan → Build
ADW (3-phase)   →  Plan → Build → Test
ADW (full)      →  Plan → Build → Test → Review → Document
ADW (ZTE)       →  Plan → Build → Test → Review → Document → Ship
Cron Trigger    →  Auto-run ADWs on schedule
Task File       →  Parallel multi-agent with tasks.md
AEA             →  Agents embedded in the application
```

## Multi-Agent Task Tracking (tasks.md)

For parallel work, use `tasks.md` with status tracking:

| Symbol | Status | Meaning |
|--------|--------|---------|
| `[]` | Pending | Ready for pickup |
| `[⏰]` | Blocked | Waits for previous tasks |
| `[🟡]` | In progress | Agent working (with ADW ID) |
| `[✅]` | Completed | Done (with commit hash) |
| `[❌]` | Failed | Error (with reason) |

Tasks are grouped by git worktree. Each worktree is an isolated branch for parallel agent execution.

## Daily Actions

1. Spend 50%+ of time on the agentic layer
2. Focus on primitives and composable units
3. Build from prompts to ADWs to full pipelines
4. Template engineering for problem classes, not one-offs
5. Ask: "Am I working on the agentic layer or the application layer?"

## Auditing Your Work

Use `/agentic-audit` to check whether your recent work was on the agentic or application layer, and get recommendations for agentic improvements.
