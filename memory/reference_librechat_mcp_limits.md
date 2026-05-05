---
name: LibreChat MCP detection limits
description: LibreChat does not expose MCP connection state to agents. Any reliability improvements in SAGE must be reactive, based on tool-call responses.
type: reference
originSessionId: cd2e15b6-737e-4614-ab77-5755bf620879
---
**Verified in LibreChat codebase (2026-04-20) via agent research:**

Connection state (`connected` / `connecting` / `disconnected` / `error`) lives in:
- `packages/api/src/mcp/connection.ts` (MCPConnection)
- `packages/api/src/mcp/MCPManager.ts` (MCPManager)
- Surfaced only via REST endpoint `getServerConnectionStatus` in `api/server/services/MCP.js` (line 809)
- Consumed by UI component `client/src/components/MCP/MCPServerStatusIcon.tsx`

**NOT exposed to the agent:**
- No system-prompt injection of MCP state
- No tool the model can call to query status
- No runtime signal when a server disconnects mid-conversation

**What the agent CAN observe:**
- Server unavailable at tool-registration time → LibreChat registers `createUnavailableToolStub` (api/server/services/MCP.js line 108). Model sees a normal tool, call returns an "unavailable" message.
- Server drops mid-conversation → `reconnectServer` attempt at line 293, failure surfaces when the agent invokes the tool.

**Implication for SAGE design:** All MCP reliability logic must be reactive (based on tool-call response) or behavioral (asking CSM to confirm upfront). Proactive status gates are not possible without LibreChat changes.

**Docs consulted:**
- https://www.librechat.ai/docs/features/mcp
- https://www.librechat.ai/docs/configuration/librechat_yaml/object_structure/mcp_servers
