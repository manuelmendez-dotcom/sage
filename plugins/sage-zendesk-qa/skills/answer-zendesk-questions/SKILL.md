---
name: answer-zendesk-questions
description: Research and answer Zendesk product, configuration, workflow, plan, limitation, best-practice, integration, and troubleshooting questions for Customer Success. Use for direct CSM questions or discrete Zendesk questions extracted from customer emails, notes, and transcripts. Begin with Z2, expand conditionally to official Zendesk web sources through Tavily, then use Unleash and Slack for internal evidence. Do not use for account-data analysis, goal extraction, success plans, decks, or other non-Q&A deliverables.
---

# Answer Zendesk Questions

Turn Zendesk questions into concise, evidence-grounded CSM briefings. Treat the public product record and internal operational evidence as different tiers. Never complete a product claim from memory.

## Core contract

- Search a verified source this turn before stating any Zendesk behavior, availability, limit, path, option, action, UI label, or effective date.
- Use Z2 first. Use Tavily only for an official public sweep that can add value. Use Unleash and Slack only when internal evidence can resolve a problem signal, recent change, documentation gap, or conflict.
- Keep public and internal evidence visibly separate. Never turn Slack, Jira, or an internal discussion into an announced product commitment.
- Default to a CSM-facing diagnostic briefing. Produce customer-ready copy only when explicitly requested.
- Do not narrate a future deliverable. If customer-ready copy is requested or promised, include the complete copyable draft in the same response.
- Match the language rules in [references/response-formats.md](references/response-formats.md).
- Say `couldn't verify` when the available evidence does not support a claim.

## 1. Normalize the request

Read the entire input and extract every actionable Zendesk question. Ignore greetings, signatures, duplicate quoted text, and unrelated discussion.

For each question, capture:

- Desired outcome and product area.
- Named customer, plan, add-ons, role, configuration, and constraints.
- Reported facts versus assumptions.
- Symptoms, errors, timing, and any claimed product behavior.

Silently classify each item as `BASIC_FEATURE`, `CONFIGURATION`, `WORKFLOW`, `TROUBLESHOOTING`, `BEST_PRACTICE`, `WORKAROUND`, `INTEGRATION`, `BILLING_ADMIN`, `REPORTING`, or `NON_ZENDESK`.

Keep a checklist for multi-question inputs. Answer or explicitly block every named item.

## 2. Apply the plan and packaging gate

Read [references/plan-and-packaging.md](references/plan-and-packaging.md) whenever the question involves capability, availability, limits, add-ons, pricing, or configuration for a specific customer.

- Extract the plan and add-ons from the current message and usable conversation context. Do not ask for information already present.
- For a named customer or pasted customer content, ask for the plan first when the question is materially capability-, tier-, capacity-, or add-on-dependent. Ask one focused question and stop.
- Do not ask for a plan for purely conceptual CSM preparation when the answer is universal.
- Announce a plan extracted from context once, using the real source: `Plan confirmed from the customer email: Suite Professional.`
- Never substitute `verify in the instance` for a required plan question.

## 3. Research Z2 first

Read [references/source-routing.md](references/source-routing.md) before calling sources.

Search the Z2 Help Center for every Zendesk question. Use concise feature-and-intent terms.

- Use one query for a simple concept or fact.
- Use two focused query variants for packaging, best practice, troubleshooting, multi-step configuration, frequently changing features, and enumerated availability questions.
- Retrieve relevant article content before relying on procedures, UI controls, action verbs, paths, limits, or packaging claims. Prefer TOC and section retrieval for long articles.
- Cap full article reads at two strong candidates per topic.
- Use `fetch_z2_content_by_url` when the user provides a Help Center URL or Tavily discovers one.
- Treat `user_segment_id: null` as public/customer-shareable. Treat non-null content as internal-only.

If Z2 is unreachable, stop without a product answer. State that Z2 is required for an accurate response and ask the user to reconnect it.

## 4. Expand through official public sources when useful

Use Tavily after Z2 only when:

- Z2 is empty, thin, ambiguous, or apparently stale.
- The question concerns an official Zendesk product, pricing, status, release, marketplace, or developer surface outside normal Help Center coverage.
- A fast-changing or high-risk claim warrants an additional official public check.

Restrict the search to the official Zendesk domains defined in [references/source-routing.md](references/source-routing.md). Retrieve the actual page before relying on it; do not answer from a search snippet alone.

When Tavily finds a `support.zendesk.com` article, fetch that URL through Z2 and use the Z2 result as the authority.

Do not call Tavily as a ritual second search when Z2 already answers a basic question completely.

## 5. Use the internal layer when signaled

Use Unleash and direct Slack when the question involves a bug, error, outage, regression, intermittent behavior, undocumented configuration edge case, recent rollout, work-in-progress status, public-source conflict, or a request to see whether someone has solved the problem.

- Search Unleash for indexed Jira, Slack, worklog, and internal knowledge. Set `include_jira: true` for suspected bugs and known issues.
- Search public Slack channels with small exact-term queries. Use channel, author, thread, and date modifiers only when useful. Read the strongest relevant threads before relying on them.
- When both can contribute, search Unleash and public Slack as complementary peers in the same internal layer.
- Cap heavy internal reads at two relevant resources per question.
- Search public Slack channels without an additional consent gate when the internal layer is warranted.
- Ask for explicit current-conversation consent before searching private channels or DMs. Stop and wait for that consent.

If one internal MCP is unavailable, continue with the other and disclose the missing coverage. If both are unavailable when internal validation is material, say that the issue could not be internally validated and recommend the appropriate escalation.

## 6. Reconcile evidence

Read [references/evidence-policy.md](references/evidence-policy.md) whenever Tavily, Unleash, or Slack is used, sources conflict, or evidence is incomplete.

- Validate the customer's premise before prescribing configuration or escalating.
- Reconcile documented patterns with the customer's actual workflow: who acts, what signals return, what the end user experiences, and whether a manual step is realistic.
- Lead with a supported replacement when a feature is deprecated.
- Treat retrieval absence as absence of evidence, not proof that a feature is unavailable.
- Apply the source-date and disclosure rules before resolving conflicts.
- Use only documented workarounds in customer-ready copy. Present internal or community leads as validation paths, not promises.

Read [references/solution-and-escalation.md](references/solution-and-escalation.md) when the answer may require Support, Security, Product, Account Management, Professional Services, a Solution Architect, Marketplace, App Builder, or custom development.

Do not present custom development as an implementation option merely because an API object or field exists. Verify the write path, relevant prerequisites, and architecture from current sources. Otherwise label it a technical discovery path and route it to an appropriate technical owner.

## 7. Produce the right response

Read [references/response-formats.md](references/response-formats.md) and select the matching format.

Default to a compact CSM diagnostic briefing using only the applicable labeled beats:

1. Direct answer or customer-question labels for multi-question inputs.
2. `On their plan` when plan changes the answer and is confirmed.
3. `Recommendation` grounded in both evidence and the customer's stated reality.
4. `Support / development / external app` only when a real handoff or non-native path exists.
5. `Public sources` with the few public URLs that materially support the answer.
6. `CSM notes` only when internal evidence, a conflict, a meaningful assumption, or a verification gap exists.

Do not add an escalation section merely to say no escalation is needed. Do not expose internal links, Jira keys, employee identities, private Slack details, or unannounced information in customer-ready copy.

## 8. Verify before responding

Confirm silently that:

- Every extracted question is answered or explicitly blocked.
- Every product claim traces to a source searched this turn.
- Action verbs, UI labels, paths, limits, and dates are grounded.
- The plan gate and add-on minimum-tier check passed where relevant.
- Public, internal, and unverified evidence are not blurred.
- Internal information is absent from customer-ready copy.
- Every promised deliverable is present in the response; no research-plan narration remains.
- Recommendations fit the customer's actual workflow rather than only a generic documented pattern.
- The response format and language match the input.

Repair any failed check before responding. Never render a knowingly ungrounded answer.
