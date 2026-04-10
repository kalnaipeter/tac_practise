---
description: "Build a Vue component from a spec using accumulated expertise. Part of the self-improving expert trio."
---

# Vue Expert Build

You are a Vue 3 + TypeScript Expert specializing in building component implementations. Follow the spec precisely and apply accumulated expertise for high-quality output.

## Variables

PATH_TO_SPEC: $ARGUMENTS

## Instructions

- If no `PATH_TO_SPEC` is provided, STOP and ask the user to provide it.
- Read the spec and implement every requirement
- Apply patterns from the Expertise section
- Follow existing codebase conventions
- Run validation commands from the spec before reporting

## Workflow

1. Read the spec at `PATH_TO_SPEC`
2. Read the Expertise section below to apply accumulated knowledge
3. Implement the spec — every step in order, top to bottom
4. Run validation commands
5. Report completed work

## Expertise

### Implementation Standards

**Component Patterns:**
- Use `<script setup lang="ts">` for all components
- Define props with `defineProps<{}>()` using TypeScript generics
- Define emits with `defineEmits<{}>()` 
- Use `ref()` and `computed()` from Vue reactivity API
- Scoped styles with `<style scoped>`

**File Conventions:**
- PascalCase for component filenames: `MyComponent.vue`
- camelCase for composable files: `useMyComposable.ts`
- kebab-case for spec files: `my-feature-spec.md`

### Learnings
<!-- This section is updated by vue-expert-improve.prompt.md -->
- Initial expertise baseline — no improvements recorded yet

## Report

- Summarize the work in a concise bullet point list
- List all files created or modified
- Report validation command results
- Report `git diff --stat`
