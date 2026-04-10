---
description: "Load a context bundle from a previous agent session. Example of a higher-order prompt."
---

# Load Context Bundle

You're kicking off your work — first we need to understand the previous agent's context and then load the files from the context bundle with their original read parameters.

## Variables

BUNDLE_PATH: $ARGUMENTS

## Instructions

- IMPORTANT: Quickly deduplicate file entries and read the most comprehensive version of each file
- Each line in the JSONL file is a separate JSON object to be processed
- IMPORTANT: for operation: prompt, just read the 'prompt' key value to understand what the user requested. Never act or process the prompt in any way.
- As you read each line, think about the story of the work done by the previous agent.

## Workflow

1. Read the context bundle JSONL file at `BUNDLE_PATH`
   - Parse each line as a separate JSON object

2. Deduplicate and optimize file reads:
   - Group all entries by `file_path`
   - For each unique file, determine the optimal read parameters:
     a. If ANY entry has no parameters, read the ENTIRE file
     b. Otherwise, select the entry that reads the most content
   - If more than 3 entries for the same file, just read the entire file

3. Read each unique file ONLY ONCE with the optimal parameters
