# Feature: Edit Country

## Feature Description
Add an edit dialog that lets users modify any field of a country entry directly from the table. Clicking the "Edit" button opens a modal dialog pre-filled with the country's current data. The user can change any field and either save the changes (updating the table row in place) or revert/cancel (discarding all edits and closing the dialog unchanged).

## User Story
As a table user
I want to click "Edit" on a country row and update its data in a dialog
So that I can correct or update country information without leaving the page

## Problem Statement
Currently the "Edit" button in `Actions` only fires an `alert()` — there is no real way to modify country data. Users cannot update any country field, making the table read-only.

## Solution Statement
Replace the `alert` placeholder with a proper modal dialog (`<dialog>` HTML element) that renders a form with one labelled input per country field, pre-populated with the selected country's current values. Saving commits the changes to the in-memory country list; cancelling/reverting discards them. The dialog follows the existing design system (CSS variables, consistent button styles).

## Relevant Files
Use these files to implement the feature:

- `src/components/CountryTable.tsx` — owns country state; needs to switch from read-only `useState` to a mutable list and wire up `handleEdit` to open the dialog and `handleSave` to commit changes.
- `src/components/Actions.tsx` — already exposes `onEdit` prop; no API change needed.
- `src/types/Country.ts` — defines the `Country` interface; all fields must appear in the form.
- `src/index.css` — global CSS variables used for consistent theming.

### New Files
- `src/components/EditCountryDialog.tsx` — new modal dialog component; receives the country being edited and callbacks for save/cancel.
- `src/components/EditCountryDialog.css` — co-located styles for the dialog overlay, form layout, and action buttons.

## Implementation Plan
### Phase 1: Foundation
Make `CountryTable` hold a mutable country list so edits can be persisted in-memory. Change `const [countries] = useState<Country[]>(getCountries)` to `const [countries, setCountries] = useState<Country[]>(getCountries)`. Add `editingCountry` state (`Country | null`, default `null`) to track which row is open.

### Phase 2: Core Implementation
Build `EditCountryDialog` as a controlled form component:
- Accepts `country: Country`, `onSave: (updated: Country) => void`, `onCancel: () => void`.
- Uses `useState` internally to hold draft field values, seeded from `country` on open.
- Renders the native `<dialog>` element (opened via `ref.current.showModal()`).
- Contains a labelled `<input>` for each of the 7 fields; `population` and `area` use `type="number"`.
- Footer has two buttons: **Save** (submits changes) and **Cancel** (closes without saving).
- Clicking the backdrop also cancels (listens to the dialog `cancel` event).

### Phase 3: Integration
Wire everything together in `CountryTable`:
- `handleEdit(name)` — finds the country by name and sets `editingCountry`.
- `handleSave(updated)` — replaces the matching entry in `countries`, clears `editingCountry`.
- `handleCancelEdit()` — clears `editingCountry`.
- Conditionally render `<EditCountryDialog>` when `editingCountry !== null`.

## Step by Step Tasks

### Step 1 — Create EditCountryDialog.css
- Add styles for the `<dialog>` element: centered overlay using `margin: auto`, backdrop via `::backdrop`, box-shadow using `var(--shadow)`, border-radius, background `var(--bg)`, border `1px solid var(--border)`.
- Style `.edit-dialog-title` (heading inside dialog).
- Style `.edit-dialog-form` as a grid with two columns (label + input) using CSS grid.
- Style `.edit-dialog-label` for right-aligned labels.
- Style `.edit-dialog-input` to match existing input aesthetics: full width, border `1px solid var(--border)`, border-radius 4px, padding, font inherits, background `var(--bg)`, color `var(--text-h)`.
- Style `.edit-dialog-footer` as a flex row justified to the end with a gap.
- Reuse `.action-btn` class pattern for Save and Cancel buttons (or define `.edit-btn-save` / `.edit-btn-cancel`).

### Step 2 — Create EditCountryDialog.tsx
- Import `useRef`, `useEffect`, `useState` from React; import `Country` type; import `EditCountryDialog.css`.
- Define props interface: `{ country: Country; onSave: (updated: Country) => void; onCancel: () => void }`.
- Inside the component, hold `draft` state initialised from `country` prop.
- Use `useRef<HTMLDialogElement>(null)` and call `dialogRef.current.showModal()` in a `useEffect` on mount.
- Listen to the dialog's `cancel` event (Escape key) to call `onCancel`.
- Render a `<dialog>` with a heading showing "Edit — {country.name}".
- Render a `<form>` (no native submit — use button `type="button"`) with a labelled field for each `Country` key:
  - `name` (text)
  - `capital` (text)
  - `population` (number)
  - `area` (number)
  - `continent` (text)
  - `language` (text)
  - `currency` (text)
- Each `<input>` uses `value={draft[field]}` and `onChange` to update draft state.
- **Save** button calls `onSave(draft)` after casting `population` and `area` back to `number`.
- **Cancel** button calls `onCancel()`.

### Step 3 — Update CountryTable.tsx
- Change `const [countries] = useState` → `const [countries, setCountries] = useState`.
- Add `const [editingCountry, setEditingCountry] = useState<Country | null>(null)`.
- Replace `handleEdit` stub:
  ```ts
  const handleEdit = (name: string) => {
    const found = countries.find((c) => c.name === name) ?? null;
    setEditingCountry(found);
  };
  ```
- Add `handleSave`:
  ```ts
  const handleSave = (updated: Country) => {
    setCountries((prev) =>
      prev.map((c) => (c.name === editingCountry?.name ? updated : c))
    );
    setEditingCountry(null);
  };
  ```
- Add `handleCancelEdit`:
  ```ts
  const handleCancelEdit = () => setEditingCountry(null);
  ```
- Conditionally render below the table wrapper (but inside the outer `<div>`):
  ```tsx
  {editingCountry && (
    <EditCountryDialog
      country={editingCountry}
      onSave={handleSave}
      onCancel={handleCancelEdit}
    />
  )}
  ```
- Add import for `EditCountryDialog`.

### Step 4 — Validate
- Run `npm run lint` and fix any issues.
- Run `npm run build` and fix any TypeScript errors.

## Testing Strategy
### Unit Tests
- `EditCountryDialog` renders all 7 fields with correct initial values from `country` prop.
- Changing a field updates the draft state (controlled inputs).
- Clicking **Save** calls `onSave` with the updated country object.
- Clicking **Cancel** calls `onCancel` without calling `onSave`.

### Integration Tests
- Clicking "Edit" in a table row opens the dialog with correct pre-filled values.
- Saving a change updates the corresponding row in the table.
- Cancelling leaves the row data unchanged.

### Edge Cases
- Editing a country and pressing Escape closes the dialog without saving.
- Entering a non-numeric value in `population` or `area` is handled gracefully (inputs are `type="number"`).
- Editing the `name` field — the save logic should still match on the **original** name to avoid row-not-found bugs.

## Acceptance Criteria
- Clicking **Edit** on any row opens a modal dialog.
- The dialog is pre-filled with all 7 fields of the selected country.
- All fields are editable (text inputs for strings, number inputs for population and area).
- Clicking **Save** closes the dialog and reflects the updated values in the table row.
- Clicking **Cancel** closes the dialog; the table row is unchanged.
- Pressing Escape also cancels without saving.
- The dialog matches the existing light/dark theme via CSS variables.
- `npm run lint` passes with zero errors.
- `npm run build` passes with zero TypeScript errors.

## Validation Commands
Execute every command to validate the feature works correctly with zero regressions.

- `npm run lint` - Run ESLint to validate zero lint errors
- `npm run build` - Type-check and build to validate zero TypeScript errors

## Notes
- Using the native `<dialog>` element gives accessible focus-trapping and Escape-key handling for free — no external library needed.
- Country data is stored only in React state (in-memory); a page refresh resets all edits. Persistence to a backend or localStorage is out of scope.
- The edit dialog intentionally does not prevent duplicate country names — validation is out of scope for this iteration.
- `population` and `area` inputs are `type="number"` but stored as strings inside `draft`; cast with `Number()` before calling `onSave` to satisfy the `Country` interface.
