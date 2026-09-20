#!/bin/zsh
# C-6 conductor Grok still (E1 probe): grok_image.sh <name> "<prompt>"  → ~/astra-burst/grok/C-6/<name>/<name>.png, ledgered in grok_calls
B=/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst
NAME=$1; PROMPT=$2; WORK="$HOME/astra-burst/grok/C-6/$NAME"; rm -rf "$WORK"; mkdir -p "$WORK"; cd "$WORK"; T0=$(date +%s)
~/.grok/bin/grok -p "Use your image generation tool ONCE with this exact prompt: \"$PROMPT\". When it returns, save/copy the resulting image into the current directory as $NAME.png (download it if the tool returns a URL), then print exactly one line: SAVED <absolute path> <size in bytes>. Do nothing else; do not generate a second image; do not make a video." --always-approve > "$WORK/grok_stdout.txt" 2>&1
RC=$?; T1=$(date +%s); f=$(find "$WORK" -maxdepth 1 -type f \( -name "*.png" -o -name "*.jpg" -o -name "*.jpeg" -o -name "*.webp" \) | head -1)
if [ -n "$f" ]; then OK=true; SHA=$(shasum -a 256 "$f" | cut -c1-64); else OK=false; SHA=""; fi
python3 -c "import json,subprocess,sys;subprocess.run(['python3','$B/runs/C-6/conductor_scripts/cl.py','grok_calls',json.dumps(dict(id='GI-$NAME',kind='image_gen',cell='$NAME',ok=('$OK'=='true'),rc=$RC,wall_s=$((T1-T0)),image='$f',image_sha256='$SHA',prompt_sha256=__import__('hashlib').sha256(sys.argv[1].encode()).hexdigest()))],check=True,stdout=subprocess.DEVNULL)" "$PROMPT"
echo "$(date -u +%FT%TZ) IMAGE $NAME ok=$OK rc=$RC wall=$((T1-T0))s file=$f"
