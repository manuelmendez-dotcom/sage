#!/usr/bin/env python3
"""Install the runtime and plugin through Codex's supported marketplace commands."""
from __future__ import annotations

import argparse
import fcntl
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import venv

REPOSITORY = "https://github.com/manuelmendez-dotcom/sage.git"
MARKETPLACE = "zendesk-scaled-cs"
PLUGIN = "qbr-renewal"
PLUGIN_ROOT = Path(__file__).resolve().parents[1]


def run(*args: str) -> str:
    result = subprocess.run(args, text=True, capture_output=True)
    if result.returncode:
        # Commands never contain auth tokens; avoid printing environment/config.
        raise RuntimeError(result.stderr.strip() or f"{args[0]} failed ({result.returncode})")
    return result.stdout


def canonical_repo(value: str) -> str:
    value = value.rstrip("/").removesuffix(".git")
    if value.startswith("git@github.com:"):
        return "https://github.com/" + value.split(":", 1)[1]
    if value == "manuelmendez-dotcom/sage":
        return "https://github.com/" + value
    return value


def prepare_marketplace(codex: str, source: str = REPOSITORY) -> Path:
    listing = json.loads(run(codex, "plugin", "marketplace", "list", "--json"))
    existing = next((item for item in listing["marketplaces"] if item["name"] == MARKETPLACE), None)
    if existing is None:
        result = json.loads(run(codex, "plugin", "marketplace", "add", source, "--json"))
        return Path(result["installedRoot"])

    root = Path(existing["root"])
    configured = existing.get("marketplaceSource", {})
    if configured.get("sourceType") == "git":
        if canonical_repo(configured.get("source", "")) != canonical_repo(REPOSITORY):
            raise RuntimeError(f"{MARKETPLACE} uses a different repository; its configuration was preserved.")
        run(codex, "plugin", "marketplace", "upgrade", MARKETPLACE)
        return root

    # Respect an existing local SAGE checkout and its marketplace registration.
    # Development installs can pass that same root directly without a remote fetch.
    if source != REPOSITORY and Path(source).resolve() == root.resolve():
        return root
    if not (root / ".git").exists():
        raise RuntimeError(f"Your local marketplace at {root} needs updating from {REPOSITORY}; it was preserved.")
    origin = run("git", "-C", str(root), "remote", "get-url", "origin").strip()
    if canonical_repo(origin) != canonical_repo(REPOSITORY):
        raise RuntimeError(f"The existing marketplace at {root} has a different origin; it was preserved.")
    if run("git", "-C", str(root), "status", "--porcelain").strip():
        raise RuntimeError(f"Your SAGE checkout at {root} has local changes. Save them, then rerun; nothing was overwritten.")
    if run("git", "-C", str(root), "branch", "--show-current").strip() != "main":
        raise RuntimeError(f"Your SAGE checkout at {root} is not on main. Update it separately, then rerun.")
    run("git", "-C", str(root), "fetch", "origin", "main")
    run("git", "-C", str(root), "merge", "--ff-only", "origin/main")
    return root


def install_runtime(data_root: Path) -> Path:
    data_root.mkdir(parents=True, exist_ok=True)
    with (data_root / "install.lock").open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        runtime = data_root / "runtime-v1"
        python = runtime / "bin" / "python"
        if not python.exists():
            venv.EnvBuilder(with_pip=True).create(runtime)
        requirements = PLUGIN_ROOT / "requirements.txt"
        marker = runtime / "qbr-requirements.txt"
        if not marker.exists() or marker.read_bytes() != requirements.read_bytes():
            print("Installing local delivery dependencies…", flush=True)
            run(str(python), "-m", "pip", "install", "--disable-pip-version-check", "--quiet", "-r", str(requirements))
            run(str(python), "-c", "import mcp, requests")
            marker.write_bytes(requirements.read_bytes())
        else:
            run(str(python), "-c", "import mcp, requests")
    return python


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--codex", default="codex")
    parser.add_argument("--source", default=REPOSITORY, help="Local marketplace root for development; defaults to the published repository")
    args = parser.parse_args()
    if sys.version_info < (3, 10):
        parser.error("Python 3.10+ is required")
    data_root = Path(os.environ.get("QBR_RENEWAL_DATA_HOME", str(Path.home() / ".local/share/qbr-renewal"))).expanduser().resolve()
    if not shutil.which("pomerium-cli"):
        parser.error("Install Pomerium CLI first: brew install pomerium/tap/pomerium-cli")
    if not shutil.which("pom-mcp-bridge") and not os.access(data_root / "bin/pom-mcp-bridge", os.X_OK):
        parser.error("Install the company QBR bridge first; see the plugin README")
    try:
        run(args.codex, "plugin", "add", "--help")
        root = prepare_marketplace(args.codex, args.source)
        if not (root / "plugins" / PLUGIN / ".codex-plugin/plugin.json").is_file():
            raise RuntimeError("The configured marketplace does not yet contain QBR & Renewal Brief.")
        install_runtime(data_root)
        result = json.loads(run(args.codex, "plugin", "add", f"{PLUGIN}@{MARKETPLACE}", "--json"))
        print(f"Installed QBR & Renewal Brief {result['version']}.")
        print("SAGE remains independently installed. No existing MCP settings were removed.")
        print("Restart Codex and open a new task. Complete your own QBR, Google Drive and Z2 sign-ins when prompted.")
        print('Try: Prepare a QBR and one-page renewal brief for [customer], using owned products only.')
        return 0
    except (OSError, RuntimeError, ValueError) as error:
        print(f"Installation could not finish: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
