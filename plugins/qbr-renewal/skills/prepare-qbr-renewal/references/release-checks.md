# Selective release checks

Adapted from whatsnew. Use for newer capabilities, EAP/GA, rollout and conflicting
availability claims. Do not add a general release roundup to every brief.

Search both public Z2 sections, then fetch relevant article bodies:

- What's New `4405298877338`:
  https://support.zendesk.com/hc/en-us/sections/4405298877338-What-s-new-in-Zendesk
- Announcements `4405298833818`:
  https://support.zendesk.com/hc/en-us/sections/4405298833818-Announcements

Discover current tool schemas. Typical tools are `search_z2_articles` (`query`,
`section_ids`, `locale`, `limit`), `get_z2_articles_by_ids` and
`fetch_z2_content_by_url`. Verify section and audience metadata. Snippets do not
substantiate claims. Split capped searches and deduplicate IDs; do not invent
pagination/date filters. Fetch linked public docs for precise requirements.

When current EAP status matters, check the live directory and later announcements:
https://support.zendesk.com/hc/en-us/articles/4408829663642-Current-and-upcoming-Zendesk-early-access-programs-EAPs

Use the archive for historical context, gaps or an explicit user request:
https://docs.google.com/presentation/d/1UG6cBxpmZxvjo0Nm4BoHGlm27BG5YVu_k71UqbqMaiQ/edit

Inspect its live outline and relevant ranges; never hard-code month positions.
Return to Z2 to verify material archive discoveries. Unconfirmed findings stay
internal and labelled “public confirmation not found.” Publicly resolved simple
questions need no archive lookup.

Distinguish announcement, rollout, kit month and article edit date. An old EAP
label does not prove a current EAP; later GA evidence may supersede it. General
availability does not prove this customer's access or activation. Preserve plan,
channel, language and phased-rollout conditions. Cite individual public articles.
Do not automatically expand into Slack, Unleash, other decks or general web search.
