# BV2F Tier-B ALLOWLIST (lane PT, 0.3; R-C9-163 B-1, R-C9-166)

Each Tier-B file may differ from its v1 source (git at the pin in `PIN_COMMIT`) ONLY by replacing the v1 lines listed in its `allow` block. Added lines are free-form but every one carries `BV2F` or sits in the appended `_bv2f_frame_grid` loader / the marked block. `verify.sh` fails if a patch removes any v1 line not listed here, or if `patch(v1, patches/<file>.diff) != shipped file`.

## capture_blockout.gd

GUIDE (guide render size), TOP/TOP_PX_PER_M (top-down map size/scale), GRID_* (walk-grid extent/step) become vars read from --frame-grid; the scene literal becomes SCENE. Defaults = v1. Not parameterised: PLAY 1920x1080 (play frame, M0(c) keeps v1 zoom), CRUCIBLE_SHOT (v1-only still), the comment at :111.

```allow capture_blockout.gd
const GUIDE := Vector2i(5376, 3328)
const TOP_PX_PER_M := 40.0
const TOP := Vector2i(2296, 1816)
const GRID_STEP := 0.1
const GRID_U := Vector2(-21.0, 18.0)
const GRID_V := Vector2(-19.0, 12.0)
	scene = load("res://scenes/barrow_full.tscn").instantiate()
```

## capture_ids.gd

GUIDE and the scene literal from --frame-grid; the two label strings that print 5376x3328 now format GUIDE (identical bytes for v1). Not parameterised: the formula constants 100.617553710938 / 80.3076 at :131-132 and :149 (px/m and pitch are v1's under M0(c)).

```allow capture_ids.gd
const GUIDE := Vector2i(5376, 3328)
	scene = load("res://scenes/barrow_full.tscn").instantiate()
		"_what": "C-9 T10-2 step 3: the guide view (5376 x 3328, capture_blockout's camera) as an ID render",
	print("[ids] ids.png 5376x3328, %d placements, camera vs px_from_uv worst %.3f px over %d points" % [
		idx, worst, n_chk])
```

## paint_world_prep.py

painting path + sha prefix, PPM, PITCH, yaw (C47/S47 names kept) from $BV2F_FRAME_GRID; defaults = v1. Not parameterised: LIT/OUT/TAKE/layout paths (BF-relative: the root comes from v1run.py), web constants, heather grade, snow field px.

```allow paint_world_prep.py
PAINTING = os.path.join(BF, "paint", "barrow_full_painted.png")
PAINT_SHA_PREFIX = "eecb42661af490dd"
PPM = 100.617553710938
PITCH = math.radians(52.95354112560294)
C47, S47 = math.cos(math.radians(47.0)), math.sin(math.radians(47.0))
```

## t10bf_drive.sh

every tool call -> frozen Tier-A copies ($A); verify.sh first (exit 8); cfg is argv[1]; prefix and log name from the cfg; usage/rate-limit text in a burst's run json/err -> exit 7 (DEV-15, regex = barrow_v2/tools/*_drive.sh). Disk guard 20 GiB kept (charter § 6 gate).

```allow t10bf_drive.sh
B=/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst; C=$B/runs/C-9/conductor_scripts; CFG=$C/cfg_t10bf.json
L=$HOME/astra-burst/logs/C-9; mkdir -p $L; LOG=$L/t10bf_drive.log
echo "$(date -u +%FT%TZ) T10BF DRIVE START" >> $LOG
  ready=($(python3 $C/guided_paint.py $CFG ready))
  [ ${#ready} -eq 0 ] && { echo "$(date -u +%FT%TZ) T10BF DRIVE DONE (nothing ready)" >> $LOG; break; }
    SUF=$suf python3 $C/guided_paint.py $CFG stage $k >> $LOG 2>&1
    SUF=$suf python3 $C/guided_paint.py $CFG brief $k >> $LOG 2>&1
    if ! python3 $C/refs_guard.py briefs/C-9/T10BF-$k$suf.task.json >> $LOG 2>&1; then
      echo "$(date -u +%FT%TZ) HALT H-guard on T10BF-$k$suf" >> $LOG; exit 3; fi
    specs+=("T10BF-$k$suf:GENERATE")
  wl="t10bf_w$(date +%s)"
  zsh $C/wave.sh $wl ${specs[@]}
    bid=${s%%:*}; k=${${bid#T10BF-}%-r1}
```

## take_from_paint.py

painting default path + sha prefix from $BV2F_FRAME_GRID; defaults = v1. Frame is already read from the layout JSON; RES/GRES (m-based rasters) and the px filter sizes (valid at v1's px/m, unchanged under M0(c)) are not parameterised.

```allow take_from_paint.py
PAINTING = args[args.index("--painting") + 1] if "--painting" in args else os.path.join(BF, "paint", "barrow_full_painted.png")
PAINT_SHA_PREFIX = "eecb42661af490dd"          # the stitched paint-over the coordinator accepted
```
