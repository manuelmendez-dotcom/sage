# Source routing

Use the smallest evidence set that can answer the question safely. Preserve this order: Z2, official public web, internal evidence.

## Routing table

| Signal | Sources |
|---|---|
| Basic product concept or universal behavior | Z2 only |
| Configuration how-to without problem signals | Z2; Tavily only if Z2 is thin |
| Plan, packaging, limit, or add-on | Z2; Tavily official pricing/product page when useful |
| Best practice or recommended approach | Z2 first; Tavily official Zendesk material when Z2 lacks sufficient breadth |
| Reporting, Explore, API, webhook, or developer question | Z2; Tavily restricted to official Zendesk developer pages if needed |
| Pricing or public product comparison | Z2 plus Tavily restricted to official product/pricing pages |
| Marketplace or third-party integration | Z2 plus Tavily restricted to official Zendesk Marketplace/product pages |
| Troubleshooting, bug, error, outage, regression, intermittent behavior | Z2; Tavily official status/release sweep; Unleash plus public Slack |
| Z2 and official web conflict or appear stale | Unleash plus public Slack for current internal context |
| Known issue, workaround, recent rollout, or `has anyone solved this?` | Z2 first; then Unleash plus public Slack |
| Clearly non-Zendesk external SaaS needed to answer an integration question | Tavily on the vendor's official documentation after the Zendesk side is checked |

Google Drive is outside this skill.

## Z2 playbook

1. Search with a short product term plus the desired action or symptom.
2. For load-bearing questions, run two variants: feature-specific and capability/intent.
3. Retrieve the strongest content before using procedural or packaging claims.
4. For long articles, inspect the TOC and retrieve only the relevant sections.
5. Verify public status through `user_segment_id` before linking an article to a customer.
6. For multiple named features or integrations, ensure each item receives a targeted search unless an earlier result explicitly covers it.
7. Stop when the public answer is clear, current, applicable, and complete.

Do not rely on titles or snippets for detailed procedures, exact UI controls, or eligibility. Search metadata can establish that a topic exists, but body content must support the actual claim.

## Tavily official-public playbook

Use `search_depth: "fast"` and `max_results: 5` by default. Escalate depth only when the first official sweep is materially thin.

Run one official-domain sweep per unresolved claim. Run at most one refined follow-up when a distinct load-bearing claim remains unresolved; do not chain broad Tavily searches for the same question.

Default official allowlist:

- `support.zendesk.com`
- `www.zendesk.com`
- `developer.zendesk.com`
- `status.zendesk.com`

Use `include_domains`; do not place `site:` in the query. Retrieve the relevant page with Tavily Extract before relying on its content.

Classify results accurately:

- Official product, pricing, developer, status, and corporate pages: official public evidence.
- Community posts: community evidence, not official product truth. Exclude by default unless the user asks for community experience or a workaround requires it.
- Marketplace listings: Zendesk-hosted listings whose product claims may belong to a third-party vendor. Do not treat them as Zendesk-native behavior.

If Tavily surfaces a Help Center URL, fetch it through Z2. This restores Z2 metadata, article content, and public-segment checks.

## Internal playbook

Trigger the internal layer for problem signals or meaningful public gaps. Problem signals include `bug`, `error`, `not working`, `broken`, `intermittent`, `failing`, `conflict`, `stuck`, `outage`, `crash`, `timeout`, `regression`, `no funciona`, `falla`, `roto`, `intermitente`, `bloqueado`, and `caída`.

### Unleash

- Search with the feature plus symptom or operational concept.
- Use `include_jira: true` for suspected bugs, incidents, regressions, roadmap/status questions, and known issues.
- Default to five results. Increase only for genuinely broad or thin searches.
- Prefer results from the last 12 months. Use older material only when it specifically matches a long-standing issue.
- Retrieve full content only when the snippet does not contain the needed resolution, status, or configuration detail.

### Slack

- Search public channels using several small exact-term searches instead of one long natural-language query.
- Add `in:`, `from:`, `is:thread`, and date modifiers only when they improve precision.
- Read the full thread before relying on a message.
- Prefer recent threads and identify the date in CSM notes.
- Search private channels or DMs only after explicit current-conversation consent.
- Never post, react, or otherwise mutate Slack from this skill.

Unleash and Slack are complementary. Unleash provides indexed semantic discovery and Jira context; Slack provides fresher channel-native context. Search both when both can materially resolve an internal problem.

## Search budget

| Complexity | Typical maximum calls |
|---|---:|
| Simple Z2 question | 2–3 |
| Z2 plus official public sweep | 4–5 |
| Troubleshooting with internal validation | 6–8 |
| Multi-topic question | 8–10 |

Stop expanding once the answer is sufficiently supported. One refined query is preferable to chains of synonyms.

## Failure handling

- Z2 unavailable: stop; no Zendesk product answer from memory.
- Tavily unavailable: continue with Z2 unless the question specifically depends on an official non-Help-Center source; disclose the public-web gap.
- Unleash or Slack unavailable: use the remaining internal source and disclose incomplete internal coverage.
- Both internal sources unavailable when internal validation is material: state that internal validation could not be completed and route appropriately.
- Empty results: rephrase once, then stop or move to the next applicable layer. Never equate a retrieval miss with product unavailability.
