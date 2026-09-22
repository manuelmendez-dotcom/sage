#!/usr/bin/env bash
# Installs only QBR & Renewal Brief; existing SAGE remains independently installed.
set -euo pipefail
export PATH="/opt/homebrew/bin:/usr/local/bin:$HOME/.npm-global/bin:$HOME/bin:$PATH"
qbr_setup_guide='https://docs.google.com/document/d/1cdcSGinExD8K5Ydu7RCLnkU28ZQoXVxf_BvEgrlSlmo/edit'
qbr_data_root="${QBR_RENEWAL_DATA_HOME:-$HOME/.local/share/qbr-renewal}"

if [[ "$(uname -s)" != Darwin ]]; then
  echo 'This installer supports macOS. See the plugin README for requirements.' >&2
  exit 1
fi
qbr_codex="$(command -v codex || true)"
if [[ -z "$qbr_codex" && -x /Applications/Codex.app/Contents/Resources/codex ]]; then
  qbr_codex=/Applications/Codex.app/Contents/Resources/codex
fi
if [[ -z "$qbr_codex" ]] || ! "$qbr_codex" plugin add --help >/dev/null 2>&1; then
  echo 'Install or update Codex with plugin CLI support, then rerun this command.' >&2
  exit 1
fi

# The company bridge is distributed through authenticated Drive, not this repo.
# Accept an existing installation, or copy the verified Apple Silicon download
# into a user-owned directory without sudo or changes to other MCP connections.
if ! command -v pom-mcp-bridge >/dev/null 2>&1 && [[ ! -x "$qbr_data_root/bin/pom-mcp-bridge" ]]; then
  qbr_download="$HOME/Downloads/pom-mcp-bridge"
  qbr_expected_sha='b212cb0bfc04fd8518b3b25b8ba28f95dedb044a77042e74dcf6aeaa0d2e2cb5'
  if [[ "$(uname -m)" == arm64 && -f "$qbr_download" ]] &&
     [[ "$(shasum -a 256 "$qbr_download" | awk '{print $1}')" == "$qbr_expected_sha" ]]; then
    mkdir -p "$qbr_data_root/bin"
    cp "$qbr_download" "$qbr_data_root/bin/pom-mcp-bridge"
    chmod 755 "$qbr_data_root/bin/pom-mcp-bridge"
  else
    echo 'One-time prerequisite: download/install the company QBR bridge, then rerun.' >&2
    echo "Setup guide: $qbr_setup_guide" >&2
    echo 'Apple Silicon: the original pom-mcp-bridge download may stay in Downloads; this installer can copy it.' >&2
    echo 'Intel: obtain a compatible bridge from the QBR owner and install it first.' >&2
    exit 1
  fi
fi

qbr_python=''
for qbr_candidate in python3.13 python3.12 python3.11 python3.10 python3; do
  if command -v "$qbr_candidate" >/dev/null 2>&1 &&
     "$qbr_candidate" -c 'import sys; raise SystemExit(sys.version_info < (3, 10))' 2>/dev/null; then
    qbr_python="$(command -v "$qbr_candidate")"
    break
  fi
done
if [[ -z "$qbr_python" ]]; then
  if command -v brew >/dev/null 2>&1; then
    echo 'Installing Python for local report delivery…'
    brew install python@3.12
    qbr_python="$(brew --prefix python@3.12)/bin/python3.12"
  else
    echo 'Python 3.10+ is required. Install Python or Homebrew, then rerun.' >&2
    exit 1
  fi
fi
if ! command -v pomerium-cli >/dev/null 2>&1; then
  if command -v brew >/dev/null 2>&1; then
    echo 'Installing Pomerium CLI for your own QBR sign-in…'
    brew install pomerium/tap/pomerium-cli
  else
    echo 'Install Pomerium CLI (brew install pomerium/tap/pomerium-cli), then rerun.' >&2
    exit 1
  fi
fi

qbr_temp="$(mktemp -d "${TMPDIR:-/tmp}/qbr-renewal.XXXXXX")"
trap 'rm -rf "$qbr_temp"' EXIT
echo 'Downloading QBR & Renewal Brief…'
git clone --quiet --depth 1 https://github.com/manuelmendez-dotcom/sage.git "$qbr_temp/sage"
"$qbr_python" "$qbr_temp/sage/plugins/qbr-renewal/scripts/install.py" --codex "$qbr_codex"
