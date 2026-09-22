import asyncio
import contextlib
import io
from pathlib import Path
import sys
import unittest
from unittest.mock import AsyncMock, patch

import anyio
import httpx
from mcp import ClientSession, types

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "mcp"))
import qbr_proxy
import server as delivery


class ProxyTests(unittest.IsolatedAsyncioTestCase):
    async def test_connection_check_only_discovers_tools_without_generating(self):
        upstream = AsyncMock()
        names = ["get_qbr_capabilities", "search_qbr_accounts", "start_qbr_deck", "get_qbr_generation_status", "download_qbr_artifact"]
        upstream.list_tools.return_value = types.ListToolsResult(tools=[types.Tool(name=name, inputSchema={"type": "object"}) for name in names])

        @contextlib.asynccontextmanager
        async def connected():
            yield upstream

        with patch.object(qbr_proxy, "upstream_session", connected):
            status = await qbr_proxy.check_connection()
        self.assertTrue(status["connected"])
        self.assertEqual("ready", status["status"])
        upstream.list_tools.assert_awaited_once()
        upstream.call_tool.assert_not_awaited()

    async def test_authentication_rejection_is_reported_without_private_details(self):
        response = httpx.Response(401, request=httpx.Request("POST", qbr_proxy.QBR_URL + "/mcp"))
        error = httpx.HTTPStatusError("private-token", request=response.request, response=response)

        @contextlib.asynccontextmanager
        async def rejected():
            raise ExceptionGroup("private-authentication-details", [error])
            yield

        with patch.object(qbr_proxy, "upstream_session", rejected):
            status = await qbr_proxy.check_connection()
        self.assertFalse(status["connected"])
        self.assertEqual("authentication_rejected", status["status"])
        self.assertEqual(401, status["http_status"])
        self.assertNotIn("private", str(status))

    async def test_incomplete_server_catalogue_is_not_reported_ready(self):
        upstream = AsyncMock()
        upstream.list_tools.return_value = types.ListToolsResult(tools=[])

        @contextlib.asynccontextmanager
        async def connected():
            yield upstream

        with patch.object(qbr_proxy, "upstream_session", connected):
            status = await qbr_proxy.check_connection()
        self.assertFalse(status["connected"])
        self.assertIn("start_qbr_deck", status["missing_tools"])
        upstream.call_tool.assert_not_awaited()

    async def test_local_diagnostic_remains_available_when_remote_authentication_fails(self):
        server_write, client_read = anyio.create_memory_object_stream(20)
        client_write, server_read = anyio.create_memory_object_stream(20)
        app = delivery.mcp._mcp_server
        with patch.object(qbr_proxy, "pomerium_token", side_effect=qbr_proxy.QbrSignInError("private-token")):
            async with anyio.create_task_group() as group:
                group.start_soon(app.run, server_read, server_write, app.create_initialization_options())
                async with ClientSession(client_read, client_write) as client:
                    await client.initialize()
                    listing = await client.list_tools()
                    diagnostic = next(tool for tool in listing.tools if tool.name == "check_qbr_connection")
                    self.assertTrue(diagnostic.annotations.readOnlyHint)
                    result = await client.call_tool("check_qbr_connection", {})
                    self.assertEqual("sign_in_required", result.structuredContent["status"])
                    self.assertFalse(result.structuredContent["connected"])
                    self.assertNotIn("private-token", str(result))
                group.cancel_scope.cancel()

    async def test_tool_discovery_and_results_survive_real_mcp_exchange(self):
        upstream = AsyncMock()
        upstream.list_tools.side_effect = [
            types.ListToolsResult(tools=[types.Tool(name="get_qbr_capabilities", inputSchema={"type": "object"})], nextCursor="next"),
            types.ListToolsResult(tools=[types.Tool(name="start_qbr_deck", inputSchema={"type": "object", "properties": {"account_ids": {"type": "array"}}, "required": ["account_ids"]})]),
        ]
        remote_result = types.CallToolResult(content=[types.TextContent(type="text", text="Job queued")], structuredContent={"job_id": "synthetic"}, isError=False)
        upstream.call_tool.return_value = remote_result
        proxy = await qbr_proxy.make_proxy(upstream)
        server_write, client_read = anyio.create_memory_object_stream(20)
        client_write, server_read = anyio.create_memory_object_stream(20)
        async with anyio.create_task_group() as group:
            group.start_soon(proxy.run, server_read, server_write, proxy.create_initialization_options())
            async with ClientSession(client_read, client_write) as client:
                await client.initialize()
                listing = await client.list_tools()
                self.assertEqual(["get_qbr_capabilities", "start_qbr_deck"], [t.name for t in listing.tools])
                result = await client.call_tool("start_qbr_deck", {"account_ids": [123]})
                self.assertEqual(remote_result, result)
                self.assertEqual(1, upstream.call_tool.await_count)
                upstream.call_tool.return_value = types.CallToolResult(content=[types.TextContent(type="text", text="Access denied")], isError=True)
                error = await client.call_tool("get_qbr_capabilities", {})
                self.assertTrue(error.isError)
                self.assertEqual(2, upstream.call_tool.await_count)
            group.cancel_scope.cancel()

    async def test_authentication_stays_on_original_origin(self):
        seen = []

        def handle(request):
            seen.append(request)
            return httpx.Response(302, headers={"Location": "https://other.example/auth"})

        async with qbr_proxy.authenticated_client("synthetic-token", transport=httpx.MockTransport(handle)) as client:
            result = await client.get(qbr_proxy.QBR_URL + "/mcp")
        self.assertEqual(302, result.status_code)
        self.assertEqual(1, len(seen))
        self.assertEqual("synthetic-token", seen[0].headers["X-Pomerium-Authorization"])
        self.assertIn("_pomerium=synthetic-token", seen[0].headers["Cookie"])

    async def test_repeated_pagination_is_rejected(self):
        upstream = AsyncMock()
        upstream.list_tools.return_value = types.ListToolsResult(tools=[], nextCursor="same")
        with self.assertRaises(RuntimeError):
            await qbr_proxy.make_proxy(upstream)
        self.assertEqual(2, upstream.list_tools.await_count)


class ProxyErrorTests(unittest.TestCase):
    def test_connection_error_does_not_expose_credential_output(self):
        stream = io.StringIO()
        with patch.object(sys, "argv", ["qbr_proxy"]), patch.object(qbr_proxy, "serve", AsyncMock(side_effect=RuntimeError("private-token"))), contextlib.redirect_stderr(stream):
            self.assertEqual(1, qbr_proxy.main())
        self.assertNotIn("private-token", stream.getvalue())


if __name__ == "__main__":
    unittest.main()
