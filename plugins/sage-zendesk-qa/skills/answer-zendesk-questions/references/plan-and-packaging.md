# Plan and packaging policy

## Plan gate

Extract the plan and add-ons from the current message, pasted email, transcript excerpt, notes, and usable conversation context.

Ask for the plan before answering when all are true:

- A specific customer is in play.
- The question concerns capability, availability, capacity, configuration, limits, packaging, pricing, or add-on eligibility.
- The plan is absent and the answer is likely to change by tier.

Lead with one question and stop:

> What Zendesk plan is the customer currently on?

Match the user's language. Do not bury the plan question in a partial briefing. A request such as `do everything` does not waive this gate.

Do not ask for the plan for universal conceptual CSM-prep questions such as what a trigger is, how triggers differ from automations, general ticket lifecycle behavior, or generic API structure.

For troubleshooting, research universal causes first when plan is unlikely to matter. Ask for the plan if the resolution path or availability depends on it.

## Packaging guard

Do not say `included`, `available on your plan`, `no plan change required`, or an equivalent unless:

1. The customer's plan and relevant add-ons are confirmed.
2. Availability is verified in current Z2 content or a current official Zendesk product/pricing page.

If the evidence supports likely availability but not a definitive claim, say:

> Based on the available documentation, this should be available on the current plan, but confirm it in the instance before promising it.

Do not use the hedge as a replacement for a required plan question.

## Add-ons

An add-on is not plan-agnostic. Before recommending Copilot, Workforce Management, Quality Assurance, Advanced Data Privacy and Protection, or another add-on:

- Verify the add-on's minimum eligible plan.
- Compare it with the customer's confirmed plan.
- Distinguish `available to purchase on the current plan` from `requires a plan upgrade first, then the add-on`.
- Route contract-specific price and commercial terms to the account team.

## Approved AI-agent packaging truth

Last reviewed: 2026-07-22.

Zendesk's April–May 2026 rollout replaced the prior Essential/Advanced capability split with a single AI-agent offering for Zendesk customers. The commercial conversation is Automated Resolution volume rather than a separate Advanced capability tier.

Official reference: https://support.zendesk.com/hc/en-us/articles/10487730059034-Announcing-expanded-access-to-AI-agent-capabilities-for-all-Zendesk-customers

Older articles may still describe capabilities as `Advanced only`. Use those older articles for behavior or configuration only, not current packaging. If a newer official public source dated after this review explicitly changes the policy, use the newer evidence and flag the change to the CSM.

Do not recommend purchasing `AI Advanced` as a separate capability upgrade without newer official evidence that supersedes the rollout.
