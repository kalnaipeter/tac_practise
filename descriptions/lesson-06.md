# Lesson 06 — One Agent, One Prompt, One Purpose

## Core Concepts

- **Massive context windows lead to distracted, confused agents.** The solution: one agent, one prompt, one purpose. Give each agent a single, focused job and a prompt that contains only the context needed for that job.
- **Specialized agents with focused prompts** — Instead of cramming everything into one mega-prompt, break the SDLC into discrete phases (plan, build, test, review, document, patch) and assign each phase its own agent with its own prompt file.
- **Free up the context window** — By limiting each agent to a single purpose, the context window is fully available for the complex reasoning that purpose requires. No pollution from unrelated concerns.
- **Reproducible, improvable prompts** — Every agent's prompt is a committed file in the codebase. You can version control it, diff it, review it, and improve it independently. Each prompt can be evaluated and tuned on its own.
- **Each step of engineering requires different information, tools, and context** — A planner needs the issue + codebase structure. A reviewer needs the spec + the diff + a browser. A documenter needs the spec + screenshots + the changes. Honor this with dedicated agents.

## Key Takeaways

1. **Create dedicated agents for each workflow step.** Plan, build, test, review, document, and patch are all separate agents with separate prompts.
2. **Keep prompts focused on single purposes.** The `/review` command only knows how to review. The `/patch` command only knows how to patch. The `/document` command only knows how to document.
3. **Free up context windows for complex problems.** A review agent doesn't need build context. A documenter doesn't need test context.
4. **Commit and version control all agent prompts.** Every spec and command file is a versioned artifact. Changes to agent behavior are tracked in git.
5. **Evaluate and improve individual agent performance.** Because each prompt is isolated, you can improve the review prompt without touching the build prompt.
6. **ADW compositions chain single-purpose agents.** `adw_plan_build_review.py` chains plan → build → review. `adw_plan_build_document.py` chains plan → build → document. Mix and match phases.

## New ADW Phases Introduced

| Phase | ADW Script | Spec/Command | Purpose |
|-------|-----------|--------------|---------|
| **Review** | `adw_review.py` | `.github/prompts/review.prompt.md` | Review implementation against spec, take screenshots, identify issues by severity |
| **Patch** | `adw_patch.py` | `.github/prompts/patch.prompt.md` | Quick-fix a specific issue from a review change request |
| **Document** | `adw_document.py` | `.github/prompts/document.prompt.md` | Generate feature docs from git diff + spec + screenshots |

## New ADW Compositions

| Composition | Pipeline | When to Use |
|-------------|----------|-------------|
| `adw_plan_build_review.py` | Plan → Build → Review | Core workflow — build + verify against spec |
| `adw_plan_build_document.py` | Plan → Build → Document | When you want docs but skip tests/review |
| `adw_plan_build_test_review.py` | Plan → Build → Test → Review | Full validation — tests + spec review |
| `adw_sdlc.py` | Plan → Build → Test → Review → Document | Complete SDLC for production features |

## The Agent State Pattern

Each ADW run creates an `agents/{adw_id}/` directory containing:
- `adw_state.json` — Tracks `adw_id`, `issue_number`, `branch_name`, `plan_file`, `issue_class`
- Agent-specific folders (e.g., `sdlc_planner/`, `reviewer/`, `documenter/`) with prompts and outputs
- `review_img/` — Screenshots captured during review

State is passed between phases via `adw_state.json`, making phases composable and resumable.

## Conditional Docs Pattern

The `conditional_docs.md` file acts as a routing table for agent context. Instead of every agent reading every doc, agents check `.github/prompts/conditional-docs.prompt.md` and only read documentation relevant to their current task. This keeps context windows lean.

After every feature is documented, its entry is added to `conditional-docs.prompt.md` so future agents can find it when relevant.

## Review → Patch Cycle

When the review agent finds **blocker** issues:
1. It creates a patch plan for each blocker
2. A patch implementor agent resolves each issue
3. The review re-runs to verify the fix
4. This loops up to MAX_REVIEW_RETRY_ATTEMPTS times

Issue severity: `skippable` (non-blocking), `tech_debt` (non-blocking but should fix), `blocker` (must fix before release).

## Applied Changes

- Created **`.github/prompts/review.prompt.md`** — Review command spec that tells the agent how to review implementation against a specification, capture screenshots, and report issues with severity classification.
- Created **`.github/prompts/patch.prompt.md`** — Patch command spec for creating focused fix plans from review change requests. Supports `/chore`, `/bug`, `/feature` classification with minimal targeted changes.
- Created **`.github/prompts/document.prompt.md`** — Document command spec for generating feature documentation from git diff analysis, spec files, and screenshots. Updates `conditional-docs.prompt.md` after each feature.
- Created **`.github/prompts/conditional-docs.prompt.md`** — Routing table that tells agents which documentation to read based on what they're working on. Updated as new features are documented.
- Created **`adws/adw_review.py`** — Review phase ADW script that reviews implementation against spec, captures screenshots, and resolves blocker issues.
- Created **`adws/adw_patch.py`** — Patch phase ADW script for quick-fixing specific issues from review or issue comments.
- Created **`adws/adw_document.py`** — Document phase ADW script that generates feature documentation and updates conditional docs.
- Created **`adws/adw_plan_build_review.py`** — Composition: Plan → Build → Review pipeline.
- Created **`adws/adw_plan_build_document.py`** — Composition: Plan → Build → Document pipeline.
- Created **`adws/adw_plan_build_test_review.py`** — Composition: Plan → Build → Test → Review pipeline.
- Created **`adws/adw_sdlc.py`** — Full SDLC composition: Plan → Build → Test → Review → Document.
- Updated **`CLAUDE.md`** — Added new ADW workflows and compositions to the documentation.

## Relation to TAC Goal

This lesson is about **specialization at the agent level**. Instead of one agent doing everything, you build a team of focused agents — each with a single prompt, a single purpose. The ADW system becomes a pipeline of specialists: the planner plans, the builder builds, the reviewer reviews, the documenter documents. This is the "system that builds a system" — composable, improvable, and fully automated.
