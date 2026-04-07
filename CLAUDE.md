# tac_practise — Agent Context

> A simple React + TypeScript country information table, used as a practice ground for TAC (Tactical Agentic Coding) lessons.

## Tech Stack

- **Frontend:** React 19 + TypeScript 5.9 + Vite 8
- **Styling:** Plain CSS (no framework)
- **Linting:** ESLint 9 with typescript-eslint
- **Package Manager:** npm

## Commands

```bash
npm run dev       # Start dev server (http://localhost:5173)
npm run build     # Type-check then build for production
npm run lint      # Run ESLint across the project
npm run preview   # Preview the production build
```

## Architecture

```
src/
├── App.tsx                    # Root component — renders CountryTable
├── main.tsx                   # Entry point — mounts App into DOM
├── components/
│   ├── CountryTable.tsx       # Main table displaying country data
│   ├── CountryTable.css
│   ├── Actions.tsx            # Show/Edit/Delete action buttons per row
│   ├── Actions.css
│   ├── ThemeToggle.tsx        # Dark/light mode toggle button
│   └── ThemeToggle.css
├── services/
│   └── countryService.ts      # Data layer — returns hardcoded Country[]
├── types/
│   └── Country.ts             # Country interface (name, capital, population, area, continent, language, currency)
├── index.css                  # Global styles
└── App.css                    # App-level styles
```

## Key Types

- `Country` — core data type with: name, capital, population, area, continent, language, currency

## ADW — AI Developer Workflows

The `adws/` directory contains an out-of-loop agentic system (PETER Framework) that automates the full SDLC:

- **Prompt Input:** GitHub Issues (`/chore`, `/bug`, `/feature`)
- **Trigger:** Webhook (`trigger_webhook.py`) or Cron (`trigger_cron.py`)
- **Environment:** Feature branch per issue
- **Review:** Auto-created Pull Request

### Pipelines

| Pipeline | Phases | Use When |
|----------|--------|----------|
| `adw_plan_build.py` | Plan → Build → PR | Quick iteration, no validation |
| `adw_plan_build_test.py` | Plan → Build → Test → PR | Standard development with feedback loop |
| `adw_plan_build_review.py` | Plan → Build → Review | Build + spec verification (screenshots) |
| `adw_plan_build_document.py` | Plan → Build → Document | Build + auto-documentation |
| `adw_plan_build_test_review.py` | Plan → Build → Test → Review | Full validation + spec review |
| `adw_sdlc.py` | Plan → Build → Test → Review → Document | Complete SDLC for production features |

### Standalone Phases

| Phase | Script | Purpose |
|-------|--------|---------|
| Test | `adw_test.py` | Validate → resolve → revalidate (loop until green) |
| Review | `adw_review.py` | Review implementation against spec, capture screenshots |
| Patch | `adw_patch.py` | Quick-fix specific issue from 'adw_patch' keyword |
| Document | `adw_document.py` | Generate feature docs + update conditional_docs |

```bash
cd adws/
# Pipelines
uv run adw_plan_build.py 123          # Plan + Build only
uv run adw_plan_build_test.py 123     # Plan + Build + Test feedback loop
uv run adw_plan_build_review.py 123   # Plan + Build + Review against spec
uv run adw_plan_build_test_review.py 123  # Plan + Build + Test + Review
uv run adw_sdlc.py 123               # Full SDLC: Plan + Build + Test + Review + Document

# Standalone phases (require prior ADW state)
uv run adw_test.py 123                # Run validation only on current branch
uv run adw_test.py 123 abc12345       # Run validation with existing ADW ID
uv run adw_review.py 123 abc12345     # Review with existing ADW state
uv run adw_patch.py 123               # Quick-fix from 'adw_patch' keyword
uv run adw_document.py 123 abc12345   # Document with existing ADW state

# Triggers
uv run trigger_webhook.py             # Real-time webhook server
uv run trigger_cron.py                # Poll every 20s
```

## Feedback Loop — Validation Protocol

IMPORTANT: Every change must be validated. Follow the closed-loop cycle: **Request → Validate → Resolve**.

After any code change, run these commands in order:

1. `npm run lint` — If there are errors at all, resolve them
2. `npm run build` — If there are errors at all, resolve them

IMPORTANT: If you run into any errors at all, stop and resolve them immediately then rerun every validation step from step 1. Do not skip re-validation after a fix.

For bug fixes, read `.github/prompts/bug-validation.prompt.md` for the full validation protocol including root cause analysis format.
For defining what tests to run, read `.github/prompts/test.prompt.md` for the exact test execution sequence.
For resolving specific test failures, read `.github/prompts/resolve-failed-test.prompt.md` for the resolution protocol.
For reviewing implementation against a spec, read `.github/prompts/review.prompt.md` for the review protocol.
For quick-fixing a specific issue, read `.github/prompts/patch.prompt.md` for the patch plan format.
For generating feature documentation, read `.github/prompts/document.prompt.md` for the documentation format.
For context routing, read `.github/prompts/conditional-docs.prompt.md` to know which docs to read for your current task.

## Copilot-Only Workflow

For using all prompts and workflows without external LLM backends, see `ai_docs/copilot-workflow.md`.

Key prompt: `/flow <description>` runs the full pipeline (Plan → Build → Test → Fix → Review) in one shot.

IMPORTANT: When adding new prompts or changing workflows, update `ai_docs/copilot-workflow.md` to keep it current.

## Conventions

- Functional components only (no class components)
- One component per file, PascalCase filenames for components
- CSS files co-located with their component (ComponentName.css)
- Types live in `src/types/`, services in `src/services/`
- Strict TypeScript — no `any`, no unused locals/params
- Data flows: `services/` → `components/` via imports

## Project Context

This is a TAC course practice app. Each lesson adds agent-enabling infrastructure (prompts, specs, docs, context files) — not just features. The app's purpose is to be a realistic target for agentic coding workflows.

Lesson repos live in `../lessons/` (tac-1 through tac-11) as reference material for what each lesson teaches.

## Descriptions

Lesson notes and applied changes are documented in `descriptions/lesson-{NN}.md`.
