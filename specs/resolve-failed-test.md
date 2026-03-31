# Resolve Failed Test

> Fix a specific failing test using the provided failure details. This is the "Resolve" step of the Request → Validate → Resolve cycle.

## Instructions

### 1. Analyze the Failure

- Review the test name, purpose, and error message from the failure data
- Understand what the test is trying to validate
- Identify the root cause from the error details

### 2. Context Discovery

- Check recent changes: `git diff origin/main --stat --name-only`
- If a relevant spec exists in `specs/*.md`, read it to understand requirements
- Focus only on files that could impact this specific test

### 3. Reproduce the Failure

- IMPORTANT: Use the `execution_command` from the test data
- Run it to see the full error output and stack trace
- Confirm you can reproduce the exact failure

### 4. Fix the Issue

- THINK HARD about the root cause before jumping to a fix
- Make minimal, targeted changes to resolve only this test failure
- Do not modify unrelated code or tests
- Be surgical — fix the failure at hand, don't refactor

### 5. Validate the Fix

- Re-run the same `execution_command` to confirm the test now passes
- Then rerun ALL validation commands from `specs/test.md` to check for regressions
- IMPORTANT: If any validation step fails after your fix, resolve it immediately and rerun ALL steps

## Test Failure Input

The failing test data will be provided as a JSON object:

```json
{
  "test_name": "string",
  "passed": false,
  "execution_command": "string",
  "test_purpose": "string",
  "error": "string"
}
```

## Report

After resolution, provide:
- Root cause identified
- Specific fix applied (files changed and why)
- Confirmation that the test now passes
- Confirmation that all other validation steps still pass
