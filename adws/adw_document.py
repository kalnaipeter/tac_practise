#!/usr/bin/env -S uv run
# /// script
# dependencies = ["python-dotenv", "pydantic"]
# ///

"""
ADW Document — tac_practise (standalone documentation phase)

Usage: uv run adw_document.py <github-issue-number> <adw-id>

Generates feature documentation from git diff analysis, spec files, and
review screenshots. Updates conditional_docs.md so future agents can find
relevant documentation.

Workflow:
1. Load existing state (requires prior plan/build workflow)
2. Find spec file and review screenshots
3. Generate feature documentation in app_docs/
4. Update .github/prompts/conditional-docs.prompt.md
5. Commit documentation

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
from typing import Optional
import re
import time
import urllib.request
import urllib.error
from dotenv import load_dotenv

# Load environment variables — check both adws/ and project root
load_dotenv()
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env"))

_claude_env = os.getenv("CLAUDE_CODE_PATH", "claude")
CLAUDE_PATH = shutil.which(_claude_env) or _claude_env

# LLM backend: "claude" (default) or "gemini"
LLM_BACKEND = os.getenv("LLM_BACKEND", "claude").lower()
_gemini_env = os.getenv("GEMINI_CLI_PATH", "gemini")
GEMINI_PATH = shutil.which(_gemini_env) or _gemini_env
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def make_adw_id() -> str:
    """Generate a short 8-character UUID for ADW tracking."""
    return str(uuid.uuid4())[:8]


def setup_logger(adw_id: str) -> logging.Logger:
    """Set up logger that writes to both console and file."""
    log_dir = os.path.join(PROJECT_ROOT, "agents", adw_id)
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "document_execution.log")

    logger = logging.getLogger(f"adw_document_{adw_id}")
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
    logger.info(f"ADW Document Logger initialized - ID: {adw_id}")
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


def _parse_retry_delay(error_text: str) -> int:
    """Extract retry delay from Gemini rate-limit error, or return default 65s."""
    match = re.search(r'retry in (\d+)', error_text)
    return int(match.group(1)) + 5 if match else 65


def _gemini_api_call(prompt: str, logger: logging.Logger) -> str:
    """Call Gemini REST API directly (1 request per call, no CLI overhead)."""
    api_key = os.getenv("GEMINI_API_KEY", "").strip('"')
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY not set")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?key={api_key}"
    body = json.dumps({"contents": [{"parts": [{"text": prompt}]}]}).encode()
    max_retries = 3
    for attempt in range(1, max_retries + 1):
        req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"})
        try:
            resp = urllib.request.urlopen(req, timeout=120)
            data = json.loads(resp.read())
            return data["candidates"][0]["content"]["parts"][0]["text"].strip()
        except urllib.error.HTTPError as e:
            err_body = e.read().decode()
            if e.code == 429 and attempt < max_retries:
                delay = _parse_retry_delay(err_body)
                logger.warning(f"Gemini API rate limit (attempt {attempt}/{max_retries}). Waiting {delay}s...")
                time.sleep(delay)
                continue
            err_msg = json.loads(err_body).get("error", {}).get("message", err_body[:200])
            raise RuntimeError(f"Gemini API error {e.code}: {err_msg}")
    raise RuntimeError(f"Gemini API failed after {max_retries} retries")


def run_claude(prompt: str, adw_id: str, logger: logging.Logger, text_only: bool = False, model: str = "sonnet") -> str:
    """Execute a prompt via LLM CLI (Claude or Gemini) and return output."""
    # For Gemini text-only: use direct API (1 req vs ~5+ via CLI)
    if LLM_BACKEND == "gemini" and text_only:
        logger.debug(f"Running Gemini API direct (text-only): {prompt[:200]}...")
        return _gemini_api_call(prompt, logger)

    if LLM_BACKEND == "gemini":
        cmd = [GEMINI_PATH, "-p", " ", "-m", GEMINI_MODEL, "--approval-mode", "yolo", "-o", "text"]
    else:
        if text_only:
            cmd = [CLAUDE_PATH, "--print", "--model", model]
        else:
            cmd = [CLAUDE_PATH, "-p", "-", "--model", model,
                   "--output-format", "text", "--dangerously-skip-permissions"]

    max_retries = 3
    for attempt in range(1, max_retries + 1):
        logger.debug(f"Running {LLM_BACKEND} attempt {attempt}/{max_retries} ({'text-only' if text_only else 'agentic'}): {prompt[:200]}...")
        env = os.environ.copy()
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if api_key:
            env["ANTHROPIC_API_KEY"] = api_key
        result = subprocess.run(cmd, capture_output=True, text=True, env=env, input=prompt)
        combined_output = (result.stderr or "") + (result.stdout or "")
        if result.returncode != 0:
            if result.stdout and result.stdout.strip():
                logger.warning(f"{LLM_BACKEND} exited with code {result.returncode} but produced output — continuing")
                return result.stdout.strip()
            if "quota" in combined_output.lower() or "429" in combined_output or "rate" in combined_output.lower():
                if attempt < max_retries:
                    delay = _parse_retry_delay(combined_output)
                    logger.warning(f"Rate limit hit (attempt {attempt}/{max_retries}). Waiting {delay}s before retry...")
                    time.sleep(delay)
                    continue
                else:
                    logger.error(f"Rate limit still exceeded after {max_retries} attempts")
            error_msg = result.stderr or result.stdout or "Unknown error"
            logger.error(f"{LLM_BACKEND} error: {error_msg}")
            raise RuntimeError(f"{LLM_BACKEND} execution failed: {error_msg}")
        return result.stdout.strip()
    raise RuntimeError(f"{LLM_BACKEND} failed after {max_retries} retries")


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


def check_for_changes(logger: logging.Logger) -> bool:
    """Check if there are any changes between current branch and origin/main."""
    result = subprocess.run(
        ["git", "diff", "origin/main", "--stat"],
        capture_output=True, text=True
    )
    has_changes = bool(result.stdout.strip())
    if not has_changes:
        logger.info("No changes detected between current branch and origin/main")
    return has_changes


def main():
    """Main entry point — standalone documentation phase."""
    load_dotenv()

    if len(sys.argv) < 3:
        print("Usage: uv run adw_document.py <issue-number> <adw-id>")
        print("\nGenerates feature documentation from implementation.")
        print("Requires a prior ADW run (plan/build) so state exists.")
        sys.exit(1)

    issue_number = sys.argv[1]
    adw_id = sys.argv[2]

    logger = setup_logger(adw_id)

    if LLM_BACKEND == "claude" and not os.getenv("ANTHROPIC_API_KEY"):
        logger.error("Missing ANTHROPIC_API_KEY (required when LLM_BACKEND=claude)")
        sys.exit(1)

    logger.info(f"ADW Document - ID: {adw_id}")
    logger.info(f"Documenting for issue #{issue_number}")

    # Connect to GitHub (optional)
    try:
        repo_path = get_repo_path()
        make_issue_comment(issue_number, f"{adw_id}_documenter: ✅ Starting documentation phase", repo_path)
    except Exception:
        repo_path = None
        logger.warning("Could not connect to GitHub — running in local-only mode")

    # Load state
    state = load_state(adw_id, logger)
    if not state.get("branch_name"):
        logger.error("No branch name in state — run adw_plan.py first")
        sys.exit(1)

    # Check for changes
    if not check_for_changes(logger):
        logger.info("No changes to document — skipping")
        if repo_path:
            make_issue_comment(
                issue_number,
                f"{adw_id}_documenter: ℹ️ No changes detected — skipping documentation",
                repo_path,
            )
        sys.exit(0)

    # Find spec file
    spec_path = state.get("plan_file", "")

    # Find screenshots from review
    screenshots_dir = ""
    review_img_dir = os.path.join(PROJECT_ROOT, "agents", adw_id, "reviewer", "review_img")
    if os.path.exists(review_img_dir) and os.listdir(review_img_dir):
        screenshots_dir = review_img_dir
        logger.info(f"Found screenshots in: {screenshots_dir}")

    # Create app_docs directory
    app_docs_dir = os.path.join(PROJECT_ROOT, "app_docs")
    os.makedirs(app_docs_dir, exist_ok=True)

    # Run documentation generation
    doc_prompt = (
        f"Read the file .github/prompts/document.prompt.md and follow its instructions with these variables:\n"
        f"- adw_id: {adw_id}\n"
        f"- spec_path: {spec_path}\n"
        f"- documentation_screenshots_dir: {screenshots_dir}\n\n"
        f"IMPORTANT: Follow every step in the instructions including updating conditional_docs.md.\n"
        f"Return the path to the documentation file created."
    )

    try:
        output = run_claude(doc_prompt, adw_id, logger)
        logger.info(f"Documentation generated: {output}")

        git_commit(f"documenter: add documentation for #{issue_number}")

        if repo_path:
            make_issue_comment(
                issue_number,
                f"{adw_id}_documenter: ✅ Documentation generated: {output}",
                repo_path,
            )
    except RuntimeError as e:
        logger.error(f"Documentation failed: {e}")
        if repo_path:
            make_issue_comment(
                issue_number,
                f"{adw_id}_documenter: ❌ Documentation failed: {e}",
                repo_path,
            )
        sys.exit(1)

    logger.info(f"ADW Document completed for issue #{issue_number}")


if __name__ == "__main__":
    main()
