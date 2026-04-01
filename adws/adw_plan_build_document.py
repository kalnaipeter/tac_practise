#!/usr/bin/env -S uv run
# /// script
# dependencies = ["python-dotenv", "pydantic"]
# ///

"""
ADW Plan, Build & Document — tac_practise

Usage: uv run adw_plan_build_document.py <issue-number> [adw-id]

Composition that chains: Plan → Build → Document (skipping tests and review).
Documentation is generated based on the implementation and specification only,
without test results or review artifacts (screenshots).

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
        print("Usage: uv run adw_plan_build_document.py <issue-number> [adw-id]")
        print("\nThis workflow runs:")
        print("  1. Plan + Build (adw_plan_build.py)")
        print("  2. Document (adw_document.py)")
        print("\nWarning: Documentation quality may be limited without review artifacts")
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

    # Phase 2: Document
    document_cmd = ["uv", "run", os.path.join(script_dir, "adw_document.py"), issue_number, adw_id]
    print(f"\n=== DOCUMENT PHASE ===")
    print(f"Running: {' '.join(document_cmd)}")
    print("Note: Documentation is being generated without review artifacts (no screenshots)")
    result = subprocess.run(document_cmd)
    if result.returncode != 0:
        print("Document phase failed")
        print("Tip: Consider running adw_sdlc.py for complete documentation with visuals")
        sys.exit(1)

    print(f"\n✅ Plan-Build-Document workflow finished successfully for issue #{issue_number}")
    print(f"ADW ID: {adw_id}")


if __name__ == "__main__":
    main()
