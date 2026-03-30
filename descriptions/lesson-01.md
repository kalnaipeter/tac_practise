# Lesson 01 — Stop Coding

## Core Concepts

- **Stop writing code manually.** Language models in the right agent architecture, running on supercomputers, are vastly superior coders. Engineering was never about typing code — it's about designing systems.
- **Agentic Coding vs AI Coding:** A simple AI coding prompt just asks the model to generate code. An agentic coding prompt leverages the 4 pillars — **CONTEXT, MODEL, PROMPT, TOOLS** — to orchestrate a full workflow (branch, create, run, commit, report) in a single call.
- **Programmable Agentic Coding:** You can invoke agents programmatically from shell scripts, Python, or TypeScript — making them composable and automatable.

## Key Takeaways

1. **Resist the urge to type code manually** — go all-in on agentic coding tools.
2. **Don't code, write prompts and review** — your job is to communicate *what* you want built.
3. **Agentic prompts are structured:** They use action keywords (`RUN`, `CREATE`, `REPORT`) to give agents clear multi-step workflows.
4. **The 4 Agentic Principles:** Every agentic prompt should consider Context, Model, Prompt, and Tools.
5. **Programmable agents** can be triggered from any language (bash, python, typescript) by reading a prompt file and piping it to an agent CLI.

## Environment Setup

The lesson establishes the standard TAC toolchain:
- Claude Code, Astral UV, Git, GitHub CLI
- Python 3.10+, Bun, NPM, Vite, Pytest
- Bash/Shell (WSL on Windows)

## Applied Changes

- Added `.github/prompts/create-component.prompt.md` — a reusable agentic prompt for creating React components, demonstrating the lesson's principle of writing prompts instead of code.

## Relation to TAC Goal

This is the foundation: **stop being the coder, start being the architect.** Building a system that builds a system starts with delegating code-writing to agents entirely. The programmable agentic coding pattern (script → prompt file → agent CLI) is the first building block of automated workflows.
