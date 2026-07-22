# Solution and escalation routing

## Solution order

When the customer's need has several possible implementation paths, consider them in this order:

1. Native Zendesk capability verified in Z2.
2. Official Zendesk integration or Marketplace option, clearly labeled.
3. App Builder when the need is an agent-side sidebar experience, in-ticket context, external-system lookup, or a focused one-click action.
4. Custom integration or development.

Do not recommend App Builder, Marketplace, or custom development until the native path and limitation are understood. Verify App Builder and Marketplace feasibility through current sources; do not assume an app can access data merely because an API exists.

## Support handoff detection

While reading Z2, watch for `contact Support`, `submit a request`, `requires Zendesk assistance`, `requires backend changes`, `enable via Support`, or equivalent language.

When that action is genuinely required for the customer's path, state:

> This needs Support to action: [verified reason]. I can draft the request if useful.

Do not trigger a handoff from an incidental or optional Support mention.

## Escalation table

| Scenario | Route |
|---|---|
| Confirmed Jira bug or active incident | Support or Engineering; name the known issue internally and offer the documented workaround |
| Security or compliance interpretation | Security team |
| Data loss or production-impacting issue | Immediate Support escalation |
| Contract, price, renewal, or account-specific packaging | Account team |
| Feature does not exist | Product feedback; do not promise roadmap delivery |
| Unreleased or roadmap information | Product team; no customer commitment without an approved public source |
| Complex multi-system implementation | Professional Services or Solution Architect |
| API feasibility confirmed but implementation unproven | Solution Architect, Professional Services, partner, or customer's technical team |
| Conflicting or insufficient evidence | Appropriate subject-matter owner or Support |

Keep escalation to one clear recommendation in the CSM briefing. Do not manufacture an escalation section when the issue resolves CSM-side.

## Premise and workflow checks

Before prescribing steps:

- Verify that the product behaves the way the customer assumes.
- Confirm who actually performs each step.
- Confirm whether an external system returns a completion or closure signal.
- Prefer automation when the stated workflow has no reliable human actor.
- Do not copy a generic best practice when it recreates the customer's problem under a different label.

If evidence contradicts the customer's premise, explain the contradiction and recommend a scoped retest before escalating.
