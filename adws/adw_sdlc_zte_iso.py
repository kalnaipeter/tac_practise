#!/usr/bin/env -S uv run
# /// script
# dependencies = ["python-dotenv", "pydantic"]
# ///

"""
ADW SDLC ZTE Iso — tac_practise (Zero Touch Execution)

Usage: uv run adw_sdlc_zte_iso.py <issue-number> [adw-id] [--skip-e2e] [--skip-resolution]

Zero Touch Execution: Complete SDLC with automatic shipping.
1. Plan (isolated)
2. Build (isolated)
3. Test (isolated)
4. Review (isolated)
5. Document (isolated)
6. Ship (approve & merge PR)

ZTE = Zero Touch Execution: The entire workflow runs to completion without
human intervention, automatically shipping code to production if all phases pass.

WARNING: This will automatically merge to main if all phases pass!

IMPORTANT: 'ZTE' must be EXPLICITLY uppercased in issue commands.
Do not run this if 'zte' is not capitalized.

Adapted from TAC Lesson 7 — Zero-Touch Engineering.
"""

import subprocess
import sys
import os
import uuid
import json


def make_adw_id() -> str:
    return str(uuid.uuid4())[:8]


def load_state(adw_id: str) -> dict:
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    state_path = os.path.join(project_root, "agents", adw_id, "adw_state.json")
    if os.path.exists(state_path):
        with open(state_path, "r") as f:
            return json.load(f)
    return {}


def save_state(adw_id: str, state: dict):
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    state_dir = os.path.join(project_root, "agents", adw_id)
    os.makedirs(state_dir, exist_ok=True)
    with open(os.path.join(state_dir, "adw_state.json"), "w") as f:
        json.dump(state, f, indent=2)


def get_ports_for_adw(adw_id: str) -> tuple:
    try:
        id_chars = ''.join(c for c in adw_id[:8] if c.isalnum())
        index = int(id_chars, 36) % 15
    except ValueError:
        index = hash(adw_id) % 15
    return 9100 + index, 9200 + index


def run_phase(script_name: str, issue_number: str, adw_id: str, extra_args: list = None) -> int:
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
        print("Usage: uv run adw_sdlc_zte_iso.py <issue-number> [adw-id] [--skip-e2e] [--skip-resolution]")
        print("\nZero Touch Execution: Complete SDLC with automatic shipping")
        print("\nPipeline:")
        print("  1. Plan (isolated)")
        print("  2. Build (isolated)")
        print("  3. Test (isolated)")
        print("  4. Review (isolated)")
        print("  5. Document (isolated)")
        print("  6. Ship (approve & merge PR)")
        print("\nWARNING: This will automatically merge to main if all phases pass!")
        sys.exit(1)

    issue_number = sys.argv[1]
    adw_id = sys.argv[2] if len(sys.argv) > 2 else make_adw_id()
    print(f"Using ADW ID: {adw_id}")
    print(f"ZTE MODE: Code will be automatically merged if all phases pass!")

    # Initialize state
    backend_port, frontend_port = get_ports_for_adw(adw_id)
    state = load_state(adw_id) or {}
    state.update({
        "adw_id": adw_id,
        "issue_number": issue_number,
        "backend_port": backend_port,
        "frontend_port": frontend_port,
        "model_set": state.get("model_set", "base"),
        "zte_mode": True,
        "all_adws": state.get("all_adws", []),
    })
    save_state(adw_id, state)

    # Phase 1: Plan + Build + Test
    print(f"\n=== ZTE: PLAN + BUILD + TEST PHASE ===")
    rc = run_phase("adw_plan_build_test.py", issue_number, adw_id)
    if rc != 0:
        print("ZTE ABORTED: Plan + Build + Test phase failed")
        sys.exit(1)

    # Phase 2: Review
    print(f"\n=== ZTE: REVIEW PHASE ===")
    extra = ["--skip-resolution"] if skip_resolution else []
    rc = run_phase("adw_review.py", issue_number, adw_id, extra)
    if rc != 0:
        print("ZTE ABORTED: Review phase failed")
        sys.exit(1)

    # Phase 3: Document
    print(f"\n=== ZTE: DOCUMENT PHASE ===")
    rc = run_phase("adw_document.py", issue_number, adw_id)
    if rc != 0:
        print("WARNING: Document phase failed but continuing with shipping")

    # Phase 4: Ship (approve & merge)
    print(f"\n=== ZTE: SHIP PHASE (APPROVE & MERGE) ===")
    rc = run_phase("adw_ship_iso.py", issue_number, adw_id)
    if rc != 0:
        print("ZTE ABORTED: Ship phase failed")
        sys.exit(1)

    print(f"\n=== ZERO TOUCH EXECUTION COMPLETED ===")
    print(f"ADW ID: {adw_id}")
    print(f"Code has been automatically merged to main!")
    print(f"Ports: backend={backend_port}, frontend={frontend_port}")


if __name__ == "__main__":
    main()
