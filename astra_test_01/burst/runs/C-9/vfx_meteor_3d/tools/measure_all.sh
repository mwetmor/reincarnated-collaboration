#!/bin/bash
# C-9 lane B, v2 (the integration build): every desktop measurement, in order, each behind the heavy lock.
#   1. IDLE A/B -- the PAGE scene (barrow_painted.tscn, her), the Meteor never cast: without ?meteor=b (the
#      page as at HEAD: its shaders byte-identical) against with it, barrow_full's own --frame-cost instrument
#      (she walks a loop, vsync off, 600 frames), alternated A B A B A B, Forward+ then Compatibility (--as-web)
#   2. THE CAST BUDGET as a DELTA (the harness): cold caches, 1 cold cast + 19 on / 20 off interleaved
#   3. THE FILMS: play speed and quarter speed
set -o pipefail
HERE=$(cd "$(dirname "$0")" && pwd); ROOT=$HERE/..; G=/Applications/Godot.app/Contents/MacOS/Godot
L=$HOME/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-7/conductor_scripts/heavy_lock.py
W=$ROOT/work/v2; mkdir -p "$W"
FREE=$(df -g /System/Volumes/Data | awk 'NR==2{print $4}'); [ "$FREE" -ge 20 ] || { echo "HALT disk"; exit 9; }
run() { python3 "$L" C-9 -- python3 "$HERE/tmo.py" "$1" -- "${@:2}"; }
for R in fplus compat; do
  EXTRA=(); WEB=()
  [ $R = compat ] && EXTRA=(--rendering-method gl_compatibility --rendering-driver opengl3_angle) && WEB=(--as-web)
  for i in 1 2 3; do
    for V in a b; do
      MB=(); [ $V = b ] && MB=(--meteor b)
      run 240 $G --path "$ROOT/godot" "${EXTRA[@]}" --resolution 1920x1080 res://scenes/barrow_painted.tscn -- "${WEB[@]}" --c sorceress "${MB[@]}" --frame-cost > "$W/idle_${R}_${V}_$i.log" 2>&1
      echo "idle $R $V $i: $(grep -a -o 'frame_cost ms_per_frame=[0-9.]*' "$W/idle_${R}_${V}_$i.log") $(grep -a -c 'armed' "$W/idle_${R}_${V}_$i.log")"
    done
  done
done
mkdir -p "$W/probe_fplus" "$W/probe_compat"
run 240 $G --path "$ROOT/godot" --resolution 1920x1080 -- --meteor b --meteor-lightprobe --out "$W/probe_fplus" > "$W/probe_fplus.log" 2>&1
run 240 $G --path "$ROOT/godot" --rendering-method gl_compatibility --rendering-driver opengl3_angle --resolution 1920x1080 -- --as-web --meteor b --meteor-lightprobe --out "$W/probe_compat" > "$W/probe_compat.log" 2>&1
python3 "$HERE/lightprobe.py" "$W/probe_fplus" "$W/probe_compat" "$ROOT/artifacts/v2/web_fire_light_match.json" | tail -22
UD="$HOME/Library/Application Support/Godot/app_userdata/C-9 Meteor lane B (3D first)"
[ -d "$UD" ] && mv "$UD" "$UD.cache-v2-$(date +%H%M%S)"
run 700 $G --path "$ROOT/godot" --resolution 1920x1080 -- --meteor b --meteor-perf --out "$W/perf_fplus_1080_cold.json" > "$W/perf_fplus.log" 2>&1
echo "perf: $(ls -la $W/perf_fplus_1080_cold.json 2>&1)"
bash "$HERE/film.sh" "$ROOT/artifacts/v2" "/private/tmp/claude-501/-Users-admin-Games-reincarnated-collaboration/7b4d3123-ce50-4e1f-af04-9f5d427f755a/scratchpad/film2"
echo "== measure_all done"
