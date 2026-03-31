# Bug Resolution — Closed-Loop Validation Spec

> This spec defines all validation steps required to close the feedback loop when solving a bug. Every bug fix MUST pass all validation before being considered complete.

## Instructions

- IMPORTANT: Follow the Request → Validate → Resolve cycle. Do the work, validate it, and if anything fails, resolve immediately then **rerun every validation step from the top**.
- IMPORTANT: If you run into any errors at all, stop and resolve them immediately then rerun every validation step.
- Use `THINK HARD` about the root cause before jumping to a fix.
- Be surgical — fix the bug at hand, don't refactor unrelated code.

## Validation Commands

Execute every command below in order. Every command must exit with code 0 (no errors). If any command fails, fix the issue and restart from step 1.

### 1. Lint Check

```bash
npm run lint
```

- Catches: unused imports, undeclared variables, style violations, import errors
- IMPORTANT: If there are errors at all, resolve them before continuing

### 2. TypeScript Type Check & Build

```bash
npm run build
```

- Catches: type errors, interface mismatches, missing props, incompatible types
- This runs `tsc` then `vite build` — both must succeed
- IMPORTANT: If there are errors at all, resolve them before continuing

### 3. Unit Tests (when configured)

```bash
npm test
```

- Catches: logic errors, regressions, broken contracts
- IMPORTANT: If there are errors at all, resolve them before continuing

### 4. E2E Validation (when configured)

```bash
npx playwright test
```

- Catches: UI regressions, broken user flows, integration failures
- IMPORTANT: If there are errors at all, resolve them before continuing

## Feedback Loop Protocol

```
1. Make the fix
2. Run ALL validation commands above (steps 1-4)
3. If ANY command fails:
   a. Read the error output carefully
   b. THINK HARD about what caused each failure
   c. Fix the issue
   d. Go back to step 2 (rerun ALL commands, not just the one that failed)
4. If ALL commands pass → bug is resolved ✅
```

## Bug Plan Format

When planning a bug fix, use this structure in `specs/`:

```md
# Bug: <bug name>

## Bug Description
<describe the bug — symptoms, expected vs actual behavior>

## Root Cause Analysis
THINK HARD about why this is happening.
<explain the root cause>

## Fix
<describe the minimal fix>

## Relevant Files
<list files to change and why>

## Steps
<ordered list of changes>

## Validation Commands
IMPORTANT: Execute every command. If you run into any errors at all, stop and resolve them immediately then rerun every validation step.

1. `npm run lint` — resolve all errors
2. `npm run build` — resolve all errors
3. `npm test` — resolve all errors
4. `npx playwright test` — resolve all errors (if UI-related)
```

## Usage

Reference this spec in any bug-fixing prompt:

```
Read specs/bug.md and follow its validation protocol.
Fix: <description of the bug>
```
