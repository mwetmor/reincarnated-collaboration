#!/bin/bash
# C-9: build an unsigned, local macOS .app of the cliffside A/B build and stage it
# where Matt can double-click it.
#
# The SHAPE is ported from reincarnated-godot/desktop/build_desktop.sh (KC2-PLAY
# Wave 1), which is the pipeline this project already proved on this Mac: mirror ->
# overlay -> headless import -> export-release -> POST-EXPORT VERIFICATION -> stage.
# Only the target changes. That script is read-only for this run (it writes inside
# reincarnated-godot, which this run may not touch), so its shape is re-implemented
# here and writes stay inside runs/C-9/.
#
#   usage: tools/build_app.sh
#   env:   GODOT       default /Applications/Godot.app/Contents/MacOS/Godot
#          HEAVY_LOCK  C-7's shared advisory lock; all Godot work runs under it
#          STAGE       staging directory on the Desktop
#          SKIP_LAUNCH_CHECK=1 to skip the headless launch probe
#
# UNSIGNED and local. Signing/notarisation is a Matt call, not a flag this script
# may flip; it clears the quarantine bit by hand instead, in the open.
set -euo pipefail

SRC=$(cd "$(dirname "$0")/.." && pwd)
NAME="C-9 Cliffside AB"
BUNDLE_ID=${BUNDLE_ID:-com.reincarnated.c9cliffsideab}
ARCH=${ARCH:-universal}   # what the STOCK 4.6.3 macos template can build; arm64 needs a custom template
GODOT=${GODOT:-/Applications/Godot.app/Contents/MacOS/Godot}
HEAVY_LOCK=${HEAVY_LOCK:-$HOME/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-7/conductor_scripts/heavy_lock.py}
DEST=$(dirname "$SRC")/cliffside_B_app
APP="$DEST/build/$NAME.app"
LOG="$DEST/build/logs"
STAGE=${STAGE:-"$HOME/Desktop/Astra Burst Review - 2026-09-26/C-9 cliffside AB v2"}

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

# MUST precede the import: Godot refuses a universal/arm64 macOS export outright
# without ETC2/ASTC enabled, and the flag changes what --import emits.
echo "== overlay project settings"
python3 - "$DEST" <<'PY'
import pathlib, re, sys
pg = pathlib.Path(sys.argv[1]) / "project.godot"
t = pg.read_text()
line = "textures/vram_compression/import_etc2_astc=true"
if line not in t:
    m = re.search(r"^\[rendering\]\s*$", t, re.M)
    if m:
        t = t[:m.end()] + "\n" + line + t[m.end():]
    else:
        t = t.rstrip("\n") + "\n\n[rendering]\n\n" + line + "\n"
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
  echo "import failed; see $LOG/import.log" >&2; tail -20 "$LOG/import.log" >&2; exit 4; }

echo "== export macOS"
mkdir -p "$DEST/build"
rm -rf "$APP"
"$GODOT" --headless --path "$DEST" --export-release "macOS" "build/$NAME.app" \
  > "$LOG/export.log" 2>&1 || {
  echo "export failed; see $LOG/export.log" >&2; tail -30 "$LOG/export.log" >&2; exit 5; }

# ---------------------------------------------------------------------------
# POST-EXPORT VERIFICATION — an export that returns 0 is not an export that
# produced a launchable app. This half is the load-bearing half.
# ---------------------------------------------------------------------------
echo "== verify"
FAIL=0
ck() { if [ "$1" = 0 ]; then echo "   ok   $2"; else echo "   FAIL $2" >&2; FAIL=1; fi; }

if [ -d "$APP" ]; then ck 0 ".app bundle exists"; else ck 1 ".app bundle exists"; fi
PLIST="$APP/Contents/Info.plist"
if [ -f "$PLIST" ]; then ck 0 "Info.plist present"; else ck 1 "Info.plist present"; fi

# The executable is named from config/name, NOT from the export path. Ask.
EXE_NAME=$(/usr/libexec/PlistBuddy -c "Print :CFBundleExecutable" "$PLIST" 2>/dev/null || echo "")
if [ -n "$EXE_NAME" ]; then ck 0 "CFBundleExecutable declared ('$EXE_NAME')"; else ck 1 "CFBundleExecutable declared"; fi
BIN="$APP/Contents/MacOS/$EXE_NAME"
if [ -f "$BIN" ]; then ck 0 "executable present"; else ck 1 "executable present at Contents/MacOS/$EXE_NAME"; fi
if [ -x "$BIN" ]; then ck 0 "executable bit set"; else ck 1 "executable bit set"; fi
if [ -f "$BIN" ] && file -b "$BIN" | grep -q "Mach-O"; then ck 0 "binary is Mach-O"; else ck 1 "binary is Mach-O"; fi
GOT_ARCH=$(lipo -archs "$BIN" 2>/dev/null || echo "?")
echo "   info binary arch: $GOT_ARCH (requested $ARCH)"
if echo "$GOT_ARCH" | grep -q arm64; then ck 0 "binary runs on Apple Silicon"; else ck 1 "binary runs on Apple Silicon"; fi

PCK=$(find "$APP/Contents/Resources" -name '*.pck' | head -1 || true)
if [ -n "$PCK" ] && [ -f "$PCK" ]; then ck 0 "pck present ($(basename "$PCK"), $(du -h "$PCK" | cut -f1))"
else ck 1 "pck present in Contents/Resources"; fi

BID=$(/usr/libexec/PlistBuddy -c "Print :CFBundleIdentifier" "$PLIST" 2>/dev/null || echo "")
if [ "$BID" = "$BUNDLE_ID" ]; then ck 0 "CFBundleIdentifier == $BUNDLE_ID"; else ck 1 "CFBundleIdentifier (got '$BID')"; fi

# Both texture registers AND both player sprites must actually be inside the pck. A
# build that exports cleanly with only the A set would toggle to a blank plate, or to
# an invisible player, and say nothing.
if [ -n "$PCK" ] && [ -f "$PCK" ]; then
  MISSING=0
  for p in parallax/tiles/tile_0_0.png parallax/tiles/tile_4096_0.png \
           parallax/tiles_b/tile_0_0.png parallax/tiles_b/tile_4096_0.png \
           parallax/layers/sky.png parallax/layers/far_ruins.png \
           parallax/layers/forest_valley.png parallax/layers/mist.png \
           parallax/layers_b/sky.png parallax/layers_b/far_ruins.png \
           parallax/layers_b/forest_valley.png parallax/layers_b/mist.png \
           parallax/layers_b/offsets.json \
           frames/keeper.tres frames/knight.tres \
           scenes/knight_rig_E.tscn frames/knight_rig_E.json \
           sprites_figures/angel.png sprites_figures/demon.png frames/figures_b.json; do
    # NOTE: grep the BARE path, not "res://$p". An IMPORTED resource (a .png, a .tres)
    # appears in the pck's string table as "res://<path>", but a plain INCLUDED file --
    # every .json here -- appears as "<path>" with no scheme. Checking for "res://$p"
    # therefore reports a JSON that is present and loadable as MISSING. It did exactly
    # that for parallax/layers_b/offsets.json on 2026-09-27: the check ran, returned
    # cleanly, and returned the wrong answer, because the instrument did not match the
    # domain. The bare path matches both encodings and is still unique per file.
    grep -a -q "$p" "$PCK" || { echo "   missing from pck: $p" >&2; MISSING=1; }
  done
  if [ "$MISSING" -eq 0 ]; then ck 0 "A+B textures, layer offsets and both SpriteFrames in the pck"
  else ck 1 "A+B textures, layer offsets and both SpriteFrames in the pck"; fi

  # Every knight cell x 12 frames, no mirroring. The RUN cells exist only for the
  # directions Grok delivered a clip for, so the expected count is read from
  # frames/knight_fit.json's own declaration rather than hardcoded -- a hardcoded 192
  # would pass while silently shipping no run at all.
  RUN_DIRS=$(python3 -c "import json;print(' '.join(json.load(open('$DEST/frames/knight_fit.json'))['run_directions']))")
  WANT_KN=$(python3 -c "print(16*12 + len('$RUN_DIRS'.split())*12)")
  KN=0
  for d in $RUN_DIRS; do
    for i in 00 01 02 03 04 05 06 07 08 09 10 11; do
      grep -a -q "sprites_knight/run/$d/run_${d}_${i}.png" "$PCK" && KN=$((KN+1))
    done
  done
  for d in S SW W NW N NE E SE; do
    for st in walk idle; do
      for i in 00 01 02 03 04 05 06 07 08 09 10 11; do
        grep -a -q "sprites_knight/$st/$d/${st}_${d}_${i}.png" "$PCK" && KN=$((KN+1))
      done
    done
  done
  if [ "$KN" -eq "$WANT_KN" ]; then
    ck 0 "all $WANT_KN knight frames in the pck (16 walk/idle + $(echo $RUN_DIRS | wc -w | tr -d ' ') run cells x 12)"
  else ck 1 "knight frames in the pck: $KN/$WANT_KN"; fi

  # R-C9-34: every rig part. A rig that exports with one part missing toggles to a
  # knight missing a leg and says nothing, so count them rather than trusting the scene.
  #
  # The list is READ FROM THE SCENE, not written here. It was a hardcoded 14 until
  # R-C9-40 added a fifteenth part (body_backdrop, the piece that closes the gap
  # between the tabard flaps) -- and the check went on reporting "all 14 knight-rig
  # parts in the pck", green, while saying nothing at all about the one part the whole
  # fix depends on. A check that enumerates what it expects stops matching the thing it
  # checks the first time the thing grows.
  PARTS=$(grep -o 'sprites_rig_E/[a-z_]*\.png' "$DEST/scenes/knight_rig_E.tscn" \
          | sed 's|sprites_rig_E/||; s|\.png$||' | sort -u)
  WANT_RG=$(echo "$PARTS" | wc -w | tr -d ' ')
  RG=0
  MISSING_RG=""
  for p in $PARTS; do
    if grep -a -q "sprites_rig_E/$p.png" "$PCK"; then RG=$((RG+1));
    else MISSING_RG="$MISSING_RG $p"; fi
  done
  if [ "$RG" -eq "$WANT_RG" ]; then ck 0 "all $WANT_RG knight-rig parts in the pck"
  else ck 1 "knight-rig parts in the pck: $RG/$WANT_RG (missing:$MISSING_RG)"; fi
fi

xattr -dr com.apple.quarantine "$APP" 2>/dev/null || true
echo "   ok   quarantine attribute cleared (unsigned local build)"

if [ -z "${SKIP_LAUNCH_CHECK:-}" ] && [ -x "$BIN" ]; then
  if "$BIN" --headless --quit > "$LOG/launch.log" 2>&1; then ck 0 "headless launch probe exits 0"
  else echo "   FAIL headless launch probe; see $LOG/launch.log" >&2; tail -20 "$LOG/launch.log" >&2; FAIL=1; fi
fi

[ "$FAIL" -eq 0 ] || { echo "== BUILD RED" >&2; exit 6; }

echo "== stage -> $STAGE"
mkdir -p "$STAGE"
rm -rf "$STAGE/$NAME.app"
ditto "$APP" "$STAGE/$NAME.app"
xattr -dr com.apple.quarantine "$STAGE/$NAME.app" 2>/dev/null || true
echo "== BUILD GREEN  $(du -sh "$STAGE/$NAME.app" | cut -f1)  at $STAGE"
