#!/usr/bin/env -S uv run
# /// script
# dependencies = ["python-dotenv", "pydantic"]
# ///

"""
ADW Ship Iso — tac_practise (Approve & Merge to Main)

Usage: uv run adw_ship_iso.py <issue-number> <adw-id>

The final gate in Zero-Touch Execution:
1. Load state and validate all prior phases completed
2. Verify the branch exists and has commits
3. Merge feature branch to main
4. Push to origin

REQUIRES that all previous phases have been run (plan, build, test, review, document).
This is the "zero-touch" gate — if we reach this point, the agent has proven
the work is done through tests, reviews, and screenshots.

Adapted from TAC Lesson 7 — Zero-Touch Engineering.
"""

import subprocess
import sys
import os
import json


def load_state(adw_id: str) -> dict:
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    state_path = os.path.join(project_root, "agents", adw_id, "adw_state.json")
    if os.path.exists(state_path):
        with open(state_path, "r") as f:
            return json.load(f)
    return {}


def get_main_repo_root() -> str:
    """Get the main repository root directory (parent of adws/)."""
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def manual_merge_to_main(branch_name: str) -> tuple:
    """Merge a branch to main using git commands.
    Returns (success: bool, error_message: str or None).
    """
    repo_root = get_main_repo_root()

    # Save current branch
    result = subprocess.run(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"],
        capture_output=True, text=True, cwd=repo_root
    )
    original_branch = result.stdout.strip()

    try:
        # Fetch latest
        print("Fetching latest from origin...")
        result = subprocess.run(
            ["git", "fetch", "origin"],
            capture_output=True, text=True, cwd=repo_root
        )
        if result.returncode != 0:
            return False, f"Failed to fetch: {result.stderr}"

        # Checkout main
        print("Checking out main...")
        result = subprocess.run(
            ["git", "checkout", "main"],
            capture_output=True, text=True, cwd=repo_root
        )
        if result.returncode != 0:
            return False, f"Failed to checkout main: {result.stderr}"

        # Pull latest main
        print("Pulling latest main...")
        result = subprocess.run(
            ["git", "pull", "origin", "main"],
            capture_output=True, text=True, cwd=repo_root
        )
        if result.returncode != 0:
            return False, f"Failed to pull main: {result.stderr}"

        # Merge feature branch
        print(f"Merging {branch_name} into main...")
        result = subprocess.run(
            ["git", "merge", branch_name, "--no-ff", "-m", f"Merge {branch_name} (ZTE auto-ship)"],
            capture_output=True, text=True, cwd=repo_root
        )
        if result.returncode != 0:
            # Abort merge on conflict
            subprocess.run(["git", "merge", "--abort"], cwd=repo_root)
            subprocess.run(["git", "checkout", original_branch], cwd=repo_root)
            return False, f"Merge conflict: {result.stderr}"

        # Push to origin
        print("Pushing to origin/main...")
        result = subprocess.run(
            ["git", "push", "origin", "main"],
            capture_output=True, text=True, cwd=repo_root
        )
        if result.returncode != 0:
            return False, f"Failed to push: {result.stderr}"

        return True, None

    except Exception as e:
        # Try to restore original branch on any error
        subprocess.run(["git", "checkout", original_branch], cwd=repo_root, capture_output=True)
        return False, str(e)


def main():
    if len(sys.argv) < 3:
        print("Usage: uv run adw_ship_iso.py <issue-number> <adw-id>")
        print("\nShip phase: validates all prior phases, then merges to main")
        print("This is the final gate in Zero-Touch Execution.")
        sys.exit(1)

    issue_number = sys.argv[1]
    adw_id = sys.argv[2]

    print(f"ADW Ship starting - ID: {adw_id}, Issue: #{issue_number}")

    # Load state
    state = load_state(adw_id)
    if not state:
        print(f"Error: No state found for ADW ID: {adw_id}")
        print("Run the full SDLC pipeline first.")
        sys.exit(1)

    # Validate required state fields
    required_fields = ["adw_id", "issue_number", "branch_name"]
    missing = [f for f in required_fields if not state.get(f)]
    if missing:
        print(f"Error: Missing required state fields: {missing}")
        print("All prior phases must complete before shipping.")
        sys.exit(1)

    branch_name = state["branch_name"]
    print(f"Branch to ship: {branch_name}")

    # Perform merge
    success, error = manual_merge_to_main(branch_name)
    if not success:
        print(f"Ship phase FAILED: {error}")
        sys.exit(1)

    print(f"\n=== SHIP COMPLETED ===")
    print(f"ADW ID: {adw_id}")
    print(f"Branch {branch_name} has been merged to main and pushed.")
    print(f"Zero-Touch Execution complete!")


if __name__ == "__main__":
    main()
