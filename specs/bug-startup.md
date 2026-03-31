# Bug: Startup bug — Paginator.tsx parse errors prevent app from running

## Bug Description
The application fails to start with a Vite/OXC transform error. Two typos in `src/components/Paginator.tsx` cause JSX parse failures and a TypeScript reference error:
1. Opening tag `<labell>` does not match closing tag `</label>` (extra `l`).
2. `{totalPagesasd}` references an undefined variable instead of `{totalPages}`.

Expected: App starts and renders normally.
Actual: Vite throws `[PARSE_ERROR] Expected corresponding JSX closing tag for 'labell'` and TypeScript cannot resolve `totalPagesasd`.

## Problem Statement
Two typos in `Paginator.tsx` make the file unparseable by the OXC compiler and type-invalid for TypeScript.

## Solution Statement
Fix both typos in `Paginator.tsx`: change `<labell>` → `<label>` and `totalPagesasd` → `totalPages`.

## Steps to Reproduce
1. Clone the repo on branch `bug-12-518ebf9c-startup-bug`.
2. Run `npm run dev`.
3. Observe Vite parse error in the terminal.

## Root Cause Analysis
Manual editing introduced two typos in `Paginator.tsx`:
- `<labell className="paginator__rows-label">` — the opening JSX tag has an extra `l`, making it a non-standard HTML element that does not match the closing `</label>` tag.
- `{totalPagesasd}` — extra characters appended to the prop name `totalPages`, making it an undeclared identifier.

## Relevant Files
Use these files to fix the bug:

- `src/components/Paginator.tsx` — contains both typos that cause the parse error and TypeScript error.

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### Fix opening label tag typo
- In `Paginator.tsx` line 22, change `<labell` to `<label`.

### Fix totalPages variable typo
- In `Paginator.tsx` line 36, change `{totalPagesasd}` to `{totalPages}`.

### Validate
- Run validation commands below.

## Validation Commands
Execute every command to validate the bug is fixed with zero regressions.

- `npm run lint` - Run ESLint to validate zero lint errors
- `npm run build` - Type-check and build to validate zero TypeScript errors

## Notes
Both issues are simple typos introduced during development. No logic changes are needed.
