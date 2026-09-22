"""Exercise the MCP command and cwd as actually resolved by Codex."""
import asyncio
import json
import os
from pathlib import Path
import shlex
import shutil
import subprocess
import sys
import tempfile
import unittest

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


@unittest.skipUnless(shutil.which("codex"), "Codex CLI is required for the packaging integration check")
class InstalledPackageTests(unittest.TestCase):
    def test_codex_resolved_delivery_connects(self):
        repo = Path(__file__).resolve().parents[3]
        with tempfile.TemporaryDirectory(prefix="qbr-package-") as temporary:
            folder = Path(temporary)
            profile = folder / "profile"
            profile.mkdir()
            runtime = folder / "runtime"
            python = runtime / "runtime-v1/bin/python"
            python.parent.mkdir(parents=True)
            # Reuse test dependencies without downloading a second environment.
            python.write_text("#!/bin/sh\nexec " + shlex.quote(sys.executable) + ' "$@"\n')
            python.chmod(0o755)
            env = dict(os.environ, CODEX_HOME=str(profile), QBR_RENEWAL_DATA_HOME=str(runtime))

            def run(*args):
                completed = subprocess.run(args, env=env, capture_output=True, text=True, check=True)
                return json.loads(completed.stdout)

            run("codex", "plugin", "marketplace", "add", str(repo), "--json")
            installed = run("codex", "plugin", "add", "qbr-renewal@zendesk-scaled-cs", "--json")
            inventory = run("codex", "mcp", "list", "--json")
            delivery = next(item for item in inventory if item["name"] == "qbr-renewal-delivery")
            transport = delivery["transport"]
            self.assertEqual(Path(installed["installedPath"]).resolve(), Path(transport["cwd"]).resolve())

            async def connect():
                params = StdioServerParameters(command=transport["command"], args=transport["args"], cwd=transport["cwd"], env=env)
                async with stdio_client(params) as (read, write):
                    async with ClientSession(read, write) as session:
                        await session.initialize()
                        tools = await session.list_tools()
                        self.assertEqual({"check_qbr_connection", "save_qbr_artifact"}, {tool.name for tool in tools.tools})
                        result = await session.call_tool("save_qbr_artifact", {"job_id": "invalid"})
                        self.assertTrue(result.isError)

            asyncio.run(asyncio.wait_for(connect(), timeout=15))


if __name__ == "__main__":
    unittest.main()
