#!/usr/bin/env python3
import sys, csv, json, collections
sys.path.insert(0, "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/scratch/2026-08-08-kc2-ed3-diff")
import lib2
E2, E3 = lib2.E2, lib2.E3
CH = set(json.load(open("fulldiff_summary.json"))["changed"])

def V(p):
    p = p.lower()
    if p not in E3.idx and p not in E2.idx: return "ABSENT-BOTH"
    if p not in E2.idx: return "ONLY-III"
    if p not in E3.idx: return "ONLY-II"
    return "CHANGED" if p in CH else "IDENTICAL"

groups = collections.OrderedDict()

# --- (1) SurvivalMode3 tier-16 wave/pool/spawn tables covering waves 151-160 ---
# tier16 = global waves 151-160 (w01..w10)
t16 = sorted(p for p in E3.idx if p.startswith("records/proxies/tier16waves/"))
groups["(1) tier16waves proxies (global w151-160)"] = t16
# spawn points + level controllers for tier16
groups["(1b) tier16 spawnpoint / level entities"] = sorted(
    p for p in E3.idx if "tier16" in p and not p.startswith("records/proxies/tier16waves/"))

# --- (2) w151-w158 rostered monster records + summon bodies ---
CSV = "/Users/admin/Games/reincarnated-engine/data/kc2/pe6_crucible_wave_pools_v2.csv"
try:
    rows = list(csv.DictReader(open(CSV)))
    mons = set()
    pools = set()
    for r in rows:
        if 151 <= int(r["global_wave"]) <= 158:
            pools.add(r["pool_record"].lower())
            for col in ("roster_records", "champ_records"):
                for rec in (r.get(col) or "").split("|"):
                    rec = rec.strip().lower()
                    if rec: mons.add(rec)
    groups["(2) w151-158 pool proxy records"] = sorted(pools)
    groups["(2) w151-158 rostered monster records"] = sorted(mons)
except Exception as e:
    groups["(2) CSV ERROR"] = [str(e)]

SUMMON_BODIES = [
 "records/creatures/enemies/swampcrab_a00_summon.dbr",
 "records/creatures/enemies/swampcrab_b01_summon.dbr",
 "records/creatures/enemies/swampcrab_c01_summon.dbr",
 "records/creatures/enemies/springscrab_a00_summon.dbr",
 "records/creatures/enemies/skeleton_a02_summon.dbr",
 "records/creatures/enemies/ghost_a01_summon.dbr",
 "records/creatures/enemies/livingplant_a01_summon.dbr",
 "records/creatures/enemies/aetherialcorruption_c01_summon.dbr",
 "records/creatures/enemies/aetherialcorruption_b02_summon.dbr",
 "records/creatures/enemies/aetherialcolossus_c02_summon.dbr",
 "records/creatures/enemies/fleshshaper_spirit_01.dbr",
 "records/creatures/enemies/trap_brambletrap_a01.dbr",
 "records/creatures/enemies/trap_icespike_hero_a01.dbr",
 "records/creatures/enemies/trap_lightningspike_hero_a01.dbr",
 "records/creatures/enemies/krieg_aethertrap.dbr",
]
groups["(2b) summon bodies (crabling/spikeshell/archer/apparition)"] = SUMMON_BODIES

# --- (3) survival scalar arrays + counterparts ---
groups["(3) balancing/scalar arrays"] = [p for p in E3.find("balancingadjustment")]

# --- (5) L-58 mechanism chains ---
MECH = []
for i in range(1,6):
    MECH.append(f"records/creatures/enemies/swampcrab_h{i:02d}.dbr")
MECH += [
 "records/creatures/enemies/boss&quest/swampcrab_ugdenbog_01.dbr",
 "records/skills/nonplayerskillsgdx1/bossskills/carraxus_summonswampcrabc.dbr",
 "records/skills/nonplayerskillsgdx1/monsterskills/swampcrab_crabgenerator.dbr",
 "records/skills/nonplayerskillsgdx3/monsterskills/springscrab_crabgenerator.dbr",
 "records/creatures/enemies/skeletalgolem_b01.dbr",
 "records/creatures/enemies/skeletalgolem_c01.dbr",
 "records/creatures/enemies/skeletalgolem_a01.dbr",
]
for i in range(1,6):
    MECH.append(f"records/creatures/enemies/aetherialcorruption_h{i:02d}.dbr")
groups["(5) L-58 mechanism-chain records (path-guessed; ABSENT means path differs)"] = MECH

out = {}
for g, plist in groups.items():
    res = [(p, V(p)) for p in plist]
    out[g] = res
    n = collections.Counter(v for _, v in res)
    print(f"\n=== {g}  ({len(res)} records) -> {dict(n)}")
    for p, v in res:
        if v != "IDENTICAL":
            print(f"   {v:12s} {p}")
    if all(v == "IDENTICAL" for _, v in res) and res:
        print("   ALL IDENTICAL")
json.dump(out, open("kc2set_verdicts.json","w"), indent=1)
