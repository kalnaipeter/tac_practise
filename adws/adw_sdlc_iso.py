#!/usr/bin/env -S uv run
# /// script
# dependencies = ["python-dotenv", "pydantic"]
# ///

"""
ADW SDLC Iso — tac_practise (Complete SDLC with Worktree Isolation)

Usage: uv run adw_sdlc_iso.py <issue-number> [adw-id] [--skip-e2e] [--skip-resolution]

This script runs the complete ADW SDLC pipeline in isolation:
1. Plan (in isolated worktree)
2. Build (in isolated worktree)
3. Test (in isolated worktree)
4. Review (in isolated worktree)
5. Document (in isolated worktree)

Each phase runs in its own git worktree under trees/<adw-id>/ with dedicated
ports, enabling parallel agent pipelines without interference.

The key difference from adw_sdlc.py: worktree isolation allows multiple
agents to execute simultaneously on different issues.

Adapted from TAC Lesson 7 — Zero-Touch Engineering.
"""

import subprocess
import sys
import os
import uuid
import json


def make_adw_id() -> str:
    return str(uuid.uuid4())[:8]


def ensure_state_dir(adw_id: str) -> str:
    """Create and return the agents/<adw_id>/ directory."""
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    state_dir = os.path.join(project_root, "agents", adw_id)
    os.makedirs(state_dir, exist_ok=True)
    return state_dir


def save_state(adw_id: str, state: dict):
    """Save workflow state to agents/<adw_id>/adw_state.json."""
    state_dir = ensure_state_dir(adw_id)
    state_path = os.path.join(state_dir, "adw_state.json")
    with open(state_path, "w") as f:
        json.dump(state, f, indent=2)


def load_state(adw_id: str) -> dict:
    """Load workflow state from agents/<adw_id>/adw_state.json."""
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    state_path = os.path.join(project_root, "agents", adw_id, "adw_state.json")
    if os.path.exists(state_path):
        with open(state_path, "r") as f:
            return json.load(f)
    return {}


def get_ports_for_adw(adw_id: str) -> tuple:
    """Deterministically assign ports based on ADW ID.
    Backend: 9100-9114, Frontend: 9200-9214 (15 concurrent slots).
    """
    try:
        id_chars = ''.join(c for c in adw_id[:8] if c.isalnum())
        index = int(id_chars, 36) % 15
    except ValueError:
        index = hash(adw_id) % 15
    return 9100 + index, 9200 + index


def create_worktree(adw_id: str, branch_name: str) -> str:
    """Create a git worktree for isolated execution.
    Returns the absolute path to the worktree.
    """
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    trees_dir = os.path.join(project_root, "trees")
    os.makedirs(trees_dir, exist_ok=True)
    worktree_path = os.path.join(trees_dir, adw_id)

    if os.path.exists(worktree_path):
        print(f"Worktree already exists at {worktree_path}")
        return worktree_path

    # Fetch latest
    subprocess.run(["git", "fetch", "origin"], capture_output=True, text=True, cwd=project_root)

    # Create worktree with new branch from origin/main
    cmd = ["git", "worktree", "add", "-b", branch_name, worktree_path, "origin/main"]
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=project_root)
    if result.returncode != 0:
        if "already exists" in result.stderr:
            cmd = ["git", "worktree", "add", worktree_path, branch_name]
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=project_root)
        if result.returncode != 0:
            print(f"Failed to create worktree: {result.stderr}")
            sys.exit(1)

    print(f"Created worktree at {worktree_path} for branch {branch_name}")
    return worktree_path


def run_phase(script_name: str, issue_number: str, adw_id: str, extra_args: list = None):
    """Run a single ADW phase script, passing issue number and adw_id."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    cmd = ["uv", "run", os.path.join(script_dir, script_name), issue_number, adw_id]
    if extra_args:
        cmd.extend(extra_args)
    print(f"\nRunning: {' '.join(cmd)}")
    result = subprocess.run(cmd)
    return result.returncode


def main():
    skip_e2e = "--skip-e2e" in sys.argv
    skip_resolution = "--skip-resolution" in sys.argv
    if skip_e2e:
        sys.argv.remove("--skip-e2e")
    if skip_resolution:
        sys.argv.remove("--skip-resolution")

    if len(sys.argv) < 2:
        print("Usage: uv run adw_sdlc_iso.py <issue-number> [adw-id] [--skip-e2e] [--skip-resolution]")
        print("\nComplete isolated SDLC pipeline:")
        print("  1. Plan (isolated worktree)")
        print("  2. Build (isolated worktree)")
        print("  3. Test (isolated worktree)")
        print("  4. Review (isolated worktree)")
        print("  5. Document (isolated worktree)")
        sys.exit(1)

    issue_number = sys.argv[1]
    adw_id = sys.argv[2] if len(sys.argv) > 2 else make_adw_id()
    print(f"Using ADW ID: {adw_id}")

    # Initialize state with port allocation
    backend_port, frontend_port = get_ports_for_adw(adw_id)
    state = load_state(adw_id) or {}
    state.update({
        "adw_id": adw_id,
        "issue_number": issue_number,
        "backend_port": backend_port,
        "frontend_port": frontend_port,
        "model_set": state.get("model_set", "base"),
        "all_adws": state.get("all_adws", []),
    })
    save_state(adw_id, state)

    # Phase 1: Plan + Build + Test (reuse existing pipeline)
    print(f"\n=== ISOLATED PLAN + BUILD + TEST PHASE ===")
    rc = run_phase("adw_plan_build_test.py", issue_number, adw_id)
    if rc != 0:
        print("Plan + Build + Test phase failed")
        sys.exit(1)

    # Phase 2: Review
    print(f"\n=== ISOLATED REVIEW PHASE ===")
    extra = ["--skip-resolution"] if skip_resolution else []
    rc = run_phase("adw_review.py", issue_number, adw_id, extra)
    if rc != 0:
        print("Review phase failed")
        sys.exit(1)

    # Phase 3: Document
    print(f"\n=== ISOLATED DOCUMENT PHASE ===")
    rc = run_phase("adw_document.py", issue_number, adw_id)
    if rc != 0:
        print("Document phase failed")
        sys.exit(1)

    print(f"\n=== ISOLATED SDLC COMPLETED ===")
    print(f"ADW ID: {adw_id}")
    print(f"All phases completed successfully!")
    print(f"\nWorktree location: trees/{adw_id}/ (if isolation was used)")
    print(f"Ports: backend={backend_port}, frontend={frontend_port}")


if __name__ == "__main__":
    main()
