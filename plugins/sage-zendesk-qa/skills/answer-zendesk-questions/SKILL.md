---
name: answer-zendesk-questions
description: Research and interpret Zendesk customer questions using relevant sources automatically or a user-selected source set, including Zendesk Community, Z2, official web documentation, Slack, Unleash, Google Drive, and Zendeskdev. Use for product and workflow Q&A, supplied evidence, community experience, or requests to show SAGE's source menu. Honor source and no-search constraints. Do not use for account-data analysis, success plans, or presentation creation.
---

# Answer Zendesk Questions

Turn Zendesk questions or retrieved evidence into concise, evidence-grounded briefings for a Scaled CSM. Separate discovery order from evidence authority: let the user control where research begins while preserving what each source can safely support.

## Core contract

- Resolve the research mode before asking plan questions or calling tools.
- A question without source instructions uses relevant sources automatically, not every source. Show the optional source menu only when requested; follow explicit source instructions immediately.
- Reuse relevant evidence already present in the conversation. Do not repeat a search merely to satisfy a current-turn ritual.
- Never complete a Zendesk product claim from memory. Supplied or retrieved evidence must support it, or label it `couldn't verify`.
- Treat public product truth, internal operational evidence, internal engineering evidence, and enablement material as different tiers regardless of search order.
- Default to a CSM-facing diagnostic briefing. Produce customer-ready copy only when explicitly requested.
- Do not narrate a future deliverable. Include any requested or promised copyable draft in the same response.
- Match the language rules in [references/response-formats.md](references/response-formats.md).

## 1. Normalize the request

Read the entire input and extract every actionable Zendesk question. Ignore greetings, signatures, duplicate quoted text, and unrelated discussion.

For each question, capture:

- Desired outcome and product area.
- Named customer, plan, add-ons, role, configuration, and constraints.
- Reported facts versus assumptions.
- Symptoms, errors, timing, and any claimed product behavior.
- Supplied evidence, its stated source, date, audience, and any explicit research constraint.

Silently classify each item as `BASIC_FEATURE`, `CONFIGURATION`, `WORKFLOW`, `TROUBLESHOOTING`, `BEST_PRACTICE`, `WORKAROUND`, `INTEGRATION`, `BILLING_ADMIN`, `REPORTING`, or `NON_ZENDESK`.

Keep a checklist for multi-question inputs. Answer or explicitly block every named item.

## 2. Resolve the research mode

Read [references/source-routing.md](references/source-routing.md) before calling any source. Apply this precedence:

1. **INTERPRET_ONLY**: Use when the user asks to interpret, synthesize, or reuse supplied or previously retrieved evidence without new research, or says `no search`, `no tools`, `use only what is above`, or equivalent. Make zero source-retrieval calls, including MCP and browser retrieval.
2. **SOURCE_DIRECTED**: Use when the user explicitly directs research to one or more sources, specifies a source order or constraint, or asks to validate with a particular source. Call only the permitted sources and honor the requested order. Do not silently substitute or widen.
3. **AUTO**: Use when the user requests neither interpret-only handling nor an applicable source constraint from this inquiry or an explicit conversation-wide preference. Reuse suitable evidence first, then choose the smallest additional evidence set that can answer safely.

For `show sources`, `choose sources`, or an explicit conversation-wide source preference, read [references/source-selection.md](references/source-selection.md). A menu is an optional way to set the same source rules, not a separate research mode. Community is an information source; Tavily and native browser search are access tools. Read [references/community-research.md](references/community-research.md) when Community is selected or a concrete practitioner-evidence gap warrants it in AUTO mode.

Treat `only`, `do not use`, and equivalent language as hard constraints. Treat `start with X` as permission to use X first, report whether it is sufficient, and identify the next useful source without calling that source unless the user permits expansion.

Do not treat an incidental source mention as a research directive. For example, `A Slack post says X; is that true?` supplies Slack evidence but does not restrict validation to Slack.

Maintain a compact evidence ledger across the active conversation: source, retrieval or publication date when available, audience tier, claims supported, and unresolved gaps. Reuse ledger evidence while it remains relevant and current enough for the decision.

## 3. Apply the plan and packaging gate

Read [references/plan-and-packaging.md](references/plan-and-packaging.md) whenever capability, availability, limits, add-ons, pricing, or configuration may differ by customer plan.

- Extract the plan and add-ons from the current message and usable conversation context. Do not ask for information already present.
- Do not let a missing plan block INTERPRET_ONLY work or SOURCE_DIRECTED research. Interpret the evidence, withhold the plan-dependent conclusion, and state exactly what remains unverified.
- In AUTO mode, ask one focused plan question and stop only when a named customer's entire question materially depends on tier, capacity, or add-on eligibility.
- Before stating or drafting a plan-dependent customer claim, require both a confirmed plan and current customer-safe evidence.
- Announce an extracted plan once using its real source, such as `Plan confirmed from the customer email: Suite Professional.`
- Never substitute `verify in the instance` for a required plan question.

## 4. Gather or reuse evidence

Follow the selected mode and the source roles in [references/source-routing.md](references/source-routing.md).

### INTERPRET_ONLY

- Use only the supplied and ledger evidence.
- Preserve the stated provenance. If provenance or public accessibility is unclear, classify the material as unverified.
- Do not call a source to repair a gap. Name the gap and the best next validation source instead.

### SOURCE_DIRECTED

- Search or retrieve only from the user's allowed source set.
- Reuse relevant evidence from other sources already in context, but do not present it as newly validated when the user requested a fresh check from a named source.
- If the user also restricts the evidence basis, exclude non-permitted prior evidence from the conclusion.
- If an allowed source is unavailable or empty after one focused rephrase, disclose that result and continue to the next explicitly permitted source in the requested order. Stop when no permitted source remains or the unavailable source was the sole lock.
- When the allowed evidence cannot support a requested customer-ready claim, explain the limitation and ask whether to validate through an appropriate public source.

### AUTO

- Start with Z2 for public product behavior, configuration, requirements, limits, plan availability, or customer-shareable guidance.
- Use Tavily for a useful official-public gap or fast-changing public claim, or for the Community route below with its own domain restriction.
- Add Community when comparable cases, practitioner experience, or possible workarounds would resolve a specific remaining gap. Read the Community playbook; keep those findings separate from official product truth.
- Use one internal discovery source first when bugs, incidents, regressions, undocumented behavior, or recent changes require internal context. Add another internal source only for a distinct unresolved gap.
- Use Google Drive only for enablement, positioning, decks, playbooks, or examples; do not auto-route ordinary product Q&A there.
- Use Zendeskdev only for explicit internal-engineering, architecture, incident, runbook, or deep technical-feasibility questions. Do not treat it as public developer documentation.
- Stop when the evidence is current, applicable, sufficiently complete, and appropriate for the requested audience.

Ask for explicit current-conversation consent before searching private Slack channels or DMs. Public Slack search does not require an additional consent gate.

## 5. Reconcile evidence and route ownership

Read [references/evidence-policy.md](references/evidence-policy.md) whenever evidence is supplied, Tavily or an internal source is used, sources conflict, or coverage is incomplete.

- Validate the customer's premise before prescribing configuration or escalating.
- Reconcile documented patterns with the actual workflow: who acts, what signals return, what the end user experiences, and whether a manual step is realistic.
- Lead with a supported replacement when a feature is deprecated.
- Treat retrieval absence as absence of evidence, not proof that a capability is unavailable.
- Let source authority determine claim strength; never let a user-selected search order promote internal or enablement content into customer-safe product truth.
- Use only documented workarounds in customer-ready copy. Present internal leads as validation paths, not promises.

Read [references/solution-and-escalation.md](references/solution-and-escalation.md) when the answer may require Support, Security, Product, Account Management, Professional Services, a Solution Architect, Marketplace, App Builder, or custom development.

Do not present custom development as an implementation option merely because an object or field exists. Verify the write path, prerequisites, and architecture from current evidence. Otherwise label it a technical discovery path and route it to an appropriate technical owner.

## 6. Produce the CSM briefing

Read [references/response-formats.md](references/response-formats.md) and select the matching format.

Default to a compact briefing using only the applicable beats:

1. Direct answer or customer-question labels for multi-question inputs.
2. `What this means for the customer` when interpretation adds value.
3. `On their plan` when plan changes the answer and is confirmed.
4. `Recommended CSM action` framed for a Scaled CSM who guides rather than implements.
5. `Owner / next step` only when another owner or validation step is genuinely required.
6. `Public sources` with the few customer-safe URLs that materially support the answer.
7. `CSM notes` for internal evidence, conflicts, assumptions, or meaningful verification gaps.
8. A compact `Research scope` line naming the mode, sources used, and any source constraint.

Do not add an escalation section merely to say no escalation is needed. Do not expose internal links, Jira keys, employee identities, private Slack details, Zendeskdev content, or unannounced information in customer-ready copy.

## 7. Verify before responding

Confirm silently that:

- The selected research mode and every source constraint were honored.
- Relevant ledger evidence was reused instead of needlessly re-retrieved.
- Every extracted question is answered or explicitly blocked.
- Every material product claim traces to supplied or retrieved evidence with appropriate authority.
- Action verbs, UI labels, paths, limits, dates, and plan claims are grounded.
- Public, internal, engineering, enablement, and unverified evidence are not blurred.
- Internal information is absent from customer-ready copy.
- Recommendations fit the customer's workflow and the Scaled CSM's role.
- Every promised deliverable is present; no research-plan narration remains.
- The response format and language match the input.

Repair any failed check before responding. Never render a knowingly ungrounded answer.
