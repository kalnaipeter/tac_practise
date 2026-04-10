---
description: "Take a screenshot of the running app. Uses Playwright MCP. IMPORTANT: .vscode/mcp.json and this prompt must be copied to the workspace root to work — VS Code resolves these from the root, not subfolders."
---

# Screenshot

Take a screenshot of the tac_practise app for visual verification. Uses the Playwright MCP server.

## Variables

URL: $1 or http://localhost:5173 if not provided
SCREENSHOT_DIR: tac_practise/app_docs/assets/

## Workflow

1. **Start dev server** — Run `cd tac_practise && npm run dev` in async/background mode
2. **Navigate** — Call `browser_navigate` with the `URL`
3. **Screenshot** — Call `browser_screenshot`
4. **Save** — Save the screenshot to `SCREENSHOT_DIR/screenshot.png`

## Report

- Report the screenshot file path
- Report the URL that was captured
- Mention any visual issues noticed
