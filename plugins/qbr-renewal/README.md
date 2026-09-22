# QBR Conversations

Bring your own QBR PowerPoint or PDF. The plugin analyzes it and directly prepares
a concise CSM conversation brief for a renewal or discovery meeting.

## What you get

- **Value already realised:** supported wins, comparable YoY trends and industry
  peer context, with clear limits where evidence is missing.
- **Focus areas and next value moves:** up to three priorities tied to account
  evidence, relevant Zendesk capabilities, measures and prerequisites.
- **Meeting preparation:** a short talk track, discovery questions and one proposed
  next step. Detailed CSM source notes stay separate.

The default is a 450–650 word brief in the conversation. No menu or additional
confirmation comes before analysis. Ask for a document if needed, or request a
narrower analysis of a particular metric or priority. The supplied file remains
unchanged. Follow-up questions reuse its reviewed evidence.

If no file is provided, the plugin asks for it. It does not generate QBRs, search
Drive for customer reports, operate the QBR website, or upload/convert/deliver a
new deck. You can also explicitly provide an existing native Google Slides link
as the source. Multiple ambiguous reports or an unreadable source may require
one clarification.

## Install in one go

On a Mac with Codex, paste this command into Terminal:

```bash
curl -fsSL https://raw.githubusercontent.com/manuelmendez-dotcom/sage/main/install-qbr.sh | bash
```

Restart Codex and open a new task. Attach your QBR PowerPoint or PDF and select
QBR Conversations. Google Drive and Z2 support recommendation research; sign in
when needed. Browser access and QBR website sign-in are not required. The installer
does not grant company service or document permissions.

The plugin contains **one coordinating skill and two research connections:
Google Drive and Z2 Help Center**. Colleagues do not need separate personal skills,
a QBR MCP, Pomerium bridge or Local Delivery plugin.

The installer automatically obtains an official Codex CLI when needed and a
managed Python for setup. The bundled PPTX extractor uses Python's standard
library. Setup files stay under `~/.local/share/qbr-renewal`; no sudo or shell-
profile changes are required. Fresh setup needs no preinstalled Homebrew,
Python, Git or Terminal CLI.

The same command updates the plugin and retires recognised obsolete QBR MCP,
Local Delivery and private bridge components from earlier versions. SAGE,
unrelated connections, shared tools, credentials and customer reports are
preserved. Legacy source folders may remain on disk but are not installed.

Existing clean local SAGE checkouts update by fast-forward on `main`; modified
checkouts, other branches and other origins are preserved with an explanatory
error. New installs use a managed repository snapshot. Apple Silicon is tested;
Intel download checksums are provided but not tested on an Intel Mac. The
installer does not support Windows/Linux.

Advanced options: `QBR_RENEWAL_SOURCE_DIR` selects a local snapshot;
`QBR_RENEWAL_DATA_HOME` selects the setup directory; `QBR_CODEX_BIN` selects a CLI.
Normal setup requires none of these. Review the [installer](../../install-qbr.sh)
if desired.

## Start a task

Attach the report and use one of these prompts:

> Analyze this QBR and prepare a one-page renewal conversation brief.

> Use this file to explain value already realised, focus areas and product-linked
> next value moves. Include YoY and industry peers where supported.

> Help me prepare for discovery using this QBR. What should I explore with the customer?

## Sources and evidence

| Module | Role and sources |
| --- | --- |
| value-conversation evidence method | Reviews the supplied QBR, including charts, notes, definitions and recent trends. Replaces the original five-slide default with the conversation brief. |
| cxrecommendations approach | Refreshes the live Scaled CS master and relevant supporting decks; uses official Zendesk documentation to validate product/plan claims. |
| whatsnew approach | Selectively checks What's New and Announcements through Z2 for newer capabilities, rollout and EAP/GA questions. |

Recommendations connect an account signal to an action, relevant capability,
expected operational benefit, measure and prerequisite. Owned products are not
assumed to be activated. Product names are research leads, not a fixed catalogue.
There are no invented benchmarks, ROI promises or unverified entitlements.

Account results come from the supplied report and dated user context. Product
research does not replace missing account data. Report warnings and material
coverage gaps stay visible in the analysis and separate CSM source notes without
editing the original. Image-only values require visual review. An explicit
report-only request limits analysis to that report and leaves current product
availability unverified.

Customer files, internal deck copies and credentials stay outside the plugin
repository. Analysis does not include cloud uploads, deletion, sharing,
permission changes, customer messages or instance configuration.

## Troubleshooting and validation

| Situation | Next step |
| --- | --- |
| No report is supplied | Attach or identify the QBR PowerPoint/PDF to analyze. A customer name alone does not provide performance data. |
| Source is unreadable or account identity is unclear | Clarify the source; accessible portions can be reviewed with stated gaps. No substitute report is generated or searched for. |
| Drive or Z2 research is unavailable | Continue with accessible account evidence and label affected product recommendations conditional. |
| User supplies a Google Slides link without access | Restore access to that specific source or provide a local PowerPoint/PDF. |
| Old generation behavior remains in an open task | Restart Codex and open a new task after updating. |
| Local SAGE changes prevent update | Save the changes and update the checkout, then rerun. The installer does not reset or stash work. |

Automated checks cover safe marketplace updates, retirement of recognised legacy
QBR components, preservation of unrelated configuration, actual Codex installation
and PPTX evidence extraction. Behavioral acceptance scenarios cover supplied-file
analysis, missing sources and the brief in [the evaluation guide](../../evals/qbr-renewal/cases.md).
These checks do not prove every customer report is fully readable or every
colleague has access to the research sources.

Uninstall through Codex plugin settings, or run
`codex plugin remove qbr-renewal@zendesk-scaled-cs` when the CLI is on PATH.
SAGE and supplied customer files remain in place.
