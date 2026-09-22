#!/usr/bin/env bash
# Shared paths are outside the versioned plugin cache, so upgrades stay portable.
qbr_data_root="${QBR_RENEWAL_DATA_HOME:-$HOME/.local/share/qbr-renewal}"
export PATH="$qbr_data_root/bin:/opt/homebrew/bin:/usr/local/bin:$PATH"
