#!/usr/bin/env bash
# Wrapper for install.py (needs python3). See install.py --help.
#   bash install.sh <repo> --mode greenfield
#   bash install.sh <repo> --mode brownfield --docs-dir docs/z21   then   bash install.sh <repo> --apply-map --docs-dir docs/z21
set -euo pipefail
exec python3 "$(cd "$(dirname "$0")" && pwd)/install.py" "$@"
