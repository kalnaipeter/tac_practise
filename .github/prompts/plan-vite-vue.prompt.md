---
description: "Create a plan for building a Vite + Vue 3 + TypeScript app. Example of a domain-specific template metaprompt."
---

# Plan Vite Vue

Create a plan for building a net new Vite + Vue 3 + TypeScript MVP application from scratch based on the prompt. This command designs and architects a complete Vue.js application, creating a comprehensive implementation roadmap.

## Variables

PROMPT: $ARGUMENTS
APP_NAME: <Create a concise app name based on the prompt, underscores not dashes>

## Instructions

- If the `PROMPT` is not provided, stop and ask the user to provide it.
- IMPORTANT: Create a concise `APP_NAME` based on the `PROMPT` using underscores (e.g., `todo_tracker`, `dashboard_app`).
- Create the plan in `specs/plan-{APP_NAME}-vite-vue.md`
- Research the codebase starting with `CLAUDE.md` and `README.md`
- IMPORTANT: Replace every `<placeholder>` in the `Plan Format`
- Follow existing patterns and conventions in the codebase
- When finished, return only the path to the plan file created.

## Codebase Structure

- `CLAUDE.md` — Project context (start here)
- `README.md` — Project overview
- `adws/` — AI Developer Workflow scripts
- `src/` — Application source code
- `.github/prompts/` — Prompt templates
- `specs/` — Specification and plan documents
- `ai_docs/` — Documentation context for agents

## Workflow

1. **Research the Codebase**: Start with `CLAUDE.md` and `README.md` to understand structure and conventions
2. **Write Plan**: Create the plan document in `specs/` following the Plan Format template

## Plan Format

```md
# Plan: <task name>

## Metadata
prompt: `{PROMPT}`
app_name: `{APP_NAME}`
task_type: <webapp|dashboard|spa|ui>
complexity: <simple|medium|complex>

## Task Description
<describe the task in detail based on the prompt>

## Objective
<clearly state what will be accomplished when this plan is complete>

## Relevant Files
<list files relevant to the task with explanations>

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### 1. <First Task Name>
- <specific action>
- <specific action>

### 2. <Second Task Name>
- <specific action>

## Acceptance Criteria
<list specific, measurable criteria for completion>

## Validation Commands
- `npm run dev` — Run development server
- `npm run build` — Build for production
```

## Report

IMPORTANT: Return only the path to the plan file created.
