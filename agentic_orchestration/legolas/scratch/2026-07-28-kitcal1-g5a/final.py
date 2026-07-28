import importlib.util, json
spec = importlib.util.spec_from_file_location("g5a", "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/scratch/2026-07-28-kitcal1-g5a/g5a_resolve.py")
R = importlib.util.module_from_spec(spec); spec.loader.exec_module(R)
T=R.tags()
def hp(p,cl,pak):
    m=R.rec(p); b=R.rec(m["characterAttributeEquations"])
    L=R.evaleq(b["characterLife"],cl); s=0.0;f=0.0
    for i in range(1,13):
        sn=m.get(f"skillName{i}"); sl=m.get(f"skillLevel{i}")
        if not sn or not R.has(sn): continue
        rk=R.evaleq(sl,cl) if isinstance(sl,str) else sl
        rk=0 if rk is None else int(rk)
        if rk<1: continue
        sk=R.rec(sn)
        if sk.get("Class")!="Skill_Passive": continue
        v=R.arr(sk.get("characterLifeModifier"),rk)
        if isinstance(v,(int,float)): s+=v
        v2=R.arr(sk.get("characterLife"),rk)
        if isinstance(v2,(int,float)): f+=v2
    return (L+f)*(1+(s+pak)/100), L, s
print("zombie_a01 cl4:", hp("records/creatures/enemies/zombie_a01.dbr",4,50))
for cl in (11,12,13):
    print("Eastmire Herder cl%d"%cl, hp("records/creatures/enemies/trollhalfswamp_a02.dbr",cl,50))
print("Eastmire Warrior cl11", hp("records/creatures/enemies/trollhalfswamp_b02.dbr",11,50))
print("Deepmire Vanguard cl11", hp("records/creatures/enemies/slitha_melee_b01.dbr",11,50))
print()
for cl in (11,12,13,14,15,16,17,18):
    print(f"Primordian cl{cl}: pak50={hp('records/creatures/enemies/boss&quest/slith_wightmirecave01.dbr',cl,50)[0]:.1f}  pak35={hp('records/creatures/enemies/boss&quest/slith_wightmirecave01.dbr',cl,35)[0]:.3f}")
print()
for p in ["records/creatures/enemies/boss&quest/warden01.dbr","records/creatures/enemies/boss&quest/warden02.dbr"]:
    for cl in (18,):
        print(p.split('/')[-1], f"cl{cl}: pak50={hp(p,cl,50)[0]:.0f}  pak35={hp(p,cl,35)[0]:.0f}")
print()
for p in ["records/creatures/enemies/hero/boar_h01.dbr","records/creatures/enemies/hero/zombie_h01.dbr","records/creatures/enemies/hero/rifthound_h01.dbr"]:
    for cl in (15,20):
        print(p.split('/')[-1], f"cl{cl}: pak50={hp(p,cl,50)[0]:.0f}  pak35={hp(p,cl,35)[0]:.0f}")
