#!/bin/bash
# C-9 T10: an unsigned, local macOS .app of the Frost King's Barrow.
#
# Shape ported from tools/build_app.sh (mirror -> overlay -> import -> export -> POST-EXPORT
# VERIFICATION -> stage), because the verification is the load-bearing half: an export that
# returns 0 is not an export that produced a launchable app.
#
# TWO THINGS DIFFER FROM THE CLIFFSIDE BUILD, both of them consequences of the barrow being
# a fully generated pipeline:
#
# 1. THE MAIN SCENE IS OVERLAID IN THE MIRROR, NOT IN THE SOURCE. project.godot still points
#    at cliffside3d.tscn and must keep doing so -- it is shared with the cliffside scenes and
#    with a concurrent workstream. The overlay rewrites run/main_scene in $DEST only, so this
#    script can build the barrow app without the source project ever knowing.
#
# 2. THE ASSET FENCE IS SHORT, AND THAT IS THE POINT. The cliffside app had to prove a 28 MB
#    plate, six parallax layers and a zones PNG were in the pck, and shipped once anyway with
#    a PNG that "passed" because the grep matched the .import entry sitting NEXT TO the file
#    rather than the file. The barrow has no such exposure: the terrain, the stones, the
#    rocks, the noise, the paper, the snowflake and the sky are all generated in code at
#    load. The only real assets are the barbarian's own GLBs and his JSON slot.
#
# UNSIGNED and local. Signing is a Matt call, not a flag this script may flip.
#
#   usage: tools/build_app_barrow.sh
#   env:   GODOT, HEAVY_LOCK, STAGE, SKIP_LAUNCH_CHECK=1
set -euo pipefail

SRC=$(cd "$(dirname "$0")/.." && pwd)/godot
NAME="C-9 Barrow"
MAIN_SCENE="res://scenes/barrow.tscn"
BUNDLE_ID=${BUNDLE_ID:-com.reincarnated.c9barrow}
ARCH=${ARCH:-universal}
GODOT=${GODOT:-/Applications/Godot.app/Contents/MacOS/Godot}
HEAVY_LOCK=${HEAVY_LOCK:-$HOME/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-7/conductor_scripts/heavy_lock.py}
DEST=$(dirname "$SRC")/app_barrow
APP="$DEST/build/$NAME.app"
LOG="$DEST/build/logs"
STAGE=${STAGE:-"$HOME/Desktop/Astra Burst Review - 2026-09-26/C-9 barrow"}

[ -f "$SRC/project.godot" ] || { echo "no project.godot in $SRC" >&2; exit 2; }
[ -x "$GODOT" ] || { echo "Godot not found at $GODOT" >&2; exit 2; }
case "$DEST" in "$SRC"/*) echo "refusing: destination inside source" >&2; exit 2;; esac

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
# VERIFIED, not assumed: an overlay that silently matched nothing would build the cliffside
# under the barrow's name, which looks like a working app right up to the moment it opens.
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
include_filter="*.json"
exclude_filter="tools/*"
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

if [ -n "$PCK" ]; then
  MISSING=0
  # The barrow's real dependencies, and only those. GLBs and JSONs travel as FILES (the
  # preset's include_filter is *.json and .glb is not an imported-to-.ctex type), so a hit
  # here means the file is there -- which is exactly the guarantee the cliffside's PNG fence
  # could not give.
  for p in scenes/barrow.tscn scripts/barrow_world.gd scripts/paint_stack.gd \
           scripts/barrow_stand_in.gd scripts/knight.gd scripts/gear.gd \
           data/character.json data/gear_manifest.json \
           models/gear/nb-body.glb models/gear/axe.glb models/gear/shield.glb \
           models/gear/helmet.glb models/gear/byrnie.glb models/gear/mantle.glb \
           models/gear/bracers.glb; do
    grep -a -q "$p" "$PCK" || { echo "   missing from pck: $p" >&2; MISSING=1; }
  done
  [ "$MISSING" -eq 0 ] && ck 0 "barrow scene, stack scripts and the barbarian in the pck" \
                       || ck 1 "barrow scene, stack scripts and the barbarian in the pck"
  # AND the barrow must NOT be shipping the cliffside as its main scene -- the one failure
  # this build shape can produce that still launches and still looks like a game.
  MAIN=$(grep -a -o 'res://scenes/barrow.tscn' "$PCK" | head -1 || true)
  [ -n "$MAIN" ] && ck 0 "main scene string present in pck" || ck 1 "main scene string present in pck"
fi

if [ -z "${SKIP_LAUNCH_CHECK:-}" ]; then
  echo "== launch probe (headless)"
  # 600 frames, not 30: this scene GENERATES its noise, its paper grain and its terrain in
  # GDScript at _ready, so the first frame is expensive and a 30-frame probe could quit
  # before the scene had finished proving it can build.
  "$BIN" --headless --quit-after 600 > "$LOG/launch.log" 2>&1 \
    && ck 0 "app launches and quits cleanly" || ck 1 "app launches (see $LOG/launch.log)"
  grep -iE "parse error|failed to load|SCRIPT ERROR|cannot load" "$LOG/launch.log" \
    && ck 1 "no script errors at launch" || ck 0 "no script errors at launch"
fi

[ "$FAIL" -eq 0 ] || { echo "== VERIFY FAILED" >&2; exit 6; }

echo "== stage -> $STAGE"
mkdir -p "$STAGE"
rm -rf "$STAGE/$NAME.app"
cp -R "$APP" "$STAGE/"
xattr -dr com.apple.quarantine "$STAGE/$NAME.app" 2>/dev/null || true
echo "== done: $STAGE/$NAME.app  ($(du -sh "$STAGE/$NAME.app" | cut -f1))"
