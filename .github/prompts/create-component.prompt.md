---
description: "Create a new React component in tac_practise with proper structure. Use when: adding a new component, creating UI features."
---

# Create React Component

You are working on the `tac_practise` React + TypeScript application.

## Variables

- `$COMPONENT_NAME` — Name of the component (PascalCase)
- `$DESCRIPTION` — What the component does

## Workflow

1. CREATE `src/components/${COMPONENT_NAME}.tsx`:
   - Use functional component with TypeScript
   - Import types from `src/types/` if needed
   - Use data from `src/services/` if needed

2. CREATE `src/components/${COMPONENT_NAME}.css`:
   - Use CSS variables from the app's theme (--border, --text-h, --accent-bg, etc.)

3. VERIFY the component compiles with no TypeScript errors

## Constraints
- DO NOT modify existing components unless integrating into App.tsx
- KEEP the component focused and simple
- USE the existing service layer for data
