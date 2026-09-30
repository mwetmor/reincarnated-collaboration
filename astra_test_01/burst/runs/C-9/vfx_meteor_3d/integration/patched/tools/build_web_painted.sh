#!/bin/bash
# C-9 T10-2 -- THE PAINTED BARROW AS A PHONE PAGE, for /playtest/barrow-painted/ on the loadout
# site. ADDITIVE: /playtest/barrow/ (cliffside3d's phone build) is not touched. drax.
#
# The shape is cliffside3d/tools/build_web_barrow.sh's, which built /playtest/barrow/:
#   1. mirror barrow_full/godot into web_painted/ (outside the source; its .godot import cache is
#      kept between builds);
#   2. adapt the MIRROR's imports for phones -- the ten world models DISCARD their textures (every
#      one of their surfaces wears the painting or a bake: a texture of theirs would be download
#      for nothing), his gear's textures VRAM-compressed with mipmaps and cut to 512;
#   3. a Web preset exporting only the painted Barrow's dependencies, single-threaded (no COOP/COEP
#      on our Vercel), phone texture formats, <base href="/playtest/barrow-painted/">, the rotate
#      hint and the back chip -- and the PHONE's painted data (data/painted_web/: the painting
#      within 4096 px as WebP, the bakes at 512), never the desktop's 33 MB PNG;
#   4. export, then FENCE it: threads off, the base href, no file at or over 50 MB (GitHub refuses
#      100), the raw files in the pck -- and a LAUNCH of the exported pck itself (Compatibility on
#      ANGLE, the web branches on), whose "[barrow_painted] web:" line must say every painted file
#      was read and its sha256 matched, the painting loaded at its phone size, all 54 plates in
#      place, 977 heather sprays and the snow built. The file table cannot say that: only the
#      running scene reads the files (the splat shipped missing that way once);
#   5. stage build/web/ into reincarnated-loadout/public/playtest/barrow-painted/ (never commits).
#
#   usage: tools/build_web_painted.sh [--no-stage]
set -euo pipefail

SRC=$(cd "$(dirname "$0")/.." && pwd)/godot
DEST=$(dirname "$SRC")/web_painted
LOG=$DEST/build/logs
LOADOUT=${LOADOUT:-$HOME/Games/reincarnated-loadout}
STAGE=$LOADOUT/public/playtest/barrow-painted
GODOT=${GODOT:-/Applications/Godot.app/Contents/MacOS/Godot}
HEAVY_LOCK=${HEAVY_LOCK:-$HOME/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-7/conductor_scripts/heavy_lock.py}
MAX_FILE_MB=50
GATE=${DISK_GATE_GIB:-20}
NO_STAGE=0
[ "${1:-}" = "--no-stage" ] && NO_STAGE=1

[ -f "$SRC/project.godot" ] || { echo "no project.godot in $SRC" >&2; exit 2; }
grep -q '^renderer/rendering_method.web="gl_compatibility"' "$SRC/project.godot" \
  || { echo "project.godot lacks rendering_method.web=gl_compatibility" >&2; exit 2; }
[ -f "$SRC/data/painted_web/manifest.json" ] || { echo "no phone data: run tools/paint_world_prep.py --web" >&2; exit 2; }
FREE=$(df -g /System/Volumes/Data | awk 'NR==2{print $4}')
[ "$FREE" -ge "$GATE" ] || { echo "HALT: under $GATE GiB free" >&2; exit 9; }

if [ -z "${C9_LOCKED:-}" ]; then
  echo "== acquiring heavy lock"
  exec env C9_LOCKED=1 python3 "$HEAVY_LOCK" C-9 -- bash "$0" "$@"
fi

echo "== mirror $SRC -> $DEST (the desktop's painted data stays behind)"
mkdir -p "$DEST" "$LOG"
rsync -a --delete --exclude '.godot/' --exclude 'build/' --exclude 'export_presets.cfg' \
  --exclude 'tools/' --exclude 'data/painted/' "$SRC"/ "$DEST"/
touch "$DEST/build/.gdignore"

echo "== the mirror opens on the painted Barrow"
python3 - "$DEST" <<'MAINSCENE'
import pathlib, re, sys
pg = pathlib.Path(sys.argv[1]) / "project.godot"
t = pg.read_text()
t = re.sub(r'^run/main_scene=".*"$', 'run/main_scene="res://scenes/barrow_painted.tscn"', t, flags=re.M)
t = re.sub(r'^config/name=".*"$', 'config/name="C-9 Barrow painted"', t, flags=re.M)
pg.write_text(t)
got = dict(re.findall(r'^(run/main_scene|config/name)="(.*)"$', t, flags=re.M))
assert got.get("run/main_scene") == "res://scenes/barrow_painted.tscn", got
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
nd = ng = ncut = 0
# THE WORLD MODELS WEAR THE PAINTING: their own textures are never drawn, so they are not imported
for imp in sorted(list((root / "models" / "barrow").glob("*.glb.import")) + list((root / "models" / "barrow" / "kit").glob("*.glb.import"))):
    t = imp.read_text()
    t = setk(t, "gltf/embedded_image_handling", "0")
    imp.write_text(t)
    nd += 1
# HIS GEAR AND HERS: VRAM-compressed with mipmaps (the importer's detect-3D step never runs
# headless), cut to 512 -- he stands ~190 px tall on the phone's 3D frame, she ~170 (the installed
# phone build's sizing)
for imp in sorted(list((root / "models" / "gear").glob("*.import")) + list((root / "models" / "sorceress").glob("*.import"))):
    src = imp.with_suffix("")
    if src.suffix.lower() not in (".png", ".jpg", ".jpeg"):
        continue
    t = imp.read_text()
    t = setk(t, "compress/mode", "2")
    t = setk(t, "mipmaps/generate", "true")
    if max(Image.open(src).size) > 512:
        t = setk(t, "process/size_limit", "512")
        ncut += 1
    imp.write_text(t)
    ng += 1
print(f"world models' textures discarded: {nd}; his and her gear textures VRAM+mips: {ng} (cut to 512: {ncut})")
PY

echo "== import"
"$GODOT" --headless --path "$DEST" --import > "$LOG/import.log" 2>&1 || {
  echo "import failed" >&2; tail -20 "$LOG/import.log" >&2; exit 4; }

echo "== preset: Web / nothreads / the painted Barrow's dependencies only"
FILES=$(cd "$DEST" && {
  echo "scenes/barrow_painted.tscn"
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
include_filter="data/barrow_full_layout.json,data/character.json,data/gear_manifest.json,data/character_sorceress.json,data/gear_manifest_sorceress.json,data/sockets_sorceress.json,data/barrow_full_splat.bin,data/painted_web/*.json,data/painted_web/*.bin,data/painted_web/bakes/*.bin,data/meteor/*.bin,data/meteor/*.json"
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
html/head_include="<base href=\"/playtest/barrow-painted/\"><style>#rotate-hint{display:none;position:fixed;inset:0;z-index:10;background:#0b0f16;color:#e8eef7;font:600 20px/1.4 system-ui,sans-serif;align-items:center;justify-content:center;text-align:center;padding:24px}@media (orientation:portrait) and (pointer:coarse){#rotate-hint{display:flex}}#back-chip{position:fixed;top:calc(env(safe-area-inset-top,0px) + 8px);left:calc(env(safe-area-inset-left,0px) + 8px);z-index:20;font:600 13px/1 system-ui,-apple-system,sans-serif}#back-chip a{display:block;padding:9px 13px;border-radius:999px;background:rgba(11,15,22,.78);color:#e8eef7;border:1px solid rgba(143,200,255,.45);text-decoration:none}</style><script>addEventListener('DOMContentLoaded',function(){var d=document.createElement('div');d.id='rotate-hint';d.textContent='Rotate your phone to landscape to play';document.body.appendChild(d);var n=document.createElement('div');n.id='back-chip';n.innerHTML='<a href=\"/playtest/\">← Playtests</a>';document.body.appendChild(n);n.addEventListener('pointerdown',function(e){e.stopPropagation();},true);});</script>"
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
mkdir -p "$DEST/build/web"
"$GODOT" --headless --path "$DEST" --export-release "Web" build/web/index.html > "$LOG/export.log" 2>&1 || {
  echo "export failed" >&2; tail -30 "$LOG/export.log" >&2; exit 5; }

echo "== verify"
FAIL=0
ck() { if [ "$1" = 0 ]; then echo "   ok   $2"; else echo "   FAIL $2" >&2; FAIL=1; fi; }
W="$DEST/build/web"
grep -q "GODOT_THREADS_ENABLED = false" "$W/index.html" && ck 0 "threads OFF (no COOP/COEP needed)" || ck 1 "threads OFF"
grep -q '<base href="/playtest/barrow-painted/">' "$W/index.html" && ck 0 "base href /playtest/barrow-painted/" || ck 1 "base href"
BIG=0
for f in "$W"/*; do
  sz=$(stat -f %z "$f")
  if [ "$sz" -ge $((MAX_FILE_MB * 1000 * 1000)) ]; then ck 1 "$(basename "$f") is $((sz / 1000000)) MB -- at or over $MAX_FILE_MB MB"; BIG=1; fi
done
[ "$BIG" -eq 0 ] && ck 0 "every file under $MAX_FILE_MB MB"
MISSING=0
BAKES=$(python3 -c "import json;print(' '.join('data/painted_web/'+b['file'] for b in json.load(open('$DEST/data/painted_web/manifest.json'))['bakes'].values()))")
for p in scenes/barrow_painted.tscn scripts/barrow_full.gd scripts/painted_world.gd scripts/paint_stack.gd \
         scripts/snow_field.gd scripts/barrow_heather.gd scripts/barrow_touch.gd scripts/knight.gd \
         scripts/foot_lock.gd data/barrow_full_layout.json data/barrow_full_splat.bin \
         data/painted_web/manifest.json data/painted_web/heather.json data/painted_web/painting.bin \
         data/painted_web/lit.bin data/painted_web/snow_grid.bin $BAKES models/gear/nb-body.glb \
         scripts/sorceress_knight.gd scripts/spell_fx.gd data/character_sorceress.json \
         data/gear_manifest_sorceress.json data/sockets_sorceress.json models/sorceress/so-body.glb \
         models/sorceress/robe.glb models/sorceress/mantle.glb models/sorceress/belt.glb \
         models/sorceress/bracers.glb models/sorceress/circlet.glb models/sorceress/staff.glb; do
  grep -a -q "$p" "$W/index.pck" || { echo "   missing from pck: $p" >&2; MISSING=1; }
done
[ "$MISSING" -eq 0 ] && ck 0 "the painted Barrow, its phone data (the painting, 25 bakes, the light map, the snow grid), him and her in the pck" \
                     || ck 1 "the painted Barrow's files in the pck"
if grep -a -q "data/painted/painting.bin" "$W/index.pck"; then ck 1 "the desktop's 33 MB painting is in the pck"; else ck 0 "the desktop's painting is NOT in the pck"; fi
if grep -a -o -i -E "vfx_(frost|fire|lightning|arcane|holy|poison)_(bolt|impact)[^A-Za-z0-9_]|creativekind|gigapack|untied ?games" "$W/index.pck" | head -1 | grep -q .; then
  ck 1 "license fence: a library kit name inside the pck"
else
  ck 0 "license fence clean"
fi
# THE LAUNCH FENCE: the exported pck, run by the desktop Godot under the web's renderer with the
# web branches on, until the scene prints its web line. Windowed: the dummy renderer builds no image.
"$GODOT" --main-pack "$W/index.pck" --rendering-method gl_compatibility --rendering-driver opengl3_angle \
  --resolution 640x360 --quit-after 1500 -- --as-web > "$LOG/launch.log" 2>&1 || true
WEBLINE=$(grep -a '^\[barrow_painted\] web:' "$LOG/launch.log" | head -1 || true)
echo "   launch: ${WEBLINE:-<no [barrow_painted] web: line>}"
echo "$WEBLINE" | grep -q "files_sha_ok=28/28 painting_ok=true ground=painting.bin(as_painted)_ok=true lit_ok=true snow_grid_ok=true" \
  && ck 0 "every painted file read from the pck, sha256 matched: 28/28 (the painting, the light map, the snow grid, 25 bakes)" \
  || ck 1 "a painted file did not load or did not match its sha256"
echo "$WEBLINE" | grep -q "painting_px=\[4096, 2536\]" && ck 0 "the painting loaded at its phone size, 4096 x 2536" || ck 1 "the painting's size"
echo "$WEBLINE" | grep -q "plates: bakes=25/25 on the real models, painting on primitives=29/29" \
  && ck 0 "all 54 plates in place: 25/25 bakes, 29/29 primitives wearing the painting" || ck 1 "not every plate is in place"
echo "$WEBLINE" | grep -q "birches=33 inks_hidden=25 heather=977 snow=true" \
  && ck 0 "instances: 33 birches, 977 heather sprays, the snow field" || ck 1 "the instance counts"
echo "$WEBLINE" | grep -q "pen=depth-only+stencil" && ck 0 "the web pen, with the painting's no-pen stencil class" || ck 1 "the web pen"
grep -a -q '^\[barrow_full\] built placements=87 splat_ok=true' "$LOG/launch.log" && ck 0 "the blockout under it built: 87 placements, the splat read" || ck 1 "the blockout build line"
if grep -a -q -E "SCRIPT ERROR|SHADER ERROR|Parse Error" "$LOG/launch.log"; then
  ck 1 "launch log free of script and shader errors"; grep -a -E -A2 "SCRIPT ERROR|SHADER ERROR|Parse Error" "$LOG/launch.log" | head -12 >&2
else
  ck 0 "launch log free of script and shader errors"
fi
# HER (?c=sorceress on the page; the same scene with -- --c sorceress here): her slot read, her
# gear bound, her tree VALID (sorceress_knight.gd fills the two clipless nodes that otherwise freeze
# her), the placeholder spells armed at both casts' release times
"$GODOT" --main-pack "$W/index.pck" --rendering-method gl_compatibility --rendering-driver opengl3_angle \
  --resolution 640x360 --quit-after 1500 -- --as-web --c sorceress > "$LOG/launch_sorceress.log" 2>&1 || true
SLINE=$(grep -a '^\[barrow_painted\] web:' "$LOG/launch_sorceress.log" | head -1 || true)
echo "   launch (sorceress): $(echo "$SLINE" | cut -c1-160)"
echo "$SLINE" | grep -q "who=sorceress" && echo "$SLINE" | grep -q "files_sha_ok=28/28" \
  && ck 0 "?c=sorceress: she walks the same painted Barrow, every painted file read and matched" || ck 1 "?c=sorceress did not build"
echo "$SLINE" | grep -q "sorceress_tree=valid" && ck 0 "her animation tree valid (clipless nodes filled: $(echo "$SLINE" | sed -n 's/.*clipless=\([^ ]*\).*/\1/p'))" || ck 1 "her animation tree"
# the releases the fence expects are HER PACKAGE'S (casts.<clip>.release_s in the installed
# character_sorceress.json), never a number written here: v2 moved them (0.9167 -> 0.9333, 1.625 -> 1.6333)
WANT_SPELLS=$(python3 - "$SRC/data/character_sorceress.json" <<'SPELLS'
import json, sys
casts = json.load(open(sys.argv[1]))["casts"]
# as spell_fx.gd reads them: every clip key not starting with "_", by its slot
by_slot = {c["slot"]: dict(c, clip=k) for k, c in casts.items() if not k.startswith("_") and isinstance(c, dict)}
print("spells=placeholder:" + ",".join("%s@%s" % (by_slot[s]["clip"], by_slot[s]["release_s"]) for s in ("attack", "chop")))
SPELLS
)
echo "$SLINE" | grep -q "$WANT_SPELLS" && ck 0 "her placeholder spells armed at both releases ($WANT_SPELLS, from her package)" || ck 1 "her placeholder spells (wanted $WANT_SPELLS)"
if grep -a -q -E "SCRIPT ERROR|SHADER ERROR|Parse Error" "$LOG/launch_sorceress.log"; then
  ck 1 "her launch free of script and shader errors"; grep -a -E -A2 "SCRIPT ERROR|SHADER ERROR|Parse Error" "$LOG/launch_sorceress.log" | head -12 >&2
else
  ck 0 "her launch free of script and shader errors"
fi
echo "   sizes:"; ls -l "$W" | awk 'NR>1 {printf "   %12d  %s\n", $5, $9}'
# LANE B METEOR (?c=sorceress&meteor=b: her page with the Meteor built 3D first, scripts/meteor_fx.gd):
# the painted plates read and sha-matched, every pipeline warmed at load, the placeholder Meteor off,
# the Fire Ball kept -- and no script or shader error. Without ?meteor=b nothing above changes.
"$GODOT" --main-pack "$W/index.pck" --rendering-method gl_compatibility --rendering-driver opengl3_angle \
  --resolution 640x360 --quit-after 1500 -- --as-web --c sorceress --meteor b > "$LOG/launch_meteor_b.log" 2>&1 || true
MLINE=$(grep -a '^\[meteor_b\] armed' "$LOG/launch_meteor_b.log" | head -1 || true)
echo "   launch (meteor=b): $(echo "$MLINE" | cut -c1-200)"
echo "$MLINE" | grep -q "plates_sha_ok=true" && echo "$MLINE" | grep -q "warmed=true" \
  && echo "$MLINE" | grep -q "placeholder_meteor=off" && echo "$MLINE" | grep -q "fire_ball=kept" \
  && ck 0 "?meteor=b: the Meteor armed (plates matched, pipelines warmed, placeholder off, Fire Ball kept)" \
  || ck 1 "?meteor=b: the Meteor did not arm"
if grep -a -q -E "SCRIPT ERROR|SHADER ERROR|Parse Error" "$LOG/launch_meteor_b.log"; then
  ck 1 "?meteor=b launch free of script and shader errors"; grep -a -E -A2 "SCRIPT ERROR|SHADER ERROR|Parse Error" "$LOG/launch_meteor_b.log" | head -12 >&2
else
  ck 0 "?meteor=b launch free of script and shader errors"
fi
[ "$FAIL" -eq 0 ] || { echo "== VERIFY FAILED" >&2; exit 6; }

if [ "$NO_STAGE" -eq 0 ]; then
  echo "== stage -> $STAGE"
  mkdir -p "$STAGE"
  rsync -a --delete --exclude '.gdignore' "$W/" "$STAGE/"
fi
echo "== done"
