# Feature: Table Paginator

## Feature Description
Add a paginator bar below the country table that lets users control how many rows are shown per page and navigate between pages. The paginator displays a "rows per page" selector (e.g. 5 / 10 / 25) and prev/next page buttons alongside a page indicator (e.g. "Page 2 of 3"). When the total number of countries fits on one page the paginator still renders but disables irrelevant controls.

## User Story
As a table viewer
I want to control how many countries are shown at once and switch between pages
So that I can browse large datasets without scrolling through every row at once

## Problem Statement
The table currently renders all countries in a single, unbounded list. As the dataset grows this becomes unwieldy — users must scroll to find entries and there is no way to limit the visible set. Pagination is the standard solution for tabular data of variable length.

## Solution Statement
Introduce a standalone `Paginator` component rendered below the `<table>` inside `CountryTable`. Pagination state (`currentPage`, `rowsPerPage`) lives in `CountryTable` so the slice of the `countries` array passed to the table body always matches the current page. The `Paginator` component receives the state and callbacks as props, keeping it fully controlled and easy to test.

## Relevant Files
- **`src/components/CountryTable.tsx`** — owns the `countries` array and renders the table; will gain `currentPage` / `rowsPerPage` state and the slicing logic, and will render `<Paginator />`.
- **`src/components/CountryTable.css`** — existing table styles; paginator sits below the table so no existing rules need changing, but the wrapper may need a small bottom-padding tweak.
- **`src/services/countryService.ts`** — read-only; the total country count drives total page calculation.
- **`src/types/Country.ts`** — read-only; `Country[]` is what gets sliced.

### New Files
- **`src/components/Paginator.tsx`** — new controlled component; renders rows-per-page `<select>` and page navigation controls.
- **`src/components/Paginator.css`** — styles co-located with the component, following project conventions.

## Implementation Plan
### Phase 1: Foundation
Define the `Paginator` component interface and create the component + CSS skeleton so it can be imported without errors. No logic yet — just the props contract and empty render.

### Phase 2: Core Implementation
Implement the full `Paginator` UI: rows-per-page selector with options [5, 10, 25], a page info label ("Page X of Y"), and Prev / Next buttons that disable at the boundaries. Wire up all callbacks.

### Phase 3: Integration
Add `currentPage` and `rowsPerPage` state to `CountryTable`. Compute the visible slice before mapping rows. Render `<Paginator />` after `</table>`. Reset `currentPage` to 1 whenever `rowsPerPage` changes. Verify the full flow works end-to-end.

## Step by Step Tasks

### Step 1: Create Paginator.tsx with props interface
- Create `src/components/Paginator.tsx`
- Define `PaginatorProps` interface:
  - `currentPage: number`
  - `totalPages: number`
  - `rowsPerPage: number`
  - `rowsPerPageOptions: number[]`
  - `onPageChange: (page: number) => void`
  - `onRowsPerPageChange: (rows: number) => void`
- Export a functional `Paginator` component that consumes these props

### Step 2: Implement Paginator UI
- Render a `<div className="paginator">` containing:
  - A label + `<select>` for rows-per-page bound to `rowsPerPage` / `onRowsPerPageChange`; options come from `rowsPerPageOptions`
  - A `<span>` showing `Page {currentPage} of {totalPages}`
  - A "Prev" `<button>` — disabled when `currentPage === 1`
  - A "Next" `<button>` — disabled when `currentPage === totalPages`
- Call `onPageChange(currentPage - 1)` / `onPageChange(currentPage + 1)` on button click

### Step 3: Create Paginator.css
- Create `src/components/Paginator.css`
- Style `.paginator` as a flex row, space-between, centered vertically, with top margin to separate it from the table
- Style the select and buttons to match the existing app look (use CSS variables `--border`, `--text-h`, `--accent-bg` already used in `CountryTable.css`)
- Disabled buttons should have reduced opacity and `cursor: not-allowed`

### Step 4: Add pagination state to CountryTable
- Import `Paginator` and `./Paginator.css` (Paginator.tsx already imports its own CSS, no separate import needed in CountryTable)
- Add state:
  ```ts
  const ROWS_OPTIONS = [5, 10, 25];
  const [rowsPerPage, setRowsPerPage] = useState<number>(5);
  const [currentPage, setCurrentPage] = useState<number>(1);
  ```
- Derive computed values:
  ```ts
  const totalPages = Math.max(1, Math.ceil(countries.length / rowsPerPage));
  const paginatedCountries = countries.slice(
    (currentPage - 1) * rowsPerPage,
    currentPage * rowsPerPage
  );
  ```
- Replace `countries.map(...)` in the table body with `paginatedCountries.map(...)`

### Step 5: Render Paginator in CountryTable
- After the closing `</table>` tag, render:
  ```tsx
  <Paginator
    currentPage={currentPage}
    totalPages={totalPages}
    rowsPerPage={rowsPerPage}
    rowsPerPageOptions={ROWS_OPTIONS}
    onPageChange={setCurrentPage}
    onRowsPerPageChange={(rows) => {
      setRowsPerPage(rows);
      setCurrentPage(1);
    }}
  />
  ```

### Step 6: Run validation commands
- Run `npm run build` — must exit with zero errors
- Run `npm run lint` — must exit with zero errors

## Testing Strategy
### Unit Tests
- `Paginator` renders the correct page label for given `currentPage` / `totalPages`
- "Prev" button is disabled on page 1; "Next" button is disabled on the last page
- Clicking "Prev" calls `onPageChange` with `currentPage - 1`
- Clicking "Next" calls `onPageChange` with `currentPage + 1`
- Changing the select calls `onRowsPerPageChange` with the numeric value

### Integration Tests
- Changing rows-per-page resets to page 1 and shows the correct slice of countries
- Navigating pages shows the correct subset of rows

### Edge Cases
- Total countries not evenly divisible by `rowsPerPage` — last page shows the remainder
- `rowsPerPage` larger than total countries — `totalPages` is 1, both Prev and Next disabled
- Changing `rowsPerPage` while on page 3 resets to page 1 (no stale page)

## Acceptance Criteria
- [ ] A paginator bar is rendered below the country table
- [ ] The rows-per-page selector offers options 5, 10, and 25; default is 5
- [ ] The table body shows only the rows for the current page
- [ ] "Prev" is disabled on page 1; "Next" is disabled on the last page
- [ ] Clicking "Prev" / "Next" navigates to the correct page
- [ ] Changing rows-per-page resets to page 1
- [ ] The page indicator displays "Page X of Y" accurately
- [ ] `npm run build` exits with zero TypeScript errors
- [ ] `npm run lint` exits with zero lint errors

## Validation Commands
Execute every command to validate the feature works correctly with zero regressions.

- `npm run build` - Type-check and build to validate zero TypeScript errors
- `npm run lint` - Run ESLint to validate zero lint errors

## Notes
- No new npm packages are required — pagination is pure React state + array slicing.
- `ROWS_OPTIONS` is defined as a `const` inside `CountryTable.tsx` (not exported) since it is only used there and passed down as a prop; this keeps the component self-contained.
- If a search/filter feature is added later, the `currentPage` reset on filter change should follow the same pattern used here for `rowsPerPage` change.
- The paginator intentionally does not show individual page number buttons (1, 2, 3…) to keep the implementation minimal; this can be added as a follow-up enhancement.
