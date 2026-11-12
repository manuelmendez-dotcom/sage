# Plan and packaging policy

## Plan gate

Extract the plan and add-ons from the current message, pasted email, transcript excerpt, notes, and usable conversation context.

Gate the plan-dependent conclusion, not evidence ingestion or interpretation.

In `INTERPRET_ONLY` and `SOURCE_DIRECTED` modes:

- Complete the requested interpretation or permitted research without asking for the plan first.
- Identify whether any conclusion depends on tier, capacity, or add-on eligibility.
- Withhold only the dependent conclusion when the plan is absent.
- Ask one focused plan question after the usable analysis when that answer is needed to proceed.

In `AUTO` mode, ask for the plan first and stop only when all are true:

- A specific customer is in play.
- The question concerns capability, availability, capacity, configuration, limits, packaging, pricing, or add-on eligibility.
- The plan is absent and the answer is likely to change by tier.
- The entire useful answer materially depends on that missing plan.

Lead with one question and stop:

> What Zendesk plan is the customer currently on?

Match the user's language. A request such as `do everything` does not waive the gate for a definitive plan-dependent claim.

Do not ask for the plan for universal conceptual CSM-prep questions such as what a trigger is, how triggers differ from automations, general ticket lifecycle behavior, or generic API structure.

For capability recommendations, research useful candidates and their documented eligibility conditions even if the plan is unknown; withhold only customer-specific availability. A historical release date or general EAP status does not require a customer plan.

For troubleshooting, research or interpret universal causes first when plan is unlikely to matter. Ask for the plan only when the resolution path or availability materially depends on it.

## Packaging guard

Do not say `included`, `available on your plan`, `no plan change required`, or an equivalent unless:

1. The customer's plan and relevant add-ons are confirmed.
2. Availability is verified in current Z2 content or a current official Zendesk product/pricing page.

When eligibility is incomplete, state what the documentation establishes and the exact missing condition. Do not hedge an unsupported entitlement into “should be available” or replace a necessary plan question with “check the instance.”

## Add-ons

An add-on is not plan-agnostic. Before confirming customer-specific eligibility for Copilot, Workforce Management, Quality Assurance, Advanced Data Privacy and Protection, or another add-on:

- Verify the add-on's minimum eligible plan.
- Compare it with the customer's confirmed plan.
- Distinguish `available to purchase on the current plan` from `requires a plan upgrade first, then the add-on`.
- Route contract-specific price and commercial terms to the account team.

## Packaging changes and historical terminology

Do not maintain a frozen packaging truth in this skill. Revalidate current public sources when packaging is material; use the releases reference for announcements and subsequent changes.

This announcement is a research lead, not a current entitlement rule:
https://support.zendesk.com/hc/en-us/articles/10487730059034-Announcing-expanded-access-to-AI-agent-capabilities-for-all-Zendesk-customers

Check its actual content, rollout scope and subsequent official documentation before applying it. Older articles can remain useful for behavior while using obsolete plan/tier names. Do not infer a purchase requirement, retirement of a tier or billing model from a remembered rollout or an old label. Distinguish the capability, eligibility and commercial terms; route account-specific contractual questions to the account team.
