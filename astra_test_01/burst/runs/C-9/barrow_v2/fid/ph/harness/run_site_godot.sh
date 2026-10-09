#!/bin/zsh
# BV2F lane PH, s52 (e) FULL SITE (R-C9-331; scene BV2F_PILOT=site_ph3): P3 sea base-only at the site guide plate, P9 life
# (sway + no-wind RED; sea view with the geometry mask), P9c (floe_view_choose view + the L5 view, rest + RED, 5 pairs).
# Heavy lock per step; 21 GiB gate per step. Views: results/site/p9c_views.json.
set -u
C9=/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9
G=/Applications/Godot.app/Contents/MacOS/Godot
LOCK=/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-7/conductor_scripts/heavy_lock.py
H=$C9/barrow_v2/fid/ph/harness/godot
R=$C9/barrow_v2/fid/ph/renders/${PH_RDIR:-site}
S=res://scenes/bv2f_pilot_painted.tscn
export BV2F_VARIANT=art BV2F_PILOT=site_ph3
gate() { FREE=$(df -g /System/Volumes/Data | awk 'NR==2{print $4}'); if [ "$FREE" -lt 21 ]; then echo "HALT: ${FREE} GiB free < 21"; exit 9; fi; }
run() { local out=$1; shift; mkdir -p $out; gate; (cd $C9/barrow_full/godot && python3 $LOCK C-9 -- $G "$@" > $out/log.txt 2>&1); echo "$out rc=$?"; }
for v in "$@"; do
  case $v in
    p3) run $R/p3_sea --path . --resolution 640x360 --script $H/ph_p3_sea.gd -- --out $R/p3_sea --guide 6656 4096 ;;
    life) run $R/life --path . --resolution 1920x1080 --script $H/ph_life.gd -- life $S $R/life uv:-3,11.7
          run $R/life_nowind --path . --resolution 1920x1080 --script $H/ph_life.gd -- life $S $R/life_nowind uv:-3,11.7 --no-wind ;;
    sea) run $R/life_sea --path . --resolution 1920x1080 --script $H/ph_life.gd -- life $S $R/life_sea uv:-29,-5.5 ;;
    p9c) run $R/p9c_rest --path . --resolution 1920x1080 --script $H/ph_life.gd -- life $S $R/p9c_rest uv:-23.976,-21.834 --floe-pairs 5
         run $R/p9c_red --path . --resolution 1920x1080 --script $H/ph_life.gd -- life $S $R/p9c_red uv:-23.976,-21.834 --floe-pairs 5 --floe-red ;;
    p9c_l5) run $R/p9c_l5_rest --path . --resolution 1920x1080 --script $H/ph_life.gd -- life $S $R/p9c_l5_rest uv:-18.409,-23.42 --floe-pairs 5
            run $R/p9c_l5_red --path . --resolution 1920x1080 --script $H/ph_life.gd -- life $S $R/p9c_l5_red uv:-18.409,-23.42 --floe-pairs 5 --floe-red ;;
    null) for m in bobt rigid static; do
            run $R/p9c_null_$m --path . --resolution 1920x1080 --script $H/ph_life.gd -- life $S $R/p9c_null_$m uv:-23.976,-21.834 --floe-pairs 5 --floe-null $m
          done ;;
    idprobe) run $R/p9c_idprobe --path . --resolution 1920x1080 --script $H/ph_life.gd -- life $S $R/p9c_idprobe uv:-23.976,-21.834 --floe-pairs 2 --floe-null static --floe-ids --floe-solo ;;
    v3) for vw in main:-23.976,-21.834 l5:-18.409,-23.42; do
          n=${vw%%:*}; uv=${vw#*:}
          for m in rigid static bobt; do
            run $R/v3_${n}_$m --path . --resolution 1920x1080 --script $H/ph_life.gd -- life $S $R/v3_${n}_$m uv:$uv --floe-pairs 5 --floe-null $m --floe-ids --floe-solo
          done
          run $R/v3_${n}_red --path . --resolution 1920x1080 --script $H/ph_life.gd -- life $S $R/v3_${n}_red uv:$uv --floe-pairs 5 --floe-null bobt --floe-red --floe-ids --floe-solo
        done ;;
  esac
done
