#!/usr/bin/env -S uv run
# /// script
# dependencies = ["fastapi", "uvicorn", "python-dotenv"]
# ///

"""
GitHub Webhook Trigger — tac_practise ADW

FastAPI webhook endpoint that receives GitHub issue events and triggers ADW workflows.
Responds immediately to meet GitHub's 10-second timeout by launching adw_plan_build.py
in the background.

Usage: uv run trigger_webhook.py

Endpoints:
  POST /gh-webhook  — Receives GitHub issue/comment events
  GET  /health      — Health check

Triggers on:
  - New issue opened
  - Comment with body "adw" on any issue
"""

import os
import subprocess
import uuid
from fastapi import FastAPI, Request
from dotenv import load_dotenv
import uvicorn

load_dotenv()

PORT = int(os.getenv("PORT", "8001"))
app = FastAPI(title="ADW Webhook Trigger", description="GitHub webhook endpoint for tac_practise ADW")


@app.post("/gh-webhook")
async def github_webhook(request: Request):
    """Handle GitHub webhook events."""
    event_type = request.headers.get("X-GitHub-Event", "")
    payload = await request.json()
    action = payload.get("action", "")
    issue = payload.get("issue", {})
    issue_number = issue.get("number")

    should_trigger = False
    trigger_reason = ""

    if event_type == "issues" and action == "opened" and issue_number:
        should_trigger = True
        trigger_reason = "New issue opened"
    elif event_type == "issue_comment" and action == "created" and issue_number:
        comment_body = payload.get("comment", {}).get("body", "").strip().lower()
        if comment_body == "adw":
            should_trigger = True
            trigger_reason = "Comment with 'adw' command"

    if should_trigger:
        adw_id = str(uuid.uuid4())[:8]
        script_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(script_dir)
        trigger_script = os.path.join(script_dir, "adw_plan_build.py")

        cmd = ["uv", "run", trigger_script, str(issue_number), adw_id]
        subprocess.Popen(cmd, cwd=project_root, env=os.environ.copy())

        return {
            "status": "accepted",
            "issue": issue_number,
            "adw_id": adw_id,
            "message": f"ADW workflow triggered for issue #{issue_number}",
            "reason": trigger_reason,
        }

    return {"status": "ignored", "reason": f"Not a triggering event (event={event_type}, action={action})"}


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy", "service": "adw-webhook-trigger"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=PORT)
