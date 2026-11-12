# Source routing

Select sources by the unresolved question, not a mandatory connector waterfall. Separate source identity, retrieval tool, audience, and authority.

## Mode and preference contract

| Mode | Trigger | Retrieval behavior |
|---|---|---|
| INTERPRET_ONLY | Interpretation/reuse without new research, or an explicit no-search instruction | No source retrieval, including MCP, web, and browser |
| SOURCE_DIRECTED | Selected sources, priority, exclusion, or requested validation source | Honor the stated order and the permitted set |
| AUTO | No applicable research constraint | Reuse evidence, then choose the smallest sufficient additional set |

Current explicit instructions take precedence over earlier preferences. Keep source restrictions for related follow-ups; a new unrelated question returns to AUTO unless there is an explicit conversation-wide preference. See [source-selection.md](source-selection.md) for the optional menu.

- `Start with X` / `primero X` sets priority. Search X first and then expand if a specific gap warrants it, without an extra permission request, within all other applicable constraints.
- `Only X`, `do not use Y`, a closed selection such as `use X and Y`, or `start with X and ask before using anything else` constrains the source set. Do not silently widen it.
- `Search Slack only` limits new retrieval but permits relevant prior Z2 evidence. `Base the answer only on Slack` excludes other-source evidence too.
- `A Slack post says X; is it true?` supplies provenance; it does not restrict public validation.

Community is a source; Tavily is an access tool. `Community only` allows public retrieval of community.zendesk.com through an available permitted tool, not external Help Center links. A tool restriction such as `Tavily only` also controls the access method. Do not circumvent a source restriction by changing connectors.

## Source roles and exclusions

| Source | Use | Authority and limits |
|---|---|---|
| Z2 Help Center | Product behavior, how-to, prerequisites, limits, packaging, Updates | Official product evidence when the article is public; inspect audience metadata |
| Official public web | Developer/API, status, pricing, Marketplace, relevant vendor documentation, public fallback | Authority depends on original publisher; a vendor listing does not establish native behavior |
| Zendesk Community | Comparable workflows, practitioner experience, feedback, possible workarounds | Community-reported evidence; read replies and later corrections |
| Z2 Ticket Context | Supplied case, comparable solved cases, Problem Tickets, diagnostic history | Internal case evidence, including comments labeled PUBLIC; not public product documentation |
| Slack | Fresh internal product/release discussion, direct threads, operational context | Conversational internal evidence; check dates and the complete relevant thread |

**Unleash, Google Drive and Zendeskdev are outside this research profile.** Do not call them from SAGE, including as fallbacks or through globally available connections. Do not retrieve Drive or Zendeskdev content through a different connector. Public API questions belong to developer.zendesk.com. Leave shared connections and other plugins unchanged.

SAGE does not provide direct Jira retrieval or a unified internal-document search. Slack discussions and Ticket Context may supply relevant case evidence, but do not claim to have verified a Jira record merely because they reference it. If the answer requires the original internal record, identify that gap and the appropriate owner or separate investigation instead of inventing a replacement source.

Supplied excerpts can still be interpreted when the user asks, preserving their provenance and internal status. That is not permission to search an excluded repository or turn internal content into a public claim.

## Routes by question

| Signal | Initial route | Expand only for a specific gap |
|---|---|---|
| Basic product concept, configuration, limit or ordinary how-to | Relevant Z2 documentation | Official web if Z2 lacks the needed coverage |
| Capability recommendation for an objective | Current product documentation + targeted Updates check | Community/cases for practical fit; internal sources for a distinct unresolved issue |
| Release, historical change, EAP or rollout | Relevant Updates sections and linked articles | Current documentation to validate present behavior/status |
| Supplied ticket ID | Ticket Context: get the ticket | Relevant Z2, comparable cases, PTs or audit events as needed |
| Reproducible symptom, known bug, regression | Product baseline if not established; relevant cases/PTs | Slack for recent discussion; identify any unresolved engineering-record gap |
| Practitioner workaround or comparable workflow | Existing product baseline, then Community or case research | Validate proposed public guidance in current documentation |
| Known Slack thread/channel or explicit fresh internal discussion | Slack directly | Public validation for customer-facing product claims if allowed |
| Public API, webhook or SDK details | Official developer documentation; relevant Z2 if useful | Vendor docs for the other side of an integration |
| Current outage/service disruption | status.zendesk.com and relevant Service notifications | Ticket/PT/internal context if needed for the case |

Read [releases-and-capabilities.md](releases-and-capabilities.md), [ticket-research.md](ticket-research.md), or [community-research.md](community-research.md) for their respective routes. Native features and recent changes should be understood before recommending custom work.

## Retrieval playbooks

### Z2

- Search concise product + action/symptom terms. Use known `category_ids` / `section_ids` to narrow scope.
- Search results identify candidates. Retrieve article content before relying on procedures, UI labels, limits, dates, or availability.
- Use a supplied Help Center URL directly. For long articles, inspect the TOC, then request relevant sections. Fetch full content only if needed; get audience metadata from article/search results as well.
- Check `user_segment_id` (`null` means public in this MCP; non-null means restricted). TOC/section content alone does not establish audience.
- Avoid fetching whole Help Center sections merely to discover candidates: the response can contain many complete article bodies. A category lookup returns a lighter section map.

### Public web / Tavily

Use focused `include_domains`, usually `search_depth: "fast"` and `max_results: 5`. Do not put `site:` in the query. Retrieve the original page before relying on a search result.

Select the relevant domains: `support.zendesk.com`, `developer.zendesk.com`, `status.zendesk.com`, `www.zendesk.com`, or a relevant vendor's official documentation. Community uses its own domain and playbook.

When a discovered Help Center article needs audience metadata, use Z2 if permitted. When retrieval is explicitly Tavily-only, keep that method and disclose a missing metadata check if it affects the conclusion. Do not retrieve excluded Help Center evidence through another tool.

### Slack

- Search public channels using short feature/error terms and helpful date/channel filters. Scope searches to known public channels when possible; an unrestricted workspace search may include private channels.
- Do not search private channels or DMs without explicit consent in this conversation. If the connector cannot enforce the public scope, establish allowed public channel IDs first or report that limitation.
- Read the relevant thread, including later corrections, before relying on a message. A release discussion does not replace a public rollout announcement.
- This skill never posts, reacts, or changes Slack.

## Evidence reuse, efficiency and failure handling

Maintain a compact working ledger: original URL/ID, retrieval/publication/discussion date, audience, supported claim, and remaining gap. Reuse it when relevant and current enough; re-fetch only for a new claim, meaningful freshness concern, missing content/metadata, conflict, or explicit fresh-check request.

Retrieve only the content needed for the claim. Batch independent reads and stop when evidence is current, applicable and sufficient. One focused rephrase is usually more useful than chains of synonyms. Simple Q&A often needs only search + article; complex or historical questions may need more. Do not turn a soft efficiency target into a correctness cutoff or claim exhaustive coverage from bounded searches.

- In INTERPRET_ONLY, identify gaps without repair calls.
- With a closed source set, disclose failures and continue only within that set. Request expansion only if a material conclusion still needs an excluded source.
- In AUTO or priority-only research, use a relevant permitted fallback. If Z2 fails, official-public web can help, but disclose a load-bearing audience/content gap.
- If no evidence supports a claim, say it could not be verified. Empty search results do not establish feature absence.
