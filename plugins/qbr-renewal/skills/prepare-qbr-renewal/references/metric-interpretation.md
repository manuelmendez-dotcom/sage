# Metric interpretation

Keep the QBR's definitions; do not substitute another product's or dashboard's definition.

| Signal | Interpret with | Do not infer |
| --- | --- | --- |
| Created/solved tickets | Demand/throughput, period and channel mix | Business growth, agent-only workload or backlog from unmatched counts |
| First reply/full resolution time | Calendar/business clock, median/mean, period and case mix | Handling time, labour effort or a cause of delay |
| CSAT | Response count and eligible population | Dissatisfaction or disabled surveys from zero/blank values |
| One-touch/zero-touch | Exact public-reply/touch definition | AI resolution, deflection or service quality by itself |
| Knowledge views/self-service ratio | Source-defined numerator and denominator | Tickets avoided or money saved |
| AI conversations/resolutions | Exact resolution definition and matched period | Every conversation is resolved or a new avoided ticket |
| Copilot acceptance/usage | Suggestions shown, accepted/edited/dismissed and eligible population | Poor acceptance from zero events, or entitlement from a feature row |
| Seats/active agents | Role, login/work definition and time window | Wasted licences, productive FTE or staffing cuts |
| Topics | Volume, classification confidence, population and period | Reliable automation eligibility from a small or uncertain sample |
| Benchmarks | Cohort, month, population and comparable definition | Promised targets or causal results |
| WFM/other feature events | Product-specific event definition and rollout context | Implementation readiness or productivity outcome |

## Arithmetic and comparisons

- Relative change: `(current - prior) / prior * 100`. A zero prior makes this undefined; use absolute change.
- Percentage-point change: `current percentage - prior percentage`. Distinguish it from relative percent change.
- Compare matching complete periods and definitions. Never label a single available month as a sustained trend. Check the selected headline against the latest monthly pattern: acknowledge a material recovery, reversal or spike rather than letting an annual comparison obscure it.
- Do not average monthly medians into an annual median. Rates need matching denominators to combine correctly. Preserve an explicitly reported average-of-monthly-rates label if used. If an aggregate appears to include months with no eligible observations as zero, flag the concern and exclude it from value headlines until its treatment is clear; do not silently reconstruct a replacement score.
- When the customer-start date, migration context or data coverage makes a historical comparison uncertain, flag comparability rather than declaring the data false or using it as a win.
- Missing, zero and not applicable are distinct. A rate with no eligible observations is not a measured failure rate.
- Verify printed changes against source inputs where possible, retain precision and round only for display. Do not read exact values from unlabeled chart heights. For percentage growth from a small base, show the starting and ending counts or absolute change and assess whether the result is meaningful enough to lead the story. If rounded inputs hide the denominator or change, do not claim the printed percentage was verified.
- Keep observed changes separate from causal or financial impact. No default scenarios or assumed financial inputs in this version.

Use local code/calculator for derived claims and put formulas and source inputs in notes. If essential inputs are absent, omit that calculation and continue the rest of the conversation.
