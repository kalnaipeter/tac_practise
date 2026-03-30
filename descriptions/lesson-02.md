# Lesson 02 — Adopt Your Agent's Perspective

## Core Concepts

- **Your agent is brilliant, but blind.** Every new session starts as a blank instance — ephemeral, no context, no memories. If you want your agent to perform like you would, it needs your perspective: the information, tools, and resources you'd use to solve the problem.
- **The Core Four (In-Agent):** Context, Model, Prompt, Tools — the levers you control directly inside the agent.
- **The 12 Leverage Points** span three layers:
  - **In-Agent:** Context (system prompts, conversation history), Model (LLM selection), Prompt (user instructions), Tools (available functions)
  - **Through-Agent:** Standard Out (command output, logging), Types (schemas, classes, structures), Documentation (3rd party & internal), Tests (self-validation feedback loops)
  - **Around-Agent:** Architecture (codebase structure), Plans (detailed prompts for massive work), Templates (reusable agentic prompts), ADWs (AI Developer Workflows)
- **SDLC for Agents:** Plan → Code → Test → Review → Document — agents follow the same cycle, but you must equip them for each phase.

## Key Takeaways

1. **Before launching an agent, ask:** "With my agent's core four (context, model, prompt, tools), is it possible to complete the task I've given it?"
2. **Standard output is agent visibility** — clear logging and consistent command output let your agent see what's happening.
3. **Types guide your agent** — TypeScript types, Pydantic models, and consistent schemas act as guardrails that prevent drift.
4. **Tests are self-validation loops** — write tests so your agent can verify its own work without you.
5. **Architecture is context** — a well-structured codebase gives the agent implicit understanding of where things belong.
6. **Specs, ai_docs, and plans** are how you give your agent the same knowledge you'd have when tackling a complex task.

## Patterns from tac-2 Repo

The tac-2 repo demonstrates the "agent's perspective" principle through its project structure:
- **`specs/`** — Detailed implementation specs (plans) that tell the agent exactly what to build
- **`ai_docs/`** — 3rd party documentation (OpenAI, Anthropic quickstarts) so the agent doesn't hallucinate API usage
- **`.claude/settings.json`** — Tool permissions (allow/deny) that give the agent safe autonomy
- **`.claude/commands/`** — Reusable agent commands (prime, install, tools) for common workflows
- **`agents/` and `adws/`** — Scaffolding for agent configurations and AI Developer Workflows
- **`trees/`** — Codebase structure snapshots for architecture context
- **`scripts/`** — Operational scripts the agent can use (start, stop)

## Applied Changes

- Added **`CLAUDE.md`** — project-level context file giving any agent instant understanding of the codebase, tech stack, commands, architecture, and conventions.
- Added **`specs/`** directory with a sample feature spec — demonstrating how to write plans that agents can execute.
- Added **`ai_docs/`** directory with a README — a home for 3rd party documentation agents need.
- Added **`scripts/`** directory with dev and build scripts — giving agents standard-out visibility via operational tooling.

## Relation to TAC Goal

Lesson 1 said "stop coding, start prompting." Lesson 2 says "your prompts will fail if your agent can't see what you see." This lesson is the bridge from ad-hoc prompting to **systematic agent enablement**. Every leverage point you wire up — types, tests, docs, specs, architecture — makes your "system that builds a system" more reliable and autonomous. The 12 leverage points are the design parameters of that system.
