# Task List

> Multi-agent task tracking file. Tasks are grouped by git worktree.
> Status: `[]` pending | `[⏰]` blocked | `[🟡]` in progress | `[✅]` completed | `[❌]` failed

## How to Use

1. Add tasks under a `## Git Worktree <name>` heading
2. Each task is a single line: `[status] description {optional,tags}`
3. Tasks within a worktree execute sequentially (blocked tasks wait for prior tasks)
4. Tasks across worktrees execute in parallel
5. Tags control routing: `{opus}` for complex tasks, `{adw_plan_implement}` for two-phase workflow

## Git Worktree main
[] Example: Add a new feature using /flow prompt
