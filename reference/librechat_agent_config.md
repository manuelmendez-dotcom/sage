# LibreChat Agent Configuration — SAGE + Datifyer

This file is the canonical record of LibreChat-side agent settings that are NOT inside `prompts/sage_v3.2.md` or `prompts/datifyer_v3.0.md`. It exists so the configuration is recoverable if the LibreChat agent record is overwritten or lost.

**Update this file whenever the UI config changes.** The prompts in `prompts/` reference this file — they are NOT the source of truth for handoff config.

## SAGE agent

### Model parameters
- Model: GPT-5.4 (direct OpenAI, not Bedrock)
- `reasoning_effort`: `medium`
- `verbosity`: `low`
- `useResponsesApi`: `on`

### Handoff to Datifyer

**Handoff description** (the tool description GPT-5.4 reads when deciding whether to invoke the handoff):

```
Transfer to Datifyer for customer data analysis when the input is a Google Sheet workbook link, AIH PDF (Ticket Volume & Performance Metrics or Trended Metrics View), dashboard screenshot, chart or graph image, pasted data table, OR when SAGE has already read a CSV or Excel file and the CSM has explicitly accepted an ROI handoff. Do not transfer for email drafting, writing, product questions, troubleshooting, or any SAGE native deliverable (recommendations, success plan, slide guide, configuration guide).
```

**Passthrough content** (what SAGE generates and passes to Datifyer at the handoff):

```
Instructions: You are being invoked by SAGE to perform customer data analysis. Produce your standard 5 section output (Snapshot, Story, Numbers, Probes, Menu) following your system prompt.

Source handling, in priority order:
1. If this handoff carries a Google Sheet link, AIH PDF, dashboard screenshot, chart image, or pasted data table, extract directly using your per-format extraction rules.
2. If this handoff carries pre-extracted numbers from SAGE (two-stage CSV or Excel flow, recognizable by a "Pre-read from SAGE" or "Extracted from CSV" block in the user context), treat those numbers as the source and do not re-extract the original file, since file content does not transfer across the handoff boundary; populate the standard schema from the provided values, tag provenance as "SAGE pre-read (CSV or Excel upload)", and proceed to the 5-section output.
3. If this handoff carries a CSV or Excel filename but no pre-extracted numbers, respond with a single-line clarification asking SAGE to send the extracted numbers or the CSM to paste them, and do not produce a 5-section output from the filename alone.

Apply your source-provenance rule, ROI-input discipline, and industry-enrichment tiers per your system prompt. Produce the full output shape with whatever fields the source contains, flag gaps.
```

**Content parameter name:** `instructions` (default).

### Why the Handoff fields, not the system prompt

LibreChat's Handoff feature creates a transfer tool the parent agent invokes. Per LibreChat translation strings (`com_ui_agent_handoff_*`):
- `Handoff description` = tool description the parent reads to decide WHEN to call.
- `Passthrough content` = the prompt-side instruction packaged as the tool input.

These two fields together replace what would otherwise be a long block in `<routing_spec>` listing accepted formats and the handoff payload. The system prompt still owns: rendering the redirect for rejected formats, attachment-presence rule, AIH title-match guard, file_search override, session ownership, failure handling, output contract, payload-echo ban.

## Datifyer agent

### Model parameters
- Model: GPT-5.4 (direct OpenAI)
- `reasoning_effort`: `medium`
- `verbosity`: `low`
- `useResponsesApi`: `on`

(Datifyer is the child in the handoff. It is NOT configured with its own handoff back to SAGE — return is handled by Datifyer's exit-signal logic in `prompts/datifyer_v3.0.md` and LibreChat's automatic handback at end-of-run.)

## Recovery procedure

If the LibreChat agent config is lost or overwritten:
1. Open the SAGE agent in LibreChat → Agent Builder.
2. Paste the **Handoff description** above into the SAGE → Datifyer handoff field.
3. Paste the **Passthrough content** above into the corresponding field.
4. Confirm model parameters match the table above.
5. Save.

If the wording above is updated in production but this file lags, the production UI is canonical. Update this file to match within the same change.
