# Source routing

Let the user control discovery order. Let evidence authority control what the response may safely claim.

## Contents

- [Mode contract](#mode-contract)
- [Evidence reuse](#evidence-reuse)
- [Source roles](#source-roles)
- [AUTO routing table](#auto-routing-table)
- [Source playbooks](#source-playbooks)
- [Search budget](#search-budget)
- [Failure handling](#failure-handling)

## Mode contract

| Mode | Trigger | Tool behavior |
|---|---|---|
| `INTERPRET_ONLY` | Usable evidence is present and the user requests interpretation, reuse, or no new research | Make zero source-retrieval calls, including MCP and browser retrieval |
| `SOURCE_DIRECTED` | The user explicitly selects a source, source set, order, constraint, or validation source | Call only the allowed sources in the requested order |
| `AUTO` | No interpret-only instruction and no applicable source preference | Reuse suitable evidence, then use the smallest sufficient additional set; do not search all sources |

Do not silently widen a source-directed request. A source lock limits discovery; it never promotes the authority of the allowed evidence.

Resolve applicable source preferences from current explicit instructions, then the ongoing inquiry's restrictions or an explicit conversation-wide preference. A no-search instruction takes precedence. Preserve restrictions for related follow-ups; do not carry a one-question choice into an unrelated inquiry. Use [source-selection.md](source-selection.md) for the optional menu and preference lifetime.

Resolve source identity separately from retrieval method. `Community` means `community.zendesk.com`; Tavily or native browser search can access that same source without widening it. `Official web documentation` uses appropriate official domains. A user who explicitly specifies a tool, such as `Tavily only`, also constrains the access method. A mere mention such as `a community post says` is evidence provenance, not a research directive.

A source named as provenance is not automatically a source directive. `Slack says X; is it true?` supplies internal evidence and ordinarily calls for AUTO public validation unless the user also directs the research to Slack.

Distinguish research constraints from evidence constraints:

- `Search Slack only` limits new calls to Slack but permits comparison with relevant prior evidence already in context.
- `Base the answer only on Slack` excludes other-source evidence from the conclusion as well as from new calls.

Treat `start with X` as one initial source call or focused search sequence. Report whether it was sufficient and identify—but do not call—the next useful source unless the user permits expansion.

## Evidence reuse

Before searching, inspect the active conversation for relevant retrieved content. Reuse evidence when its source, topic, scope, and date remain suitable for the current decision.

Maintain a compact ledger containing:

- Source and content title or identifier.
- Retrieval, publication, or discussion date when available.
- Audience tier: public product, official public, community, internal operational, internal engineering, enablement, or unverified.
- Claims supported.
- Material gaps or conflicts.

Do not search the same source again solely because the user asks a follow-up. Re-query only when the earlier evidence does not cover the new claim, freshness materially matters, or the user asks for a fresh check.

## Source roles

| Source | Use | Authority and limits |
|---|---|---|
| Z2 Help Center | Product behavior, setup, requirements, limits, plans, troubleshooting, public developer documentation | Primary customer-safe product record when the article is public |
| Zendesk Community | Comparable cases, practitioner experience, feedback, and possible workarounds; use [community-research.md](community-research.md) | Community evidence; neither the site AI nor an accepted answer establishes current product truth |
| Official web documentation | Official Zendesk product, pricing, status, release, Marketplace, developer, and relevant vendor pages, accessed through Tavily or another permitted web tool | Official-public corroboration; third-party vendor claims remain separately labeled |
| Unleash | Indexed internal knowledge, Jira, worklogs, known issues, recent decisions | Internal operational evidence; never a public commitment |
| Slack | Fresh practitioner discussion, live operational context, and direct thread evidence | Internal conversational evidence; corroborate consequential claims |
| Google Drive | Enablement, decks, playbooks, positioning, examples, and talk tracks | Internal enablement evidence; never overrides current product documentation |
| Zendeskdev | Internal engineering documentation, architecture, runbooks, incidents, and deep technical feasibility | Internal engineering evidence; not public developer documentation |

## AUTO routing table

| Signal | Initial route | Conditional expansion |
|---|---|---|
| Basic product concept or universal behavior | Z2 | Stop when complete |
| Configuration how-to without problem signals | Z2 | Tavily official Zendesk only if Z2 is materially thin |
| Plan, packaging, limit, add-on, or pricing | Z2 | Tavily official product or pricing page when useful |
| Best practice or recommended approach | Z2 | Tavily official Zendesk guidance when Z2 lacks breadth |
| Comparable cases, practitioner experience, or possible workarounds would resolve a remaining gap | Z2 for the relevant product baseline | Community through Tavily; native Community AI search when requested or when it resolves a retrieval gap |
| Explicit Community research request | Community through the requested method or the Community playbook | Official verification only when the user also permits it; Community-only stays restricted |
| Public API, webhook, SDK, or developer question | Z2 | Tavily restricted to official developer.zendesk.com pages |
| Marketplace or third-party integration | Z2 | Tavily restricted to official Marketplace and relevant vendor documentation |
| Current outage or public status | Z2 for documented behavior | Tavily restricted to official status or release sources |
| Suspected bug, regression, known issue, or Jira question | Z2 | Unleash first; add Slack only for a distinct freshness or practitioner gap |
| Explicit request for recent Slack experience | Slack | Identify the public or internal validation source without calling it unless permitted |
| Enablement, deck, playbook, positioning, or talk track | Google Drive | Z2 only when the user permits product-claim validation |
| Internal architecture, runbook, incident mechanics, or deep engineering feasibility | Zendeskdev | Unleash only for a distinct Jira or decision gap |
| Z2 and official web conflict or appear stale | Unleash or Slack, selected by the conflict signal | Use the second internal source only when it resolves a distinct gap |
| Clearly non-Zendesk vendor behavior needed for an integration answer | Tavily on the vendor's official documentation | Validate the Zendesk side through Z2 when needed |

Do not call Google Drive for ordinary product Q&A. Do not route public API questions to Zendeskdev merely because the word `developer` appears.

## Source playbooks

### Z2

1. Search with a short product term plus the desired action or symptom.
2. Run a second focused variant only for load-bearing packaging, troubleshooting, multi-step configuration, or enumerated availability questions.
3. Retrieve the strongest article content before using procedures, UI controls, actions, limits, or plan claims.
4. Inspect the TOC and retrieve relevant sections for long articles.
5. Check `user_segment_id` before treating an article as customer-shareable.
6. Use a supplied Help Center URL directly.

Titles and snippets can identify candidates but cannot support detailed claims.

### Tavily

Use `search_depth: "fast"` and `max_results: 5` by default. Run one official-domain sweep per unresolved claim and at most one refined follow-up.

For official web research, the default Zendesk allowlist is:

- `support.zendesk.com`
- `www.zendesk.com`
- `developer.zendesk.com`
- `status.zendesk.com`

For Community research, use `include_domains: ["community.zendesk.com"]` instead and follow [community-research.md](community-research.md). A Community-only restriction does not permit following external Help Center, Marketplace, or vendor links. With multiple sources permitted, keep source-specific searches and evidence labels clear.

Use `include_domains`; do not place `site:` in the query. Retrieve the actual page before relying on it.

In AUTO mode, fetch a discovered Help Center URL through Z2 to restore article metadata. In SOURCE_DIRECTED mode, use Z2 only when permitted. If official Help Center content is allowed but the user restricts retrieval to Tavily, retrieve it through Tavily and disclose that Z2 audience metadata was not checked. If Help Center content itself is outside the permitted set, do not retrieve it through either tool.

### Unleash

- Search with the product or feature plus the symptom, issue, or operational concept.
- Use `include_jira: true` for suspected bugs, incidents, regressions, roadmap status, and known issues.
- Start with five results and retrieve only the strongest relevant resources.
- Prefer recent evidence; use older material only for a specifically matching long-standing issue.

### Slack

- Search public channels with several small exact-term searches rather than one long natural-language query.
- Add channel, author, thread, and date modifiers only when they improve precision.
- Read the full relevant thread before relying on a message.
- Ask for current-conversation consent before searching private channels or DMs.
- Never post, react, or mutate Slack from this skill.

### Google Drive

- Retrieve a supplied canonical URL directly.
- Search with plain text when no canonical link is available; prefer recent or clearly owned material and inspect modified dates.
- Retrieve only the relevant document section, slide range, or sheet when the result is large.
- Label deck language as enablement or positioning until current public documentation validates any product claim.
- Preserve ambiguity when similarly named or stale files cannot be resolved safely.

### Zendeskdev

- Use only for explicitly internal engineering topics or SOURCE_DIRECTED requests.
- Search with the product plus the engineering concept, incident symptom, service, or runbook term.
- Retrieve the relevant article or external indexed content before relying on it.
- Keep engineering details in CSM notes and minimize sensitive content.
- Route public API behavior to Z2 or official developer.zendesk.com content instead.

## Search budget

| Complexity | Typical maximum calls |
|---|---:|
| Simple Z2 question | 2–3 |
| One source-directed question | 2–4 within the allowed source |
| Z2 plus official-public expansion | 4–5 |
| Troubleshooting with one internal layer | 5–7 |
| Multi-topic question | 8–10 |

Stop expanding when the answer is sufficiently supported. Prefer one refined query to chains of synonyms.

## Failure handling

- `INTERPRET_ONLY`: never repair a gap with a tool call; identify the next useful source.
- `SOURCE_DIRECTED`: if an allowed source is unavailable, disclose the failure and continue only to the next source already permitted by the user. Do not substitute an unpermitted source; stop when the allowed set is exhausted.
- `AUTO`, Z2 unavailable: use Tavily restricted to official Zendesk sources only when it can support the claim; disclose the missing Z2 metadata check. Stop when customer-safe status or exact Help Center content is load-bearing.
- `AUTO`, optional source unavailable: continue only when the remaining evidence is sufficient and disclose the coverage gap.
- Empty results: rephrase once within the permitted source, then stop or identify the next source. Never equate a retrieval miss with product unavailability.
