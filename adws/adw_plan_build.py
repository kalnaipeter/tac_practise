#!/usr/bin/env -S uv run
# /// script
# dependencies = ["python-dotenv", "pydantic"]
# ///

"""
ADW Plan & Build — tac_practise

Usage: uv run adw_plan_build.py <github-issue-number> [adw-id]

Workflow:
1. Fetch GitHub issue details
2. Classify issue type (/chore, /bug, /feature)
3. Create feature branch
4. Plan Agent: Generate implementation plan in specs/*.md
5. Build Agent: Implement the solution
6. Create PR with full context

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


def make_adw_id() -> str:
    """Generate a short 8-character UUID for ADW tracking."""
    return str(uuid.uuid4())[:8]


def setup_logger(adw_id: str) -> logging.Logger:
    """Set up logger that writes to both console and file."""
    log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "agents", adw_id)
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "execution.log")

    logger = logging.getLogger(f"adw_{adw_id}")
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
    logger.info(f"ADW Logger initialized - ID: {adw_id}")
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


def run_claude(prompt: str, adw_id: str, logger: logging.Logger) -> str:
    """Execute a prompt via Claude Code CLI and return output."""
    cmd = [CLAUDE_PATH, "--print", "--model", "sonnet", "-p", prompt]
    logger.debug(f"Running Claude: {prompt[:200]}...")
    # Pass full environment so Claude picks up ANTHROPIC_API_KEY
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


def classify_issue(issue: dict, adw_id: str, logger: logging.Logger) -> str:
    """Classify a GitHub issue as /chore, /bug, or /feature."""
    prompt = (
        "You are a GitHub issue classifier. "
        "Based on the issue below, respond with ONLY one word — one of these three exactly:\n"
        "/chore\n/bug\n/feature\n\n"
        "No explanation, no other text. Just the command.\n\n"
        f"Issue Title: {issue['title']}\n"
        f"Issue Body: {issue.get('body', '')}"
    )
    result = run_claude(prompt, adw_id, logger)
    logger.info(f"Classification raw response: {result}")
    # Extract the command from the response (Claude may add extra text)
    for cmd in ("/chore", "/bug", "/feature"):
        if cmd in result.lower():
            return cmd
    raise ValueError(f"Invalid classification: {result}")


def generate_branch_name(issue: dict, issue_class: str, adw_id: str) -> str:
    """Generate and checkout a feature branch."""
    issue_type = issue_class.replace("/", "")
    number = issue["number"]
    # Create a slug from the title
    slug = issue["title"].lower()[:40].replace(" ", "-")
    slug = "".join(c for c in slug if c.isalnum() or c == "-").strip("-")
    branch_name = f"{issue_type}-{number}-{adw_id}-{slug}"

    subprocess.run(["git", "checkout", "main"], capture_output=True, text=True)
    subprocess.run(["git", "pull"], capture_output=True, text=True)
    subprocess.run(["git", "checkout", "-b", branch_name], capture_output=True, text=True, check=True)
    return branch_name


def git_commit(message: str) -> None:
    """Stage all changes and commit."""
    subprocess.run(["git", "add", "-A"], capture_output=True, text=True, check=True)
    subprocess.run(["git", "commit", "-m", message], capture_output=True, text=True, check=True)


def create_pull_request(branch_name: str, issue: dict, adw_id: str) -> str:
    """Push branch and create a PR."""
    subprocess.run(["git", "push", "-u", "origin", branch_name], capture_output=True, text=True, check=True)
    title = f"{branch_name.split('-')[0]}: #{issue['number']} - {issue['title']}"
    body = (
        f"## Summary\n\n"
        f"Resolves #{issue['number']}\n\n"
        f"**ADW ID:** `{adw_id}`\n\n"
        f"## Issue\n\n{issue.get('body', 'No description')}\n"
    )
    cmd = ["gh", "pr", "create", "--title", title, "--body", body, "--base", "main"]
    result = subprocess.run(cmd, capture_output=True, text=True, env=get_github_env(), check=True)
    return result.stdout.strip()


def main():
    """Main ADW orchestrator."""
    load_dotenv()

    if len(sys.argv) < 2:
        print("Usage: uv run adw_plan_build.py <issue-number> [adw-id]")
        sys.exit(1)

    issue_number = sys.argv[1]
    adw_id = sys.argv[2] if len(sys.argv) > 2 else make_adw_id()
    logger = setup_logger(adw_id)
    repo_path = get_repo_path()

    # Check prerequisites
    if not os.getenv("ANTHROPIC_API_KEY"):
        logger.error("Missing ANTHROPIC_API_KEY")
        sys.exit(1)

    logger.info(f"ADW ID: {adw_id}")
    logger.info(f"Processing issue #{issue_number}")

    # 1. Fetch issue
    issue = fetch_issue(issue_number, repo_path)
    make_issue_comment(issue_number, f"{adw_id}_ops: ✅ Starting ADW workflow", repo_path)

    # 2. Classify
    issue_command = classify_issue(issue, adw_id, logger)
    logger.info(f"Issue classified as: {issue_command}")
    make_issue_comment(issue_number, f"{adw_id}_ops: ✅ Issue classified as: {issue_command}", repo_path)

    # 3. Create branch
    branch_name = generate_branch_name(issue, issue_command, adw_id)
    logger.info(f"Working on branch: {branch_name}")
    make_issue_comment(issue_number, f"{adw_id}_ops: ✅ Working on branch: {branch_name}", repo_path)

    # 4. Plan — use the appropriate template
    logger.info("Building implementation plan...")
    make_issue_comment(issue_number, f"{adw_id}_planner: ✅ Building implementation plan", repo_path)
    plan_prompt = f"Read the file .github/prompts/{issue_command.replace('/', '')}.prompt.md and follow its instructions with these arguments: {issue['title']}: {issue.get('body', '')}"
    plan_output = run_claude(plan_prompt, adw_id, logger)
    make_issue_comment(issue_number, f"{adw_id}_planner: ✅ Implementation plan created", repo_path)

    # 5. Commit plan
    git_commit(f"planner: {issue_command.replace('/', '')}: add implementation plan for #{issue['number']}")
    logger.info("Plan committed")

    # 6. Implement
    logger.info("Implementing solution...")
    make_issue_comment(issue_number, f"{adw_id}_implementor: ✅ Implementing solution", repo_path)
    implement_prompt = f"Read the file .github/prompts/implement.prompt.md and follow its instructions. Find the latest plan in specs/ and implement it."
    implement_output = run_claude(implement_prompt, adw_id, logger)
    make_issue_comment(issue_number, f"{adw_id}_implementor: ✅ Solution implemented", repo_path)

    # 7. Commit implementation
    git_commit(f"implementor: {issue_command.replace('/', '')}: implement #{issue['number']} - {issue['title']}")
    logger.info("Implementation committed")

    # 8. Create PR
    logger.info("Creating pull request...")
    make_issue_comment(issue_number, f"{adw_id}_ops: ✅ Creating pull request", repo_path)
    pr_url = create_pull_request(branch_name, issue, adw_id)
    logger.info(f"Pull request created: {pr_url}")
    make_issue_comment(issue_number, f"{adw_id}_ops: ✅ Pull request created: {pr_url}", repo_path)

    logger.info(f"ADW workflow completed successfully for issue #{issue_number}")
    make_issue_comment(issue_number, f"{adw_id}_ops: ✅ ADW workflow completed successfully", repo_path)


if __name__ == "__main__":
    main()
