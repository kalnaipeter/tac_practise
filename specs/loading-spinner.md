# Feature: Loading Spinner

## Feature Description
Add a loading spinner overlay that appears immediately when the app starts and automatically hides after 3 seconds. This is a testing/chore utility to validate spinner behaviour and loading-state patterns before real async data fetching is introduced. The spinner covers the main content area and displays a CSS-animated spinning indicator.

## User Story
As a developer
I want to see a loading spinner for 3 seconds on app start
So that I can verify the spinner component works correctly before wiring it to real async operations

## Problem Statement
The app has no loading-state handling. When real data fetching is introduced (e.g. fetching countries from an API), there will be a need for a spinner component and loading-state pattern. This chore establishes that infrastructure with a simple timer-based trigger so it can be reviewed and styled before it is needed.

## Solution Statement
Introduce a standalone `LoadingSpinner` component with a CSS-animated spinner. In `App.tsx`, add a `loading` boolean state initialised to `true`. A `useEffect` sets a 3-second timeout that flips `loading` to `false`. While `loading` is `true`, render `<LoadingSpinner />` instead of the normal content. When it expires, the normal app content (`ThemeToggle` + `CountryTable`) is rendered.

## Relevant Files
- **`src/App.tsx`** — root component; will gain `loading` state, `useEffect` timer, and conditional rendering of `<LoadingSpinner />`.
- **`src/App.css`** — app-level styles; may need minor adjustments to ensure the spinner is centred correctly.

### New Files
- **`src/components/LoadingSpinner.tsx`** — new functional component that renders the animated spinner markup.
- **`src/components/LoadingSpinner.css`** — co-located styles with the CSS keyframe animation and layout.

## Implementation Plan
### Phase 1: Foundation
Create the `LoadingSpinner` component and its CSS with the keyframe animation so it can be imported and rendered independently.

### Phase 2: Core Implementation
Implement the full spinner UI: a centred overlay `<div>` containing the spinning element. Define the `@keyframes spin` animation in CSS and apply it to the spinner element.

### Phase 3: Integration
Wire the spinner into `App.tsx` using a `loading` boolean state and a `useEffect` with a 3-second `setTimeout`. Conditionally render `<LoadingSpinner />` while loading, and the normal app content once the timeout fires.

## Step by Step Tasks

### Step 1: Create LoadingSpinner.tsx
- Create `src/components/LoadingSpinner.tsx`
- Export a default functional component `LoadingSpinner` with no props
- Render:
  ```tsx
  <div className="spinner-overlay">
    <div className="spinner" />
  </div>
  ```
- Import `./LoadingSpinner.css`

### Step 2: Create LoadingSpinner.css
- Create `src/components/LoadingSpinner.css`
- Define `.spinner-overlay`:
  - `display: flex; align-items: center; justify-content: center`
  - `position: fixed; inset: 0`
  - `background: var(--bg, #ffffff)` (respects theme)
  - `z-index: 999`
- Define `.spinner`:
  - `width: 48px; height: 48px`
  - `border: 5px solid var(--border, #ccc)`
  - `border-top-color: var(--accent-bg, #3b82f6)` (accent colour for the moving arc)
  - `border-radius: 50%`
  - `animation: spin 0.8s linear infinite`
- Define `@keyframes spin`:
  ```css
  @keyframes spin {
    to { transform: rotate(360deg); }
  }
  ```

### Step 3: Wire spinner into App.tsx
- Add `useState` and `useEffect` to the React import in `src/App.tsx`
- Add state: `const [loading, setLoading] = useState<boolean>(true);`
- Add effect:
  ```ts
  useEffect(() => {
    const timer = setTimeout(() => setLoading(false), 3000);
    return () => clearTimeout(timer);
  }, []);
  ```
- Import `LoadingSpinner` from `./components/LoadingSpinner`
- Wrap existing JSX with conditional rendering:
  ```tsx
  if (loading) return <LoadingSpinner />;
  return (
    <>
      <ThemeToggle />
      <CountryTable />
    </>
  );
  ```

### Step 4: Run validation commands
- Run `npm run build` — must exit with zero errors
- Run `npm run lint` — must exit with zero errors

## Testing Strategy
### Unit Tests
- `LoadingSpinner` renders the `.spinner-overlay` and `.spinner` elements
- `App` renders `LoadingSpinner` on initial mount (`loading` is `true`)
- After 3 seconds (mocked timer), `App` renders `CountryTable` instead of `LoadingSpinner`

### Integration Tests
- On app load the spinner is visible and the table is not
- After the 3-second timer fires the spinner is gone and the table is visible

### Edge Cases
- Timer is cleared on unmount (cleanup in `useEffect` prevents state updates on unmounted component)
- Theme CSS variables are available when the spinner renders (spinner inherits `--bg` and `--border` correctly in both light and dark modes)

## Acceptance Criteria
- [ ] A spinner overlay is visible immediately on app start
- [ ] The spinner rotates continuously using a CSS animation
- [ ] After exactly 3 seconds the spinner disappears and the normal app content renders
- [ ] The spinner uses theme CSS variables so it looks correct in both light and dark mode
- [ ] The `useEffect` cleanup clears the timer on unmount (no memory leak)
- [ ] `npm run build` exits with zero TypeScript errors
- [ ] `npm run lint` exits with zero lint errors

## Validation Commands
Execute every command to validate the feature works correctly with zero regressions.

- `npm run build` - Type-check and build to validate zero TypeScript errors
- `npm run lint` - Run ESLint to validate zero lint errors

## Notes
- No new npm packages are required — the spinner is pure CSS animation.
- The 3-second duration is intentionally hardcoded as a test value; when real async fetching is added, replace the timer with the actual loading state from the data layer.
- The `return () => clearTimeout(timer)` cleanup in `useEffect` prevents a React warning about setting state on an unmounted component (important for strict mode double-invocation).
- CSS variable fallbacks (`var(--bg, #ffffff)`) ensure the spinner renders correctly even if CSS variables are not yet applied.
