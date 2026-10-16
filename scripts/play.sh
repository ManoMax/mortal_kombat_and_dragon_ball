#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../engine"
unset GTK_PATH GTK_EXE_PREFIX GTK_IM_MODULE_FILE GIO_MODULE_DIR
export GTK_MODULES=
export LD_LIBRARY_PATH="$PWD/lib:/usr/lib/x86_64-linux-gnu"
if [[ ${1:-} == --menu ]]; then
  shift
  exec ./Ikemen_GO_Linux -windowed "$@"
fi
exec ./Ikemen_GO_Linux -windowed -width 960 -height 720 -p1 goku -p2 vegeta -p1.ai 0 -p2.ai 0 -p1.input 1 -p2.input 2 -s stage0 "$@"
