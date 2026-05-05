---
name: Manuel pressure-tests recommendations before shipping
description: Manuel consistently pushes back on proposed changes with "is this necessary?" / "logic?" / "latency/friction?" questions. Over-engineering gets caught.
type: feedback
originSessionId: cd2e15b6-737e-4614-ab77-5755bf620879
---
**Rule:** Before proposing prompt changes, pressure-test each item against three criteria: is it necessary, is the logic sound, does it add too much latency or friction. Drop items that don't pass all three.

**Why:** Manuel caught a proposed 3-layer MCP reliability design (preflight ping + required/optional classification + health line). Preflight ping was over-engineered: 3-5 seconds added to every heavy task to catch rare failures. He asked the three questions directly and the first layer didn't survive. The other two did.

**How to apply:** When proposing multi-part prompt changes, self-audit each part against those three criteria before presenting. If I present without filtering, he'll filter for me and we'll discard parts that should have been dropped upfront. Default to leaner proposals. When in doubt, ship the smallest change that solves the actual failure, not the comprehensive change that covers adjacent risks.
