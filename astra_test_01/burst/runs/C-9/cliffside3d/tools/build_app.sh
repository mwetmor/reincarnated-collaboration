#!/bin/bash
# C-9 R-C9-61: build an unsigned, local macOS .app of the character-test cliffside.
#
# Shape ported from runs/C-9/cliffside_B/tools/build_app.sh (mirror -> overlay ->
# import -> export -> POST-EXPORT VERIFICATION -> stage). Only the target and the
# verification list change; the verification is the load-bearing half, because an
# export that returns 0 is not an export that produced a launchable app.
#
#   usage: tools/build_app.sh
#   env:   GODOT, HEAVY_LOCK, STAGE, SKIP_LAUNCH_CHECK=1
#
# UNSIGNED and local. Signing is a Matt call, not a flag this script may flip.
set -euo pipefail

SRC=$(cd "$(dirname "$0")/.." && pwd)/godot
NAME="C-9 Cliffside 3D"
BUNDLE_ID=${BUNDLE_ID:-com.reincarnated.c9cliffside3d}
ARCH=${ARCH:-universal}
GODOT=${GODOT:-/Applications/Godot.app/Contents/MacOS/Godot}
HEAVY_LOCK=${HEAVY_LOCK:-$HOME/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-7/conductor_scripts/heavy_lock.py}
DEST=$(dirname "$SRC")/app
APP="$DEST/build/$NAME.app"
LOG="$DEST/build/logs"
STAGE=${STAGE:-"$HOME/Desktop/Astra Burst Review - 2026-09-26/C-9 cliffside 3D"}

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

# MUST precede the import: Godot refuses a universal macOS export outright without
# ETC2/ASTC enabled, and the flag changes what --import emits.
echo "== overlay project settings"
python3 - "$DEST" <<'PY'
import pathlib, re, sys
pg = pathlib.Path(sys.argv[1]) / "project.godot"
t = pg.read_text()
line = "textures/vram_compression/import_etc2_astc=true"
if line not in t:
    m = re.search(r"^\[rendering\]\s*$", t, re.M)
    t = (t[:m.end()] + "\n" + line + t[m.end():]) if m \
        else t.rstrip("\n") + "\n\n[rendering]\n\n" + line + "\n"
    pg.write_text(t)
    print("overlay set:", line)
else:
    print("overlay: already applied")
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
  # What this scene cannot run without. The plate IS the test, and a missing 28 MB
  # texture exports cleanly and renders a grey box that looks like a build problem
  # rather than a missing asset.
  MISSING=0
  # NOTE on what a hit here means: a PNG is IMPORTED to .ctex, so its path survives in the
  # pck only inside the .import entry -- the grep matches the entry, not the file. That is
  # the trap that shipped an app which passed this fence and then failed at launch on
  # `Error opening file data/v4_zones.png`. The JSONs below travel as real files (the
  # preset's include_filter is *.json) and for those a hit does mean the file is there.
  for p in plate/plate_v4.png data/v4_layout.json data/v4_zones.png data/parallax.json \
           data/figure.json data/character.json data/landmarks.json props/props.json \
           models/gear/nb-body.glb data/gear_manifest.json scripts/cliffside_blockout.gd \
           models/gear/helmet.glb models/gear/byrnie.glb models/gear/axe.glb \
           layers/sky.png layers/far_ruins.png layers/forest_valley.png layers/mist.png \
           layers/landmarks/cathedral.png layers/landmarks/tower.png \
           props/assets/tree_living_a.png props/assets/bridge_post_1.png; do
    grep -a -q "$p" "$PCK" || { echo "   missing from pck: $p" >&2; MISSING=1; }
  done
  [ "$MISSING" -eq 0 ] && ck 0 "plate, layout, layers and model in the pck" \
                       || ck 1 "plate, layout, layers and model in the pck"
fi

if [ -z "${SKIP_LAUNCH_CHECK:-}" ]; then
  echo "== launch probe (headless, 1 frame)"
  "$BIN" --headless --quit-after 30 > "$LOG/launch.log" 2>&1 \
    && ck 0 "app launches and quits cleanly" || ck 1 "app launches (see $LOG/launch.log)"
  grep -iE "parse error|failed to load|SCRIPT ERROR" "$LOG/launch.log" \
    && ck 1 "no script errors at launch" || ck 0 "no script errors at launch"
fi

[ "$FAIL" -eq 0 ] || { echo "== VERIFY FAILED" >&2; exit 6; }

echo "== stage -> $STAGE"
mkdir -p "$STAGE"
rm -rf "$STAGE/$NAME.app"
cp -R "$APP" "$STAGE/"
xattr -dr com.apple.quarantine "$STAGE/$NAME.app" 2>/dev/null || true
echo "== done: $STAGE/$NAME.app  ($(du -sh "$STAGE/$NAME.app" | cut -f1))"
