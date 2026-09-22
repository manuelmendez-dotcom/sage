#!/usr/bin/env bash
set -euo pipefail
qbr_script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
source "$qbr_script_dir/common.sh"
if ! command -v pom-mcp-bridge >/dev/null 2>&1; then
  echo 'QBR bridge missing. Run the QBR & Renewal Brief installer; see the plugin README.' >&2
  exit 1
fi
exec pom-mcp-bridge https://qbr-express.internal.zenai-apps.com
