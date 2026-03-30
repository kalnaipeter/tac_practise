# Search & Filter Feature

## Overview
Add a search bar and continent filter dropdown above the country table so users can find countries quickly.

## Architecture
- New component: `src/components/SearchFilter.tsx` + `SearchFilter.css`
- State management: lift filter state into `CountryTable.tsx`, pass filtered data to the table body
- No new services needed — filtering is client-side on the existing `Country[]`

## Data Models
No new types. Uses existing `Country` interface fields:
- Search: matches against `name` and `capital` (case-insensitive)
- Filter: matches against `continent` (exact match, or "All")

## Implementation Steps
1. Create `SearchFilter` component with a text input and a `<select>` dropdown
2. Extract unique continents from `countryService` data for the dropdown options
3. Add `searchTerm` and `continentFilter` state to `CountryTable`
4. Filter the `countries` array before mapping to `<tr>` elements
5. Style the search/filter bar to sit above the table

## Acceptance Criteria
- [ ] Typing in the search box filters countries by name or capital in real-time
- [ ] Selecting a continent from the dropdown shows only countries on that continent
- [ ] Selecting "All" in the dropdown resets the continent filter
- [ ] Both filters work together (search + continent)
- [ ] No TypeScript errors, `npm run build` succeeds
