# Context Engineering Guide — R&D Framework

> A focused agent is a performant agent.

## The Problem

The context window is the PRECIOUS and DELICATE resource that determines your agent's performance. There's a sweet spot — too little context and the agent can't reason; too much and it loses focus, hallucinates, or ignores instructions.

## The Framework: R&D (Reduce & Delegate)

There are only two ways to manage your context window:

### Reduce
Remove junk context, minimize token usage, focus on what matters.
- Prune irrelevant files from context before working
- Use concise output styles (see `ai_docs/output-styles.md`)
- Reset and re-prime instead of accumulating stale context
- Read files incrementally when full content isn't needed

### Delegate
Offload work to sub-agents, separate agents, or specialized systems.
- Use sub-agents for isolated tasks (docs scraping, research)
- Use the Architect/Editor pattern (plan in one session, build in another)
- Use background agents for parallel work streams
- Each agent gets exactly the context it needs — no more

## Techniques by Level

### Beginner

| # | Technique | Framework | Key Insight |
|---|-----------|-----------|-------------|
| 1 | Measure to manage | Foundation | You can't optimize what you don't measure. Check context usage regularly. |
| 2 | Avoid unnecessary MCP servers | Reduce | MCP servers consume context on startup. Only load what you need. |
| 3 | More prime, less CLAUDE.md | Reduce | Keep CLAUDE.md minimal (universals only). Use `/prime` variants for task-specific context. |

### Intermediate

| # | Technique | Framework | Key Insight |
|---|-----------|-----------|-------------|
| 4 | Control output tokens | Reduce | Output tokens cost 3-5x more and get added back to context. Compound costs over many prompts. |
| 5 | Use sub-agents properly | Delegate | Sub-agent system prompts stay isolated. They return concise reports, not full dumps. |
| 6 | Architect/Editor pattern | R&D | Planner wastes tokens finding context (its job). Builder gets clean context for precise execution. |

### Advanced

| # | Technique | Framework | Key Insight |
|---|-----------|-----------|-------------|
| 7 | Reset + prime (not compact) | Reduce | `/compact` leaves unknown state. Clear and re-prime for exact, known context. Never exceed 200k tokens. |
| 8 | Context bundles | Reduce | Track files read/written per session in JSONL. Reload exact context for fresh agents. |
| 9 | One agent, one purpose | R&D | Forces single focus. Plan the agent pipeline. Maximum performance per agent. |

### Agentic

| # | Technique | Framework | Key Insight |
|---|-----------|-----------|-------------|
| 10 | System prompt control | Reduce | Fine-tune agent behavior at the deepest level. Trade time for context efficiency. |
| 11 | Primary multi-agent delegation | Delegate | Fully independent agents with complete context isolation. Agents orchestrating agents. |
| 12 | Agent experts | R&D | Self-improving agents with plan→build→improve cycles. Expertise compounds over time. |

## Copilot-Adapted Practices

These techniques map to the Copilot workflow in this project:

| Lesson Technique | Copilot Equivalent |
|---|---|
| `/prime` dynamic priming | `/prime`, `/prime-bug`, `/prime-feature`, `/prime-testing` |
| Concise output styles | Keep responses focused; avoid verbose explanations when not needed |
| Sub-agent delegation | Copilot subagents via prompt composition |
| Architect/Editor pattern | `/quick-plan` → review spec → `/build` |
| Context bundles | `/load-bundle` prompt for replaying previous session context |
| Background agents | `/background` prompt for parallel autonomous work |
| Agent experts (plan/build/improve) | `experts/*.prompt.md` with `/expert-improve` for self-improvement loop |
| One agent one purpose | Each prompt file has a single responsibility |

## Anti-Patterns

- **Bloated CLAUDE.md** — Don't document everything in one file. Use dynamic priming instead.
- **Never measuring context** — Without measurement, optimization is guesswork.
- **Using compact as a fix** — Compact loses information unpredictably. Reset + prime is deterministic.
- **Loading all MCP servers globally** — Each server adds startup context cost. Load only what you need.
- **Monolithic agents** — One agent doing everything = unfocused context = poor output quality.
- **Verbose output by default** — Every output token gets added back to context. Compound costs kill performance.

## Decision Tree: When to Apply What

```
Starting work?
├── New session → /prime (or /prime-bug, /prime-feature, /prime-testing)
├── Resuming previous work → /load-bundle <path>
└── Parallel task → /background

Planning work?
├── Simple fix → /patch directly
├── Feature → /quick-plan → review → /build
└── Complex feature → /feature → review spec → /implement

Context getting large?
├── Under 100k tokens → Keep working
├── 100k-200k tokens → Finish current task, then reset + prime
└── Over 200k tokens → STOP. Split the task. Reset + prime.

Improving agents?
├── After shipping a feature → /expert-improve <expert-path>
└── Periodically → Review and trim CLAUDE.md, check for stale context
```
