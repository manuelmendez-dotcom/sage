# SAGE Zendesk Q&A regression cases

Use each prompt in a fresh task with the plugin installed. Review the tool trace and output against `rubric.md`.

## 1. Generic concept, no plan gate

Prompt: `What is the difference between a trigger and an automation in Zendesk?`

Expected: Z2 only; no plan question; concise public-source-backed explanation.

## 2. Missing plan must lead

Prompt: `Customer asks whether they can use custom ticket statuses, skills-based routing, and time tracking. The email does not state their plan.`

Expected: ask the plan first and stop; no search or partial packaging answer.

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

Expected: Z2 first, official public sweep if useful, then complementary Unleash and public Slack searches; internal findings clearly labeled and dated.

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
