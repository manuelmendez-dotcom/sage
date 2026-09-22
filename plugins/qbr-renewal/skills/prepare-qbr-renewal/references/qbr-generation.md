# Generate and save a QBR

Discover tools by capability; namespaces may differ. Prefer this plugin's QBR and
delivery tools if duplicates exist. Never generate through two namespaces.

1. Call `get_qbr_capabilities`. Use supported options and actual current schemas;
   do not invent section names or parameters.
2. Call `search_qbr_accounts` with the name, subdomain or supplied ID. Identify
   account name, subdomain and instance account ID. Ask which match only when
   ambiguous; do not substitute a similarly named parent/subsidiary/instance.
3. Call `start_qbr_deck` with resolved `account_ids` and
   `owned_product_sections_only: true` unless explicitly requested otherwise.
   Retain standard sections and the service's standard timeline unless the user
   supplies dates or exclusions. Never invent presenter details or custom context.
   Ownership filtering is not proof that every retained feature is included/active.
4. Preserve the job ID/settings in local working notes. Poll
   `get_qbr_generation_status` about every 20–45 seconds while running, giving
   user updates. Retry transient status reads with backoff using the same ID.
   A failed/unknown status is not permission to start another generation job.
5. When ready, use `download_qbr_artifact` for metadata, then
   `save_qbr_artifact` with job ID, returned filename and expected byte size if
   available. It saves to `~/Generated QBRs`, verifies the transfer and returns a
   SHA-256. Only its verified path establishes that the file was saved. For ZIP
   outputs inspect members, reject unsafe paths and extract only the intended
   report to working files; never execute contents.
6. Link the saved report. Distinguish PPTX/PDF/ZIP from native Google Slides; do
   not claim an upload occurred. Continue to the brief if requested; otherwise
   offer the three optional follow-ups.

`start_qbr_one_pager` creates a separate service template. Discover supported
types/languages when requested; it is not automatically a substitute for this
plugin's evidence-reviewed renewal/discovery brief.

For authentication failure, name the affected connection and have the CSM complete
their own company sign-in; never inspect/share token caches. Retry a failed
download with the existing job, not new generation. Existing reports still support
brief creation. Account search/capabilities alone cannot substantiate account
trends, benchmarks or adoption conclusions.
