# Bug: Problem with Opening Application

## Bug Description
When opening the application, the UI fails to load and the browser console shows:
`Uncaught TypeError: Cannot read properties of undefined (reading 'toLocaleString')`
at `formatNumber` in `CountryTable.tsx:21`. The error occurs because `formatNumber` receives `undefined` instead of a number.

## Problem Statement
`CountryTable.tsx` references four property names on the `Country` object that do not exist on the `Country` interface due to typos. Accessing a non-existent property returns `undefined`, and calling `.toLocaleString()` on `undefined` throws a `TypeError` at runtime, crashing the component.

## Solution Statement
Correct the four typo'd property names in `CountryTable.tsx` so they match the `Country` interface exactly.

## Steps to Reproduce
1. Run `npm run dev`
2. Open `http://localhost:5173` in a browser
3. Observe the blank UI and the TypeError in the browser console

## Root Cause Analysis
`CountryTable.tsx` contains the following typos when mapping over country data:
- `country.popuaalation` → should be `country.population`
- `country.areaa` → should be `country.area`
- `country.continenqwet` → should be `country.continent`
- `country.langeawuage` → should be `country.language`

Because these properties don't exist on the `Country` interface, TypeScript would flag them at build time, but in Vite dev mode the code is served without a type-check pass, so the typos reach the browser as-is. At runtime, `country.popuaalation` evaluates to `undefined`, and `formatNumber(undefined)` calls `undefined.toLocaleString()`, throwing the TypeError and crashing the render.

## Relevant Files
- **`src/components/CountryTable.tsx`** — contains the typo'd property accesses; this is the only file that needs to change
- **`src/types/Country.ts`** — defines the correct `Country` interface; used as reference to confirm correct property names

## Step by Step Tasks

### Fix typos in CountryTable.tsx
- Change `country.popuaalation` → `country.population` (line 48)
- Change `country.areaa` → `country.area` (line 49)
- Change `country.continenqwet` → `country.continent` (line 50)
- Change `country.langeawuage` → `country.language` (line 51)

### Validate the fix
- Run validation commands below to confirm zero errors

## Validation Commands
Execute every command to validate the bug is fixed with zero regressions.

- `npm run lint` - Run ESLint to validate zero lint errors
- `npm run build` - Type-check and build to validate zero TypeScript errors

## Notes
- The fix is purely cosmetic (typo correction) — no logic changes, no new dependencies, no new files.
- TypeScript strict mode would have caught these at build time; running `npm run build` before serving would have surfaced these errors before they reached the browser.
