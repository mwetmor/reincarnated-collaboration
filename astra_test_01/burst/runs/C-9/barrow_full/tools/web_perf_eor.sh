#!/bin/bash
# C-9 (conductor, deploy of 2026-10-03): the dark knight's Eye of Reckoning budget ON THE PAGE -- ?c=warlord&perf=eor
# (perf_fireball.gd: 20 alternating channels, effect on/off, the default kc2 node-pool effect), Chrome at phone size over
# the local brotli server, heavy lock. INFORMATION for the deploy; FAILS only if any frame exceeds 33 ms.
#   tools/web_perf_eor.sh [outdir]
set -uo pipefail
HERE=$(cd "$(dirname "$0")" && pwd); O=${1:-$HERE/../take/build/eor_perf}; mkdir -p "$O"
PW=${PLAYWRIGHT_CORE:-$HOME/Games/reincarnated-collaboration/agentic_orchestration/galadriel/pipeline/node_modules/playwright-core}
if [ -z "${C9_LOCKED:-}" ]; then exec env C9_LOCKED=1 python3 "$HOME/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-7/conductor_scripts/heavy_lock.py" C-9 -- bash "$0" "$@"; fi
node "$HERE/web_br_server.js" "$HOME/Games/reincarnated-loadout/public" 8796 > "$O/server.log" 2>&1 & SP=$!; sleep 1
PLAYWRIGHT_CORE=$PW node "$HERE/web_perf_fb.js" 'http://localhost:8796/playtest/barrow-painted/play.html?c=warlord&perf=eor' "$O" warlord_eor; kill $SP
python3 - "$O/warlord_eor_perf.json" <<'PY'
import json, sys
d = json.load(open(sys.argv[1])); p = d["perf"]
on, off = p["warm_on"], p["warm_off_control"]
worst = max(on["max_ms"], off["max_ms"], p["cold_first_cast"]["max_ms"])
print("eor perf: +%.3f ms/frame (on %.3f vs off %.3f), draws +%d, worst on %.1f / off %.1f ms, over 33 ms: %d / %d, errors %d"
      % (p["delta_mean_ms"], on["mean_ms"], off["mean_ms"], p["delta_dc_peak"], on["max_ms"], off["max_ms"], on["over_33ms"], off["over_33ms"], len(d["errors"])))
sys.exit(1 if (on["over_33ms"] or p["cold_first_cast"]["over_33ms"] or d["errors"]) else 0)
PY
