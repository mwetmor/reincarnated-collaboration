# Executes the committed manifests with re-verification at deletion time. Lane DUP: the repo copy must still exist with the same
# sha256; CACHE: delete; KEEP: never. Godot frames: file must exist, be untracked, and match the manifest size. Logs every action.
import json, os, hashlib, subprocess, time, sys
def sha(p,b=1<<20):
    h=hashlib.sha256()
    with open(p,'rb') as f:
        for c in iter(lambda:f.read(b),b''): h.update(c)
    return h.hexdigest()
log=open('deletions.log','a'); freed=0; n=0; skipped=0
L=json.load(open('lane_dupes_manifest.json'))
for p,s,cls,ref in L['files']:
    if cls=='KEEP' or not os.path.isfile(p): continue
    if cls=='DUP':
        if not (ref and os.path.isfile(ref) and os.path.getsize(ref)==s and sha(ref)==sha(p)): skipped+=1; log.write(f'SKIP-noverify\t{p}\n'); continue
    os.remove(p); freed+=s; n+=1; log.write(f'DEL-{cls}\t{s}\t{p}\n')
G='/Users/admin/Games/reincarnated-godot'
tracked=set(subprocess.run(['git','-C',G,'ls-files','harness_logs','tmp'],capture_output=True,text=True).stdout.split('\n'))
M=json.load(open('manifest_godot_frames.json'))
for p,s in M['delete']:
    rel=os.path.relpath(p,G)
    if rel in tracked or not os.path.isfile(p) or os.path.getsize(p)!=s or '/tmp/kc2/' in p: skipped+=1; log.write(f'SKIP\t{p}\n'); continue
    os.remove(p); freed+=s; n+=1; log.write(f'DEL-GODOTFRAME\t{s}\t{p}\n')
# prune now-empty dirs under the touched roots only
for root in [os.path.expanduser('~/astra-burst/runs/'+r) for r in ('C-5','C-6','C-7')]+[G+'/tmp',G+'/harness_logs']:
    for d,_,_ in sorted(os.walk(root),key=lambda x:-len(x[0])):
        if d!=root and not os.listdir(d) and '/tmp/kc2' not in d: os.rmdir(d)
log.close(); print('deleted %d files, %.2f GB; skipped %d'%(n,freed/1e9,skipped))
