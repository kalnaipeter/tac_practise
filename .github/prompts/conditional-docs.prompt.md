# Conditional Documentation Guide

This prompt helps you determine what documentation you should read based on the specific changes you need to make in the codebase. Review the conditions below and read the relevant documentation before proceeding with your task.

## Instructions
- Review the task you've been asked to perform
- Check each documentation path in the Conditional Documentation section
- For each path, evaluate if any of the listed conditions apply to your task
  - IMPORTANT: Only read the documentation if any one of the conditions match your task
- IMPORTANT: You don't want to excessively read documentation. Only read the documentation if it's relevant to your task.

## Conditional Documentation

- README.md
  - Conditions:
    - When first understanding the project structure
    - When you want to learn the commands to start or stop the dev server

- CLAUDE.md
  - Conditions:
    - When you need to understand the project architecture
    - When you need to know the tech stack or commands
    - When you need to understand the ADW system

- src/index.css
  - Conditions:
    - When you need to make changes to global styles or theming

- adws/README.md
  - Conditions:
    - When you're operating in the `adws/` directory
    - When you need to understand the ADW pipeline

- .github/prompts/test.prompt.md
  - Conditions:
    - When you need to run validation commands
    - When you need to understand the test execution sequence

- .github/prompts/bug-validation.prompt.md
  - Conditions:
    - When fixing a bug
    - When you need the bug plan format template

- .github/prompts/review.prompt.md
  - Conditions:
    - When reviewing implementation against a specification
    - When you need to take screenshots for verification

- .github/prompts/patch.prompt.md
  - Conditions:
    - When creating a patch plan for a specific issue
    - When fixing a review issue

- app_docs/feature-flow-show-country-dialog.md
  - Conditions:
    - When working with the Show Country dialog
    - When modifying country detail display or flag images
    - When adding new fields to the Country data model

- app_docs/bugfix-stable-table-column-widths.md
  - Conditions:
    - When modifying table column widths or layout
    - When changing the CountryTable CSS or adding/removing columns
    - When working on pagination or table data display
