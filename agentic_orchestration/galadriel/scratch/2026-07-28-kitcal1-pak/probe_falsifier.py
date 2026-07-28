import importlib.util, pathlib
G5=pathlib.Path("/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/scratch/2026-07-28-kitcal1-g5a/g5a_resolve.py")
sp=importlib.util.spec_from_file_location("g5a",G5); M=importlib.util.module_from_spec(sp); sp.loader.exec_module(M)
for rec,spawn in [("records/creatures/enemies/zombiemutated_a01.dbr",13),
                  ("records/creatures/enemies/boss&quest/warden01.dbr",15),
                  ("records/creatures/enemies/boss&quest/warden02.dbr",15),
                  ("records/creatures/enemies/zombie_a01.dbr",1)]:
    try: r=M.resolve(rec,spawn)
    except KeyError: print(rec,"MISSING"); continue
    tdm=r["dmg_terms"]["skillTdmPct"]; pak=r["dmg_terms"]["pakTdmPct"]
    print(f"{rec} spawn={spawn} charLevel={r['charLevel']}")
    print(f"   passive TDM sources: {r['contrib'].get('offensiveTotalDamageModifier')}")
    print(f"   sum skill TDM = {tdm}   + pak {pak}  => ADDITIVE mult = {1+(tdm+pak)/100:+.3f}"
          f"   MULT mult = {(1+tdm/100)*(1+pak/100):.4f}")
    print(f"   physMin/Max raw = {r['dmg_terms']['physMin_raw']}/{r['dmg_terms']['physMax_raw']}")
