# SAGE & Datifyer — What Changed and Why We're Ready

*Internal brief for leadership — June 2026*

## Executive summary

**The problem.** SAGE and Datifyer worked, but they weren't consistent or efficient enough to put in front of customers with confidence. The agents searched more than they needed to — pulling from multiple knowledge sources by default and running redundant lookups — which made them slower and wasteful. Their output varied run to run, sometimes padded with generic language not tied to what the customer actually said. Most critically, Datifyer's ROI math could swing up to 3× on the exact same inputs, which meant the numbers couldn't be trusted in a customer conversation. The common thread: the agents needed tighter rails and leaner processes, not more features.

**What we fixed.** We ran regression tests to see how the agents were actually retrieving information, then tightened the rules — fewer, more deliberate searches, a strict order of which source to check first, and a cap on how much we pull from team documents — and re-tested to confirm accuracy held. We rewrote both prompts to align with how our underlying model performs best, which made the agents follow their guardrails far more consistently while spending fewer tokens on low-value work. And we pressure-tested Datifyer's ROI math until it stopped moving, locking the inputs and formulas so the same data now produces the same defensible numbers every time. The result is two agents that behave predictably, stay grounded in the right sources, run leaner, and produce customer-ready output — ready for broader rollout.

---

## The short version

SAGE and Datifyer started as capable but inconsistent. They gave good answers, but not always the *same* answer to the same question, they searched more than they needed to, and they occasionally reached for sources or made claims they shouldn't. Over the last several weeks we ran a focused optimization program — tightening how and when the agents retrieve information, making the prompts more efficient and aligned to how the underlying model works best, and locking down the numbers Datifyer produces. The result is two agents that behave predictably, stay grounded in real Zendesk sources, work leaner, and produce customer-ready output without hand-holding. They're ready for broader rollout.

---

## Why we had to do the work

The original version had three problems that all pointed the same direction — **the agents needed tighter rails and leaner processes, not more capability.**

1. **Retrieval was loose and wasteful.** The agents had access to several knowledge sources (the Help Center, internal systems, team Drive, the public web) and weren't disciplined about which to use when, or how much to pull. That meant extra tool calls, slower answers, wasted processing on low-value work, and occasional reliance on the wrong source.

2. **Delivery was inconsistent.** The way SAGE packaged recommendations, slide guides, and setup instructions varied run to run. Output was sometimes padded with generic best-practice language that wasn't tied to what the customer actually said.

3. **Datifyer's math drifted.** This was the most serious. On identical inputs, the ROI numbers could vary by 3× — a cost-per-ticket that swung wildly, a headline savings figure that landed anywhere across a huge range. Numbers that move on the same input can't be put in front of a customer.

---

## What we changed

### 1. We tightened how and when the agents retrieve information (MCP discipline)

This was a measured effort, not a guess. We ran **regression tests across the agents' knowledge sources** — the Zendesk Help Center, our internal systems, and team Drive — to see how each was actually being used, then tightened the rules accordingly:

- **Stricter firing rules** for when each source is called. The Help Center is always checked first; the others are pulled in only when the question genuinely calls for them, rather than by default.
- **Fewer tool calls per question** — we cut redundant searching so the agents reach an answer in fewer, more deliberate steps. Leaner processes, faster responses.
- **Capped Drive retrieval** so the agents pull only the information they need from team documents instead of large, low-value chunks.
- **Re-ran regressions after tightening** to confirm retrieval quality held up — that pulling less and searching more selectively did not cost us accuracy.

(If a source the answer depends on is unreachable, the agent stops and says so rather than guessing — it fails safely.)

**Why it matters:** the agents do less low-value work, respond faster, and stay grounded in the right source — without sacrificing answer quality.

### 2. We reshaped how SAGE delivers output (delivery modes)

- **Recommendations** now tie every suggestion to something the customer actually said, with a clear Pain → Path → Goal logic. No marketing language, no generic filler.
- **The Strategic Slide Guide** was rebuilt from a flat list of slide titles into structured cards — each with a customer-language headline, content, and the outcome it drives — grouped by logical phase. The CSM gets a usable build plan, not an index.
- **Configuration Guide mode** produces step-by-step setup instructions for a specific customer workflow, with every step grounded in a Help Center article.
- Across all modes, we cleanly separated **customer-facing content from CSM-only notes**, so internal metadata never leaks into something sent to a customer.

**Why it matters:** consistent, customer-ready deliverables that need far less CSM editing.

### 3. We rebuilt the prompts to work the way the model works best

The instructions that drive both agents were rewritten to align with how our underlying model (OpenAI's latest) actually performs best — clearer structure, no contradictory rules, and explicit guardrails the model reliably follows. We did this pass for **both SAGE and Datifyer.**

**Why it matters:** the agents follow their rules far more consistently, adhere to their guardrails, and spend fewer tokens on low-value steps — which means more reliable behavior at a leaner cost per interaction.

### 4. We locked down Datifyer's numbers (the optimization that mattered most)

This was the heaviest engineering effort. We pressure-tested Datifyer's ROI math across more than twenty runs on a real customer dataset until the numbers stopped moving. Key locks:

- **Two trusted inputs only** — the QBR workbook and the official metrics export. Every other file format is politely redirected up front rather than processed unreliably.
- **Fixed cost formula** with named, verified constants and a built-in sanity check that rejects impossible figures.
- **A guardrail on the headline range** so the savings number can't land outside a defensible band.
- **No guessing on critical inputs** — if the country, salary, or seat count is missing or ambiguous, Datifyer asks one targeted question instead of inventing a default. It will never infer a customer's country from an email address or memory.
- **A standardized, three-pillar ROI layout** (Deflection / Productivity / Capacity) in clean, customer-ready formatting.

**Why it matters:** the same inputs now produce the same defensible numbers, every time. That's the difference between a tool the team experiments with and one they can use in front of a customer.

---

## The final product

**SAGE** — the main Customer Success agent. Answers product questions grounded in official Zendesk documentation, analyzes call transcripts, builds customer-language recommendations and slide guides, drafts setup instructions, and writes customer communications. It knows when to ask, when to hold back, and when a source is missing — and it runs every output through a set of silent quality checks before showing it.

**Datifyer** — the data-analysis specialist SAGE hands off to. Turns a customer's QBR workbook or metrics export into a deterministic, customer-ready ROI story. Predictable math, no fabricated inputs, clean formatting.

## Why we're ready now

- Every change was driven by a **real failure caught in testing**, not theoretical polish. Each fix was validated against actual customer transcripts and datasets before it shipped.
- The agents are **predictable** — the same input produces the same trustworthy output, which is the bar for putting anything in front of a customer.
- They **fail safely** — when something's missing or a system is down, they ask or flag rather than guess.
- They **work leaner** — fewer wasted searches and tighter prompts mean faster responses and less effort spent on low-value steps.
- We regression-tested against multiple real customer accounts with **no behavior regressions.**

The work that remains is normal iteration and monitoring, not foundational fixes. The foundation is solid.
