# Zendesk Community research

Use for source-directed Community questions or a specific practitioner-evidence gap in AUTO mode. Community-only research remains within `community.zendesk.com`, even when the discussion or AI overview links to external documentation. Follow source-routing.md for the permitted source set and evidence restrictions.

## Access and discovery

- The connected Z2 Help Center tools cover `support.zendesk.com`; do not send Community URLs to Z2 or assume changing a hostname adds support.
- Use the existing Tavily search and extraction tools for public Community content. Start with `include_domains: ["community.zendesk.com"]`, `search_depth: "fast"`, and `max_results: 5`. Use concise product, symptom, or workflow terms; retrieve a supplied discussion URL directly. Remove customer identifiers that are unnecessary to the search.
- Read the strongest relevant discussions, not just snippets. Rephrase once if results are materially weak. Stop when the question has sufficient evidence; do not crawl the entire community for a single inquiry.
- Use the site's native search and AI overview through the available browser/computer-use capability when requested, when Tavily leaves a meaningful gap, or when interactive replies cannot be retrieved completely. If browser access is unavailable, disclose that limitation and continue with permitted public retrieval when useful. Do not claim to have consulted the site's AI through a Tavily search.
- Native search is available at `https://community.zendesk.com/` and search pages use `/search?q=...`. Inspect the current UI before interacting. Use the search field, read the AI overview and search results, and refine visible content-type, category, or tag filters only when useful. UI labels can change.
- An AI overview is a discovery aid, not an independent evidentiary source. Inspect its related links and original discussion replies. Use a follow-up question only to resolve a concrete gap, and verify any new references it supplies.
- Reading and searching do not authorize creating a post, replying, voting, following, or contacting a member. Do not use the separate Contact us/support messaging widget for community research.

## Read the discussion

Capture the canonical discussion URL, original question and date, relevant reply dates, author role when visible, accepted/best-answer status, and later qualifications or corrections. Follow pagination or expand nested replies when needed to support the conclusion. If completeness cannot be established, say the evidence is partial.

Prioritize workflow fit and evidence quality, not just likes, badges, or recency. Distinguish:

- A question or feature request from evidence that a feature exists.
- A suggestion from a reported successful result.
- Customer experience, partner/vendor advice, visible Zendesk employee responses, and official documentation.
- An accepted answer from a currently verified solution; a later reply may qualify or contradict it.
- Product-feedback status from a release or delivery commitment.

Deduplicate alternate URLs to the same discussion. Preserve direct reply anchors when available. Do not invent dates, staff status, or accepted-answer labels. Treat commercial recommendations as partner/vendor claims and inspect attached screenshots only when they materially support the answer.

## Access gaps and verification

If a link returns access forbidden, a login requirement, or an unavailable page, report the access limitation. Do not infer what the hidden content says from its title or the AI overview. Continue with accessible relevant sources within the allowed set. Authenticated access must use normal authorized browser access; no bypass or credential extraction. Do not assume any logged-in result is public or customer-shareable.

For Community-only research, label possible workarounds and behavior claims as community-reported. Do not silently use Z2 to validate them. Identify the exact unresolved claim and useful official validation source when needed.

When Z2 or official web verification is permitted, retrieve current documentation for the material behavior, limits, prerequisites, and plan claims. Explain whether it confirms, qualifies, contradicts, or leaves the community finding unverified. An employee badge or the AI's confident wording does not replace product documentation.

For migrated Help Center links with a Community hostname, do not silently rewrite the host and fetch it under a Community-only restriction. When official verification is allowed, locate the current official page and retrieve it through the appropriate permitted tool.

## Output

Use the shared concise CSM briefing. Include the answer, the relevant community experience and dates, verified documentation when permitted, and remaining gaps. Cite the original discussions or replies rather than the AI search page. Keep community evidence distinct from official sources. Include the tools used only when material, for example: `Research scope: Source-directed · Community only · Used: Tavily and native Community AI search`.

Do not add an Official verification section to a Community-only brief just to say it was not performed. Put the verification gap next to the affected claim. Apply the existing confidentiality rules to customer-ready drafts and authenticated restricted content.

## Verified access observations

On 2026-09-14, a public browser session exposed an `AI Community Agent` overview, related links, follow-up input, and filtered search results. One AI-linked page returned access forbidden while other public discussions and replies were retrievable through Tavily. These observations establish useful access routes, not complete index coverage or permanent UI behavior.

- [Community search guidance](https://community.zendesk.com/get-started-134/getting-started-in-the-zendesk-community-21279)
- [Public discussion used to check reply retrieval](https://community.zendesk.com/support-7/trigger-based-on-domain-21355)
