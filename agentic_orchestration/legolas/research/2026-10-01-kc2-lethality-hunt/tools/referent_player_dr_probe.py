"""legolas lethality hunt: scan the referent's allocated skill/devotion chains + equipped items for
player-side damage-reduction-class fields. READ-ONLY (save parse via S-1 gdcg7, records via S-1 arz)."""
import sys, re, json
S1='/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/scratch/2026-09-21-s1-bio'
sys.path.insert(0,S1)
import os; os.chdir(S1)
import gdcg7 as G, arz
SAVE="/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/scratch/2026-08-05-eorwarlguts-parse/player.gdc"
PAT=re.compile(r'(?i)racial|absorp|reduction|defensiveTotal|protection|damagetaken|DamageMult|defensiveReflect')
res=G.parse(SAVE)
out=[]
def take(label, rec, rank=None):
    a,d=arz.find(rec)
    if d is None: out.append((label,rec,rank,'NOT-FOUND',{})); return None
    hits={}
    for k,v in d.items():
        if not PAT.search(k): continue
        if isinstance(v,list):
            if not v: continue
            vv = v[min(rank,len(v))-1] if rank else v
        else: vv=v
        if vv in (0,0.0,'','0',None) or (isinstance(vv,list) and not any(vv)): continue
        hits[k]=vv
    out.append((label,rec,rank,a,hits)); return d
CHAIN=("buffSkillName","petSkillName","skillName","modifierSkillName","passiveSkillName")
seen=set()
def walk(label, rec, rank, depth=0):
    if (rec,rank) in seen or depth>3: return
    seen.add((rec,rank)); d=take(label+('' if depth==0 else f' >{depth}'),rec,rank)
    if not d: return
    for c in CHAIN:
        n=d.get(c)
        if isinstance(n,str) and n.endswith('.dbr'): walk(label,n,rank,depth+1)
for s in res["blocks"]["character_skills"]["skills"]:
    r=s.get("level") or 0
    if r<=0: continue
    walk(("DEVOTION" if "/devotion/" in s["name"] else "SKILL")+f" r{r}", s["name"], r)
inv=res["blocks"]["inventory"]
for grp in ("equipment","weapon1","weapon2"):
    for it in inv.get(grp,[]):
        if not it.get("baseName"): continue
        take(f"ITEM[{grp}]", it["baseName"])
        for f in ("prefixName","suffixName","modifierName","transmuteName","componentName","augmentName","relicBonus"):
            x=it.get(f)
            if x: take(f"ITEM[{grp}].{f}", x)
n=0
for label,rec,rank,a,h in out:
    if h: n+=1; print(label, rank, rec.replace('records/',''), json.dumps(h))
print('records scanned', len(out), 'with hits', n, 'not found', sum(1 for o in out if o[3]=='NOT-FOUND'))
