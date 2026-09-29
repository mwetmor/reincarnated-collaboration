# R-C9-70 item 4 (+ KC2 conductor OK: harness_logs all; tmp/ except tmp/kc2/): manifest of deletable frame dumps.
# Candidate = untracked PNG (or its Godot .import sibling) inside a first-level folder that ALSO holds a video (mp4/avi/gif/webm),
# and whose filename is not cited by any .md/.json/.txt/.gd in the collaboration or godot repos. Everything else is kept.
import os, json, subprocess, re, sys, time
G='/Users/admin/Games/reincarnated-godot'; C='/Users/admin/Games/reincarnated-collaboration'
tracked=set(subprocess.run(['git','-C',G,'ls-files','harness_logs','tmp'],capture_output=True,text=True).stdout.split('\n'))
# cited basenames
cited=set()
for repo in (C,G):
    r=subprocess.run(['grep','-rhoE','--include=*.md','--include=*.json','--include=*.txt','--include=*.gd',r'(harness_logs|tmp)/[^ "\x27)]+\.png',repo],capture_output=True,text=True)
    for m in r.stdout.split('\n'):
        if m: cited.add(os.path.basename(m))
VID=('.mp4','.avi','.gif','.webm','.mov')
man={'generated':time.strftime('%Y-%m-%dT%H:%M:%S'),'rule':'untracked PNG frame dumps (+ .import siblings) in first-level folders that also keep a video; cited filenames kept; tmp/kc2 excluded (KC2 conductor)','cited_basenames':len(cited),'folders':[],'delete':[]}
tot=0
for root in ('harness_logs','tmp'):
    for top in sorted(os.listdir(os.path.join(G,root))):
        tp=os.path.join(G,root,top)
        if not os.path.isdir(tp) or (root=='tmp' and top=='kc2'): continue
        files=[os.path.join(d,f) for d,_,fs in os.walk(tp) for f in fs]
        has_vid=any(f.lower().endswith(VID) for f in files)
        dele=[]; keepb=0
        for f in files:
            rel=os.path.relpath(f,G); low=f.lower()
            try: s=os.path.getsize(f) if not os.path.islink(f) else 0
            except OSError: continue
            is_png=low.endswith('.png'); is_imp=low.endswith('.png.import')
            base=os.path.basename(f[:-7] if is_imp else f)
            if has_vid and (is_png or is_imp) and rel not in tracked and base not in cited: dele.append([f,s])
            else: keepb+=s
        db=sum(s for _,s in dele); tot+=db
        man['folders'].append(dict(path=tp,has_video=has_vid,delete_count=len(dele),delete_bytes=db,keep_bytes=keepb))
        man['delete']+=dele
man['total_delete_bytes']=tot
json.dump(man,open('manifest_godot_frames.json','w'))
print('delete %.2f GB in %d files; folders with video %d / %d; cited basenames %d'%(tot/1e9,len(man['delete']),sum(f['has_video'] for f in man['folders']),len(man['folders']),len(cited)))
for f in sorted(man['folders'],key=lambda x:-x['delete_bytes'])[:12]: print('  %6.2fG del  %6.2fG keep  vid=%s  %s'%(f['delete_bytes']/1e9,f['keep_bytes']/1e9,f['has_video'],f['path'].replace(G+'/','')))
