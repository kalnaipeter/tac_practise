# Lesson 7 — Zero-Touch Engineering

## Core Concepts

**Zero-Touch Engineering (ZTE)** is the third level of agentic coding maturity:

| Level | Name | Touchpoints | Human Role |
|-------|------|-------------|------------|
| 1 | In-Loop | Many | Write code alongside agents |
| 2 | Out-Loop (PETER/PITER) | 2 | Prompt + Review |
| 3 | Zero-Touch (PITE) | 1 | Prompt only |

At the ZTE level, your presence KPI drops from two touchpoints (prompt and review) to just one (prompt only). Agents ship end-to-end with such reliability that human review becomes a bottleneck, not a safety net — work flows directly from prompt to production.

### Key Patterns

- **Isolated Execution (`_iso` suffix):** Every ADW workflow runs in its own git worktree under `trees/<adw_id>/` with dedicated ports, enabling parallel agent pipelines without interference. Supports 15 concurrent instances.
- **Worktree Isolation:** `install_worktree.md` creates a complete, independent copy of the repo — own `.env`, own ports, own MCP config — so multiple agents can execute simultaneously.
- **State Persistence:** `agents/{adw_id}/adw_state.json` tracks all phases of a workflow, enabling chaining (Plan → Build → Test → Review → Document → Ship).
- **Model Selection:** `agent.py` maps each slash command to base/heavy model sets (sonnet/opus). The `classify_adw.md` command extracts `adw_slash_command`, `adw_id`, and `model_set` from issue text.
- **Issue-Driven Workflows:** All work starts from GitHub Issues using slash commands:
  - `/feature adw_sdlc_iso` — full SDLC for features
  - `/bug adw_sdlc_iso` — full SDLC for bugs
  - `/chore adw_sdlc_ZTE_iso` — zero-touch with auto-merge
  - `model_set heavy` — appended to use opus for key phases
- **`adw_sdlc_iso.py`:** The complete SDLC pipeline (Plan → Build → Test → Review → Document) running in isolation. Used for features and bugs where you still review the PR.
- **`adw_sdlc_zte_iso.py`:** ZTE variant that adds a Ship phase (approve + merge to main) — the agent proves the work is done (e.g., screenshots), and the code merges automatically. ZTE must be EXPLICITLY uppercased to run.
- **`adw_ship_iso.py`:** The Ship phase — validates ALL state fields are populated, performs git merge to main, auto-approves. This is the "zero-touch" gate.
- **In-Loop Review (`/in_loop_review <branch>`):** When you want to manually verify agent work — fetches the branch, prepares the app, starts it for you to inspect.
- **Worktree Cleanup:** `cleanup_worktrees.md` manages lifecycle of isolated environments.
- **Agentic KPIs:** `track_agentic_kpis.md` maintains performance metrics (streak, plan size, diff size, presence) in `app_docs/agentic_kpis.md`.

### Going from PITER to PITE

The progression is:
1. **PITER** (Out-Loop): Prompt → Implement → Test → Execute → **Review** — two touchpoints (prompt + review)
2. **PITE** (Zero-Touch): Prompt → Implement → Test → Execute — one touchpoint (prompt only), review is automated

The key enabler: making your ADWs so reliable that the review step becomes irrelevant. The agent proves correctness through tests, screenshots, and structured validation.

## Key Takeaways

1. **Parallel pipelines via isolation** — Worktrees + port allocation = multiple agents working simultaneously without conflicts
2. **One-prompt workflows** — `/chore adw_sdlc_ZTE_iso update the background color` creates an issue, runs the full SDLC, and auto-merges
3. **Model flexibility** — `model_set heavy` switches key phases to opus for harder tasks
4. **Proof of completion** — Agents take screenshots, run tests, and post results to issues — the review is automated, not skipped
5. **When things go wrong, fix the ADW** — Don't fix the code manually; update the ADW scripts or commands so the system improves permanently
6. **Trees folder** — Separated worktrees for each agent instance, cleaned up after merge

## Applied Changes

### New ADW Scripts (Isolated)
- `adws/adw_sdlc_iso.py` — Complete isolated SDLC pipeline (Plan → Build → Test → Review → Document)
- `adws/adw_sdlc_zte_iso.py` — Zero-Touch Execution: full SDLC + auto-ship (approve & merge)
- `adws/adw_ship_iso.py` — Ship phase: validates state completeness, merges to main

### New ADW Modules
- `adws/adw_modules/worktree_ops.py` — Worktree creation, validation, port allocation, cleanup
- `adws/adw_modules/data_types.py` updates — `ModelSet`, `ADWWorkflow`, `SlashCommand` types for ZTE
- `adws/adw_modules/agent.py` updates — `SLASH_COMMAND_MODEL_MAP` with base/heavy model selection

### New Commands (Claude Code / Copilot prompts)
- `classify_adw.prompt.md` — Extract ADW workflow, ID, and model_set from issue text
- `in-loop-review.prompt.md` — Quick checkout + review for validating agent work
- `install-worktree.prompt.md` — Set up isolated worktree with custom ports
- `cleanup-worktrees.prompt.md` — Manage worktree lifecycle
- `ship.prompt.md` — Approve and merge PR (ZTE gate)

### Updated Files
- `CLAUDE.md` — Added ZTE pipelines, isolated workflow commands, model selection docs
- `flow.prompt.md` — Added ZTE-specific Phase 6c (ship) and worktree isolation support
- `copilot-workflow.md` — Added ZTE prompts, updated pipeline table, ADW coverage

## Relation to TAC Goal

Lesson 7 is the culmination of the "build a system which builds a system" goal. By combining:
- **Isolation** (worktrees) — agents don't interfere with each other
- **State** (adw_state.json) — phases chain reliably
- **Validation** (tests + screenshots + reviews) — agents prove their work
- **Shipping** (adw_ship_iso) — agents merge their own code

...you achieve a codebase that nearly runs itself. The human's role shifts from coding + reviewing to just prompting. The system builds the system.
