# SAGE Project — Claude Code Context

## What This Project Is
SAGE (Scaled AI Guide for Everything) is a LibreChat agent built for Zendesk's Scaled Customer Success team. It helps CSMs answer product questions, analyze call transcripts, build recommendations, and draft customer communications.

## Project Files
- `promptsmith.md` — Skill file for analyzing and writing LibreChat agent prompts
- `Infrastructure_ Librechat.pdf` — Visual guide showing LibreChat setup (screenshots, mostly images)
- `Current Sage Librechat Config.png` — Screenshot of the agent panel configuration
- `Versions/sage_v3.0_main_prompt.md` — Previous SAGE production prompt. Active 2026-04-24 to 2026-04-26. Superseded by V3.1.
- `Versions/sage_v3.1_main_prompt.md` — **Active production SAGE** (rolled out 2026-04-26). Adds Welcome MCP probe (4 parallel tool calls, pre-empts mid-session auth failures), template-language rule in Deliverables (forces translation of headers/columns/examples), QBR Express workbook wording. Builds on all V3.0 architecture.
- `Versions/Datifyer_v3.0.md` — Previous Datifyer production prompt. Active 2026-04-24 to 2026-04-26. Superseded by V3.1.
- `Versions/Datifyer_v3.1.md` — **Active production Datifyer** (rolled out 2026-04-26). Range-based ROI, plain-English discipline, two-zone UX, math-integrity spec. Built from 9+ iterations ending 2026-04-26.
- `Versions/old/Quill_v2.md` — Quill standalone email writing agent (separate from SAGE)
- `SAGE_Overview.md` — One-pager covering capabilities, guardrails, connections, value, use cases (for manager meetings)
- `SAGE_Presentation.excalidraw` — Visual presentation covering the same points
- `Tiered Inquiry Handling System for CSM AI Assistant - Sage.xlsx` — Use case matrix from team member
- `CHANGELOG.md` — CSM-facing changelog
- `AI_Rollout_Questionnaire_Responses.md` — AI rollout governance documentation

## Infrastructure
- **Platform:** LibreChat (self-hosted, accessed via VPN)
- **Model (current):** GPT 5.4 (via OpenAI API, direct connection)
- **Model (previous):** Claude Sonnet 4.6 (via AWS Bedrock, added latency due to extra routing layer)
- **Why the switch:** AWS Bedrock adds an intermediary between LibreChat and the model (authentication overhead, regional routing, default timeouts too short for large payloads). This caused latency on every step and NGHTTP2_INTERNAL_ERROR failures on complex queries. GPT 5.4 connects directly to OpenAI's API, removing that overhead. Same prompt, shorter path.
- **Thinking budget:** 2000 tokens (candidate for reduction to 1024 after testing)
- **Agent architecture:** SAGE is the main agent. Datifyer is a specialist agent for sheet analysis (handoff from SAGE). Quill is a standalone email writing agent CSMs use directly (not a SAGE handoff).

## MCP Architecture (4 MCPs)
| MCP | Tools | Role |
|-----|-------|------|
| Z2 Help Center (3 tools) | search_z2_articles, get_z2_articles_by_ids, fetch_z2_content_by_url | Primary source. Official Zendesk product docs. Always searched first. |
| Unleash (2 tools) | search, get_content | Internal knowledge only: Jira tickets, Slack threads, worklogs, config edge cases. NOT product docs. Called for troubleshooting, bugs, and complex configuration questions. |
| Google Drive (5 tools) | gdrive_search, gdrive_get_document, gdrive_get_presentation, gdrive_get_sheet, gdrive_get_sheet_names | Team knowledge: playbooks, decks, comparison charts. Stale content risk. Use sort_order: recently_modified. |
| Tavily (5 tools used) | tavily_search, tavily_extract, tavily_crawl, tavily_skill, tavily_research | Public web: Explore recipes, community, dev docs, marketplace. Default search_depth: fast. |

## Architecture Principles (carried into V3)
These are the load-bearing rules the V3 prompts implement. Kept as context for why the prompts look the way they do.

1. **Signal-based routing.** Z2 is always first. Other sources only called when the question type signals they're needed.
2. **SAGE drafts emails directly.** No Quill handoff. Quill is a separate standalone agent.
3. **Step budgeting.** Tool calls capped by query complexity to stay under the 25-step limit.
4. **Tavily optimized.** Default `search_depth: "fast"`. Use `include_domains`, not `site:` operators.
5. **Datifyer session ownership.** Once Datifyer produces output, Datifyer owns every subsequent turn until explicit exit.
6. **Email reply mirroring.** Communication Mode follows the customer's structure. No re-headlining or reframing.
7. **Best-practice research trigger.** "best practice," "mejores prácticas," "recommended way" force Z2 search before answering, even in Communication Mode follow-ups.
8. **No unverified packaging claims (Constraint #19).** SAGE cannot state "included on your plan" or "no plan change required" without confirming plan and availability.
9. **Configuration Guide mode.** Z2-grounded step-by-step setup guides. Per-account variability line for intent/field/group-based guides. No partial guides.
10. **MCP reliability layer.** Required vs optional MCPs per task type. Required fails = stop. Optional fails = flag and continue. `MCPs reached:` line in Sources & Confidence.
11. **Hardened plan detection.** Active extraction from context first. Announce extracted plans explicitly. Mandatory ask when plan is absent and matters.
12. **Language policy with sticky CSM override.** Customer-facing output always matches customer language (non-negotiable). Internal-facing defaults to customer language but respects `"give me this in English"` override.
13. **Goals Analysis customer-language framing.** Category headers reflect customer's situation, not Zendesk product taxonomy.
14. **Recommendations grounded in call.** No generic best practices. Dependency sequencing stated in "Why It Fits" column.
15. **Scoped workflow pause.** Pause signal fires only for unrelated topics, not clarifications about the active deliverable.
16. **AI Product Truth (Constraint #21).** Essential vs Advanced distinction retiring April 27 – May 18, 2026. Single AI agent offering going forward. Never recommend "upgrading to AI Advanced" as a separate purchase.
17. **Industry enrichment spec.** Four-tier approach (already in context → domain infer → ask → graceful skip). Stored in COMPANY_CONTEXT slot, reused across modes.

## V3.1 additions on top of V3.0
- **Welcome MCP probe.** Four parallel tool calls on greeting-only starts (Z2 search, Drive search, Unleash search, Tavily extract on zendesk.com). Surfaces auth failures and connection issues at session start, before real work is at stake.
- **Template-language rule.** Explicit instruction at top of Deliverables that every English header, column name, status value, and example in the templates is a translation slot, not a literal string. Fixes mixed-language Recommendations and Success Plan outputs.
- **Wording refinement.** "QBR Express workbook (Google Sheet pre-loaded with Snowflake data via Coefficient)" replaces the generic QBR workbook phrasing.

## Prompt Lines

### Active production (V3.1, rolled out 2026-04-26)
- SAGE: `Versions/sage_v3.1_main_prompt.md`
- Datifyer: `Versions/Datifyer_v3.1.md`
- Style: cookbook-aligned — XML spec blocks, compressed tool specs, length and reasoning delegated to API parameters, customer-ready default output quality.
- **Required LibreChat agent settings (both prompts assume them):**
  - Model: GPT-5.4 (direct OpenAI, not Bedrock)
  - `reasoning_effort: medium`
  - `verbosity: low`
  - `useResponsesApi: off`
- Feedback loop: user brings bad output or new need, file is edited directly.

### Previous production (V3.0, 2026-04-24 to 2026-04-26)
- SAGE: `Versions/sage_v3.0_main_prompt.md`
- Datifyer: `Versions/Datifyer_v3.0.md`
- Status: superseded by V3.1. Kept for reference and rollback if needed.

### When to edit which
- Bug or missing feature in production → edit the V3.1 files (`sage_v3.1_main_prompt.md` / `Datifyer_v3.1.md`) directly.
- Never edit V3.0 files unless rolling back. V3.0 is a frozen reference snapshot.
- New experiments that aren't production-ready yet should be created as new files (e.g., `sage_v3.2_experimental.md`) and added to `.gitignore`'s allowlist if they need to be tracked.

## What's Next
- Monitor V3.1 in production for real CSM feedback.
- Watch for the specific V3.1 changes in action: welcome MCP probe catching auth issues, Deliverables outputs staying in-language, no mixed-language headers.
- Continue monitoring GPT-5.4 for behavior drift (banned words, hedge language, verbosity, backstage leaking).

## How to Use promptsmith.md
The promptsmith skill is used to analyze and score LibreChat agent prompts. To invoke it, read the file and adopt its framework. It provides: classification, dimensional scoring (1-10), diagnosis by severity, and rewrite guidance. It has LibreChat-specific knowledge (capabilities, handoffs, artifacts, step limits).
