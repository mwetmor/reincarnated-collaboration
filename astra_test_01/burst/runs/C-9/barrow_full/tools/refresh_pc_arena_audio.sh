#!/bin/bash
# Incremental audio refresh of an already built native mirror. No art/runtime rebuild.
# The full build retains its 20 GiB gate. This operation needs an existing audited
# mirror and ZIP, and 8 GiB for the ~2.5 GB export + temporary verified ZIP.
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/.." && pwd)
DEST=$ROOT/pc_arena
TOOLS=$ROOT/tools
GODOT=${GODOT:-/Applications/Godot.app/Contents/MacOS/Godot}
LOCK=$HOME/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-7/conductor_scripts/heavy_lock.py
"$GODOT" --version | grep -q '^4.6.3.stable' || exit 2
[ -f "$DEST/build/BarrowArena-Windows-x64.zip" ] || { echo 'Run the full native build first' >&2; exit 2; }
[ -f "$DEST/.godot/global_script_class_cache.cfg" ] || exit 2
[ -f "$DEST/kc2/bundle/BUNDLE_STAMP.json" ] || exit 2
FREE=$(df -g /System/Volumes/Data | awk 'NR==2{print $4}')
[ "$FREE" -ge 8 ] || { echo 'HALT: audio refresh needs 8 GiB free' >&2; exit 9; }
if [ "${C9_AUDIO_LOCKED:-}" != 1 ]; then
  exec env C9_AUDIO_LOCKED=1 python3 "$LOCK" C-9-PC-AUDIO -- bash "$0"
fi
for SCRIPT in arena_mode.gd arena_hud.gd arena_audio.gd; do
  cp "$ROOT/godot/scripts/arena/$SCRIPT" "$DEST/scripts/arena/$SCRIPT"
done
mkdir -p "$DEST/data/audio"
cp "$ROOT/godot/data/audio/arena_audio.json" "$DEST/data/audio/arena_audio.json"
python3 "$TOOLS/arena_stage_audio.py" --project "$DEST" > "$DEST/build/logs/audio_stage.log"
"$GODOT" --headless --path "$DEST" --import > "$DEST/build/logs/audio_import.log" 2>&1
"$GODOT" --headless --path "$DEST" --export-release WindowsArena \
  "$DEST/build/BarrowArena-Windows-x64/BarrowArena.exe" > "$DEST/build/logs/audio_export.log" 2>&1
python3 "$TOOLS/pck_web_extensions.py" "$DEST/build/BarrowArena-Windows-x64/BarrowArena.pck"
python3 "$TOOLS/pck_native_alias.py" "$DEST/build/BarrowArena-Windows-x64/BarrowArena.pck"
python3 "$TOOLS/arena_native_package.py" "$DEST"
ISOLATED=$(mktemp -d "${TMPDIR:-/tmp}/barrow-audio-packed.XXXXXX")
trap 'rmdir "$ISOLATED" 2>/dev/null || true' EXIT
rm -f "$DEST/build/logs/native/native_probe.json" "$DEST/build/logs/native/audio_probe.json"
"$GODOT" --headless --path "$ISOLATED" --main-pack "$DEST/build/BarrowArena-Windows-x64/BarrowArena.pck" \
  --script "$TOOLS/arena_native_probe.gd" -- --reference-probe --evidence-dir "$DEST/build/logs/native" \
  > "$DEST/build/logs/audio_native_scene.log" 2>&1
grep -q 'NATIVE_SCENE: PASS' "$DEST/build/logs/audio_native_scene.log" || exit 7
! grep -q 'SCRIPT ERROR:' "$DEST/build/logs/audio_native_scene.log" || exit 7
"$GODOT" --headless --audio-driver CoreAudio --path "$ISOLATED" \
  --main-pack "$DEST/build/BarrowArena-Windows-x64/BarrowArena.pck" \
  --script "$TOOLS/arena_audio_probe.gd" -- --audio-evidence "$DEST/build/logs/native/audio_probe.json" \
  > "$DEST/build/logs/audio_native_mix.log" 2>&1
grep -q 'ARENA_AUDIO: PASS' "$DEST/build/logs/audio_native_mix.log" || exit 7
! grep -q 'SCRIPT ERROR:' "$DEST/build/logs/audio_native_mix.log" || exit 7
python3 "$TOOLS/arena_native_zip.py" "$DEST"
