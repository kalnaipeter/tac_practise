# Lesson 10 — Elite Context Engineering

## Lesson Title
Elite Context Engineering (TAC-10)

## Core Concepts

### The R&D Framework
Context engineering is the practice of deliberately selecting, shaping, and managing the information placed into an AI system's context window. There are only two ways to manage context effectively:

- **Reduce** — Remove junk context, minimize token usage, focus on what matters
- **Delegate** — Offload work to sub-agents, separate agents, or specialized systems

### Four Levels of Context Engineering

**Beginner — Foundation:**
1. **Measure to manage** — Use `/context` to see what your agent processes every prompt. Without measuring, you're just vibe coding.
2. **Avoid MCP servers** — MCP servers consume context on startup. Only load them when needed, not globally.
3. **More prime, less CLAUDE.md** — CLAUDE.md is always loaded. Keep it minimal (absolute universals only). Use dynamic `/prime` commands for task-specific context.

**Intermediate — R&D in action:**
4. **Control output tokens** — Output tokens cost 3-5x more than input and get added back to context. Use concise output styles to reduce compound costs.
5. **Use sub-agents properly** — Sub-agent system prompts stay isolated from primary context. They return concise reports, not full data dumps.
6. **Architect/Editor pattern** — Separate planning from implementation. Planner wastes tokens finding context (that's its job). Builder gets crystal-clear context for error-free execution.

**Advanced — Systematic control:**
7. **Avoid compact, reset + prime** — `/compact` is a bandaid with unknown state. Use `/clear` + `/prime` for exact, known context. Never exceed 200k tokens — split the task instead.
8. **Context bundles** — Track files read/written per session in JSONL. Reload exact previous context with `/load_bundle`. Enables instant context restoration for fresh agents.
9. **One agent, one purpose** — Forces you to define the agent's single purpose, plan the agent pipeline, and execute with maximum focus.

**Agentic — Bleeding edge:**
10. **System prompt control** — `--append-system-prompt` for fine-tuned behavior (e.g., force 100-line incremental reads). Trades time for context efficiency.
11. **Primary multi-agent delegation** — Orchestrate multiple fully independent agent instances. Complete context isolation. `/background` command for parallel work.
12. **Agent experts** — Self-improving specialized agents with plan→build→improve cycles. The improve step updates the expert's own knowledge for future runs.

## Key Takeaways

- **A focused agent is a performant agent** — The golden rule. Every technique serves this principle.
- **Context window is PRECIOUS and DELICATE** — There's a sweet spot. Too little = agent can't reason. Too much = agent loses focus.
- **Search and destroy** — Find the right context agentically, remove or delegate everything else.
- **Compound costs** — Output tokens get added back to context. Over hundreds of prompts, even small savings compound massively.
- **Two-phase always** — Separate planning (context gathering/waste) from execution (focused, clean context).
- **Context priming > static files** — Dynamic, controllable setup beats always-on context.

## Applied Changes

### New Prompts
- **`/prime-bug`** — Bug-focused context prime: loads bug-validation, resolve-failed-test, and test prompts
- **`/prime-feature`** — Feature-focused context prime: loads feature, implement, review, and test prompts
- **`/prime-testing`** — Testing-focused context prime: loads test, resolve-failed-test, and bug-validation prompts
- **`/expert-improve`** — Generalized expert improve prompt: reviews recent changes and updates any expert's `### Learnings` section

### New Context Files
- **`ai_docs/context-engineering-guide.md`** — Complete R&D framework reference with all 12 techniques and Copilot-adapted practices
- **`ai_docs/output-styles.md`** — Guide for controlling output verbosity to reduce token waste

### Updated Files
- **`CLAUDE.md`** — Added Context Engineering section with priming guidance and output efficiency rules
- **`copilot-workflow.md`** — Added new prompts to Available Prompts table, updated ADW Coverage Comparison
- **`flow.prompt.md`** — No structural change needed (existing flow already covers the pipeline)

## Relation to TAC Goal

This lesson is the **control system** for the system that builds systems. Without context engineering, agents degrade as complexity grows — they lose focus, waste tokens on irrelevant context, and produce lower-quality output. The R&D framework ensures every agent in the pipeline operates at peak performance:

- **Reduce** keeps each agent focused on its single purpose
- **Delegate** preserves context isolation across the multi-agent pipeline
- **Specialized priming** ensures agents get exactly the context they need — no more, no less
- **Expert self-improvement** creates agents that get smarter over time

Context engineering is the difference between "agents that work on toy problems" and "agents that work on real systems."
