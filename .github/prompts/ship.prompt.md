# Ship (Approve & Merge)

Merge the current feature branch to main. This is the final gate in a Zero-Touch Execution workflow.

CRITICAL: Only run this after ALL prior phases have passed (plan, build, test, review, document). This merges code to main — it is not reversible.

## Instructions

### Step 1 — Pre-Flight Checks

Verify you are NOT on `main`:
```bash
git branch --show-current
```

If on `main`, STOP — there is nothing to ship.

Verify the branch has commits ahead of main:
```bash
git log origin/main..HEAD --oneline
```

If no commits, STOP — nothing to ship.

### Step 2 — Final Validation

Run a quick validation to confirm the build is green:
```bash
npm run lint
npm run build
```

If either fails, STOP — do not ship broken code.

### Step 3 — Push Branch

```bash
git push origin HEAD
```

### Step 4 — Merge to Main

```bash
git checkout main
git pull origin main
git merge <branch-name> --no-ff -m "Merge <branch-name> (ZTE auto-ship)"
git push origin main
```

### Step 5 — Report

```
## Ship Report

**Branch:** <branch-name>
**Status:** Merged to main
**Validation:** lint pass, build pass
**Merge commit:** <hash>
```
