---
description: "Prime for bug fixing. Loads bug-specific context: root cause analysis, validation protocol, test resolution."
---

# Prime for Bug Fixing

Load focused context for diagnosing and fixing bugs. This primes you with exactly the right tools — no excess context.

## Steps

1. READ `tac_practise/CLAUDE.md` — project context (stack, architecture, commands)
2. LIST all files in `tac_practise/src/` recursively — understand the codebase structure
3. READ `tac_practise/src/types/Country.ts` — core data type
4. READ `tac_practise/.github/prompts/bug.prompt.md` — bug diagnosis protocol
5. READ `tac_practise/.github/prompts/bug-validation.prompt.md` — validation after fix
6. READ `tac_practise/.github/prompts/resolve-failed-test.prompt.md` — resolution protocol for test failures
7. READ `tac_practise/.github/prompts/test.prompt.md` — test execution sequence
8. SCAN `tac_practise/specs/` — check for any related specs or patch specs
9. SUMMARIZE: tech stack, architecture, bug-fixing workflow (diagnose → fix → validate → test → verify)
