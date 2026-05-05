---
name: SAGE V3 production line (V3.0 and V3.1)
description: V3 is the active production line. V3.0 rolled out 2026-04-24, superseded 2026-04-26 by V3.1. V3.1 adds Welcome MCP probe, Deliverables template-language rule, QBR Express wording. Versioning reset from here.
type: project
originSessionId: 83e0638a-a7c3-442c-8e9d-61490abf18e5
---
**Active production:** `Versions/production/sage_v3.1_main_production.md` (rolled out 2026-04-26) — NOT `sage_v3.1_main_prompt.md` (that file exists in `Versions/` root but is a staging/scratch variant; production edits land in `Versions/production/sage_v3.1_main_production.md`)
**Previous production (frozen reference):** `Versions/sage_v3.0_main_prompt.md` (active 2026-04-24 to 2026-04-26)

**Folder structure:** `Versions/production/` holds the two live files (`sage_v3.1_main_production.md` + `Datifyer_v3.1_production.md`). Everything else in `Versions/` is a frozen reference snapshot (V3.0 files, staging variants, old/).

**Why:** The V2 / openai_v1 / lean_test naming had become unmanageable. Manuel reset the versioning on 2026-04-26: V3.0 is the prompt that was in production as `sage_openai_v1_main_prompt.md`; V3.1 is the prompt that was in the `lean_test` sandbox, promoted to production after MCP-failure testing surfaced two prompt bugs (silent welcome, mixed-language Deliverables). All V2.x files and the V2.4 sonnetized line were deleted. Versioning restarts from V3.0 / V3.1 as the only live branches.

**How to apply:**
- All SAGE feature work and bug fixes land in V3.1 directly.
- Never edit V3.0 unless doing a deliberate rollback.
- New experiments that aren't ready for production should be new files (e.g., `sage_v3.2_experimental.md`). Add to `.gitignore` allowlist if they need tracking.
- Do NOT touch Datifyer's prompt from a SAGE work session without explicit approval, and vice versa.

**V3.0 architecture (inherited from sage_openai_v1 and V2.4 before that):**
- XML spec blocks: `<plan_detection_spec>`, `<mcp_reliability_spec>`, `<source_routing_spec>`, `<output_chaining_spec>`, `<language_policy_spec>`, `<industry_enrichment_spec>`, `<verification_loop>`, `<completeness_contract>`, `<output_contract>`.
- Configuration Guide mode with placeholder discipline, path column discipline, per-account variability line.
- Constraint #19 (no unverified packaging claims) with explicit announcement wording by source (transcript / note / email / direct statement).
- Constraint #21 (AI Product Truth) — Essential vs Advanced retiring April 27 – May 18, 2026.
- Goals Analysis in customer language with worked example.
- Recommendations with dependency sequencing in "Why It Fits" column. No consulting-style items.
- Success Plan brevity: Goals 2-5 words, Outcomes 3-6 words, one-slide cap.
- Traffic-light Sources & Confidence block scoped to standalone Q&A + Config Guide + pause-signal-triggered Q&A.
- Transparency layer three tiers (A full block / B MCPs-reached line / C nothing).
- Follow-up handling splits meaning clarifications (no research) from factual clarifications (scoped Z2 search).
- Industry enrichment: four tiers (context → domain infer → ask → skip), stored in COMPANY_CONTEXT.

**V3.1 additions on top of V3.0:**
1. **Welcome MCP probe.** Four parallel probe calls on greeting-only starts (Z2 `search_z2_articles` with "ticket", Drive `gdrive_search` with "playbook", Unleash `search` with "routing", Tavily `tavily_extract` on https://www.zendesk.com). Results discarded; only success vs. failure is classified. Status line renders 🟢/🟡/🔴 per MCP. Surfaces auth failures and connection issues at session start.
2. **Template-language rule in `# MODE: DELIVERABLES`.** Explicit instruction that every English header, column name, status value, and example in the templates is a translation slot, not a literal string. Fixes mixed-language Recommendations and Success Plan outputs under `verbosity: low`.
3. **QBR Express workbook wording.** Welcome message now says "QBR Express workbook (Google Sheet pre-loaded with Snowflake data via Coefficient)" instead of the generic canonical-QBR phrasing.

**LibreChat settings (load-bearing for V3.1):**
- Model: GPT-5.4 (direct OpenAI, not Bedrock)
- `reasoning_effort: medium`
- `verbosity: low`
- `useResponsesApi: off`

**Known open items from testing (2026-04-26):**
- **Silent fallback bug (not yet fixed in V3.1).** When Z2 returns auth-required (amber key) and the CSM does not authenticate, SAGE fell through to Unleash for a packaging question (Advanced AI on Suite Growth). `<mcp_reliability_spec>` line 376 forbids this. Needs a prompt tightening to make "required MCP failure = stop" non-negotiable regardless of which alternative source is available. Reproduce before drafting the fix.
- **Welcome message compression under `verbosity: low`.** V3.0 welcome dropped the "click the indicator to reconnect" action line and the "checking now takes a few seconds" motivator. V3.1 welcome probe replaces most of that paragraph, but verify the probe version renders completely.

**Feedback loop with Manuel:**
- "This output is wrong" — paste what SAGE returned + the ask. Read V3.1, diagnose which rule produced it, fix in V3.1, explain edit.
- "New capability" — describe the need. Propose cleanest expression consistent with cookbook structure, apply after review.
- Manuel does not paste the prompt. Read it from the file path.
