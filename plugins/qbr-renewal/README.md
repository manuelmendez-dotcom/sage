# QBR & Renewal Brief

One plugin generates a customer QBR through the QBR Express website, delivers a
verified native Google Slides presentation, and prepares a concise CSM renewal
or discovery brief.

## What you get

- **QBR deck:** the site's generated content, limited to owned product sections by
  default, converted into one native Google Slides presentation per account in
  the root of My Drive. Explicit format and folder choices take precedence.
- **CSM brief:** value already realised, comparable YoY/industry context, focus
  areas, up to three product-linked next value moves, measures, discovery
  questions and one proposed next step. Detailed CSM source notes stay separate.
- **Follow-ups:** a deck-only request offers the brief, account exploration or a
  focused presentation. A renewal-preparation request continues directly to the
  brief without waiting for a menu choice.

The default brief appears in the conversation. Ask for a file if needed. The
working PPTX supports conversion and evidence review; it is not a second default
deliverable. Temporary Drive PPTX files created by the run are moved to Trash only
after native format, substantive content, slide counts and visuals are verified.
Supplied originals and older reports are preserved.

## Install in one go

On a Mac with Codex, paste this command into Terminal:

```bash
curl -fsSL https://raw.githubusercontent.com/manuelmendez-dotcom/sage/main/install-qbr.sh | bash
```

Restart Codex and open a new task with browser/computer-use access. Complete your
own QBR website/Okta, Google and research-connector sign-ins when needed. The
installer does not grant company service or document permissions.

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
| qbr-express | Website account selection, generation and download; Google Slides conversion, native-format/content/visual verification and temporary-file cleanup. |
| value-conversation evidence method | Reviews the QBR, including charts, notes, definitions and recent trends. Replaces the original five-slide default with the requested brief. |
| cxrecommendations approach | Refreshes the live Scaled CS master and relevant supporting decks; uses official Zendesk documentation to validate product/plan claims. |
| whatsnew approach | Selectively checks What's New and Announcements through Z2 for newer capabilities, rollout and EAP/GA questions. |

Recommendations connect an account signal to an action, relevant capability,
expected operational benefit, measure and prerequisite. Owned products are not
assumed to be activated. Product names are research leads, not a fixed catalogue.
There are no invented benchmarks, ROI promises or unverified entitlements.

The QBR website controls available settings. Generation warnings remain visible
in the handoff and, when editable, native file metadata or internal speaker notes.
Conversion does not repair missing source data. A Slides URL alone does not prove
conversion: the workflow checks the native MIME type and reads actual slides
through the Drive connector. Image-only values need visual review.

The package contains instructions, research connections and a local extractor;
it contains no customer reports, internal deck copies or credentials. Normal
requests permit delivery into the intended user's Drive, not external sharing,
permission changes, customer messages or instance configuration.

## Troubleshooting and validation

| Situation | Next step |
| --- | --- |
| Browser access is unavailable | Enable Codex browser/computer-use access or supply an existing report for the brief. Do not reinstall a QBR MCP or bridge. |
| The QBR website requires sign-in | Complete your own sign-in in the preserved browser tab, then continue the same run. |
| Generation/download is uncertain | Inspect the existing request and exact new download before retrying. Do not start a duplicate job. |
| Conversion or verification is blocked | Keep the working PPTX for recovery and report the incomplete stage; do not call it completed Slides delivery. |
| Drive is unavailable | Restore Drive access for default Slides delivery; an explicit local-only request can still proceed. |
| Z2/product sources are unavailable | Preserve the measured account story and label affected product recommendations conditional. |
| Old QBR tools remain in an open task | Restart Codex and open a new task after updating. |
| Local SAGE changes prevent update | Save the changes and update the checkout, then rerun. The installer does not reset or stash work. |

Automated checks cover safe marketplace updates, removal of recognised legacy
QBR components, preservation of unrelated configuration, actual Codex installation
and evidence extraction. Behavioral acceptance cases cover website generation,
Slides conversion and the brief in [the evaluation guide](../../evals/qbr-renewal/cases.md).
These package checks do not establish a fresh end-to-end customer generation or
every colleague's browser/Google permissions.

Uninstall through Codex plugin settings, or run
`codex plugin remove qbr-renewal@zendesk-scaled-cs` when the CLI is on PATH.
SAGE and generated reports remain in place.
