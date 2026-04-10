---
description: "Fire off a background agent to perform tasks autonomously. Example of a delegate prompt with system prompt embedding."
---

# Background Agent

Run a background agent instance to perform tasks autonomously while you continue working.

## Variables

USER_PROMPT: $1
MODEL: $2 (defaults to 'sonnet' if not provided)
REPORT_FILE: $3 (defaults to './agents/background/background-report-<timestamp>.md' if not provided)

## Instructions

- Capture timestamp in a variable FIRST to ensure consistency across file creation and references
- Create the initial report file with header BEFORE launching the background agent
- Fire off a new agent instance using the background/async mode
- IMPORTANT: Pass the `USER_PROMPT` exactly as provided with no modifications
- Set the model based on `MODEL` parameter
- All report format instructions are embedded as a system prompt for the background agent

## Workflow

1. Create the report directory if it doesn't exist:
   ```
   mkdir -p agents/background
   ```

2. Set default values for parameters:
   - `MODEL` defaults to 'sonnet'
   - `TIMESTAMP` (capture once for consistency)
   - `REPORT_FILE` (using the captured timestamp)

3. Create the initial report file with just the header (IMPORTANT: Only IF no report file is provided):
   ```
   # Background Agent Report - <TIMESTAMP>
   ```

<primary-agent-delegation>
4. Launch the background agent with the following system prompt embedded:

   "IMPORTANT: You are running as a background agent. Your primary responsibility is to execute work and document your progress continuously in REPORT_FILE. Follow this structure:

   ## Task Understanding
   Clearly state what the user requested.

   ## Progress
   Document each major step as you work. Update this section continuously.

   ## Results
   List concrete outcomes and deliverables with specific details.

   ## Task Completed (or Task Failed)
   Final summary."
</primary-agent-delegation>
