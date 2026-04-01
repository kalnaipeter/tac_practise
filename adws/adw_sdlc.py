#!/usr/bin/env -S uv run
# /// script
# dependencies = ["python-dotenv", "pydantic"]
# ///

"""
ADW SDLC — tac_practise (Complete Software Development Life Cycle)

Usage: uv run adw_sdlc.py <issue-number> [adw-id]

Composition that chains ALL phases: Plan → Build → Test → Review → Document.
This is the full automated SDLC pipeline for production features.

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
        print("Usage: uv run adw_sdlc.py <issue-number> [adw-id]")
        print("\nThis runs the complete Software Development Life Cycle:")
        print("  1. Plan + Build + Test (adw_plan_build_test.py)")
        print("  2. Review (adw_review.py)")
        print("  3. Document (adw_document.py)")
        sys.exit(1)

    issue_number = sys.argv[1]
    adw_id = sys.argv[2] if len(sys.argv) > 2 else make_adw_id()
    print(f"Using ADW ID: {adw_id}")

    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Phase 1: Plan + Build + Test
    pbt_cmd = ["uv", "run", os.path.join(script_dir, "adw_plan_build_test.py"), issue_number, adw_id]
    print(f"\n=== PLAN + BUILD + TEST PHASE ===")
    print(f"Running: {' '.join(pbt_cmd)}")
    result = subprocess.run(pbt_cmd)
    if result.returncode != 0:
        print("Plan + Build + Test phase failed")
        sys.exit(1)

    # Phase 2: Review
    review_cmd = ["uv", "run", os.path.join(script_dir, "adw_review.py"), issue_number, adw_id]
    print(f"\n=== REVIEW PHASE ===")
    print(f"Running: {' '.join(review_cmd)}")
    result = subprocess.run(review_cmd)
    if result.returncode != 0:
        print("Review phase failed")
        sys.exit(1)

    # Phase 3: Document
    document_cmd = ["uv", "run", os.path.join(script_dir, "adw_document.py"), issue_number, adw_id]
    print(f"\n=== DOCUMENT PHASE ===")
    print(f"Running: {' '.join(document_cmd)}")
    result = subprocess.run(document_cmd)
    if result.returncode != 0:
        print("Document phase failed")
        sys.exit(1)

    print(f"\n✅ Full SDLC workflow finished successfully for issue #{issue_number}")
    print(f"ADW ID: {adw_id}")


if __name__ == "__main__":
    main()
