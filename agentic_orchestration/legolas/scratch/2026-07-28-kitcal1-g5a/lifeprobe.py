import importlib.util, sys, json
spec = importlib.util.spec_from_file_location("g5a", "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/scratch/2026-07-28-kitcal1-g5a/g5a_resolve.py")
R = importlib.util.module_from_spec(spec); spec.loader.exec_module(R)

def dump(path, cl):
    m = R.rec(path)
    bio = m.get("characterAttributeEquations")
    b = R.rec(bio)
    print(f"=== {path}  charLevelEq={m.get('charLevel')}  class={m.get('monsterClassification')} cl={cl}")
    print("   bio:", bio)
    for k in ("characterLife","characterMana"):
        print(f"   {k} = {b.get(k)}  -> {R.evaleq(b.get(k), cl)}")
    # monster-record own life fields
    for k,v in m.items():
        if "ife" in k and "Leech" not in k:
            print("   MREC", k, "=", v)
    for i in range(1,13):
        sn = m.get(f"skillName{i}"); sl = m.get(f"skillLevel{i}")
        if not sn: continue
        rank = R.evaleq(sl, cl) if isinstance(sl,str) else sl
        rank = 0 if rank is None else int(rank)
        if not R.has(sn): 
            print(f"   sk{i} {sn} rank={rank} MISSING"); continue
        s = R.rec(sn)
        life = {}
        for k,v in s.items():
            if k.startswith("characterLife") or k=="characterLife":
                life[k] = R.arr(v, rank)
        print(f"   sk{i} {sn} class={s.get('Class')} lvlEq={sl} rank={rank} life={life}")
    print("   PAK:", {k:v for k,v in R.pak_vals().items() if "ife" in k})

dump("records/creatures/enemies/boss&quest/slith_wightmirecave01.dbr", 13)
dump("records/creatures/enemies/hero/boar_h07.dbr", 10)
