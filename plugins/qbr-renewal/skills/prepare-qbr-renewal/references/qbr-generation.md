# QBR website generation and Google Slides delivery

This module incorporates the qbr-express skill in this single plugin. Use it for
account selection, generation, conversion and delivery; the coordinating skill
handles the renewal brief and product recommendations.

Generate customer QBRs through https://qbr-express.internal.zenai-apps.com/ (Customer Success Content Hub). Use the live website as the authority for available options. The default deliverable is one converted, native Google Slides presentation per requested account in the root of My Drive, readable through the Drive connector for later queries and reuse. The generated PPTX is a temporary conversion input, not a second deliverable. Preserve the generated content; do not redesign or rewrite the deck.

## Customer and settings

- Use the customer name or instance domain from the request. Search Accounts and match the legal account name, instance domain, instance account ID, and CSM where available. Select only the intended account. Ask for clarification when several plausible matches remain.
- If the site reports no owned accounts, its unrestricted search can still locate the customer. Do not interpret an empty owned-account list as absence of an account.
- Keep QBR deck selected. Preserve user-requested settings; otherwise use current site defaults and briefly state this assumption. For this plugin, enable the site’s owned-products-only option unless the user explicitly requests another product scope. Confirm its live UI state before generation; do not infer ownership from product names. Preserve other site defaults and do not infer special periods, brands or customer context.
- Fill Prepared by from established user context or the site. A displayed account CSM alone does not prove the presenter's identity. Do not invent a title. Leave optional fields empty when unknown.
- Supporting files and customer context are optional. Include them only when supplied or requested for this run.
- Optional brand trends may require CX Reports and Dashboards permissions. Standard generation can proceed without brand trends. Do not request new permissions as part of an ordinary QBR run. If brand trends were requested, explain the access blocker.

## Browser operation

Use the website through the available browser/computer-use tools and their current documentation. Do not use QBR MCP, a bridge, Local Delivery, direct endpoint calls or token extraction for account lookup, generation or downloads. Supported Drive upload/read connectors can still handle delivery and verification. Keep browser activity in the background unless the user needs to interact.

Use existing matching tabs when available. The site's Okta SSO and Google sign-in may resolve automatically after initial loading states. Check the resulting page before treating authentication as blocked. If user authentication is required, preserve the tab for handoff and explain the specific blocker.

Ground controls in fresh accessibility or DOM observations. Do not reuse element indices, browser tab IDs, sign-in state URLs, or download locations from a previous run.

## Generate and download

1. Confirm the intended account is selected and the settings match the request.
2. Click Download selected deck (the label may differ for multiple accounts). A single account produces an editable `.pptx`; multiple accounts may produce a `.zip`.
3. Monitor generation until the site reports completion or a concrete failure. Progress can take several minutes. Use bounded waits and meaningful updates. Do not click Generate again while an existing request is running.
4. Inspect the final status for data warnings as well as completion. A downloaded deck can still contain incomplete data. Report the affected area and useful error detail without claiming the content has been validated.
5. Locate the newly downloaded file using the exact filename reported by the site and verify it exists. Do not substitute an older similarly named QBR. Continue to Google Slides conversion by default. Keep the local PPTX available until conversion and verification finish; retaining or linking it is not part of default completion. If conversion is blocked, retain the working file for recovery and report the blocker without presenting the PPTX as completed Slides delivery. Honor an explicit local-only request.

An observed example was a successful download accompanied by a Snowflake error in “New Data” for invalid identifier `AI.IS_AI_AGENT_REMOVED`. Treat this only as an example of a partial-data warning, not an expected error or a reason to regenerate automatically. Backend SQL failures need attention from the site owner; this skill does not repair them.

## Upload for Google Slides conversion

This plugin’s default is Google Slides only: one converted presentation in My Drive, with no duplicate PowerPoint left in the destination. A normal QBR request includes conversion, verification, and moving any temporary Drive PPTX created by this run to Trash after verification. Do not stop at download or upload, or ask for the destination again. Use a different folder when specified. Honor explicit alternatives such as local-only, no upload, upload-only, PPTX-only, or keeping both formats. Verify the intended Google account before uploading.

1. Open Google Drive and verify the signed-in account is the intended destination account.
2. Navigate to the requested folder. For My Drive, use its root, even if a seemingly relevant folder such as Automated QBRs is visible.
3. Prefer a supported upload/import action that directly creates native Google Slides without retaining a separate Drive PPTX. Otherwise, use New > File upload with the exact downloaded file as a temporary conversion input. For browser automation, read the current file-upload documentation and use its supported file chooser API with the absolute local path. Avoid native clipboard shortcuts when the browser disables them.
4. Wait for “upload complete.” A 100% transfer indicator accompanied by “Finishing upload” is not yet completion. On an uncertain result, inspect Drive before retrying to avoid duplicates.
5. Locate the uploaded file and capture its exact file ID or URL, filename, and location so any temporary PPTX can be identified for cleanup. Continue to conversion and verification. For a multi-account ZIP, inspect members, reject unsafe paths, and extract only the intended decks locally without executing contents; upload and convert each requested account’s PPTX; deliver one native presentation per account.

## Native Google Slides conversion and verification

Verify the native presentation before removing the temporary Drive PPTX. Opening a PowerPoint in the Slides editor is not conversion, and upload alone does not complete this workflow.

1. If the upload did not already create a native presentation, open the temporary PPTX in Google Slides and use the live UI’s conversion action, typically File > Save as Google Slides. Do not change Drive’s global upload-conversion setting.
2. Keep the customer or instance name and report date in the native copy’s name so future searches distinguish reporting versions. Preserve the source name without the `.pptx` suffix, or append “Google Slides” if necessary for clarity. Capture the new file’s URL. Inspect existing matching files before retrying a conversion whose outcome is uncertain; reuse a verified matching copy rather than creating duplicates.
3. Verify the new file is native Google Slides. With the Drive connector, search by the report name and confirm MIME type `application/vnd.google-apps.presentation`. A `docs.google.com/presentation/...` URL alone is insufficient: Drive also uses these URLs for Office files. The source PPTX has MIME type `application/vnd.openxmlformats-officedocument.presentationml.presentation`.
4. Read the native copy through the available presentation-reading connector (currently `gdrive_get_presentation`). For large decks, an outline response is only an index: follow its slide selector to read actual slide content. Verify representative substantive slides, including a metrics/table slide and a narrative/product slide when present. Confirm the returned text corresponds to the customer and report. A successful search alone does not establish readability.
5. Compare source and converted slide counts, and inspect representative converted charts, tables, and dense slides for obvious conversion loss. Reuse source slide extraction or rendering tools where available. This is a conversion check, not a new editorial or business-data review. If the connector omits chart values or information embedded in images, state that limitation; visually inspect or render the native Slides presentation when a later question depends on those details. Image-only chart values are a text-extraction limitation, not a reason to retain a duplicate Drive PPTX when the visuals are preserved. Do not claim every metric or presenter note is retrievable from a text export.
6. Preserve any material generation warnings in the native file as described below, then complete the temporary-file cleanup. If conversion, substantive connector reading, or visual verification is blocked or shows material content loss, keep the temporary PPTX for recovery and report what remains incomplete. Do not regenerate or create duplicate conversions automatically.

The Google Drive desktop app exposed through computer use and the Drive content connector are different capabilities. Use the browser/app for uploading and conversion when no suitable write connector exists, and use the content connector to verify later retrieval. The currently available presentation reader supports native Google Slides, not uploaded PPTX files. PDF conversion does not solve this reader’s limitation.

For deck-only requests, do not create an additional summary, PDF or permanent PPTX deliverable by default. For renewal/discovery requests, continue into the coordinating skill’s evidence review and brief after deck delivery; the brief remains part of that requested output. Use the native Slides presentation as the source for later queries, including visual inspection of embedded details. When the user later requests analysis or another artifact, retrieve relevant slides and cite their numbers and the Slides link; do not rely solely on a past chat summary.

## Temporary-file cleanup

After successful native-format, content, slide-count, and visual verification, move only the temporary Drive PPTX created by this run to Trash. Identify it by its captured file ID or URL, not by filename alone. Verify that it is trashed and the native Slides presentation remains in the intended destination. Do not empty Trash, remove older files, or delete user-supplied originals. If the upload created only a native presentation, no Drive cleanup is needed.

Local PPTX downloads are working files, not required retained artifacts or final links. No second local copy is needed. If cleanup is blocked, preserve the files and disclose the remaining duplicate instead of claiming that Google Slides-only delivery is complete. An explicit request to retain the PPTX overrides this cleanup.

## Data warnings and scope

Carry forward material generation warnings in the handoff. When generation reports a warning, also preserve it in the native file’s description if editable, or in a clearly labeled internal source note on the first slide’s speaker notes. Identify the affected area and exact useful error detail without changing the customer-facing slide content. Verify that the warning was saved; if this cannot be done, disclose that it is recorded only in the handoff. Do not infer that upload, conversion, or a successful text read repairs incomplete data.

This workflow does not authorize sharing, changing access permissions, sending messages, or inventing missing figures. Keep known data warnings separate from new conversion or extraction limitations.

## Completion

Default completion requires one verified native Google Slides presentation per requested account in the intended destination, a successful connector read of actual slide content, conversion checks, and any temporary Drive PPTX from this run moved to Trash. The local original and a separate Drive PPTX are not required deliverables. For deck-only delivery, provide the Google Slides link or links, material unresolved warnings or limitations, and the coordinating skill’s optional follow-ups. When renewal/discovery preparation was requested, include the brief as well. Do not include PowerPoint or local download links unless requested. If a stage is blocked, state what exists and what remains incomplete. Complete any explicitly requested alternative format accurately.
