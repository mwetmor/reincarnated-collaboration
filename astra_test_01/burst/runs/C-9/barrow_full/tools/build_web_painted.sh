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
# PIN (conductor, R-C9-152): build another lane's files from a COMMIT, not from its live working copy -- e.g.
#   PIN_SHA=e98bda6bf PIN_PATHS="scripts/eor_kc2_fx.gd scripts/whirlwind_channel.gd" tools/build_web_painted.sh
# writes `git show $PIN_SHA:<godot>/<path>` over the MIRROR's copy only (the source tree is never touched) and records it
if [ -n "${PIN_SHA:-}" ]; then
  REPO=$(git -C "$SRC" rev-parse --show-toplevel); REL=$(python3 -c "import os,sys;print(os.path.relpath(sys.argv[1],sys.argv[2]))" "$SRC" "$REPO")
  for p in ${PIN_PATHS:-}; do
    git -C "$REPO" show "$PIN_SHA:$REL/$p" > "$DEST/$p" || { echo "PIN failed: $PIN_SHA:$REL/$p" >&2; exit 3; }
    echo "   pinned $p @ $PIN_SHA ($(shasum -a 256 "$DEST/$p" | cut -c1-16))"
  done
fi

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
for imp in sorted(list((root / "models" / "gear").glob("*.import")) + list((root / "models" / "sorceress").glob("*.import"))
                  + list((root / "models" / "warlord").glob("*.import")) + list((root / "models" / "variants").glob("*/*.import"))):
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
# R-C9-118: the craters' painted albedo and emission at 512 (a crater is ~220 px across at the play camera; her pack
# crossed the 50 MB fence at 1024 with crater v5's ice and earth variants)
nc = 0
for imp in sorted((root / "data" / "vfx" / "crater_v4").glob("crater_*_*.png.import")):
    t = imp.read_text()
    t = setk(t, "process/size_limit", "512")
    imp.write_text(t)
    nc += 1
print(f"world models' textures discarded: {nd}; his and her gear textures VRAM+mips: {ng} (cut to 512: {ncut}); crater textures cut to 512: {nc}")
PY

echo "== import"
"$GODOT" --headless --path "$DEST" --import > "$LOG/import.log" 2>&1 || {
  echo "import failed" >&2; tail -20 "$LOG/import.log" >&2; exit 4; }

echo "== presets: TWO PACKS -- the barbarian's (index.pck) and hers (sorceress.pck), one wasm"
# HER PACK (C-9 (c)): her Fire Ball's atlas brought the one pck over the 50 MB fence, so the page picks
# its main pack by ?c=, as /playtest/cliffside/ does: each pack the painted Barrow, the scripts, and ONE
# character -- his gear, or her body, gear and spell effects. Nothing he loads is in hers, nor hers in his.
list_files() { (cd "$DEST" && {
  echo "scenes/barrow_painted.tscn"
  ls scripts/*.gd scripts/variants/*.gd
  for m in birch lintel post raven stone_mid stone_short stone_tall; do echo "models/barrow/$m.glb"; done
  for k in cairn log shield; do echo "models/barrow/kit/$k.glb"; done
  case "$1" in him) ls models/gear/*.glb;; her) ls models/sorceress/*.glb;; wl) ls models/warlord/*.glb;; esac
} | sed 's|^|"res://|; s|$|"|' | paste -sd, -); }
FILES_HIM=$(list_files him)
FILES_HER=$(list_files her)
FILES_WL=$(list_files wl)
# R-C9-117: A VARIANT PACK PER SLOT (the select page's armor / hold), fetched by the page only for that slot
vfiles() { (cd "$DEST" && ls models/variants/$1/*.glb | sed 's|^|"res://|; s|$|"|' | paste -sd, -); }
VARIANTS="so_bmc so_bmd so_bm134 barb_gladc barb_gladb barb_t1211 barb_f25l barb_f40l"  # R-C9-127: N25/N40 dropped
vinc() { case "$1" in
  so_bm134) echo "data/slots/so_bm134.json,data/slots/so_bm134_ss4.json,data/slots/gear_so_bm134.json,data/slots/sockets_so_bm134.json";;  # R-C9-138
  so_*) echo "data/slots/$1.json,data/slots/gear_$1.json,data/slots/sockets_so_bm.json";;
  barb_glad*) echo "data/slots/$1.json,data/slots/gear_$1.json";;
  barb_n*) echo "data/slots/$1.json,data/slots/gear_t12d.json";;
  *) echo "data/slots/$1.json,data/slots/gear_t12.json";; esac; }
INC_COMMON="data/barrow_full_layout.json,data/barrow_full_splat.bin,data/painted_web/*.json,data/painted_web/*.bin,data/painted_web/bakes/*.bin"
INC_HIM="$INC_COMMON,data/character.json,data/gear_manifest.json"
INC_WL="$INC_COMMON,data/slots/warlord.json,data/slots/gear_warlord.json,data/slots/warlord_ice.json,data/slots/gear_warlord_ice.json,data/slots/warlord_eyes.json,data/vfx/eor_kc2/*"  # R-C9-143: EOR2's preloads (textures + shaders) are not followed by the resources filter
INC_HER="$INC_COMMON,data/character_sorceress.json,data/gear_manifest_sorceress.json,data/sockets_sorceress.json,data/vfx/fire_ball/*.json,data/vfx/fire_ball/*.bin,data/vfx/meteor_mix2/*.json,data/vfx/meteor_mix2/*.bin,data/vfx/crater_v4/*,data/meteor/*.bin,data/meteor/*.json"
cat > "$DEST/build/.preset_options" <<'OPTS'
[preset.0.options]

custom_template/debug=""
custom_template/release=""
variant/extensions_support=false
variant/thread_support=false
vram_texture_compression/for_desktop=false
vram_texture_compression/for_mobile=true
html/export_icon=true
html/custom_html_shell=""
html/head_include="<base href=\"/playtest/barrow-painted/\"><style>#rotate-hint{display:none;position:fixed;inset:0;z-index:10;background:#0b0f16;color:#e8eef7;font:600 20px/1.4 system-ui,sans-serif;align-items:center;justify-content:center;text-align:center;padding:24px}@media (orientation:portrait) and (pointer:coarse){#rotate-hint{display:flex}}#back-chip{position:fixed;top:calc(env(safe-area-inset-top,0px) + 8px);left:calc(env(safe-area-inset-left,0px) + 8px);z-index:20;font:600 13px/1 system-ui,-apple-system,sans-serif}#back-chip a{display:block;padding:9px 13px;border-radius:999px;background:rgba(11,15,22,.78);color:#e8eef7;border:1px solid rgba(143,200,255,.45);text-decoration:none}</style><script>addEventListener('DOMContentLoaded',function(){var d=document.createElement('div');d.id='rotate-hint';d.textContent='Rotate your phone to landscape to play';document.body.appendChild(d);var n=document.createElement('div');n.id='back-chip';n.innerHTML='<a href=\"/playtest/barrow-painted/?select=1\">← Characters</a>';document.body.appendChild(n);n.addEventListener('pointerdown',function(e){e.stopPropagation();},true);});</script>"
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
OPTS
preset() {  # index name files include
  printf '[preset.%s]\n\nname="%s"\nplatform="Web"\nrunnable=%s\nadvanced_options=false\ndedicated_server=false\ncustom_features=""\n' \
    "$1" "$2" "$( [ "$1" = 0 ] && echo true || echo false )"
  printf 'export_filter="resources"\nexport_files=PackedStringArray(%s)\ninclude_filter="%s"\nexclude_filter="tools/*"\n' "$3" "$4"
  printf 'export_path="build/web/index.html"\npatches=PackedStringArray()\nencryption_include_filters=""\nencryption_exclude_filters=""\n'
  printf 'seed=0\nencrypt_pck=false\nencrypt_directory=false\nscript_export_mode=2\n\n'
  sed "s/^\[preset.0.options\]/[preset.$1.options]/" "$DEST/build/.preset_options"
  echo
}
# LANE A FOR REFERENCE (?meteor=a): its full atlas is its own pack, fetched by the page only for ?meteor=a;
# MIX v2 is her default and ships A's BURST (meteor_mix2); the first mix's FALL frames (?meteor=mix1) are
# their own small pack, meteor_mix1.pck, fetched only for ?meteor=mix1
{ preset 0 "Web" "$FILES_HIM" "$INC_HIM"; preset 1 "WebHer" "$FILES_HER" "$INC_HER"; preset 2 "WebMeteorA" "" "data/vfx/meteor_a/*.json,data/vfx/meteor_a/*.bin"
  preset 3 "WebMeteorMix1" "" "data/vfx/meteor_mix/*.json,data/vfx/meteor_mix/*.bin"
  preset 4 "WebWarlord" "$FILES_WL" "$INC_WL"
  n=5; for v in $VARIANTS; do preset $n "WebVar_$v" "$(vfiles $v)" "$(vinc $v)"; n=$((n+1)); done; } > "$DEST/export_presets.cfg"

echo "== export Web"
mkdir -p "$DEST/build/web"
"$GODOT" --headless --path "$DEST" --export-release "Web" build/web/index.html > "$LOG/export.log" 2>&1 || {
  echo "export failed" >&2; tail -30 "$LOG/export.log" >&2; exit 5; }
"$GODOT" --headless --path "$DEST" --export-pack "WebHer" build/web/sorceress.pck > "$LOG/export_her.log" 2>&1 || {
  echo "export (her pack) failed" >&2; tail -30 "$LOG/export_her.log" >&2; exit 5; }
"$GODOT" --headless --path "$DEST" --export-pack "WebMeteorA" build/web/meteor_a.pck > "$LOG/export_meteor_a.log" 2>&1 || {
  echo "export (lane A's pack) failed" >&2; tail -30 "$LOG/export_meteor_a.log" >&2; exit 5; }
"$GODOT" --headless --path "$DEST" --export-pack "WebMeteorMix1" build/web/meteor_mix1.pck > "$LOG/export_meteor_mix1.log" 2>&1 || {
  echo "export (the first mix's fall pack) failed" >&2; tail -30 "$LOG/export_meteor_mix1.log" >&2; exit 5; }
"$GODOT" --headless --path "$DEST" --export-pack "WebWarlord" build/web/warlord.pck > "$LOG/export_warlord.log" 2>&1 || {
  echo "export (the dark knight's pack) failed" >&2; tail -30 "$LOG/export_warlord.log" >&2; exit 5; }
for v in $VARIANTS; do
  "$GODOT" --headless --path "$DEST" --export-pack "WebVar_$v" build/web/variant_$v.pck > "$LOG/export_variant_$v.log" 2>&1 || {
    echo "export (variant $v) failed" >&2; tail -30 "$LOG/export_variant_$v.log" >&2; exit 5; }
done
echo "== the page picks its pack by ?c="
python3 - "$DEST/build/web" <<'CHOOSER'
import os, re, sys
w = sys.argv[1]
p = os.path.join(w, "index.html")
t = open(p).read()
packs = {"barbarian": ("index.pck", os.path.getsize(os.path.join(w, "index.pck"))),
         "sorceress": ("sorceress.pck", os.path.getsize(os.path.join(w, "sorceress.pck"))),
         "warlord": ("warlord.pck", os.path.getsize(os.path.join(w, "warlord.pck")))}
m = re.search(r"const GODOT_CONFIG = (\{.*?\});", t)
assert m, "no GODOT_CONFIG in index.html"
js = ("\nconst GODOT_PACKS = {" + ", ".join('"%s": {"pack": "%s", "size": %d}' % (k, v[0], v[1]) for k, v in packs.items()) + "};\n"
      "(function () {\n"
      "\tconst c = (new URLSearchParams(window.location.search).get('c') || '').toLowerCase();\n"
      "\tconst pick = (c === 'sorceress' || c === 'warlord') ? c : 'barbarian';\n"
      "\tGODOT_CONFIG['mainPack'] = GODOT_PACKS[pick].pack;\n"
      "\tGODOT_CONFIG['fileSizes'] = {[GODOT_PACKS[pick].pack]: GODOT_PACKS[pick].size, 'index.wasm': GODOT_CONFIG['fileSizes']['index.wasm']};\n"
      "}());\n")
t = t[:m.end()] + js + t[m.end():]
open(p, "w").write(t)
print("packs:", {k: v[1] for k, v in packs.items()})
CHOOSER

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
COMMON="scenes/barrow_painted.tscn scripts/barrow_full.gd scripts/painted_world.gd scripts/paint_stack.gd
         scripts/snow_field.gd scripts/barrow_heather.gd scripts/barrow_touch.gd scripts/knight.gd
         scripts/foot_lock.gd data/barrow_full_layout.json data/barrow_full_splat.bin
         data/painted_web/manifest.json data/painted_web/heather.json data/painted_web/painting.bin
         data/painted_web/lit.bin data/painted_web/snow_grid.bin $BAKES"
for p in $COMMON models/gear/nb-body.glb data/character.json data/gear_manifest.json; do
  grep -a -q "$p" "$W/index.pck" || { echo "   missing from index.pck: $p" >&2; MISSING=1; }
done
for p in $COMMON scripts/sorceress_knight.gd scripts/spell_fx.gd scripts/fire_ball_fx.gd data/character_sorceress.json \
         data/gear_manifest_sorceress.json data/sockets_sorceress.json models/sorceress/so-body.glb \
         models/sorceress/robe.glb models/sorceress/mantle.glb models/sorceress/belt.glb \
         models/sorceress/bracers.glb models/sorceress/circlet.glb models/sorceress/staff.glb \
         data/vfx/fire_ball/fire_ball.json data/vfx/fire_ball/atlas_0.bin data/vfx/fire_ball/atlas_1.bin \
         scripts/meteor_a_fx.gd scripts/meteor_fx.gd scripts/cinders_fx.gd scripts/crater_fx.gd scripts/crater_v4_fx.gd data/vfx/meteor_mix2/meteor_mix2.json \
         data/vfx/meteor_mix2/atlas_0.bin data/vfx/meteor_mix2/atlas_1.bin; do
  grep -a -q "$p" "$W/sorceress.pck" || { echo "   missing from sorceress.pck: $p" >&2; MISSING=1; }
done
# the crossings by each pack's FILE TABLE (tools/pck_list.py): a path a script or the uid cache names is
# not a packed file, and grepping the bytes finds both
python3 "$SRC/../tools/pck_list.py" "$W/index.pck" | grep -q "^models/sorceress/" && { echo "   her models are in HIS pack" >&2; MISSING=1; }
python3 "$SRC/../tools/pck_list.py" "$W/sorceress.pck" | grep -q "^models/gear/" && { echo "   his models are in HER pack" >&2; MISSING=1; }
# MIX v2: only A's burst ships in her pack; A's full atlas is meteor_a.pck's alone, the first mix's fall
# frames meteor_mix1.pck's alone
python3 "$SRC/../tools/pck_list.py" "$W/sorceress.pck" | grep -q "^data/vfx/meteor_a/" && { echo "   lane A's full atlas is in HER pack" >&2; MISSING=1; }
python3 "$SRC/../tools/pck_list.py" "$W/sorceress.pck" | grep -q "^data/vfx/meteor_mix/" && { echo "   the first mix's fall frames are in HER pack" >&2; MISSING=1; }
for f in meteor_mix.json atlas_0.bin; do
  python3 "$SRC/../tools/pck_list.py" "$W/meteor_mix1.pck" | grep -q "^data/vfx/meteor_mix/$f$" || { echo "   missing from meteor_mix1.pck: $f" >&2; MISSING=1; }
done
for f in meteor_a.json atlas_0.bin atlas_1.bin; do
  python3 "$SRC/../tools/pck_list.py" "$W/meteor_a.pck" | grep -q "^data/vfx/meteor_a/$f$" || { echo "   missing from meteor_a.pck: $f" >&2; MISSING=1; }
done
[ "$MISSING" -eq 0 ] && ck 0 "the painted Barrow and its phone data in both packs; him in index.pck, her and her Fire Ball in sorceress.pck, neither in the other's" \
                     || ck 1 "the packs' contents"
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
"$GODOT" --main-pack "$W/sorceress.pck" --rendering-method gl_compatibility --rendering-driver opengl3_angle \
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
print("spells=" + ",".join("%s@%s" % (by_slot[s]["clip"], by_slot[s]["release_s"]) for s in ("attack", "chop")))
SPELLS
)
# lane B's Meteor (her default) takes the chop slot off spell_fx and reads its release itself; the
# placeholder run below must still show both
WANT_FB=${WANT_SPELLS%%,*}
echo "$SLINE" | grep -q "$WANT_FB" && ck 0 "her Fire Ball armed at its release ($WANT_FB, from her package)" || ck 1 "her Fire Ball's release (wanted $WANT_FB)"
FB=$(echo "$SLINE" | sed -n 's/.*fire_ball=\([^ ]*\).*/\1/p')
echo "$FB" | grep -q "^baked(pages=2,px=4096x[0-9]*,frames=[0-9]*,impact_sets=2,sha_ok)\(+c75\)\?$" \
  && ck 0 "her FIRE BALL baked and loaded from her pack: $FB" || ck 1 "her Fire Ball (got '$FB')"
if grep -a -q -E "SCRIPT ERROR|SHADER ERROR|Parse Error" "$LOG/launch_sorceress.log"; then
  ck 1 "her launch free of script and shader errors"; grep -a -E -A2 "SCRIPT ERROR|SHADER ERROR|Parse Error" "$LOG/launch_sorceress.log" | head -12 >&2
else
  ck 0 "her launch free of script and shader errors"
fi
echo "   sizes:"; ls -l "$W" | awk 'NR>1 {printf "   %12d  %s\n", $5, $9}'
# LANE B METEOR (?c=sorceress&meteor=b: her page with the Meteor built 3D first, scripts/meteor_fx.gd):
# the painted plates read and sha-matched, every pipeline warmed at load, the placeholder Meteor off,
# the Fire Ball kept -- and no script or shader error. Without ?meteor=b nothing above changes.
"$GODOT" --main-pack "$W/sorceress.pck" --rendering-method gl_compatibility --rendering-driver opengl3_angle \
  --resolution 640x360 --quit-after 1500 -- --as-web --c sorceress --meteor b > "$LOG/launch_meteor_b.log" 2>&1 || true
MLINE=$(grep -a '^\[meteor_b\] armed' "$LOG/launch_meteor_b.log" | head -1 || true)
MSL=$(grep -a '^\[barrow_painted\] web:' "$LOG/launch_meteor_b.log" | head -1 || true)
echo "$MSL" | grep -q "fire_ball=baked(" && echo "$MSL" | grep -q "meteor=3d(lane_b)" \
  && ck 0 "?meteor=b: her baked Fire Ball still loads beside it (fire_ball=baked, meteor=3d)" \
  || ck 1 "?meteor=b: her Fire Ball or the meteor word"
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
# HER DEFAULT METEOR IS MATT'S MIX v3 (no query): the ball of fire with its dark core, A's painted burst,
# the crater, the warp in the post pass, no ring, the shadow on; ?meteor_shadow=0 turns the shadow off;
# ?meteor=mix2 is MIX v2; ?meteor=mix1 (fetched, Chrome) the first mix; ?meteor=b lane B as shipped;
# ?meteor=placeholder falls back
echo "$SLINE" | grep -q "meteor=mix4(fall=lane_b_core,impact=lane_a,burn=crater_v4,warp=post,ring=off,shadow=on,fall_s=0.82)" \
  && ck 0 "her default Meteor is MIX v4 (R-C9-118: crater v4)" || ck 1 "her default Meteor (got: $(echo "$SLINE" | grep -o 'meteor=[^ ]*'))"
"$GODOT" --main-pack "$W/sorceress.pck" --rendering-method gl_compatibility --rendering-driver opengl3_angle \
  --resolution 640x360 --quit-after 900 -- --as-web --c sorceress --meteor mix2 > "$LOG/launch_meteor_mix2.log" 2>&1 || true
M2LINE=$(grep -a '^\[barrow_painted\] web:' "$LOG/launch_meteor_mix2.log" | head -1 || true)
echo "$M2LINE" | grep -q "meteor=mix2(fall=lane_b_dark,impact=lane_a,burn=cinders,ring=off,rock_shadow=on)" \
  && ck 0 "?meteor=mix2: MIX v2 kept" || ck 1 "?meteor=mix2 (got: $(echo "$M2LINE" | grep -o 'meteor=[^ ]*'))"
grep -a -q -E "SCRIPT ERROR|SHADER ERROR|Parse Error" "$LOG/launch_meteor_mix2.log" && ck 1 "?meteor=mix2 launch errors" || ck 0 "?meteor=mix2 launch free of script and shader errors"
"$GODOT" --main-pack "$W/sorceress.pck" --rendering-method gl_compatibility --rendering-driver opengl3_angle \
  --resolution 640x360 --quit-after 900 -- --as-web --c sorceress --meteor-shadow 0 > "$LOG/launch_meteor_noshadow.log" 2>&1 || true
NLINE=$(grep -a '^\[barrow_painted\] web:' "$LOG/launch_meteor_noshadow.log" | head -1 || true)
echo "$NLINE" | grep -q "meteor=mix4(fall=lane_b_core,impact=lane_a,burn=crater_v4,warp=post,ring=off,shadow=off,fall_s=0.82)" \
  && ck 0 "?meteor_shadow=0: MIX v4 without the shadow" || ck 1 "?meteor_shadow=0 (got: $(echo "$NLINE" | grep -o 'meteor=[^ ]*'))"
# ?meteor=mix4 (R-C9-109): CRATER v4 -- the real 3D crater, painted, with its particles; not her default until Matt's look
"$GODOT" --main-pack "$W/sorceress.pck" --rendering-method gl_compatibility --rendering-driver opengl3_angle \
  --resolution 640x360 --quit-after 900 -- --as-web --c sorceress --meteor mix4 > "$LOG/launch_meteor_mix4.log" 2>&1 || true
M4LINE=$(grep -a '^\[barrow_painted\] web:' "$LOG/launch_meteor_mix4.log" | head -1 || true)
echo "$M4LINE" | grep -q "meteor=mix4(fall=lane_b_core,impact=lane_a,burn=crater_v4,warp=post,ring=off,shadow=on,fall_s=0.82)" \
  && ck 0 "?meteor=mix4: crater v4 armed (3 variants from her pack), the fall at 0.82 s" || ck 1 "?meteor=mix4 (got: $(echo "$M4LINE" | grep -o 'meteor=[^ ]*'))"
grep -a -q -E "SCRIPT ERROR|SHADER ERROR|Parse Error" "$LOG/launch_meteor_mix4.log" && ck 1 "?meteor=mix4 launch errors" || ck 0 "?meteor=mix4 launch free of script and shader errors"
python3 "$SRC/../tools/pck_list.py" "$W/sorceress.pck" | grep -c "^data/vfx/crater_v4/" | grep -q -v "^0$" && ck 0 "crater v4's meshes and paintings in her pack" || ck 1 "crater v4's data missing from her pack"
# R-C9-118 CRATER v5 (b) ground-aware craters + R-C9-142 the object SCORCH (part (a), the meteor stopping on objects, RETIRED),
# behind ?v5=b; ?scorch=0 the scorch off (a measurement switch, not on the page)
"$GODOT" --main-pack "$W/sorceress.pck" --rendering-method gl_compatibility --rendering-driver opengl3_angle \
  --resolution 640x360 --quit-after 900 -- --as-web --c sorceress --v5 b > "$LOG/launch_v5.log" 2>&1 || true
grep -a -q '^\[barrow_painted\] web:' "$LOG/launch_v5.log" && ! grep -a -q -E "SCRIPT ERROR|SHADER ERROR|Parse Error" "$LOG/launch_v5.log" \
  && grep -a -q '^\[crater_v5\] crater_v5=on(b) scorch=on(objects=' "$LOG/launch_v5.log" \
  && ck 0 "?v5=b: ground-aware craters + object scorch launch clean" || ck 1 "?v5=b launch (got: $(grep -a '^\[crater_v5\]' "$LOG/launch_v5.log" | head -1 | cut -c1-120))"
"$GODOT" --main-pack "$W/sorceress.pck" --rendering-method gl_compatibility --rendering-driver opengl3_angle \
  --resolution 640x360 --quit-after 900 -- --as-web --c sorceress --v5 b --scorch 0 > "$LOG/launch_v5_noscorch.log" 2>&1 || true
grep -a -q '^\[crater_v5\] crater_v5=on(b) scorch=off' "$LOG/launch_v5_noscorch.log" && ! grep -a -q -E "SCRIPT ERROR|SHADER ERROR|Parse Error" "$LOG/launch_v5_noscorch.log" \
  && ck 0 "?v5=b&scorch=0: the scorch off" || ck 1 "?v5=b&scorch=0"
python3 "$SRC/../tools/pck_list.py" "$W/sorceress.pck" | grep -c "^data/vfx/crater_v4/crater_\(101\|102\|201\|202\)" | grep -q "^[1-9]" \
  && ck 0 "crater v5's ice and earth variants in her pack" || ck 1 "crater v5's ice/earth variants missing from her pack"
# ?fb=c75 (R-C9-110): her Fire Ball's burst tightened to 0.75; the default stays as it was until Matt's look
"$GODOT" --main-pack "$W/sorceress.pck" --rendering-method gl_compatibility --rendering-driver opengl3_angle \
  --resolution 640x360 --quit-after 900 -- --as-web --c sorceress --fb full > "$LOG/launch_fb_c75.log" 2>&1 || true
FLINE=$(grep -a '^\[barrow_painted\] web:' "$LOG/launch_fb_c75.log" | head -1 || true)
echo "$SLINE" | grep -q "sha_ok)+c75" && echo "$FLINE" | grep -q "sha_ok)" && ! echo "$FLINE" | grep -q "+c75" \
  && ck 0 "R-C9-118: her default Fire Ball is c75 (fire_ball=baked(...)+c75); ?fb=full the old burst" || ck 1 "fb default / ?fb=full (got: $(echo "$SLINE" | grep -o 'fire_ball=[^ ]*') / $(echo "$FLINE" | grep -o 'fire_ball=[^ ]*'))"
grep -a -q -E "SCRIPT ERROR|SHADER ERROR|Parse Error" "$LOG/launch_fb_c75.log" && ck 1 "?fb=c75 launch errors" || ck 0 "?fb=c75 launch free of script and shader errors"
"$GODOT" --main-pack "$W/sorceress.pck" --rendering-method gl_compatibility --rendering-driver opengl3_angle \
  --resolution 640x360 --quit-after 900 -- --as-web --c sorceress --meteor placeholder > "$LOG/launch_meteor_placeholder.log" 2>&1 || true
PLINE=$(grep -a '^\[barrow_painted\] web:' "$LOG/launch_meteor_placeholder.log" | head -1 || true)
echo "$PLINE" | grep -q "meteor=placeholder" && echo "$PLINE" | grep -q "fire_ball=baked(" && echo "$PLINE" | grep -q "$WANT_SPELLS" \
  && ck 0 "?meteor=placeholder falls back (meteor=placeholder, both releases $WANT_SPELLS, the Fire Ball still baked)" || ck 1 "?meteor=placeholder fallback"
# LANE A (?meteor=a) comes from meteor_a.pck and the first mix (?meteor=mix1) from meteor_mix1.pck, both
# fetched by the page: fenced above by their file tables, and in Chrome (tools/web_perf_fb.js), not by a
# desktop launch (it cannot fetch)
# R-C9-117: THE DARK KNIGHT'S PACK AND THE VARIANT SLOTS, each launched as the page would (the variant's pack handed
# to the desktop, which cannot fetch), and the pack crossings: no character's models in another's pack
"$GODOT" --main-pack "$W/warlord.pck" --rendering-method gl_compatibility --rendering-driver opengl3_angle \
  --resolution 640x360 --quit-after 900 -- --as-web --c warlord > "$LOG/launch_warlord.log" 2>&1 || true
WLINE=$(grep -a '^\[barrow_painted\] web:' "$LOG/launch_warlord.log" | head -1 || true)
echo "$WLINE" | grep -q "who=warlord slot=warlord eyes=2:9e4dff" && echo "$WLINE" | grep -q "files_sha_ok=28/28" \
  && ck 0 "?c=warlord: the dark knight walks the painted Barrow from warlord.pck, two eye-glow nodes, violet" || ck 1 "?c=warlord (got: $(echo "$WLINE" | cut -c1-120))"
grep -a -q -E "SCRIPT ERROR|SHADER ERROR|Parse Error" "$LOG/launch_warlord.log" && ck 1 "?c=warlord launch errors" || ck 0 "?c=warlord launch free of script and shader errors"
"$GODOT" --main-pack "$W/warlord.pck" --rendering-method gl_compatibility --rendering-driver opengl3_angle \
  --resolution 640x360 --quit-after 900 -- --as-web --c warlord --eye ice > "$LOG/launch_warlord_ice.log" 2>&1 || true
grep -a '^\[barrow_painted\] web:' "$LOG/launch_warlord_ice.log" | head -1 | grep -q "who=warlord slot=warlord_ice eyes=2:59bfff" \
  && ! grep -a -q -E "SCRIPT ERROR|SHADER ERROR|Parse Error" "$LOG/launch_warlord_ice.log" \
  && ck 0 "?c=warlord&eye=ice: the ice helm from the same pack, two eye-glow nodes, ice" || ck 1 "?c=warlord&eye=ice"
# R-C9-128: THE EYE OF RECKONING -- the ported whirlwind bound on his spin clip (final_k_eor's eor_spin_start + loop, read
# by slot_knight.gd), red by default, ?eortint=original the source's own look
echo "$WLINE" | grep -q "eyes=2:9e4dff ww=red " && ck 0 "?c=warlord: the Eye of Reckoning bound (the ported whirlwind on his spin clip), red" || ck 1 "?c=warlord Eye of Reckoning (got: $(echo "$WLINE" | cut -c1-90))"
"$GODOT" --main-pack "$W/warlord.pck" --rendering-method gl_compatibility --rendering-driver opengl3_angle \
  --resolution 640x360 --quit-after 900 -- --as-web --c warlord --eortint original > "$LOG/launch_warlord_eor_orig.log" 2>&1 || true
grep -a '^\[barrow_painted\] web:' "$LOG/launch_warlord_eor_orig.log" | head -1 | grep -q "ww=original " \
  && ! grep -a -q -E "SCRIPT ERROR|SHADER ERROR|Parse Error" "$LOG/launch_warlord_eor_orig.log" \
  && ck 0 "?c=warlord&eortint=original: the Eye of Reckoning in the source's own colours" || ck 1 "?c=warlord&eortint=original"
for v in $VARIANTS; do
  case "$v" in so_*) MP=sorceress.pck; C=sorceress; Q="--armor ${v#so_}";; barb_glad*) MP=index.pck; C=barbarian; Q="--armor ${v#barb_}";; *) MP=index.pck; C=barbarian; Q="--hold ${v#barb_}";; esac
  "$GODOT" --main-pack "$W/$MP" --rendering-method gl_compatibility --rendering-driver opengl3_angle \
    --resolution 640x360 --quit-after 900 -- --as-web --c $C $Q --variant-pack "$W/variant_$v.pck" > "$LOG/launch_variant_$v.log" 2>&1 || true
  VLINE=$(grep -a '^\[barrow_painted\] web:' "$LOG/launch_variant_$v.log" | head -1 || true)
  if echo "$VLINE" | grep -q "who=$C slot=$v " && ! grep -a -q -E "SCRIPT ERROR|SHADER ERROR|Parse Error" "$LOG/launch_variant_$v.log"; then
    ck 0 "variant $v: launches from $MP + variant_$v.pck ($(( $(stat -f %z "$W/variant_$v.pck") / 1000000 )) MB), no script or shader error"
  else ck 1 "variant $v (got: $(echo "$VLINE" | cut -c1-120); errors: $(grep -a -c -E 'SCRIPT ERROR|SHADER ERROR' "$LOG/launch_variant_$v.log"))"; fi
done
# R-C9-138: the arena kit's alternate idle (?armor=bm134&soidle=ss4) from the same variant pack
"$GODOT" --main-pack "$W/sorceress.pck" --rendering-method gl_compatibility --rendering-driver opengl3_angle \
  --resolution 640x360 --quit-after 900 -- --as-web --c sorceress --armor bm134 --soidle ss4 --variant-pack "$W/variant_so_bm134.pck" > "$LOG/launch_variant_so_bm134_ss4.log" 2>&1 || true
grep -a '^\[barrow_painted\] web:' "$LOG/launch_variant_so_bm134_ss4.log" | head -1 | grep -q "who=sorceress slot=so_bm134_ss4 " \
  && ! grep -a -q -E "SCRIPT ERROR|SHADER ERROR|Parse Error" "$LOG/launch_variant_so_bm134_ss4.log" \
  && ck 0 "?armor=bm134&soidle=ss4: the arena kit with the sword-and-shield idle, from variant_so_bm134.pck" || ck 1 "?armor=bm134&soidle=ss4"
# R-C9-139: CHARACTER LIGHT (?charlight=a|b|c, scripts/char_light.gd: the characters' own ramp materials only; no light added)
echo "$SLINE" | grep -q "charlight=current" && ck 0 "no ?charlight: the shipped light (charlight=current)" || ck 1 "default charlight (got: $(echo "$SLINE" | grep -o 'charlight=[^ ]*'))"
"$GODOT" --main-pack "$W/sorceress.pck" --rendering-method gl_compatibility --rendering-driver opengl3_angle \
  --resolution 640x360 --quit-after 900 -- --as-web --c sorceress --charlight b --v5 b > "$LOG/launch_charlight_b_her.log" 2>&1 || true
grep -a '^\[barrow_painted\] web:' "$LOG/launch_charlight_b_her.log" | head -1 | grep -q "charlight=b(" \
  && ! grep -a -q -E "SCRIPT ERROR|SHADER ERROR|Parse Error" "$LOG/launch_charlight_b_her.log" \
  && ck 0 "?c=sorceress&charlight=b&v5=b: sun + fill on her, the Meteor's fire shaders and the scorch clean" || ck 1 "?charlight=b (sorceress)"
for CL in a c; do
"$GODOT" --main-pack "$W/warlord.pck" --rendering-method gl_compatibility --rendering-driver opengl3_angle \
  --resolution 640x360 --quit-after 900 -- --as-web --c warlord --charlight $CL > "$LOG/launch_charlight_${CL}_wl.log" 2>&1 || true
grep -a '^\[barrow_painted\] web:' "$LOG/launch_charlight_${CL}_wl.log" | head -1 | grep -q "charlight=${CL}(" \
  && ! grep -a -q -E "SCRIPT ERROR|SHADER ERROR|Parse Error" "$LOG/launch_charlight_${CL}_wl.log" \
  && ck 0 "?c=warlord&charlight=$CL clean" || ck 1 "?charlight=$CL (warlord)"
done
"$GODOT" --main-pack "$W/index.pck" --rendering-method gl_compatibility --rendering-driver opengl3_angle \
  --resolution 640x360 --quit-after 900 -- --as-web --charlight b > "$LOG/launch_charlight_b_him.log" 2>&1 || true
grep -a '^\[barrow_painted\] web:' "$LOG/launch_charlight_b_him.log" | head -1 | grep -q "charlight=b(" \
  && ! grep -a -q -E "SCRIPT ERROR|SHADER ERROR|Parse Error" "$LOG/launch_charlight_b_him.log" \
  && ck 0 "barbarian ?charlight=b clean" || ck 1 "?charlight=b (barbarian)"
# TEXTURE PROVENANCE (the coordinator, after the E1 lane's flat-texture finding): every body and gear GLB the packs carry
# against its intended source (the painted / graded atlas its lane's record names, or its own lane export where no painted
# atlas exists) -- tools/texture_provenance.py; the shipped final_i dark knight body (Tripo's flat texture) is its
# negative control
if python3 "$SRC/../tools/texture_provenance.py" --json "$LOG/texture_provenance.json" > "$LOG/texture_provenance.txt" 2>&1; then
  ck 0 "texture provenance: $(tail -1 "$LOG/texture_provenance.txt" | sed 's/texture provenance: //')"
else
  ck 1 "texture provenance: $(tail -1 "$LOG/texture_provenance.txt" | sed 's/texture provenance: //'); FAIL rows: $(grep '^FAIL' "$LOG/texture_provenance.txt" | awk '{print $3}' | tr '\n' ' ')"
fi
# C-9 BIND-ORDER: every gear piece of every pack, on its body's skeleton in one fixed pose, rendered bound by bone INDEX
# and by bone NAME; ANY pixel difference fails (the piece's file order differs from its body's -- the wl_e1 stage-K
# defect: final_j's pieces landed on the wrong bones by index). tools/probe_bind_order.gd, run on the source project
# (the staged copy carries no tools/), imported first so a re-staged piece is what it reads.
"$GODOT" --headless --path "$SRC" --import > "$LOG/bind_order_import.log" 2>&1 || true
perl -e 'alarm shift; exec @ARGV' 900 "$GODOT" --path "$SRC" --resolution 640x640 --rendering-method gl_compatibility \
  --rendering-driver opengl3_angle --script tools/probe_bind_order.gd -- --out "$LOG/bind_order" > "$LOG/bind_order.txt" 2>&1
BO=$?
BOL=$(grep -a '^bind order:' "$LOG/bind_order.txt" | tail -1)
if [ "$BO" -eq 0 ] && [ -n "$BOL" ]; then
  ck 0 "${BOL}: every gear piece draws the same pixels bound by index and by name"
else
  ck 1 "${BOL:-bind order: no result (exit $BO)}; FAIL rows: $(grep -a '^BIND FAIL' "$LOG/bind_order.txt" | awk '{print $3"/"$4}' | tr '\n' ' ')"
fi
CROSS=0
for pk in index.pck sorceress.pck; do python3 "$SRC/../tools/pck_list.py" "$W/$pk" | grep -q -E "^models/(warlord|variants)/" && { echo "   $pk carries the dark knight or a variant" >&2; CROSS=1; }; done
python3 "$SRC/../tools/pck_list.py" "$W/warlord.pck" | grep -q -E "^models/(gear|sorceress|variants)/" && { echo "   warlord.pck carries another character" >&2; CROSS=1; }
[ "$CROSS" -eq 0 ] && ck 0 "lazy per character: his, her and the dark knight's packs carry only their own models; every variant is its own pack" || ck 1 "pack crossings"
[ "$FAIL" -eq 0 ] || { echo "== VERIFY FAILED" >&2; exit 6; }

# R-C9-117: THE SELECT SCREEN IS THE PAGE'S INDEX; the game moves to play.html (same directory, same base href, the same
# packs). Old links with a query go straight to the game (the select page's first script).
mv "$W/index.html" "$W/play.html"
mkdir -p "$W/select"
cp "$SRC/../tools/select/index.html" "$W/index.html"
cp "$SRC/../tools/select/"*.jpg "$W/select/"
grep -q "location.replace('play.html' + location.search)" "$W/index.html" && grep -q "const GODOT_PACKS" "$W/play.html" \
  && grep -q '"warlord": {"pack": "warlord.pck"' "$W/play.html" && [ -s "$W/select/barbarian.jpg" ] && [ -s "$W/select/sorceress.jpg" ] && [ -s "$W/select/warlord.jpg" ] \
  && echo "   ok   the select page is the index (3 portraits), the game is play.html with the dark knight's pack" \
  || { echo "   FAIL the select page / play.html" >&2; exit 6; }

if [ "$NO_STAGE" -eq 0 ]; then
  echo "== stage -> $STAGE"
  mkdir -p "$STAGE"
  rsync -a --delete --exclude '.gdignore' "$W/" "$STAGE/"
fi
echo "== done"
