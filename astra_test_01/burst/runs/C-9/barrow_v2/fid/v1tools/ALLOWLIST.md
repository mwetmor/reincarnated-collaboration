# BV2F Tier-B ALLOWLIST (lane PT, 0.3; R-C9-163 B-1, R-C9-166)

Each Tier-B file may differ from its v1 source (git at the pin in `PIN_COMMIT`) ONLY by replacing the v1 lines listed in its `allow` block. **Added lines (Gate-2 W-1, enforced by `verify.sh`):** every non-blank added line carries `BV2F` or sits inside a `BV2F-BEGIN` … `BV2F-END` block. Blank lines are exempt. `verify.sh` fails if a patch removes any v1 line not listed here, or if `patch(v1, patches/<file>.diff) != shipped file`.

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

## guided_paint.py

DEV-10 (charter § 7, R-C9-189 Phase 2'): ONE added line appends `cfg['chunk_notes'][k]` (per-chunk notes generated from the ID render by fid/pt/tools/chunk_notes.py) to the brief when the cfg carries it; a cfg without `chunk_notes` gives v1's brief byte for byte. No v1 line is removed. The Tier-A v1 copy (tierA/conductor_scripts/guided_paint.py) is kept unchanged; the driver calls this Tier-B copy.

```allow guided_paint.py
```

## guided_stitch.py

DEV-23 (R-C9-241, Pilot Repaint 2): a LOW-FREQUENCY TONE MATCH at each chunk's pasted-context boundary, BEFORE v1's partition-of-unity ramps -- the colour step between the ICE/SNOW pixels (bright, low chroma) of the context side (the strip's last 48 px) and of the NEW paint's first 48 px, smoothed along the boundary (normalised Gaussian, sigma 56 px; none where the boundary crosses no ice/snow), is added to the NEW paint's ice/snow pixels (soft mask: rock, wood, scrub, dark water untouched) and faded to 0 over 300 px into the chunk (smoothstep); the context strip is untouched. Only a smooth field is added; high-frequency paint detail is untouched. Added lines only (a BV2F-BEGIN/END block + two marked lines); no v1 line is removed. DEV-25 (R-C9-248): after DEV-23, a GRAIN-AMPLITUDE MATCH at the same boundary -- the detail (image minus a 3 px Gaussian) of the NEW paint is scaled by the snow/ice ratio strip/new (smoothed along the boundary, clipped 0.5..1.0: it only softens) fading to 1 over 300 px; no pixel moves, only the detail's amplitude. A second BV2F-BEGIN/END block + two marked lines; no v1 line removed. DEV-26 (R-C9-249): a MINIMUM-ERROR BOUNDARY CUT replaces v1's straight linear ramps -- one dynamic-programming path per global overlap band (least squared difference between the two chunks, objects = non-snow/ice pixels cost 4000 so the cut threads snow and ice), feathered 12 px (smoothstep), paths kept 14 px inside the band; the chunk weights stay a partition of unity (v1's assert unchanged). A third BV2F-BEGIN/END block + two marked lines; no v1 line removed. BV2F_DEV23=0 BV2F_DEV25=0 BV2F_DEV26=0 gives v1's stitch byte for byte. The Tier-A v1 copy is kept; PT's build calls this Tier-B copy.



```allow guided_stitch.py
```
