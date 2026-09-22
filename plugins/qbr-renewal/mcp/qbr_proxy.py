"""Bundled stdio connection to QBR Express; no separate pom-mcp-bridge binary."""
from __future__ import annotations

import argparse
import asyncio
from contextlib import asynccontextmanager
from datetime import timedelta
import logging
import sys

import httpx
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client
from mcp.server import Server
from mcp.server.stdio import stdio_server

from qbr_auth import QBR_URL, QbrRuntimeMissingError, QbrSignInError, pomerium_token


def authenticated_client(token: str, **kwargs) -> httpx.AsyncClient:
    # Both mechanisms are route-scoped. Never follow redirects with credentials.
    return httpx.AsyncClient(headers={"X-Pomerium-Authorization": token},
                             cookies={"_pomerium": token}, follow_redirects=False,
                             timeout=httpx.Timeout(30, read=300), **kwargs)


async def discover_tools(upstream: ClientSession) -> list:
    tools = []
    cursor = None
    seen = set()
    while True:
        page = await upstream.list_tools(cursor=cursor)
        tools.extend(page.tools)
        cursor = page.nextCursor
        if not cursor:
            break
        if cursor in seen or len(seen) >= 20:
            raise RuntimeError("QBR returned an invalid tool catalogue cursor")
        seen.add(cursor)
    return tools


async def make_proxy(upstream: ClientSession) -> Server:
    tools = await discover_tools(upstream)
    app = Server("QBR Express for Renewal Preparation")

    @app.list_tools()
    async def list_tools():
        return tools

    @app.call_tool()
    async def call_tool(name, arguments):
        # Preserve structured output and error flags; never replay generation calls.
        return await upstream.call_tool(name, arguments, read_timeout_seconds=timedelta(seconds=300))

    return app


@asynccontextmanager
async def upstream_session():
    token = await asyncio.to_thread(pomerium_token)
    async with authenticated_client(token) as client:
        async with streamable_http_client(QBR_URL + "/mcp", http_client=client) as (read, write, _):
            async with ClientSession(read, write) as upstream:
                await upstream.initialize()
                yield upstream


def connection_failure(error: BaseException) -> dict:
    """Classify failures without returning exception text, headers or credentials."""
    pending = [error]
    failures = []
    while pending:
        current = pending.pop()
        nested = getattr(current, "exceptions", None)
        if nested:
            pending.extend(nested)
        else:
            failures.append(current)
    statuses = [item.response.status_code for item in failures if isinstance(item, httpx.HTTPStatusError)]
    result = {"connected": False, "status": "connection_failed", "message": "QBR Express MCP could not connect. Check the service connection and reconnect the plugin."}
    if 401 in statuses or 403 in statuses:
        status = 401 if 401 in statuses else 403
        result.update(status="authentication_rejected" if status == 401 else "access_denied", http_status=status,
                      message=f"QBR Express MCP returned HTTP {status}. Complete company sign-in and verify QBR access. If rejection persists, contact the QBR service owner.")
    elif any(isinstance(item, QbrRuntimeMissingError) for item in failures):
        result.update(status="runtime_missing", message="The QBR sign-in component is missing. Rerun the one-command installer.")
    elif any(isinstance(item, QbrSignInError) for item in failures):
        result.update(status="sign_in_required", message="Complete company sign-in in your browser, then check the QBR MCP connection again.")
    elif any(isinstance(item, (TimeoutError, httpx.TimeoutException)) for item in failures):
        result.update(status="connection_timeout", message="The QBR MCP connection check timed out. Complete any pending sign-in and check again.")
    elif statuses:
        result.update(status="service_error", http_status=statuses[0])
    return result


async def check_connection() -> dict:
    async def inspect():
        async with upstream_session() as upstream:
            tools = await discover_tools(upstream)
            required = {"get_qbr_capabilities", "search_qbr_accounts", "start_qbr_deck", "get_qbr_generation_status", "download_qbr_artifact"}
            missing = sorted(required - {tool.name for tool in tools})
            if missing:
                return {"connected": False, "status": "generation_tools_missing", "missing_tools": missing,
                        "message": "The server responded but its QBR tool catalogue is incomplete. Contact the QBR service owner. No report was generated."}
            return {"connected": True, "status": "ready", "tool_count": len(tools),
                    "message": "QBR Express MCP connected and its generation tools are available. If they are absent from this task, reconnect the plugin and open a new task. No report was generated."}
    try:
        return await asyncio.wait_for(inspect(), timeout=105)
    except Exception as error:
        result = connection_failure(error)
        result["message"] += " This check did not generate a report."
        return result


async def serve(check_only: bool = False) -> None:
    if check_only:
        result = await check_connection()
        print(result["message"])
        if not result["connected"]:
            raise SystemExit(1)
        return
    async with upstream_session() as upstream:
        proxy = await make_proxy(upstream)
        async with stdio_server() as (stdin, stdout):
            await proxy.run(stdin, stdout, proxy.create_initialization_options())


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Check connection without generating a report")
    args = parser.parse_args()
    logging.basicConfig(level=logging.WARNING)
    try:
        asyncio.run(serve(args.check))
        return 0
    except KeyboardInterrupt:
        return 130
    except Exception as error:
        # CLI output and transport exceptions may contain authentication details.
        print(connection_failure(error)["message"], file=sys.stderr)
        print("If a report was already started, keep its job ID and do not start a replacement.", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
