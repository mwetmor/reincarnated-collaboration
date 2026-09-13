# Conductor orchestrator: repeatedly stage+brief ready chunk/layer panels and run waves (≤6); stop on any non-zero burst exit.
import subprocess, json, pathlib, time, sys
S='/private/tmp/claude-501/-Users-admin-Games-reincarnated-collaboration/423f7949-3b86-43e3-82bd-845c71630541/scratchpad'
B='/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst'
log=open(S+'/autopaint.log','a')
def run(*a): return subprocess.run(list(a), capture_output=True, text=True, cwd=B)
wave=0
while True:
    ch=run('python3', S+'/grid_paint.py', 'ready').stdout.split()
    la=run('python3', S+'/layer_paint.py', 'ready').stdout.split()
    items=[('chunk',k) for k in ch]+[('layer',i) for i in la]
    if not items:
        log.write(time.strftime('%H:%M:%S')+' ALL DONE\n'); log.flush(); break
    items=items[:6]; specs=[]
    for kind,x in items:
        if kind=='chunk':
            run('python3', S+'/grid_paint.py', 'stage', x); r=run('python3', S+'/grid_paint.py', 'brief', x); specs.append(f'CS-v3-{x}:GENERATE')
        else:
            run('python3', S+'/layer_paint.py', 'stage', x); r=run('python3', S+'/layer_paint.py', 'brief', x); specs.append(f'{x}:GENERATE')
        if r.returncode: log.write(f'BRIEF FAIL {x} {r.stderr[-300:]}\n'); log.flush(); sys.exit(1)
    wave+=1; log.write(time.strftime('%H:%M:%S')+f' wave {wave}: {specs}\n'); log.flush()
    subprocess.run([S+'/wave.sh', f'ap{wave}']+specs)
    bad=[]
    for sp in specs:
        bid=sp.split(':')[0]
        try: ex=json.load(open(f'{S}/{bid}_run.json'))['exit']
        except Exception as e: ex=f'unreadable {e}'
        if ex!=0: bad.append((bid,ex))
    if bad:
        log.write(time.strftime('%H:%M:%S')+f' STOP: non-zero exits {bad}\n'); log.flush(); sys.exit(2)
