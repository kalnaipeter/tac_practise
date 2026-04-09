# Lesson 8: Prioritize Agentics

## Core Concepts

**"The more time you invest in your agentic layer, the more your agents can solve problem classes autonomously."**

TAC-8 is the capstone lesson — all previous tactics compressed into one principle: **spend at least 50% of your engineering time on the agentic layer, not the application layer.** The agentic layer is the ring around your codebase where you template your engineering. This is where irreplaceable engineers operate differently: building the system that builds the system.

### The 12 Leverage Points

1. **Context** — Agent knowledge (CLAUDE.md, ai_docs/)
2. **Model** — Model selection per phase
3. **Prompt** — Instruction quality (commands/, prompts/)
4. **Tools** — Agent capabilities (MCP, CLI)
5. **Standard Output** — Structured results (JSON, JSONL)
6. **Types** — Data models (Pydantic, TypeScript)
7. **Docs** — Documentation layer (ai_docs/, app_docs/)
8. **Tests** — Validation (test-fix loops)
9. **Architecture** — System design patterns
10. **Plans** — Specifications (specs/)
11. **Templates** — Reusable command templates
12. **AI Developer Workflows** — ADW orchestration scripts

### Agent Layer Primitives (Minimum Viable Agentic Layer)

The minimum agentic layer requires only three things:
- **Prompts/Commands** — Templates for chore, feature, bug, plan, implement
- **ADW files** — Workflow scripts that chain prompts together
- **Plan files** — Specs that guide agent execution

### Five Progressive Architectures (from tac-8 sub-apps)

| App | Architecture | Key Pattern |
|-----|-------------|-------------|
| App 1: Agent Layer Primitives | Single agent + templates | Minimum viable: prompts → ADWs → pipelines |
| App 2: Multi-Agent Todone | Parallel agents via tasks.md | Git worktree isolation, dependency tracking, task status symbols |
| App 3: Observability Dashboard | Hook-based event tracking | Pre/post tool use hooks, real-time monitoring |
| App 4: Agentic Prototyping | Notion-driven task routing | Prototype tags (`{{prototype: type}}`), framework-specific plan templates |
| App 5: NLQ-to-SQL AEA | Full SDLC + AEA server | Zero-touch execution, state chaining, embedded agent application |

### The AEA Pattern (Agent Embedded Application)

The AEA server (`adw_trigger_aea_server.py`) embeds an AI agent directly into the application. Users interact via command palette (Cmd+P → /aea), multiple agents can run in parallel, and the system operates outside the developer loop inside the application itself.

## Key Takeaways

1. **50/50 Rule** — Spend at least half your engineering time on the agentic layer
2. **Primitives first** — Start with prompts + ADWs + plans, then compose into pipelines
3. **Template for problem classes** — Don't solve one-offs; template engineering patterns that solve categories of problems
4. **Composable units** — Build small, focused primitives that chain together (plan → implement → test → review → document → ship)
5. **The daily question** — "Am I working on the agentic layer or the application layer?"
6. **Multi-agent parallelism** — Use git worktrees + task files for parallel agent execution
7. **AEA = agents in the app** — Embed agent interfaces directly into applications for out-of-loop operation
8. **From prompts to full pipelines** — The progression: prompts → ADWs → triggers → full SDLC → ZTE

## TAC-8 Sub-Apps — Detailed Reference

### App 1: Agent Layer Primitives
**What:** The minimum viable agentic layer — `agent.py` module + slash command templates (`/chore`, `/implement`) + basic ADW scripts.
**Use for:** Understanding the foundational building blocks (prompts, ADWs, specs).
**Status in tac_practise:** Fully absorbed — all patterns already applied.
**Future improvements:** None needed.

### App 2: Multi-Agent Todone
**What:** A `tasks.md` file + cron trigger (`adw_trigger_cron_todone.py`) that polls for pending tasks and spawns parallel agents in isolated git worktrees. Tasks have status symbols (`[]`, `[🟡]`, `[✅]`), dependency tracking, and tags for routing.
**Use for:** Running multiple agents in parallel on different tasks — e.g., "add 5 features at once" with each in its own worktree.
**Status in tac_practise:** `tasks.md` format added as reference. Cron trigger not implemented.
**Requirements:** Claude Code CLI + API key. `uv run` + subprocess spawning.
**Future improvements:** Implement `adw_trigger_cron_todone.py` adapted for tac_practise when Claude Code CLI is available. Would enable parallel task execution across worktrees.

### App 3: Observability Dashboard
**What:** Claude Code hooks (`pre_tool_use.py`, `post_tool_use.py`, etc.) that stream events to a Bun server + SQLite + Vue dashboard. Tracks what agents are doing in real time.
**Use for:** Monitoring multi-agent activity, auditing tool usage, blocking dangerous commands (`rm -rf`).
**Requirements:** Claude Code hooks infrastructure. Not applicable to Copilot.
**Status in tac_practise:** Not implemented.
**Future improvements:** If using Claude Code, add hook scripts to `.claude/hooks/` for security guards (block `rm -rf`, `.env` access) and event streaming to a monitoring dashboard.

### App 4: Agentic Prototyping
**What:** A Notion-integrated system. Cron polls a Notion database, detects `{{prototype: vite_vue}}` tags, and spawns agents that auto-generate full prototypes using framework-specific plan templates (`/plan_vite_vue`, `/plan_uv_mcp`, etc.).
**Use for:** Rapid prototyping — describe what you want in Notion, and an agent builds it.
**Requirements:** Notion MCP server + Claude Code CLI.
**Status in tac_practise:** Not implemented.
**Future improvements:** Create framework-specific plan templates (e.g., `/plan-react-component`, `/plan-vite-app`) that could be used standalone via Copilot prompts, even without Notion integration. The prototype tag routing pattern could be adapted to use GitHub Issues as the task source.

### App 5: NLQ-to-SQL with AEA Server
**What:** Full SDLC automation + an AEA (Agent Embedded Application) server. The AEA is a FastAPI server that lets users trigger AI agents from within the app itself (via command palette). It manages agent sessions, conversation history, and subprocess execution.
**Use for:** Embedding agent capabilities directly into your application — users interact with agents without leaving the app.
**Requirements:** Claude Code CLI + API key for the AEA server.
**Status in tac_practise:** SDLC pipelines fully replicated (`adw_sdlc_iso.py`, `adw_sdlc_zte_iso.py`). AEA server not implemented.
**Future improvements:** The AEA pattern is the most advanced architecture. When Claude Code CLI is available, implement `adw_trigger_aea_server.py` to embed agent interaction directly into the tac_practise app. This would allow users to trigger `/feature`, `/bug`, `/chore` workflows from within the running application.

### Summary: What's Available Now vs Future

| App | Available in Copilot? | Needs Claude Code CLI? | Priority for Future |
|-----|----------------------|----------------------|-------------------|
| App 1: Primitives | Yes — fully applied | No | Done |
| App 2: Todone | tasks.md format only | Yes — cron trigger | Medium |
| App 3: Observability | No | Yes — hooks | Low |
| App 4: Prototyping | Plan templates possible | Yes — Notion + cron | Medium |
| App 5: AEA | SDLC pipelines done | Yes — AEA server | High |

## Applied Changes

### New Files
- `ai_docs/agentic-layer-guide.md` — Guide to the agentic layer architecture, the 12 leverage points, and how to prioritize agentic work
- `.github/prompts/agentic-audit.prompt.md` — Prompt to audit whether work is on the agentic or application layer
- `.github/prompts/plan-agentic.prompt.md` — Template for planning agentic layer improvements (prompts, ADWs, specs)
- `adws/adw_plan_build_test_review_document.py` — Convenience alias for the full `adw_sdlc.py` pipeline (explicit phase naming)
- `tasks.md` — Multi-agent task tracking file (todone pattern from App 2)

### Modified Files
- `CLAUDE.md` — Added agentic layer section, 12 leverage points, and routing for new prompts
- `ai_docs/copilot-workflow.md` — Added new prompts, updated version
- `.github/prompts/flow.prompt.md` — Added agentic audit reminder in the report phase

## Relation to TAC Goal

This is the ultimate lesson: **stop coding, start building the system that builds the system.** Every previous lesson (context engineering, prompt engineering, specialized agents, ADWs, ZTE) was building toward this moment. The agentic layer — prompts, plans, ADWs, triggers — is the scalable infrastructure. Application code is the output. By prioritizing the agentic layer, you make every future feature, bug fix, and chore faster because agents can handle them autonomously. This scales any system using the 12 leverage points.
