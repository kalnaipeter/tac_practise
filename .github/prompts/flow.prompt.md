# Full Development Flow

Run the complete development pipeline for a task in one shot: Plan → Build → Test → Fix → Review → Document.

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

### Phase 5 — Review Against Spec

IMPORTANT: This is not a quick glance. This is a structured review of the implementation against the spec.

**5a. Code Review:**
- Run `git diff origin/main` to see all changes
- Compare every acceptance criterion in the spec against the actual implementation
- Check: TypeScript `any` types? Unused imports/variables? Pattern violations?
- If code issues found, fix them and go back to Phase 4

**5b. Visual Review (if the feature has UI changes):**
- Ensure the dev server is running (`npm run dev`)
- Navigate to http://localhost:5173
- IMPORTANT: Take screenshots of the critical functionality paths (1-5 screenshots)
  - Name them: `01_<descriptive-name>.png`, `02_<descriptive-name>.png`, etc.
  - Store in `agents/flow/review_img/` (create if needed)
  - IMPORTANT: Read back each screenshot to verify it matches the spec — do not assume
- Focus only on critical paths that prove the feature works as specified
- If any visual issue is found, describe it with severity:
  - `blocker` — prevents release, harms user experience
  - `tech_debt` — works but creates future problems
  - `skippable` — cosmetic, non-blocking

**5c. Spec Verdict:**
- Does the implementation satisfy ALL acceptance criteria in the spec?
- If NO → fix the gap and return to Phase 3
- If YES → proceed

### Phase 6 — Document

Follow the documentation process from `.github/prompts/document.prompt.md`:
- Analyze git diff to understand what changed
- Create documentation in `app_docs/` directory
- If screenshots were taken in Phase 5, copy them to `app_docs/assets/` and reference them
- Update `conditional-docs` with an entry for the new doc

### Phase 7 — Report

Provide a structured summary:

```
## Flow Report

**Task type:** feature | bug | chore
**Spec:** specs/<name>.md (if created)

### Files Changed
- list of files created or modified

### Validation
- Lint: pass/fail
- Build: pass/fail

### Review
- Spec match: yes/no
- Screenshots: list paths (or "N/A — no UI changes")
- Issues found: list or "none"

### Documentation
- Doc file: app_docs/<name>.md (or "skipped")

### Decisions & Trade-offs
- any notable choices made during implementation
```

## Relevant Files

- `CLAUDE.md` — Project context, architecture, conventions
- `specs/` — Where feature specs are created
- `src/components/` — React components
- `src/services/` — Data layer
- `src/types/` — TypeScript interfaces
- `.github/prompts/review.prompt.md` — Full review protocol reference
- `.github/prompts/document.prompt.md` — Full documentation protocol reference
- `.github/prompts/conditional-docs.prompt.md` — Conditional doc routing
