# Install Worktree

Set up an isolated git worktree environment with custom port configuration for parallel agent execution.

This enables multiple agents to work on different issues simultaneously, each in their own complete copy of the repository with dedicated ports.

## Parameters

Provide three values separated by spaces: `<worktree-path> <backend-port> <frontend-port>`

Example: `trees/abc12345 9101 9201`

## Instructions

### Step 1 — Create Worktree

```bash
git fetch origin
git worktree add -b <branch-name> <worktree-path> origin/main
```

Use the worktree directory name as the branch prefix (e.g., `iso/abc12345`).

### Step 2 — Create Port Configuration

Create `<worktree-path>/.ports.env`:
```
BACKEND_PORT=<backend-port>
FRONTEND_PORT=<frontend-port>
VITE_BACKEND_URL=http://localhost:<backend-port>
```

### Step 3 — Copy Environment Files

Copy `.env` from the main repo to the worktree (if it exists).
Append the `.ports.env` contents to the worktree's `.env`.

### Step 4 — Install Dependencies

```bash
cd <worktree-path>
npm install
```

### Step 5 — Verify

Confirm:
- Worktree directory exists
- `.ports.env` is created with correct ports
- Dependencies are installed
- The worktree is registered with git (`git worktree list`)

## Report

- Worktree path (absolute)
- Port assignments (backend + frontend)
- Branch name
- Any issues encountered
