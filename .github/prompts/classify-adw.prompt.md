# Classify ADW Workflow

Extract ADW workflow information from the task description and determine the correct pipeline to run.

## Instructions

Analyze the text below and extract:
1. **ADW workflow command** — which pipeline to run
2. **Model set** — `base` (default, uses standard models) or `heavy` (uses more capable models for complex tasks)

### Valid ADW Commands

| Command | Pipeline | Use When |
|---------|----------|----------|
| `adw_sdlc_iso` | Plan → Build → Test → Review → Document | Standard feature/bug with human review |
| `adw_sdlc_ZTE_iso` | Plan → Build → Test → Review → Document → Ship | Zero-Touch: auto-merge if all passes |
| `adw_plan_build` | Plan → Build → PR | Quick iteration, no validation |
| `adw_plan_build_test` | Plan → Build → Test → PR | Standard with test loop |
| `adw_plan_build_review` | Plan → Build → Review | Build + spec verification |
| `adw_plan_build_test_review` | Plan → Build → Test → Review | Full validation |
| `adw_sdlc` | Plan → Build → Test → Review → Document | Full SDLC (non-isolated) |

### Model Set Selection

- Default is `base` — uses standard model (sonnet equivalent)
- If text contains `model_set heavy` → use `heavy` (opus equivalent for complex tasks)
- `heavy` is recommended for: complex features, tricky bugs, architectural changes

### CRITICAL Safety Rule

Do NOT select `adw_sdlc_ZTE_iso` unless `ZTE` is EXPLICITLY uppercased in the input.
If `zte` appears in lowercase, use `adw_sdlc_iso` instead. ZTE auto-merges to main — it must be an intentional choice.

### Response Format

Respond with a JSON object:
```json
{
  "adw_slash_command": "adw_sdlc_iso",
  "model_set": "base"
}
```

## Text to Analyze

$input
