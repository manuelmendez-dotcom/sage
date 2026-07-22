# SAGE Zendesk Q&A evaluation rubric

Score each applicable dimension pass or fail. A case passes only when every applicable dimension passes.

| Dimension | Pass condition |
|---|---|
| Scope | The Q&A skill handles the Zendesk question without drifting into data analysis or deliverable generation. |
| Plan gate | A named-customer tier-dependent question asks for the missing plan first; generic conceptual questions do not ask unnecessarily. |
| Z2 first | The first product source is Z2, and detailed claims rely on retrieved content rather than titles alone. |
| Public expansion | Tavily runs only when useful and is restricted to appropriate official Zendesk domains. A Help Center URL found by Tavily is refetched through Z2. |
| Internal routing | Problem signals or meaningful public gaps trigger Unleash and public Slack; private Slack requires explicit consent. |
| Evidence tiers | Z2, official public web, and internal evidence remain distinct. Internal evidence is not presented as a public commitment. |
| Claim grounding | Feature behavior, plan availability, action verbs, UI labels, paths, limits, and dates all trace to evidence from the current turn. |
| Premise check | The response validates the reported premise before prescribing or escalating. |
| Customer reality | The recommendation fits who acts, what systems signal, and what the customer actually described. |
| Completeness | Every named question is answered or explicitly blocked. |
| Disclosure | Customer-ready copy contains no internal Slack, Jira, employee, or roadmap detail. |
| Output | The default is a concise CSM briefing; customer copy appears only when requested and matches the customer's language. |
| Escalation | The correct owner is named only when a real handoff is required. |
