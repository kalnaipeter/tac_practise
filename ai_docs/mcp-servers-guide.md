# MCP Servers Guide

## What is MCP?

MCP (Model Context Protocol) adds specialized tools to your agent beyond reading/writing files and running terminal commands. MCP servers expose structured, typed tools that the agent can discover and call directly.

## Configured Servers

### Playwright (Browser Automation)

**Config:** `.vscode/mcp.json` → `playwright`

**IMPORTANT — Workspace Root Requirement:**
VS Code resolves `.vscode/mcp.json` and `.github/prompts/*.prompt.md` from the **workspace root**, not subfolders. If `tac_practise/` is a subfolder (not the workspace root), you must copy these files to the root:
- Copy `tac_practise/.vscode/mcp.json` → `<workspace-root>/.vscode/mcp.json`
- Copy `tac_practise/.github/prompts/screenshot.prompt.md` → `<workspace-root>/.github/prompts/screenshot.prompt.md`

**What it adds:**
- `browser_navigate` — Open URLs in a headless browser
- `browser_screenshot` — Capture page screenshots
- `browser_click` — Click elements on the page
- `browser_type` — Type into input fields
- `browser_evaluate` — Run JavaScript in the browser console

**Package:** `@playwright/mcp` (via npx, no install needed)

**Used by:** `.github/prompts/screenshot.prompt.md`

**Use cases:**
- Visual verification after UI changes (screenshot before/after)
- E2E testing — navigate, interact, assert visual state
- Automated review — agents can "see" what the app looks like
- Bug reproduction — navigate to a broken state and screenshot it

**Setup:**
1. MCP config is in `.vscode/mcp.json` — ensure it's at the **workspace root**
2. `Ctrl+Shift+P` → "MCP: List Servers" → verify `playwright` shows up
3. Start the server from the list — it should discover 21 tools
4. Open a **new chat** (MCP tools are discovered at session start)
5. IMPORTANT: Use **default agent mode**, not custom modes — custom agents with restricted `tools:` lists may not have access to MCP tools
6. No `npm install` needed — uses `npx` to fetch on demand

## Adding New MCP Servers

### In `.vscode/mcp.json`

Add a new entry under `"servers"`:

```json
{
  "servers": {
    "playwright": { ... },
    "new-server": {
      "command": "npx",
      "args": ["@some-org/mcp-server-name@latest"]
    }
  }
}
```

### Referencing MCP Tools in Prompts

Once a server is running, its tools are available like any other tool. Reference them by their exact tool names in your prompts — short, direct instructions work best:

```md
Use `browser_navigate` to go to http://localhost:5173 and then take a screenshot with `browser_screenshot`.
```

IMPORTANT: Keep MCP prompt instructions as simple direct sentences. Verbose structured formats (numbered steps, sections, variables) cause the agent to skim and skip the MCP tool calls. A single sentence works more reliably than a multi-section workflow.

## Future MCP Servers to Consider

| Server | Purpose | When to Add |
|--------|---------|-------------|
| **Firecrawl** | Clean web → markdown scraping | When `load-ai-docs.prompt.md` needs better extraction than `fetch_webpage` |
| **GitHub** | Create issues, PRs, review comments | When ADW workflows need to auto-create PRs |
| **SQLite/Postgres** | Direct database queries | If the app adds a database layer |
| **Replicate** | Image generation/editing | When `create-image.prompt.md` / `edit-image.prompt.md` need a real backend |

## How MCP Relates to the Agentic Layer

MCP servers are **leverage point #4 (Tools)** from the 12 leverage points in `agentic-layer-guide.md`. They expand what agents can do without writing custom scripts:

- **Without MCP:** Agent runs `curl` in terminal, parses raw text output
- **With MCP:** Agent calls a typed tool, gets structured data back

This matters for reliability — structured tools don't break when output format changes.
