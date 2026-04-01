# Feature: Show Country Dialog

## Feature Description
When a user clicks the "Show" button in the country table, a modal dialog opens displaying all information about the selected country (name, capital, population, area, continent, language, currency). Below the information, a centered country flag image is displayed. The dialog can be dismissed by clicking a close button or clicking outside the modal overlay.

## User Story
As a table user
I want to click the Show button on a country row and see a detailed dialog
So that I can quickly view all country details and its flag without leaving the table view

## Problem Statement
Currently, clicking the "Show" button only triggers a browser `alert()` with the country name. Users have no way to view full country details or a visual flag representation in a rich, accessible dialog UI.

## Solution Statement
Replace the `alert()` stub in `CountryTable` with state that tracks the selected country. Create a new `CountryDialog` component that renders as a modal overlay showing all `Country` fields in a structured layout, with a centered flag image fetched from `flagcdn.com` using a name-to-ISO-code mapping. The dialog closes on backdrop click or close button click.

## Relevant Files
Use these files to implement the feature:

- **`src/components/CountryTable.tsx`** — holds `handleShow`; needs state for `selectedCountry` and renders `CountryDialog`
- **`src/components/Actions.tsx`** — already wires `onShow` callback; no changes needed
- **`src/types/Country.ts`** — `Country` interface drives the dialog's data shape
- **`src/services/countryService.ts`** — `getCountryByName` can retrieve the full country object on show
- **`src/index.css`** — global CSS variables (colors, shadows) to reuse in dialog styles

### New Files
- **`src/components/CountryDialog.tsx`** — new modal dialog component
- **`src/components/CountryDialog.css`** — styles for the modal overlay, dialog box, info rows, flag, and close button

## Implementation Plan
### Phase 1: Foundation
Add a `selectedCountry` state (`Country | null`) to `CountryTable` and wire it to `handleShow` so clicking Show stores the country object. Pass it to the new `CountryDialog` component once created.

### Phase 2: Core Implementation
Build `CountryDialog` as a portal-free modal (appended inside the existing DOM tree with a fixed overlay). It receives a `country: Country | null` and an `onClose: () => void` prop. When `country` is non-null, render:
- A semi-transparent backdrop (`position: fixed, inset: 0`)
- A centered dialog box with all 7 country fields displayed as label/value rows
- A centered `<img>` flag loaded from `https://flagcdn.com/w160/{isoCode}.png` using a country-name-to-ISO-code map
- A close button (×) in the top-right corner

### Phase 3: Integration
- Update `CountryTable` to import and render `<CountryDialog>` below the table, passing `selectedCountry` and a `handleClose` setter.
- Ensure `handleShow` now calls `setSelectedCountry(getCountryByName(name) ?? null)` instead of `alert`.
- Clicking the backdrop calls `onClose`; pressing Escape also closes (via `useEffect` + `keydown` listener).

## Step by Step Tasks

### Step 1: Create the ISO code mapping utility
- In `CountryDialog.tsx`, define a `const COUNTRY_ISO: Record<string, string>` object mapping each country name present in `countryService.ts` to its ISO 3166-1 alpha-2 code (lowercase):
  - Hungary → hu, Germany → de, Japan → jp, Brazil → br, Australia → au, Canada → ca, Egypt → eg, South Korea → kr

### Step 2: Create `CountryDialog.tsx`
- Create `src/components/CountryDialog.tsx`
- Import `useEffect` from React and `Country` type
- Props: `{ country: Country | null; onClose: () => void }`
- Return `null` when `country` is null (nothing to show)
- Render a `<div className="dialog-backdrop">` wrapping a `<div className="dialog-box">`
- Inside `dialog-box`:
  - Close button `<button className="dialog-close" onClick={onClose}>×</button>`
  - `<h2 className="dialog-title">{country.name}</h2>`
  - A `<dl className="dialog-info">` with `<dt>` / `<dd>` pairs for: Capital, Population (formatted with `toLocaleString()`), Area (formatted + " km²"), Continent, Language, Currency
  - A `<div className="dialog-flag">` containing `<img src={...} alt={`Flag of ${country.name}`} />`
- Add `useEffect` to listen for `Escape` key → call `onClose`; clean up listener on unmount

### Step 3: Create `CountryDialog.css`
- Create `src/components/CountryDialog.css`
- `.dialog-backdrop`: `position: fixed; inset: 0; background: rgba(0,0,0,0.45); display: flex; align-items: center; justify-content: center; z-index: 1000;` — clicking it calls `onClose`
- `.dialog-box`: `background: var(--bg); border: 1px solid var(--border); border-radius: 10px; padding: 2rem; min-width: 320px; max-width: 480px; width: 90%; position: relative; box-shadow: var(--shadow);` — stop propagation on click so backdrop click doesn't trigger close
- `.dialog-close`: positioned top-right (`position: absolute; top: 0.75rem; right: 1rem`), minimal styling, large × glyph
- `.dialog-title`: margin adjustments, uses `--text-h`
- `.dialog-info`: `display: grid; grid-template-columns: auto 1fr; gap: 0.4rem 1rem; margin: 1rem 0;`
- `dt`: `font-weight: 600; color: var(--text-h);`
- `dd`: `margin: 0; color: var(--text);`
- `.dialog-flag`: `text-align: center; margin-top: 1.5rem;`
- `.dialog-flag img`: `max-width: 160px; border: 1px solid var(--border); border-radius: 4px;`

### Step 4: Update `CountryTable.tsx`
- Import `useState` (already imported), `getCountryByName` from `countryService`, `CountryDialog`
- Add state: `const [selectedCountry, setSelectedCountry] = useState<Country | null>(null);`
- Replace `handleShow`: `const handleShow = (name: string) => setSelectedCountry(getCountryByName(name) ?? null);`
- Add `const handleClose = () => setSelectedCountry(null);`
- Render `<CountryDialog country={selectedCountry} onClose={handleClose} />` just before the closing `</div>` of `country-table-wrapper`

### Step 5: Validate
- Run `npm run lint` — resolve any lint errors
- Run `npm run build` — resolve any TypeScript/build errors

## Testing Strategy
### Unit Tests
- `CountryDialog` renders `null` when `country` prop is `null`
- `CountryDialog` renders all 7 fields when a country is provided
- `CountryDialog` calls `onClose` when the × button is clicked
- `CountryDialog` calls `onClose` when the backdrop is clicked
- `CountryDialog` does NOT call `onClose` when the dialog box itself is clicked
- Flag `<img>` has the correct `src` for each known country

### Integration Tests
- Clicking "Show" on a table row opens the dialog with correct country data
- Clicking close in the dialog returns to the table (dialog disappears)

### Edge Cases
- Country name not in ISO map → flag `src` resolves to `undefined`; handle gracefully (hide img or show placeholder)
- Very long country names or values don't break the dialog layout
- Dialog is accessible: focus is trapped or at minimum the close button is focusable

## Acceptance Criteria
- Clicking the "Show" button for any country opens a dialog (no `alert`)
- The dialog displays all 7 fields: name, capital, population, area, continent, language, currency
- Population and area are formatted with `toLocaleString()` / unit suffix
- A flag image is rendered centered below the info, sized ~160px wide
- The dialog closes when the × button is clicked
- The dialog closes when the backdrop is clicked
- The dialog closes when the Escape key is pressed
- No TypeScript errors (`npm run build` passes)
- No lint errors (`npm run lint` passes)
- Dark mode CSS variables apply correctly to the dialog

## Validation Commands
Execute every command to validate the feature works correctly with zero regressions.

- `npm run lint` - Run ESLint to validate zero lint errors
- `npm run build` - Type-check and build to validate zero TypeScript errors

## Notes
- Flag images are sourced from `https://flagcdn.com/w160/{isoCode}.png` (free, no API key needed). The `w160` variant gives a ~160px-wide PNG.
- The ISO mapping only needs to cover the 8 countries currently in `countryService.ts`. If new countries are added in the future, extend the map.
- No new npm packages are required; the feature uses only React built-ins and plain CSS.
- The dialog does not use `<dialog>` HTML element to keep the implementation simple and consistent with the existing plain-CSS approach, but a future enhancement could migrate to native `<dialog>` for better accessibility.
