# Full Development Flow

Run the complete development pipeline for a task in one shot — equivalent to the full ADW SDLC pipeline.

Pipeline: Classify → Branch → Plan → Build → Test (loop) → Review (with screenshots) → Document → Commit → Report.

## Instructions

You are executing a sequential multi-phase development pipeline.

CRITICAL: Follow these steps exactly. Do NOT skip phases. Do NOT combine phases. Do NOT take shortcuts.

Read `CLAUDE.md` first for project context.

CRITICAL: At the start of EVERY phase, print this marker before doing any work:
```
=== PHASE N: <Phase Name> ===
```
At the end of EVERY phase, print:
```
=== PHASE N COMPLETE ===
```
This is mandatory — it proves you executed every phase. Under no circumstances omit these markers.

### Phase 1 — Classify

Determine the task type from the description:
- **feature** — New functionality or enhancement
- **bug** — Something is broken or behaving incorrectly
- **chore** — Refactoring, cleanup, config, maintenance

### Phase 2 — Branch

CRITICAL: Do NOT skip branch creation. Every task gets its own branch.

Create a dedicated branch for this work:

```bash
git checkout main
git pull origin main
git checkout -b <type>/<short-slug>
```

Use the classification from Phase 1 as the branch prefix (e.g., `feature/dark-mode-toggle`, `bug/search-clear`, `chore/lint-config`).

Verify you are on the new branch before proceeding:
```bash
git branch --show-current
```

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

**6b. Visual Review:**
CRITICAL: If the task is a feature or bug with UI changes, you MUST take screenshots. Do NOT skip this step. Never assume "it probably looks fine" — verify visually.

- Ensure the dev server is running (`npm run dev`)
- Navigate to http://localhost:5173
- CRITICAL: Take screenshots of the critical functionality paths (aim for 1-5 screenshots)
  - Name them: `01_<descriptive-name>.png`, `02_<descriptive-name>.png`, etc.
  - Store in `agents/flow/review_img/` (create the directory if needed)
  - CRITICAL: Read back each screenshot to verify it matches the spec — do not assume it's correct. If a screenshot is blank or wrong, retake it.
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
- CRITICAL: Update `.github/prompts/conditional-docs.prompt.md` with an entry for the new doc file — this is how future agents discover relevant documentation. Do NOT skip this step.
- If the task introduced new conventions, patterns, or libraries, update the **Conventions** section in `CLAUDE.md` so all future agents inherit the knowledge.
- Commit:
  ```bash
  git add -A
  git commit -m "docs: add documentation for <task>"
  ```

### Phase 8 — Final Commit & Push

CRITICAL: Verify you are NOT on `main` before pushing. You should be on the branch created in Phase 2.

```bash
git branch --show-current
git push origin HEAD
```

If `git branch --show-current` returns `main`, STOP — you skipped Phase 2. Go back and create the branch.

After push, report the branch name so the user can create a PR.

### Phase 9 — Report

Before reporting, verify you completed every phase. Double-check:
- [ ] Phase 2: Are you on a feature/bug/chore branch (not main)?
- [ ] Phase 3: Was a spec file created in `specs/`?
- [ ] Phase 5: Did lint and build pass?
- [ ] Phase 6b: Were screenshots taken (for UI features)?
- [ ] Phase 7: Was documentation created in `app_docs/`?
- [ ] Phase 7: Was `conditional-docs.prompt.md` updated with a new entry?
- [ ] Phase 8: Was the branch pushed?

If any checkbox fails, go back and complete that phase before reporting.

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

### Agentic Layer Check
- Was this task on the agentic layer or application layer?
- Suggested agentic improvement (if any): <one-liner or "none">
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
- `.github/prompts/ship.prompt.md` — Ship (merge to main) protocol for ZTE
