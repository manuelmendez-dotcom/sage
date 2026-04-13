# SAGE Project — Claude Code Context

## What This Project Is
SAGE (Scaled AI Guide for Everything) is a LibreChat agent built for Zendesk's Scaled Customer Success team. It helps CSMs answer product questions, analyze call transcripts, build recommendations, and draft customer communications.

## Project Files
- `sage_v2_main_prompt.md` — Previous SAGE production prompt (baseline)
- `Datifyer.md` — Previous Datifyer prompt (baseline)
- `promptsmith.md` — Skill file for analyzing and writing LibreChat agent prompts
- `SAGE_v2.1_Changes.md` — One-pager documenting what changed from v2.0 to v2.1
- `Infrastructure_ Librechat.pdf` — Visual guide showing LibreChat setup (screenshots, mostly images)
- `Original Sage prompt.pdf` — PDF export of the v2.0 prompt
- `Current Sage Librechat Config.png` — Screenshot of the agent panel configuration
- `Versions/sage_v2.1_main_prompt.md` — SAGE v2.1 prompt
- `Versions/sage_v2.1.1_main_prompt.md` — Current SAGE production prompt (v2.1.1, adds Unleash for config edge cases)
- `Versions/Datifyer_v2.md` — Current Datifyer production prompt (optimized)
- `Versions/Quill_v2.md` — Quill standalone email writing agent (was handoff from SAGE, now standalone)
- `SAGE_Overview.md` — One-pager covering capabilities, guardrails, connections, value, use cases (for manager meetings)
- `SAGE_Presentation.excalidraw` — Visual presentation covering the same points
- `Tiered Inquiry Handling System for CSM AI Assistant - Sage.xlsx` — Use case matrix from team member (validated against v2.1, 14/15 covered)

## Infrastructure
- **Platform:** LibreChat (self-hosted, accessed via VPN)
- **Model (current):** GPT 5.4 (via OpenAI API, direct connection)
- **Model (previous):** Claude Sonnet 4.6 (via AWS Bedrock, added latency due to extra routing layer)
- **Why the switch:** AWS Bedrock adds an intermediary between LibreChat and the model (authentication overhead, regional routing, default timeouts too short for large payloads). This caused latency on every step and NGHTTP2_INTERNAL_ERROR failures on complex queries. GPT 5.4 connects directly to OpenAI's API, removing that overhead. Same prompt, shorter path.
- **Thinking budget:** 2000 tokens (candidate for reduction to 1024 after testing)
- **Agent architecture:** SAGE is the main agent. Datifyer is a specialist agent for sheet analysis (handoff from SAGE). Quill is a standalone email writing agent (removed from SAGE handoff in v2.1, now offered as a separate agent CSMs can use directly).

## MCP Architecture (4 MCPs)
| MCP | Tools | Role |
|-----|-------|------|
| Z2 Help Center (3 tools) | search_z2_articles, get_z2_articles_by_ids, fetch_z2_content_by_url | Primary source. Official Zendesk product docs. Always searched first. |
| Unleash (2 tools) | search, get_content | Internal knowledge only: Jira tickets, Slack threads, worklogs, config edge cases. NOT product docs. Called for troubleshooting, bugs, and complex configuration questions (v2.1.1). |
| Google Drive (5 tools) | gdrive_search, gdrive_get_document, gdrive_get_presentation, gdrive_get_sheet, gdrive_get_sheet_names | Team knowledge: playbooks, decks, comparison charts. Stale content risk. Use sort_order: recently_modified. |
| Tavily (5 tools used) | tavily_search, tavily_extract, tavily_crawl, tavily_skill, tavily_research | Public web: Explore recipes, community, dev docs, marketplace. Default search_depth: fast. |
| Researcher (dropped in v2.1) | — | Was unused. Removed. |

## Key Architecture Decisions (v2.1 / v2.1.1)
1. **Signal-based routing replaced mandatory 3-source search.** Z2 is always first. Other sources only called when the question type signals they're needed.
2. **Quill handoff removed.** SAGE drafts emails directly. Saved 15-45 sec per email flow.
3. **Researcher MCP dropped.** Was listed in welcome message but had zero instructions.
4. **Step budgeting added.** Tool calls are capped by query complexity to avoid hitting the 25-step limit.
5. **Tavily optimized.** Default search_depth changed from "advanced" to "fast". Added tavily_skill and tavily_research. Use include_domains instead of site: operators.
6. **Datifyer routing scoped.** Bare number triggers ("1", "2", "3") deactivate once SAGE presents its own checkpoint.
7. **Model switched from Sonnet 4.6 (Bedrock) to GPT 5.4 (direct OpenAI).** Bedrock added latency on every step and caused NGHTTP2 errors on large payloads. Direct API removed the overhead.
8. **Unleash expanded to config edge cases (v2.1.1).** Now also called for complex configuration questions (routing, permissions, automation interactions), not just bugs.

## What's Next
- Monitor accuracy on GPT 5.4 for 1-2 weeks (watch for: banned words, hedge language, verbosity, backstage leaking)
- Experiment with reducing thinking budget (2000 → 1024)
- Model config tuning (temperature, top_p)
- Consider splitting SAGE into router + specialists if further speed needed

## How to Use promptsmith.md
The promptsmith skill is used to analyze and score LibreChat agent prompts. To invoke it, read the file and adopt its framework. It provides: classification, dimensional scoring (1-10), diagnosis by severity, and rewrite guidance. It has LibreChat-specific knowledge (capabilities, handoffs, artifacts, step limits).
