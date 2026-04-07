# Show Country Dialog

**ADW ID:** flow
**Date:** 2026-04-07
**Specification:** specs/show-country-dialog.md

## Overview

Added a Show Country dialog that opens when clicking the Show button in the country table. The dialog displays all country details in a read-only format with the country's flag image rendered below using flagcdn.com.

## What Was Built

- `ShowCountryDialog` component — read-only modal dialog showing all country details
- Flag image integration via flagcdn.com using ISO 3166-1 alpha-2 country codes
- `countryCode` field added to the `Country` data model

## Technical Implementation

### Files Modified

- `src/types/Country.ts`: Added `countryCode: string` to the Country interface
- `src/services/countryService.ts`: Added ISO country codes to all 8 country records
- `src/components/ShowCountryDialog.tsx`: New read-only dialog component with flag image
- `src/components/ShowCountryDialog.css`: Styles for the show dialog (grid layout, flag styling)
- `src/components/CountryTable.tsx`: Wired up `handleShow` to open `ShowCountryDialog` instead of alert
- `src/components/EditCountryDialog.tsx`: Preserved `countryCode` through edit saves

### Key Changes

- Uses native `<dialog>` element with `showModal()` for proper modal behavior
- Flag images loaded from `https://flagcdn.com/w320/{countryCode}.png`
- Details rendered as a `<dl>` definition list with grid layout (label-value pairs)
- Follows the same dialog pattern as `EditCountryDialog` (useRef, cancel event, backdrop)
- Dark mode compatible via CSS custom properties

## How to Use

1. Open the application at http://localhost:5173
2. Find a country in the table
3. Click the **Show** button in the Actions column
4. View all country details and flag in the dialog
5. Click **Close** or press **Escape** to dismiss

## Testing

- Run `npm run lint` — zero errors
- Run `npm run build` — zero errors
- Manual verification: click Show on any row, confirm dialog opens with all fields and flag

## Notes

- flagcdn.com provides free flag images by ISO country code, no API key needed
- If a country code is invalid, the image will fail to load but the `alt` text provides fallback
