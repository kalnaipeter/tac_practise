#!/usr/bin/env -S uv run
# /// script
# dependencies = ["python-dotenv", "pydantic"]
# ///

"""
ADW Review — tac_practise (standalone review phase)

Usage: uv run adw_review.py <github-issue-number> <adw-id> [--skip-resolution]

Reviews implementation against the spec file, captures screenshots of critical
functionality, and optionally resolves blocker issues via patch plans.

Workflow:
1. Load existing branch/state from prior workflow
2. Find the spec file for the current branch
3. Run review against the spec (compare implementation to requirements)
4. If blocker issues found and --skip-resolution not set:
   - Create patch plan for each blocker
   - Implement resolution
   - Re-review
5. Commit review results and report to GitHub issue

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

# LLM backend: "claude" (default) or "gemini"
LLM_BACKEND = os.getenv("LLM_BACKEND", "claude").lower()
_gemini_env = os.getenv("GEMINI_CLI_PATH", "gemini")
GEMINI_PATH = shutil.which(_gemini_env) or _gemini_env
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

# Maximum number of review-resolve-rereview cycles
MAX_REVIEW_RETRIES = 3

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def make_adw_id() -> str:
    """Generate a short 8-character UUID for ADW tracking."""
    return str(uuid.uuid4())[:8]


def setup_logger(adw_id: str) -> logging.Logger:
    """Set up logger that writes to both console and file."""
    log_dir = os.path.join(PROJECT_ROOT, "agents", adw_id)
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "review_execution.log")

    logger = logging.getLogger(f"adw_review_{adw_id}")
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
    logger.info(f"ADW Review Logger initialized - ID: {adw_id}")
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


def get_current_branch() -> str:
    """Get the current git branch name."""
    result = subprocess.run(["git", "branch", "--show-current"], capture_output=True, text=True)
    return result.stdout.strip()


def build_screenshot_markdown(review_result: dict, repo_path: str, logger: logging.Logger) -> str:
    """Commit review screenshots, push, and return markdown image links using raw GitHub URLs."""
    screenshots = review_result.get("screenshots", [])
    if not screenshots:
        return ""

    # Collect valid screenshot files
    valid_files = []
    for path in screenshots:
        if os.path.isfile(path):
            valid_files.append(path)
        else:
            logger.warning(f"Screenshot not found: {path}")

    if not valid_files:
        return ""

    # Commit and push screenshots so they're accessible via raw URL
    git_commit("reviewer: add review screenshots")
    branch = get_current_branch()
    subprocess.run(["git", "push", "-u", "origin", branch], capture_output=True, text=True)

    # Build markdown image links using raw GitHub URLs
    parts = ["\n\n### Review Screenshots\n"]
    for path in valid_files:
        filename = os.path.basename(path)
        # Convert absolute path to repo-relative path
        rel_path = os.path.relpath(path, PROJECT_ROOT).replace("\\", "/")
        raw_url = f"https://raw.githubusercontent.com/{repo_path}/{branch}/{rel_path}"
        parts.append(f"![{filename}]({raw_url})")

    return "\n".join(parts)


def run_claude(prompt: str, adw_id: str, logger: logging.Logger, text_only: bool = False, model: str = "sonnet") -> str:
    """Execute a prompt via LLM CLI (Claude or Gemini) and return output."""
    if LLM_BACKEND == "gemini":
        if text_only:
            cmd = [GEMINI_PATH, "-p", prompt, "-m", GEMINI_MODEL, "--approval-mode", "plan", "-o", "text"]
        else:
            cmd = [GEMINI_PATH, "-p", prompt, "-m", GEMINI_MODEL, "--approval-mode", "yolo", "-o", "text"]
    else:
        if text_only:
            cmd = [CLAUDE_PATH, "--print", "--model", model]
        else:
            cmd = [CLAUDE_PATH, "-p", "-", "--model", model,
                   "--output-format", "text", "--dangerously-skip-permissions"]

    logger.debug(f"Running {LLM_BACKEND} ({'text-only' if text_only else 'agentic'}): {prompt[:200]}...")
    env = os.environ.copy()
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if api_key:
        env["ANTHROPIC_API_KEY"] = api_key
    stdin_input = prompt if LLM_BACKEND == "claude" else None
    result = subprocess.run(cmd, capture_output=True, text=True, env=env, input=stdin_input)
    if result.returncode != 0:
        error_msg = result.stderr or result.stdout or "Unknown error"
        logger.error(f"{LLM_BACKEND} error: {error_msg}")
        raise RuntimeError(f"{LLM_BACKEND} execution failed: {error_msg}")
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


def find_spec_file(state: dict, logger: logging.Logger) -> Optional[str]:
    """Find the spec file from state or by scanning the specs directory."""
    # Check state first
    plan_file = state.get("plan_file")
    if plan_file and os.path.exists(os.path.join(PROJECT_ROOT, plan_file)):
        logger.info(f"Found spec from state: {plan_file}")
        return plan_file

    # Fallback: find spec matching current branch
    branch_result = subprocess.run(
        ["git", "branch", "--show-current"], capture_output=True, text=True
    )
    branch = branch_result.stdout.strip()
    if branch:
        # Look for spec files that were added/modified in this branch
        diff_result = subprocess.run(
            ["git", "diff", "origin/main", "--name-only"], capture_output=True, text=True
        )
        for line in diff_result.stdout.strip().split("\n"):
            if line.startswith("specs/") and line.endswith(".md"):
                logger.info(f"Found spec from git diff: {line}")
                return line

    logger.warning("No spec file found")
    return None


def run_review(spec_file: str, adw_id: str, logger: logging.Logger) -> dict:
    """Run the review agent against a spec file. Returns parsed review result."""
    review_image_dir = os.path.join(PROJECT_ROOT, "agents", adw_id, "reviewer", "review_img")
    os.makedirs(review_image_dir, exist_ok=True)

    review_prompt = (
        f"Read the file .github/prompts/review.prompt.md and follow its instructions with these variables:\n"
        f"- adw_id: {adw_id}\n"
        f"- spec_file: {spec_file}\n"
        f"- agent_name: reviewer\n"
        f"- review_image_dir: {review_image_dir}\n\n"
        f"IMPORTANT: Return ONLY valid JSON as specified in the review.md Report section."
    )

    # Use opus for review (complex reasoning task)
    output = run_claude(review_prompt, adw_id, logger, model="opus")

    # Parse JSON from the output
    try:
        # Try to extract JSON from the output (may have markdown wrapping)
        json_start = output.find("{")
        json_end = output.rfind("}") + 1
        if json_start >= 0 and json_end > json_start:
            review_result = json.loads(output[json_start:json_end])
            return review_result
        else:
            logger.error(f"No JSON found in review output: {output[:500]}")
            return {"success": False, "review_summary": "Failed to parse review output", "review_issues": [], "screenshots": []}
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse review JSON: {e}\nOutput: {output[:500]}")
        return {"success": False, "review_summary": f"JSON parse error: {e}", "review_issues": [], "screenshots": []}


def resolve_blocker(issue: dict, spec_file: str, adw_id: str, logger: logging.Logger) -> bool:
    """Create and implement a patch for a blocker issue. Returns True if resolved."""
    review_change_request = f"{issue['issue_description']}\n\nSuggested resolution: {issue['issue_resolution']}"
    screenshot = issue.get("screenshot_path", "")

    patch_prompt = (
        f"Read the file .github/prompts/patch.prompt.md and follow its instructions with these variables:\n"
        f"- adw_id: {adw_id}\n"
        f"- review_change_request: {review_change_request}\n"
        f"- spec_path: {spec_file}\n"
        f"- agent_name: review_patch_agent\n"
        f"{'- issue_screenshots: ' + screenshot if screenshot else ''}\n\n"
        f"Create the patch plan, then implement it immediately.\n"
        f"After implementation, run `npm run lint` and `npm run build` to validate."
    )

    try:
        run_claude(patch_prompt, adw_id, logger)
        return True
    except RuntimeError as e:
        logger.error(f"Failed to resolve blocker: {e}")
        return False


def main():
    """Main entry point — standalone review phase."""
    load_dotenv()

    if len(sys.argv) < 3:
        print("Usage: uv run adw_review.py <issue-number> <adw-id> [--skip-resolution]")
        print("\nReviews implementation against the spec file.")
        print("Requires a prior ADW run (plan/build) so state exists.")
        sys.exit(1)

    issue_number = sys.argv[1]
    adw_id = sys.argv[2]
    skip_resolution = "--skip-resolution" in sys.argv

    logger = setup_logger(adw_id)

    if LLM_BACKEND == "claude" and not os.getenv("ANTHROPIC_API_KEY"):
        logger.error("Missing ANTHROPIC_API_KEY (required when LLM_BACKEND=claude)")
        sys.exit(1)

    logger.info(f"ADW Review - ID: {adw_id}")
    logger.info(f"Reviewing for issue #{issue_number}")

    # Connect to GitHub (optional)
    try:
        repo_path = get_repo_path()
        make_issue_comment(issue_number, f"{adw_id}_reviewer: ✅ Starting review phase", repo_path)
    except Exception:
        repo_path = None
        logger.warning("Could not connect to GitHub — running in local-only mode")

    # Load state from prior workflow
    state = load_state(adw_id, logger)

    # Find spec file
    spec_file = find_spec_file(state, logger)
    if not spec_file:
        logger.error("No spec file found — cannot review without a specification")
        if repo_path:
            make_issue_comment(issue_number, f"{adw_id}_reviewer: ❌ No spec file found for review", repo_path)
        sys.exit(1)

    logger.info(f"Reviewing against spec: {spec_file}")

    # Run review with retry loop for blocker resolution
    for attempt in range(1, MAX_REVIEW_RETRIES + 1):
        logger.info(f"\n=== Review attempt {attempt}/{MAX_REVIEW_RETRIES} ===")

        review_result = run_review(spec_file, adw_id, logger)
        logger.info(f"Review result: success={review_result.get('success')}")
        logger.info(f"Review summary: {review_result.get('review_summary', 'N/A')}")

        if review_result.get("success", False):
            # Review passed
            logger.info("Review passed — no blocker issues")
            git_commit(f"reviewer: review passed for #{issue_number}")

            if repo_path:
                summary = review_result.get("review_summary", "Implementation matches spec")
                screenshot_md = build_screenshot_markdown(review_result, repo_path, logger)
                make_issue_comment(
                    issue_number,
                    f"{adw_id}_reviewer: ✅ Review passed\n\n{summary}{screenshot_md}",
                    repo_path,
                )
            break

        # Review found issues
        blocker_issues = [
            i for i in review_result.get("review_issues", [])
            if i.get("issue_severity") == "blocker"
        ]

        if not blocker_issues or skip_resolution:
            # No blockers, or resolution skipped
            logger.info("Review complete — no blockers to resolve (or resolution skipped)")
            git_commit(f"reviewer: review complete for #{issue_number}")

            if repo_path:
                summary = review_result.get("review_summary", "Review complete")
                non_blocker_count = len(review_result.get("review_issues", [])) - len(blocker_issues)
                screenshot_md = build_screenshot_markdown(review_result, repo_path, logger)
                make_issue_comment(
                    issue_number,
                    f"{adw_id}_reviewer: ✅ Review complete\n\n{summary}\n\n"
                    f"Non-blocker issues found: {non_blocker_count}{screenshot_md}",
                    repo_path,
                )
            break

        # Resolve blockers
        logger.info(f"Found {len(blocker_issues)} blocker issues — attempting resolution")
        if repo_path:
            make_issue_comment(
                issue_number,
                f"{adw_id}_reviewer: 🔧 Resolving {len(blocker_issues)} blocker issues (attempt {attempt})",
                repo_path,
            )

        resolved = 0
        for blocker in blocker_issues:
            logger.info(f"Resolving: {blocker.get('issue_description', 'Unknown issue')}")
            if resolve_blocker(blocker, spec_file, adw_id, logger):
                resolved += 1

        git_commit(f"reviewer: resolve {resolved} blocker issues for #{issue_number} (attempt {attempt})")

        if attempt >= MAX_REVIEW_RETRIES:
            logger.error(f"Review still has blockers after {MAX_REVIEW_RETRIES} attempts")
            if repo_path:
                make_issue_comment(
                    issue_number,
                    f"{adw_id}_reviewer: ⚠️ Blockers remain after {MAX_REVIEW_RETRIES} resolution attempts — manual review needed",
                    repo_path,
                )
            sys.exit(1)

    logger.info(f"ADW Review completed for issue #{issue_number}")


if __name__ == "__main__":
    main()
