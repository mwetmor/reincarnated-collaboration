#!/bin/bash
# C-9 R-C9-83 -- THE BARROW AS A PHONE WEB BUILD, for /playtest/barrow/ on the loadout site.
#
# ONE PROJECT (the coordinator's call): cliffside3d/godot, whose web differences live in the
# project itself -- project.godot's rendering_method.web = gl_compatibility, and the scene's
# own PaintStack.is_web() / is_compatibility() branches (heather as depthless cards drawn after
# the post pass, the depth-only pen at 6 px, the ambient moved into the sun's pass, the web
# shadow bias, half-float snow textures, the full kit and the thumb controls). This script only
# BUILDS it:
#
#   1. mirrors godot/ into web_barrow/ (outside the source, like app_barrow/; its .godot import
#      cache is kept between builds, so a rebuild imports only what changed);
#   2. adapts the MIRROR's import settings for phones -- every 3D texture VRAM-compressed with
#      mipmaps, the 4K gear textures and the 2K body cut to 1024, the five ground tiles lossy;
#   3. writes a Web preset that exports ONLY the Barrow's dependencies (listed below; the macOS
#      app ships every resource in the project, 320 MB), single-threaded (no COOP/COEP on our
#      Vercel), phone texture formats, <base href="/playtest/barrow/">, the rotate hint;
#   4. exports, then FENCES the result: threads off, the base href, the Barrow scene and its
#      web pieces inside the pck, NO FILE AT OR OVER 50 MB (GitHub refuses 100) -- and a LAUNCH
#      of the exported pck itself (Compatibility on ANGLE, the web branches on), whose own
#      "[barrow] web:" line must say the splat loaded and the dressing is all there. The file
#      table cannot say that: an imported PNG ships as its .import remap, so a grep for its
#      name matches whether or not the scene can read it (the splat shipped missing that way);
#   5. stages build/web/ into reincarnated-loadout/public/playtest/barrow/ (never commits).
#
#   usage: tools/build_web_barrow.sh [--no-stage]
set -euo pipefail

SRC=$(cd "$(dirname "$0")/.." && pwd)/godot
TOOLS=$(cd "$(dirname "$0")" && pwd)
DEST=$(dirname "$SRC")/web_barrow
LOG=$DEST/build/logs
LOADOUT=${LOADOUT:-$HOME/Games/reincarnated-loadout}
STAGE=$LOADOUT/public/playtest/barrow
GODOT=${GODOT:-/Applications/Godot.app/Contents/MacOS/Godot}
HEAVY_LOCK=${HEAVY_LOCK:-$HOME/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-7/conductor_scripts/heavy_lock.py}
MAX_FILE_MB=50
NO_STAGE=0
[ "${1:-}" = "--no-stage" ] && NO_STAGE=1

[ -f "$SRC/project.godot" ] || { echo "no project.godot in $SRC" >&2; exit 2; }
grep -q '^renderer/rendering_method.web="gl_compatibility"' "$SRC/project.godot" \
  || { echo "project.godot lacks rendering_method.web=gl_compatibility" >&2; exit 2; }
FREE=$(df -g /Users/admin | awk 'NR==2{print $4}')
[ "$FREE" -ge 25 ] || { echo "HALT: under 25 GiB free (R-C9-87)" >&2; exit 9; }

if [ -z "${C9_LOCKED:-}" ]; then
  echo "== acquiring heavy lock"
  exec env C9_LOCKED=1 python3 "$HEAVY_LOCK" C-9 -- bash "$0" "$@"
fi

echo "== mirror $SRC -> $DEST"
mkdir -p "$DEST" "$LOG"
rsync -a --delete --exclude '.godot/' --exclude 'build/' --exclude 'export_presets.cfg' \
  --exclude 'tools/' --exclude 'layers/' --exclude 'plate/' --exclude 'props/' \
  "$SRC"/ "$DEST"/
touch "$DEST/build/.gdignore"

echo "== the mirror opens on the Barrow (the source project's main scene is the cliffside)"
python3 - "$DEST" <<'MAINSCENE'
import pathlib, re, sys
pg = pathlib.Path(sys.argv[1]) / "project.godot"
t = pg.read_text()
t = re.sub(r'^run/main_scene=".*"$', 'run/main_scene="res://scenes/barrow.tscn"', t, flags=re.M)
t = re.sub(r'^config/name=".*"$', 'config/name="C-9 Barrow"', t, flags=re.M)
pg.write_text(t)
got = dict(re.findall(r'^(run/main_scene|config/name)="(.*)"$', t, flags=re.M))
assert got.get("run/main_scene") == "res://scenes/barrow.tscn", got
print("main scene:", got)
MAINSCENE

echo "== adapt the mirror's imports for phones"
python3 - "$DEST" <<'PY'
import pathlib, re, sys
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
root = pathlib.Path(sys.argv[1])
def setk(text, key, val):
    if re.search(rf"^{re.escape(key)}=.*$", text, re.M):
        return re.sub(rf"^{re.escape(key)}=.*$", f"{key}={val}", text, flags=re.M)
    return text.replace("[params]", f"[params]\n\n{key}={val}", 1)
n3d = ncut = ntile = 0
# every texture the 3D models carry: VRAM-compressed with mipmaps (the importer's detect-3D
# step never runs headless, so on its own these stay lossless PNG blobs in the pck), and SIZED
# BY WHAT THEY COVER ON A PHONE: 1024 for the pieces that stand large in frame (the outcrop,
# the stones, the barrow's lintel and posts), 512 for the rest -- a rock, a juniper, the raven,
# his gear and his body are 40-150 px tall on a 390 px-high screen. The gear's 4K and the
# body's 2K come down with them. (1024 across the board was 48.0 MB of pck: 30 textures at
# 0.70 MB each; 512 is 0.18.)
BIG = ("outcrop_a_", "stone_tall_", "stone_mid_", "stone_short_", "lintel_", "post_")
for imp in sorted((root / "models").rglob("*.import")):
    src = imp.with_suffix("")
    if src.suffix.lower() not in (".png", ".jpg", ".jpeg"):
        continue
    t = imp.read_text()
    t = setk(t, "compress/mode", "2")
    t = setk(t, "mipmaps/generate", "true")
    limit = 1024 if src.name.startswith(BIG) else 512
    if max(Image.open(src).size) > limit:
        t = setk(t, "process/size_limit", str(limit))
        ncut += 1
    imp.write_text(t)
    n3d += 1
# the ground tiles: lossy WebP -- the scene decodes them and builds its own mipmaps at load,
# so what the pck carries is only a download, and a painted tile loses nothing at q0.85
for name in ("bark", "heather", "ice", "path", "rock", "snow"):
    imp = root / "textures" / "barrow" / f"{name}.png.import"
    if imp.exists():
        t = imp.read_text()
        t = setk(t, "compress/mode", "1")
        t = setk(t, "compress/lossy_quality", "0.85")
        imp.write_text(t)
        ntile += 1
print(f"3D textures VRAM+mips: {n3d} (cut down: {ncut}); ground tiles lossy: {ntile}")
PY

echo "== import"
"$GODOT" --headless --path "$DEST" --import > "$LOG/import.log" 2>&1 || {
  echo "import failed" >&2; tail -20 "$LOG/import.log" >&2; exit 4; }

echo "== preset: Web / nothreads / Barrow dependencies only"
FILES=$(cd "$DEST" && {
  echo "scenes/barrow.tscn"
  ls scripts/*.gd
  for m in birch juniper lintel post raven rock_large rock_small stone_mid stone_short stone_tall; do
    echo "models/barrow/$m.glb"; done
  for k in boulder cairn dead_tree heather_clump log outcrop_a rocks shield skull stump; do
    echo "models/barrow/kit/$k.glb"; done
  ls models/gear/*.glb
  ls textures/barrow/*.png
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
include_filter="data/barrow_*.json,data/kit_assets.json,data/heather_cards.json,data/character.json,data/gear_manifest.json,data/height_a_*.json,data/height_a_*.png,data/splat_ids_*.png"
exclude_filter="tools/*"
export_path="build/web/index.html"
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
html/head_include="<base href=\"/playtest/barrow/\"><style>#rotate-hint{display:none;position:fixed;inset:0;z-index:10;background:#0b0f16;color:#e8eef7;font:600 20px/1.4 system-ui,sans-serif;align-items:center;justify-content:center;text-align:center;padding:24px}@media (orientation:portrait) and (pointer:coarse){#rotate-hint{display:flex}}#back-chip{position:fixed;top:calc(env(safe-area-inset-top,0px) + 8px);left:calc(env(safe-area-inset-left,0px) + 8px);z-index:20;font:600 13px/1 system-ui,-apple-system,sans-serif}#back-chip a{display:block;padding:9px 13px;border-radius:999px;background:rgba(11,15,22,.78);color:#e8eef7;border:1px solid rgba(143,200,255,.45);text-decoration:none}</style><script>addEventListener('DOMContentLoaded',function(){var d=document.createElement('div');d.id='rotate-hint';d.textContent='Rotate your phone to landscape to play';document.body.appendChild(d);var n=document.createElement('div');n.id='back-chip';n.innerHTML='<a href=\"/playtest/\">← Playtests</a>';document.body.appendChild(n);n.addEventListener('pointerdown',function(e){e.stopPropagation();},true);});</script>"
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

echo "== export Web"
mkdir -p "$DEST/build/web"          # the export overwrites every file it writes
"$GODOT" --headless --path "$DEST" --export-release "Web" build/web/index.html > "$LOG/export.log" 2>&1 || {
  echo "export failed" >&2; tail -30 "$LOG/export.log" >&2; exit 5; }

echo "== verify"
FAIL=0
ck() { if [ "$1" = 0 ]; then echo "   ok   $2"; else echo "   FAIL $2" >&2; FAIL=1; fi; }
W="$DEST/build/web"
grep -q "GODOT_THREADS_ENABLED = false" "$W/index.html" && ck 0 "threads OFF (no COOP/COEP needed)" || ck 1 "threads OFF"
grep -q '<base href="/playtest/barrow/">' "$W/index.html" && ck 0 "base href /playtest/barrow/" || ck 1 "base href"
for f in "$W"/*; do
  sz=$(stat -f %z "$f")
  if [ "$sz" -ge $((MAX_FILE_MB * 1000 * 1000)) ]; then ck 1 "$(basename "$f") is $((sz / 1000000)) MB -- at or over $MAX_FILE_MB MB"; fi
done
[ "$FAIL" -eq 0 ] && ck 0 "every file under $MAX_FILE_MB MB"
MISSING=0
# raw files only (scripts, JSON, GLB): an IMPORTED path's name is in the pck as its .import remap
# whether or not the scene can read it, so those are proven by the launch below instead
for p in scenes/barrow.tscn scripts/barrow_world.gd scripts/barrow_touch.gd scripts/barrow_heather.gd \
         data/heather_cards.json models/barrow/kit/outcrop_a.glb \
         models/gear/nb-body.glb data/barrow_dress_a.json; do
  grep -a -q "$p" "$W/index.pck" || { echo "   missing from pck: $p" >&2; MISSING=1; }
done
[ "$MISSING" -eq 0 ] && ck 0 "the Barrow and its web pieces are in the pck" || ck 1 "the Barrow and its web pieces are in the pck"
if grep -a -o -i -E "vfx_(frost|fire|lightning|arcane|holy|poison)_(bolt|impact)[^A-Za-z0-9_]|creativekind|gigapack|untied ?games" "$W/index.pck" | head -1 | grep -q .; then
  ck 1 "license fence: a library kit name inside the pck"
else
  ck 0 "license fence clean"
fi
# THE LAUNCH FENCE: the exported pck, run by the desktop Godot under the web's renderer with the
# web branches on (--as-web), until the scene has printed its "[barrow] web:" line. Windowed,
# not headless: the dummy renderer hands back no image from a texture, and the splat and the
# tiles are read that way. MIN_INSTANCES: the source project instances 650 at this commit;
# the first phone build shipped 137 (no splat, no heather) and nothing failed.
MIN_INSTANCES=${MIN_INSTANCES:-600}
"$GODOT" --main-pack "$W/index.pck" --rendering-method gl_compatibility --rendering-driver opengl3_angle \
  --resolution 640x360 --quit-after 1200 -- --as-web > "$LOG/launch.log" 2>&1 || true
WEBLINE=$(grep -a '^\[barrow\] web:' "$LOG/launch.log" | head -1 || true)
echo "   launch: ${WEBLINE:-<no [barrow] web: line>}"
INST=$(echo "$WEBLINE" | sed -n 's/.*instances=\([0-9]*\).*/\1/p')
echo "$WEBLINE" | grep -q "splat=ok" && ck 0 "the launched pck read the splat" || ck 1 "the launched pck read the splat"
[ -n "$INST" ] && [ "$INST" -ge "$MIN_INSTANCES" ] && ck 0 "dressing instanced: $INST (>= $MIN_INSTANCES)" \
  || ck 1 "dressing instanced: ${INST:-?} (< $MIN_INSTANCES)"
grep -a -q '^\[barrow\] foot_lock nodes=0' "$LOG/launch.log" && ck 0 "no foot-lock node" || ck 1 "no foot-lock node"
if grep -a -q -E "SCRIPT ERROR|SHADER ERROR|Parse Error" "$LOG/launch.log"; then
  ck 1 "launch log free of script and shader errors"; grep -a -E -A2 "SCRIPT ERROR|SHADER ERROR|Parse Error" "$LOG/launch.log" | head -12 >&2
else
  ck 0 "launch log free of script and shader errors"
fi
echo "   sizes:"; ls -l "$W" | awk 'NR>1 {printf "   %12d  %s\n", $5, $9}'
[ "$FAIL" -eq 0 ] || { echo "== VERIFY FAILED" >&2; exit 6; }

if [ "$NO_STAGE" -eq 0 ]; then
  echo "== stage -> $STAGE"
  mkdir -p "$STAGE"
  rsync -a --delete --exclude '.gdignore' "$W/" "$STAGE/"
fi
echo "== done"
