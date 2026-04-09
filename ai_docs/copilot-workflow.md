# Copilot-Only Workflow Guide

> Version: 4.0  
> Last updated: 2026-04-09  
> How to use all TAC lesson infrastructure with only VS Code Copilot — no external LLM backends needed.

## Overview

The TAC practice app has a full suite of prompt files, specs, and context engineering that works directly inside VS Code Copilot Chat. You do NOT need Claude CLI, Gemini CLI, or any paid API to use them.

The ADW (Automated Dev Workflow) scripts in `adws/` require an external LLM backend. This guide covers the **Copilot-only** alternative that achieves the same results manually.

## Quick Start

1. Open VS Code with Copilot active
2. Open Copilot Chat (Ctrl+Shift+I or the sidebar)
3. Type `/` to see available prompts, or click 📎 → **Prompt...** to browse them
4. Pick a prompt and provide your task description as the argument

## Available Prompts

All prompts live in `.github/prompts/`. Each has a single purpose.

### Planning & Building

| Prompt | Command | Purpose |
|---|---|---|
| **feature** | `/feature <description>` | Plan a new feature → creates a spec in `specs/` |
| **implement** | `/implement <spec-file>` | Build from an existing spec file |
| **create-component** | `/create-component <Name>` | Scaffold a new React component with CSS |
| **install** | `/install <package>` | Add a dependency properly |

### Bug Fixing

| Prompt | Command | Purpose |
|---|---|---|
| **bug** | `/bug <description>` | Diagnose and fix a bug (root cause analysis) |
| **bug-validation** | `/bug-validation` | Validate that a bug fix actually works |
| **patch** | `/patch <description>` | Quick targeted fix for a specific issue |

### Quality & Validation

| Prompt | Command | Purpose |
|---|---|---|
| **test** | `/test` | Full validation: lint + build + unit tests + E2E |
| **resolve-failed-test** | `/resolve-failed-test` | Fix failing validation errors (structured protocol) |
| **review** | `/review` | Review against spec with screenshots + JSON report |

### Documentation & Context

| Prompt | Command | Purpose |
|---|---|---|
| **document** | `/document` | Generate feature docs in `app_docs/` with screenshots |
| **conditional-docs** | `/conditional-docs` | Update docs only if code changed |
| **prime** | `/prime` | Load full project context into Copilot |

### Maintenance

| Prompt | Command | Purpose |
|---|---|---|
| **chore** | `/chore <description>` | Refactoring, cleanup, config changes |

### Agentic Layer (Lesson 8)

| Prompt | Command | Purpose |
|---|---|---|
| **agentic-audit** | `/agentic-audit` | Audit agentic vs application layer work ratio + recommend improvements |
| **plan-agentic** | `/plan-agentic <description>` | Plan an agentic layer improvement (prompts, ADWs, specs, context) |

### Zero-Touch Engineering (Lesson 7)

| Prompt | Command | Purpose |
|---|---|---|
| **classify-adw** | `/classify-adw <text>` | Extract ADW workflow + model_set from issue text |
| **in-loop-review** | `/in-loop-review <branch>` | Checkout agent's branch, start app for manual review |
| **install-worktree** | `/install-worktree <path> <be-port> <fe-port>` | Set up isolated worktree with custom ports |
| **cleanup-worktrees** | `/cleanup-worktrees [list\|all\|<id>]` | Manage/remove isolated worktrees |
| **ship** | `/ship` | Merge current branch to main (ZTE final gate) |

### Full Pipeline

| Prompt | Command | Purpose |
|---|---|---|
| **flow** | `/flow <description>` | Complete SDLC: classify → branch → plan → build → test → review → document → push |

## Standard Workflows

### Feature Development (mirrors `adw_plan_build_test.py`)

This is the equivalent of the automated Plan → Build → Test pipeline:

```
Step 1:  /feature Add sorting to the country table
         → Creates a spec in specs/sorting.md

Step 2:  Review the generated spec, edit if needed

Step 3:  /implement specs/sorting.md
         → Copilot builds the feature from the spec

Step 4:  /test
         → Runs lint + build validation

Step 5:  (if tests fail) /resolve-failed-test
         → Fixes errors, then go back to Step 4

Step 6:  /review
         → Quality review of the implementation

Step 7:  git add, commit, push, open PR
```

### Bug Fix (mirrors `adw_plan_build.py` with /bug classification)

```
Step 1:  /bug The search filter doesn't clear when switching pages

Step 2:  /bug-validation
         → Confirms the fix works

Step 3:  /test
         → Validates no regressions

Step 4:  git commit + PR
```

### Quick Fix (mirrors `adw_patch.py`)

```
Step 1:  /patch Fix the TypeScript error in CountryTable.tsx line 45

Step 2:  /test

Step 3:  git commit
```

### Full SDLC (mirrors `adw_sdlc.py`)

```
Step 1:  /feature <description>     → Plan
Step 2:  /implement specs/<name>.md → Build
Step 3:  /test                      → Validate
Step 4:  /resolve-failed-test       → Fix (if needed, repeat Step 3)
Step 5:  /review                    → Review
Step 6:  /document                  → Document
Step 7:  git commit + PR            → Ship
```

### Zero-Touch Execution (mirrors `adw_sdlc_zte_iso.py`)

Same as Full SDLC but auto-merges to main after all phases pass:

```
Step 1:  /flow <description>        → Runs phases 1-7 automatically
Step 2:  /ship                      → Merge to main (ZTE gate)
```

Or for parallel work with isolation:

```
Step 1:  /install-worktree trees/abc12345 9101 9201  → Set up isolated env
Step 2:  (work in worktree)
Step 3:  /ship                                        → Merge when done
Step 4:  /cleanup-worktrees abc12345                  → Clean up
```

### Reviewing Agent Work

When an agent has completed work on a branch and you want to inspect it:

```
Step 1:  /in-loop-review feature/my-branch  → Checkout + start app
Step 2:  (manually inspect in browser)
Step 3:  git checkout main                  → Return to main
```

## Sequential Flow Prompt — `/flow`

For running a complete pipeline in one go, use the **flow prompt**:

```
/flow Add dark mode toggle
/flow The table doesn't sort correctly  
/flow Migrate to CSS modules
```

This runs the **full SDLC sequence** in a single Copilot session — equivalent to running all ADW scripts combined.

### What `/flow` Does (9 phases)

| Phase | ADW Equivalent | What Happens |
|---|---|---|
| 1. Classify | `classify_issue()` | Determines feature / bug / chore |
| 2. Branch | `generate_branch_name()` | `git checkout -b <type>/<slug>` from main |
| 3. Plan | Plan Agent + `feature.prompt.md` | Creates spec in `specs/` with acceptance criteria + validation commands, commits |
| 4. Build | Build Agent + `implement.prompt.md` | Implements the spec, commits |
| 5. Validate | `adw_test.py` test-fix loop | Runs lint → build → unit tests → E2E. Max 4 attempts, commits each fix |
| 6. Review | `adw_review.py` + `review.prompt.md` | Spec verification, screenshots (1-5), severity classification, patch specs for blockers |
| 7. Document | `adw_document.py` + `document.prompt.md` | Creates docs in `app_docs/`, copies screenshots, updates conditional-docs |
| 8. Push | `create_pull_request()` | `git push origin HEAD` |
| 9. Report | Status comment | Structured summary: files, validation, review, screenshots, docs |

### ADW Coverage Comparison

| ADW Capability | Covered by `/flow`? |
|---|---|
| Issue classification | Yes — Phase 1 |
| Git branch creation | Yes — Phase 2 |
| Spec creation from template | Yes — Phase 3, with validation commands section |
| Implementation from spec | Yes — Phase 4 |
| Lint + build validation | Yes — Phase 5 |
| Unit tests + E2E tests | Yes — Phase 5 (skip if not configured) |
| Test-fix-retest loop (max 4) | Yes — Phase 5, commits each fix attempt |
| Resolve-failed-test protocol | Yes — Phase 5 references the prompt |
| Review against spec | Yes — Phase 6a, every acceptance criterion |
| Screenshots with read-back | Yes — Phase 6b, 1-5 screenshots in `agents/flow/review_img/` |
| Issue severity (blocker/tech_debt/skip) | Yes — Phase 6b |
| Patch specs for blockers | Yes — Phase 6b, creates `specs/patch/` |
| Documentation generation | Yes — Phase 7 |
| Screenshots in docs | Yes — Phase 7 copies to `app_docs/assets/` |
| Conditional-docs update | Yes — Phase 7 |
| Git commits per phase | Yes — plan, build, fixes, docs each committed |
| Git push | Yes — Phase 8 |
| Structured report | Yes — Phase 9 |
| Worktree isolation (`adw_sdlc_iso`) | Via `/install-worktree` — manual setup for parallel work |
| ADW classification (`classify_adw`) | Via `/classify-adw` — extract workflow + model_set from text |
| In-loop review | Via `/in-loop-review <branch>` — checkout + start app for manual inspection |
| Worktree cleanup | Via `/cleanup-worktrees` — manage isolated environments |
| Ship / auto-merge (ZTE) | Via `/ship` — merge to main after all phases pass |
| Agentic layer audit | Via `/agentic-audit` — check 50/50 ratio, recommend improvements |
| Agentic improvement planning | Via `/plan-agentic` — plan prompt/ADW/spec improvements |

### What `/flow` Does NOT Cover (by design)

These are ADW-only capabilities that require external infrastructure:

| ADW Capability | Why Not in `/flow` |
|---|---|
| GitHub issue fetching (`gh issue view`) | You describe the task directly — no issue needed |
| GitHub issue comments (status updates) | No issue to comment on — progress is visible in chat |
| ADW ID tracking | Copilot session is the tracking unit |
| State persistence (`adw_state.json`) | Single session — no need to save/resume |
| Execution logging to file | Chat transcript serves as the log |
| Webhook / cron triggers | You trigger manually with `/flow` |
| Multi-agent subprocess isolation | Single agent — shared context (usually better for coherence) |
| Model selection per phase (opus for review) | Copilot chooses the model |
| Rate limit retry logic | Handled by Copilot runtime |
| Automatic worktree creation + port allocation | ADW scripts handle this; Copilot uses `/install-worktree` manually |
| Zero-Touch auto-merge (`adw_sdlc_zte_iso`) | Use `/ship` manually after `/flow`; ZTE auto-merge is ADW-only |

## Comparison: ADW Automation vs `/flow` (Copilot)

| Aspect | ADW (automated) | `/flow` (Copilot) |
|---|---|---|
| **Trigger** | GitHub webhook / cron | You type `/flow <task>` |
| **LLM backend** | Claude CLI / Gemini API | VS Code Copilot (included) |
| **Cost** | API credits needed | Free with Copilot subscription |
| **Speed** | Hands-free, ~5 min | Interactive, ~10-15 min |
| **Control** | Review PR after | Watch each phase, intervene anytime |
| **Prompts used** | Same `.github/prompts/` | Same `.github/prompts/` |
| **Git automation** | Full (branch, commit, push, PR) | Full (branch, commit, push — you create PR) |
| **Test loop** | Max 4 retries, commit per fix | Max 4 retries, commit per fix |
| **Review** | Screenshots + JSON report | Screenshots + markdown report |
| **Documentation** | Auto-generated with screenshots | Auto-generated with screenshots |
| **Context isolation** | Fresh per phase (focused) | Shared session (more coherent) |
| **Resumable** | Yes (state file) | No (single session) |
| **GitHub integration** | Issue fetch + status comments | None (manual task description) |

## Context Files

These files help Copilot understand the project:

- **`CLAUDE.md`** — Full project context (stack, architecture, commands, conventions)
- **`.github/instructions/codebase.instructions.md`** — Auto-loaded by Copilot for all files
- **`ai_docs/`** — 3rd party reference docs
- **`specs/`** — Feature specifications
- **`descriptions/`** — Lesson notes and applied changes

## Tips

1. **Always `/prime` first** in a new chat session to load project context
2. **Review specs before implementing** — the plan is your checkpoint
3. **Run `/test` after every change** — catch errors early
4. **Use `/conditional-docs`** to keep docs in sync with code changes
5. **Specs are reusable** — if a build goes wrong, delete the code and `/implement` the spec again

## Maintaining This Document

CRITICAL: When adding new prompts, changing workflows, or applying new TAC lessons, update this guide to reflect the current state. The version number and date at the top should be incremented.
