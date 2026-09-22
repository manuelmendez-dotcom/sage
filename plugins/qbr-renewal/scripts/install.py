#!/usr/bin/env python3
"""Install one browser-based QBR plugin and retire its obsolete QBR connections."""
from __future__ import annotations

import argparse
import fcntl
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

REPOSITORY = "https://github.com/manuelmendez-dotcom/sage.git"
MARKETPLACE = "zendesk-scaled-cs"
PLUGIN = "qbr-renewal"
LEGACY_PLUGIN = "qbr-local-delivery@qbr-express-local-delivery"
LEGACY_MARKETPLACE = "qbr-express-local-delivery"
QBR_URL = "https://qbr-express.internal.zenai-apps.com"


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


def sync_snapshot(snapshot: Path, destination: Path) -> Path:
    """Replace only this installer's own marketplace snapshot, with rollback."""
    destination.parent.mkdir(parents=True, exist_ok=True)
    with (destination.parent / "marketplace.lock").open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        staging = destination.with_name(destination.name + ".incoming")
        backup = destination.with_name(destination.name + ".previous")
        if backup.exists() and not destination.exists():
            backup.rename(destination)
        if staging.exists():
            shutil.rmtree(staging)
        shutil.copytree(snapshot, staging, ignore=shutil.ignore_patterns(".git", "__pycache__", ".venv"))
        if not (staging / ".agents/plugins/marketplace.json").is_file():
            raise RuntimeError("The downloaded package has no marketplace catalogue")
        if backup.exists():
            shutil.rmtree(backup)
        if destination.exists():
            destination.rename(backup)
        try:
            staging.rename(destination)
        except OSError:
            if backup.exists():
                backup.rename(destination)
            raise
        if backup.exists():
            shutil.rmtree(backup)
    return destination


def prepare_marketplace(codex: str, source: str = REPOSITORY, snapshot: Path | None = None, data_root: Path | None = None) -> Path:
    listing = json.loads(run(codex, "plugin", "marketplace", "list", "--json"))
    existing = next((item for item in listing["marketplaces"] if item["name"] == MARKETPLACE), None)
    managed = data_root / "marketplace" if data_root is not None else None
    if existing is None:
        if snapshot is not None and managed is not None:
            source = str(sync_snapshot(snapshot, managed))
        result = json.loads(run(codex, "plugin", "marketplace", "add", source, "--json"))
        return Path(result["installedRoot"])

    root = Path(existing["root"])
    if snapshot is not None and managed is not None and root.resolve() == managed.resolve():
        return sync_snapshot(snapshot, managed)
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


def retire_legacy_qbr(codex: str, data_root: Path) -> None:
    """Remove only the known QBR components replaced by this plugin."""
    installed = json.loads(run(codex, "plugin", "list", "--json"))["installed"]
    if any(item["pluginId"] == LEGACY_PLUGIN for item in installed):
        run(codex, "plugin", "remove", LEGACY_PLUGIN, "--json")
        print("Removed the separate QBR Local Delivery plugin.")
    remaining = [item for item in installed if item["pluginId"] != LEGACY_PLUGIN]
    markets = json.loads(run(codex, "plugin", "marketplace", "list", "--json"))["marketplaces"]
    if (any(item["name"] == LEGACY_MARKETPLACE for item in markets)
            and not any(item.get("marketplaceName") == LEGACY_MARKETPLACE for item in remaining)):
        run(codex, "plugin", "marketplace", "remove", LEGACY_MARKETPLACE, "--json")

    for server in json.loads(run(codex, "mcp", "list", "--json")):
        if server["name"] not in {"qbr-express", "qbr_express"}:
            continue
        transport = server["transport"]
        destinations = [transport.get("url", ""), *transport.get("args", [])]
        if any(value.rstrip("/") in {QBR_URL, QBR_URL + "/mcp"} for value in destinations):
            run(codex, "mcp", "remove", server["name"])
            print("Removed the obsolete standalone QBR MCP connection.")

    # These exact paths belonged to this installer, not shared system tooling.
    runtime = data_root / "runtime-v1"
    if runtime.is_symlink():
        runtime.unlink()
    elif (runtime / "qbr-requirements.txt").is_file():
        shutil.rmtree(runtime)
    private_bin = data_root / "bin"
    if not private_bin.is_symlink():
        for name in ("pomerium-cli", "pomerium-v0.33.1.verified", "pom-mcp-bridge"):
            (private_bin / name).unlink(missing_ok=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--codex", default="codex")
    parser.add_argument("--source", default=REPOSITORY, help="Local marketplace root for development; defaults to the published repository")
    parser.add_argument("--snapshot", type=Path, help="Downloaded repository snapshot for setup without Git")
    args = parser.parse_args()
    if sys.version_info < (3, 10):
        parser.error("Python 3.10+ is required")
    data_root = Path(os.environ.get("QBR_RENEWAL_DATA_HOME", str(Path.home() / ".local/share/qbr-renewal"))).expanduser().resolve()
    try:
        run(args.codex, "plugin", "add", "--help")
        root = prepare_marketplace(args.codex, args.source, args.snapshot, data_root)
        if not (root / "plugins" / PLUGIN / ".codex-plugin/plugin.json").is_file():
            raise RuntimeError("The configured marketplace does not yet contain QBR Conversations.")
        result = json.loads(run(args.codex, "plugin", "add", f"{PLUGIN}@{MARKETPLACE}", "--json"))
        print(f"Installed QBR Conversations {result['version']}.")
        retire_legacy_qbr(args.codex, data_root)
        print("One QBR plugin: fresh website generation, PowerPoint delivery, and a conversation brief when requested.")
        print("SAGE and unrelated connections are preserved. No QBR MCP, bridge or delivery runtime is required.")
        print("Restart Codex and open a new task with browser access. Sign in to the QBR website; Google Drive and Z2 are used only when needed for research or explicitly requested sources.")
        print('Try: Prepare a QBR and one-page renewal brief for [customer], using owned products only.')
        return 0
    except (OSError, RuntimeError, ValueError) as error:
        print(f"Installation could not finish: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
