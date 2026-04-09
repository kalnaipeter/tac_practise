# Agentic Layer Audit

Audit recent work to determine whether time was spent on the agentic layer or the application layer, then recommend agentic improvements.

## Instructions

Read `CLAUDE.md` for project context, then read `ai_docs/agentic-layer-guide.md` for the 12 leverage points.

### Step 1 — Inventory Recent Changes

Run `git log --oneline -20` to see recent commits. For each commit, classify it:

- **Agentic layer** — Changes to prompts, ADWs, specs, ai_docs, CLAUDE.md, agent configs, plans, templates
- **Application layer** — Changes to src/, components, services, types, styles, index.html

### Step 2 — Calculate the Ratio

Count agentic vs application commits. Report:

```
## Agentic Layer Audit

### Recent Commits (last 20)
| Commit | Message | Layer |
|--------|---------|-------|
| ... | ... | agentic / application |

### Ratio
- Agentic: N/20 (X%)
- Application: N/20 (X%)
- Target: 50%+ agentic
- Status: ON TRACK / BELOW TARGET
```

### Step 3 — Recommend Improvements

THINK HARD about what agentic improvements would increase agent autonomy. Check each leverage point:

1. **Context** — Is `CLAUDE.md` comprehensive? Are ai_docs up to date?
2. **Prompt** — Are there prompt templates for common tasks? Any gaps?
3. **Plans** — Do specs have validation commands? Are plan formats consistent?
4. **Tests** — Is the test-fix loop working? Any untested paths?
5. **Templates** — Are there reusable templates for problem classes?
6. **ADWs** — Are pipelines covering the full SDLC? Any missing phases?

For each gap found, suggest a specific improvement with the file to create or modify.

### Step 4 — Report

```
### Recommended Agentic Improvements
1. [Leverage Point] — Description of improvement → file to create/modify
2. ...

### Next Action
The single highest-impact improvement to make right now.
```

## Relevant Files

- `CLAUDE.md` — Project context
- `ai_docs/agentic-layer-guide.md` — The 12 leverage points and architecture
- `.github/prompts/` — All prompt templates
- `adws/` — ADW scripts
- `specs/` — Plan files
