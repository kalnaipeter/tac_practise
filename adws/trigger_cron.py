#!/usr/bin/env -S uv run
# /// script
# dependencies = ["schedule", "python-dotenv", "pydantic"]
# ///

"""
Cron-based ADW Trigger — tac_practise

Polls GitHub every 20 seconds for:
1. New issues without comments (auto-process)
2. Issues where the latest comment is "adw" (manual trigger)

Usage: uv run trigger_cron.py
"""

import os
import signal
import subprocess
import sys
import json
import time
import uuid
from typing import Set, Dict, Optional

import schedule
from dotenv import load_dotenv

load_dotenv()


def get_github_env() -> Optional[dict]:
    """Get environment with GitHub token if set."""
    pat = os.getenv("GITHUB_PAT")
    if not pat:
        return None
    return {"GH_TOKEN": pat, "PATH": os.environ.get("PATH", "")}


def get_repo_path() -> str:
    """Get owner/repo from git remote origin."""
    result = subprocess.run(["git", "remote", "get-url", "origin"], capture_output=True, text=True, check=True)
    return result.stdout.strip().replace("https://github.com/", "").replace(".git", "")


REPO_PATH = get_repo_path()
processed_issues: Set[int] = set()
issue_last_comment: Dict[int, Optional[str]] = {}
shutdown_requested = False


def signal_handler(signum, frame):
    global shutdown_requested
    print(f"\nReceived signal {signum}, shutting down...")
    shutdown_requested = True


signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)


def fetch_open_issues() -> list:
    """Fetch open issues from GitHub."""
    cmd = ["gh", "issue", "list", "-R", REPO_PATH, "--state", "open", "--json", "number,title,comments"]
    result = subprocess.run(cmd, capture_output=True, text=True, env=get_github_env())
    if result.returncode != 0:
        return []
    return json.loads(result.stdout)


def check_and_trigger():
    """Check for issues that need processing."""
    if shutdown_requested:
        return

    issues = fetch_open_issues()
    for issue in issues:
        number = issue["number"]
        comments = issue.get("comments", [])

        if not comments and number not in processed_issues:
            print(f"Issue #{number} has no comments — triggering ADW")
            trigger_adw(number)
            processed_issues.add(number)
        elif comments:
            latest = comments[-1]
            body = latest.get("body", "").strip().lower()
            comment_id = latest.get("id")
            if body == "adw" and issue_last_comment.get(number) != comment_id:
                print(f"Issue #{number} has 'adw' comment — triggering ADW")
                trigger_adw(number)
                issue_last_comment[number] = comment_id


def trigger_adw(issue_number: int):
    """Launch adw_plan_build.py as a background process."""
    adw_id = str(uuid.uuid4())[:8]
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    script = os.path.join(script_dir, "adw_plan_build.py")
    cmd = ["uv", "run", script, str(issue_number), adw_id]
    subprocess.Popen(cmd, cwd=project_root, env=os.environ.copy())
    print(f"Launched ADW {adw_id} for issue #{issue_number}")


def main():
    print(f"Starting ADW cron trigger for {REPO_PATH}")
    print("Polling every 20 seconds. Ctrl+C to stop.\n")

    schedule.every(20).seconds.do(check_and_trigger)
    check_and_trigger()  # Run immediately on start

    while not shutdown_requested:
        schedule.run_pending()
        time.sleep(1)

    print("ADW cron trigger stopped.")


if __name__ == "__main__":
    main()
