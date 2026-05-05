---
name: Datifyer V3 production line (V3.0, V3.1, V3.1_production)
description: V3.1_production is active production (rolled out 2026-05-05). Mirrors SAGE naming — `_production.md` is the active file, `_v3.1.md` is staging (frozen reference), `_v3.0.md` is previous production (frozen reference).
type: project
originSessionId: 317886d8-0b67-4fc0-b4d4-e1af062bab50
---
**Active production:** `Versions/production/Datifyer_v3.1_production.md` (rolled out 2026-05-05).
**Previous staging (frozen reference):** `Versions/Datifyer_v3.1.md` (active 2026-04-26 to 2026-05-05). Do NOT edit.
**Previous production (frozen reference):** `Versions/Datifyer_v3.0.md` (active 2026-04-24 to 2026-04-26). Do NOT edit.

**Folder structure:** `Versions/production/` holds the two live files (`sage_v3.1_main_production.md` + `Datifyer_v3.1_production.md`). Everything else in `Versions/` is a frozen reference snapshot.

Naming mirrors SAGE: `{agent}_v3.1_production.md` = live file, `{agent}_v3.1.md` = staging/prior iteration.

**How to apply:**
- Bug fixes and feature work land in `Datifyer_v3.1_production.md` directly.
- Never edit `Datifyer_v3.1.md` or `Datifyer_v3.0.md` — both are frozen reference snapshots.
- New experimental lines go in a new file (e.g., `Datifyer_v3.2_experimental.md`).

**Why V3.1_production exists (2026-05-05 promote):** V3.1 had severe reproducibility bugs on ROI output. Same PAYPER sheet yielded cost/ticket €27-€128, headline ranges €11k-€108k, growth clause €130k-€360k across runs. Traced to Tavily salary drift, FRT/TTC Trend cell flipping, Ticket volume recompute, industry website-ask, Layer 5 base confusion (closed vs created). Fixed incrementally over 24+ PAYPER runs plus follow-up refinements; reached numeric lock across consecutive re-runs on both Sheet and PDF inputs.

**Load-bearing determinism architecture in V3.1_production:**

1. **Two accepted inputs only.** Google Sheet QBR workbook (primary, Sheet-side extraction path) + AIH Trended Metrics View PDF (fallback, 24-month operational data). All other formats (CSV, Excel, screenshots, pasted tables, non-AIH PDFs) rejected at SAGE with a redirect message — never handed to Datifyer.

2. **Scoped extraction set.** Sheet: Metrics A-L, Account Details 10 fields (PRODUCT_OFFERINGS_LIST, not CORE_BASE_PLAN), Tickets by Channel full, Benchmarks skipped by default. PDF: full section-map from AIH labels to schema (Created/Solved volumes, FRT/TTC/Zero-touch/One-touch/Self-service/CSAT, Channel mix + YoY, Agent Count + Activated/Remaining seats).

3. **Scientific-notation normalization** at extraction (`2.29E-01` → 0.229 → 22.9%). Validates 0.0-1.0 range post-parse.

4. **Snapshot row count varies by path.** Sheet = 5 rows (Customer / Industry / Plans / Seats / Snapshot date). PDF = 3 rows (Customer subdomain / Seats / Snapshot date). Industry/Country/Plans rows OMITTED on PDF path (not rendered as N/A).

5. **Numbers section.** Volume callout = 1 prose sentence above table. Table = 3 cols: Area | [Latest Month YYYY] | `12-month read`. Middle column = single anchor-month row value (deterministic by construction — tried median, drifted, rolled back). Ticket volume NOT in table. Read column = only trend signal for service metrics, factually directional or factually state-describing.

6. **Rule 4 outlier caveat.** If anchor-month value > 2× 11-month-rest median OR < 0.5× it, Read column renders caveat (e.g., `Mar spike; typical ~360 hrs`) instead of generic direction phrase. Honest render preserved — CSM sees the value AND the outlier context.

7. **Sub-1% render rule.** Ratios (Zero-touch, One-touch, Self-service, CSAT Response Rate) below 0.01 render as `<1%`, including exact-zero case. Cross-source parity: Sheet near-zero decimals and PDF literal zeros both render the same way.

8. **Country hallucination HARD BAN on PDF path.** Country was NOT in the PDF. Do NOT infer from subdomain, prior session, account pattern. ROI header on PDF collapses to `{SEATS} seats · Directional estimates for CSM conversation`.

9. **PDF seat-verification nudge (conditional).** Fires in salary gate when Active Agents < 0.85 × Activated OR Agent Count changed by ≥2 over the 12-month window. Tells CSM the three candidate numbers (activated, active, 12-mo-ago) so CSM can override `seats:` at gate.

10. **ROI confirmation gate.** CSM types loaded salary with regional hint band (EMEA €25-40k / AMER $40-70k / APAC $20-35k / LATAM $12-25k). Bare salary (no `go` required) runs ROI directly. Blank-country branch (PDF always hits this): `"I don't have the customer's region from the source — type the loaded annual salary you'd like to use."`

11. **Currency-mismatch gate ask.** If CSM's typed symbol (`$40K`) conflicts with country-derived currency (Spain → EUR), gate asks once: `1 → EUR (local) / 2 → USD as typed`. Blocks silent-override bug. Bare-number + known-country is silent-pass (no re-ask).

12. **Salary = CSM-typed, no transformation.** Tavily salary retired. `LOADED_SALARY = CSM_TYPED_SALARY` literal. `HOURLY_WAGE = LOADED_SALARY / 1800`. `MONTHLY_WORKING_HOURS = 150` (fixed constant, NEVER 240).

13. **Cost-per-ticket formula lock + worked example.** `COST_PER_TICKET = HOURLY_WAGE / (AVG_MONTHLY_CLOSED / SEATS / 150)`. PAYPER: €30k → €73, €40k → €91. Three-check verification: `COST × TPH ≈ HOURLY`, `COST > HOURLY × 10` = bug.

14. **Layer 2 headline ratio check.** `B/A` (15%/5%) MUST be in [2.9, 3.1]. If not, recompute. Catches the `$36k/$44k` compression bug.

15. **Layer 5 growth base lock.** `ADDITIONAL_MONTHLY_TICKETS = AVG_MONTHLY_CLOSED × GROWTH_RATE`. Closed-always. Created inflated agent count by 30-50%.

16. **💰 block:** two numbered bullets. "Save money on today's volume" (5% low / 15% high explicit). "Avoid hiring as volume grows — up to €C/year" with "X more agents" concrete anchor. Plain-English discipline.

17. **Menu header retired.** Numbered options self-announce. Applies to Sections 1-5 first run, email, ROI, Q&A, any ROI adjustment.

18. **Section 8 scoped ask.** "Ask me how I got these numbers" opens with scope ask (cost per ticket / growth rate / deflection / hiring avoidance / source-vs-CSM provenance). CSM picks one; scoped answer follows. Prevents one-shot methodology dump.

19. **Money rounding = nearest-thousand half-up.** `108,108` → `€108k` (not €107k floor).

20. **{CORE_PLAN} ROI header picker.** From PRODUCT_OFFERINGS_LIST (Sheet path), priority: Suite Enterprise > Suite Growth > Suite Team > Suite Professional > Support tiers. Snapshot `Plans active` row still renders full list verbatim.

**Iteration lessons carried forward:**

1. **Shorter spec > longer spec.** Verbose step-by-step formulas + cautionary examples often produce MORE drift than terse one-liners.

2. **Every metric with a rendered Trend cell is a bug candidate.** Dropped Trend column entirely — major determinism win.

3. **Single-render per number.** Show volume ONCE (callout), reused from growth calc.

4. **CSM-typed salary > Tavily-fetched salary.** 30-60% variance with Tavily. Asking CSM is slower but deterministic.

5. **Prompt-layer ceiling is real.** Some bugs can't be spec'd away. Architecture changes (drop the cell, single-row extract, visible caption) succeed where additional rules fail. Tried median for middle column to smooth volatility — drifted across runs despite explicit anchor rule — rolled back to latest-month single-row.

6. **Visible checkpoints > internal-only dumps.** Internal trace rules get skipped silently by model. Visible output that commits model to a specific value (anchor-month header like `Apr 2026`) is enforced by coherence.

7. **Spec contradictions matter more than spec detail.** Explicit exception clauses needed when one rule supersedes another (e.g., `<output_contract>` "5 sections always" vs. ROI gate "after go render only ROI" — required a carve-out).

**PAYPER ground truth (baseline test customer):**
- AVG_MONTHLY_CREATED = 972, AVG_MONTHLY_CLOSED = 660, GROWTH_RATE = +34% 12v12
- Sheet Apr 2026: FRT 3 hrs, TTC 418 hrs, ZT 24%, OT 21%, SS <1%
- PDF Mar 2026: FRT 2.8 hrs, TTC 1,066 hrs (outlier — caveat fires), ZT 23%, OT 26%, SS <1%
- With €40k salary: cost/ticket €91, Pillar 1 Conservative €36k, Pillar 1 Moderate €108k, 7 additional agents, €280k growth clause
