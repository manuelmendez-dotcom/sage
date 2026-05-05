---
name: Prompt-layer determinism ceiling (LibreChat GPT-5.4)
description: Pattern observations from 24-run PAYPER debug on Datifyer — what spec-layer fixes can and cannot lock. Transferable to SAGE and future prompt work.
type: reference
originSessionId: 317886d8-0b67-4fc0-b4d4-e1af062bab50
---
**Context:** 24 test runs of Datifyer on identical PAYPER Google Sheet produced headline numbers varying up to 3× (cost/ticket €27-€128, ROI ranges €11k-€108k). Pure prompt-layer fixes had diminishing returns. Pattern held across different bug types.

**What prompt-layer CAN lock reliably (observed across 20+ runs after fix):**

1. **Single-source-of-truth inputs that bypass model computation.** CSM-typed salary locked the loaded-salary input. Spec-defined constants (1,800 annual hours) locked downstream cost math.

2. **Extraction from structured fields with explicit column mapping.** Metrics tab A-L, Account Details named fields. Model reliably reads what's scoped.

3. **Simple single-step calculator calls with one input path.** Volume 12v12 growth rate (+34% PAYPER) held across every run because there's one obvious formula and one obvious data source.

4. **Format rules that have no competing alternative interpretation.** Em-dash vs italic `qualitative` rendering — model picks what spec says when there's no other reasonable choice.

5. **Hard gate pauses with explicit "wait for user input" instruction.** ROI confirmation gate successfully stopped math until CSM replied.

**What prompt-layer STRUGGLES to lock (observed drift across runs even with tight spec):**

1. **Cells with adjacent-column data.** FRT (RBA_FRT_MEDIAN_HOURS) and TTC (RBA_TTC_MEDIAN_HOURS) are adjacent in the sheet. Model swapped Trend cells between these two columns in multiple runs despite explicit metric-to-cell binding.

2. **Aggregation method when multiple are plausible.** "Average" = arithmetic mean in spec, but model sometimes used median of monthly medians for FRT/TTC (which are already per-month medians). Spec saying "arithmetic mean not median" didn't prevent the flip consistently.

3. **Same quantity computed twice for display.** Ticket volume middle column (separate recompute) drifted 852-972 even when spec said "reuse the Trend numerator." Model recomputed anyway, dropping months inconsistently.

4. **Choice between two related data fields as a formula base.** Growth math base — AVG_MONTHLY_CLOSED (capacity) vs AVG_MONTHLY_CREATED (demand). Flipped across runs, causing 30-50% swing in ADDITIONAL_AGENTS_NEEDED.

5. **Tavily salary sanity-check fallback values.** Model rendered €23k, €31k, €33k, €32.5k when spec said "use canonical €25k EMEA fallback." Fallback value drifted within the fallback path itself.

6. **Re-render of content between turns.** Output contract "5 sections always appear" fought ROI gate's "render only ROI after go" — model re-rendered full 5-section summary on ROI request.

**What fixes DO work when bugs are in the struggle-list:**

- **Drop the cell entirely.** Replacing Trend percentages with `qualitative` label + factual Read column eliminated drift completely.
- **Single-render architecture.** Moving volume out of the table into a one-line callout (used ONCE in output) killed the recompute drift.
- **Move math off the model.** CSM-typed salary > Tavily lookup. User ownership > model inference.
- **Architecture change > spec tightening.** When Rule 4f verbose version failed, reverting to short spec AND restructuring (drop Trend column) succeeded.
- **Explicit hard-ban + concrete example.** Verification rules citing the specific past failure ("7→9 drift on PAYPER") hold better than rules stating only the positive invariant.

**What fixes DON'T work (even when they seem tight):**

- More verbose spec blocks with step-by-step formulas.
- Banned-word lists that model must avoid (occasionally pulled back into output).
- Cautionary examples of wrong output (model sometimes treats them as valid alternatives).
- Cross-reference rules between sections (Rule 4a refers to Rule 2, etc.) — attention window doesn't always activate both.

**Decision heuristic for future prompt debugging:**

When a bug appears:
1. First check if it's in the "CAN lock" bucket — if so, tighten spec once and expect it to hold.
2. If in "STRUGGLE" bucket, don't try 3+ spec revisions. Move to architecture change: drop the cell, move the render, take math out of model, ask CSM instead.
3. Concrete failure examples in verification rules help when kept short. Verbose spec always hurts.
4. If spec is getting longer to fix a bug, that's a signal the bug is architectural.

**Platform-specific notes:**

- LibreChat has no code-interpreter / Python execution for the agent. Deterministic math outside the model is not available inside Datifyer's runtime.
- Custom MCP servers could provide deterministic compute but require infra + deploy path.
- Google Sheet formulas (Coefficient-driven QBR Express pre-compute) offered as Option 2 for ROI determinism — user declined for now.
