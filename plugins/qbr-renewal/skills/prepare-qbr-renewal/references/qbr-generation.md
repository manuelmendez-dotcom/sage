# QBR website generation and PowerPoint delivery

This module adapts qbr-express for this plugin: generate through the website and
deliver the downloaded PPTX. The coordinating skill handles the optional brief.
Its PPTX default takes precedence over the standalone skill's Slides workflow.

Use https://qbr-express.internal.zenai-apps.com/ (Customer Success Content Hub).
Deliver one fresh PowerPoint per requested account with a clickable local file
link. Keep the generated content unchanged. Default delivery requires no Drive
upload, Slides conversion, timestamped rename or deletion.

## Fresh extraction for every new request

Start every new QBR or renewal/discovery-preparation request at the website and
generate/download a fresh deck, even minutes after a completed run for the same
account. Do not search Drive for a prior customer deck or ask whether to reuse
one. Unchanged metrics do not cancel a new request; a fresh extraction does not
prove the underlying data has refreshed. Preserve actual reporting periods.

Reuse a report only for an explicit request to use it, an explicit no-generation
request, or follow-up analysis/refinement of the current results. Within one
active run, continue the same job through download and recovery; status checks
and retries do not create extra jobs. Research for a requested brief may retrieve
product source decks through Drive; it does not replace the fresh extraction.

## Customer and settings

- Use the customer name or instance domain from the request. Search Accounts and match the legal account name, instance domain, instance account ID, and CSM where available. Select only the intended account. Ask for clarification when several plausible matches remain.
- If the site reports no owned accounts, its unrestricted search can still locate the customer. Do not interpret an empty owned-account list as absence of an account.
- Keep QBR deck selected and apply the checkbox defaults below. Explicit settings requested by the user for this run take precedence. Preserve other site defaults; do not infer special periods, brands or customer context, or infer product ownership from product names.
- Fill Prepared by from established user context or the site. A displayed account CSM alone does not prove the presenter's identity. Do not invent a title. Leave optional fields empty when unknown.
- Supporting files and customer context are optional. Include them only when supplied or requested for this run.
- Optional brand trends may require CX Reports and Dashboards permissions. Standard generation can proceed without brand trends. Do not request new permissions as part of an ordinary QBR run. If brand trends were requested, explain the access blocker.

### Default checkboxes

| Website control | Required state |
| --- | --- |
| Include customer stories | Unchecked |
| Only include product sections customers have | Checked |
| Usage | Unchecked |
| Appendix | Unchecked |
| What's new | Unchecked |

Observe each control's actual checked state and set it explicitly; do not blindly
toggle controls or assume the site remembers a previous run. After selecting or
changing accounts, recheck all five states immediately before generation because
the page may reset them. If a control is missing or its state cannot be verified,
report the specific blocker before generating; do not silently use site defaults.

Excluding the What's new deck section does not disable selective release research
for the renewal brief. The recommendation and release-check modules still apply.

## Browser operation

Use available browser/computer-use tools and their current documentation. Do not
use QBR MCP, a bridge, Local Delivery, direct endpoint calls or token extraction
for account lookup, generation or downloads. Keep browser activity in the
background unless the user needs to interact.

Use an existing matching tab when available. The site's Okta SSO may resolve
automatically after initial loading states; check the resulting page before
reporting an authentication blocker. If sign-in is required, preserve the tab for
handoff and explain the specific blocker. Google sign-in is not a prerequisite
for default PPTX delivery.

Ground controls in fresh accessibility or DOM observations. Do not reuse element
indices, tab IDs, sign-in URLs or download paths from a previous run.

## Generate and download

1. Confirm the intended account and all five checkbox states above, applying
   explicit user overrides for this run.
2. Click Download selected deck (the label may differ for multiple accounts).
   A single account produces `.pptx`; multiple accounts may produce `.zip`.
3. Monitor the same generation until completion or a concrete failure. Use bounded
   waits and meaningful updates. Do not click Generate again while it is running.
4. Capture any source-data warnings as well as completion. A successful download
   can contain incomplete data; retain that distinction in the handoff.
5. Locate this run's actual new download using the observed request, download time
   and path, including any browser-added filename suffix. Do not substitute an
   older similarly named QBR or infer freshness from filename alone. If it landed
   in a temporary browser cache, copy it to a persistent task output folder outside
   plugin/source repositories. Keep its filename; use a separate run folder to
   avoid overwriting earlier files. Verify the final link points to that file.
6. For a multi-account ZIP, inspect members and extract only the intended PPTX
   files to the task output folder, rejecting absolute/traversal paths and links.
   Do not execute archive contents. Deliver each requested account's PPTX.

If a completed run's download fails, inspect/retry that download without starting
a duplicate job. A site query failure may require its owner to fix it; do not
repair backend SQL or regenerate automatically.

## Basic file check and delivery

Confirm the file is nonempty and its PPTX package/slide XML is readable, with a
positive slide count and customer identity consistent with the selected account.
Use the bundled `scripts/extract_qbr.py` (relative to the skill) without media
extraction for a quick inventory if useful. Keep that inventory for a later brief.
This is a file/identity check, not a full business-data or visual review. Do not
render or analyse the entire deck for a deck-only request. If identity cannot be
confirmed from text, inspect the opening slide rather than guessing.

Deliver the retained PPTX as a clickable file link, using its absolute path in
Codex. File download and basic checks complete deck-only delivery. Do not open
Drive, create Slides, rename cloud files, edit speaker notes, or move files to
Trash as part of this default flow. Keep the file available for the next step.
Honour an explicit request for a different format or cloud destination using
available tools; it is not a prerequisite for PowerPoint delivery.

## Warnings and the next step

Put any material generation warning in one short note beside the file link,
identifying the affected section and useful error detail. Preserve the original
PPTX; do not modify its notes or metadata to record the warning. Carry the warning
into separate CSM source notes and the brief when relevant. For example, a failure
of the site's New Data query on `AI.IS_AI_AGENT_REMOVED` is a source-data gap,
not a reason to withhold a readable deck or skip the next-step offer. Report only
warnings actually observed in this run.

The same final response must offer **Prepare the one-page conversation brief**
as the recommended next step and **Explore the account results** as an alternative,
using the coordinating skill's follow-up controls or a short numbered list. The
user chooses whether to continue after a deck-only request. Do not end with an
approval question about filenames, uploads or cleanup.

If renewal preparation, a summary or a conversation brief was already requested,
continue directly to evidence review of this PPTX and deliver the requested brief
along with the file link. Do not ask whether to start or generate another deck.
If the new file is missing, corrupt or for the wrong account, report the actual
blocker rather than claiming delivery. Missing Drive/Z2 access does not block
PowerPoint delivery; it affects only research-dependent recommendations.
