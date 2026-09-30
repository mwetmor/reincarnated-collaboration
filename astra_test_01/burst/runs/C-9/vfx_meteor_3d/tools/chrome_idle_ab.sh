#!/bin/bash
# C-9 lane B v2: the PAGE in Chrome at phone size, without and with ?meteor=b, the Meteor never cast in the
# standing and walking phases -- barrow_full's own web_painted_test.js (its fps by phase), twice each, A B A B.
HERE=$(cd "$(dirname "$0")" && pwd); ROOT=$(cd "$HERE/.." && pwd)
T=$HOME/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/barrow_full/tools
L=$HOME/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-7/conductor_scripts/heavy_lock.py
export PLAYWRIGHT_CORE=/Users/admin/.npm/_npx/705bc6b22212b352/node_modules/playwright-core
node "$T/web_br_server.js" "$ROOT/web/serve" 8811 > "$ROOT/work/logs/serve_page.log" 2>&1 &
SRV=$!
sleep 1
# THE SERVER MUST BE THIS ONE (the first run found the port taken and measured another session's page)
grep -q '^listening 8811' "$ROOT/work/logs/serve_page.log" || { echo 'HALT: port 8811 is not ours'; exit 7; }
for i in 1 2; do
  for V in a b; do
    Q="?touch=1&fps=1&c=sorceress"; [ $V = b ] && Q="$Q&meteor=b"
    python3 "$L" C-9 -- python3 "$HERE/tmo.py" 420 -- node "$T/web_painted_test.js" "http://127.0.0.1:8811/playtest/barrow-painted/$Q" "$ROOT/work/v2/chrome_idle_${V}_$i" 40 > "$ROOT/work/v2/chrome_idle_${V}_$i.log" 2>&1
    python3 -c "
import json,statistics as st
r=json.load(open('$ROOT/work/v2/chrome_idle_${V}_$i/report.json'))
print('$V $i', {k:(round(st.mean(v),1),len(v)) for k,v in r['fps_by_phase'].items()}, 'built_ms', r['in_page_ms_from_navigation'].get('barrow_built'), 'errors', len(r['errors']))"
  done
done
kill $SRV
