# Full Development Flow

Run the complete development pipeline for a task in one shot: Plan → Build → Test → Fix → Review.

## Instructions

You are executing a sequential multi-phase development pipeline. Complete ALL phases below in order. Do NOT skip phases. If a phase fails, fix the issue and restart from that phase.

Read `CLAUDE.md` first for project context.

### Phase 1 — Classify

Determine the task type from the description:
- **feature** — New functionality or enhancement
- **bug** — Something is broken or behaving incorrectly  
- **chore** — Refactoring, cleanup, config, maintenance

### Phase 2 — Plan

**If feature or chore:**
- Research the codebase to understand existing patterns
- Create a detailed spec in `specs/<task-name>.md` following the format in `.github/prompts/feature.prompt.md`
- IMPORTANT: The spec must have concrete implementation steps and acceptance criteria

**If bug:**
- Reproduce the bug by reading relevant code
- Identify the root cause
- Document the fix approach (no spec file needed for bugs)

### Phase 3 — Build

**If feature or chore:**
- Implement the spec you created in Phase 2
- Follow existing patterns and conventions from `CLAUDE.md`

**If bug:**
- Apply the fix identified in Phase 2
- Follow the root cause analysis format from `.github/prompts/bug.prompt.md`

### Phase 4 — Validate

Run the validation sequence. IMPORTANT: Execute these commands and check their output:

1. `npm run lint` — Fix ALL errors before continuing
2. `npm run build` — Fix ALL errors before continuing

If either fails:
- Fix the issue
- IMPORTANT: Rerun BOTH checks from step 1 (not just the one that failed)
- Repeat until both pass

### Phase 5 — Review

Review your own implementation:
- Does the code match the spec (if one was created)?
- Are there any TypeScript `any` types? Remove them.
- Are there unused imports or variables? Remove them.
- Does the code follow existing patterns in the codebase?
- Are CSS files co-located with their components?

If issues found, fix them and go back to Phase 4.

### Phase 6 — Report

Summarize what was done:
1. Task type (feature/bug/chore)
2. Files created or modified
3. Spec file location (if created)
4. Validation results (lint + build)
5. Any decisions or trade-offs made

## Relevant Files

- `CLAUDE.md` — Project context, architecture, conventions
- `specs/` — Where feature specs are created
- `src/components/` — React components
- `src/services/` — Data layer
- `src/types/` — TypeScript interfaces
- `.github/prompts/` — Individual phase prompts for reference
