# Feature: Show Country Dialog

## Feature Description
Add a "Show" dialog that opens when the user clicks the Show button in the country table's Actions column. The dialog displays all country details in a read-only format, and beneath the details renders the country's flag using the flagcdn.com service (which provides flag images by ISO 3166-1 alpha-2 country codes).

## User Story
As a user browsing the countries table
I want to click the Show button and see a dialog with full country details and a flag image
So that I can quickly view all information about a country in a clear, visual format

## Problem Statement
Currently clicking Show just triggers an alert with the country name. There is no detailed view of a country's data, and no visual representation (flag) is available.

## Solution Statement
Create a new `ShowCountryDialog` component (mirroring the existing `EditCountryDialog` pattern) that:
1. Opens as a `<dialog>` modal when `handleShow` is called.
2. Displays all Country fields (name, capital, population, area, continent, language, currency) in a read-only layout.
3. Renders the country's flag below the details using `https://flagcdn.com/w320/{code}.png` where `{code}` is a two-letter ISO country code.
4. Add a `countryCode` field to the Country type and data so flags can be resolved.
5. A Close button dismisses the dialog.

## Relevant Files
Use these files to implement the feature:

- `src/types/Country.ts` — Add `countryCode` field to the Country interface
- `src/services/countryService.ts` — Add ISO country codes to each country record
- `src/components/CountryTable.tsx` — Wire up `handleShow` to open the new dialog instead of alerting
- `src/components/Actions.tsx` — Already has Show button, no changes needed
- `src/components/EditCountryDialog.tsx` — Reference for dialog pattern (useRef, showModal, backdrop, cancel handling)
- `src/components/EditCountryDialog.css` — Reference for dialog styling

### New Files
- `src/components/ShowCountryDialog.tsx` — New read-only dialog component
- `src/components/ShowCountryDialog.css` — Styles for the show dialog

## Implementation Plan
### Phase 1: Foundation
- Extend the `Country` interface with `countryCode: string`
- Add ISO 3166-1 alpha-2 codes to every country entry in `countryService.ts`

### Phase 2: Core Implementation
- Create `ShowCountryDialog.tsx` using the same `<dialog>` pattern as `EditCountryDialog`
- Create `ShowCountryDialog.css` with read-only detail styling and flag image
- Display all fields as label-value pairs (not inputs)
- Render flag image from flagcdn.com using the country code

### Phase 3: Integration
- In `CountryTable.tsx`, add state for `showingCountry`
- Replace the alert in `handleShow` to set `showingCountry`
- Render `ShowCountryDialog` when `showingCountry` is set
- Pass `onClose` handler to clear state

## Step by Step Tasks

### Step 1: Extend Country type
- Add `countryCode: string` to the `Country` interface in `src/types/Country.ts`

### Step 2: Add country codes to data
- In `src/services/countryService.ts`, add `countryCode` to every country object:
  - Hungary → "hu", Germany → "de", Japan → "jp", Brazil → "br", Australia → "au", Canada → "ca", Egypt → "eg", South Korea → "kr"

### Step 3: Create ShowCountryDialog component
- Create `src/components/ShowCountryDialog.tsx`
- Accept props: `country: Country`, `onClose: () => void`
- Use `useRef<HTMLDialogElement>` + `useEffect` to call `showModal()` on mount
- Handle native dialog cancel event → call `onClose`
- Render all country fields as read-only label-value pairs
- Render flag image: `<img src="https://flagcdn.com/w320/${country.countryCode}.png" alt="Flag of ${country.name}" />`
- Render a Close button

### Step 4: Create ShowCountryDialog styles
- Create `src/components/ShowCountryDialog.css`
- Follow the same pattern as `EditCountryDialog.css` (dialog sizing, backdrop, spacing)
- Style the detail grid (label + value pairs)
- Style the flag image (bounded width, centered)

### Step 5: Wire up CountryTable
- In `CountryTable.tsx`, add `showingCountry` state (`Country | null`)
- Change `handleShow` to find the country by name and set `showingCountry`
- Render `<ShowCountryDialog>` conditionally when `showingCountry` is set
- Pass `onClose={() => setShowingCountry(null)}`

### Step 6: Update EditCountryDialog for new field
- Add `countryCode` to the edit form so it persists through edits (hidden or readonly input)

### Step 7: Run Validation Commands
- `npm run lint`
- `npm run build`

## Testing Strategy
### Unit Tests
- No unit test runner configured; rely on build-time type checks and lint.

### Integration Tests
- No E2E tests configured; validate via visual review.

### Edge Cases
- Country code doesn't exist at flagcdn → the `<img>` should have an `alt` fallback text
- Dialog should close on Escape key (native `<dialog>` cancel event)
- Dark mode compatibility (use CSS variables)

## Acceptance Criteria
- Clicking Show button opens a modal dialog (not an alert)
- Dialog displays all 7 Country fields as read-only text
- Flag image is displayed below the details using flagcdn.com
- Dialog has a Close button that dismisses it
- Escape key also dismisses the dialog
- Dialog works correctly in dark mode
- No TypeScript or lint errors

## Validation Commands
- `npm run lint` - Run ESLint to validate zero lint errors
- `npm run build` - Type-check and build to validate zero TypeScript errors

## Notes
- Using flagcdn.com which provides free flag images by ISO 3166-1 alpha-2 codes, no API key required
- The country code field is a small, non-breaking addition to the data model
