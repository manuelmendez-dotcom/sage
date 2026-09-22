"""Bundled stdio connection to QBR Express; no separate pom-mcp-bridge binary."""
from __future__ import annotations

import argparse
import asyncio
from datetime import timedelta
import logging
import sys

import httpx
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client
from mcp.server import Server
from mcp.server.stdio import stdio_server

from qbr_auth import QBR_URL, pomerium_token


def authenticated_client(token: str, **kwargs) -> httpx.AsyncClient:
    # Both mechanisms are route-scoped. Never follow redirects with credentials.
    return httpx.AsyncClient(headers={"X-Pomerium-Authorization": token},
                             cookies={"_pomerium": token}, follow_redirects=False,
                             timeout=httpx.Timeout(30, read=300), **kwargs)


async def make_proxy(upstream: ClientSession) -> Server:
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
    app = Server("QBR Express for Renewal Preparation")

    @app.list_tools()
    async def list_tools():
        return tools

    @app.call_tool()
    async def call_tool(name, arguments):
        # Preserve structured output and error flags; never replay generation calls.
        return await upstream.call_tool(name, arguments, read_timeout_seconds=timedelta(seconds=300))

    return app


async def serve(check_only: bool = False) -> None:
    token = await asyncio.to_thread(pomerium_token)
    async with authenticated_client(token) as client:
        async with streamable_http_client(QBR_URL + "/mcp", http_client=client) as (read, write, _):
            async with ClientSession(read, write) as upstream:
                await upstream.initialize()
                proxy = await make_proxy(upstream)
                if check_only:
                    print("QBR Express connected successfully.")
                    return
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
    except Exception:
        # CLI output and transport exceptions may contain authentication details.
        print("QBR Express could not connect. Complete company sign-in, verify service access, then reconnect. No report was generated.", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
