---
description: "Review recent changes and update any expert's accumulated learnings. The generalized self-improvement prompt."
---

# Expert Improve

Review recent changes and update an expert prompt's accumulated knowledge. This is the self-improvement loop: work gets done → learnings get captured → future work benefits.

## Variables

EXPERT_PATH: $ARGUMENTS (path to the expert prompt file to improve, e.g., `experts/vue-expert-plan.prompt.md`)

## Instructions

- Review all recent changes to identify patterns worth capturing
- Extract learnings from implementation experiences
- Update ONLY the `## Expertise` → `### Learnings` section of the target expert prompt
- Do NOT modify Workflow or Instructions sections — they remain stable
- Document discovered best practices concisely
- If no relevant learnings found, stop and report — don't add noise

## Workflow

1. **Read the Target Expert**
   - Read the expert prompt file at `.github/prompts/${EXPERT_PATH}`
   - Understand its domain, existing expertise, and current learnings

2. **Analyze Recent Changes**
   - Run `git diff` to examine uncommitted changes
   - Run `git diff --cached` for staged changes
   - Run `git log --oneline -10` to review recent commits
   - Focus on files within the expert's domain

3. **Determine Relevance**
   Evaluate if changes contain new expertise worth capturing:
   - New patterns or techniques discovered?
   - Better approaches found through implementation?
   - Edge cases or gotchas encountered?
   - Performance or quality improvements identified?
   
   IMPORTANT: **If no relevant learnings found → STOP HERE and report "No expertise updates needed"**

4. **Extract and Apply Learnings**
   If relevant changes found:
   - Identify concise, actionable learnings
   - Add them to the `### Learnings` section of the target expert prompt
   - Each learning should be a single bullet point — specific enough to apply, short enough to scan
   - Include context: what was tried, what worked, what to avoid

5. **Report**

## Report

1. **Changes Analyzed** — Files reviewed via git diff, relevance determination
2. **Learnings Extracted** — New patterns discovered (or "No relevant learnings found")
3. **Expert Updates Made** — What was added to `### Learnings` (or "No expertise updates needed")
