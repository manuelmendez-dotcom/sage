# SAGE — Overview

## What SAGE Does

SAGE is an AI copilot for the Scaled Customer Success team. It combines product knowledge, customer data analysis, and structured deliverable generation into a single assistant that CSMs can use throughout their entire workflow.

## Capabilities

| Capability | What it does |
|-----------|-------------|
| **Zendesk Q&A** | Answers product questions with research-backed responses, sourced and referenced. Covers features, configuration, troubleshooting, workflows, plan availability, and best practices. |
| **Transcript Analysis** | Reads call transcripts, extracts customer goals with direct quotes, and cross-references against account data when available. |
| **Recommendations** | Builds prioritized, dependency-ordered recommendations grounded in customer goals, account data, and team playbooks. |
| **Slide Guide** | Maps recommendations to specific slides in the Scaled CS deck and CTA decks, organized by presentation flow. |
| **Success Plan** | Generates a customer-facing success plan with goals, strategies, resources, measurable outcomes, and next steps. Fits on one slide. |
| **Customer Email Drafting** | Writes ready-to-send emails based on research already done. Matches the customer's language automatically. |
| **Data Analysis (via Datifyer)** | Hands off Google Sheet workbooks to Datifyer for account performance summaries, channel mix, benchmarks, and ROI projections. |
| **Smart Plan Detection** | Identifies the customer's Zendesk plan from context before researching, ensuring answers are accurate for that specific plan. |

## Guardrails

| Guardrail | How it works |
|-----------|-------------|
| **Never fabricates data** | If a source doesn't confirm it, SAGE doesn't say it. Missing data is labeled "N/A." |
| **Never invents recommendations** | Every recommendation traces back to at least one confirmed source. |
| **Hedges when uncertain** | Strong evidence is stated as fact. Weak evidence is flagged: "appears available but verify in the instance." |
| **Source attribution on every answer** | Every claim references where it was found (Help Center article, Jira ticket, team playbook). CSMs can verify. |
| **Escalation awareness** | Recognizes when a question is out of CSM scope (bugs, security, billing, complex implementations) and advises holding off until the right team confirms. Offers to draft the escalation. |
| **Internal process boundary** | Does not answer internal business process questions (sales qualification, compensation, pipeline procedures). Redirects to the appropriate team. |
| **Confidential content flagging** | Flags Google Drive documents marked as confidential, internal only, or draft before surfacing their content. |
| **Conversation isolation** | Each new customer query starts fresh. No assumptions carry over between different customers in the same conversation. |

## What SAGE Is Connected To

| Source | What it provides | When SAGE uses it |
|--------|-----------------|-------------------|
| **Z2 Help Center** | Official Zendesk product documentation, setup guides, release notes, plan requirements | Every question (primary source) |
| **Unleash (Internal KB)** | Jira tickets, Slack threads, internal worklogs, known bugs | Troubleshooting and bug-related questions only |
| **Google Drive** | Team playbooks, comparison charts, CTA decks, past solutions | Recommendations, plan comparisons, team knowledge requests |
| **Tavily** | Explore recipes, community workarounds, developer docs, marketplace apps | Reporting questions, API/developer questions, content the Help Center doesn't cover |

SAGE routes to the right source based on the question type. Simple product questions use only the Help Center. Complex or ambiguous questions pull from multiple sources and cross-reference.

## Value

| Area | Impact |
|------|--------|
| **Speed** | A simple Zendesk question that used to take over a minute now resolves in seconds. Full workflows (transcript to success plan) complete in roughly half the time. |
| **Consistency** | Every CSM gets the same research depth, the same source hierarchy, the same evidence standards. Output quality doesn't depend on who's asking. |
| **Accuracy** | Answers are grounded in sources, not general knowledge. When SAGE can't confirm something, it says so instead of guessing. |
| **CSM time saved** | Research, recommendations, slide matching, success plans, and email drafting happen in one conversation instead of across multiple tools. |
| **Onboarding** | New CSMs get the same quality of research and recommendations as experienced ones from day one. |

## Main Use Cases

**1. Pre-call preparation**
CSM pastes a Google Sheet link. SAGE hands off to Datifyer, which generates an account summary with metrics, benchmarks, product adoption, channel mix, and opportunities. CSM walks into the call prepared.

**2. Post-call workflow**
CSM pastes the call transcript. SAGE extracts goals, builds recommendations, matches slides, generates a success plan, and drafts a follow-up email. One conversation covers the entire post-call workflow.

**3. Day-to-day Zendesk questions**
CSM asks about a feature, configuration, or troubleshooting issue. SAGE researches across Help Center and (when needed) internal KB, then provides a sourced answer with clear next steps. Can draft a customer reply on the spot.

**4. Customer email drafting**
CSM pastes bullet points, notes, or a customer email. SAGE (or Quill as a standalone agent) drafts a ready-to-send reply in the customer's language, matching cultural tone and professional norms.

**5. Plan and feature comparisons**
CSM asks what's included in a specific plan or whether a feature is available. SAGE checks comparison charts, Help Center docs, and internal notes, then provides a clear answer with plan-specific context.
