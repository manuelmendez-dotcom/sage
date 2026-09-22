"""Install the browser workflow and migrate legacy QBR components through Codex."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


@unittest.skipUnless(shutil.which("codex"), "Codex CLI is required for the integration check")
class InstalledPackageTests(unittest.TestCase):
    def test_install_and_upgrade_retire_only_legacy_qbr_components(self):
        repo = Path(__file__).resolve().parents[3]
        with tempfile.TemporaryDirectory(prefix="qbr-browser-package-") as temporary:
            folder = Path(temporary)
            profile = folder / "profile"
            profile.mkdir()
            data = folder / "data"
            env = dict(os.environ, CODEX_HOME=str(profile), QBR_RENEWAL_DATA_HOME=str(data))

            def run(*args):
                completed = subprocess.run(args, env=env, capture_output=True, text=True, check=True)
                return json.loads(completed.stdout)

            legacy = folder / "legacy"
            plugin = legacy / "plugins/qbr-local-delivery"
            (plugin / ".codex-plugin").mkdir(parents=True)
            (plugin / ".codex-plugin/plugin.json").write_text(json.dumps({"name": "qbr-local-delivery", "version": "0.1.0"}))
            (legacy / ".agents/plugins").mkdir(parents=True)
            (legacy / ".agents/plugins/marketplace.json").write_text(json.dumps({
                "name": "qbr-express-local-delivery", "plugins": [{
                    "name": "qbr-local-delivery", "source": {"source": "local", "path": "./plugins/qbr-local-delivery"},
                    "policy": {"installation": "AVAILABLE", "authentication": "ON_USE"}, "category": "Productivity"
                }]}))
            run("codex", "plugin", "marketplace", "add", str(legacy), "--json")
            run("codex", "plugin", "add", "qbr-local-delivery@qbr-express-local-delivery", "--json")
            subprocess.run(["codex", "mcp", "add", "qbr-express", "--", "/usr/local/bin/pom-mcp-bridge", "https://qbr-express.internal.zenai-apps.com"], env=env, capture_output=True, check=True)
            subprocess.run(["codex", "mcp", "add", "unrelated", "--", "/usr/bin/true"], env=env, capture_output=True, check=True)
            run("codex", "plugin", "marketplace", "add", str(repo), "--json")
            sage = run("codex", "plugin", "add", "sage-zendesk-qa@zendesk-scaled-cs", "--json")
            sage_root = Path(sage["installedPath"])

            def sage_hashes():
                return {str(p.relative_to(sage_root)): hashlib.sha256(p.read_bytes()).hexdigest() for p in sage_root.rglob("*") if p.is_file()}

            original_sage = sage_hashes()
            runtime = data / "runtime-v1"
            runtime.mkdir(parents=True)
            (runtime / "qbr-requirements.txt").write_text("obsolete fixture")
            (data / "bin").mkdir()
            for name in ("pomerium-cli", "pomerium-v0.33.1.verified", "pom-mcp-bridge"):
                (data / "bin" / name).write_text("obsolete fixture")
            (data / "bin/keep-helper").write_text("preserve")

            command = [sys.executable, str(repo / "plugins/qbr-renewal/scripts/install.py"), "--source", str(repo)]
            for _ in range(2):
                subprocess.run(command, env=env, capture_output=True, text=True, check=True)

            installed = run("codex", "plugin", "list", "--json")["installed"]
            qbr = [item for item in installed if item["name"].startswith("qbr-")]
            self.assertEqual(["qbr-renewal"], [item["name"] for item in qbr])
            self.assertTrue(qbr[0]["enabled"])
            self.assertEqual(original_sage, sage_hashes())
            self.assertFalse(runtime.exists())
            self.assertEqual(["keep-helper"], [p.name for p in (data / "bin").iterdir()])
            servers = run("codex", "mcp", "list", "--json")
            names = {server["name"] for server in servers}
            self.assertFalse(any(name.startswith("qbr-") for name in names))
            self.assertTrue({"google-drive", "z2-help-center", "unrelated"}.issubset(names))
            markets = run("codex", "plugin", "marketplace", "list", "--json")["marketplaces"]
            self.assertNotIn("qbr-express-local-delivery", [item["name"] for item in markets])


if __name__ == "__main__":
    unittest.main()
