# SAGE — What's New for CSMs

*From v2.1.2.3 to the current version*

- **Shorter, more focused outputs:** verbosity has been reduced across modes. Expect tighter responses with less filler — the quality is the same, the reading time is less.
- **Configuration Guide mode:** SAGE now produces step-by-step setup guides for a specific customer workflow, grounded in the Help Center.
- **Hardened plan detection:** SAGE confirms the customer's plan before output and asks when it's missing — no more silent assumptions.
- **Customer-language goals:** goal categories in transcript analysis now use the customer's own words, not Zendesk product terms.
- **Grounded recommendations:** every recommendation ties to something the customer actually said — no generic best-practice padding.
- **Dependency sequencing:** when a recommendation requires another to be in place first, SAGE states it explicitly.
- **Slide-ready Success Plans:** goals in 2-5 words, outcomes in 3-6 words, one-slide fit, every goal has resources.
- **Email drafts mirror the customer:** follows their structure instead of reframing, no "your concern is valid" openers.
- **Language-matched follow-ups:** post-draft prompts match the thread language, no English fallback in Spanish threads.
- **AI Product Truth automation:** SAGE applies the April 2026 AI agent rollout messaging automatically, overriding older docs.
- **Scoped workflow pause:** mid-deliverable clarifications answer inline; only unrelated questions pause the workflow.
- **Factual challenges trigger research:** push back on a number and SAGE re-searches instead of defending from memory.
- **Conflict flagging with dates:** when Help Center articles disagree, SAGE shows both with last-updated dates.
- **Sticky language override:** CSM can switch internal output language mid-session and it persists.
- **No fabricated packaging claims:** SAGE won't say "included on your plan" without confirmation, except for AI agent messaging.
- **Industry-tailored output:** SAGE asks for the customer's website once per session and uses it to sharpen recommendations, guides, and emails.
- **Datifyer accepts any data format:** Google Sheet workbooks, Excel, CSV, PDF exports, screenshots, pasted tables.
- **Datifyer standardized 5-section output:** Snapshot, the story right now, the numbers, what to probe, menu.
- **Customer-ready ROI:** customer-language pillar headers, whole-number rounding, dynamic month names, plain-word trend labels.
- **Datifyer asks before guessing:** missing country or seat count triggers a single targeted question, never a default.
- **ROI baseline smoothed to 12 months:** comparable across sources regardless of export length.

---

## Since v3.0 production (May 2026 → current)

V3.0 was rebuilt around OpenAI's GPT-5.4 cookbook patterns and tested through 30 production passes. Each pass solved a specific failure mode caught in real CSM testing — not theoretical polish. Headlines for the manager:

### New capabilities and modes
- **Step-by-step Configuration Guide** for any named customer workflow (SLA setup, routing, macros) — every step grounded in a Help Center article, customer-input placeholders for things the customer must choose themselves.
- **Strategic Slide Guide** rebuilt as cards, not a deck-title index. Each slide = customer-language headline + content + expected outcome, grouped under phase headers derived from a dependency chain. Talk track on demand only — saves CSM scrolling.
- **App Builder recommendations** automatically proposed when the customer's need matches one of 12 canonical no-code patterns (in-ticket context, external data, agent productivity, CSAT actions).

### Reliability and adherence
- **Centralized stop conditions** so SAGE knows when to ask, when to abstain, when to retry — no more silent over-eager output.
- **Verification loop** runs five silent gates (grounding, packaging, attribution, language, mode contract) before any output. Failed gate blocks output until repaired.
- **Hard cap on broad-narrative searches.** Best-practice and strategy questions now stop after 5 calls — synthesis happens, no more re-query loops.
- **AI Product Truth source override** so SAGE never cites pre-rollout "Advanced only" articles as packaging truth, even when they rank high in Help Center search.
- **Mixed-input handling.** Multi-paste turns (brief + email + sheet) process in a fixed priority order with a one-line acknowledgment to the CSM — never silently out of order.

### Output quality
- **Recommendations** now follow a Pain → Path → Goal bridge in every "Why It Fits" cell. No marketing language, no consultant-speak, no generic best practices.
- **Sources block** consolidated to one canonical home in the citation rules — no more duplicated end-of-deliverable references.
- **CSM/customer-facing split** clarified across all deliverables. CSM-only metadata (MCPs reached, verify-before-sharing flags, escalations) lives in a separate footer block, never bleeds into customer-facing artifacts.
- **Slide Guide CORE vs SATELLITE classification.** Stock features every account already has (ticket fields, triggers, automations) render as custom diagnostic slides; differentiated capabilities (Copilot, AI Agents, App Builder) pull from the deck. Plan-tier scoped to Suite Growth+ baseline with explicit edge-tier annotations.

### CSM workflow ergonomics
- **No website ask.** SAGE never asks for the customer's website. Industry context is captured silently from the brief, transcript, or shared docs — or skipped without comment.
- **Plan-only ask** when plan is missing. One question, plain line, in the customer's language.
- **Welcome MCP probe** confirms Help Center, Drive, Unleash, and Tavily reachability before the first turn — CSM sees a green/amber/red icon for each.
- **Agent panel parameters confirmed.** `useResponsesApi: on` is now load-bearing — without it, the GPT-5.4 reasoning and verbosity tuning silently drops.

### Datifyer (separate agent, same line)
- **Format routing simplified.** SAGE redirects unsupported data formats with a single canonical message. Datifyer accepts only the QBR Sheet and the Sarnowsky PDF — every other format gets a Help Center-style answer from SAGE instead of a forced handoff.
- **Country hallucination ban** locked. PDF path never infers country from email domain or memory.

### Production hardening
- **Compressed-context graceful degradation.** When LibreChat summarization drops earlier session context, SAGE asks the CSM to paste it back instead of fabricating from training memory.
- **30 commits since v3.0**, each with a tested before/after on a real CSM transcript or Gong brief. Zero behavior regressions in the regression test corpus (PAYPER, Altenar, Naturecan, ACME).
