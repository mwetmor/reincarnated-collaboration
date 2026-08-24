"""Harvest glyph templates from eor-test-2 using Lap K's certified values as labels."""
import csv, numpy as np, pickle, collections
from d4_ocr import stream, mask_of, boxes, norm, FPS
V2='/Volumes/reincarnated/visual-artifacts/GD-matt-test/eor-test-2/video/eor-warlord-wave-150-160-2026-08-05 21-37-25.mp4'
LAPK='/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/notes/2026-08-14-kc2-pm4-lap-k-death-anchor/pm4k_full_trace.csv'
lab={}
for r in csv.DictReader(open(LAPK)):
    if r['hp_cur'] and r['hp_max']:
        lab[round(float(r['t_s'])*FPS)] = f"{int(r['hp_cur'])}/{int(r['hp_max'])}"
print('labelled frames available:', len(lab))
acc=collections.defaultdict(list); used=0; seen=0
for i,img in stream(V2, 675.0, 885.0):
    f = round(675.0*FPS)+i
    s = lab.get(f)
    seen+=1
    if not s: continue
    bs = boxes(mask_of(img))
    if len(bs)!=len(s): continue
    m = mask_of(img)
    ok=True; tmp=[]
    for (a,b),ch in zip(bs,s):
        if a==0 or b>=img.shape[1]: ok=False; break
        v=norm(m[:,a:b])
        if v is None: ok=False; break
        tmp.append((ch,v))
    if not ok: continue
    for ch,v in tmp: acc[ch].append(v)
    used+=1
print(f'frames streamed {seen}, frames contributing templates {used}')
tpl={}; wid={}
for ch,vs in acc.items():
    A=np.stack(vs)
    med=np.median(A,0); med=med-med.mean(); med/=np.linalg.norm(med)
    tpl[ch]=med
    print(f'  {ch!r}: n={len(vs)}')
pickle.dump(tpl, open('d4_templates.pkl','wb'))
print('saved d4_templates.pkl chars:', sorted(tpl))
