#!/bin/bash
# Build ONE character's Godot web export for the three-pck cliffside trio.
#
# drax, 2026-09-21. Derived from ~/Games/reincarnated-godot/web/build_playtest.sh,
# which stays READ-ONLY this session (brief constraint) -- this driver reuses that
# repo's _overlay/ scripts in place and writes only under runs/C-8/web/.
#
# usage: build_char.sh <source_godot_project_dir> <char>
#   char in {warlord, keeper, necro}; all three build against route "cliffside"
#   so every shell carries the same <base href="/playtest/cliffside/">.
#
# Differences from build_playtest.sh, and why:
#   * DEST is runs/C-8/web/stage-<char>/ (reincarnated-godot is read-only here).
#   * A SECOND lossy pass (lossy_sprites.py) drops the texture threshold from
#     2048 px to 512 px. The overlay's 2048 threshold covers the parallax plates
#     and ground tiles but MISSES the character sprites entirely -- 544 frames at
#     512x512 RGBA = 39.1 MB of the warlord project, every byte of it lossless.
#     That is the single largest term in the pck and it is per-character, which is
#     exactly the term the three-pck split exists to isolate.
#   * No staging step: assemble_trio.py stages one engine + three pcks.
set -euo pipefail

SRC=${1:?usage: build_char.sh <source_godot_project_dir> <char>}
CHAR=${2:?usage: build_char.sh <source_godot_project_dir> <char>}
ROUTE=cliffside
GODOT=${GODOT:-/Applications/Godot.app/Contents/MacOS/Godot}
WEB=$(cd "$(dirname "$0")" && pwd)
OVERLAY=${OVERLAY:-$HOME/Games/reincarnated-godot/web/_overlay}
DEST=$WEB/stage-$CHAR
LOG=$DEST/build/logs
SRC=$(cd "$SRC" && pwd)

[ -f "$SRC/project.godot" ] || { echo "no project.godot in $SRC" >&2; exit 2; }
[ -f "$OVERLAY/apply_overlay.py" ] || { echo "no overlay at $OVERLAY" >&2; exit 2; }
case "$DEST" in "$SRC"*) echo "refusing: destination inside source" >&2; exit 2;; esac

echo "== [$CHAR] mirror $SRC -> $DEST"
mkdir -p "$DEST"
rsync -a --delete \
  --exclude '.godot/' --exclude 'build/' --exclude '.gitignore' \
  --exclude '*.import' --exclude '*.uid' \
  --exclude 'export_presets.cfg' --exclude 'scripts/touch_controls.gd' \
  "$SRC"/ "$DEST"/
mkdir -p "$LOG"

echo "== [$CHAR] overlay (pass 1)"
OVERLAY_OUT=$(python3 -B "$OVERLAY/apply_overlay.py" "$DEST" "$ROUTE")
echo "$OVERLAY_OUT" | grep -v '^lossy WebP' || true

echo "== [$CHAR] import (pass 1)"
"$GODOT" --headless --path "$DEST" --import > "$LOG/import.log" 2>&1

# The overlay only writes lossy flags where a .import already exists; a fresh
# mirror has none, so it reports NEEDS_IMPORT and the flags land on this pass.
echo "== [$CHAR] overlay (pass 2) + sprite lossy pass"
python3 -B "$OVERLAY/apply_overlay.py" "$DEST" "$ROUTE" | grep -c '^lossy WebP' \
  | sed "s/^/  overlay lossy (>=2048px): /"
python3 -B "$WEB/lossy_sprites.py" "$DEST"

# Held WHIRLWIND touch button. Gated on the project declaring an `attack`
# action, so it is STRUCTURALLY impossible to add to the Keeper/Necromancer
# builds -- their F does nothing because the action does not exist, and a dead
# button would read as a bug rather than as an absence. Must run AFTER the
# overlay's second pass, which rewrites scripts/touch_controls.gd from source.
python3 -B "$WEB/whirlwind_button_patch.py" "$DEST"

echo "== [$CHAR] import (pass 2)"
"$GODOT" --headless --path "$DEST" --import > "$LOG/import2.log" 2>&1

echo "== [$CHAR] export Web"
mkdir -p "$DEST/build/web"
"$GODOT" --headless --path "$DEST" --export-release "Web" build/web/index.html > "$LOG/export.log" 2>&1

# --- fences, carried over verbatim in intent from build_playtest.sh ---
grep -q "GODOT_THREADS_ENABLED = false" "$DEST/build/web/index.html" \
  || { echo "threads not OFF -- would require COOP/COEP" >&2; exit 3; }
grep -q "<base href=\"/playtest/$ROUTE/\">" "$DEST/build/web/index.html" \
  || { echo "base href missing" >&2; exit 3; }
if grep -a -o -i -E "vfx_(frost|fire|lightning|arcane|holy|poison)_(bolt|impact)[^A-Za-z0-9_]|vfx/(frost|fire|lightning|arcane|holy|poison)/|creativekind|gigapack|untied ?games" \
     "$DEST/build/web/index.pck" | head -1 | grep -q .; then
  echo "license fence: forbidden name inside index.pck" >&2; exit 3
fi
DANGLING=0
while IFS= read -r res; do
  [ -f "$DEST/${res#res://}" ] || { echo "dangling resource in index.pck: $res" >&2; DANGLING=1; }
done < <(grep -a -o "res://[A-Za-z0-9_./-]*\.gdshader" "$DEST/build/web/index.pck" | sort -u)
[ "$DANGLING" -eq 0 ] || { echo "export references resources not in the project" >&2; exit 3; }

echo "== [$CHAR] sizes (bytes):"
ls -l "$DEST/build/web" | awk 'NR>1 {printf "  %12d  %s\n", $5, $9}'
echo "== [$CHAR] done"
