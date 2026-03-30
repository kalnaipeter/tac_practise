# Lesson 3 — Template Your Engineering

## Core Concepts

- **Engineering templates as reusable agentic units** — Encode your problem-solving patterns (bug fixes, chores, features, refactors) into slash-command templates that agents can execute consistently across any codebase.
- **Meta-prompts** — Higher-order prompts that generate plans. A `/bug` command doesn't fix the bug — it creates a structured plan in `specs/*.md` that a separate `/implement` command then executes. Plans into plans.
- **Information-dense keywords** — Phrases like `THINK HARD` and `IMPORTANT` act as attention anchors, directing the agent's reasoning effort to critical sections (root-cause analysis, execution order).
- **$ARGUMENTS passthrough** — Templates accept runtime arguments (`/bug "sql injection in query builder"`) that get injected into the template, making each command a parameterized workflow.
- **Plan Format as a contract** — Every template enforces a strict markdown structure (Description → Relevant Files → Steps → Validation Commands) so output is predictable, reviewable, and implementable.
- **Separation of planning and execution** — Planning commands (`/bug`, `/feature`, `/chore`) produce specs. The `/implement` command consumes specs. This two-phase approach gives you a review checkpoint before code changes.

## Key Takeaways

1. **Don't code — template.** Instead of solving individual problems, create templates that solve *classes* of problems. One `/bug` template handles every bug, forever.
2. **Structured output > freeform output.** Enforcing a Plan Format means every plan has root cause analysis, step-by-step tasks, and validation commands. No guessing what the agent will produce.
3. **Commands are composable.** `/install` calls `/prime`, `/implement` takes any spec. Small templates chain into larger workflows.
4. **THINK HARD and IMPORTANT are strategic directives.** They're not decoration — they focus the agent's reasoning on the parts that matter most (bug root cause, task execution order).
5. **Validation is built into every template.** Every plan ends with `Validation Commands` — the agent must prove its work. No "trust me, it works."
6. **The specs/ folder becomes your system of record.** Every planned change lives as a reviewable markdown file before any code is touched.

## Applied Changes

- Created `.github/prompts/` directory with command templates adapted for the tac_practise React + TypeScript app:
  - `bug.md` — Bug planning: creates a spec with root cause analysis, fix steps, and validation
  - `chore.md` — Chore planning: creates a spec for maintenance/cleanup tasks
  - `feature.md` — Feature planning: creates a spec with user story, phased implementation, and testing strategy
  - `implement.md` — Plan execution: reads a spec and implements it, then reports changes
- Each template uses `$ARGUMENTS` for parameterized input, `THINK HARD` for reasoning focus, and `IMPORTANT` for execution order
- Templates point to tac_practise's architecture (`src/components/`, `src/services/`, `src/types/`)
- Validation commands use `npm run build` and `npm run lint` (matching the tac_practise tech stack)

## Relation to TAC Goal

Lesson 3 is where the system starts *scaling*. Lessons 1–2 established programmable prompts and project structure. Now you encode your engineering workflows into reusable templates — the agent doesn't just follow instructions, it follows your *methodology*. Every `/bug` produces plans in the same format, every `/feature` follows the same phases, every plan gets validated the same way. You're building a system where your engineering judgment is embedded in templates that any agent can execute repeatedly. This is the "builds a system" part of "build a system that builds a system."
