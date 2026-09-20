#!/bin/zsh
# C-6 conductor Grok still WITH a reference image (identity carry attempt): grok_image_ref.sh <name> <ref png> "<prompt>"
B=/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst
NAME=$1; REF=$2; PROMPT=$3; WORK="$HOME/astra-burst/grok/C-8/$NAME"; mkdir -p "$WORK"; cd "$WORK"; T0=$(date +%s)
~/.grok/bin/grok -p "Use your image generation / image editing tool ONCE, giving it this reference image as input: $REF . Prompt: \"$PROMPT\". If your tool cannot take an input image, say REF_UNSUPPORTED on its own line and then generate from the prompt alone. When it returns, save/copy the resulting image into the current directory as $NAME.png (download it if the tool returns a URL), then print exactly one line: SAVED <absolute path> <size in bytes>. Do nothing else; one image only; no video." --always-approve > "$WORK/grok_stdout.txt" 2>&1
RC=$?; T1=$(date +%s); f="$WORK/$NAME.png"; if [ -f "$f" ]; then OK=true; SHA=$(shasum -a 256 "$f" | cut -c1-64); else OK=false; SHA=""; fi
REFUSED=$(grep -c REF_UNSUPPORTED "$WORK/grok_stdout.txt")
python3 -c "import json,subprocess,sys,hashlib;subprocess.run(['python3','$B/runs/C-8/conductor_scripts/cl.py','grok_calls',json.dumps(dict(id='GI-$NAME',kind='image_gen_ref',cell='$NAME',ok=('$OK'=='true'),rc=$RC,wall_s=$((T1-T0)),image='$f',image_sha256='$SHA',ref='$REF',ref_unsupported=int('$REFUSED'),prompt_sha256=hashlib.sha256(sys.argv[1].encode()).hexdigest()))],check=True,stdout=subprocess.DEVNULL)" "$PROMPT"
echo "$(date -u +%FT%TZ) IMAGE $NAME ok=$OK rc=$RC wall=$((T1-T0))s ref_unsupported=$REFUSED"
