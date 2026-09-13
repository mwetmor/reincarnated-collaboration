# Fold staged Grok clips into the run (ONLY between TOOLING bursts): copy MP4 → runs/C-3/xvideo/in, append grok_calls to the ledger.
import json, shutil, subprocess, pathlib, hashlib
S = pathlib.Path('/private/tmp/claude-501/-Users-admin-Games-reincarnated-collaboration/423f7949-3b86-43e3-82bd-845c71630541/scratchpad')
B = pathlib.Path('/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst'); st = S/'grok_stage.jsonl'; done = S/'grok_folded.jsonl'
if not st.exists(): print('nothing staged'); raise SystemExit
snap = st.with_suffix('.folding'); st.rename(snap)
lines = [l for l in snap.read_text().splitlines() if l.strip()]; n = 0
for l in lines:
    e = json.loads(l)
    if e['ok']:
        src = pathlib.Path(e['staged_mp4']); dst = B/e['clip']; dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dst); assert hashlib.sha256(dst.read_bytes()).hexdigest() == e['clip_sha256']
    subprocess.run(['python3', str(S/'cl.py'), 'grok_calls', json.dumps(e)], check=True, capture_output=True); n += 1
    with done.open('a') as d: d.write(l + '\n')
snap.unlink(); print('folded', n)
