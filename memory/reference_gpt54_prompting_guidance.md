---
name: GPT-5.4 / GPT-5 prompting guidance (OpenAI cookbook, fetched 2026-04-21)
description: Distilled guidance from OpenAI's GPT-5 and GPT-5.4 prompting guides that is relevant to SAGE on LibreChat. Use to inform v2.5 passes 2-4.
type: reference
originSessionId: cc62068c-7019-4b0c-b4cc-18866b65b4aa
---
**Sources fetched:**
- https://developers.openai.com/api/docs/guides/prompt-guidance (GPT-5.4 specific)
- https://developers.openai.com/cookbook/examples/gpt-5/gpt-5_prompting_guide
- https://developers.openai.com/cookbook/examples/gpt-5/gpt-5_troubleshooting_guide
- https://developers.openai.com/cookbook/examples/gpt-5/gpt-5-1_prompting_guide
- https://developers.openai.com/cookbook/examples/gpt-5/gpt-5-2_prompting_guide

**Key principles relevant to SAGE:**

1. **Contradictions hurt more on GPT-5.4 than on prior models.** The model burns reasoning tokens reconciling conflicts. Removing them is the single highest-leverage cleanup. This is why pass 1 is contradiction fixes.

2. **XML spec blocks improve instruction adherence** (e.g., `<plan_detection_spec>`, `<mcp_reliability_spec>`). Cursor used this pattern; OpenAI recommends it. Structure beats prose on GPT-5.4.

3. **GPT-5.4 "good default pattern" for each section:** Task → Critical rule → Exact step order → Edge cases → Output format → One correct example. Avoid: implied next steps, unspecified edge cases, schema-only prompts, generic instructions without structure.

4. **Verbosity is an API parameter, not a prose rule.** `verbosity: low/medium/high` is the native knob. Prompt rules like "keep responses concise" are redundant and waste tokens. Inline overrides for specific contexts work (Cursor used global low + high for coding tools).

5. **Reasoning effort is an API parameter** (`minimal/low/medium/high/xhigh`). Not to be steered by prose. Medium is a fine default for SAGE.

6. **Tool descriptions:** 1-2 sentences per tool, plus "don't use for..." notes. Paragraphs of routing logic can be replaced by crisp tool specs + a routing table.

7. **Agentic eagerness is tunable:** `<persistence>` and `<context_gathering>` blocks control it. SAGE's step budget section can become a `<context_gathering>` block with explicit stop criteria.

8. **Tool preambles** (1-sentence "why I'm calling this tool") improve user experience in long-running agentic flows. Already partially present in SAGE's Research Completion Message.

9. **Metaprompting works.** Ask GPT-5.4 itself to flag contradictions or failure modes in a prompt. Used successfully in pass 1 audit.

10. **Remove Claude-era hedging.** GPT-5.4 doesn't hedge the same way Claude did; banned-word lists targeting "dive in, leverage, empower, unleash" etc. are likely no-ops on GPT-5.4 and can be tested empirically before keeping.

**Does NOT apply to SAGE:**
- Responses API migration (LibreChat uses Chat Completions; `useResponsesApi` is off for SAGE)
- Coding-specific guidance (apply_patch, Cursor integration)
- Frontend app generation patterns

**LibreChat-supported parameters confirmed:**
- `reasoning_effort`: minimal/low/medium/high/xhigh
- `verbosity`: low/medium/high
- `reasoning_summary`: none/auto/concise/detailed
- `useResponsesApi`: bool
- Not settable on GPT-5: temperature, presence_penalty, frequency_penalty, top_p

**How to apply:** Consult this memory in any future SAGE prompt-engineering session. Do not re-fetch the cookbook unless OpenAI publishes a newer guide or the guidance here is being applied to a different model.
