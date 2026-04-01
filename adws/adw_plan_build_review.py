#!/usr/bin/env -S uv run
# /// script
# dependencies = ["python-dotenv", "pydantic"]
# ///

"""
ADW Plan, Build & Review — tac_practise

Usage: uv run adw_plan_build_review.py <github-issue-number> [adw-id]

Composition that chains: Plan → Build → Review (skipping tests).
The review phase evaluates implementation against the specification.

The scripts are chained together via persistent state (adw_state.json).
"""

import subprocess
import sys
import os


def make_adw_id() -> str:
    import uuid
    return str(uuid.uuid4())[:8]


def main():
    if len(sys.argv) < 2:
        print("Usage: uv run adw_plan_build_review.py <issue-number> [adw-id]")
        print("\nThis workflow runs:")
        print("  1. Plan + Build (adw_plan_build.py)")
        print("  2. Review (adw_review.py)")
        sys.exit(1)

    issue_number = sys.argv[1]
    adw_id = sys.argv[2] if len(sys.argv) > 2 else make_adw_id()
    print(f"Using ADW ID: {adw_id}")

    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Phase 1: Plan + Build
    plan_build_cmd = ["uv", "run", os.path.join(script_dir, "adw_plan_build.py"), issue_number, adw_id]
    print(f"\n=== PLAN + BUILD PHASE ===")
    print(f"Running: {' '.join(plan_build_cmd)}")
    result = subprocess.run(plan_build_cmd)
    if result.returncode != 0:
        print("Plan + Build phase failed")
        sys.exit(1)

    # Phase 2: Review
    review_cmd = ["uv", "run", os.path.join(script_dir, "adw_review.py"), issue_number, adw_id]
    print(f"\n=== REVIEW PHASE ===")
    print(f"Running: {' '.join(review_cmd)}")
    print("Note: Review is running without test results")
    result = subprocess.run(review_cmd)
    if result.returncode != 0:
        print("Review phase failed")
        sys.exit(1)

    print(f"\n✅ Plan-Build-Review workflow finished successfully for issue #{issue_number}")
    print(f"ADW ID: {adw_id}")


if __name__ == "__main__":
    main()
