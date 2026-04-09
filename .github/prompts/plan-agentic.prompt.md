# Plan Agentic Layer Improvement

Create a plan to improve the agentic layer — prompts, ADWs, specs, context, or templates. This is for engineering the system that builds the system, not for application features.

## Instructions

Read `CLAUDE.md` for project context and `ai_docs/agentic-layer-guide.md` for the 12 leverage points.

THINK HARD about which leverage points this improvement targets.

- Research the existing agentic layer: prompts in `.github/prompts/`, ADWs in `adws/`, specs in `specs/`, context in `ai_docs/`
- Create a plan in `specs/agentic-<descriptive-name>.md` using the `Plan Format` below
- IMPORTANT: Replace every `<placeholder>` with real values
- Be precise — agentic layer changes affect all future agent work

## Plan Format

```md
# Agentic Improvement: <name>

## Target Leverage Points
<list which of the 12 leverage points this improves, and why>

## Current State
<describe what exists now and why it's insufficient>

## Desired State
<describe what should exist after this improvement>

## Relevant Files
<list files to create or modify, with bullet points explaining the change>

### New Files
<files that need to be created>

### Modified Files
<existing files that need changes>

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### 1. <First Task>
- <specific action>
- <specific action>

### 2. <Second Task>
- <specific action>

## Validation
<how to verify the improvement works — test the prompt, run the ADW, check the output>

## Impact
<what problem classes does this now handle that weren't handled before?>
```

## Agentic Improvement
$ARGUMENTS

## Relevant Files

- `CLAUDE.md` — Project context and conventions
- `ai_docs/agentic-layer-guide.md` — 12 leverage points reference
- `.github/prompts/` — Existing prompt templates
- `adws/` — ADW scripts
- `specs/` — Existing specs and plans
