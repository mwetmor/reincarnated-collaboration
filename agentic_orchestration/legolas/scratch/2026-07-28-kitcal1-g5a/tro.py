import importlib.util
spec = importlib.util.spec_from_file_location("g5a", "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/scratch/2026-07-28-kitcal1-g5a/g5a_resolve.py")
R = importlib.util.module_from_spec(spec); spec.loader.exec_module(R)
T=R.tags()
PAK=R.pak_vals(); PL=PAK["characterLifeModifier"]
def terms(p,cl):
    m=R.rec(p); b=R.rec(m["characterAttributeEquations"])
    L=R.evaleq(b["characterLife"],cl); s=0.0;f=0.0;src=[]
    for i in range(1,13):
        sn=m.get(f"skillName{i}"); sl=m.get(f"skillLevel{i}")
        if not sn: continue
        rk=R.evaleq(sl,cl) if isinstance(sl,str) else sl
        rk=0 if rk is None else int(rk)
        if rk<1 or not R.has(sn): continue
        sk=R.rec(sn)
        if sk.get("Class")!="Skill_Passive": continue
        v=R.arr(sk.get("characterLifeModifier"),rk)
        if isinstance(v,(int,float)) and v: s+=v; src.append((sn.split('/')[-1],rk,v))
        v2=R.arr(sk.get("characterLife"),rk)
        if isinstance(v2,(int,float)) and v2: f+=v2
    return m,L,s,f,src
for p in ["records/creatures/enemies/trollhalfswamp_a02.dbr","records/creatures/enemies/trollhalfswamp_b02.dbr",
          "records/creatures/enemies/trollhalfswamp_a01.dbr","records/creatures/enemies/trollhalfswamp_b01.dbr",
          "records/creatures/enemies/slitha_melee_b01.dbr","records/creatures/enemies/slitha_shaman_c01.dbr",
          "records/creatures/enemies/slitha_melee_a01.dbr"]:
    try: m,L,s,f,src=terms(p,11)
    except KeyError: print("MISSING",p); continue
    print(f"{p.split('/')[-1]:32s} {str(T.get(m.get('description'),'')):26s} {m.get('monsterClassification'):9s} cle={m.get('charLevel')}")
    for cl in (9,10,11,12,13):
        m,L,s,f,src=terms(p,cl)
        print(f"    cl{cl}: bio={L:.1f} smod={s} add50={(L+f)*(1+(s+50)/100):.2f} add35={(L+f)*(1+(s+35)/100):.2f}")
