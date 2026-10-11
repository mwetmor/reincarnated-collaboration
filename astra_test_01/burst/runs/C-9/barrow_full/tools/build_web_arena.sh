#!/bin/bash
# C-9 BV2F ARENA (R-C9-391/394) -- THE ARENA AS ONE WEB PAGE (PC mouse/keyboard + phone touch), for
# /playtest/barrow-arena/ on the loadout site. Shape: tools/build_web_painted.sh (e8d0d0f's route).
#   1. mirror barrow_full/godot -> web_arena/ (only what the arena reads; its .godot import cache kept between builds)
#   2. tools/arena_bundle.py: vendor + verify the KC2 runtime (a0e75469) and the model pack of record, the leech table
#      (the R-C9-394 path shim's input), the outside files, and the waves' kits at native size as q95 WebP, in KIT PACKS
#   3. import; Web preset (nothreads, Compatibility, base href) + one preset per kit pack; export
#   4. FENCE: file sizes + isolated packaged-input probe + real Chrome startup/desktop/touch/failure tests
#   5. stage build/web/ into reincarnated-loadout/public/playtest/barrow-arena/ (never commits, never pushes)
#   usage: tools/build_web_arena.sh [--no-stage]
set -euo pipefail
SRC=$(cd "$(dirname "$0")/.." && pwd)/godot
TOOLS=$(cd "$(dirname "$0")" && pwd)
DEST=$(dirname "$SRC")/web_arena
LOG=$DEST/build/logs
LOADOUT=${LOADOUT:-$HOME/Games/reincarnated-loadout}
STAGE=$LOADOUT/public/playtest/barrow-arena
GODOT=${GODOT:-/Applications/Godot.app/Contents/MacOS/Godot}
HEAVY_LOCK=${HEAVY_LOCK:-$HOME/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-7/conductor_scripts/heavy_lock.py}
MAX_FILE_MB=50
GATE=${DISK_GATE_GIB:-26}
NO_STAGE=0
REFRESH=0
for ARG in "$@"; do
  case "$ARG" in
    --no-stage) NO_STAGE=1 ;;
    --refresh) REFRESH=1 ;;
    *) echo "Unknown option: $ARG" >&2; exit 2 ;;
  esac
done
if [ "$REFRESH" = 1 ]; then
  # Reuse existing audited art/imports; exports total <600 MB. Full build's
  # 26 GiB reservation remains unchanged. Refresh has a separate 8 GiB gate.
  [ -f "$DEST/build/web/index.pck" ] && [ -f "$DEST/.godot/global_script_class_cache.cfg" ] || exit 2
  GATE=8
fi
FREE=$(df -g /System/Volumes/Data | awk 'NR==2{print $4}')
[ "$FREE" -ge "$GATE" ] || { echo "HALT: ${FREE} GiB free, under the $GATE GiB gate" >&2; exit 9; }
if [ -z "${C9_LOCKED:-}" ]; then
  exec env C9_LOCKED=1 python3 "$HEAVY_LOCK" C-9 -- bash "$0" "$@"
fi

echo "== 1 mirror $SRC -> $DEST"
mkdir -p "$DEST" "$LOG"
# Exclusions also protect receiver caches. macOS openrsync's --delete-excluded
# ignores P rules and destroys those caches; do not use that switch here.
rsync -a --delete --exclude 'kc2/model_pack/' --exclude 'kc2/art/' --exclude 'kc2/bundle/' --exclude '.godot/' --exclude 'build/' --exclude 'export_presets.cfg' --exclude 'tools/' \
  --exclude 'data/painted/' --exclude 'data/painted_web/' --exclude 'data/bv2f/site_ph3/' --exclude 'data/bv2f/pilot*/' \
  --exclude 'data/bv2f/site_ph4/painted/' --exclude 'models/barrow/' --exclude 'models/gear/' --exclude 'models/sorceress/' \
  --exclude 'models/variants/' --exclude 'data/vfx/meteor*/' --exclude 'data/meteor/' --exclude 'data/bv2f/stair_snow/' --exclude 'data/barrow_v2_sw/' --exclude 'kc2/kc2_runtime' --exclude 'kc2/art_x/' --exclude 'kc2/.gdignore' \
  --exclude 'captures/' "$SRC"/ "$DEST"/
mkdir -p "$DEST/build" "$LOG"; touch "$DEST/build/.gdignore"
cp "$TOOLS/arena_web_shell.html" "$DEST/arena_web_shell.html"
python3 - "$DEST" <<'PY'
import pathlib, re, sys
pg = pathlib.Path(sys.argv[1]) / "project.godot"
t = pg.read_text()
t = re.sub(r'^run/main_scene=".*"$', 'run/main_scene="res://scenes/bv2f_arena.tscn"', t, flags=re.M)
t = re.sub(r'^config/name=".*"$', 'config/name="C-9 Barrow arena"', t, flags=re.M)
pg.write_text(t)
assert 'run/main_scene="res://scenes/bv2f_arena.tscn"' in t
assert 'renderer/rendering_method.web="gl_compatibility"' in t, "no web Compatibility renderer"
PY

echo "== 2 bundle"
python3 "$TOOLS/arena_web_texture_detail.py" "$DEST" | tee "$LOG/world_texture_detail.log"
if [ "$REFRESH" = 1 ]; then
  python3 "$TOOLS/arena_restore_web_cache.py" "$DEST"
  python3 "$TOOLS/arena_bundle.py" "$DEST" --refresh | tee "$LOG/bundle.log"
else
  python3 "$TOOLS/arena_bundle.py" "$DEST" | tee "$LOG/bundle.log"
fi
python3 "$TOOLS/arena_stage_audio.py" --project "$DEST" | tee "$LOG/audio_stage.log"
# Prune unused derived payloads only in this disposable export mirror.
python3 - "$DEST" <<'PY'
import json, pathlib, sys
root = pathlib.Path(sys.argv[1]); audio = root / 'data/audio'
manifest = json.loads((audio / 'arena_audio.json').read_text())
used = {c['file'] for c in manifest['clips'].values()}
for p in audio.glob('*.bin'):
    if p.name not in used: p.unlink()
groups, group, size = [], [], 0
for c in manifest['clips'].values():
    if group and size + c['bytes'] > 38_000_000:
        groups.append(group); group, size = [], 0
    group.append('data/audio/' + c['file']); size += c['bytes']
if group: groups.append(group)
stamp_path = root / 'kc2/bundle/BUNDLE_STAMP.json'
stamp = json.loads(stamp_path.read_text())
stamp['audio_packs'] = {'audio_%d.pck' % i: g for i, g in enumerate(groups)}
stamp['kit_packs'] += list(stamp['audio_packs'])
stamp_path.write_text(json.dumps(stamp, indent=1))
PY

echo "== 2b the rig's textures for the web (VRAM + mips, bounded at 2048; the walk build's rule)"
python3 - "$DEST" <<'PY'
import pathlib, re, sys
root = pathlib.Path(sys.argv[1])
def setk(t, k, v):
    return re.sub(rf"^{re.escape(k)}=.*$", f"{k}={v}", t, flags=re.M) if re.search(rf"^{re.escape(k)}=", t, re.M) \
        else t.replace("[params]", f"[params]\n\n{k}={v}", 1)
n = 0
for imp in sorted((root / "models" / "warlord").glob("*.import")):
    if imp.with_suffix("").suffix.lower() in (".png", ".jpg", ".jpeg"):
        t = imp.read_text()
        for k, v in (("compress/mode", "2"), ("mipmaps/generate", "true"), ("process/size_limit", "2048")):
            t = setk(t, k, v)
        imp.write_text(t)
        n += 1
print("warlord textures for web:", n)
PY

echo "== 3 import"
"$GODOT" --headless --path "$DEST" --import > "$LOG/import.log" 2>&1 || { tail -20 "$LOG/import.log" >&2; exit 4; }

echo "== 3b presets"
python3 - "$DEST" <<'PY'
import json, pathlib, sys
root = pathlib.Path(sys.argv[1])
st = json.load(open(root / "kc2/bundle/BUNDLE_STAMP.json"))
scripts = sorted("res://" + str(p.relative_to(root)) for p in (root / "scripts").rglob("*.gd"))
glbs = sorted("res://" + str(p.relative_to(root)) for p in (root / "models" / "warlord").glob("*.glb"))
files = ["res://scenes/bv2f_arena.tscn"] + scripts
art_kits = [k for v in st["kit_pack_members"].values() for k in v]
head = ('<base href="/playtest/barrow-arena/"><style>#rotate-hint{display:none;position:fixed;inset:0;z-index:10;'
        'background:#0b0f16;color:#e8eef7;font:600 20px/1.4 system-ui,sans-serif;align-items:center;justify-content:center;'
        'text-align:center;padding:24px}@media (orientation:portrait) and (pointer:coarse){#rotate-hint{display:flex}}</style>'
        '<script>addEventListener(\'DOMContentLoaded\',function(){var d=document.createElement(\'div\');d.id=\'rotate-hint\';'
        'd.textContent=\'Rotate your phone to landscape to play\';document.body.appendChild(d);});</script>')
def q(s):
    return s.replace('\\', '\\\\').replace('"', '\\"')
opts = """custom_template/debug=""
custom_template/release=""
variant/extensions_support=false
variant/thread_support=false
vram_texture_compression/for_desktop=false
vram_texture_compression/for_mobile=true
html/export_icon=true
html/custom_html_shell="res://arena_web_shell.html"
html/head_include="%s"
html/canvas_resize_policy=2
html/focus_canvas_on_start=true
html/experimental_virtual_keyboard=false
progressive_web_app/enabled=false
progressive_web_app/ensure_cross_origin_isolation_headers=false
threads/emscripten_pool_size=8
threads/godot_pool_size=4
""" % q(head)
out = []
def preset(i, name, filt, files_, inc, exc):
    out.append('[preset.%d]\n\nname="%s"\nplatform="Web"\nrunnable=%s\nadvanced_options=false\ndedicated_server=false\n'
               'custom_features=""\nexport_filter="%s"\nexport_files=PackedStringArray(%s)\ninclude_filter="%s"\n'
               'exclude_filter="%s"\nexport_path="build/web/index.html"\npatches=PackedStringArray()\n'
               'encryption_include_filters=""\nencryption_exclude_filters=""\nseed=0\nencrypt_pck=false\n'
               'encrypt_directory=false\nscript_export_mode=0\n\n[preset.%d.options]\n\n%s\n' % (
                   i, name, "true" if i == 0 else "false", filt, ",".join('"%s"' % f for f in files_), inc, exc, i, opts))
# script_export_mode=0: scripts ship as TEXT -- the vendored runtime's .gd bytes are its source bytes (the launch
#   refusal re-hashes them from the pck)
preset(0, "WebArena", "resources", files,
       "data/*.json,data/*.bin,data/*.f32,data/*.gdshader,data/*.webp,kc2/bundle/*,kc2/model_pack/manifest.json,kc2/kc2_runtime/*,kc2/art/join1_index.json,data/vfx/*",
       "tools/*,data/audio/*.bin,kc2/model_pack/model/*,kc2/bundle/eor4x*,models/*,data/bv2f/ext/*,data/bv2f/site_ph4/*," + ",".join("kc2/art/%s/*" % k for k in art_kits))
# the hero's rig (his GLBs + the eor4x clips) rides in its own pack: it is read only when the arena opens
preset(1, "hero_0", "resources", glbs, "kc2/bundle/eor4x*", "tools/*")
n = 2
for pk, mem in {**st["model_packs"], **st["vfx_packs"], **st['audio_packs']}.items():
    preset(n, pk.replace(".pck", ""), "resources", [], ",".join(mem), "tools/*")
    n += 1
for i, (pk, kits) in enumerate(st["kit_pack_members"].items()):
    preset(n, pk.replace(".pck", ""), "resources", [], ",".join("kc2/art/%s/*" % k for k in kits), "tools/*")
    n += 1
# the site's data (the extension models, the ph4 level and phone painting): its own packs, loaded before the scene builds
preset(n, "site_0", "resources", [], "data/bv2f/ext/*,data/bv2f/site_ph4/level/*", "tools/*")
preset(n + 1, "site_1", "resources", [], "data/bv2f/site_ph4/painted_web/*", "tools/*")
(root / "export_presets.cfg").write_text("\n".join(out))
print("presets: main + %d kit packs; %d scripts, %d glbs" % (len(st["kit_pack_members"]), len(scripts), len(glbs)))
PY

echo "== 3c export"
rm -rf "$DEST/build/web"; mkdir -p "$DEST/build/web"
"$GODOT" --headless --path "$DEST" --export-release "WebArena" "$DEST/build/web/index.html" > "$LOG/export.log" 2>&1 \
  || { tail -30 "$LOG/export.log" >&2; exit 5; }
python3 "$TOOLS/pck_web_extensions.py" "$DEST/build/web/index.pck"
for PK in $(python3 -c "import json;print(' '.join(json.load(open('$DEST/kc2/bundle/BUNDLE_STAMP.json'))['kit_packs']))"); do
  "$GODOT" --headless --path "$DEST" --export-pack "${PK%.pck}" "$DEST/build/web/$PK" >> "$LOG/export.log" 2>&1 \
    || { tail -30 "$LOG/export.log" >&2; exit 5; }
done

echo "== 3d split oversized data packs without changing payload bytes"
python3 "$TOOLS/arena_split_web_packs.py" "$DEST" | tee "$LOG/pack_split.log"
# The main pack embeds the final mount list after oversized packs are split.
"$GODOT" --headless --path "$DEST" --export-release "WebArena" "$DEST/build/web/index.html" >> "$LOG/export.log" 2>&1
python3 "$TOOLS/pck_web_extensions.py" "$DEST/build/web/index.pck"

cp "$(dirname "$SRC")/audio_review/derived_sfx/HERO_SFX_REVIEW.html" "$DEST/build/web/hero-sfx.html"

echo "== 4 fence"
ls -la "$DEST/build/web" | tee "$LOG/files.txt"
BIG=$(find "$DEST/build/web" -type f -size +${MAX_FILE_MB}M | wc -l | tr -d ' ')
[ "$BIG" = "0" ] || { echo "FENCE: a file at or over $MAX_FILE_MB MB" >&2; exit 6; }
grep -q 'base href="/playtest/barrow-arena/"' "$DEST/build/web/index.html" || { echo "FENCE: base href" >&2; exit 6; }
echo "== 4b isolated pack-order and byte-identity probe (no loose project files)"
python3 "$TOOLS/arena_web_payload_audit.py" "$DEST" | tee "$LOG/payload_audit.log"
ISOLATED=$(mktemp -d "${TMPDIR:-/tmp}/barrow-arena-probe.XXXXXX")
"$GODOT" --headless --path "$ISOLATED" --main-pack "$DEST/build/web/index.pck" \
  --script "$TOOLS/arena_pack_order_probe.gd" -- --as-web --pack-dir "$DEST/build/web" \
  > "$LOG/pack_probe.log" 2>&1 || { cat "$LOG/pack_probe.log" >&2; exit 7; }
grep -q 'PACK_ORDER: PASS' "$LOG/pack_probe.log" || { cat "$LOG/pack_probe.log" >&2; exit 7; }
echo "== 4c actual WebAssembly browser smoke tests"
SMOKE_ROOT=$(mktemp -d "${TMPDIR:-/tmp}/barrow-arena-web.XXXXXX")
mkdir -p "$SMOKE_ROOT/playtest"
ln -s "$DEST/build/web" "$SMOKE_ROOT/playtest/barrow-arena"
SMOKE_PORT=${ARENA_SMOKE_PORT:-8796}
node "$TOOLS/web_br_server.js" "$SMOKE_ROOT" "$SMOKE_PORT" > "$LOG/smoke_server.log" 2>&1 &
SMOKE_PID=$!
trap 'kill "$SMOKE_PID" 2>/dev/null || true' EXIT
for MODE in desktop --touch --fail-pack; do
  node "$TOOLS/web_arena_test.cjs" "http://127.0.0.1:$SMOKE_PORT/playtest/barrow-arena/" "$LOG/browser-${MODE#--}" "$MODE" \
    > "$LOG/browser-${MODE#--}.log" 2>&1 || { tail -30 "$LOG/browser-${MODE#--}.log" >&2; exit 7; }
done
if [ "$NO_STAGE" = "1" ]; then echo "built (not staged): $DEST/build/web"; exit 0; fi
echo "== 5 stage -> $STAGE (no commit, no push)"
mkdir -p "$STAGE"
rsync -a --delete "$DEST/build/web/" "$STAGE/"
du -sh "$STAGE"
