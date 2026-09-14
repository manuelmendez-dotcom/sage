# Optional source selection

Use this reference when the user requests the source menu, asks to choose sources before research, or sets a conversation-wide source preference. Ordinary questions proceed through the existing router without a menu.

## Menu behavior

Show a short conversational menu when asked, using the user's language. No source calls are needed to display it. Do not claim to create a permanent app control or saved setting.

| Choice | Research behavior |
|---|---|
| Automatic | Select the smallest relevant source set for the question; do not search everything. |
| Community only | Research and base the answer on Zendesk Community evidence only. |
| Community + official verification | Start with Community, then verify material product claims through Z2 and, where useful, official Zendesk web documentation. |
| Choose sources | Select any combination of Z2 Help Center, Zendesk Community, Official web documentation, Slack, Unleash, Google Drive, or Zendeskdev. |
| Supplied content only | Interpret the evidence already provided without new searches or browser retrieval. |

If the user asks to see all individual sources, expand the Choose sources row. Describe Tavily and browser access as tools, not additional evidence sources. Official web documentation means the appropriate official Zendesk domains and a relevant vendor's official documentation when the question requires it.

If a question accompanies an explicit request to choose first, retain the question and wait for the selection before researching. Continue that question when the selection arrives. A source selection without a question needs only an acknowledgement and an invitation to paste the inquiry.

An explicit source instruction with a question bypasses the menu. `Use Community and Z2` authorizes exactly those two sources; it does not automatically select the broader Community + official verification preset. `Community only` chosen from this menu includes an evidence constraint as described in its row. A literal `search Community only` follows the existing search-only rule and can still use relevant evidence already in context unless the user excludes it.

## Preference lifetime

- Current explicit instructions override an earlier preference for the current inquiry. A no-search instruction takes precedence over a stored research preference.
- Keep a question's source restrictions through its related follow-ups. A new unrelated question returns to Automatic unless the user explicitly set a conversation-wide preference.
- `For this conversation, use Community only` applies across questions in this task until changed. Track this in conversation context; do not edit global settings or promise persistence in other tasks.
- A one-question override does not erase a conversation-wide default unless the user says to replace it. `Go back to automatic` clears the earlier source preference.
- When expanding beyond a restricted set is already explicitly authorized, proceed without asking again. Otherwise identify the useful next source and request expansion only if needed.

## Examples

- `What is the difference between triggers and automations?` → Automatic; usually Z2 is sufficient.
- `Use Community only and base your answer exclusively on its discussions: [question]` → Community research and Community evidence only.
- `Find community examples, then verify the proposed solution with Z2` → Community followed by Z2.
- `A community post says this works. Is it true?` → Supplied community evidence, not a source lock; validate through the normal router.
- `Start with Community` → Search Community; do not call another source without permission.
- `Show sources before researching this: [question]` → Menu first; preserve the pending inquiry.
