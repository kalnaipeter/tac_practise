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

Core pipeline: `adw_plan_build.py` → classify → branch → plan → implement → commit → PR

```bash
cd adws/
uv run adw_plan_build.py 123          # Process single issue
uv run trigger_webhook.py             # Real-time webhook server
uv run trigger_cron.py                # Poll every 20s
```

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
