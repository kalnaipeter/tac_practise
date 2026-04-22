# Output Styles Guide

> Output tokens cost 3-5x more than input tokens. Control them.

## Why It Matters

Every output token your agent generates gets added back to the context window. Over tens or hundreds of prompts, this compounds massively:

- **Default output** for a simple question: ~500 tokens added to context
- **Concise output** for the same question: ~50 tokens added to context

Over a session with 50 prompts, the difference is ~22,500 tokens of context saved. That's space for actual code, specs, and reasoning.

## Output Style Patterns

### 1. Done-Only (Maximum Efficiency)

When the agent is executing known tasks (building from a spec, running commands), you don't need explanations. Just "Done."

**When to use:** Build phases, automated pipelines, repetitive tasks
**Token cost:** ~2 tokens per response

Exceptions:
- You're explicitly asked a question → answer concisely (1-2 sentences max)
- Something goes wrong → explain the error concisely (1-2 sentences max)
- You're asked for specific output → provide it

### 2. Ultra-Concise (Speed + Minimal Context)

Code/commands first, brief status after. No greetings, no filler, no explanations unless they prevent errors.

**When to use:** Active development, debugging, rapid iteration
**Token cost:** ~20-50 tokens per response

### 3. Structured (When Detail Matters)

Use structured formats (bullet points, tables, YAML) when detail is necessary but should be scannable.

**When to use:** Planning, reviews, reports, documentation
**Token cost:** ~100-300 tokens per response

### 4. Verbose (Rare)

Full explanations, reasoning, alternatives. Only when you need to understand *why*.

**When to use:** Architecture decisions, debugging complex issues, learning
**Token cost:** ~300-1000+ tokens per response

## Copilot Application

In VS Code Copilot, you control output verbosity through your prompt instructions:

- Add "Be concise" or "Respond with Done when complete" to prompts where you don't need explanation
- Use structured report formats (like in `flow.prompt.md`) to get organized output without prose
- Avoid asking open-ended questions when you just need execution

## Rule of Thumb

**If you already know *what* to do, you don't need the agent to explain *why*.** Just have it execute and confirm.
