---
name: Naturecan configuration guide incident (2026-04-20)
description: Boss flagged an incorrect SAGE-generated triage setup guide for Naturecan. Root cause, diagnosis, and planned v2.1.2.4 fix.
type: project
originSessionId: cd2e15b6-737e-4614-ab77-5755bf620879
---
**Incident:** Manager (boss) asked Mo (mohamed.temraoui) to use SAGE to generate a step-by-step guide for a customer (Naturecan) on implementing 3 intelligent triage rules. The original doc had errors. Boss sent corrected version and asked manuel to flag separately.

**Original doc:** https://docs.google.com/document/d/1bgLm_FeQtK2WGvNVsqQtfGhIk8t7iu1PTONqt22V9Es/edit?tab=t.vm4h9gc6ewjk
**Corrected doc:** https://docs.google.com/document/d/1bgLm_FeQtK2WGvNVsqQtfGhIk8t7iu1PTONqt22V9Es/edit?tab=t.0

**Boss's asks:**
1. How do we make product-specific outputs more accurate? Open to cross-checking even with added latency.
2. Have you seen similar errors recently? Any patterns worth knowing about?

**Two concrete failures in the generated guide:**
1. **Wrong architecture.** Original used skills-based routing (push model: create skills, assign agents, use skill conditions). Naturecan's actual workflow is views-based (pull model: trigger tags the ticket, view filters by tag). The correction rewrote the guide using Views + Triggers. Z2 has accurate articles on BOTH architectures, so Z2 being connected would not have caught this.
2. **Hardcoded intent names.** Original used `Billing::Refund::Refund request` etc. as if universal. Intent taxonomies vary per account. They live in the customer's instance at Admin Center > AI > Intelligent triage > Intent, not in Z2.

**Root cause:** Context. SAGE didn't have enough information about Naturecan's workflow before writing, and the prompt doesn't force it to ask. MCP state (whether Z2 was connected) is a risk factor but not the root cause, since Z2 doesn't know which architecture fits the customer.

**Why:** SAGE v2.1.2.3 has strong guardrails for Q&A, transcripts, recommendations, success plans, and emails. Step-by-step configuration guides fall between modes. Nothing currently forces workflow-fit check, exhaustive Z2 verification of paths/syntax, or refusal when Z2 is unreachable.

**How to apply:** This is the pattern to extend. v2.1.2.3 already tightened the same shape for packaging claims (Constraint #23) and best-practice phrasing. Configuration guides are the next gap. Next step is drafting v2.1.2.4.
