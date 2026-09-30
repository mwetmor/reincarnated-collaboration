#!/bin/bash
# C-9 lane B v2 on the FIRE BALL base (barrow_full 339be5e3b): parse checks, the Fire Ball's own budget run with
# the Meteor attached, the two-pack page fences.
HERE=$(cd "$(dirname "$0")" && pwd); ROOT=$(cd "$HERE/.." && pwd); G=/Applications/Godot.app/Contents/MacOS/Godot
L=$HOME/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-7/conductor_scripts/heavy_lock.py
W=$ROOT/work/v2fb; mkdir -p "$W"
FREE=$(df -g /System/Volumes/Data | awk 'NR==2{print $4}'); [ "$FREE" -ge 20 ] || { echo "HALT disk"; exit 9; }
run() { python3 "$L" C-9 -- python3 "$HERE/tmo.py" "$1" -- "${@:2}"; }
run 900 $G --headless --path "$ROOT/godot" --import > "$W/import.log" 2>&1
run 240 $G --path "$ROOT/godot" --resolution 1280x720 --quit-after 400 res://scenes/barrow_painted.tscn -- --c sorceress --meteor b > "$W/parse_fplus.log" 2>&1
run 240 $G --path "$ROOT/godot" --rendering-method gl_compatibility --rendering-driver opengl3_angle --resolution 1280x720 --quit-after 400 res://scenes/barrow_painted.tscn -- --as-web --c sorceress --meteor b > "$W/parse_compat.log" 2>&1
grep -h -E "SCRIPT ERROR|SHADER ERROR|Parse Error|meteor_b\] armed|barrow_painted\] who" "$W/parse_fplus.log" "$W/parse_compat.log" | cut -c1-300
for V in on off; do
  run 900 $G --path "$ROOT/godot" --resolution 1920x1080 res://scenes/barrow_painted.tscn -- --c sorceress --meteor b --perf $([ $V = on ] && echo fb || echo fbc) > "$W/perf_fb_$V.log" 2>&1
  echo "fire ball budget ($V) with the Meteor attached:"; grep -a -E "perf_fb|fire_ball|SCRIPT ERROR" "$W/perf_fb_$V.log" | tail -4 | cut -c1-400
done
bash "$ROOT/pagecheck/tools/build_web_painted.sh" --no-stage > "$ROOT/work/logs/pagecheck_fb.log" 2>&1; echo "pagecheck exit $?"
grep -E "ok |FAIL|launch" "$ROOT/work/logs/pagecheck_fb.log" | cut -c1-230
echo "== done"
