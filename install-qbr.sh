#!/usr/bin/env bash
# One-command macOS setup. All downloaded components stay in the plugin's data directory.
set -euo pipefail
qbr_data_root="${QBR_RENEWAL_DATA_HOME:-$HOME/.local/share/qbr-renewal}"
if [[ "$(uname -s)" != Darwin ]]; then
  echo 'This installer currently supports macOS.' >&2
  exit 1
fi
case "$(uname -m)" in
  arm64)
    qbr_uv_arch=aarch64
    qbr_uv_sha=85f00cbdc6dd3e97eba4c31b4d014375a9fdfe8f570023b84e5102fc3456896b
    qbr_codex_sha=5e5a51470dce2423f9d96bd191d0bbc4cc0e2848a6833df5178eaf47a07a3768
    ;;
  x86_64)
    qbr_uv_arch=x86_64
    qbr_uv_sha=8dcf05a8c809bb3c471d2b614788ba27a6e41298fc8c31ac84b5f4339fd468e5
    qbr_codex_sha=ff22ad0bf28b8568dbfb28ef0ea64451fe5170fa0f9118bf764ca6cb24c27791
    ;;
  *) echo 'Unsupported Mac processor.' >&2; exit 1 ;;
esac

qbr_temp="$(mktemp -d "${TMPDIR:-/tmp}/qbr-renewal.XXXXXX")"
trap 'rm -rf "$qbr_temp"' EXIT
mkdir -p "$qbr_data_root/bin"
export PATH="$qbr_data_root/bin:$PATH"

qbr_fetch_verified() {
  curl --proto '=https' --tlsv1.2 -fsSL --retry 2 "$1" -o "$2"
  if [[ "$(shasum -a 256 "$2" | awk '{print $1}')" != "$3" ]]; then
    echo 'A downloaded component failed its checksum check. Installation stopped.' >&2
    exit 1
  fi
}

echo 'Preparing QBR Conversations…'
if [[ ! -x "$qbr_data_root/bin/uv" ]] || [[ "$("$qbr_data_root/bin/uv" --version 2>/dev/null)" != "uv 0.12.17"* ]]; then
  qbr_fetch_verified "https://github.com/astral-sh/uv/releases/download/0.12.17/uv-$qbr_uv_arch-apple-darwin.tar.gz" "$qbr_temp/uv.tar.gz" "$qbr_uv_sha"
  tar -xzf "$qbr_temp/uv.tar.gz" -C "$qbr_temp" "uv-$qbr_uv_arch-apple-darwin/uv"
  mv "$qbr_temp/uv-$qbr_uv_arch-apple-darwin/uv" "$qbr_data_root/bin/uv"
fi
qbr_codex="${QBR_CODEX_BIN:-$(command -v codex || true)}"
if [[ -z "$qbr_codex" ]] || ! "$qbr_codex" plugin add --help >/dev/null 2>&1; then
  qbr_fetch_verified "https://github.com/openai/codex/releases/download/rust-v0.155.1/codex-$qbr_uv_arch-apple-darwin.tar.gz" "$qbr_temp/codex.tar.gz" "$qbr_codex_sha"
  tar -xzf "$qbr_temp/codex.tar.gz" -C "$qbr_temp" "codex-$qbr_uv_arch-apple-darwin"
  mv "$qbr_temp/codex-$qbr_uv_arch-apple-darwin" "$qbr_data_root/bin/codex"
  qbr_codex="$qbr_data_root/bin/codex"
fi

export UV_PYTHON_INSTALL_DIR="$qbr_data_root/python"
export UV_CACHE_DIR="$qbr_data_root/cache"
"$qbr_data_root/bin/uv" python install 3.12 --no-bin --no-progress
qbr_python="$("$qbr_data_root/bin/uv" python find --managed-python --no-project 3.12)"

# A local archive-backed marketplace avoids a Git/Xcode prerequisite on new Macs.
echo 'Downloading the plugin…'
qbr_source="${QBR_RENEWAL_SOURCE_DIR:-}"
if [[ -z "$qbr_source" ]]; then
  curl --proto '=https' --tlsv1.2 -fsSL --retry 2 https://codeload.github.com/manuelmendez-dotcom/sage/tar.gz/refs/heads/main -o "$qbr_temp/repo.tar.gz"
  mkdir "$qbr_temp/repo"
  tar -xzf "$qbr_temp/repo.tar.gz" --strip-components=1 -C "$qbr_temp/repo"
  qbr_source="$qbr_temp/repo"
fi
"$qbr_python" "$qbr_source/plugins/qbr-renewal/scripts/install.py" --codex "$qbr_codex" --snapshot "$qbr_source"
