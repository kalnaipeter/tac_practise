---
description: "Create a new prompt file from a high-level description using a specified template format. Example of a template metaprompt."
---

# MetaPrompt Workflow

Based on the `High Level Prompt` follow the `Workflow` to create a new prompt in the `Specified Format`. Before you start, read the `Documentation`.

## Variables

HIGH_LEVEL_PROMPT: $ARGUMENTS

## Workflow

- We're building a new prompt to satisfy the request in the `High Level Prompt`.
- Save the new prompt to `.github/prompts/<name-of-prompt>.prompt.md`
  - The name should make sense based on the `High Level Prompt`
- VERY IMPORTANT: The prompt should be in the `Specified Format`
  - Do not create any additional sections or headers that are not in the `Specified Format`
- IMPORTANT: Replace every block of `<some request>` with the request detailed within the braces.
- If the `High Level Prompt` requested multiple arguments, give each their own section.
- If no variables are requested or mentioned, do not create a Variables section.
- Think through what the static variables vs dynamic variables are — dynamic first, static second.

## Documentation

- Read `CLAUDE.md` for project conventions
- Read `ai_docs/copilot-workflow.md` for prompt patterns used in this project
- Scan existing prompts in `.github/prompts/` for style reference

## Specified Format

```md
---
description: "<description to identify this prompt>"
---

# <name_of_prompt>

<prompt purpose: describe what the prompt does at a high level and reference any sections like Instructions or Workflow>

## Variables

<NAME_OF_DYNAMIC_VARIABLE>: $1
<NAME_OF_DYNAMIC_VARIABLE>: $2
<NAME_OF_STATIC_VARIABLE>: <SOMETHING STATIC>

## Instructions

<bullet point list of rules, constraints, and important behaviors>

## Workflow

<step by step numbered list of tasks to complete>

## Report

<details of how the prompt should respond back to the user>
```
