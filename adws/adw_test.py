#!/usr/bin/env -S uv run
# /// script
# dependencies = ["python-dotenv", "pydantic"]
# ///

"""
ADW Test — tac_practise (standalone test phase)

Usage: uv run adw_test.py <github-issue-number> [adw-id]

Standalone validation/test phase that can run independently or be chained
after adw_plan_build.py. Implements the closed-loop feedback pattern:
Request → Validate → Resolve.

Workflow:
1. Load existing branch/state (or create test-only branch)
2. Run all validation commands (lint, build)
3. If failures → ask agent to resolve → rerun ALL validations
4. Loop until green or max retries exhausted
5. Commit results and report to GitHub issue

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

# Maximum number of test-fix-retest cycles
MAX_VALIDATION_RETRIES = 4

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def make_adw_id() -> str:
    """Generate a short 8-character UUID for ADW tracking."""
    return str(uuid.uuid4())[:8]


def setup_logger(adw_id: str) -> logging.Logger:
    """Set up logger that writes to both console and file."""
    log_dir = os.path.join(PROJECT_ROOT, "agents", adw_id)
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "test_execution.log")

    logger = logging.getLogger(f"adw_test_{adw_id}")
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
    logger.info(f"ADW Test Logger initialized - ID: {adw_id}")
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


def make_issue_comment(issue_number: str, comment: str, repo_path: str) -> None:
    """Post a comment on a GitHub issue."""
    cmd = ["gh", "issue", "comment", issue_number, "-R", repo_path, "--body", comment]
    subprocess.run(cmd, capture_output=True, text=True, env=get_github_env())


def run_claude(prompt: str, adw_id: str, logger: logging.Logger, text_only: bool = False) -> str:
    """Execute a prompt via Claude Code CLI and return output."""
    if text_only:
        cmd = [CLAUDE_PATH, "--print", "--model", "sonnet"]
    else:
        cmd = [CLAUDE_PATH, "-p", "-", "--model", "sonnet",
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


def run_validation(logger: logging.Logger) -> Tuple[bool, str]:
    """Run all validation commands and return (all_passed, output_summary).

    Runs each command from the validation stack. Returns combined output.
    """
    validation_commands = [
        ("Lint", "npm run lint"),
        ("Build (TypeScript + Vite)", "npm run build"),
    ]

    results = []
    all_passed = True

    for name, cmd in validation_commands:
        logger.info(f"Running validation: {name} → {cmd}")
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, cwd=PROJECT_ROOT
        )
        passed = result.returncode == 0
        output = result.stdout + result.stderr
        results.append(
            f"### {name}\n"
            f"- Command: `{cmd}`\n"
            f"- Status: {'✅ PASS' if passed else '❌ FAIL'}\n"
            f"- Output:\n```\n{output[:1000]}\n```"
        )
        if not passed:
            all_passed = False
            logger.warning(f"Validation FAILED: {name}")
            # Stop on first failure — no point running more if lint fails
            break
        else:
            logger.info(f"Validation PASSED: {name}")

    summary = "\n\n".join(results)
    return all_passed, summary


def resolve_failures(summary: str, adw_id: str, logger: logging.Logger) -> None:
    """Ask agent to fix validation failures using the resolve protocol."""
    resolve_prompt = (
        "Read the file specs/resolve-failed-test.md to understand the resolution protocol.\n"
        "Read the file specs/bug.md to understand the full validation stack.\n\n"
        "The following validation commands have failures. "
        "IMPORTANT: Fix every error, then rerun ALL validation commands to confirm zero errors.\n\n"
        f"Validation Results:\n{summary}\n\n"
        "IMPORTANT: Be surgical — fix only what's broken. Do not refactor unrelated code.\n"
        "After fixing, run `npm run lint` and `npm run build` to confirm everything passes."
    )
    run_claude(resolve_prompt, adw_id, logger)


def test_and_resolve(adw_id: str, logger: logging.Logger) -> Tuple[bool, str]:
    """Run the feedback loop: validate → resolve → revalidate until green.

    Returns (all_passed, final_summary).
    """
    final_summary = ""
    for attempt in range(1, MAX_VALIDATION_RETRIES + 1):
        logger.info(f"\n=== Validation attempt {attempt}/{MAX_VALIDATION_RETRIES} ===")
        all_passed, summary = run_validation(logger)
        final_summary = summary

        if all_passed:
            logger.info(f"All validations passed on attempt {attempt}")
            return True, summary

        if attempt >= MAX_VALIDATION_RETRIES:
            logger.error(f"Validation still failing after {MAX_VALIDATION_RETRIES} attempts")
            return False, summary

        # Resolve failures
        logger.info("Validation failures detected — asking agent to resolve...")
        resolve_failures(summary, adw_id, logger)

        # Commit any fixes
        git_commit(f"tester: resolve validation failures (attempt {attempt})")

    return False, final_summary


def main():
    """Main entry point — standalone test phase."""
    load_dotenv()

    if len(sys.argv) < 2:
        print("Usage: uv run adw_test.py <issue-number> [adw-id]")
        print("\nRuns validation feedback loop (lint, build) on the current branch.")
        print("Resolves failures automatically and retries until green or max attempts.")
        sys.exit(1)

    issue_number = sys.argv[1]
    adw_id = sys.argv[2] if len(sys.argv) > 2 else make_adw_id()
    logger = setup_logger(adw_id)

    if not os.getenv("ANTHROPIC_API_KEY"):
        logger.error("Missing ANTHROPIC_API_KEY")
        sys.exit(1)

    logger.info(f"ADW Test - ID: {adw_id}")
    logger.info(f"Running validation for issue #{issue_number}")

    # Optionally report to GitHub
    try:
        repo_path = get_repo_path()
        make_issue_comment(issue_number, f"{adw_id}_tester: ✅ Starting validation feedback loop", repo_path)
    except Exception:
        repo_path = None
        logger.warning("Could not connect to GitHub — running in local-only mode")

    # Run the feedback loop
    validation_passed, final_summary = test_and_resolve(adw_id, logger)

    # Commit final state
    git_commit(f"tester: validation complete for #{issue_number}")

    # Report results
    if repo_path:
        if validation_passed:
            make_issue_comment(
                issue_number,
                f"{adw_id}_tester: ✅ All validations passed\n\n{final_summary}",
                repo_path,
            )
        else:
            make_issue_comment(
                issue_number,
                f"{adw_id}_tester: ⚠️ Validation issues remain after {MAX_VALIDATION_RETRIES} attempts — manual review needed\n\n{final_summary}",
                repo_path,
            )

    status = "passed" if validation_passed else "FAILED"
    logger.info(f"ADW Test completed — validation {status} for issue #{issue_number}")
    sys.exit(0 if validation_passed else 1)


if __name__ == "__main__":
    main()
