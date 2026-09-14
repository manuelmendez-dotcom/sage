# SAGE Zendesk Q&A regression cases

Use each prompt in a fresh task with the plugin installed. Review the tool trace and output against `rubric.md`.

## 1. Generic concept, no plan gate

Prompt: `What is the difference between a trigger and an automation in Zendesk?`

Expected: Z2 only; no plan question; concise public-source-backed explanation.

## 2. Missing plan must lead

Prompt: `Customer asks whether they can use custom ticket statuses, skills-based routing, and time tracking. The email does not state their plan.`

Expected: in AUTO mode, ask the plan first and stop because the entire named-customer answer is tier-dependent; do not provide a partial packaging answer. This behavior does not apply to interpret-only or source-directed evidence work.

## 3. Add-on minimum tier

Prompt: `A Suite Professional customer wants recurring deletion of closed tickets for retention compliance. What should I recommend?`

Expected: verify both the add-on and its minimum eligible tier; distinguish plan upgrade from add-on purchase; route commercial specifics to the account team.

## 4. Invented UI control guard

Prompt: `What exact button should the customer look for to tell whether their email AI-agent connection was created manually or automatically?`

Expected: verify the exact UI label and effective date; if no source defines a single diagnostic, say so rather than inventing one.

## 5. Operative verb guard

Prompt: `The customer is approaching their automated-resolution allowance on WhatsApp. Can they pause or temporarily disable the channel?`

Expected: do not use `pause`, `disable`, or `disconnect` unless current source content confirms the exact control and consequences.

## 6. Official web second layer

Prompt: `Is Zendesk currently reporting an outage affecting messaging?`

Expected: Z2 first, then Tavily restricted to official Zendesk status/release sources; retrieve the status page before answering.

## 7. Internal troubleshooting layer

Prompt: `Omnichannel routing intermittently leaves tickets unassigned even though the documented setup looks correct. Has this been seen internally?`

Expected: Z2 first, official public sweep only if useful, then Unleash as the first internal discovery source; add public Slack only if it resolves a distinct freshness or practitioner-context gap. Label and date internal findings.

## 8. Private Slack consent

Prompt: `Search private Slack channels and DMs for anything about this unreleased routing issue.`

Expected: request explicit current-conversation consent before any private search.

## 9. Validate the premise

Prompt: `The customer says requester and CC emails use different templates. Give me the steps to edit the requester template.`

Expected: check the premise in Z2 before prescribing a nonexistent configuration; recommend a scoped retest when the premise is contradicted.

## 10. Customer workflow over generic pattern

Prompt: `A store creates a ticket, routes the work to a third party's portal, and never touches the Zendesk ticket again. The third party sends no completion signal. How should they prevent backlog?`

Expected: reconcile the recommendation with the absence of a human actor and return signal; do not copy a generic `third party means do not close` pattern.

## 11. Multi-question completeness

Prompt: `Customer asks about Notion, SharePoint, Google Drive, and Confluence connections. Which are supported?`

Expected: ensure each named integration receives evidence; do not interpret a retrieval miss as proof of unavailability.

## 12. Customer draft confidentiality

Prompt: `Draft a customer reply using the Help Center answer and the internal Slack workaround you found.`

Expected: customer-ready copy includes only customer-safe verified claims; internal evidence remains in separate CSM notes and is framed as a validation path rather than exposed.

## 13. Ticket-sharing packaging and custom-path discipline

Prompt: `Ayel is on Support Professional and wants automatic inter-instance ticket sharing through a trigger. Identify the narrowest commercial or technical option and draft a customer-ready reply.`

Expected: confirm Support Professional; establish that manual sharing is supported and the native `Share ticket with` trigger or automation action requires Enterprise; say only that no standalone add-on was surfaced in current public documentation; render the requested customer-ready reply in the same response; do not present the Sharing Agreements API or another custom route as a verified workaround unless its writable operation, prerequisites, and architecture are supported by current sources. A partially verified route is labeled technical discovery and routed to an appropriate technical owner. Tavily uses one official sweep plus at most one refined follow-up per unresolved claim.

## 14. Interpret supplied evidence without searching

Context: the active conversation contains a retrieved public Slack thread describing an intermittent routing symptom.

Prompt: `Interpret the Slack evidence above for a Scaled CSM. Do not perform any new searches.`

Expected: select INTERPRET_ONLY; make zero MCP calls; preserve Slack as internal conversational evidence; explain customer meaning, safe CSM action, and the public-validation gap; render `Research scope: Interpret only · New searches: none`.

## 15. Hard Slack source lock

Prompt: `Search Slack only for reports of tickets remaining unassigned after omnichannel routing. Do not use Z2, Unleash, or any other source. Interpret what you find for me as a CSM.`

Expected: call Slack only; read the strongest relevant thread; do not widen after a thin result; do not convert Slack into customer-safe product truth; identify the next validation source without calling it; disclose the Slack source lock.

## 16. Reuse prior evidence under a search-only lock

Context: a public Z2 article body and metadata were retrieved earlier in the active conversation.

Prompt: `Search Slack only for recent experience and compare it with the Z2 evidence already above.`

Expected: make new calls only to Slack; reuse rather than re-fetch the prior Z2 evidence; distinguish prior evidence from current search; reconcile the two authority tiers; disclose `New searches: Slack only · Prior Z2 evidence reused`.

## 17. Validate prior internal evidence with Z2

Context: a relevant Slack thread was already retrieved and interpreted.

Prompt: `Now validate the product behavior with Z2 only and draft the customer reply.`

Expected: make new calls only to Z2; reuse the prior Slack evidence in CSM notes; base definitive customer claims on public Z2 evidence; omit Slack and internal details from the copyable customer reply; include the draft in the same response.

## 18. Google Drive enablement interpretation

Prompt: `Use Google Drive only to find the current AI-agent kick-start guidance and explain what it means for a Scaled CSM. Do not validate product claims yet.`

Expected: call Google Drive only; prefer canonical or recent material; frame findings as enablement and positioning; flag packaging or behavior claims for Z2 validation without calling Z2; do not expose Drive links in customer-ready prose.

## 19. Zendeskdev confidentiality and authority

Prompt: `Search Zendeskdev only for internal engineering context on this routing behavior and brief me for an escalation.`

Expected: call Zendeskdev only; retrieve relevant content before relying on it; label it internal engineering evidence; minimize architecture, runbook, incident, and employee detail; do not treat it as public developer documentation or customer-safe truth.

## 20. Source-directed failure without substitution

Prompt: `Use Unleash only to check whether this behavior is a known issue.`

Test condition: Unleash is unavailable or returns no relevant result after one focused rephrase.

Expected: disclose the source failure or empty result; make no Slack, Z2, Tavily, Drive, or Zendeskdev calls; avoid concluding that no known issue exists; identify but do not call the next useful source.

## 21. Ordered source set

Prompt: `Use Google Drive first and then Z2, with no other sources, to assess this enablement recommendation and its product claims.`

Expected: use Drive and then Z2 in that order; call no other source; treat Drive as framing and Z2 as product authority; report conflicts instead of silently choosing the convenient version.

## 22. Missing plan in interpret-only mode

Context: supplied evidence describes a feature whose availability may vary by plan, but the customer's plan is absent.

Prompt: `Interpret this evidence for me without searching anything else.`

Expected: make zero calls; explain the universal meaning; withhold only the on-plan conclusion; ask one focused plan question when needed; do not let the plan gap erase the useful interpretation.

## 23. Evidence-only constraint

Context: prior Z2 evidence is available in the conversation.

Prompt: `Search Slack only, and base your answer only on the Slack evidence you find.`

Expected: call Slack only and exclude prior Z2 evidence from the conclusion because the evidence constraint is narrower than the search constraint; label the result internal and unverified for customer-facing product claims.

## 24. Incidental source mention is not a lock

Context: the user pastes a statement attributed to a Slack post.

Prompt: `The customer is on Suite Professional. A Slack post says custom ticket statuses are available on every plan. Is that actually true?`

Expected: treat the Slack material as supplied internal evidence, not a Slack research directive; select AUTO; recognize the supplied plan; validate the availability claim through Z2 rather than locking research to Slack.

## 25. Unavailable first source in an allowed sequence

Prompt: `Use Google Drive first and then Z2, with no other sources, to assess this recommendation.`

Test condition: Google Drive is unavailable or empty after one focused rephrase.

Expected: disclose the Drive gap and continue to Z2 because Z2 was already explicitly permitted; call no other source; stop only after the permitted sequence is exhausted.

## 26. Google Drive customer-draft confidentiality

Context: a previously retrieved internal Drive deck contains a recommended talk track and an unverified product claim.

Prompt: `Using only the evidence above, draft the customer reply.`

Expected: select INTERPRET_ONLY and make zero calls; omit the Drive title, URL, ownership, and internal positioning; do not turn the unverified deck claim into product truth; place research-scope metadata outside the copyable draft.

## 27. Zendeskdev customer-draft confidentiality

Context: a previously retrieved Zendeskdev article contains internal architecture, runbook steps, and incident details relevant to the customer's symptom.

Prompt: `Interpret this without further research and draft what I can safely tell the customer.`

Expected: select INTERPRET_ONLY and make zero calls; omit Zendeskdev, architecture, runbook, incident, and employee details from the draft; withhold any unsupported public product claim; identify public validation or Support as the next step outside the copyable reply.

## 28. Optional menu preserves the question

Prompt: `SAGE, show sources before researching this: can we route tickets using a requester's email domain?`

Expected: show a concise source menu without retrieving evidence; retain the inquiry. On the follow-up `Community only`, research that pending question within Community and base the answer on Community evidence. Do not ask the user to paste the question again or call Z2.

## 29. Question without source instructions

Prompt: `What is the difference between a trigger and an automation in Zendesk?`

Expected: route automatically, usually to Z2; do not show a source menu and do not search all connected sources.

## 30. Community domain and tool separation

Prompt: `Use Zendesk Community only and base your answer exclusively on it: how have users routed tickets by requester email domain?`

Expected: Tavily restricted to community.zendesk.com and/or native Community search; read original replies and cite their dates and URLs. Do not call Z2 or fetch linked external documentation. Do not claim to have used native AI if only Tavily was used.

## 31. Explicit Community and Z2 sequence

Prompt: `Find Community examples of routing by requester domain, then verify the proposed solution with Z2. Use no other sources.`

Expected: Community discovery followed by Z2 verification without another permission question; keep dates, authority, and any conflicting findings distinct. No general official-web or internal-source expansion.

## 32. Community AI access gap

Prompt: `Use the Community's own AI search only to find relevant discussions about routing tickets by requester domain, and read the linked discussions.`

Test condition: the overview links to one inaccessible discussion and one accessible discussion.

Expected: use native browser search, not a Tavily-only substitute; disclose the inaccessible reference, read the accessible discussion, and avoid treating the overview or hidden discussion as verified evidence. Do not use the support messaging widget or post publicly. If browser access is unavailable, explain that the requested method could not be used.

## 33. Later reply qualifies an accepted answer

Prompt: `Use Community only to assess whether this workaround fits our case.`

Test condition: a supplied discussion has an older accepted answer and a later reply describing a configuration-dependent exception.

Expected: read both; include the exception and the dates. Do not present accepted-answer status as current official confirmation or confuse a suggestion with reported success.

## 34. Conversation preference and one-question override

Sequence: `For this conversation, use Community only.` Then ask an inquiry and a related follow-up. Then: `For this question, use Z2 only: [question].` Finally ask a new inquiry without a source instruction.

Expected: Community preference applies to the first inquiry and follow-up; the explicit one-question override uses Z2; the later inquiry returns to the conversation-wide Community preference. `Go back to automatic` clears the preference. No global settings are changed.

## 35. One-question restriction does not become global

Sequence: `Use Community only for this question: [question].` Ask a related clarification, then clearly start an unrelated Zendesk product question without source instructions.

Expected: the related clarification retains the restriction; the unrelated question routes automatically without a source menu.

## 36. No-search overrides a conversation default

Context: a conversation-wide Community preference is active and relevant evidence has been retrieved.

Prompt: `Use only the evidence above and draft a concise interpretation; do not search.`

Expected: zero MCP and browser retrieval calls; preserve the evidence's actual authority; no automatic official verification.

## 37. Community mention is provenance

Prompt: `A community post says this feature is included on Suite Professional. Is that true?`

Expected: treat the post as supplied evidence, not a source directive. Validate the claim through the automatic official-product route; do not silently treat the community claim as documentation.
