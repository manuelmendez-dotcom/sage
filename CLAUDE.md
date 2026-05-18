# SAGE Project — Claude Code Context

## What This Project Is
SAGE (Scaled AI Guide for Everything) is a LibreChat agent built for Zendesk's Scaled Customer Success team. It helps CSMs answer product questions, analyze call transcripts, build recommendations, and draft customer communications. Datifyer is its specialist sub-agent for sheet/PDF data analysis.

## Repo Layout

```
SAGE/
├── CLAUDE.md                  ← this file (project context)
├── prompts/                   ← live production prompts
│   ├── sage_v3.0.md           ← active SAGE prompt
│   └── datifyer_v3.0.md       ← active Datifyer prompt
├── reference/                 ← context + regression tests + tools
│   ├── SAGE_Overview.md       ← manager-facing one-pager
│   ├── CHANGELOG.md           ← CSM-facing changelog
│   ├── promptsmith.md         ← skill file for analyzing LibreChat prompts
│   ├── payper_*.md            ← regression test sessions (PAYPER customer)
│   ├── SAGE_v2.1_Changes.md   ← historical change notes
│   └── AI_Rollout_Questionnaire_Responses.md  ← rollout governance
├── memory/                    ← Claude Code auto-memory (cross-session context)
└── .gitignore
```

`prompts/` is the only directory whose contents drive live behavior. Everything in `reference/` is supporting context — read-only history, regression test inputs, the prompt analysis skill.

## Versioning baseline (reset 2026-05-18)

The prior V3.x history (V2.x → V3.0 → V3.1 → V3.2) is collapsed. Both live prompts are now **V3.0** as a fresh start. Internal version qualifiers ("retired in v3.2", "new in v3.2", "v3.1 anchors") have been stripped — every rule simply states what IS, not what changed. Prior history lives in git only.

Git log carries the full pre-reset commit history if archaeology is ever needed.

## Versioning workflow (forward)

1. **All edits land directly in `prompts/sage_v3.0.md` or `prompts/datifyer_v3.0.md`.** Treat the V3.0 file like a living trunk.
2. **Bump version on material change.** Refactors, render-shape changes, math changes, or new modes → increment to V3.1, V3.2, etc. Cosmetic edits, typo fixes, wording polish do NOT bump.
3. **Bump procedure:**
   - `cp prompts/sage_v3.0.md prompts/sage_v3.1.md` (or whatever bump)
   - Edit the new file. The old file stays in `prompts/` as the previous-known-good while the new one is in test.
   - Once the new file is rolled out in LibreChat, delete the old one (`git rm prompts/sage_v3.0.md`). Git history keeps the snapshot.
   - Update the file path reference in this CLAUDE.md.
4. **One trunk per agent at a time.** No parallel staging files in `prompts/`. If exploration is needed, branch in git or work in a sandbox dir under `.gitignore`.
5. **Commit message convention:** `sage: <change>` or `datifyer: <change>` for prompt edits. `repo: <change>` for everything else.
6. **Push to GitHub after every shipped edit.** `git push origin main`. The cloud copy is the disaster-recovery backup.

## Infrastructure
- **Platform:** LibreChat (self-hosted, accessed via VPN)
- **Model:** GPT-5.4 via direct OpenAI API (NOT AWS Bedrock — Bedrock added latency + NGHTTP2 errors on complex queries)
- **Required LibreChat agent settings (both prompts assume them):**
  - Model: GPT-5.4
  - `reasoning_effort: medium`
  - `verbosity: low`
  - `useResponsesApi: off`
- **Agent architecture:** SAGE = main agent. Datifyer = specialist (handoff from SAGE on sheet/PDF). Quill = standalone email writer (separate, not a SAGE handoff).

## MCP Architecture (4 MCPs)
| MCP | Tools | Role |
|-----|-------|------|
| Z2 Help Center (3) | search_z2_articles, get_z2_articles_by_ids, fetch_z2_content_by_url | Primary source — official Zendesk docs. Always searched first. |
| Unleash (2) | search, get_content | Internal-only: Jira, Slack, worklogs, config edge cases. NOT product docs. |
| Google Drive (5) | gdrive_search, gdrive_get_document, gdrive_get_presentation, gdrive_get_sheet, gdrive_get_sheet_names | Team knowledge: playbooks, decks. Stale-content risk → use `sort_order: recently_modified`. |
| Tavily (5 used) | tavily_search, tavily_extract, tavily_crawl, tavily_skill, tavily_research | Public web: Explore recipes, community, marketplace. Default `search_depth: fast`. |

## Architecture Principles (load-bearing)
These are the rules the prompts implement. Kept here as context for why prompts read the way they do.

1. **Signal-based routing.** Z2 always first. Other sources only when question type signals they're needed.
2. **SAGE drafts emails directly.** No Quill handoff.
3. **Step budgeting.** Tool calls capped by query complexity (25-step ceiling).
4. **Tavily optimized.** Default `search_depth: "fast"`. Use `include_domains`, not `site:`.
5. **Datifyer session ownership.** Once Datifyer renders, it owns subsequent turns until explicit exit.
6. **Email reply mirroring.** Communication Mode follows the customer's structure.
7. **Best-practice trigger.** "Best practice" / "mejores prácticas" forces Z2 search before answering.
8. **No unverified packaging claims.** SAGE cannot say "included on your plan" without confirming plan + availability.
9. **Configuration Guide mode.** Z2-grounded step-by-step setup with per-account variability line. No partial guides.
10. **MCP reliability layer.** Required vs optional MCPs per task type. Required fail = stop. Optional fail = flag + continue.
11. **Hardened plan detection.** Active extraction first; announce extracted plans; ask when plan is absent and matters.
12. **Language policy.** Customer-facing always matches customer language. Internal defaults to customer language with sticky English override.
13. **Goals Analysis customer-language framing.** Headers reflect customer's situation, not Zendesk taxonomy.
14. **Recommendations grounded in call.** No generic best practices. Dependency sequencing in "Why It Fits" column.
15. **Scoped workflow pause.** Pause fires only for unrelated topics, not active-deliverable clarifications.
16. **AI Product Truth.** Single AI agent offering (Essential/Advanced split retired April–May 2026).
17. **Industry enrichment.** Four-tier (in context → infer → ask → skip). Stored in COMPANY_CONTEXT, reused across modes.

## Datifyer engine notes (the why behind the rule density)

Datifyer carries dense rules because the math has been pressure-tested through multiple PAYPER regression runs. Headlines previously varied 3× on identical inputs (cost/ticket €27–€128, headline €11k–€228k). The locks that survived:

- **Two canonical inputs only.** Google Sheet QBR workbook (primary, full commercial fields) + Account Insights Hub Trended Metrics PDF (fallback, 24 months only). Excel/CSV/screenshot/other PDFs → SAGE redirects up front; never handed off.
- **Cost/ticket formula lock.** Named constants: `ANNUAL_WORKING_HOURS=1800`, `MONTHLY_WORKING_HOURS=150`. Verification rejects `COST_PER_TICKET > HOURLY_WAGE × 10`.
- **Currency-mismatch ask.** When CSM-typed symbol ≠ country-derived currency, gate asks before Layer 1.
- **Headline range ratio guard.** B/A must be in [2.9, 3.1] (15%/5% on same baseline = exactly 3.0). Hard reject if outside.
- **Median-based middle column ROLLED BACK.** Tried median for cross-source parity; the spec was unenforceable at prompt layer (model wrote window correctly, computed on different rows). Reverted to single-row latest-month value with outlier caveat in Read column when latest-month > 2× 11-month-rest median or < 0.5×.
- **Country hallucination ban (HARD).** PDF path NEVER infers country from subdomain or memory. Renders blank-country branch (asks salary + currency symbol).
- **Salary = CSM-typed only.** Tavily salary lookup retired entirely.
- **Growth rate = 12v12 rolling, closed-volume base.** Created-volume base inflated agents 30–50%.
- **3-pillar ROI render** (Deflection / Productivity / Capacity Question). No emoji anchors. No "Need different assumptions?" block. No bottom footer disclaimer (top italic legend covers directional caveat).
- **Snapshot 5 rows on Sheet path, 3 rows on PDF path** (Customer / Seats / Snapshot date).
- **Seat-verification nudge** on PDF path when active < 0.85 × activated, OR Agent Count changed by ≥2 in 12-month window.
- **Sub-1% rule.** Self-service / Zero-touch / One-touch / CSAT-response near zero render as `<1%`, never `0%`.
- **Money rounding = nearest-thousand half-up.**
- **Section 8 scoped ask.** "Ask me how I got these numbers" opens with a scoping question, not a methodology dump.

## Prompt-layer ceiling (the hard-won truth)

Some failure modes cannot be locked at the spec layer alone. The 24-run PAYPER debug pattern: if a rule needs constant tightening across runs and still drifts, the architecture is the problem, not the wording. **Drop the cell > tighten the spec.** FRT/TTC trend numerics, channel-mix ratios, and median-of-12 windows all hit this ceiling and were removed from the render rather than further specified.

## How to Use the promptsmith skill

`reference/promptsmith.md` is a skill file for analyzing and scoring LibreChat agent prompts. Read it and adopt its framework when asked to score/diagnose/rewrite a prompt. Provides classification, dimensional scoring (1-10), severity-ranked diagnosis, rewrite guidance. LibreChat-specific (capabilities, handoffs, artifacts, step limits).

## What's Next
- Iterate on V3.0 baseline. Bump version when material change ships.
- Watch for behavior drift on GPT-5.4 (banned words, hedge language, verbosity, backstage leak).
- Run regression checks against `reference/payper_*.md` sessions when touching Datifyer math.
