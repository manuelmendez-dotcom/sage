# QBR Conversations

One plugin generates a customer QBR through the QBR Express website, delivers the
PowerPoint file, and offers a concise CSM conversation brief for renewal or discovery.

Every new QBR or renewal-preparation request generates and downloads a fresh deck
from the website, even if you ran it for the same customer minutes ago. It does
not first search Drive for an older customer deck. Each run retains its actual
download without overwriting earlier files. Ask explicitly to use an existing
report when that is what you want. Follow-up questions and recovery of an
unfinished run continue with that run's report.

## What you get

- **QBR deck:** the site's generated PPTX, limited to owned product sections by
  default, with a clickable file link after a basic readability and identity check.
- **CSM brief:** value already realised, comparable YoY/industry context, focus
  areas, up to three product-linked next value moves, measures, discovery
  questions and one proposed next step. Detailed CSM source notes stay separate.
- **Follow-ups:** the same response that delivers the PPTX offers **Prepare the
  one-page conversation brief** (recommended) and **Explore the account results**.
  The CSM chooses. A renewal-preparation or deck-and-brief request continues
  directly to the brief without waiting for a menu choice.

The default brief appears in the conversation. Ask for a file if needed. Analysis
uses the delivered PPTX directly. Default delivery has no Drive upload, Slides
conversion, timestamped rename, speaker-note editing or file deletion. A request
for a different format or destination can be handled explicitly. The handoff
does not stop for housekeeping approval; supplied originals and older reports
are preserved.

The website settings are checked immediately before each generation:

| Setting | Default |
| --- | --- |
| Include customer stories | Unchecked |
| Only include product sections customers have | Checked |
| Usage | Unchecked |
| Appendix | Unchecked |
| What's new | Unchecked |

You can explicitly override these settings for a particular deck. The What's new
deck section is excluded; selective release research still informs the brief.

## Install in one go

On a Mac with Codex, paste this command into Terminal:

```bash
curl -fsSL https://raw.githubusercontent.com/manuelmendez-dotcom/sage/main/install-qbr.sh | bash
```

Restart Codex and open a new task with browser/computer-use access. Complete your
own QBR website/Okta sign-in. Google Drive and Z2 support research for a requested
brief or explicitly selected sources; they are not required for PPTX delivery.
The installer does not grant company service or document permissions.

**No QBR MCP, Pomerium bridge or QBR Local Delivery plugin is required.** The
website workflow is bundled here; colleagues do not need personal copies of any
of the four contributing skills. The plugin page shows **one skill and two
research connections: Google Drive and Z2 Help Center**. Neither generates QBRs.

The installer automatically obtains an official Codex CLI when needed and a
managed Python for setup. Its portable evidence extractor uses only Python's
standard library. It installs no QBR server, Python package environment or
Pomerium component. Setup files stay under `~/.local/share/qbr-renewal`; no sudo
or shell-profile changes are required. Fresh setup needs no preinstalled
Homebrew, Python, Git or Terminal CLI.

The same command updates the plugin. When migrating from the previous release,
it removes the recognised standalone QBR MCP connection, the separate
`qbr-local-delivery@qbr-express-local-delivery` plugin and its unused marketplace,
and this installer's old delivery runtime and private bridge components.
SAGE, unrelated connections, shared system tools, credentials and customer
reports are preserved. The original local delivery source folder may remain on
disk, but it is no longer installed or registered as a plugin.

Existing clean local SAGE checkouts update by fast-forward on `main`; modified
checkouts, other branches and other origins are preserved with an explanatory
error. New installs use a managed repository snapshot. Apple Silicon is tested;
Intel download checksums are provided but not tested on an Intel Mac. This
installer does not support Windows/Linux.

Advanced options: `QBR_RENEWAL_SOURCE_DIR` selects a local snapshot;
`QBR_RENEWAL_DATA_HOME` selects the setup directory; `QBR_CODEX_BIN` selects a CLI.
Normal setup requires none of these. Review the [installer](../../install-qbr.sh)
if desired.

## Start a task

> Create a QBR for [customer], using only the products they own.

> Prepare a QBR and one-page brief for [customer]'s renewal meeting.

> Use this existing QBR to explain value already realised and next value moves.
> Include YoY and industry peers where supported. No new slides.

## The combined workflow

| Module | Role and sources |
| --- | --- |
| qbr-express adaptation | Website account selection, fresh generation and download; basic PPTX checks and file delivery, followed by the brief/results choice. |
| value-conversation evidence method | Reviews the QBR, including charts, notes, definitions and recent trends. Replaces the original five-slide default with the requested brief. |
| cxrecommendations approach | Refreshes the live Scaled CS master and relevant supporting decks; uses official Zendesk documentation to validate product/plan claims. |
| whatsnew approach | Selectively checks What's New and Announcements through Z2 for newer capabilities, rollout and EAP/GA questions. |

Recommendations connect an account signal to an action, relevant capability,
expected operational benefit, measure and prerequisite. Owned products are not
assumed to be activated. Product names are research leads, not a fixed catalogue.
There are no invented benchmarks, ROI promises or unverified entitlements.

The QBR website controls available settings. Generation warnings appear beside
the file link and carry into the brief and CSM source notes when relevant. The
original PPTX remains unchanged. Basic file checks do not establish that all
business data is complete. A requested brief reviews substantive content,
including charts, notes and definitions; image-only values need visual review.

The package contains instructions, research connections and a local extractor;
it contains no customer reports, internal deck copies or credentials. Normal
requests deliver a local PowerPoint. Cloud uploads, external sharing, permission
changes, customer messages and instance configuration are outside that default.

## Troubleshooting and validation

| Situation | Next step |
| --- | --- |
| Browser access is unavailable | Enable Codex browser/computer-use access or supply an existing report for the brief. Do not reinstall a QBR MCP or bridge. |
| The QBR website requires sign-in | Complete your own sign-in in the preserved browser tab, then continue the same run. |
| Generation/download is uncertain | Inspect the existing request and exact new download before retrying. Do not start a duplicate job. |
| Download is missing, corrupt or for the wrong account | Explain the file problem and preserve the active run for recovery; do not substitute an older deck. |
| Drive is unavailable | Deliver the PPTX and next-step options normally. Disclose affected research gaps only if a brief is requested. |
| A readable deck has a source-data warning | Deliver the file with a short warning and the brief/results options; do not edit the deck to record the warning. |
| Z2/product sources are unavailable | Preserve the measured account story and label affected product recommendations conditional. |
| Old QBR tools remain in an open task | Restart Codex and open a new task after updating. |
| Local SAGE changes prevent update | Save the changes and update the checkout, then rerun. The installer does not reset or stash work. |

Automated checks cover safe marketplace updates, removal of recognised legacy
QBR components, preservation of unrelated configuration, actual Codex installation
and evidence extraction. Behavioral acceptance cases cover website generation,
PPTX delivery, the follow-up choice and the brief in [the evaluation guide](../../evals/qbr-renewal/cases.md).
These package checks do not establish a fresh end-to-end customer generation or
every colleague's browser/Google permissions.

Uninstall through Codex plugin settings, or run
`codex plugin remove qbr-renewal@zendesk-scaled-cs` when the CLI is on PATH.
SAGE and generated reports remain in place.
