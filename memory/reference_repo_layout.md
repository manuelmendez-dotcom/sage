---
name: repo-layout-and-versioning-workflow
description: SAGE repo structure (prompts/ trunk + reference/ context + memory/) and the version-bump workflow Manuel adopted on the 2026-05-18 reset.
metadata:
  type: reference
---
**Layout:**
```
SAGE/
├── CLAUDE.md         ← project context (THIS file's authoritative source)
├── prompts/          ← live trunks: sage_v3.0.md, datifyer_v3.0.md
├── reference/        ← supporting: SAGE_Overview, CHANGELOG, promptsmith skill, payper_* regression sessions
├── memory/           ← Claude Code auto-memory
└── .gitignore
```

`prompts/` is the only folder whose contents drive live LibreChat behavior. One trunk per agent. Experiments live in a `.gitignore`'d sandbox directory, never alongside trunks.

**Version-bump workflow (forward, post-2026-05-18 reset):**

1. Edits land directly in the V3.0 file unless they're material.
2. Bump (V3.1, V3.2…) on material change: refactor, render-shape change, math change, new mode. Cosmetic edits / typos / wording polish do NOT bump.
3. Bump procedure: `cp prompts/{agent}_v3.0.md prompts/{agent}_v3.1.md` → edit new file → both coexist while new is in test → once rolled out in LibreChat, `git rm` old file → update CLAUDE.md path reference.
4. Commit convention: `sage: <change>`, `datifyer: <change>`, or `repo: <change>`.
5. `git push origin main` after every shipped edit. Remote = disaster recovery.

**Why this shape (vs prior `Versions/production/` + `Versions/old/` + staging files):**
The prior shape had multiple "production" markers (`_production.md`, `_v3.1.md`, `_v3.0_main_prompt.md`) that disagreed on which file was authoritative, plus `Extras/` mixing live skills with screenshots, RTFs, MP4s, and conversation logs. Manuel collapsed it to one trunk per agent + one curated reference dir. Easier to reason about, easier to disaster-recover, no ambiguity on which file LibreChat is running.

**Internal version qualifiers banned in prompts.**
After the reset, prompts no longer contain "retired in v3.2" / "new in v3.2" / "v3.1 emoji anchors" phrasing. Each rule states what IS, not what changed. History lives in git, not in the prompt body. When bumping, do NOT reintroduce historical qualifiers — write the new rule clean.

Related: [[project_sage_v3]], [[project_datifyer_v3]].
