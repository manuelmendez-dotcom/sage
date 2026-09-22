# Zendesk Scaled CS plugins

Two independently installable Codex plugins share this repository and the
**Zendesk Scaled CS** marketplace:

| Plugin | Use it for |
| --- | --- |
| [SAGE CSM Q&A](plugins/sage-zendesk-qa) | Zendesk product and workflow questions, with automatic or selected research sources. |
| [QBR & Renewal Brief](plugins/qbr-renewal) | Customer QBR decks and concise renewal/discovery preparation. |

Installing QBR & Renewal Brief does not replace or uninstall SAGE.

## Install QBR & Renewal Brief on a Mac

Prerequisites: current Codex with plugin CLI support, Zendesk access, and the
[company QBR bridge](https://docs.google.com/document/d/1cdcSGinExD8K5Ydu7RCLnkU28ZQoXVxf_BvEgrlSlmo/edit).
The bridge requires a one-time company-authenticated download. If it is already
installed, no second bridge installation is needed.

Paste this in Terminal:

```bash
curl -fsSL https://raw.githubusercontent.com/manuelmendez-dotcom/sage/main/install-qbr.sh | bash
```

Then restart Codex, start a new task, and complete your own service sign-ins.
Try: **“Prepare a QBR and a one-page renewal brief for [customer], using owned
products only.”**

The same command updates this plugin. Read the
[setup, source policy and troubleshooting guide](plugins/qbr-renewal/README.md)
for details. Source code is downloadable here; access to Zendesk services and
internal decks remains controlled by each colleague's company account.
