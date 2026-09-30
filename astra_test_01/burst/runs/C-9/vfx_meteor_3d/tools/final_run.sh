#!/bin/bash
# C-9 lane B v2, the final chain: the cast delta (cold), the films, the page build + fences, the harness web build.
set -o pipefail
HERE=$(cd "$(dirname "$0")" && pwd); ROOT=$HERE/..; G=/Applications/Godot.app/Contents/MacOS/Godot
L=$HOME/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-7/conductor_scripts/heavy_lock.py
W=$ROOT/work/v2; mkdir -p "$W"
FREE=$(df -g /System/Volumes/Data | awk 'NR==2{print $4}'); [ "$FREE" -ge 20 ] || { echo "HALT disk"; exit 9; }
UD="$HOME/Library/Application Support/Godot/app_userdata/C-9 Meteor lane B (3D first)"
[ -d "$UD" ] && mv "$UD" "$UD.cache-v2b-$(date +%H%M%S)"
python3 "$L" C-9 -- python3 "$HERE/tmo.py" 700 -- $G --path "$ROOT/godot" --resolution 1920x1080 -- --meteor b --meteor-perf --out "$W/perf_fplus_1080_cold_c.json" > "$W/perf_fplus_b.log" 2>&1
python3 "$HERE/perf_report.py" "$W/perf_fplus_1080_cold_c.json" "v2 final desktop" | tail -12
bash "$HERE/film.sh" "$ROOT/artifacts/v2" "/private/tmp/claude-501/-Users-admin-Games-reincarnated-collaboration/7b4d3123-ce50-4e1f-af04-9f5d427f755a/scratchpad/film4"
bash "$ROOT/pagecheck/tools/build_web_painted.sh" --no-stage > "$ROOT/work/logs/pagecheck4.log" 2>&1; echo "pagecheck exit $?"
grep -E "ok |FAIL" "$ROOT/work/logs/pagecheck4.log" | grep -c "ok "; grep FAIL "$ROOT/work/logs/pagecheck3.log"
cp -R "$ROOT/web/src/build/web/." "$ROOT/web/page/barrow-painted/"
bash "$HERE/build_web.sh" > "$ROOT/work/logs/build_web6.log" 2>&1; echo "harness build exit $?"; tail -4 "$ROOT/work/logs/build_web5.log"
echo "== final_run done"
