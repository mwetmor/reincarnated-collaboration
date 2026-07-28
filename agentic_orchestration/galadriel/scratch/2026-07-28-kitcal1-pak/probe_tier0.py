import importlib.util, pathlib, json
G5=pathlib.Path("/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/scratch/2026-07-28-kitcal1-g5a/g5a_resolve.py")
sp=importlib.util.spec_from_file_location("g5a",G5); M=importlib.util.module_from_spec(sp); sp.loader.exec_module(M)
P="records/skills/nonplayerskills/passive/"
for t in ("00","01"):
    p=f"{P}damagebase_physical{t}.dbr"
    if not M.has(p): print(p,"ABSENT"); continue
    r=M.rec(p)
    print(p, "|", r.get("FileDescription"), "| unarmedOnly=", r.get("unarmedOnly"))
    print("   min r1-6:", r["offensivePhysicalMin"][:6], " max r1-6:", r["offensivePhysicalMax"][:6])
print()
for rec in ["records/creatures/enemies/zombie_a01.dbr",
            "records/creatures/enemies/zombie_b02h.dbr",
            "records/creatures/enemies/prawn_a01.dbr",
            "records/creatures/enemies/bonerat_meleea01.dbr",
            "records/creatures/enemies/rifthound_swamp_a01.dbr"]:
    try: m=M.rec(rec)
    except KeyError: print(rec,"MISSING"); continue
    sk=[(m.get(f"skillName{i}"), m.get(f"skillLevel{i}")) for i in range(1,13) if m.get(f"skillName{i}")]
    print(rec, "minLevel=",m.get("minLevel"), "maxLevel=",m.get("maxLevel"))
    for s,l in sk: print("    ", s, "|", l)
print()
# resolve zombie_a01 at spawn 1 and 2 under the resolver's (multiplicative) rule
for sl in (1,2,3):
    r=M.resolve("records/creatures/enemies/zombie_a01.dbr", sl)
    print(f"zombie_a01 spawn={sl} charLevel={r['charLevel']} hp={r['hp']:.0f} "
          f"dmg={r['dmg_min']:.2f}-{r['dmg_max']:.2f} (MULT rule) terms={ {k:(round(v,4) if isinstance(v,float) else v) for k,v in r['dmg_terms'].items()} }")
