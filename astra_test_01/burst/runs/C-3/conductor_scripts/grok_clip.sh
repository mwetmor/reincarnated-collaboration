#!/bin/zsh
# Run C-3 conductor Grok i2v clip (C-2 shape): grok_clip.sh <cell e.g. S_idle> <still png> [suffix]
B=/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst
S=/private/tmp/claude-501/-Users-admin-Games-reincarnated-collaboration/423f7949-3b86-43e3-82bd-845c71630541/scratchpad
CELL=$1; STILL=$2; SUF=${3:-}
NAME="${CELL}${SUF}"
PROMPT=$(python3 -c "import json,sys;print(json.load(open('$B/runs/C-3/matrix_prompts.json'))['cells']['$CELL']['prompt'])")
[ -n "$4" ] && PROMPT="$PROMPT $4"
OUTDIR="$B/runs/C-3/xvideo/in"; mkdir -p "$OUTDIR"; WORK="$HOME/astra-burst/grok/C-3/$NAME"; rm -rf "$WORK"; mkdir -p "$WORK"
cd "$WORK"; T0=$(date +%s)
~/.grok/bin/grok -p "Use your image_to_video tool ONCE with these exact arguments: image = $STILL (this still is the FIRST frame), prompt = \"$PROMPT\", duration = 6, resolution = 720p. When it returns, save/copy the resulting MP4 into the current directory as $NAME.mp4 (download it if the tool returns a URL), then print exactly one line: SAVED <absolute path> <size in bytes> <costUSD if reported>. Do nothing else; do not edit the image; do not generate a second video." --always-approve > "$WORK/grok_stdout.txt" 2>&1
RC=$?; T1=$(date +%s)
f=$(ls "$WORK"/*.mp4 2>/dev/null | head -1)
if [ -n "$f" ]; then
  [ "$STAGE" != "1" ] && cp "$f" "$OUTDIR/$NAME.mp4"
  PROBE=$(/opt/homebrew/bin/ffprobe -v error -select_streams v:0 -show_entries stream=width,height,r_frame_rate,nb_frames,duration -of csv=p=0 "$f")
  CSHA=$(shasum -a 256 "$f" | cut -c1-64); OK=true
else PROBE=""; CSHA=""; OK=false; fi
LINE=$(grep -E '^SAVED|cost|Cost' "$WORK/grok_stdout.txt" | tail -2 | tr '\n' ' ' | tr '"' "'" | cut -c1-300)
PSHA=$(printf '%s' "$PROMPT" | shasum -a 256 | cut -c1-64); SSHA=$(shasum -a 256 "$STILL" | cut -c1-64)
ENTRY="{\"id\":\"G-$NAME\",\"cell\":\"$CELL\",\"still\":\"$STILL\",\"still_sha256\":\"$SSHA\",\"prompt_sha256\":\"$PSHA\",\"extra\":\"$4\",\"clip\":\"runs/C-3/xvideo/in/$NAME.mp4\",\"clip_sha256\":\"$CSHA\",\"ok\":$OK,\"rc\":$RC,\"wall_s\":$((T1-T0)),\"probe\":\"$PROBE\",\"printed\":\"$LINE\",\"staged_mp4\":\"$f\"}"
if [ "$STAGE" = "1" ]; then echo "$ENTRY" >> $S/grok_stage.jsonl; else python3 $S/cl.py grok_calls "$ENTRY" > /dev/null; fi
echo "$(date -u +%FT%TZ) CLIP $NAME ok=$OK rc=$RC wall=$((T1-T0))s probe=$PROBE"
