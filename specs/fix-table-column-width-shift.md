# Bug Fix: Stable Table Column Widths During Pagination

## Problem

The country table columns resize when navigating between pages because `table-layout` defaults to `auto`, which calculates column widths from cell content. Different data on each page (e.g., shorter/longer country names, population digits) causes visible layout shifts.

## Root Cause

- `CountryTable.css` sets `width: 100%` on `.country-table` but does not set `table-layout: fixed`.
- No explicit column widths are defined on `<th>` elements.
- The browser recalculates column proportions on every page change based on visible row content.

## Solution

1. Add `table-layout: fixed` to `.country-table` so column widths are determined by the first row (the header) and explicit width values, not by cell content.
2. Assign percentage-based widths to each `<th>` in `CountryTable.css` so columns maintain consistent sizes regardless of data.

## Column Width Distribution

| Column | Width | Rationale |
|---|---|---|
| Name | 14% | Medium-length country names |
| Capital | 13% | Similar to name |
| Population | 12% | Right-aligned numbers, tabular-nums |
| Area (km²) | 12% | Right-aligned numbers, tabular-nums |
| Continent | 12% | Short text (e.g., "Europe") |
| Language | 12% | Short-medium text |
| Currency | 10% | Short text (e.g., "EUR") |
| Actions | 15% | Three buttons need space |

Total: 100%

## Acceptance Criteria

- [ ] Table column widths remain identical when clicking Prev/Next between pages
- [ ] No horizontal layout shift or "jump" visible on page change
- [ ] The table still fills its container (100% width)
- [ ] All content remains readable — no excessive truncation
- [ ] Long content in cells is handled gracefully (overflow hidden with ellipsis)

## Validation Commands

```bash
npm run lint
npm run build
```

## Files to Modify

- `src/components/CountryTable.css` — add `table-layout: fixed`, column widths, overflow handling
