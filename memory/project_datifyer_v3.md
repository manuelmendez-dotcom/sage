---
name: Datifyer V3.0 production line
description: Datifyer V3.0 is the active production prompt at prompts/datifyer_v3.0.md. Versioning was reset 2026-05-18 — prior V3.0/V3.1/V3.2 history collapsed; all "retired in v3.2" qualifiers stripped. The 24-run PAYPER determinism architecture is preserved; only the version markers were reset.
metadata:
  type: project
---
**Active production:** `prompts/datifyer_v3.0.md`. Single live file, no parallel staging.

**Why the reset (2026-05-18):** See [[project_sage_v3]]. Same mass cleanup. The math engine and all determinism locks survived intact — only version qualifiers in prose were rewritten.

**How to apply:**
- Bug fixes + feature work land directly in `prompts/datifyer_v3.0.md`.
- Same bump rules as SAGE — material change only.
- When testing math changes, run regression against `reference/payper_*.md` sessions (PAYPER is the canonical test customer).

**Load-bearing determinism architecture (preserved through reset):**

1. **Two accepted inputs only.** Google Sheet QBR workbook (primary, full commercial fields) + AIH Trended Metrics PDF (fallback, 24-month operational data). All other formats (CSV, Excel, screenshots, pasted tables, non-AIH PDFs) rejected at SAGE with redirect — never handed to Datifyer.

2. **Scoped extraction set.** Sheet: Metrics A-L, Account Details 10 fields (PRODUCT_OFFERINGS_LIST), Tickets by Channel full, Benchmarks skipped. PDF: full section-map (Created/Solved volumes, FRT/TTC/Zero-touch/One-touch/Self-service/CSAT, Channel mix + YoY, Agent Count + Activated/Remaining seats).

3. **Scientific-notation normalization** at extraction (`2.29E-01` → 0.229 → 22.9%). Validates 0.0–1.0 range post-parse.

4. **Snapshot rows by path.** Sheet = 5 rows (Customer / Industry / Plans / Seats / Snapshot date). PDF = 3 rows (Customer subdomain / Seats / Snapshot date). Industry/Country/Plans rows OMITTED on PDF path (not rendered as N/A).

5. **Numbers section.** Volume callout = 1 prose sentence above table. Table = 3 cols: Area | [Latest Month YYYY] | `12-month read`. Middle column = single anchor-month row value (deterministic by construction — tried median for cross-source parity, drifted across runs despite explicit anchor rule, rolled back to single-row).

6. **Rule 4 outlier caveat.** If anchor-month value > 2× 11-month-rest median OR < 0.5× it, Read column renders caveat (e.g., `Mar spike; typical ~360 hrs`). Honest render preserved.

7. **Sub-1% render rule.** Ratios (Zero-touch, One-touch, Self-service, CSAT Response Rate) below 0.01 render as `<1%`, including exact-zero. Cross-source parity.

8. **Country hallucination HARD BAN on PDF path.** Country was NOT in the PDF. Do NOT infer from subdomain, prior session, or account pattern. ROI header on PDF path: `{SEATS} seats · Directional estimates for CSM conversation`.

9. **PDF seat-verification nudge (conditional).** Fires in salary gate when Active Agents < 0.85 × Activated OR Agent Count changed by ≥2 over 12-month window.

10. **ROI confirmation gate.** Bare salary (no `go`) runs ROI directly. Blank-country branch (PDF always hits this).

11. **Currency-mismatch gate ask.** CSM-typed symbol conflicts with country-derived currency → gate asks once `1 → local / 2 → typed`. Bare-number + known-country = silent pass.

12. **Salary = CSM-typed, no transformation.** Tavily salary retired. `LOADED_SALARY = CSM_TYPED_SALARY` literal. `HOURLY_WAGE = LOADED_SALARY / 1800`. `MONTHLY_WORKING_HOURS = 150` fixed (NEVER 240).

13. **Cost-per-ticket formula lock + worked example.** Three-check verification: `COST × TPH ≈ HOURLY`, `COST > HOURLY × 10` = bug.

14. **Layer 2 headline ratio check.** `B/A` (15%/5%) MUST be in [2.9, 3.1]. Catches `$36k/$44k` compression bug.

15. **Layer 5 growth base lock.** `ADDITIONAL_MONTHLY_TICKETS = AVG_MONTHLY_CLOSED × GROWTH_RATE`. Closed-always (created inflated agent count 30–50%).

16. **3-pillar ROI render.** Pillar 1 Deflection / Pillar 2 Productivity / Pillar 3 Capacity Question. Named markdown headers, no emoji anchors, no "Need different assumptions?" block, no bottom footer disclaimer.

17. **Menu header retired.** Numbered options self-announce.

18. **Section 8 scoped ask.** "Ask me how I got these numbers" opens with scope ask, not methodology dump.

19. **Money rounding = nearest-thousand half-up.**

20. **{CORE_PLAN} ROI header picker** (when used): Suite Enterprise > Growth > Team > Professional > Support tiers.

**Iteration lessons (cross-cuts to [[reference_prompt_layer_ceiling]]):**
- Shorter spec > longer spec. Verbose formulas often produce MORE drift.
- Every rendered Trend cell is a bug candidate. Trend column dropped entirely.
- Single-render per number (volume ONCE in callout).
- CSM-typed salary > Tavily-fetched salary (30–60% variance).
- Prompt-layer ceiling is real. Architecture changes (drop the cell) succeed where rule additions fail.
- Visible checkpoints > internal-only dumps.

**PAYPER ground truth (baseline test customer):**
- AVG_MONTHLY_CREATED = 972, AVG_MONTHLY_CLOSED = 660, GROWTH_RATE = +34% 12v12
- Sheet Apr 2026: FRT 3 hrs, TTC 418 hrs, ZT 24%, OT 21%, SS <1%
- PDF Mar 2026: FRT 2.8 hrs, TTC 1,066 hrs (outlier — caveat fires), ZT 23%, OT 26%, SS <1%
- With €40k salary: cost/ticket €91, Pillar 1 Conservative €36k, Pillar 1 Moderate €108k, 7 additional agents, €280k growth clause

Related: [[project_sage_v3]], [[reference_prompt_layer_ceiling]].
