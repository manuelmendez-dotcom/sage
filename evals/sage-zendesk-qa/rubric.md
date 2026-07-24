# SAGE Zendesk Q&A evaluation rubric

Score each applicable dimension pass or fail. A case passes only when every applicable dimension passes.

| Dimension | Pass condition |
|---|---|
| Scope | The Q&A skill handles the Zendesk question without drifting into data analysis or deliverable generation. |
| Mode selection | INTERPRET_ONLY takes precedence over SOURCE_DIRECTED, which takes precedence over AUTO; the selected mode matches the user's evidence and instructions. |
| Source constraints | New calls remain inside the exact permitted source set and order; a failure or thin result does not cause silent substitution. |
| Evidence constraints | A search-only lock permits relevant prior evidence, while an instruction to base the answer only on a source excludes other-source evidence from the conclusion. |
| Evidence reuse | Relevant supplied or prior-turn evidence is reused and identified accurately; sources are re-queried only for a material gap, freshness need, conflict, public-status check, or explicit fresh validation. |
| Plan gate | The skill gates a plan-dependent conclusion rather than interpretation or permitted research; AUTO stops first only when the entire named-customer answer materially depends on the missing plan. |
| AUTO public routing | In AUTO mode, the first public product source is Z2, and detailed claims rely on retrieved content rather than titles alone. Interpret-only and source-directed work is not forced through Z2. |
| Public expansion | Tavily runs only when useful and is restricted to appropriate official Zendesk domains. A Help Center URL found by Tavily is refetched through Z2 when AUTO mode or the permitted source set allows Z2. |
| Internal routing | AUTO mode uses the internal source best matched to the signal and adds another only for a distinct gap; private Slack requires explicit consent. |
| Evidence tiers | Public product, official public, internal operational, internal engineering, enablement, and unverified evidence remain distinct regardless of search order. |
| Authority invariance | A user-selected source or source lock never promotes internal, engineering, conversational, or enablement evidence into customer-safe product truth. |
| Claim grounding | Feature behavior, plan availability, action verbs, UI labels, paths, limits, and dates trace to suitable supplied, prior-turn, or newly retrieved evidence in the active conversation. |
| Solution feasibility | A custom or non-native implementation is presented as an option only when its write path, prerequisites, and architecture are verified; otherwise it is labeled technical discovery. |
| Premise check | The response validates the reported premise before prescribing or escalating. |
| Customer reality | The recommendation fits who acts, what systems signal, and what the customer actually described. |
| Completeness | Every named question is answered or explicitly blocked. |
| Disclosure | Customer-ready copy contains no internal Slack, Jira, Zendeskdev, engineering, Google Drive, enablement, employee, incident, runbook, or roadmap detail. |
| Search economy | The skill uses the smallest sufficient set, avoids ritual repeat searches, and respects the mode-specific call budget. |
| Output | The default is a concise CSM briefing; requested or promised customer copy appears in the same response and matches the customer's language. |
| Research scope | CSM-facing output discloses the mode, sources newly used, reused evidence when material, and active source constraint; customer-ready copy excludes this metadata. |
| Escalation | The correct owner is named only when a real handoff is required. |
