# SAGE Project — Claude Code Context

## What This Project Is
SAGE (Scaled AI Guide for Everything) is a LibreChat agent built for Zendesk's Scaled Customer Success team. It helps CSMs answer product questions, analyze call transcripts, build recommendations, and draft customer communications.

## Project Files
- `promptsmith.md` — Skill file for analyzing and writing LibreChat agent prompts
- `Infrastructure_ Librechat.pdf` — Visual guide showing LibreChat setup (screenshots, mostly images)
- `Current Sage Librechat Config.png` — Screenshot of the agent panel configuration
- `Versions/sage_v3.0_main_prompt.md` — Previous SAGE production prompt. Active 2026-04-24 to 2026-04-26. Superseded by V3.1.
- `Versions/production/sage_v3.1_main_production.md` — **Active production SAGE** (rolled out 2026-04-26). Adds Welcome MCP probe (4 parallel tool calls, pre-empts mid-session auth failures), template-language rule in Deliverables (forces translation of headers/columns/examples), QBR Express workbook wording. Builds on all V3.0 architecture.
- `Versions/Datifyer_v3.0.md` — Previous Datifyer production prompt. Active 2026-04-24 to 2026-04-26. Superseded by V3.1.
- `Versions/production/Datifyer_v3.1_production.md` — **Active production Datifyer** (rolled out 2026-05-05). Dual-source (Sheet QBR + AIH PDF), determinism-passed. Currency-conflict ask, headline ratio check (B/A ≈ 3.0), cost/ticket formula lock, PDF-path Snapshot 3-row + seat nudge + country-hallucination ban, menu header retired, Rule 4 outlier caveat on latest-month middle column. Mirrors SAGE naming convention (`_production` = active file).
- `Versions/Datifyer_v3.1.md` — Previous V3.1 staging file (rolled out 2026-04-26, superseded 2026-05-05 by `_production`). Kept for reference only — do NOT edit. Production edits land in `_production.md`.
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

## Datifyer V3.1 determinism pass (2026-05-05 ship-candidate, in `Datifyer_v3.1_production.md`)
Ran 24 PAYPER iterations chasing reproducibility bugs. Prior Datifyer V3.1 produced headline variance up to 3× on identical data (cost/ticket €27-€128, headline €11k-€228k across runs). Ship-candidate locks numbers with targeted extraction scope + CSM-provided salary gate + simplified Numbers table architecture. Reached pixel-identical output across final two runs.

Changes landing in ship-candidate:
- **Scoped extraction set.** Metrics tab: columns A-L only. Account Details: 10 canonical fields (PRODUCT_OFFERINGS_LIST replaces CORE_BASE_PLAN for fuller plan rendering). Benchmarks skipped by default. Product-adoption fields retired.
- **CSAT-blank rule.** Blank CSAT_SCORE = "Not enabled"; never render 100% from blank.
- **Scientific-notation normalization.** Parses `2.29E-01` → 0.229 → 22.9% before percentage conversion.
- **Snapshot table (5 rows).** Customer, Industry, Plans active, Seats (X of Y in use), Snapshot date. No source/coverage/extraction caption line below.
- **Numbers section restructured.** One-line volume callout above table ("Ticket demand averaged 972/month over the last 12 months, up 34% year over year"). Table = 3 columns (Area, Apr 2026, Read), no Trend column. Read column MUST be factually directional or factually state-describing — no spin, no hedging. Ticket volume row DROPPED from table (single-render in callout only) — prior runs drifted 852-922 on identical data.
- **Industry enrichment killed entirely.** No website asks, no Tavily subdomain lookups. Source-only (CRM_INDUSTRY / CRM_SUB_INDUSTRY). If absent → "N/A" in Snapshot.
- **ROI confirmation gate.** CSM types loaded salary with regional hint band (EMEA €25-40k / AMER $40-70k / APAC $20-35k / LATAM $12-25k) based on CRM_TERRITORY_COUNTRY. Bare salary (no `go` required) runs ROI directly. Seats, baseline, growth rate, deflection scenarios shown as already-locked. Single gate turn, no duplicate re-render.
- **Salary = CSM-typed only.** Tavily salary lookup retired entirely. No canonical fallback substitution. Loaded = what CSM typed (no × 1.3). Hourly = salary / 1,800.
- **Growth rate = 12v12 rolling, closed-volume base.** ADDITIONAL_MONTHLY_TICKETS = AVG_MONTHLY_CLOSED × GROWTH_RATE (NOT created — created inflated ADDITIONAL_AGENTS_NEEDED by 30-50%).
- **💰 block redesigned.** Two numbered bullets: "Save money on today's volume — €A/year (low end) to €B/year (high end)" with explicit 5%/15% scenario labels; "Avoid hiring as volume grows — up to €C/year" with concrete "X more agents" anchor. Plain-English discipline — banned: efficiency opportunity, capacity, absorb, leverage, optimize.
- **Closed-vs-created rationale inline in 💰 bullet + gate.** Single explanation at each render point; no separate "Created vs Closed" paragraph in 📊.
- **📊 block shortened.** 6-row reference card, no "Why this value" column, no scenario-band re-explanation.
- **Footer = disclaimer only.** No "Based on AVG_MONTHLY_CLOSED=... source, salary, seats, scenarios" reconstruction.
- **Menu after ROI simplified.** 2 options: "Ask me how I got these numbers" / "Done — hand back to SAGE." Adjust option dropped (redundant with 🔄 block examples).

Follow-up UX edits (2026-05-05 second pass, same ship-candidate file):
- **"Menu" header retired from output.** Numbered options self-announce. Internal rules still call the block a "menu"; the word just doesn't render. Applies to all stages (A-E) and to email/ROI/Q&A render sequences.
- **Numbers-table third-column header = `12-month read`** (was `Read`). Disambiguates that the interpretation is last-12 vs prior-12, not a single-month snapshot. Window cue is load-bearing for CSM.
- **Post-ROI clarifying turns = plain prose** (new Rule 4f in `<verification_loop>`). Any follow-up Q that isn't a menu pick, 🔄 override, or exit answers in 1-8 sentences without the Snapshot/Story/Numbers/Probes template and without "Not in source — skipping" placeholder rows. Bug the rule targets: model replied to "are you calculating ROI on 12v12?" with a full 5-section re-render.
- **Section 8 scoped ask.** "Ask me how I got these numbers" now opens with a short scoping question (cost per ticket / growth rate / deflection / hiring avoidance / source-vs-CSM provenance) instead of dumping the full methodology. CSM picks one number or types a free-form Q; scoped answer follows. Prevents the one-shot wall.

Third pass — **source surface reduced to 2 canonical inputs** (2026-05-05):
- **Accepted inputs: Google Sheet workbook (primary) + Account Insights Hub: Trended Metrics View PDF (fallback only).** Excel, CSV, screenshot, pasted table, 6-month "Ticket Volume & Performance Metrics" PDF all retired from spec. SAGE-side two-stage CSV flow deprecated for Datifyer purposes — Datifyer simply rejects and redirects.
- **AIH PDF extraction map added to `<input_handling_spec>`.** Full section-by-section label → schema mapping for the 24-month AIH PDF: Created/Solved volumes, FRT/TTC, Zero/One-Touch, Self-Service, CSAT (incl. Response Rate + Responses), Channel Mix + YoY, Agent Count + Activated/Remaining seats, Agent Productivity. Month-value tables are authoritative (not chart images).
- **Extraction-confidence tiers collapsed.** Low tier retired (only Screenshot/CSV paths used it, those paths are gone). Now: High (Sheet) or Medium (PDF). Internal only — no longer rendered anywhere.
- **Growth-rate shorter-window fallbacks removed.** Both accepted sources always provide 24 months → 12v12 is always available; 6v6 retired. If source returns <24 months, stop and tell CSM, don't silently shorten.
- **Baseline assumptions-line phrasing simplified.** Only valid form now: *"(12-month baseline, 24-month source)"*. "6-month baseline, full available" wording retired.

Fourth pass — **PDF notify-fill killed, seat-verification nudge added** (2026-05-05):
- **No more notify-fill ask on PDF path.** Datifyer proceeds directly to Sections 1-5 after extracting the PDF. Missing commercial fields (Industry, Country, Plans) are OMITTED from Snapshot entirely — not rendered as "N/A" rows, not rendered at all.
- **Snapshot PDF path = 3 rows.** Customer (subdomain) / Seats / Snapshot date. Sheet path unchanged at 5 rows.
- **Country hallucination bug fixed.** Rule 196 in input_handling_spec + ROI header variant spec both now HARD BAN inferring country from subdomain, prior session, or account-name pattern. Observed bug: model rendered `Spain · 18 seats` for PAYPER PDF session where no country was in source or CSM input. Hard Constraint #8 violation. ROI header on PDF path collapses to `{SEATS} seats · Directional estimates for CSM conversation` — no country, no plan.
- **Gate blank-country branch spec'd in full.** Full render shape stated verbatim (was previously a one-liner hint). PDF path ALWAYS hits this branch.
- **Seat-verification nudge (PDF path, conditional).** Renders IN the salary-gate turn between locked-inputs list and "Reply with the salary" line when either: Active Agents last month < 0.85 × Activated Agents, OR Agent Count changed by ≥2 over the 12-month baseline window. Tells CSM actual activated/active/growth numbers so they can override `seats:` at the gate if working headcount differs. Suppressed entirely when seats are stable and active ≈ activated.
- **Why this narrowing:** notify-fill added friction (extra CSM turn) for data that's mostly optional. Hallucination risk (model filling in blanks from prior memory) outweighed the occasional real benefit. Better: render only what's in the source, warn specifically on seat ambiguity (the one number that directly moves ROI math).

Fifth pass — **reliability tightening after PAYPER PDF re-run** (2026-05-05):
- **Cost-per-ticket formula lock.** Observed bug: model rendered COST_PER_TICKET=€116 on PAYPER PDF inputs (salary €30k, 620/mo, 18 seats) where the correct value is €73. Root cause: model substituted 240 hrs/month (8×30 calendar days) for the canonical 150 hrs/month (7.5×20 workdays) monthly-hours divisor. Fix: Layer 1 rewritten with named constants (`ANNUAL_WORKING_HOURS=1800`, `MONTHLY_WORKING_HOURS=150`), single-step formula, full worked example (PAYPER €30k → €73), and a three-check verification block that rejects any output where `COST_PER_TICKET > HOURLY_WAGE × 10`. Ambiguous `(240/12) / HOURS_PER_DAY` form retired.
- **Currency fallback when country blank.** PAYPER PDF run rendered naked numbers (`43k`, `130k`, `90k`, no €) because country was blank → currency inference silently dropped the symbol. Fix: when country is absent, salary-gate re-asks if CSM typed a bare number with no symbol/code. Currency now comes from CSM symbol/code when the country map is silent. Never render ROI with naked monetary numbers.
- **Numbers-table middle column = 12-month MEDIAN, not latest-month value.** This is the cross-source reproducibility fix. PAYPER TTC monthly values swing wildly (43 → 3,173 → 1,066 across three consecutive months) → same-source re-runs could land on different middle-column numbers just because the month at the edge of the window moved. Switched to MEDIAN of the 12 monthly values for FRT, TTC, Zero-touch, One-touch, Self-service, CSAT. Channel mix → 12-month average share. Middle-column header renamed to `12-month typical`. Read column (third column) still uses MEAN-based direction computation — typical value (median) vs. trajectory (mean) answer different questions.
- **Why it matters for Sheet vs PDF parity:** Sheet snapshot date = Apr 2026 (latest-month TTC 418 hrs). PDF snapshot = Mar 2026 (latest-month TTC 1,066 hrs). Same customer, same numbers, 10× different rendered value under latest-month rule. Under median rule, both render ~360 hrs (the real typical-month figure). Cross-source renders now converge.

Sixth pass — **sub-1% render rule + median deterministic lock** (2026-05-05):
- **Sub-1% rule hardened.** Self-service/Zero-touch/One-touch/CSAT-response-rate render as literal `<1%` whenever the computed 12-month MEDIAN is ≥ 0 and < 0.01, INCLUDING the case where every month is exactly 0.000. Previously `0%` could render on PDF (all zeros) while Sheet showed `<1%` (tiny near-zero decimals). Same CSM-facing signal in both cases → render uniformly as `<1%` for cross-source parity.
- **Median recompute lock.** Observed drift: Zero-touch rendered 17% on one PAYPER PDF run and 19% on another (same file, same session). Median of 12 values is deterministic — it's not a sampling question. Fix: added explicit sorted-midpoint definition (`sorted[6] + sorted[7] / 2`, 1-indexed), mandatory calculator call, and a "re-compute from raw series, never carry forward from memory" rule. Both values in the median calc must come from the calculator, no mental pick.
- **ADDITIONAL_AGENTS_NEEDED check:** examined PAYPER run, 5.95 agents → ceiling = 6 is correct per spec. No bug. Headline $180k = 6 × $30k also correct.

Seventh pass — **cross-file consistency sweep** (2026-05-05):
Datifyer ship-candidate accepts only 2 sources (Sheet QBR workbook, AIH PDF). Swept all orphaned references to the retired formats:
- **Datifyer_v3.1_production.md:** Industry enrichment spec reconciled (PDF path → row OMITTED, not N/A). Hard Constraint #2 dropped "beyond Tavily public averages". Hard Constraint #4 rewritten ("render what's there; omit what isn't") — notify-fill language retired. Source-provenance rule updated (no notify-fill ref). Field-level provenance tags trimmed to 4 tag shapes (`source: Google Sheet`, `source: AIH PDF`, `CSM input (gate)`, `CSM override (gate)`) — Tavily tags dropped. Internal-workings line retired "fetched Tavily values". Extraction confidence Medium wording fixed. Primary input handling retired notify-fill ref. Industry row render rule path-specific. Coverage summary updated to 24-month examples. Currency fallback at line 991 no longer says "use tavily_search" (direct contradiction with line 977 fixed).
- **sage_v3.1_main_production.md:** Hard Constraint #21 rewritten to two canonical inputs only (Sheet QBR + AIH PDF). Non-accepted formats (CSV, Excel, dashboard screenshots, chart images, pasted tables, non-AIH PDFs) get a literal redirect at SAGE and are NEVER handed off to Datifyer. Two-stage CSV/Excel flow retired — it pointed at a Datifyer acceptance path that no longer exists. Welcome message updated to name the two inputs. Mode Detection table first row tightened to name AIH PDF explicitly. Second row replaced with the redirect-at-SAGE rule. Non-data-file row cross-references the two new rows. `file_search` override rule updated for the two-accept / redirect split.
- **Why it matters:** prior state risked CSM uploading an Excel file → SAGE offering Datifyer handoff → Datifyer rejecting the non-canonical source → session stall. New flow: SAGE redirects up front, session never reaches a dead-end handoff.

Eighth pass — **currency conflict resolution + headline ratio guard** (2026-05-05):
- **Currency-mismatch ask.** Observed bug: CSM typed `$40K` on a Spain-mapped Sheet session; model silently rendered ROI in USD — Spanish customer's numbers in wrong currency. Fix: when CSM's typed symbol conflicts with country-derived currency, gate now asks once (1 = local, 2 = typed) before proceeding to Layer 1. Same-currency case (typed matches country) proceeds silently, no friction. Country-blank PDF case unchanged (typed is authoritative).
- **Headline range ratio verification (Layer 2).** Observed bug: PAYPER Sheet rendered 💰 as `$36k / $44k` (ratio 1.22). Math ground truth = `$36k / $108k` (ratio exactly 3.0, because 15% / 5% = 3 on same baseline+cost). Fix: added Rule 4h in `<verification_loop>` + worked example in Layer 2 spec + hard reject if `B/A` outside [2.9, 3.1]. Any run-to-run compression now blocks before render.
- Both fixes are calculator-enforced, not mental checks. Both ship in `Datifyer_v3.1_production.md` ninth iteration.

Ninth pass — **canonical window anchor + internal-values dump** (2026-05-05):
- Observed bug: same PAYPER Sheet, two consecutive runs, same session → FRT drifted 2.2 → 3.2 → 4.0; Zero-touch drifted 17 ↔ 19%. Median of a fixed 12 values is deterministic — any swing means the model picked different 12 values each run.
- Root cause: "last 12 rows" was ambiguous — model could interpret as last-12-rows-in-tab, last-12-rows-with-data, last-12-rows-excluding-trailing-nulls-one-way-or-another, or anchor-shifted by one month.
- Fix: Window semantics rewritten in `<input_handling_spec>`. Four explicit steps: sort by DATE ascending, find anchor-month (max DATE with non-null closed tickets), canonical 12-month window = anchor back 12, prior 12-month window = anchor minus 12 back to anchor minus 23. Same anchor for ALL Numbers-table metrics in a single run. Middle-column MEDIAN, Read-column 12v12 MEAN, AVG_MONTHLY_CLOSED, and GROWTH_RATE all derive from the same two windows — never shifted.
- Internal-values dump (mandatory checkpoint): before rendering any middle-column MEDIAN, extraction trace must log `sorted = [v1..v12]; (sorted[6] + sorted[7])/2 = X`. When the model can name the 12 values it's medianning, the median is deterministic. When runs swing, the dumps will differ — that's the signal the window anchor drifted.
- Why it matters: this is the last determinism hole. Lock this and cross-run parity holds on both Sheet and PDF paths.

Tenth pass — **polish: rounding, bare-number silent-pass, plan-pick** (2026-05-05):
- **Money rounding tightened.** Spec now explicit: nearest-thousand half-up. `108,108` → `€108k` (not €107k). Floor-style rounding banned. Fixes PAYPER headline that rendered €107k instead of €108k.
- **Bare-number + known-country silent-pass.** CSM types `40K` on Spain Sheet → model now locks EUR silently, no re-ask. Re-ask only when country is blank (PDF path). Removes unnecessary friction on the common path. Currency-mismatch rule still fires when typed symbol conflicts with country (the actual bug case).
- **{CORE_PLAN} header pick logic spec'd.** ROI header takes primary Suite SKU from PRODUCT_OFFERINGS_LIST via priority ladder (Enterprise > Growth > Team > Professional, Support tiers after). Snapshot `Plans active` row still renders full list; only the header picks one. Resolves the drift where model inferred `Suite Enterprise` without a written rule.
- All three are cosmetic polish on top of the determinism lock from ninth pass. Ship-candidate stable.

Eleventh pass — **visible anchor caption (determinism made observable)** (2026-05-05):
- Observed: Sheet path FRT/TTC median kept drifting across runs (2.1 / 2.2 / 3.2 / 4 hrs) despite ninth-pass window-anchor rule and internal-values dump requirement. PDF path stayed stable. Delta = how Sheet rows arrive vs. how PDF tables arrive — internal-dump spec was unenforceable (model skipped it silently).
- Fix: replaced internal-only dump with a MANDATORY visible italic caption rendered below the Numbers table, above Probes.
- Why visible forces compliance: model cannot write the month range in output and then silently compute median on a different window without creating a visible contradiction.
- Result in testing: caption rendered correctly but median STILL drifted. Even GROWTH_RATE changed (34% → 24%). Caption was decorative — model wrote window but computed on different rows. Prompt-layer ceiling confirmed on this path.

Twelfth pass — **full rollback to session-start stable state** (2026-05-05):
- Middle column reverted to `[Latest Month YYYY]` single-row value (pre-median). Deterministic by construction.
- Window semantics reverted to the original 4-line form: "12 most recent rows = baseline, 24 most recent rows = growth input, last row = latest month." The 4-step canonical-anchor block added in ninth pass was dropped — it tried to enforce deterministic median but the added complexity appeared to destabilize GROWTH_RATE calc that was previously working on simple "last 24 rows."
- Anchor caption ("Latest 12 months: X. Prior 12 months: Y.") removed. Was load-bearing under median path, decorative after rollback.
- Middle-column header reverted from `12-month typical` to `[Latest Month YYYY]` (e.g., `Apr 2026`). Read column stays `12-month read`.
- Sub-1% rule KEPT (works on anchor-month single value, useful for cross-source parity on zero-signal metrics).
- All other passes KEPT: currency conflict ask, headline ratio check, cost/ticket formula lock + worked example, scoped Section 8, PDF seat nudge, menu header retired, PDF snapshot 3-row form, Hard-banned country hallucination, CSV/Excel/other-PDF SAGE-side redirect, etc.
- Why fully roll back windowing: user observed that 3-4 runs at session start with the original simple spec were stable. Every added layer (median, canonical window block, visible anchor caption) introduced drift instead of removing it. Prompt-layer ceiling = rule-complexity ceiling. Simpler spec → more reliable.
- Trade-off: latest-month single values CAN show outliers (PAYPER Dec TTC = 3,173). Rule 4 outlier flag still present, Read column still carries 12v12 direction for trend signal. CSM gets "what happened last month" + "how it's moving" — two honest signals, no drift.

Thirteenth pass — **outlier caveat for latest-month middle column** (2026-05-05):
- Observed on PDF run: PAYPER Mar 2026 TTC = 1,066 hrs (huge spike vs. ~358 hrs typical neighboring months). Middle column rendered 1,066 honestly but Read column said generic "Very long and getting longer" with no caveat. CSM would read as "this customer's resolution time is 1,066 hrs" when it's really a single-month spike.
- Fix: Rule 4 expanded from YoY-only to BOTH latest-month outlier (4A) and YoY-anchor outlier (4B). Latest-month outlier triggers when anchor value > 2× 11-month-rest median OR < 0.5× it. Read column caveat mandatory: *"Mar spike; typical ~360 hrs"* or similar — 3-7 words, same units as middle column.
- Applies to FRT, TTC, Zero-touch, One-touch, Self-service. CSAT partial-reporting rule unchanged. Ratios near zero get no flag (rest of window also zero = not an outlier, just zero metric).
- Why: latest-month rule is honest and deterministic but can stampede CSM into a wrong interpretation if the month happens to be a spike. Caveat keeps the value visible AND tells the CSM it's an outlier — two signals in one Read column.

Test bed: PAYPER sheet (2070537279 tab, 24 months, Spain). Ground truth computed with Python: AVG_MONTHLY_CREATED=972, AVG_MONTHLY_CLOSED=660, GROWTH_RATE=34%, FRT 12v12=+286%, TTC 12v12=+54%, zero-touch +2 pts. All match when rendered correctly.

Known residuals:
- FRT/TTC/Channel mix/ratio Trend cells retired from table (drifted across runs even with tight spec — prompt-layer ceiling on these specific cells). Read column carries direction as words, not numbers.
- Model occasionally under-renders "What's already working" line with a stretched 3rd win when only 2 real wins exist. Cosmetic.

## Prompt Lines

### Active production (V3.1, rolled out 2026-04-26)
- SAGE: `Versions/production/sage_v3.1_main_production.md`
- Datifyer: `Versions/production/Datifyer_v3.1_production.md`
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
- Bug or missing feature in production → edit the files in `Versions/production/` (`sage_v3.1_main_production.md` / `Datifyer_v3.1_production.md`) directly.
- Never edit V3.0 files unless rolling back. V3.0 is a frozen reference snapshot.
- New experiments that aren't production-ready yet should be created as new files (e.g., `sage_v3.2_experimental.md`) and added to `.gitignore`'s allowlist if they need to be tracked.

## What's Next
- Monitor V3.1 in production for real CSM feedback.
- Watch for the specific V3.1 changes in action: welcome MCP probe catching auth issues, Deliverables outputs staying in-language, no mixed-language headers.
- Continue monitoring GPT-5.4 for behavior drift (banned words, hedge language, verbosity, backstage leaking).

## How to Use promptsmith.md
The promptsmith skill is used to analyze and score LibreChat agent prompts. To invoke it, read the file and adopt its framework. It provides: classification, dimensional scoring (1-10), diagnosis by severity, and rewrite guidance. It has LibreChat-specific knowledge (capabilities, handoffs, artifacts, step limits).
