# Evidence and disclosure policy

## Evidence tiers

| Tier | Sources | Use |
|---|---|---|
| Documented product truth | Public Z2 Help Center | Customer-safe behavior, setup, requirements, limits, and availability |
| Official public corroboration | Zendesk product, pricing, developer, status, and corporate pages retrieved through Tavily | Public facts outside normal Help Center coverage |
| Internally proven or discussed | Unleash, Jira, and direct Slack | Known issues, operational experience, recent changes, implementation leads, and documentation gaps |
| Unverified | Inference, incomplete retrieval, stale or conflicting evidence | Do not present as settled fact |

Marketplace and community content require separate labels. A Zendesk-hosted Marketplace listing can describe a third-party product without establishing native Zendesk behavior. A community post is a lead, not official documentation.

## Claim discipline

Treat each of the following as a product claim requiring evidence from the current turn:

- Feature existence or absence.
- Plan and add-on availability.
- Limits, prices, dates, and rollout conditions.
- Navigation paths, field names, option names, and UI labels.
- Operative verbs such as `pause`, `disable`, `disconnect`, `delete`, or `enable`.
- Clarifying questions that assert how the product behaves.

If the source does not confirm the exact control or action, describe only what it confirms. Never invent a tidy diagnostic or button to make the answer easier.

## Contradictions

When sources disagree, check:

- Publication and last-updated dates.
- Product edition, plan, add-on, locale, rollout cohort, and scope.
- Whether internal material is a confirmed observation, tentative discussion, or work in progress.

Use Z2 as the baseline for customer-facing behavior. A newer official Zendesk page may supplement or supersede older Z2 content within its scope.

More recent internal evidence can show that public documentation is lagging. It does not automatically become a customer commitment. Report the conflict in CSM notes with dates and recommend Support, Product, or an appropriate subject-matter owner when confirmation is required.

Do not silently pick the convenient source.

## Recent and draft Help Center content

Treat an article as potentially pre-release when:

- Its section ID is `4405298897050` or the section name contains `NEW CONTENT FOR REVIEW`, `Draft`, or `Internal review`; or
- Section metadata is unavailable and the article was created or updated within the last 60 days.

For internal CSM output, cite it with a verification warning. For customer-ready output, omit a potentially inaccessible URL unless public accessibility is confirmed. Do not use draft content alone for a definitive packaging promise.

## Negative retrieval

Failure to retrieve an article is not evidence that a capability does not exist.

Use language such as:

> I did not surface dedicated documentation for this in the current search. That does not confirm the capability is unavailable.

Run one targeted rephrase and the applicable next layer. If nothing supports the claim, say `couldn't verify` and recommend the next owner or validation step.

## Customer safety

Keep customer-ready copy free of:

- Slack channel names, messages, links, private content, and employee identities.
- Jira keys, worklogs, internal statuses, and unannounced dates.
- Internal tool names and internal-only documents.
- Other customers' details.
- Speculative roadmap commitments.

Internal evidence may improve the CSM's judgment. Summarize it only in a clearly separated CSM-notes section and minimize unnecessary sensitive detail.
