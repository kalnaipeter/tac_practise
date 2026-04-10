# Lesson 9 — Agentic Prompt Engineering

## Core Concept

**"The prompt is THE fundamental unit of engineering."**

TAC-9 defines 7 progressive levels of agentic prompt formats — each level adds capabilities on top of the previous. A prompt isn't just a message; it's a reusable, composable engineering artifact with defined sections, control flow, and delegation patterns. Invest in your prompts to achieve asymmetric engineering.

## The 7 Levels of Agentic Prompt Formats

### Level 1: High Level Prompt

**Description:** A reusable, ad-hoc, static prompt. The simplest unit — a direct instruction with no dynamic parts.

**Purpose:** Quick, repeatable commands for common tasks that don't need variables or workflows.

**Sections:** Title, Description, Purpose

**Examples:**
- `.github/prompts/all-tools.prompt.md` — Lists all available tools in typescript function signature format. Pure static instruction.
- `.github/prompts/start.prompt.md` — Starts the dev server. A step-by-step checklist with no variables.

---

### Level 2: Workflow Prompt

**Description:** A sequential workflow prompt with structured input, work steps, and output.

**Purpose:** Turns a task into a repeatable process with defined phases, variables, and reporting. The workhorse level — most prompts live here.

**Sections:** Title, Description, Purpose, Workflow (step-by-step list — required), Instructions (guardrails, constraints), Variables (dynamic via `$1`/`$ARGUMENTS`, static with fixed values — very important), Metadata (YAML frontmatter: `allowed-tools`, `description`, `argument-hint`, `model`), Report (structured output format), Codebase Structure (context map — notes files without reading them)

**Key insight — Variables:** Dynamic variables (`$1`, `$2`, `$ARGUMENTS`) accept user input at runtime. Static variables have fixed values. Reference both via `{{variable_name}}` throughout the prompt. Dynamic variables come first, static variables second.

**Key insight — Codebase Structure:** This is a context map. It lists relevant files and directories so the agent knows where things are — but does NOT read them yet. Context is loaded during workflow execution, not upfront.

**Examples:**
- `.github/prompts/prime.prompt.md` — Primes codebase understanding. Workflow: read `CLAUDE.md` → list `src/` → scan specs → report summary. No variables needed.
- `.github/prompts/build.prompt.md` — Builds from a plan file. Variable: `PATH_TO_PLAN: $ARGUMENTS`. Workflow reads the plan and implements it. Reports with `git diff --stat`.
- `.github/prompts/quick-plan.prompt.md` — Creates an implementation plan from a user prompt. Saves to `specs/`. Variables: `USER_PROMPT: $ARGUMENTS`, `PLAN_OUTPUT_DIRECTORY: specs/`.

---

### Level 3: Control Flow Prompt

**Description:** A workflow prompt that runs conditions and/or loops.

**Purpose:** Handles dynamic execution paths — stops when prerequisites fail, loops over collections, branches on input state.

**Sections:** Same as Level 2 + control flow constructs within the Workflow (STOP conditions, loops, conditional defaults)

**Key patterns:**
- **STOP guards:** `"If no PATH_TO_PLAN is provided, STOP immediately and ask the user"` — prevents blind execution
- **Controlled defaults:** `"NUMBER_OF_IMAGES: $2 or 3 if not provided"` — dynamic variables with fallback values
- **Loops:** `<image-loop>` blocks that iterate over a collection, executing the same pattern per item
- **Prerequisite checks:** Verify tools/tokens exist before starting, abort cleanly if missing

**Examples:**
- `.github/prompts/create-image.prompt.md` — Generates images via an image generation API. STOP if tools are missing. STOP if no prompt provided. Loops `NUMBER_OF_IMAGES` times through `<image-loop>` block. Controlled default: 3 images if count not specified.
- `.github/prompts/edit-image.prompt.md` — Edits images via an image editing API. STOP if API not available. Loops through each edit instruction in a dropped file. Prerequisite checks before starting.
- `.github/prompts/build.prompt.md` — Also Level 3: STOP if no plan path provided, then executes the workflow.

---

### Level 4: Delegate Prompt

**Description:** A prompt that delegates work to other agents (primary or subagents).

**Purpose:** Parallelizes work across multiple agent instances. The prompt becomes an orchestrator, not an executor.

**Sections:** Same as previous + Variables with agent configuration (model, count, tools)

**Key patterns:**
- **Task tool:** Spawns subagents that run in parallel, each stateless with complete context
- **Embedded sub-prompts:** `<scrape_loop_prompt>` blocks define the exact prompt passed to each subagent
- **Background delegation:** Fire-and-forget agents that report to a file

**Examples:**
- `.github/prompts/parallel-subagents.prompt.md` — Generic parallel launcher. Variables: `PROMPT_REQUEST: $1`, `COUNT: $2`. Designs self-contained prompts per agent, launches all simultaneously via subagent/Task tool, collects results.
- `.github/prompts/load-ai-docs.prompt.md` — Scrapes documentation URLs into local markdown. Checks staleness (24h TTL), then delegates each URL to a subagent with the `scrape_loop_prompt`.
- `.github/prompts/background.prompt.md` — Fires a background agent instance. Configures model and embeds a report structure as a system prompt. This is a **system prompt** pattern — written once, used many times. The `<primary-agent-delegation>` block constructs the entire background agent setup.

---

### Level 5: Higher Order Prompt

**Description:** Accepts another prompt file as input. Provides consistent structure so the lower-level prompt can be swapped.

**Purpose:** Separation of concerns — the higher-order prompt defines HOW to execute, while the input prompt defines WHAT to execute. Like a higher-order function in programming.

**Sections:** Same as previous + Variables with a prompt file variable (required)

**Key pattern:** `PATH_TO_PLAN: $ARGUMENTS` — the entire behavior changes based on which file is passed in. The prompt's workflow is a stable execution engine; the plan/prompt file is the variable payload.

**Examples:**
- `.github/prompts/build.prompt.md` — Also Level 5: the workflow is always "read the plan, implement it, report." But the plan file changes every time. Same build engine, different blueprints.
- `.github/prompts/load-bundle.prompt.md` — Loads a JSONL context bundle from a previous agent session. The bundle path is the variable — different bundles produce entirely different context loads. Includes deduplication logic for optimizing file reads.

---

### Level 6: Template Metaprompt

**Description:** A prompt that creates new prompts in a specific dynamic format.

**Purpose:** Standardizes prompt creation itself. Instead of hand-crafting each prompt, you define a template and the metaprompt generates consistent, high-quality prompts from a high-level description.

**Sections:** Same as previous + Template (the specified output format — very important) + Documentation (reference docs for the codebase/platform)

**Key insight — Template section:** This is the heart of the metaprompt. It defines the exact markdown structure every generated prompt must follow — frontmatter, sections, variable conventions. The metaprompt replaces `<placeholder>` blocks with actual content.

**Examples:**
- `.github/prompts/metaprompt-workflow.prompt.md` — The generic metaprompt. Takes a high-level prompt description, reads project conventions and existing prompts for reference, then generates a complete prompt file in the Specified Format. Saves to `.github/prompts/<name>.prompt.md`.
- `.github/prompts/plan-vite-vue.prompt.md` — A domain-specific metaprompt for Vite + Vue 3 apps. Takes a prompt and generates a full implementation plan in a detailed Plan Format template. Includes Codebase Structure for context mapping, conditional sections based on complexity, and outputs only the plan file path.

---

### Level 7: Self-Improving Prompt

**Description:** A prompt that is updated by itself or another prompt/agent with new information.

**Purpose:** Accumulates expertise over time. The Expertise section grows as the agent encounters new patterns, making each execution smarter than the last.

**Sections:** Same as previous + Expertise (accumulated domain knowledge — architectural patterns, discovered practices, standards)

**Key insight:** The self-improving prompt works best as a system of prompts — a dedicated "improve" prompt analyzes recent work and updates only the Expertise section of the main prompt, keeping the Workflow stable. The expertise section is the living knowledge base; the workflow is the stable execution engine.

**Examples:**
- `.github/prompts/experts/vue-expert-plan.prompt.md` — Plans Vue component implementations. The Expertise section contains project-specific architectural knowledge: component patterns, file conventions, TypeScript typing approaches, composable patterns. This knowledge accumulates across multiple implementations.
- `.github/prompts/experts/vue-expert-improve.prompt.md` — The companion improver. Analyzes `git diff` and recent commits for Vue-related changes, extracts learnings, and updates ONLY the `### Learnings` subsections of the plan and build prompts. Reports "No expertise updates needed" if nothing changed. This is what makes Level 7 self-improving — a separate prompt dedicated to feeding knowledge back.
- The `experts/` folder pattern: `vue-expert-plan.prompt.md` (plan), `vue-expert-build.prompt.md` (build), `vue-expert-improve.prompt.md` (improve) — a trio where the improve prompt keeps the other two current.

## Agentic Prompt Sections Reference

Ordered by frequency of use:

| Section | Purpose | Required At |
|---------|---------|-------------|
| **Title** | Names the prompt, action-oriented | All levels |
| **Purpose** | High-level what and why | All levels |
| **Workflow** | Step-by-step execution (numbered list) | Level 2+ |
| **Variables** | Dynamic (`$1`) and static inputs | Level 2+ |
| **Instructions** | Guardrails, constraints, edge cases | Level 2+ (secondary) |
| **Metadata** | YAML frontmatter (tools, model, hints) | Level 2+ |
| **Report** | Structured output format | Level 2+ (secondary) |
| **Codebase Structure** | Context map of files (don't read yet) | Level 2+ (as needed) |
| **Relevant Files** | Specific files to read/modify | Level 2+ (as needed) |
| **Template** | Specified output format for generation | Level 6 |
| **Expertise** | Accumulated domain knowledge | Level 7 |
| **Examples** | Concrete usage scenarios | As needed |

## System Prompts vs User Prompts

The most important distinction is **scope and persistence**:

| Aspect | System Prompt | User Prompt |
|--------|--------------|-------------|
| Scope | Rules for ALL conversations | ONE specific task |
| Mutability | Fixed for the session | Refined with follow-ups |
| Failure impact | Everything breaks | One response fails |
| Frequency | Written once, used many times | Written fresh each time |
| Testing needed | High — affects everything | Low — fix on the fly |

**Best sections for system prompts:** Purpose (role/identity), Instructions (behavioral rules), Examples (response patterns)

**Avoid in system prompts:** Variables, Report, Expertise, Templates, Metadata, Codebase Structure — these are task-specific

**Example:** `.github/prompts/background.prompt.md` uses `<primary-agent-delegation>` to embed a system prompt into the background agent — defining report structure, progress tracking, and behavioral rules that apply to the entire background session. Written once in the delegate prompt, executed every time.

## Key Takeaways

1. **Levels are cumulative** — each level adds capabilities on top of the previous, not replacing them
2. **`build.prompt.md` spans 3 levels** — Level 2 (workflow), Level 3 (STOP guard), Level 5 (accepts plan file as input). Real prompts combine levels.
3. **Variables are the leverage point** — dynamic inputs (`$1`, `$ARGUMENTS`) make prompts reusable; static defaults prevent broken execution
4. **STOP guards prevent waste** — Control flow prompts that fail fast save tokens and avoid garbage output
5. **Delegate for parallelism** — Task tool spawns subagents for parallel work; background agents for fire-and-forget
6. **Template metaprompts scale prompt creation** — Instead of hand-crafting 20 prompts, create one metaprompt that generates them consistently
7. **Self-improving = plan + build + improve trio** — The improve prompt feeds learnings back into the expertise section; workflows stay stable
8. **System prompts are written once** — Invest testing time proportional to blast radius; system prompt mistakes affect everything
9. **Codebase Structure is a context map, not context** — List files to orient the agent, but don't read them upfront; load context during execution
