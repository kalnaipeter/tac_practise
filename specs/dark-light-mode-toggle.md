# Feature: Dark/Light Mode Toggle

## Feature Description
Add a toggle button to the application that lets users switch between a light and dark color scheme. The app currently has two color sets defined via CSS custom properties — one in `:root` (light) and one in `@media (prefers-color-scheme: dark)` — but there is no manual toggle. This feature adds a visible button that overrides the system preference, applying the selected theme via a `data-theme` attribute on the document root.

## User Story
As a user
I want to click a button to switch between dark and light mode
So that I can choose the color scheme that is most comfortable for my eyes regardless of my system setting

## Problem Statement
The app respects `prefers-color-scheme` but offers no manual override. Users who want to toggle themes must change their OS setting. We need a single button that switches between two explicit color sets.

## Solution Statement
1. Replace the `@media (prefers-color-scheme: dark)` block with a `[data-theme="dark"]` selector so themes are controlled by a data attribute instead of a media query.
2. Create a `ThemeToggle` component that reads the current theme, toggles the `data-theme` attribute on `<html>`, and persists the choice in `localStorage`.
3. Render the `ThemeToggle` button in `App.tsx` above the `CountryTable`.
4. On initial load, apply the theme from `localStorage` (if set) or fall back to the system preference.

## Relevant Files
Use these files to implement the feature:

- `src/index.css` — Defines all CSS custom properties for light and dark themes. The dark variables currently live inside a `@media (prefers-color-scheme: dark)` block that needs to be changed to `[data-theme="dark"]`.
- `src/App.tsx` — Root component where `ThemeToggle` will be rendered.
- `src/App.css` — May need minor layout adjustment to position the toggle.
- `src/components/CountryTable.css` — Uses CSS variables; no changes needed but verify it inherits correctly.
- `src/components/Actions.css` — Uses CSS variables; no changes needed but verify it inherits correctly.
- `CLAUDE.md` — Update architecture section to include the new component.

### New Files
- `src/components/ThemeToggle.tsx` — Toggle button component.
- `src/components/ThemeToggle.css` — Styling for the toggle button.

## Implementation Plan
### Phase 1: Foundation
- Refactor `src/index.css` to replace the `@media (prefers-color-scheme: dark)` block with a `[data-theme="dark"]` selector so the theme is driven by a data attribute.
- Define the two explicit color sets (light is the default `:root`, dark is `[data-theme="dark"]`).

### Phase 2: Core Implementation
- Create `ThemeToggle.tsx`: a button that reads the current theme from `document.documentElement.dataset.theme`, toggles between `"light"` and `"dark"`, and saves to `localStorage`.
- Create `ThemeToggle.css`: style the button to fit the existing design (uses CSS variables, matches action button style).
- On mount, initialise theme from `localStorage` key `"theme"`, falling back to `window.matchMedia('(prefers-color-scheme: dark)')`.

### Phase 3: Integration
- Import and render `<ThemeToggle />` in `App.tsx`, positioned above the country table.
- Add a small script or effect in `main.tsx` (or inline in `index.html`) to set `data-theme` before React hydrates, avoiding a flash of wrong theme.

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### Step 1: Refactor CSS variables in index.css
- Replace the `@media (prefers-color-scheme: dark) { :root { ... } }` block with `[data-theme="dark"] { ... }` using the same dark variable values.
- Keep `:root` as the light theme (it already is).
- Move the `#social .button-icon { filter: ... }` rule into the `[data-theme="dark"]` block.

### Step 2: Add early theme initialisation
- In `index.html`, add an inline `<script>` before the React bundle that reads `localStorage.getItem("theme")` and, if set, applies `document.documentElement.dataset.theme`. If not set, check `window.matchMedia('(prefers-color-scheme: dark)').matches` and apply accordingly. This prevents a flash of unstyled content.

### Step 3: Create ThemeToggle component
- Create `src/components/ThemeToggle.tsx`:
  - Uses `useState<"light" | "dark">` initialised from `document.documentElement.dataset.theme` or `"light"`.
  - On click: toggle the value, set `document.documentElement.dataset.theme`, and save to `localStorage`.
  - Renders a `<button>` with a sun icon (☀️) when dark (clicking switches to light) and a moon icon (🌙) when light (clicking switches to dark).
- Create `src/components/ThemeToggle.css`:
  - Style the button to be a fixed-position or absolutely-positioned toggle in the top-right corner.
  - Use existing CSS variables for border, background, hover states.

### Step 4: Integrate ThemeToggle in App.tsx
- Import `ThemeToggle` and render it at the top of the App return, before `<CountryTable />`.

### Step 5: Update CLAUDE.md architecture
- Add `ThemeToggle.tsx` and `ThemeToggle.css` to the architecture tree in `CLAUDE.md`.

### Step 6: Validate
- Run the `Validation Commands` to ensure zero TypeScript errors and zero lint errors.
- Manually verify: clicking the toggle switches between light and dark color sets. Refreshing the page persists the choice.

## Testing Strategy
### Unit Tests
- Not required for this scope (no test framework currently configured).

### Integration Tests
- Verify toggle button renders in the DOM.
- Verify clicking toggles `data-theme` on `<html>`.
- Verify `localStorage` is updated on toggle.

### Edge Cases
- No `localStorage` value set → fall back to system preference.
- `localStorage` has an invalid value → default to light.
- System preference changes while app is open → manual override should take priority.

## Acceptance Criteria
- [ ] A visible toggle button appears in the top-right area of the app.
- [ ] Clicking the button switches between light and dark themes immediately.
- [ ] Two distinct color sets are applied: light (white background, dark text) and dark (dark background, light text).
- [ ] The chosen theme persists across page reloads via `localStorage`.
- [ ] If no preference is stored, the app falls back to the system `prefers-color-scheme`.
- [ ] No flash of wrong theme on initial load.
- [ ] `npm run build` succeeds with zero errors.
- [ ] `npm run lint` succeeds with zero errors.

## Validation Commands
Execute every command to validate the feature works correctly with zero regressions.

- `npm run build` - Type-check and build to validate zero TypeScript errors
- `npm run lint` - Run ESLint to validate zero lint errors

## Notes
- The two color sets are already defined in `index.css` — this feature primarily wires them up to a manual toggle instead of relying solely on the OS media query.
- The light/dark variable values are already well-designed; no colour changes are needed, just the switching mechanism.
- Future enhancement: add a "system" option as a third mode that re-enables `prefers-color-scheme` following.
