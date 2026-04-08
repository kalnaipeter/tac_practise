# Cleanup Worktrees

Manage isolated ADW worktrees under `trees/`.

## Instructions

Based on the action requested (`$input`):

### If "list" or no argument:
- Run `git worktree list` to show all worktrees
- List contents of `trees/` directory if it exists
- Show which worktrees are active

### If "all":
- List all worktrees that will be removed
- For each worktree under `trees/`:
  ```bash
  git worktree remove trees/<id> --force
  ```
- Run `git worktree prune` to clean up stale entries
- Report how many worktrees were removed

### If a specific ADW ID:
- Check if `trees/<adw-id>` exists
- Run `git worktree remove trees/<adw-id> --force`
- Report success or errors

## Report

- Number of worktrees found/removed
- Any errors encountered
- Current worktree status after cleanup
