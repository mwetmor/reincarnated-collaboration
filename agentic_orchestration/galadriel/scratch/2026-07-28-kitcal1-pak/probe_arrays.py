import importlib.util, pathlib, json
G5 = pathlib.Path("/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/scratch/2026-07-28-kitcal1-g5a/g5a_resolve.py")
spec = importlib.util.spec_from_file_location("g5a", G5); M = importlib.util.module_from_spec(spec); spec.loader.exec_module(M)
for p in ["records/skills/nonplayerskills/passive/damagebase_physical01.dbr",
          "records/skills/nonplayerskills/passive/damagebase_physical02.dbr",
          "records/skills/nonplayerskills/passive/armorbase01.dbr",
          "records/skills/nonplayerskills/passive/armorbase02.dbr"]:
    r = M.rec(p)
    print("=====", p)
    for k in ("offensivePhysicalMin","offensivePhysicalMax","offensiveTotalDamageModifier","characterLifeModifier","defensiveProtection","FileDescription"):
        v = r.get(k)
        if isinstance(v, list):
            print(f"  {k} ranks1-20: {[round(x,1) for x in v[:20]]}")
        else:
            print(f"  {k} = {v}")
