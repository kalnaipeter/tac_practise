---
applyTo: "**"
---

# tac_practise — Project Instructions

Read `CLAUDE.md` in the project root for full context on the tech stack, architecture, commands, types, and conventions.

## Quick Reference

- React 19 + TypeScript 5.9 + Vite 8
- Functional components only, strict TypeScript, no `any`
- Types in `src/types/`, services in `src/services/`, components in `src/components/`
- CSS co-located with components
- Specs for planned features live in `specs/`
- 3rd party docs for agent reference live in `ai_docs/`
- Lesson descriptions in `descriptions/`

## Before Building

1. Check `specs/` for an existing spec before implementing a feature
2. Check `ai_docs/` for reference docs on any 3rd party library
3. Run `npm run build` to verify no TypeScript errors after changes
4. Run `npm run lint` to verify no lint errors after changes
