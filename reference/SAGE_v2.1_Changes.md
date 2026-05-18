# SAGE v2.1 — What Changed and Why

## The Problem
SAGE v2.0 was accurate but slow. CSMs reported long wait times, especially for simple questions. A basic Zendesk question that should take seconds was taking over a minute.

## Root Cause
SAGE was searching every knowledge source for every question, regardless of whether those sources had anything useful to contribute. A simple "how do I set up triggers?" question triggered the same full research cycle as a complex troubleshooting case.

## What We Changed

### 1. Smarter Research (biggest impact)

**Before:** Every question searched all four sources (Help Center, Internal KB, Google Drive, Tavily) every time. Most of those searches returned nothing useful for simple questions.

**Now:** SAGE classifies the question first, then only calls the sources that can actually contribute. This is how each source is used:

**Z2 Help Center (always first, every question)**
The primary source for all product knowledge. SAGE starts here and, for straightforward questions, stops here if the answer is clear and detailed. This alone resolves the majority of everyday Q&A.

**Unleash / Internal KB (only for troubleshooting and bugs)**
This source searches Jira tickets, Slack threads, and internal worklogs. It does not contain product documentation (that's the Help Center's job). SAGE only calls it when the question signals a bug, a known issue, or something "not working." This avoids redundant searches on simple product questions.

**Google Drive (only for team knowledge)**
Playbooks, comparison charts, CTA decks, and past solutions. SAGE calls it when building recommendations, looking up plan comparisons, or when the CSM asks about past approaches. It always surfaces the most recently modified documents first, and flags any content that appears outdated. It is never used as a source for product capabilities.

**Tavily (only for content the Help Center doesn't cover)**
Explore recipes, community workarounds, developer/API docs, and marketplace apps. SAGE calls it only when the question type needs these specific sources, using faster search settings by default.

**How this protects accuracy:** SAGE still verifies answers using multiple sources when the question warrants it. Troubleshooting questions still get cross-referenced against Jira. Recommendations still pull from team playbooks. The difference is that simple, well-documented questions no longer waste time searching sources that have nothing to add.

**Result:** Simple questions use 2-3 searches instead of 7-11. Roughly 3x faster for everyday Q&A, with no reduction in answer quality for complex questions.

### 2. Removed Unnecessary Handoff

**Before:** When a CSM asked SAGE to draft an email, SAGE prepared the content and then handed off to a separate agent (Quill) to write it. Two agents processing the same conversation.

**Now:** SAGE writes the email directly. One agent, one pass.

**Result:** Email drafts are 15-45 seconds faster.

### 3. Optimized Web Search Settings

**Before:** Every web search used the slowest, most thorough setting.

**Now:** Web searches default to fast mode and only escalate to thorough when fast results are thin. Also introduced two new search tools for specific use cases (developer docs and multi-topic research) that get better results in fewer calls.

**Result:** Each individual search is faster, and fewer searches are needed overall.

### 4. Step Budget

**Before:** No limit on how many searches SAGE would run. Complex questions could exhaust the system's step limit mid-research, producing incomplete answers.

**Now:** SAGE allocates searches proportionally based on question complexity, ensuring it always has enough steps to finish the response.

**Result:** Fewer incomplete responses. More predictable performance.

### 5. Reduced Prompt Size

Removed duplicated instructions and dropped an unused research tool (Researcher MCP). The prompt is shorter, which means the model processes less text on every single interaction.

**Result:** Every step is ~20-30% faster to process.

### 6. Model and Infrastructure Change

**Before:** SAGE ran on Claude Sonnet 4.6 through AWS Bedrock. Every interaction was routed through an extra infrastructure layer (LibreChat → AWS Bedrock → Anthropic) that added latency on every single step. With SAGE making 5-20 steps per query, this overhead compounded significantly. It also caused connection errors (NGHTTP2_INTERNAL_ERROR) on complex queries where the payload grew too large for Bedrock's default timeout settings.

**Now:** SAGE runs on GPT 5.4 through a direct API connection (LibreChat → OpenAI). No intermediary, no extra routing layer, no timeout issues.

The prompt and research logic are the same. What changed is the path the model uses to receive and respond to each step. Same brain, faster road.

**Result:** Noticeably faster across all interactions, and the connection errors on complex queries are resolved.

## What Didn't Change

- **Accuracy model:** The same 7-phase research and verification process. The same source hierarchy. The same evidence quality standards.
- **All modes:** Q&A, Transcript Analysis, Recommendations, Slide Guide, Success Plan, Communication — all still work the same way.
- **Datifyer integration:** Sheet analysis still hands off to Datifyer as before.
- **Output format:** Same structure, same Sources & Confidence block, same checkpoints.

## Performance Impact

Early testing shows noticeable speed improvements across all modes:

- **Simple Q&A:** Roughly 3x faster. The most common query type sees the biggest gain because it now uses only the Help Center instead of all four sources.
- **Troubleshooting:** Roughly 2x faster. Still cross-references Jira, but skips sources that don't contribute.
- **Email drafts:** Noticeably faster. One agent handles the full flow instead of two.
- **Full workflows (transcript to success plan):** Significantly faster end-to-end due to fewer tool calls at every stage.

Actual times will vary depending on query complexity, number of topics, and MCP response times. The improvement comes from doing less unnecessary work, not from cutting corners on research.

## Next Steps

- Monitor accuracy on the new model for 1-2 weeks. If you notice anything that feels different from before (less precise answers, different tone, longer responses), flag it so we can adjust.
- Consider reducing the model's thinking budget from 2000 to 1024 tokens for additional speed gains (test separately).
- Model configuration tuning (temperature, top_p) can be explored as a follow-up.
