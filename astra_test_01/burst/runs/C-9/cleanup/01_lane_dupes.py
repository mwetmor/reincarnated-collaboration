# R-C9-70 cleanup item 1: lane burst workspaces of CLOSED runs (~/astra-burst/runs/C-5, C-6, C-7).
# Classify every file: DUP (sha256 identical to a file inside the repo's astra_test_01/burst tree), CACHE (Godot import cache:
# anything under a .godot/ dir, or *.ctex / *.md5), KEEP (unique: event logs, briefs, references, any unmatched output).
# Writes a manifest; deletes NOTHING.
import hashlib, json, os, pathlib, sys, time
REPO=pathlib.Path('/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst'); LANE=pathlib.Path.home()/'astra-burst/runs'
RUNS=['C-5','C-6','C-7']
def sha(p,b=1<<20):
    h=hashlib.sha256()
    with open(p,'rb') as f:
        for c in iter(lambda:f.read(b),b''): h.update(c)
    return h.hexdigest()
t0=time.time(); sizes={}
lane=[p for r in RUNS for p in (LANE/r).rglob('*') if p.is_file()]
for p in lane: sizes.setdefault(p.stat().st_size,[]).append(p)
# hash repo files only when a lane file has the same size (cheap prefilter)
repo_hash={}
for p in REPO.rglob('*'):
    try:
        if p.is_file() and p.stat().st_size in sizes and '.git' not in p.parts: repo_hash.setdefault(sha(p),str(p))
    except OSError: pass
man={'generated':time.strftime('%Y-%m-%dT%H:%M:%S'),'runs':RUNS,'rule':'DUP = sha256 identical to a repo file; CACHE = Godot import cache (regenerable); KEEP = everything else','files':[]}
tot={'DUP':0,'CACHE':0,'KEEP':0}; cnt={'DUP':0,'CACHE':0,'KEEP':0}
for p in lane:
    s=p.stat().st_size; cls='KEEP'; ref=None
    if '.godot' in p.parts or p.suffix in ('.ctex','.md5'): cls='CACHE'
    else:
        h=sha(p) if s>0 else None
        if h and h in repo_hash: cls,ref='DUP',repo_hash[h]
    tot[cls]+=s; cnt[cls]+=1; man['files'].append([str(p),s,cls,ref])
man['totals_bytes']=tot; man['counts']=cnt
json.dump(man,open('lane_dupes_manifest.json','w'))
print({k:'%.2f GB / %d files'%(tot[k]/1e9,cnt[k]) for k in tot},'%.0fs'%(time.time()-t0))
