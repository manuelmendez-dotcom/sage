---
name: SAGE V3.0 production line
description: SAGE V3.0 is the active production prompt at prompts/sage_v3.0.md. Versioning was reset 2026-05-18 — prior V3.0/V3.1/V3.2 history collapsed; all internal version qualifiers stripped. V3.0 is the new baseline trunk.
metadata:
  type: project
---
**Active production:** `prompts/sage_v3.0.md`. Single live file, no parallel staging.

**Why the reset (2026-05-18):** Prior V3.0 → V3.1 → V3.2 → "production" → "staging" naming was unmanageable (multiple files in `Versions/production/` and `Versions/`, internal "retired in v3.2" qualifiers contradicting current rule statements). Manuel collapsed history to a single V3.0 trunk per agent in `prompts/`. Internal text was rewritten so every rule states what IS, not what changed. Git carries the pre-reset history.

**How to apply:**
- All bug fixes and feature work land directly in `prompts/sage_v3.0.md`.
- Bump version (V3.1, V3.2…) only on material change: refactor, render-shape change, math change, new mode. Cosmetic edits, typos, wording polish do NOT bump.
- Bump procedure: `cp prompts/sage_v3.0.md prompts/sage_v3.1.md` → edit new file → both coexist while new is in test → once rolled out, `git rm` the old file → update CLAUDE.md path.
- One trunk per agent in `prompts/`. Experiments go in a `.gitignore`'d sandbox dir, NOT alongside the trunk.
- Commit convention: `sage: <change>` for prompt edits, `repo: <change>` for everything else.
- Push to GitHub after every shipped edit (cloud copy = disaster recovery).

**V3.0 inherited architecture:**
- XML spec blocks: `<plan_detection_spec>`, `<mcp_reliability_spec>`, `<source_routing_spec>`, `<output_chaining_spec>`, `<language_policy_spec>`, `<industry_enrichment_spec>`, `<verification_loop>`, `<completeness_contract>`, `<output_contract>`.
- Configuration Guide mode with placeholder discipline, path column discipline, per-account variability line.
- Constraint #19 (no unverified packaging claims) — explicit announcement wording by source (transcript/note/email/direct statement).
- Constraint #21 (AI Product Truth) — single AI agent offering (Essential/Advanced split retired April–May 2026).
- Goals Analysis in customer language with worked example.
- Recommendations with dependency sequencing in "Why It Fits" column. No consulting-style items.
- Success Plan brevity: Goals 2–5 words, Outcomes 3–6 words, one-slide cap.
- Traffic-light Sources & Confidence block scoped to standalone Q&A + Config Guide + pause-signal-triggered Q&A.
- Transparency layer three tiers (A full block / B MCPs-reached line / C nothing).
- Follow-up handling splits meaning clarifications (no research) from factual clarifications (scoped Z2 search).
- Industry enrichment: four tiers (context → domain infer → ask → skip), stored in COMPANY_CONTEXT.
- Welcome MCP probe (4 parallel calls on greeting-only starts).
- Deliverables template-language rule (English headers/columns/examples are translation slots, not literals).
- QBR Express workbook wording in welcome.

**LibreChat settings (load-bearing):**
- Model: GPT-5.4 (direct OpenAI, not Bedrock)
- `reasoning_effort: medium`
- `verbosity: low`
- `useResponsesApi: off`

**Feedback loop with Manuel:**
- "This output is wrong" → paste what SAGE returned + the ask. Read `prompts/sage_v3.0.md`, diagnose which rule produced it, fix in place, explain edit.
- "New capability" → describe the need. Propose cleanest expression consistent with cookbook structure, apply after review.
- Manuel does not paste the prompt. Read it from the file path.

Related: [[project_datifyer_v3]], [[reference_prompt_layer_ceiling]], [[reference_gpt54_prompting_guidance]].
