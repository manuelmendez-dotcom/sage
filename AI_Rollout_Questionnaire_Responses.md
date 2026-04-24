# AI Rollout Questionnaire — SAGE Responses

*Responses to questions 1-7, grounded in the current state of `sage_openai_v1_main_prompt.md` and `Datifyer_openai_v1.md`. Questions 8-10 are organizational and to be answered by the business owner.*

---

## 1. Use cases approved for the pilot and what is out of scope

SAGE is approved for four primary use cases in the pilot, each with a specific purpose:

**Q&A Mode — for both CSM questions and customer-originated content**
- Direct CSM product questions (feature behavior, integrations, configuration how-to, troubleshooting, best practices, workflow questions).
- Customer-email analysis: a CSM pastes an email or a screenshot of a customer message, SAGE researches across sources and produces an answer the CSM can use to draft a reply. After Q&A, SAGE offers to draft the reply directly (Communication Mode).

**Deliverable Mode — structured outputs from a call transcript**
- Transcript Analysis (Goals Analysis) with customer-language category headers.
- Recommendations tied to stated customer needs.
- Slide Guide matching recommendations to deck content.
- Success Plan (customer-facing) with slide-ready goals and outcomes.
- Post-call summary emails.

**Configuration Guide Mode — step-by-step setup guidance for a specific customer**
- Workflow-specific guides (SLAs, routing, Copilot, triggers, macros, intents, etc.) grounded in the Help Center.
- Includes per-account variability lines and "verify in instance" flags to prevent blind execution.

**Data Mode (Datifyer, specialist handoff) — account data analysis and ROI**
- Reads Google Sheet workbooks, Account Insights Hub PDFs, Excel, CSV, pasted tables, and dashboard screenshots.
- Produces a standardized 5-section summary (Snapshot, the story right now, the numbers, what to probe on the call, menu).
- Generates customer-ready ROI with customer-language pillar headers, whole-number rounding, and calibrated assumptions.

**Out of scope:**

- **Internal business processes:** sales qualification criteria, CSQL definitions, compensation rules, pipeline procedures, internal team operations, segment policies. SAGE redirects these to the relevant team.
- **Legal, compliance, or security policy interpretation.**
- **Commitments on behalf of the customer or Zendesk:** SAGE drafts, the CSM commits.
- **Autonomous customer communication:** SAGE never sends email or posts on behalf of a CSM. All customer-facing output is a draft reviewed and sent by the CSM.
- **Roadmap commitments:** SAGE will not confirm anything about unreleased features. Redirects to product for roadmap questions.
- **Unverified packaging claims:** SAGE will not state that a capability is "included on your plan" without confirmed plan and verified availability (Constraint #23). Exception: AI agent packaging framing under Constraint #21 (approved messaging from Zendesk's April 2026 announcement).
- **Recommendations not tied to something the customer said:** no generic best practices padded in. No consulting-style process advice ("map your workflow," "align ownership") in Recommendations tables.
- **Content generation for non-CSM use cases:** SAGE is scoped to Scaled CS workflows. Other teams' use cases (marketing copy, engineering documentation, legal review, etc.) are not supported.

---

## 2. Data sources SAGE uses, and source of truth when they conflict

SAGE uses four knowledge sources, each called for specific question types (not all on every query):

- **Z2 Help Center** — official Zendesk product documentation. Primary source for product truth, feature behavior, plan requirements, setup guides, release notes.
- **Unleash** — internal knowledge base: Jira tickets, Slack threads, internal worklogs, configuration edge cases. Not product documentation; used for troubleshooting, bugs, known issues, routing quirks.
- **Google Drive** — team playbooks, comparison charts, CTA decks, presentations. Used for recommendations, slide guides, and "what have we done before" questions.
- **Tavily** — scoped public web: Explore recipes, community workarounds, developer documentation, marketplace listings. Used only for content Z2 does not cover.

**Source hierarchy when sources conflict:**

1. Z2 Help Center = baseline, what Zendesk officially says.
2. Unleash = reality check. If Unleash contradicts Z2, Unleash wins (it reflects actual customer experience).
3. Google Drive = experience layer. Document age is flagged when content appears outdated.

**One documented exception:** Constraint #21 (AI Product Truth — the April 2026 AI agent rollout) supersedes all other sources for AI agent packaging and capability gating. Any internal document or Help Center article describing AI Advanced as gated is treated as outdated.

---

## 3. How SAGE handles uncertainty or missing information

SAGE has explicit rules against fabricating or inferring beyond what sources support:

- **Never fabricate data.** Missing values: "N/A (not visible in source)."
- **Never invent recommendations.** Every recommendation is grounded in at least one confirmed source. No match: "No documented playbook for this."
- **Never present uncertain information as fact.** If SAGE cannot confirm something in a source, it does not say it. Silence beats a guess.
- **Strong vs. weak evidence handling.** Strong Z2 evidence (setup guide, config steps): stated as fact. Weak evidence (list mention, changelog line, table checkmark): SAGE adds one secondary source to verify, or hedges ("This appears available but I'd suggest verifying in the instance"). Conflicting evidence: adds a third source as tiebreaker; if still unclear, flags to the CSM.
- **No unverified packaging claims.** SAGE will not say "included on your plan" or "no plan change required" without confirmed plan and verified availability. It hedges explicitly when uncertain.
- **Recent Z2 articles flagged.** Articles created or updated in the last 60 days are flagged with "⚠️ Recently published, verify accessibility before sharing with customer" because they may be pre-release draft content.
- **Negative retrieval calibration.** When SAGE searches for an item and doesn't find an article, it does NOT say "not supported." It says "I did not retrieve a dedicated article in this search — that does not necessarily mean it isn't supported. Worth a targeted check."

---

## 4. Known failure modes and limitations

Named honestly, with current mitigations:

- **Retrieval non-determinism on Unleash and Tavily.** The same question on different runs can surface different edge-case threads because search ranking on large dynamic indexes isn't fully deterministic. Mitigation applied: when Unleash or Tavily broad search fires, SAGE runs two query variants in parallel (one on the specific feature term, one on the general operational concept) to improve retrieval coverage. This reduces variance but does not eliminate it.

- **Draft Help Center content behind login walls.** Zendesk's Help Center has a "NEW CONTENT FOR REVIEW" section containing draft articles at regular public-looking URLs. The Z2 MCP does not currently expose section metadata, so SAGE cannot deterministically identify which articles are draft. Mitigation applied: SAGE uses a 60-day recency heuristic — any article created or updated recently is flagged as potentially pre-release. Customer-facing outputs (Success Plan resources, email drafts, post-call summary email links) omit flagged URLs entirely. This over-flags some genuinely public recent articles but reliably catches the draft ones. A request has been raised to expose section metadata in the Z2 MCP for deterministic detection.

- **Extraction from image-heavy sources is low-confidence.** Screenshot and scanned-PDF inputs to Datifyer get an explicit "verify against source" flag on every value, because OCR reliability varies.

- **Plan detection depends on GPT-5.4 reading intent correctly on edge cases.** A pronoun like "they" without a named customer may be read as either customer-referenced or abstract. Defensive default: when ambiguous, SAGE asks for plan. Preserves integrity at the cost of an occasional unnecessary ask.

- **Language mixing (reported on the prior Sonnet-era prompt).** The current OpenAI variant has stricter language rules — consistency within output is enforced, no English fallback in non-English threads. Not directly re-tested on GPT-5.4 yet for short conversational phrases; if it resurfaces, additional rules will be added to explicitly ban mid-sentence code-switching.

- **Industry context depends on CSM confirmation.** SAGE asks for the customer's website once per session to tailor probes and recommendations. If the CSM skips, output falls back to generic-but-data-grounded. SAGE never guesses the customer's industry from a name alone.

---

## 5. Customer-facing outputs requiring human review before use

**Every customer-facing SAGE output is a CSM draft, not an autosend.** The CSM reviews and sends. SAGE explicitly labels drafts as drafts, asks for adjustment preferences, and never commits to sending.

Specific customer-facing outputs:

- **Success Plan** — pasted onto a customer slide by the CSM. SAGE enforces short goals (2-5 words), short outcomes (3-6 words), one-slide fit. The CSM edits before pasting.
- **Email drafts (Communication Mode)** — returned to the CSM for review. After drafting, SAGE asks: "Want me to adjust the tone, length, or focus?" The CSM sends.
- **Post-call summary emails** — same review flow as email drafts.
- **Configuration Guides** — technically CSM-facing, but often shared with customers verbatim. Per-account variability lines and "verify in instance" flags are included so the CSM knows where customer-specific values must be confirmed before the guide is used.

**Datifyer's ROI output is customer-ready by default** (customer-language pillar headers, whole-number rounding, single-currency tables, clean assumptions line) but still delivered to the CSM first. The CSM reviews and decides what to share.

No SAGE output is sent directly to a customer without CSM review.

---

## 6. Guardrails for sensitive data, hallucinations, and unsupported recommendations

**Anti-hallucination guardrails (prompt-level):**

- Constraint #1: Never fabricate data.
- Constraint #2: Never invent recommendations.
- Constraint #3: Never present uncertain information as confirmed fact.
- Source provenance rule (Datifyer): every displayed value must trace to the current-session source or an explicit CSM input. Never to conversation memory or inferred defaults. Prevents silent carryover from one session to another.
- Strict ROI input discipline (Datifyer): required commercial inputs (country, seat count, plan tier) must be extracted from source or explicitly provided by the CSM. If missing, Datifyer stops and asks with a single targeted question. Never defaults silently.

**Anti-unsupported-recommendation guardrails:**

- Recommendations must tie to at least one customer-stated goal. No generic best practices padded in.
- No consulting-style items ("map your workflow," "align ownership") in Recommendations tables. Every recommendation must name a Zendesk capability, feature, app, or documented approach.
- Scoping/framing goals don't generate product recommendations; they're surfaced in Key Insight or "What's already working" notes.
- Configuration Guide steps must trace to a specific Z2 article. Steps that can't be grounded are flagged "verify in instance" rather than invented.
- Placeholder discipline: invented tag names, group names, intent values are phrased as placeholders ("a tag of your choice, e.g., `agent_copilot_enabled`"), never as literals Zendesk expects.

**Anti-unverified-packaging-claim guardrail (Constraint #23):**

SAGE cannot say "included on your plan" or "no plan change required" without both: (a) customer's plan and add-ons confirmed, and (b) availability verified in Z2, internal KB, or the instance. The only exception is AI agent packaging under Constraint #21 (approved official messaging).

**Sensitive data:**

SAGE's prompt does not collect, store, or transmit customer data outside the session. Session content remains within the LibreChat deployment. The prompt does not have explicit PII-handling rules — this sits at the LibreChat infrastructure layer and should be reviewed separately by whoever owns that infrastructure. CSMs should be informed (via guidance outside the prompt) not to paste highly sensitive data (customer credentials, payment details, health information, etc.) into any AI tool.

**MCP reliability guardrail:**

Required MCPs per task type are enforced. If a required MCP (e.g., Z2 for Configuration Guide) fails, SAGE stops and asks the CSM to reconnect rather than produce a partial or memory-based output. This override is not negotiable via CSM request.

**Transparency layer:**

Every load-bearing SAGE output (standalone Q&A, Configuration Guide, customer-email analysis) ends with a Sources & Confidence block that explicitly lists sources consulted, gaps, escalation needed, and which MCPs were reached this run. CSMs can audit the methodology at any time. Mid-deliverable factual follow-ups include a compact "MCPs reached this turn" line for lightweight method transparency without ceremony.

---

## 7. How users know what they should not put into the tool

**Today, this guidance lives outside the prompt itself** — in the SAGE Overview document, the CHANGELOG, and any onboarding materials the team provides to CSMs. The prompt does not surface warnings to the user during session use.

**What SAGE actively refuses to do (visible to CSMs through SAGE's own responses):**

- Answers internal business process questions (sales qualification, CSQL definitions, compensation rules, pipeline procedures, internal team operations, segment policies) are redirected to the relevant team with a short message. SAGE will not answer these even if asked.
- SAGE will not produce a Configuration Guide without a confirmed customer plan. It stops and asks.
- SAGE will not produce a Recommendations deliverable without required sources (Z2 + Google Drive). It stops and asks the CSM to reconnect MCPs.
- SAGE will not make unverified packaging claims. It hedges explicitly when uncertain.

**What SAGE does NOT warn users about at session time (gap worth naming):**

- Pasting raw customer PII (names, emails, account IDs in bulk) is not blocked or warned against by the prompt. CSMs need to know through training, not through in-product warnings, that they should avoid pasting sensitive customer data unnecessarily.
- Pasting authentication credentials, API keys, or passwords is not blocked or warned against. Training responsibility.
- Sharing SAGE output externally (outside the CSM's direct customer engagement) is not controlled by the prompt. Training and policy responsibility.

**Recommendation:** a short CSM-facing usage policy should accompany rollout, covering what data types are acceptable to paste, how to handle SAGE outputs externally, and how to report sensitive-data concerns. This policy sits alongside the prompt, not inside it.

---

## 8. Ownership end to end

**Ownership:** Manuel Méndez (Scaled CSM, Zendesk) — designer, prompt author, and current maintainer. Owns the end-to-end feedback loop: observation, diagnosis, prompt fix, re-test, redeploy. Business value sits with Scaled CS leadership; operational ownership sits with the maintainer.

**Support perspective:** Issues, questions, and feedback route directly to the maintainer. Diagnosis and fix are typically same-day; the prompt is versioned on GitHub and updated in LibreChat without a code deploy.

**Known limitation to name:** Single-owner dependency. This is efficient for pilot iteration but is a bus-factor risk. A documented secondary owner or handover plan is a natural next step for broader rollout.

---

## 9. Feedback and issue reporting process, and how quickly changes can be made

**Feedback:** A formalized Google Forms questionnaire shared with the Scaled CSM team. The form captures issue description, the specific SAGE output that prompted the report, and any context the CSM wants to include. Submissions route to the maintainer.

**Change speed:** Fast. Typical cycle: feedback received → triage → root-cause identified in the prompt → prompt edit applied in the versioned file (GitHub-tracked) → re-test in a cloned agent → updated prompt re-pasted into the live SAGE or Datifyer agent in LibreChat.

- **Low-complexity fixes** (wording, rule clarifications, scope adjustments): typically same-day.
- **Substantial changes** (new spec block, mode refactor): 1-3 days depending on testing depth.
- **No code deploy required.** LibreChat picks up the updated system prompt on the next session.

**Known limitations:**
- Single-maintainer cycle; response time depends on the maintainer's availability.
- Feedback captures issues from CSMs. Customers do not interact with SAGE directly; customer-facing issues surface through the CSM.
- No automated monitoring of output quality today. Problem detection relies on CSM reports.

---

## 10. Process for problems during rollout — adjust prompts, remove sources, restrict use cases, pause rollout

**Mechanism — what can be changed and how:**

- **Adjust the prompt** — edit `sage_openai_v1_main_prompt.md` or `Datifyer_openai_v1.md`, re-test in a cloned agent, re-paste the updated prompt into the live agent in LibreChat. No code deploy required.
- **Remove or restrict a source** — adjust the source routing spec in the prompt to deprioritize, scope, or exclude a specific MCP for specific task types. The required-vs-optional MCP matrix controls which sources are mandatory per mode.
- **Restrict a use case** — narrow the Mode Detection table, tighten a Constraint, or add explicit "out of scope" language. A specific use case can be turned off without affecting the rest of the prompt.
- **Pause rollout** — disable the SAGE or Datifyer agent in LibreChat, or swap the system prompt back to the previous production version (v2.4 sonnetized line, preserved and frozen on GitHub). Rollback is a single re-paste, typically under 10 minutes.

**Authority:**

- **Low-risk changes** (prompt refinement, wording fixes, new rule additions, incremental feature scoping): the maintainer acts directly.
- **Higher-risk changes** (disabling a mode, pausing the rollout entirely, removing a source used across many scenarios, scope changes affecting customer-facing output): sign-off from Scaled CS leadership is expected before action.

**Versioning and rollback:**

All prompt changes are committed to GitHub with descriptive commit messages. Every previous version is preserved and recoverable. Rolling back is a single `git checkout` of the prior version plus a re-paste into LibreChat.

**Known limitations:**
- Rollback is manual (prompt text swap). No automated blue/green deployment. Acceptable at pilot scale; may need formalization for broader rollout.
- Issue detection depends on CSMs reporting via the Google Forms questionnaire. No automated output-quality monitoring today.
- Single-maintainer authority for low-risk changes; sign-off dependency for high-risk. Both bottleneck on maintainer availability.
