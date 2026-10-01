import sys, json, re, collections
sys.path.insert(0,"/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/research/2026-10-01-crucible-spawn-p05/tools")
import arz_stack_edition_IV as A
idx=A.index()
def rd(p):
    r,k=A.read(p); return r,k
rows=[]
proxies=sorted(k for k in idx if k.startswith('records/proxies/tier16waves/'))
mon2src=collections.defaultdict(set)
for p in proxies:
    r,_=rd(p)
    m=re.search(r'_w(\d+)_p(\d+)',p); w,pt=m.group(1),m.group(2)
    for kk,v in r.items():
        if re.fullmatch(r'pool\d+',kk) and v:
            pool,_=rd(v)
            for k2,v2 in pool.items():
                if re.fullmatch(r'name(Champion)?\d+',k2) and v2:
                    mon2src[v2.lower()].add((r['Class'],'w'+w+'p'+pt))
out=[]
for mpath in sorted(mon2src):
    r,k=rd(mpath)
    if r is None: out.append({'monster':mpath,'MISSING':True}); continue
    ctrl=r.get('controller',''); cr,_=rd(ctrl) if ctrl else (None,None)
    anm=r.get('charAnimationTableName',''); ar,_=rd(anm) if anm else (None,None)
    spawnanims={a:b for a,b in (ar or {}).items() if re.search(r'(Spawn|Respawn)Anim$',a) and b}
    out.append(dict(monster=mpath, archive=k, classes=sorted({c for c,_ in mon2src[mpath]}), seats=sorted({s for _,s in mon2src[mpath]}),
      Class=r.get('Class'), classification=r.get('monsterClassification'),
      ambushDissolveTime=r.get('ambushDissolveTime',0), ambushDissolveTexture=r.get('ambushDissolveTexture'),
      startVisible=r.get('startVisible'), spawnEffect=r.get('spawnEffect',''), prespawnEffect=r.get('prespawnEffect',''), spawnSoundEffect=r.get('spawnSoundEffect',''),
      hiddenFromCombat=r.get('hiddenFromCombat'),
      controller=ctrl, controllerClass=(cr or {}).get('Class'), controllerTpl=(cr or {}).get('templateName'),
      anm=anm, spawnanims=spawnanims, runSpeed=r.get('characterRunSpeed'), disallowRotation=r.get('disallowRotation')))
json.dump(out,open(sys.argv[1],'w'),indent=1,default=str)
for o in out:
    print(o['monster'].split('/')[-1], o.get('classes'), o.get('seats') if 'ProxyAmbush' in o.get('classes',[]) else '', 'dissT=',o.get('ambushDissolveTime'),'vis=',o.get('startVisible'),'spEff=',o.get('spawnEffect'),'pre=',o.get('prespawnEffect'),'ctrl=',o.get('controllerClass'), 'spawnanims=',list(o.get('spawnanims',{}).items())[:3])
