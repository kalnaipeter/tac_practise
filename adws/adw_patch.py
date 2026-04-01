#!/usr/bin/env -S uv run
# /// script
# dependencies = ["python-dotenv", "pydantic"]
# ///

"""
ADW Patch — tac_practise (standalone patch phase)

Usage: uv run adw_patch.py <github-issue-number> [adw-id]

Quick-fix workflow for resolving a specific issue from a review change
request or an 'adw_patch' keyword in issue comments/body.

Workflow:
1. Fetch GitHub issue details
2. Check for 'adw_patch' keyword in comments or issue body
3. Create patch plan based on content containing 'adw_patch'
4. Implement the patch plan
5. Commit changes
6. Push and create/update PR

Environment Requirements:
- ANTHROPIC_API_KEY: Anthropic API key
- CLAUDE_CODE_PATH: Path to Claude CLI (defaults to "claude")
- GITHUB_PAT: (Optional) GitHub PAT if using different account than 'gh auth login'
"""

import shutil
import subprocess
import sys
import os
import logging
import json
import uuid
from typing import Tuple, Optional
from dotenv import load_dotenv

# Load environment variables — check both adws/ and project root
load_dotenv()
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env"))

_claude_env = os.getenv("CLAUDE_CODE_PATH", "claude")
CLAUDE_PATH = shutil.which(_claude_env) or _claude_env

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def make_adw_id() -> str:
    """Generate a short 8-character UUID for ADW tracking."""
    return str(uuid.uuid4())[:8]


def setup_logger(adw_id: str) -> logging.Logger:
    """Set up logger that writes to both console and file."""
    log_dir = os.path.join(PROJECT_ROOT, "agents", adw_id)
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "patch_execution.log")

    logger = logging.getLogger(f"adw_patch_{adw_id}")
    logger.setLevel(logging.DEBUG)
    logger.handlers.clear()

    file_handler = logging.FileHandler(log_file, mode="a")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter("%(message)s"))

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    logger.info(f"ADW Patch Logger initialized - ID: {adw_id}")
    return logger


def get_github_env() -> Optional[dict]:
    """Get environment with GitHub token if GITHUB_PAT is set."""
    github_pat = os.getenv("GITHUB_PAT")
    if not github_pat:
        return None
    return {"GH_TOKEN": github_pat, "PATH": os.environ.get("PATH", "")}


def get_repo_path() -> str:
    """Get owner/repo from git remote origin."""
    result = subprocess.run(["git", "remote", "get-url", "origin"], capture_output=True, text=True, check=True)
    url = result.stdout.strip()
    return url.replace("https://github.com/", "").replace(".git", "")


def fetch_issue(issue_number: str, repo_path: str) -> dict:
    """Fetch GitHub issue via gh CLI."""
    cmd = [
        "gh", "issue", "view", issue_number, "-R", repo_path,
        "--json", "number,title,body,state,author,labels,comments,url",
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, env=get_github_env())
    if result.returncode != 0:
        raise RuntimeError(f"Failed to fetch issue #{issue_number}: {result.stderr}")
    return json.loads(result.stdout)


def make_issue_comment(issue_number: str, comment: str, repo_path: str) -> None:
    """Post a comment on a GitHub issue."""
    cmd = ["gh", "issue", "comment", issue_number, "-R", repo_path, "--body", comment]
    subprocess.run(cmd, capture_output=True, text=True, env=get_github_env())


def run_claude(prompt: str, adw_id: str, logger: logging.Logger, text_only: bool = False, model: str = "sonnet") -> str:
    """Execute a prompt via Claude Code CLI and return output."""
    if text_only:
        cmd = [CLAUDE_PATH, "--print", "--model", model]
    else:
        cmd = [CLAUDE_PATH, "-p", "-", "--model", model,
               "--output-format", "text", "--dangerously-skip-permissions"]

    logger.debug(f"Running Claude ({'text-only' if text_only else 'agentic'}): {prompt[:200]}...")
    env = os.environ.copy()
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if api_key:
        env["ANTHROPIC_API_KEY"] = api_key
    result = subprocess.run(cmd, capture_output=True, text=True, env=env, input=prompt)
    if result.returncode != 0:
        error_msg = result.stderr or result.stdout or "Unknown error"
        logger.error(f"Claude error: {error_msg}")
        raise RuntimeError(f"Claude execution failed: {error_msg}")
    return result.stdout.strip()


def git_commit(message: str) -> None:
    """Stage all changes and commit. Skips if nothing to commit."""
    subprocess.run(["git", "add", "-A"], capture_output=True, text=True, check=True)
    status = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
    if not status.stdout.strip():
        return
    subprocess.run(["git", "commit", "-m", message], capture_output=True, text=True, check=True)


def load_state(adw_id: str, logger: logging.Logger) -> dict:
    """Load ADW state from agents/{adw_id}/adw_state.json."""
    state_path = os.path.join(PROJECT_ROOT, "agents", adw_id, "adw_state.json")
    if not os.path.exists(state_path):
        logger.warning(f"No state file found at {state_path}")
        return {"adw_id": adw_id}
    with open(state_path, "r") as f:
        state = json.load(f)
    logger.info(f"Loaded state: {json.dumps(state, indent=2)}")
    return state


def save_state(state: dict, adw_id: str) -> None:
    """Save ADW state to agents/{adw_id}/adw_state.json."""
    state_dir = os.path.join(PROJECT_ROOT, "agents", adw_id)
    os.makedirs(state_dir, exist_ok=True)
    state_path = os.path.join(state_dir, "adw_state.json")
    with open(state_path, "w") as f:
        json.dump(state, f, indent=2)


def find_patch_content(issue: dict, logger: logging.Logger) -> Optional[str]:
    """Find 'adw_patch' content from issue comments or body.

    Returns the patch content string if found, None otherwise.
    """
    # Check comments (latest first) for 'adw_patch' keyword
    comments = issue.get("comments", [])
    for comment in reversed(comments):
        body = comment.get("body", "")
        if "adw_patch" in body:
            logger.info(f"Found 'adw_patch' in comment: {body[:100]}...")
            return body

    # Check issue body
    issue_body = issue.get("body", "")
    if "adw_patch" in issue_body:
        logger.info("Found 'adw_patch' in issue body")
        return f"Issue #{issue['number']}: {issue['title']}\n\n{issue_body}"

    return None


def main():
    """Main entry point — standalone patch phase."""
    load_dotenv()

    if len(sys.argv) < 2:
        print("Usage: uv run adw_patch.py <issue-number> [adw-id]")
        print("\nQuick-fix workflow triggered by 'adw_patch' keyword in issue/comments.")
        print("Creates a focused patch plan and implements it.")
        sys.exit(1)

    issue_number = sys.argv[1]
    adw_id = sys.argv[2] if len(sys.argv) > 2 else make_adw_id()
    logger = setup_logger(adw_id)

    if not os.getenv("ANTHROPIC_API_KEY"):
        logger.error("Missing ANTHROPIC_API_KEY")
        sys.exit(1)

    logger.info(f"ADW Patch - ID: {adw_id}")
    logger.info(f"Processing patch for issue #{issue_number}")

    # Connect to GitHub
    try:
        repo_path = get_repo_path()
    except Exception as e:
        logger.error(f"Could not get repo path: {e}")
        sys.exit(1)

    # Fetch issue
    issue = fetch_issue(issue_number, repo_path)
    make_issue_comment(issue_number, f"{adw_id}_patch: ✅ Starting patch workflow", repo_path)

    # Find patch content
    patch_content = find_patch_content(issue, logger)
    if not patch_content:
        logger.error("No 'adw_patch' keyword found in issue body or comments")
        make_issue_comment(
            issue_number,
            f"{adw_id}_patch: ❌ No 'adw_patch' keyword found. Add 'adw_patch' to trigger patch workflow.",
            repo_path,
        )
        sys.exit(1)

    make_issue_comment(
        issue_number,
        f"{adw_id}_patch: ✅ Found patch content — creating plan",
        repo_path,
    )

    # Load existing state (if there is one) or create branch
    state = load_state(adw_id, logger)
    branch_name = state.get("branch_name")

    if not branch_name:
        # Create a patch branch
        issue_slug = issue["title"].lower()[:30].replace(" ", "-")
        issue_slug = "".join(c for c in issue_slug if c.isalnum() or c == "-").strip("-")
        branch_name = f"patch-{issue_number}-{adw_id}-{issue_slug}"
        subprocess.run(["git", "checkout", "main"], capture_output=True, text=True)
        subprocess.run(["git", "pull"], capture_output=True, text=True)
        subprocess.run(["git", "checkout", "-b", branch_name], capture_output=True, text=True, check=True)
        state["branch_name"] = branch_name
        save_state(state, adw_id)

    logger.info(f"Working on branch: {branch_name}")

    # Create patch plan and implement it
    patch_prompt = (
        f"Read the file .github/prompts/patch.prompt.md and follow its instructions with these variables:\n"
        f"- adw_id: {adw_id}\n"
        f"- review_change_request: {patch_content}\n"
        f"- spec_path: {state.get('plan_file', '')}\n"
        f"- agent_name: patch_agent\n\n"
        f"Create the patch plan, then read it and implement every step.\n"
        f"After implementation, run `npm run lint` and `npm run build` to validate."
    )

    try:
        output = run_claude(patch_prompt, adw_id, logger, model="opus")
        logger.info("Patch implemented successfully")
        make_issue_comment(
            issue_number,
            f"{adw_id}_patch: ✅ Patch implemented",
            repo_path,
        )
    except RuntimeError as e:
        logger.error(f"Patch implementation failed: {e}")
        make_issue_comment(
            issue_number,
            f"{adw_id}_patch: ❌ Patch implementation failed: {e}",
            repo_path,
        )
        sys.exit(1)

    # Commit
    git_commit(f"patch: apply patch for #{issue_number}")

    # Push and create PR
    logger.info("Pushing and creating PR...")
    subprocess.run(["git", "push", "-u", "origin", branch_name], capture_output=True, text=True, check=True)

    title = f"patch: #{issue_number} - {issue['title']}"
    body = (
        f"## Summary\n\n"
        f"Patch for #{issue_number}\n\n"
        f"**ADW ID:** `{adw_id}`\n\n"
        f"## Patch Content\n\n{patch_content[:500]}\n"
    )
    pr_cmd = ["gh", "pr", "create", "--title", title, "--body", body, "--base", "main"]
    pr_result = subprocess.run(pr_cmd, capture_output=True, text=True, env=get_github_env())
    if pr_result.returncode == 0:
        pr_url = pr_result.stdout.strip()
        logger.info(f"PR created: {pr_url}")
        make_issue_comment(issue_number, f"{adw_id}_patch: ✅ PR created: {pr_url}", repo_path)
    else:
        logger.warning(f"PR creation failed (may already exist): {pr_result.stderr}")

    logger.info(f"ADW Patch completed for issue #{issue_number}")


if __name__ == "__main__":
    main()
