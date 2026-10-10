#!/bin/bash
# Full native arena Windows x64 export. Generated mirror only; sealed runtime copied verbatim.
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/.." && pwd)
DEST=$ROOT/pc_arena
TOOLS=$ROOT/tools
GODOT=${GODOT:-/Applications/Godot.app/Contents/MacOS/Godot}
HEAVY_LOCK=${HEAVY_LOCK:-$HOME/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-7/conductor_scripts/heavy_lock.py}
"$GODOT" --version | grep -q '^4.6.3.stable' || { echo "Godot 4.6.3 stable required" >&2; exit 2; }
FREE=$(df -g /System/Volumes/Data | awk 'NR==2{print $4}')
[ "$FREE" -ge 20 ] || { echo "HALT: under native build's 20 GiB free disk gate" >&2; exit 9; }
if [ "${C9_PC_LOCKED:-}" != 1 ]; then
  exec env C9_PC_LOCKED=1 python3 "$HEAVY_LOCK" C-9-PC -- bash "$0" "$@"
fi
mkdir -p "$DEST/build/logs"
python3 "$TOOLS/arena_native_alias_test.py" > "$DEST/build/logs/alias_test.log"
rsync -a --delete --filter 'P .godot/' --filter 'P build/' \
  --filter 'P kc2/kc2_runtime/' --filter 'P kc2/model_pack/' --filter 'P kc2/art/' --filter 'P kc2/bundle/' \
  --exclude '.godot/' --exclude 'build/' --exclude 'export_presets.cfg' --exclude 'tools/' --exclude 'captures/' \
  --exclude 'kc2/kc2_runtime' --exclude 'kc2/art_x/' --exclude 'kc2/vfx_x/' --exclude 'kc2/.gdignore' \
  "$ROOT/godot/" "$DEST/"
mkdir -p "$DEST/build/logs"
touch "$DEST/build/.gdignore"
python3 "$TOOLS/arena_bundle_native.py" "$DEST" > "$DEST/build/logs/bundle.log"
python3 - "$DEST" <<'PY'
import pathlib, re, sys
root = pathlib.Path(sys.argv[1])
p = root / 'project.godot'
t = p.read_text()
t = re.sub(r'^run/main_scene=".*"$', 'run/main_scene="res://scenes/bv2f_arena.tscn"', t, flags=re.M)
t = re.sub(r'^config/name=".*"$', 'config/name="Barrow Arena"', t, flags=re.M)
assert 'renderer/rendering_method="forward_plus"' in t
p.write_text(t)
(root / 'export_presets.cfg').write_text('''[preset.0]
name="WindowsArena"
platform="Windows Desktop"
runnable=true
advanced_options=true
dedicated_server=false
custom_features=""
export_filter="all_resources"
include_filter="*.json,*.bin,*.f32,kc2/kc2_runtime/*,kc2/art/*,kc2/vfx_x/*"
exclude_filter="tools/*,build/*,kc2/art_x/*,*.DS_Store"
export_path="build/BarrowArena-Windows-x64/BarrowArena.exe"
encrypt_pck=false
encrypt_directory=false
script_export_mode=0

[preset.0.options]
custom_template/debug=""
custom_template/release=""
debug/export_console_wrapper=1
binary_format/embed_pck=false
binary_format/architecture="x86_64"
codesign/enable=false
application/modify_resources=false
texture_format/s3tc_bptc=true
texture_format/etc2_astc=false
''')
PY
echo 'Importing full native assets...'
"$GODOT" --headless --path "$DEST" --import > "$DEST/build/logs/import.log" 2>&1
mkdir -p "$DEST/build/BarrowArena-Windows-x64"
echo 'Exporting Windows x64...'
"$GODOT" --headless --path "$DEST" --export-release WindowsArena \
  "$DEST/build/BarrowArena-Windows-x64/BarrowArena.exe" > "$DEST/build/logs/export.log" 2>&1
python3 "$TOOLS/pck_web_extensions.py" "$DEST/build/BarrowArena-Windows-x64/BarrowArena.pck"
python3 "$TOOLS/pck_native_alias.py" "$DEST/build/BarrowArena-Windows-x64/BarrowArena.pck"
for NOTICE in LICENSE.txt COPYRIGHT.txt; do
  curl --fail --silent --show-error --max-time 30 \
    "https://raw.githubusercontent.com/godotengine/godot/4.6.3-stable/$NOTICE" \
    -o "$DEST/build/BarrowArena-Windows-x64/GODOT_$NOTICE"
done
python3 "$TOOLS/arena_native_package.py" "$DEST"
ISOLATED=$(mktemp -d "${TMPDIR:-/tmp}/barrow-native-probe.XXXXXX")
trap 'rmdir "$ISOLATED" 2>/dev/null || true' EXIT
rm -f "$DEST/build/logs/native/native_probe.json"
"$GODOT" --headless --path "$ISOLATED" --main-pack "$DEST/build/BarrowArena-Windows-x64/BarrowArena.pck" \
  --script "$TOOLS/arena_native_probe.gd" -- --reference-probe --evidence-dir "$DEST/build/logs/native" \
  > "$DEST/build/logs/native_probe.log" 2>&1
grep -q 'NATIVE_SCENE: PASS' "$DEST/build/logs/native_probe.log" || { echo 'Native scene probe did not pass' >&2; exit 7; }
if grep -q 'SCRIPT ERROR:' "$DEST/build/logs/native_probe.log"; then
  echo 'Native scene probe emitted a script error' >&2; exit 7
fi
python3 "$TOOLS/arena_native_zip.py" "$DEST"
echo "Export ready: $DEST/build/BarrowArena-Windows-x64"
