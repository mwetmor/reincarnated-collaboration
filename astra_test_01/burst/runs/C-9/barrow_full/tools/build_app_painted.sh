#!/bin/bash
# C-9 T10-2 step 4: an unsigned, local macOS .app of the PAINTED Barrow -- the blockout dressed in
# the painting (scenes/barrow_painted.tscn) -- built from this sandbox, never from cliffside3d.
# tools/build_app.sh (the blockout app) is its template; what differs is marked PAINTED.
#
# PAINTED: THE LAUNCH LINE PROVES THE PAINTING LOADED (the splat-load lesson). Every painted file
# ships as its own raw bytes (a PNG or float32 buffer named .bin -- the importer never touches it,
# and the include_filter ships the file itself), and the running scene reads each one and checks its
# sha256 against data/painted/manifest.json. The probe greps that line: files_sha_ok=28/28, the
# painting, the ground, the light map, the snow's grid, 25/25 bakes, 29/29 primitives wearing the
# painting. The pck fence proves the files are THERE; only the running scene proves it READ them.
#
# Shape copied from cliffside3d/tools/build_app_barrow.sh: mirror -> overlay -> import ->
# export -> POST-EXPORT VERIFICATION -> stage. The verification is the load-bearing half: an
# export that returns 0 is not an export that produced a launchable app.
#
# THE FENCE IS THE BLOCKOUT'S OWN DEPENDENCIES: the scene, the five scripts, the layout JSON,
# the splat (PNG bytes named .bin -- the scene reads the raw file, and an include_filter ships
# only NON-resource files, so a .png would have shipped as its import and not as itself; the
# first build did exactly that and passed this fence, because the grep matched the path string
# elsewhere in the pck), the 7 welded Barrow models, the 3 kit models and the barbarian's GLBs. And the launch probe greps the line the scene prints once it has BUILT,
# which includes whether the splat's sha256 matched the layout: the pck fence proves a file
# is there, only the running scene can say it read the right one.
#
# THE VIEW IS LOCKED TO 16:9 by the project itself (stretch canvas_items, aspect keep, base
# 1920 x 1080), mirrored with the rest of godot/; the probe checks the app reports it.
#
# UNSIGNED and local. Signing is a Matt call, not a flag this script may flip.
#
#   usage: tools/build_app.sh
#   env:   GODOT, HEAVY_LOCK, STAGE, SKIP_LAUNCH_CHECK=1
set -euo pipefail

ROOT=$(cd "$(dirname "$0")/.." && pwd)
SRC=$ROOT/godot
NAME="C-9 Barrow painted"
MAIN_SCENE="res://scenes/barrow_painted.tscn"
BUNDLE_ID=${BUNDLE_ID:-com.reincarnated.c9barrowpainted}
ARCH=${ARCH:-universal}
GODOT=${GODOT:-/Applications/Godot.app/Contents/MacOS/Godot}
HEAVY_LOCK=${HEAVY_LOCK:-$HOME/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-7/conductor_scripts/heavy_lock.py}
DEST=$ROOT/app
APP="$DEST/build/$NAME.app"
LOG="$DEST/build/logs"
STAGE=${STAGE:-"$HOME/Desktop/Astra Burst Review - 2026-09-26/C-9 barrow full"}

[ -f "$SRC/project.godot" ] || { echo "no project.godot in $SRC" >&2; exit 2; }
[ -x "$GODOT" ] || { echo "Godot not found at $GODOT" >&2; exit 2; }
case "$DEST" in "$SRC"/*) echo "refusing: destination inside source" >&2; exit 2;; esac
case "$SRC" in */cliffside3d/*) echo "refusing: this script never builds from cliffside3d" >&2; exit 2;; esac

GATE=${DISK_GATE_GIB:-20}          # the conductor's gate (2026-09-30)
FREE=$(df -g /System/Volumes/Data | awk 'NR==2{print $4}')
echo "== free disk: ${FREE} GiB (gate ${GATE})"
if [ "$FREE" -lt "$GATE" ]; then echo "HALT: under ${GATE} GiB free" >&2; exit 9; fi

if [ -z "${C9_LOCKED:-}" ]; then
  [ -f "$HEAVY_LOCK" ] || { echo "HALT: heavy lock not found at $HEAVY_LOCK" >&2; exit 3; }
  echo "== acquiring heavy lock"
  exec env C9_LOCKED=1 python3 "$HEAVY_LOCK" C-9 -- bash "$0" "$@"
fi

echo "== mirror $SRC -> $DEST"
mkdir -p "$DEST" "$LOG"
rsync -a --delete --exclude '.godot/' --exclude 'build/' --exclude 'export_presets.cfg' \
  "$SRC"/ "$DEST"/

echo "== overlay project settings (main scene + name + ETC2/ASTC), in the MIRROR only"
python3 - "$DEST" "$MAIN_SCENE" "$NAME" <<'PY'
import pathlib, re, sys
dest, scene, name = sys.argv[1], sys.argv[2], sys.argv[3]
pg = pathlib.Path(dest) / "project.godot"
t = pg.read_text()
t = re.sub(r'^run/main_scene=".*"$', 'run/main_scene="%s"' % scene, t, flags=re.M)
t = re.sub(r'^config/name=".*"$', 'config/name="%s"' % name, t, flags=re.M)
line = "textures/vram_compression/import_etc2_astc=true"
if line not in t:
    m = re.search(r"^\[rendering\]\s*$", t, re.M)
    t = (t[:m.end()] + "\n" + line + t[m.end():]) if m \
        else t.rstrip("\n") + "\n\n[rendering]\n\n" + line + "\n"
pg.write_text(t)
got = dict(re.findall(r'^(run/main_scene|config/name)="(.*)"$', t, flags=re.M))
assert got.get("run/main_scene") == scene, "main scene overlay did not apply: %r" % got
assert got.get("config/name") == name, "name overlay did not apply: %r" % got
print("overlay ok:", got)
PY

echo "== preset: macOS / $ARCH / $BUNDLE_ID (UNSIGNED)"
cat > "$DEST/export_presets.cfg" <<EOF
[preset.0]

name="macOS"
platform="macOS"
runnable=true
advanced_options=false
dedicated_server=false
custom_features=""
export_filter="all_resources"
include_filter="*.json,data/*.bin,data/painted/*.bin,data/painted/bakes/*.bin,data/vfx/*/*.bin"
exclude_filter="tools/*,data/painted/ground_inpainted.bin"
export_path="build/$NAME.app"
patches=PackedStringArray()
encryption_include_filters=""
encryption_exclude_filters=""
seed=0
encrypt_pck=false
encrypt_directory=false
script_export_mode=2

[preset.0.options]

export/distribution_type=0
binary_format/architecture="$ARCH"
custom_template/debug=""
custom_template/release=""
debug/export_console_wrapper=1
application/icon=""
application/icon_interpolation=4
application/bundle_identifier="$BUNDLE_ID"
application/signature=""
application/app_category="Games"
application/short_version=""
application/version=""
application/copyright=""
application/copyright_localized={}
application/min_macos_version="10.12"
application/min_macos_version_x86="10.12"
application/export_angle=0
application/additional_plist_content=""
display/high_res=true
xcode/platform_build="14C18"
xcode/sdk_version="13.1"
xcode/sdk_build="22C55"
xcode/sdk_name="macosx13.1"
xcode/xcode_version="1420"
xcode/xcode_build="14C18"
codesign/codesign=0
codesign/installer_identity=""
codesign/apple_team_id=""
codesign/identity=""
codesign/entitlements/custom_file=""
codesign/custom_options=PackedStringArray()
notarization/notarization=0
privacy/microphone_usage_description=""
privacy/camera_usage_description=""
privacy/location_usage_description=""
privacy/address_book_usage_description=""
privacy/calendar_usage_description=""
privacy/photos_library_usage_description=""
privacy/desktop_folder_usage_description=""
privacy/documents_folder_usage_description=""
privacy/downloads_folder_usage_description=""
privacy/network_volumes_usage_description=""
privacy/removable_volumes_usage_description=""
privacy/tracking_usage_description=""
privacy/tracking_domains=PackedStringArray()
ssh_remote_deploy/enabled=false
EOF

echo "== import"
"$GODOT" --headless --path "$DEST" --import > "$LOG/import.log" 2>&1 || {
  echo "import failed" >&2; tail -20 "$LOG/import.log" >&2; exit 4; }

echo "== export macOS"
mkdir -p "$DEST/build"; rm -rf "$APP"
"$GODOT" --headless --path "$DEST" --export-release "macOS" "build/$NAME.app" \
  > "$LOG/export.log" 2>&1 || {
  echo "export failed" >&2; tail -30 "$LOG/export.log" >&2; exit 5; }

echo "== verify"
FAIL=0
ck() { if [ "$1" = 0 ]; then echo "   ok   $2"; else echo "   FAIL $2" >&2; FAIL=1; fi; }

[ -d "$APP" ] && ck 0 ".app bundle exists" || ck 1 ".app bundle exists"
PLIST="$APP/Contents/Info.plist"
[ -f "$PLIST" ] && ck 0 "Info.plist present" || ck 1 "Info.plist present"
EXE_NAME=$(/usr/libexec/PlistBuddy -c "Print :CFBundleExecutable" "$PLIST" 2>/dev/null || echo "")
BIN="$APP/Contents/MacOS/$EXE_NAME"
[ -n "$EXE_NAME" ] && ck 0 "CFBundleExecutable declared ('$EXE_NAME')" || ck 1 "CFBundleExecutable declared"
[ -x "$BIN" ] && ck 0 "executable present and executable" || ck 1 "executable at Contents/MacOS/$EXE_NAME"
GOT_ARCH=$(lipo -archs "$BIN" 2>/dev/null || echo "?")
echo "   info binary arch: $GOT_ARCH (requested $ARCH)"
echo "$GOT_ARCH" | grep -q arm64 && ck 0 "binary runs on Apple Silicon" || ck 1 "binary runs on Apple Silicon"

PCK=$(find "$APP/Contents/Resources" -name '*.pck' | head -1 || true)
[ -n "$PCK" ] && ck 0 "pck present ($(basename "$PCK"), $(du -h "$PCK" | cut -f1))" || ck 1 "pck present"
# her Fire Ball's atlas and table, by the pck's own file table (C-9 (c))
FBN=$(python3 "$ROOT/tools/pck_list.py" "$PCK" | grep -c "^data/vfx/fire_ball/" || true)
[ "$FBN" -ge 3 ] && ck 0 "her Fire Ball in the pck: $FBN files (fire_ball.json, 2 atlas pages)" || ck 1 "her Fire Ball in the pck ($FBN files)"

if [ -n "$PCK" ]; then
  MISSING=0
  BAKES=$(python3 -c "import json;print(' '.join('data/painted/'+b['file'] for b in json.load(open('$SRC/data/painted/manifest.json'))['bakes'].values()))")
  for p in scenes/barrow_painted.tscn scripts/barrow_full.gd scripts/painted_world.gd scripts/paint_stack.gd \
           scripts/snow_field.gd scripts/barrow_heather.gd \
           scripts/knight.gd scripts/gear.gd scripts/foot_lock.gd scripts/world.gd \
           data/character.json data/gear_manifest.json data/barrow_full_layout.json \
           data/painted/manifest.json data/painted/heather.json data/painted/painting.bin \
           data/painted/lit.bin data/painted/snow_grid.bin $BAKES \
           models/barrow/stone_tall.glb models/barrow/stone_mid.glb models/barrow/stone_short.glb \
           models/barrow/lintel.glb models/barrow/post.glb models/barrow/raven.glb \
           models/barrow/birch.glb models/barrow/kit/log.glb models/barrow/kit/cairn.glb \
           models/barrow/kit/shield.glb \
           models/gear/nb-body.glb models/gear/axe.glb models/gear/shield.glb \
           models/gear/helmet.glb models/gear/byrnie.glb models/gear/mantle.glb \
           models/gear/bracers.glb; do
    grep -a -q "$p" "$PCK" || { echo "   missing from pck: $p" >&2; MISSING=1; }
  done
  [ "$MISSING" -eq 0 ] && ck 0 "painted scene, scripts, layout, the painting, the light map, the snow grid, 25 bakes, 10 world models and the barbarian in the pck" \
                       || ck 1 "painted scene, scripts, layout, the painting, the light map, the snow grid, 25 bakes, 10 world models and the barbarian in the pck"
  MAIN=$(grep -a -o 'res://scenes/barrow_painted.tscn' "$PCK" | head -1 || true)
  [ -n "$MAIN" ] && ck 0 "main scene string present in pck" || ck 1 "main scene string present in pck"
fi

if [ -z "${SKIP_LAUNCH_CHECK:-}" ]; then
  echo "== launch probe (headless)"
  "$BIN" --headless --quit-after 900 > "$LOG/launch.log" 2>&1 \
    && ck 0 "app launches and quits cleanly" || ck 1 "app launches (see $LOG/launch.log)"
  grep -iE "parse error|failed to load|SCRIPT ERROR|cannot load" "$LOG/launch.log" \
    && ck 1 "no script errors at launch" || ck 0 "no script errors at launch"
  grep -q "\[barrow_full\] built placements=" "$LOG/launch.log" \
    && ck 0 "the scene printed that it BUILT: $(grep -o '\[barrow_full\] built.*' "$LOG/launch.log" | head -1)" \
    || ck 1 "the scene never printed its build line -- see $LOG/launch.log"
  grep -q "splat_ok=true" "$LOG/launch.log" \
    && ck 0 "the app read the splat and its sha256 matched the layout" \
    || ck 1 "the splat did not load or did not match -- see $LOG/launch.log"
  # THE 16:9 LOCK, as the running app reports it -- project.godot is in the pck either way;
  # only the app can say the window it opens will honour it.
  grep -q "\[barrow_full\] view stretch=canvas_items aspect=keep base=1920x1080" "$LOG/launch.log" \
    && ck 0 "the view is locked: $(grep -o '\[barrow_full\] view.*' "$LOG/launch.log" | head -1)" \
    || ck 1 "the 16:9 view lock is not in force -- see $LOG/launch.log"
  # PAINTED: what it READ, sha-checked, from the pck
  PL=$(grep -o '\[barrow_painted\] .*' "$LOG/launch.log" | head -1 || true)
  echo "   info $PL"
  echo "$PL" | grep -q "files_sha_ok=28/28 painting_ok=true ground=painting.bin(as_painted)_ok=true lit_ok=true snow_grid_ok=true" \
    && ck 0 "the painting (ground, mound, primitives), the light map and the snow grid loaded from the pck, sha256 matched" \
    || ck 1 "a painted file did not load or did not match its sha256 -- see $LOG/launch.log"
  echo "$PL" | grep -q "plates: bakes=25/25 on the real models, painting on primitives=29/29" \
    && ck 0 "all 54 plates in place: 25/25 bakes read and matched, 29/29 primitives wearing the painting" \
    || ck 1 "not every plate is in place -- see $LOG/launch.log"
  echo "$PL" | grep -q "heather=977 snow=true" \
    && ck 0 "the 977 heather sprays and the 3D snow built" || ck 1 "the heather or the snow did not build"
fi

[ "$FAIL" -eq 0 ] || { echo "== VERIFY FAILED" >&2; exit 6; }

echo "== stage -> $STAGE"
mkdir -p "$STAGE"
rm -rf "$STAGE/$NAME.app"
cp -R "$APP" "$STAGE/"
xattr -dr com.apple.quarantine "$STAGE/$NAME.app" 2>/dev/null || true
echo "== done: $STAGE/$NAME.app  ($(du -sh "$STAGE/$NAME.app" | cut -f1))"
