# Zendesk Scaled CS plugins

Two independently installable Codex plugins share this repository and the
**Zendesk Scaled CS** marketplace:

| Plugin | Use it for |
| --- | --- |
| [SAGE CSM Q&A](plugins/sage-zendesk-qa) | Zendesk product and workflow questions, with automatic or selected research sources. |
| [QBR Conversations](plugins/qbr-renewal) | Analyze your QBR file and prepare a renewal/discovery conversation brief. |

Installing QBR Conversations does not replace or uninstall SAGE.

## Install QBR Conversations on a Mac

Bring your own QBR PowerPoint or PDF. The plugin analyzes it and directly prepares
a one-page conversation brief. Google Drive and Z2 support recommendation research.
No QBR website access, browser workflow, QBR MCP, bridge or Local Delivery plugin
is needed.

Paste this in Terminal:

```bash
curl -fsSL https://raw.githubusercontent.com/manuelmendez-dotcom/sage/main/install-qbr.sh | bash
```

Then restart Codex, start a new task, and attach your QBR file.
Try: **“Analyze this QBR and prepare a one-page renewal conversation brief.”**
Complete your own research-service sign-ins when needed.

The same command updates this plugin and retires the old QBR Local Delivery
plugin, its marketplace, and the recognised standalone QBR MCP connection. SAGE
and unrelated connections remain in place. Read the
[setup, source policy and troubleshooting guide](plugins/qbr-renewal/README.md)
for details. Source code is downloadable here; access to Zendesk services and
internal decks remains controlled by each colleague's company account.
