# Lesson 05 — Always Add Feedback Loops

## Core Concepts

- **Your work is useless unless it's tested.** Agents must act, validate, and correct in a continuous cycle until the job is done right. The closed-loop pattern: **Request → Validate → Resolve**.
- **Closed-loop prompts** — Every agentic prompt should include validation commands. The agent operates on work, calls a command/tool to get feedback on success, then takes that feedback and reruns the build loop until feedback is positive.
- **Feedback mechanisms stack** — Linters, unit tests, type checks, E2E tests, and compile checks are all feedback sources. Chain them together for comprehensive validation.
- **Spending compute on testing increases confidence** — Generative AI can test and resolve at scales you could never achieve by hand. Let agents burn cycles on validation — that's the gift.
- **The `bug.md` pattern** — A spec file that holds all validation steps for closing the loop when solving a problem. It defines what "done" means in terms of passing commands.
- **`adw_plan_build_test`** — Extends the plan→build pipeline with a test phase. The ADW now has three stages: plan the work, build the work, test the work. If tests fail, resolve and rerun.

## Key Takeaways

1. **Add validation commands to every agentic prompt.** No prompt is complete without a validation section that proves the work is correct.
2. **IMPORTANT: If you run into any errors at all, stop and resolve them immediately, then rerun every validation step.** This is the core feedback loop — never skip re-validation after a fix.
3. **Create closed-loop prompts: request, validate, resolve.** The agent doesn't just do the work — it proves the work is right, and if it's not, it fixes it.
4. **Set up end-to-end tests for high-ROI agent self-validation.** E2E tests give agents the strongest feedback signal — they validate the whole system, not just units.
5. **Chain feedback mechanisms for comprehensive testing.** Run linter, then type check, then unit tests, then E2E — each layer catches different classes of errors.
6. **ADW files cover any procedure** — test, plan, implement. The ADW system is flexible enough to encode any workflow stage.

## The Feedback Loop Pattern

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   REQUEST    │────▶│   VALIDATE   │────▶│   RESOLVE    │
│  (do work)   │     │ (run checks) │     │ (fix errors) │
└──────────────┘     └──────┬───────┘     └──────┬───────┘
                            │                     │
                            │  ✅ All pass        │  Loop back
                            ▼                     │
                       ┌─────────┐                │
                       │  DONE   │◀───────────────┘
                       └─────────┘     (until green)
```

## Validation Stack for tac_practise

| Layer | Command | What It Catches |
|-------|---------|----------------|
| Lint | `npm run lint` | Code style, unused vars, import errors |
| Type Check | `npm run build` (includes tsc) | Type errors, interface mismatches |
| Unit Tests | `npm test` (when configured) | Logic errors, regressions |
| E2E Tests | Playwright / browser tests | UI bugs, integration failures |

## Applied Changes

- Created **`specs/bug.md`** — Validation spec that defines all feedback loop steps for closing the loop when solving a bug. Includes bug plan format template and the feedback loop protocol.
- Created **`specs/test.md`** — Application validation test suite defining the exact test execution sequence (lint → build → unit tests → E2E) with structured JSON output format. This is the core of what the agent runs to validate.
- Created **`specs/resolve-failed-test.md`** — The "Resolve" step of the cycle. Tells the agent how to analyze, reproduce, fix, and re-validate a specific failing test.
- Created **`adws/adw_plan_build_test.py`** — Extended the ADW pipeline to include a test/validation phase after build. Runs validation commands and loops until all pass.
- Created **`adws/adw_test.py`** — Standalone test ADW that runs the validation feedback loop independently. Can be chained after `adw_plan_build.py` or run on its own against any branch.
- Updated **`CLAUDE.md`** to include feedback loop validation instructions — every agent session now has closed-loop validation as a core directive.

### ADW File Coverage ("ADW files cover any procedure")

| ADW Script | Phase | Usage |
|---|---|---|
| `adw_plan_build.py` | Plan + Build | `uv run adw_plan_build.py <issue>` |
| `adw_plan_build_test.py` | Plan + Build + Test | `uv run adw_plan_build_test.py <issue>` |
| `adw_test.py` | Test only | `uv run adw_test.py <issue> [adw-id]` |

## Relation to TAC Goal

Lessons 1–4 built the system: stop coding, give agents context, template your workflows, automate the loop. Lesson 5 makes the system **trustworthy**. Without feedback loops, your autonomous agents are just generating code into a void — you can't ship what you haven't validated. By embedding validation into every prompt, spec, and ADW, you create agents that self-certify their work. This is what makes "build a system that builds a system" production-grade: the system doesn't just build — it proves what it built is correct.
