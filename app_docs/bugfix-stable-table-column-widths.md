# Bug Fix: Stable Table Column Widths

## Summary

Fixed a visual bug where the country table columns shifted width when navigating between pages. The table now maintains consistent column sizes regardless of the data displayed.

## Problem

When clicking Prev/Next in pagination, the table columns visibly resized because the browser was auto-calculating column widths based on the content of the currently visible rows. Different pages had different data lengths (e.g., "Chad" vs "United Kingdom"), causing layout jumps.

## Solution

Applied three CSS changes to [src/components/CountryTable.css](../src/components/CountryTable.css):

1. **`table-layout: fixed`** — Forces the browser to size columns from the header row and explicit widths, ignoring cell content.
2. **Percentage-based `<th>` widths** — Each column gets a fixed percentage (Name 14%, Capital 13%, Population 12%, Area 12%, Continent 12%, Language 12%, Currency 10%, Actions 15%).
3. **Overflow handling** — `overflow: hidden` + `text-overflow: ellipsis` + `white-space: nowrap` to gracefully truncate long content instead of expanding the column.

## Files Changed

| File | Change |
|---|---|
| `src/components/CountryTable.css` | Added `table-layout: fixed`, column widths, overflow rules |
