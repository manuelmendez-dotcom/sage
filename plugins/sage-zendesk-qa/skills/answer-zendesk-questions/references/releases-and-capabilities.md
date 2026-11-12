# Releases, capabilities and EAPs

Use for feature recommendations tied to an objective, recent changes, historical announcements, rollout dates, and EAP status. Respect the source mode: a no-search request remains no-search, and a closed set without official documentation cannot establish current official availability.

## Public Updates map

[Zendesk updates](https://support.zendesk.com/hc/en-us/categories/4405298749210-Zendesk-updates) is a category that groups these sections. Use its ID to scope discovery, not as evidence for a feature claim.

| Section | ID | Best use |
|---|---|---|
| [What's new](https://support.zendesk.com/hc/en-us/sections/4405298877338-What-s-new-in-Zendesk) | 4405298877338 | Monthly discovery summaries and links to detailed announcements |
| [Announcements](https://support.zendesk.com/hc/en-us/sections/4405298833818-Announcements) | 4405298833818 | Feature launches, availability, rollout windows, deprecations and EAP notices |
| [Release notes](https://support.zendesk.com/hc/en-us/sections/4405298847002-Release-notes) | 4405298847002 | Product-specific improvements and fixes in a period |
| [Developer updates](https://support.zendesk.com/hc/en-us/sections/4405298889242-Developer-updates) | 4405298889242 | API/platform changes and developer announcements |
| [Service notifications](https://support.zendesk.com/hc/en-us/sections/4405298854426-Service-notifications) | 4405298854426 | Service-impacting changes and operational notices |

These IDs were checked on 2026-11-12. If a section stops resolving, retrieve the category's section map once rather than guessing a replacement.

## Efficient retrieval

1. Identify the product, desired outcome and requested period. For a known feature, search its exact name. For an open-ended recommendation, use the relevant product and objective, with a recent window appropriate to the question; state any material time assumption.
2. Use `search_z2_articles` with `category_ids: [4405298749210]` or the relevant `section_ids`. Start with a small result limit such as 5–10. The tool has no exposed date-range filter; include useful month/year terms and check dates in the actual content. Do not invent filter parameters.
3. Read the strongest detailed announcement and relevant current product documentation. For a long monthly summary or release-note article, get its TOC and only the relevant sections, then follow the material linked announcement. Inspect audience metadata before treating the article as public.
4. Use Release notes for a relevant improvement/fix gap and Announcements for availability. Do not query every section for every recommendation. Avoid fetching a whole section URL to list candidates: it can return many full article bodies.
5. Stop once the feature, important limitation, status and applicability are supported. Reuse fresh relevant evidence already in the conversation.

A focused Updates check is part of capability recommendations even if an older how-to article already seems to answer the question. Match the objective to what a feature actually does; similar names are insufficient. Before proposing custom development, check for a recent native capability. If no relevant update is found, report only that bounded result, not that no new feature exists.

## Dates and availability

Distinguish the announcement/publication date, stated rollout start/end, monthly summary period, article edit date, and retrieval date. `updated_at` or `edited_at` is not a release date. A completed global rollout window does not prove that a particular customer's configuration or subscription is eligible.

For current availability, prefer the current feature documentation plus the relevant announcement over an old summary. When sources differ, compare edition, channel, prerequisites, cohort and dates before claiming a contradiction. Gate only customer-specific eligibility on a confirmed plan; a missing plan does not prevent explaining a launch or researching suitable candidates.

For EAP questions, consult the [current and upcoming EAP directory](https://support.zendesk.com/hc/en-us/articles/4408829663642-Current-and-upcoming-Zendesk-early-access-programs-EAPs), the feature's announcement, and subsequent official updates when needed. Distinguish announced EAP, enrollment open, closed, GA, and discontinued. An old invitation or an internal Slack discussion does not prove enrollment is still open. Preserve an unresolved status if current evidence is missing.

## Historical coverage

For a requested period, split broad discovery by product, month or section as needed, and inspect the dates in retrieved originals. The search tool returns at most 100 results and exposes no pagination or date filter; a section response's `count` does not establish the total archive size. Do not claim an exhaustive release inventory from one query, a monthly summary, or a section dump. Explain meaningful coverage limits, especially for `all releases` requests.

Public official web search can fill an index gap if permitted. Drive archives and internal engineering material are outside this route. Internal sources are useful only for a separate unresolved internal context question, not as substitutes for a public launch or availability statement.

Use a compact feature/date/status/implication/source table when comparing several releases; one feature usually needs a short paragraph. Keep the announcement date and rollout window in separate fields when they differ.
