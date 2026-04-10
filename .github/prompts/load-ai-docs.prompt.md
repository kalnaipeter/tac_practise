---
description: "Load documentation from URLs into local markdown files for agent context. Example of a delegate prompt with subagent scraping."
---

# Load AI Docs

Load documentation from their respective websites into local markdown files our agents can use as context.

## Variables

DELETE_OLD_AI_DOCS_AFTER_HOURS: 24

## Workflow

1. Read the `ai_docs/README.md` file
2. See if any `ai_docs/<some-filename>.md` file already exists
   1. If it does, see if it was created within the last `DELETE_OLD_AI_DOCS_AFTER_HOURS` hours
   2. If it was, skip it — take a note that it was skipped
   3. If it was not, delete it — take a note that it was deleted
3. For each url in `ai_docs/README.md` that was not skipped, use a subagent in parallel to fetch and scrape the content
   <scrape_loop_prompt>
   Fetch the URL and save the content as a clean markdown file to ai_docs/
   </scrape_loop_prompt>
4. After all tasks are complete, respond in the `Report Format`

## Report Format

```
AI Docs Report:
- <Success or Failure>: <url> - <markdown file path>
- ...
```
