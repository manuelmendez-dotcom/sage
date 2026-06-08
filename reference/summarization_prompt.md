# SAGE + Datifyer — Custom Summarization Prompts

Custom conversation-summarization prompts for the LibreChat auto-summarizer (gpt-5.4-mini) on SAGE and Datifyer. They override the generic default so that when a session hits the context limit and auto-summarizes, SAGE's load-bearing state survives instead of being dropped — so the model can pick up from the checkpoint instead of asking the CSM to repaste the last output.

## Why a custom prompt is needed

The default summarizer keeps narrative and drops SAGE's state (customer, plan, language, Datifyer math, active mode). SAGE wakes up blind and asks the user to repaste — and for SAGE, the last output alone is never enough. The fix is to name exactly what must survive. That list is the whole point of these prompts.

## How LibreChat uses these (verified against danny-avila/agents `src/summarization/node.ts`, v0.8.5+)

The summarizer is a **running-checkpoint refine loop** — it needs TWO prompts:

- **`summarization.prompt`** — fires on the FIRST compaction. Builds the initial checkpoint.
- **`summarization.updatePrompt`** — fires on EVERY later compaction. LibreChat auto-prepends the prior checkpoint as `<previous-summary>…</previous-summary>`; this prompt merges new turns in. On long sessions it runs repeatedly, so it's the load-bearing one.

No template placeholders — LibreChat does no interpolation. The only injected structure is `<previous-summary>` (updatePrompt only).

**For Bryan:** top-level `summarization:` key in `librechat.yaml`. Paste the two blocks into `prompt:` and `updatePrompt:`. YAML below.

---

## Block 1 — `summarization.prompt` (initial checkpoint)

```text
Write a checkpoint of this SAGE/Datifyer conversation. It REPLACES all earlier turns — whatever you omit is gone for the rest of the session. Output only the checkpoint, plain text, two sections.

STATE — copy these EXACTLY (numbers, currency symbols, plan names, language flags character-for-character). One per line; skip any that never came up:
- Customer name, industry, seats, plan
- Plan status: confirmed name, or unknown/asked-for
- Conversation language, and whether English is locked
- Active deliverable (Goals Analysis / Recommendations / Config Guide / email) and how far it got
- If Datifyer ran: Sheet vs PDF path; CSM-typed salary + currency symbol; agent/ticket/cost-per-ticket/growth/headline baselines; that Datifyer owns the session; any pending ask (currency mismatch, missing country, seat check)

Rules: asked-for-but-not-given → mark PENDING, never invent. Keep the latest value only. No facts that weren't in the conversation.

CONVERSATION SO FAR — brief: what was asked, what was delivered. If this conflicts with STATE, STATE wins.
```

---

## Block 2 — `summarization.updatePrompt` (running-checkpoint merge)

```text
Update the checkpoint. The prior one is above in <previous-summary>. Merge new turns in — don't restart, don't just append. Output only the merged checkpoint, same two sections.

Copy every STATE value from <previous-summary> forward exactly, unless a newer turn changed it (then keep the new one only). Add any new STATE value using the same list as before. A PENDING value that got answered → record the answer, drop PENDING.

Keep it about the same length: compress OLD narrative to one-liners to make room — never drop a STATE value. Treat prior values as ground truth; don't recompute. STATE wins over narrative on conflict.
```

---

## YAML for `librechat.yaml` (top-level `summarization:` block)

Drop the prompt text into `prompt:` and `updatePrompt:` (folded `|` scalars). Non-prompt fields are tuning defaults — adjust `model`/`trigger`/`provider` to the installed instance.

```yaml
summarization:
  enabled: true
  provider: "Internal-GPT54"      # custom-endpoint name serving the OpenAI key
  model: "gpt-5.4-mini"
  parameters:
    temperature: 0.0              # deterministic — consistent on which values survive
    top_p: 1.0
  maxSummaryTokens: 2048
  reserveRatio: 0.05
  trigger:
    type: "token_ratio"
    value: 0.8                    # fire at 80% of Max Context Tokens
  retainRecent:
    turns: 2                      # keep last 2 user-led turns verbatim, un-summarized
  prompt: |
    ...paste Block 1 here...
  updatePrompt: |
    ...paste Block 2 here...
```

### Field notes
- **`prompt` + `updatePrompt`** — both required. `prompt` fires once; `updatePrompt` fires on every later compaction and gets the auto-injected `<previous-summary>` block. Omitting `updatePrompt` leaves all refine passes on the generic default.
- **`temperature: 0.0` / `top_p: 1.0`** — deterministic, avoids cross-run drift in which values survive.
- **`maxSummaryTokens: 2048`** — SDK default; matches observed gpt-5.4-mini checkpoint size. STATE-first ordering keeps the must-keep values before any truncation point.
- **`retainRecent.turns: 2`** — last 2 turns stay verbatim regardless of summary, so a live deliverable isn't lossy-compressed mid-edit.
- **`trigger.value: 0.8`** — fires at 80% of Max Context Tokens. Raising the cap (270K → 400K) delays firing but uses these same prompts when it fires.

## Interaction with the cap-bump lever
Raising Max Context Tokens delays when summarization fires; it doesn't change what fires. These prompts are the safety net for the rare long session that crosses the threshold anyway. Both levers compose.
