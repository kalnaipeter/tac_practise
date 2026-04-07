# Full Development Flow

Run the complete development pipeline for a task in one shot — equivalent to the full ADW SDLC pipeline.

Pipeline: Classify → Branch → Plan → Build → Test (loop) → Review (with screenshots) → Document → Commit → Report.

## Instructions

You are executing a sequential multi-phase development pipeline. Complete ALL phases below in order. Do NOT skip phases. If a phase fails, fix the issue and restart from that phase.

Read `CLAUDE.md` first for project context.

IMPORTANT: Track your progress. At the start of each phase, state which phase you are entering.

### Phase 1 — Classify

Determine the task type from the description:
- **feature** — New functionality or enhancement
- **bug** — Something is broken or behaving incorrectly
- **chore** — Refactoring, cleanup, config, maintenance

### Phase 2 — Branch

Create a dedicated branch for this work:

```bash
git checkout main
git pull origin main
git checkout -b <type>/<short-slug>
```

Use the classification from Phase 1 as the branch prefix (e.g., `feature/dark-mode-toggle`, `bug/search-clear`, `chore/lint-config`).

### Phase 3 — Plan

**If feature or chore:**
- Research the codebase to understand existing patterns
- Create a detailed spec in `specs/<task-name>.md` following the format in `.github/prompts/feature.prompt.md`
- IMPORTANT: The spec must have concrete implementation steps, acceptance criteria, AND a Validation Commands section
- IMPORTANT: Replace every `<placeholder>` in the plan format with real values

**If bug:**
- Reproduce the bug by reading relevant code
- Identify the root cause
- Document the fix approach (no spec file needed for bugs)

Commit the plan:
```bash
git add specs/
git commit -m "plan: <type>: add implementation plan for <task>"
```

### Phase 4 — Build

**If feature or chore:**
- Implement the spec you created in Phase 3
- Follow existing patterns and conventions from `CLAUDE.md`
- Read `.github/prompts/implement.prompt.md` for the implementation protocol

**If bug:**
- Apply the fix identified in Phase 3
- Follow the root cause analysis format from `.github/prompts/bug.prompt.md`

Commit the implementation:
```bash
git add -A
git commit -m "build: <type>: implement <short-description>"
```

### Phase 5 — Validate (Test-Fix Loop)

Run the full validation sequence from `.github/prompts/test.prompt.md`. Be rigorous. Follow these steps exactly. Maximum **4 attempts** — if still failing after 4, stop and report the failures.

**For each attempt:**

1. `npm run lint` — If errors, stop and fix
2. `npm run build` — If errors, stop and fix
3. `npm test` — Skip if no test runner is configured
4. `npx playwright test` — Skip if Playwright is not set up

**If any step fails:**
- Read the error output carefully
- THINK HARD about the root cause (follow `.github/prompts/resolve-failed-test.prompt.md` protocol)
- Make a minimal, surgical fix — do not refactor unrelated code
- Commit the fix:
  ```bash
  git add -A
  git commit -m "fix: resolve validation failures (attempt <N>)"
  ```
- IMPORTANT: Rerun ALL steps from step 1 (not just the one that failed)
- Track which attempt you are on (1/4, 2/4, etc.)

**If all steps pass:** proceed to Phase 6.

### Phase 6 — Review Against Spec

CRITICAL: This is a thorough structured review, not a quick glance. Be precise and avoid assumptions.

**6a. Code Review:**
- Run `git diff origin/main` to see all changes
- If a spec was created, read it and verify EVERY acceptance criterion is met
- Check: TypeScript `any` types? Unused imports/variables? Pattern violations? Missing error handling?
- If code issues found → fix, commit with `git commit -m "fix: resolve review issue"`, return to Phase 5

**6b. Visual Review (if the feature has UI changes):**
- Ensure the dev server is running (`npm run dev`)
- Navigate to http://localhost:5173
- IMPORTANT: Take screenshots of the critical functionality paths (aim for 1-5 screenshots)
  - Name them: `01_<descriptive-name>.png`, `02_<descriptive-name>.png`, etc.
  - Store in `agents/flow/review_img/` (create the directory if needed)
  - IMPORTANT: Read back each screenshot to verify it matches the spec — do not assume it's correct
- Focus only on critical paths that prove the feature works as specified
- If a visual issue is found, classify its severity:
  - `blocker` — prevents release, harms user experience → create a patch spec in `specs/patch/patch-flow-<name>.md` following `.github/prompts/patch.prompt.md`, fix it, return to Phase 5
  - `tech_debt` — works but creates future problems → note it in the report
  - `skippable` — cosmetic, non-blocking → note it in the report

**6c. Spec Verdict:**
- Critically evaluate: does the implementation satisfy ALL acceptance criteria?
- If NO and blocker → fix and return to Phase 5
- If YES → proceed

### Phase 7 — Document

Follow the documentation process from `.github/prompts/document.prompt.md`:
- Run `git diff origin/main --stat` to analyze what changed
- If no meaningful changes exist, skip this phase
- Create documentation in `app_docs/` directory (filename: `feature-flow-<descriptive-name>.md`)
- If screenshots were taken in Phase 6, copy them to `app_docs/assets/` and reference them in the doc
- Update `.github/prompts/conditional-docs.prompt.md` with an entry for the new doc file
- Commit:
  ```bash
  git add -A
  git commit -m "docs: add documentation for <task>"
  ```

### Phase 8 — Final Commit & Push

```bash
git push origin HEAD
```

After push, report the branch name so the user can create a PR.

### Phase 9 — Report

Provide a structured summary:

```
## Flow Report

**Task type:** feature | bug | chore
**Branch:** <branch-name>
**Spec:** specs/<name>.md (if created)

### Files Changed
- list of files created or modified

### Validation
- Lint: pass/fail
- Build: pass/fail
- Unit tests: pass/fail/skipped
- E2E tests: pass/fail/skipped
- Attempts needed: N/4

### Review
- Spec match: yes/no/N/A
- Screenshots: list paths to agents/flow/review_img/ (or "N/A — no UI changes")
- Blocker issues: list or "none"
- Tech debt noted: list or "none"

### Documentation
- Doc file: app_docs/<name>.md (or "skipped — no changes")

### Decisions & Trade-offs
- any notable choices made during implementation
```

## Relevant Files

- `CLAUDE.md` — Project context, architecture, conventions
- `specs/` — Where feature specs are created
- `specs/patch/` — Where patch specs go for blocker fixes
- `src/components/` — React components
- `src/services/` — Data layer
- `src/types/` — TypeScript interfaces
- `.github/prompts/feature.prompt.md` — Plan format for features
- `.github/prompts/bug.prompt.md` — Bug fix protocol
- `.github/prompts/implement.prompt.md` — Implementation protocol
- `.github/prompts/test.prompt.md` — Full validation sequence (4 steps)
- `.github/prompts/resolve-failed-test.prompt.md` — Failure resolution protocol
- `.github/prompts/review.prompt.md` — Full review protocol reference
- `.github/prompts/patch.prompt.md` — Patch plan format for blocker fixes
- `.github/prompts/document.prompt.md` — Documentation generation protocol
- `.github/prompts/conditional-docs.prompt.md` — Conditional doc routing
