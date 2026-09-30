#!/bin/bash
# C-9 VFX BAKE-OFF, LANE B -- the Meteor test scene as a WEB EXPORT (Compatibility / WebGL2), for the
# phone-size measurement in Chrome. LOCAL ONLY: nothing is staged into the loadout site and nothing is
# pushed. The shape is barrow_full/tools/build_web_painted.sh's, which built /playtest/barrow-painted/:
#   1. mirror godot/ into web/src (its own .godot import cache; the desktop's painted data stays behind);
#   2. adapt the mirror's imports for phones, exactly as that script does (world models' own textures
#      discarded -- they wear bakes; his and her gear textures VRAM-compressed with mipmaps, cut to 512);
#   3. a Web preset: single-threaded, mobile texture formats, only the scene's dependencies and the
#      PHONE painted data (data/painted_web);
#   4. export, then a launch fence: the exported pck run by the desktop Godot under Compatibility with
#      the web branches on, until the scene prints its ready line.
#   usage: tools/build_web.sh
set -euo pipefail
HERE=$(cd "$(dirname "$0")" && pwd)
SRC=$HERE/../godot
DEST=$HERE/../web/src
OUTW=$HERE/../web/build
LOG=$HERE/../web/logs
GODOT=${GODOT:-/Applications/Godot.app/Contents/MacOS/Godot}
HEAVY_LOCK=${HEAVY_LOCK:-$HOME/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-7/conductor_scripts/heavy_lock.py}
GATE=${DISK_GATE_GIB:-20}
FREE=$(df -g /System/Volumes/Data | awk 'NR==2{print $4}')
[ "$FREE" -ge "$GATE" ] || { echo "HALT: under $GATE GiB free" >&2; exit 9; }
mkdir -p "$DEST" "$OUTW" "$LOG"
rsync -a --delete --exclude '.godot/' --exclude 'data/painted/' "$SRC"/ "$DEST"/
python3 - "$DEST" <<'PY'
import pathlib, re, sys
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
root = pathlib.Path(sys.argv[1])
def setk(text, key, val):
    if re.search(rf"^{re.escape(key)}=.*$", text, re.M):
        return re.sub(rf"^{re.escape(key)}=.*$", f"{key}={val}", text, flags=re.M)
    return text.replace("[params]", f"[params]\n\n{key}={val}", 1)
nd = ng = ncut = 0
for imp in sorted(list((root / "models" / "barrow").glob("*.glb.import")) + list((root / "models" / "barrow" / "kit").glob("*.glb.import"))):
    t = imp.read_text(); imp.write_text(setk(t, "gltf/embedded_image_handling", "0")); nd += 1
for imp in sorted(list((root / "models" / "gear").glob("*.import")) + list((root / "models" / "sorceress").glob("*.import"))):
    src = imp.with_suffix("")
    if src.suffix.lower() not in (".png", ".jpg", ".jpeg"):
        continue
    t = imp.read_text()
    t = setk(t, "compress/mode", "2"); t = setk(t, "mipmaps/generate", "true")
    if max(Image.open(src).size) > 512:
        t = setk(t, "process/size_limit", "512"); ncut += 1
    imp.write_text(t); ng += 1
print(f"world models' textures discarded: {nd}; gear textures VRAM+mips: {ng} (cut to 512: {ncut})")
PY
python3 "$HEAVY_LOCK" C-9 -- python3 "$HERE/tmo.py" 1200 -- "$GODOT" --headless --path "$DEST" --import > "$LOG/import.log" 2>&1 || true
python3 "$HEAVY_LOCK" C-9 -- python3 "$HERE/tmo.py" 300 -- "$GODOT" --headless --path "$DEST" --import > "$LOG/import2.log" 2>&1 || true
FILES=$(cd "$DEST" && {
  echo "scenes/meteor_test.tscn"
  ls scripts/*.gd
  for m in birch lintel post raven stone_mid stone_short stone_tall; do echo "models/barrow/$m.glb"; done
  for k in cairn log shield; do echo "models/barrow/kit/$k.glb"; done
  ls models/gear/*.glb
  ls models/sorceress/*.glb
} | sed 's|^|"res://|; s|$|"|' | paste -sd, -)
cat > "$DEST/export_presets.cfg" <<EOF
[preset.0]

name="Web"
platform="Web"
runnable=true
advanced_options=false
dedicated_server=false
custom_features=""
export_filter="resources"
export_files=PackedStringArray($FILES)
include_filter="data/barrow_full_layout.json,data/character.json,data/gear_manifest.json,data/character_sorceress.json,data/gear_manifest_sorceress.json,data/sockets_sorceress.json,data/barrow_full_splat.bin,data/painted_web/*.json,data/painted_web/*.bin,data/painted_web/bakes/*.bin"
exclude_filter=""
export_path="$OUTW/index.html"
patches=PackedStringArray()
encryption_include_filters=""
encryption_exclude_filters=""
seed=0
encrypt_pck=false
encrypt_directory=false
script_export_mode=2

[preset.0.options]

custom_template/debug=""
custom_template/release=""
variant/extensions_support=false
variant/thread_support=false
vram_texture_compression/for_desktop=false
vram_texture_compression/for_mobile=true
html/export_icon=true
html/custom_html_shell=""
html/head_include=""
html/canvas_resize_policy=2
html/focus_canvas_on_start=true
html/experimental_virtual_keyboard=false
progressive_web_app/enabled=false
progressive_web_app/ensure_cross_origin_isolation_headers=false
progressive_web_app/offline_page=""
progressive_web_app/display=1
progressive_web_app/orientation=1
progressive_web_app/icon_144x144=""
progressive_web_app/icon_180x180=""
progressive_web_app/icon_512x512=""
progressive_web_app/background_color=Color(0, 0, 0, 1)
threads/emscripten_pool_size=8
threads/godot_pool_size=4
EOF
python3 "$HEAVY_LOCK" C-9 -- python3 "$HERE/tmo.py" 900 -- "$GODOT" --headless --path "$DEST" --export-release "Web" "$OUTW/index.html" > "$LOG/export.log" 2>&1 || {
  echo "export failed" >&2; tail -30 "$LOG/export.log" >&2; exit 5; }
grep -q "GODOT_THREADS_ENABLED = false" "$OUTW/index.html" && echo "   ok   threads OFF" || echo "   FAIL threads"
ls -l "$OUTW" | awk 'NR>1 {printf "   %12d  %s\n", $5, $9}'
# THE LAUNCH FENCE: the exported pck under the web's renderer, the web branches on
python3 "$HEAVY_LOCK" C-9 -- python3 "$HERE/tmo.py" 240 -- "$GODOT" --main-pack "$OUTW/index.pck" --rendering-method gl_compatibility \
  --rendering-driver opengl3_angle --resolution 640x360 --quit-after 900 -- --as-web > "$LOG/launch.log" 2>&1 || true
grep -a -E "^\[barrow_painted\] web:|^\[meteor_b\]" "$LOG/launch.log" | cut -c1-400
if grep -a -q -E "SCRIPT ERROR|SHADER ERROR|Parse Error" "$LOG/launch.log"; then
  echo "   FAIL launch log has script/shader errors" >&2; grep -a -E -A3 "SCRIPT ERROR|SHADER ERROR|Parse Error" "$LOG/launch.log" | head -30 >&2
else
  echo "   ok   launch log free of script and shader errors"
fi
echo "== done"
