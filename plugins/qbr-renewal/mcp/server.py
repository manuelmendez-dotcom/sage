"""Save completed QBR Express artifacts locally without overwriting prior reports."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile

import requests
from mcp.server.fastmcp import FastMCP

QBR_URL = "https://qbr-express.internal.zenai-apps.com"
JOB_ID = re.compile(r"^[a-f0-9]{32}$")
CONTENT_RANGE = re.compile(r"^bytes (\d+)-(\d+)/(\d+)$")
RANGE_SIZE = 4 * 1024 * 1024
MAX_SIZE = 2 * 1024 ** 3
mcp = FastMCP("QBR Renewal Local Delivery", instructions="Save a completed QBR job locally; retry delivery with the same job ID, never regenerate it.")


def pomerium_token() -> str:
    executable = shutil.which("pomerium-cli")
    if not executable:
        raise RuntimeError("Pomerium CLI is missing. Run the QBR plugin installer.")
    try:
        result = subprocess.run([executable, "k8s", "exec-credential", QBR_URL],
                                check=True, capture_output=True, text=True, timeout=60)
        token = json.loads(result.stdout)["status"]["token"]
        if not isinstance(token, str) or not token.removeprefix("Pomerium-"):
            raise ValueError("empty credential")
        return token.removeprefix("Pomerium-")
    except (subprocess.SubprocessError, ValueError, KeyError, TypeError):
        raise RuntimeError("QBR sign-in is needed. Sign in to QBR Express and retry the same download.") from None


def safe_filename(filename: str | None) -> str:
    name = (filename or "qbr-artifact.bin").replace("\\", "/").rsplit("/", 1)[-1].strip()
    name = "".join(c for c in name if ord(c) >= 32 and ord(c) != 127)
    if name in ("", ".", ".."):
        return "qbr-artifact.bin"
    if len(name.encode("utf-8")) > 220:
        raise ValueError("Artifact filename is too long")
    return name


def publish_unique(partial: Path, directory: Path, filename: str) -> Path:
    base = Path(filename)
    for index in range(10000):
        target = directory / (filename if index == 0 else f"{base.stem} ({index}){base.suffix}")
        try:
            # Atomic create-if-absent: concurrent downloads cannot overwrite one another.
            os.link(partial, target)
            return target
        except FileExistsError:
            continue
    raise RuntimeError("Could not choose a unique artifact filename")


@mcp.tool()
def save_qbr_artifact(job_id: str, filename: str | None = None, expected_size: int | None = None) -> dict[str, str | int]:
    """Save a ready QBR artifact in ~/Generated QBRs; verify size and return SHA-256."""
    if not JOB_ID.fullmatch(job_id):
        raise ValueError("job_id must be the 32-character QBR Express job ID")
    if expected_size is not None and not 0 < expected_size <= MAX_SIZE:
        raise ValueError("expected_size must be a positive byte count up to 2 GiB")
    name = safe_filename(filename)
    token = pomerium_token()
    directory = Path.home() / "Generated QBRs"
    directory.mkdir(parents=True, exist_ok=True)
    descriptor, temp_name = tempfile.mkstemp(prefix=".qbr-", suffix=".partial", dir=directory)
    partial = Path(temp_name)
    digest = hashlib.sha256()
    total = expected_size
    written = 0
    prefix = b""
    try:
        with os.fdopen(descriptor, "wb") as output:
            while total is None or written < total:
                end = written + RANGE_SIZE - 1
                if total is not None:
                    end = min(end, total - 1)
                with requests.get(f"{QBR_URL}/generate/jobs/{job_id}/download",
                                  cookies={"_pomerium": token},
                                  headers={"Range": f"bytes={written}-{end}", "Accept-Encoding": "identity"},
                                  stream=True, timeout=(15, 180), allow_redirects=False) as response:
                    if response.status_code in (301, 302, 303, 307, 308, 401, 403):
                        raise RuntimeError("QBR sign-in/access is needed; retry the same download after signing in.")
                    response.raise_for_status()
                    if response.status_code != 206:
                        raise RuntimeError("QBR did not honour the artifact byte range")
                    if "text/html" in response.headers.get("Content-Type", "").lower():
                        raise RuntimeError("QBR returned an authentication page, not an artifact")
                    match = CONTENT_RANGE.fullmatch(response.headers.get("Content-Range", "").strip())
                    if not match:
                        raise RuntimeError("QBR returned an invalid artifact byte range")
                    start, stop, reported_total = map(int, match.groups())
                    if total is None:
                        total = reported_total
                    if not 0 < total <= MAX_SIZE or reported_total != total or start != written or not start <= stop <= min(end, total - 1):
                        raise RuntimeError("QBR returned an inconsistent artifact size/range")
                    range_written = 0
                    for chunk in response.iter_content(chunk_size=1024 * 1024):
                        if not chunk:
                            continue
                        range_written += len(chunk)
                        if range_written > stop - start + 1:
                            raise RuntimeError("QBR returned too many artifact bytes")
                        if len(prefix) < 8:
                            prefix = (prefix + chunk)[:8]
                        output.write(chunk)
                        digest.update(chunk)
                    if range_written != stop - start + 1:
                        raise RuntimeError("QBR returned an incomplete artifact byte range")
                    written += range_written
            if not prefix.startswith((b"PK\x03\x04", b"%PDF-")):
                raise RuntimeError("Downloaded content is not a supported PPTX/ZIP/PDF artifact")
        if written != total:
            raise RuntimeError("Artifact byte count did not match")
        target = publish_unique(partial, directory, name)
        return {"path": str(target), "filename": target.name, "size": written, "sha256": digest.hexdigest()}
    finally:
        partial.unlink(missing_ok=True)


if __name__ == "__main__":
    mcp.run(transport="stdio")
