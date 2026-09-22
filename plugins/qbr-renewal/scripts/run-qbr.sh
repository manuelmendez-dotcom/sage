#!/usr/bin/env bash
set -euo pipefail
qbr_script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
source "$qbr_script_dir/common.sh"
qbr_python="$qbr_data_root/runtime-v1/bin/python"
if [[ ! -x "$qbr_python" ]]; then
  echo 'QBR runtime missing. Rerun the one-command installer.' >&2
  exit 1
fi
exec "$qbr_python" "$qbr_script_dir/../mcp/qbr_proxy.py" "$@"
