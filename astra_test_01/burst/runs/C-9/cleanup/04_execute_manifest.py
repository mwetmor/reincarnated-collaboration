# Execute an audited manifest (R-C9-70) with re-verification at deletion time: the file must exist, match the manifest size,
# be UNTRACKED in the collaboration repo, and not be a kept type (video/JSON/MD/TXT/log/script/archive). Logs every action.
import json, os, subprocess, sys
man, label = sys.argv[1], sys.argv[2]
REPO='/Users/admin/Games/reincarnated-collaboration'
M=json.load(open(man)); items=M['delete']
roots=sorted({os.path.relpath(os.path.dirname(p),REPO) for p,_ in items})
tracked=set()
for i in range(0,len(roots),200):
    tracked|=set(subprocess.run(['git','-C',REPO,'ls-files','--',*roots[i:i+200]],capture_output=True,text=True).stdout.split('\n'))
KEEP=('.mp4','.webm','.gif','.mov','.avi','.json','.md','.txt','.log','.py','.gd','.sh','.zip','.tscn','.tres')
log=open(f'deletions_{label}.log','a'); freed=n=skip=0
for p,s in items:
    rel=os.path.relpath(p,REPO)
    if rel in tracked or not os.path.isfile(p) or os.path.islink(p) or os.path.getsize(p)!=s or p.lower().endswith(KEEP):
        skip+=1; log.write(f'SKIP\t{p}\n'); continue
    os.remove(p); freed+=s; n+=1; log.write(f'DEL\t{s}\t{p}\n')
for r in {os.path.join(REPO,x) for x in roots}:
    for d,_,_ in sorted(os.walk(r),key=lambda x:-len(x[0])):
        try:
            if not os.listdir(d): os.rmdir(d)
        except OSError: pass
log.close(); print(f'{label}: deleted {n} files, {freed/1e9:.2f} GB; skipped {skip}')
