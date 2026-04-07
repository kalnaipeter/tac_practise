# Copilot-Only Workflow Guide

> Version: 1.1  
> Last updated: 2026-04-07  
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
| **test** | `/test` | Run lint + build validation checks |
| **resolve-failed-test** | `/resolve-failed-test` | Fix failing lint/build errors |
| **review** | `/review` | Review current changes for quality |

### Documentation & Context

| Prompt | Command | Purpose |
|---|---|---|
| **document** | `/document` | Generate/update feature docs |
| **conditional-docs** | `/conditional-docs` | Update docs only if code changed |
| **prime** | `/prime` | Load full project context into Copilot |

### Maintenance

| Prompt | Command | Purpose |
|---|---|---|
| **chore** | `/chore <description>` | Refactoring, cleanup, config changes |

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

## Sequential Flow Prompt

For running a complete pipeline in one go, use the **flow prompt**:

```
/flow feature Add dark mode toggle
/flow bug The table doesn't sort correctly  
/flow chore Migrate to CSS modules
```

This runs the full sequence (plan → build → test → fix → review → document) automatically. See `.github/prompts/flow.prompt.md`.

The `/flow` prompt includes:
- **Spec verification** — compares implementation against every acceptance criterion
- **Visual review with screenshots** — takes 1-5 screenshots of critical UI paths, stores in `agents/flow/review_img/`
- **Issue severity classification** — blocker / tech_debt / skippable
- **Documentation generation** — creates feature docs in `app_docs/` with screenshots
- **Structured report** — files changed, validation results, review verdict, screenshots taken

## Comparison: ADW Automation vs Copilot Manual

| Aspect | ADW (automated) | Copilot (manual) |
|---|---|---|
| **Trigger** | GitHub webhook / cron | You type the prompt |
| **LLM backend** | Claude CLI / Gemini API | VS Code Copilot (included) |
| **Cost** | API credits needed | Free with Copilot subscription |
| **Speed** | Hands-free, ~5 min | Interactive, ~10-15 min |
| **Control** | Review PR after | Review each step |
| **Quality** | Same prompts | Same prompts |
| **Spec review** | Auto-generated, reviewed post | You review the spec before building |

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

IMPORTANT: When adding new prompts, changing workflows, or applying new TAC lessons, update this guide to reflect the current state. The version number and date at the top should be incremented.
