# In-Loop Review

Quick checkout and review workflow for validating agent work on a branch.

Use this when an agent has completed work on a branch and you want to manually inspect the results before merging.

## Instructions

IMPORTANT: If no branch name is provided, stop and ask for one.

Follow these steps exactly:

### Step 1 — Fetch and Checkout

```bash
git fetch origin
git checkout $input
```

### Step 2 — Install Dependencies

```bash
npm install
```

### Step 3 — Start Application

```bash
npm run dev
```

The dev server starts at http://localhost:5173.

### Step 4 — Show Changes Summary

Run `git diff origin/main --stat` to show what files changed.
Run `git log origin/main..HEAD --oneline` to show the commits.

### Step 5 — Ready for Review

Report:
- The branch name and number of commits
- Summary of files changed
- The app is running at http://localhost:5173 for manual inspection
- Remind the user to switch back to their original branch when done
