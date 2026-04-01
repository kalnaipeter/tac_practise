# Application Validation Test Suite

> Defines the exact test execution sequence for the tac_practise app. Used by `adw_test.py` and `adw_plan_build_test.py` to validate agent work. Every test must pass before work is considered done.

## Purpose

Proactively identify and fix issues before they ship. Run this suite to:
- Detect syntax errors, type mismatches, and import failures
- Identify broken builds and lint violations
- Verify the application compiles and bundles correctly
- Ensure the codebase is healthy before committing

## Instructions

- Execute each test in the sequence below, top to bottom
- `cd` into the project root before each command
- If a test fails, **stop immediately** — do not run subsequent tests
- IMPORTANT: If any test fails, fix the issue and rerun ALL tests from step 1
- Capture the result (passed/failed) and any error output

## Test Execution Sequence

### 1. Lint Check

- **Command:** `npm run lint`
- **test_name:** `eslint_lint_check`
- **What it catches:** Unused imports, undeclared variables, style violations, import errors, TypeScript-specific lint rules
- **IMPORTANT:** If there are errors at all, resolve them before continuing

### 2. TypeScript Type Check & Build

- **Command:** `npm run build`
- **test_name:** `typescript_build`
- **What it catches:** Type errors, interface mismatches, missing props, incompatible types, bundling failures (runs `tsc` then `vite build`)
- **IMPORTANT:** If there are errors at all, resolve them before continuing

### 3. Unit Tests (when configured)

- **Command:** `npm test`
- **test_name:** `unit_tests`
- **What it catches:** Logic errors, regressions, broken contracts
- **Note:** Skip if no test runner is configured yet
- **IMPORTANT:** If there are errors at all, resolve them before continuing

### 4. E2E Validation (when configured)

- **Command:** `npx playwright test`
- **test_name:** `e2e_tests`
- **What it catches:** UI regressions, broken user flows, integration failures
- **Note:** Skip if Playwright is not set up yet
- **IMPORTANT:** If there are errors at all, resolve them before continuing

## Feedback Loop Protocol

```
1. Run ALL validation commands (steps 1-4)
2. If ANY command fails:
   a. Read the error output carefully
   b. THINK HARD about the root cause
   c. Fix the issue (be surgical — don't refactor unrelated code)
   d. Go back to step 1 (rerun ALL commands, not just the failed one)
3. If ALL commands pass → validation complete ✅
```

## Output Format

When reporting test results (e.g., to GitHub issue comments), use this JSON structure:

```json
[
  {
    "test_name": "string",
    "passed": true,
    "execution_command": "string",
    "test_purpose": "string",
    "error": "optional string — only if failed"
  }
]
```

### Example

```json
[
  {
    "test_name": "eslint_lint_check",
    "passed": true,
    "execution_command": "npm run lint",
    "test_purpose": "Validates code quality, unused imports, style violations"
  },
  {
    "test_name": "typescript_build",
    "passed": false,
    "execution_command": "npm run build",
    "test_purpose": "Validates TypeScript compilation and production build",
    "error": "TS2345: Argument of type 'string' is not assignable to parameter of type 'number'"
  }
]
```

## Usage

Reference this prompt in any prompt that needs validation:

```
Read .github/prompts/test.prompt.md and execute every validation step.
IMPORTANT: If you run into any errors at all, stop and resolve them immediately then rerun every validation step.
```
