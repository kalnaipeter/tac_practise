---
description: "Prime for testing and validation. Loads test-specific context: test execution, failure resolution, validation protocols."
---

# Prime for Testing

Load focused context for running tests and resolving failures. This primes you for the validate → resolve → revalidate loop.

## Steps

1. READ `tac_practise/CLAUDE.md` — project context (stack, commands, validation protocol)
2. LIST all files in `tac_practise/src/` recursively — understand what's testable
3. READ `tac_practise/.github/prompts/test.prompt.md` — test execution sequence
4. READ `tac_practise/.github/prompts/resolve-failed-test.prompt.md` — resolution protocol for failures
5. READ `tac_practise/.github/prompts/bug-validation.prompt.md` — how to validate fixes
6. SCAN `tac_practise/specs/` — check for specs with validation commands
7. SUMMARIZE: tech stack, available test commands, validation loop (run → diagnose → fix → rerun), and any pending specs with validation criteria
