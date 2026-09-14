# Evidence and disclosure policy

Evidence authority does not change when the user changes search order. Classify every supplied, prior-turn, or newly retrieved item before using it.

## Evidence tiers

| Tier | Sources | Safe use |
|---|---|---|
| Documented product truth | Public Z2 Help Center content | Customer-safe behavior, setup, requirements, limits, and availability |
| Official public corroboration | Zendesk product, pricing, developer, status, and corporate pages retrieved through Tavily | Public facts outside normal Help Center coverage |
| Community evidence | Original Zendesk Community discussions and replies with visible dates and author roles | Comparable cases, experience, and possible workarounds; validate current product claims against permitted official documentation |
| Internal operational evidence | Unleash, Jira, direct Slack | Known issues, operational experience, recent changes, decisions, and documentation gaps |
| Internal engineering evidence | Zendeskdev and engineering material surfaced through internal sources | Architecture, runbooks, incidents, implementation constraints, and technical discovery |
| Internal enablement evidence | Google Drive decks, playbooks, examples, and positioning | CSM framing, talk tracks, examples, and recommendation context |
| Unverified | Unclear provenance, incomplete retrieval, unsupported inference, stale or conflicting evidence | Do not present as settled fact |

Marketplace and community content require separate labels. A Zendesk-hosted Marketplace listing can describe a third-party product without establishing native Zendesk behavior. A community post is a lead, not official documentation.

Community AI overviews are discovery aids, not independent sources. Retrieve the underlying discussions before relying on them. Accepted-answer status, likes, and employee badges do not by themselves establish current product behavior. Preserve later corrections and distinguish suggestions from reported results. Public Community content is customer-accessible evidence, but restricted authenticated content must not be presented as public. See [community-research.md](community-research.md).

## Supplied and prior-turn evidence

Supplied evidence inherits authority only when its provenance is clear enough to classify. A pasted Slack thread remains internal conversational evidence. A pasted Z2 excerpt is customer-safe only when its article identity and public accessibility are known. Material with unknown origin remains unverified.

Reuse prior-turn evidence when:

- The relevant content remains visible or recoverable in the active conversation.
- Its source and audience tier are known.
- It directly supports the current claim.
- Its date and scope remain suitable for the decision.

Retrieve again only when the content is incomplete, freshness materially matters, sources conflict, public accessibility is unknown and load-bearing, or the user requests a fresh check.

Record each item in the evidence ledger with its origin: `supplied`, `current search`, or `prior turn`. Do not describe reused evidence as newly validated.

## Claim discipline

Treat each of the following as a product claim requiring appropriate evidence:

- Feature existence or absence.
- Plan and add-on availability.
- Limits, prices, dates, and rollout conditions.
- Navigation paths, field names, option names, and UI labels.
- Operative verbs such as `pause`, `disable`, `disconnect`, `delete`, or `enable`.
- Clarifying questions that assert how the product behaves.

If the evidence does not confirm the exact control or action, describe only what it confirms. Never invent a tidy diagnostic or button to make the answer easier.

Internal or enablement evidence can shape CSM judgment, identify a validation path, or explain uncertainty. It cannot independently support a definitive customer-facing product or packaging claim.

## Contradictions

When sources disagree, check:

- Publication, modification, retrieval, and discussion dates.
- Product edition, plan, add-on, locale, rollout cohort, and scope.
- Whether internal material is a confirmed observation, tentative discussion, or work in progress.
- Whether a deck or talk track is positioning rather than product documentation.

Use public Z2 as the baseline for customer-facing behavior. A newer official Zendesk page may supplement or supersede older Z2 content within its scope.

More recent internal or engineering evidence can show that public documentation is lagging. It does not automatically become a customer commitment. Report the conflict in CSM notes with dates and recommend the appropriate owner when confirmation is required.

Do not silently pick the convenient source.

## Recent and draft Help Center content

Treat an article as potentially pre-release when:

- Its section ID is `4405298897050` or the section name contains `NEW CONTENT FOR REVIEW`, `Draft`, or `Internal review`; or
- Section metadata is unavailable and the article was created or updated within the last 60 days.

For internal CSM output, cite it with a verification warning. For customer-ready output, omit a potentially inaccessible URL unless public accessibility is confirmed. Do not use draft content alone for a definitive packaging promise.

## Negative retrieval

Failure to retrieve evidence is not evidence that a capability does not exist.

Use language such as:

> I did not surface dedicated documentation for this in the permitted search. That does not confirm the capability is unavailable.

Run one targeted rephrase within the selected mode. If nothing supports the claim, say `couldn't verify` and identify the next validation source or owner without silently widening the search.

## Customer safety

Keep customer-ready copy free of:

- Slack channel names, messages, links, private content, and employee identities.
- Jira keys, worklogs, internal statuses, and unannounced dates.
- Zendeskdev content, engineering architecture, internal runbooks, and incident mechanics.
- Internal Google Drive links, deck names, and internal positioning.
- Other customers' details.
- Speculative roadmap commitments.
- Research-mode and evidence-ledger metadata.

Internal, engineering, and enablement evidence may improve the CSM's judgment. Summarize it only in clearly separated CSM notes and minimize unnecessary sensitive detail.
