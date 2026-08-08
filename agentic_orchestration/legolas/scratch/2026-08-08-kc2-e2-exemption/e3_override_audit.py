#!/usr/bin/env python3
"""E-2 / S3 -- OVERRIDE AUDIT + variant band totals. READ-ONLY.

Q1 (highest risk for the p04 answer): does any pool record exist in MORE THAN ONE archive
    with a DIFFERENT ignoreGameBalance value?  If the Crucible archives (sm_mod/sm1/sm2/sm3)
    republish a base/gdx record and drop the flag, then last-writer-wins changes the answer.
Q2  hero pools with an EMPTY regular roster -- the +1 spawnMin additive cannot materialise a
    body where there is no name{j} to draw.  Census + band impact.
Q3  variant band totals over waves 151-170 so the conductor can identify which variant
    gamora's declared-override table is actually running.
"""
import sys, pathlib, re, csv, json, math, collections

sys.path.insert(0, "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arz_adapter_2026_07_24 import ArzArchive

ROOT = pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-II-20260724")
PE6 = pathlib.Path("/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/"
                   "legolas/scratch/2026-08-07-pe6-crucible/pe6_crucible_wave_pools.csv")
ORDER = [("base", "database/database.arz"), ("gdx1", "gdx1/database/GDX1.arz"),
         ("gdx2", "gdx2/database/GDX2.arz"), ("gdx3", "gdx3/database/GDX3.arz"),
         ("sm_mod", "mods/survivalmode/database/SurvivalMode.arz"),
         ("sm1", "survivalmode1/database/SurvivalMode1.arz"),
         ("sm2", "survivalmode2/database/SurvivalMode2.arz"),
         ("sm3", "survivalmode3/database/SurvivalMode3.arz")]
ARC = {}
WHERE = collections.defaultdict(list)     # path -> [archive keys, in ORDER]
for k, rel in ORDER:
    a = ArzArchive(ROOT / rel); ARC[k] = a
    for r in a.records:
        WHERE[r].append(k)
def rd(k, p):
    return ARC[k].read_record(p)
def num(v, d=0.0):
    try: return float(v)
    except Exception: return d
def igb(rec):
    if rec is None: return ("NORECORD", None, None)
    if "ignoreGameBalance" in rec:
        v = rec["ignoreGameBalance"]; return ("PRESENT", str(v), bool(num(v, 0) != 0))
    return ("ABSENT", None, False)

rows = list(csv.DictReader(open(PE6)))
pools = sorted(set(r["pool_record"] for r in rows))

# ---------------------------------------------------------------- Q1 override audit
print("=" * 110)
print("Q1  MULTI-ARCHIVE OVERRIDE AUDIT over the 635 pools of the P-E6 CSV")
print("=" * 110)
multi, diverge, samefield = 0, [], 0
for p in pools:
    ks = WHERE[p]
    if len(ks) < 2:
        continue
    multi += 1
    seen = [(k,) + igb(rd(k, p)) for k in ks]
    eff = set(s[3] for s in seen)
    st = set(s[1] for s in seen)
    if len(eff) > 1:
        diverge.append((p, seen))
    elif len(st) > 1:
        samefield += 1
print(f"  pools present in >1 archive: {multi}/{len(pools)}")
print(f"  EFFECTIVE-VALUE divergence across archives: {len(diverge)}")
print(f"  same effective value but field-presence differs: {samefield}")
for p, seen in diverge:
    print(f"    !! {p}")
    for k, st, raw, v in seen:
        print(f"         [{k:7s}] state={st:8s} raw={raw!r:8s} -> {v}")

print("\n  --- per-archive trace, the six wave-160 pools ---")
W160 = [r["pool_record"] for r in rows if r["global_wave"] == "160"]
for p in W160:
    trace = "  ".join(f"{k}:{igb(rd(k,p))[0]}={igb(rd(k,p))[2]}" for k in WHERE[p])
    print(f"    {p.replace('records/proxies/',''):58s} archives={WHERE[p]}  {trace}")

# ---------------------------------------------------------------- Q2 empty regular roster
print("\n" + "=" * 110)
print("Q2  POOLS WITH AN EMPTY REGULAR ROSTER (no name{j}) -- the +1 spawnMin additive has nothing to draw")
print("=" * 110)
def roster_n(p):
    r = rd(WHERE[p][-1], p)
    return sum(1 for j in range(1, 25) if r.get(f"name{j}")), \
           sum(1 for j in range(1, 25) if r.get(f"nameChampion{j}"))
empt = collections.Counter(); empt_pools = []
for p in pools:
    rn, cn = roster_n(p)
    r = rd(WHERE[p][-1], p)
    if rn == 0:
        empt[pathlib.Path(p).parent.name] += 1
        empt_pools.append((p, num(r.get("spawnMin")), num(r.get("spawnMax")), cn))
print(f"  {len(empt_pools)} of {len(pools)} pools have zero name{{j}} entries: {dict(empt)}")
nz = [e for e in empt_pools if e[1] or e[2]]
print(f"  of those, {len(nz)} declare spawnMin/Max != 0  ->  {nz[:5]}")
csvrn = {r['pool_record']: int(r['roster_n']) for r in rows}
dis = [p for p, *_ in empt_pools if csvrn.get(p, -1) != 0]
print(f"  agreement with the P-E6 CSV roster_n column: "
      f"{len(empt_pools)-len(dis)}/{len(empt_pools)} agree; disagree={dis[:5]}")

# ---------------------------------------------------------------- Q3 variant bands
print("\n" + "=" * 110)
print("Q3  VARIANT BAND TOTALS, waves 151-170")
print("=" * 110)
adjrec = rd(WHERE["records/game/balancingadjustment_survivalmode_enemies03.dbr"][-1],
            "records/game/balancingadjustment_survivalmode_enemies03.dbr")
def adjv(f, w):
    v = adjrec.get(f, [])
    return num(v[min(max(int(w) - 1, 0), len(v) - 1)]) if v else 0.0

REC = {p: rd(WHERE[p][-1], p) for p in pools}
IGB = {p: igb(REC[p])[2] for p in pools}
def kind(p):
    return ("BOSS" if "/poolsboss" in p else "HERO" if "/poolshero" in p
            else "DEVOTION" if "/poolsdevotion" in p else "BOUNTY" if "/poolsbounty" in p else "trash")

def E(p, w, exempt, roster_guard):
    r = REC[p]
    smin, smax = num(r.get("spawnMin")), num(r.get("spawnMax"))
    cch, cmin, cmax = num(r.get("championChance")), num(r.get("championMin")), num(r.get("championMax"))
    rn = sum(1 for j in range(1, 25) if r.get(f"name{j}"))
    if exempt:
        nmin, nmax, c0, c1 = smin, smax, cmin, cmax
    else:
        nmin = math.floor((smin + 1 + adjv("spawnMinAdj", w)) * 1.2)
        nmax = smax + 1 + adjv("spawnMaxAdj", w)
        if nmin > nmax: nmin = nmax
        c0 = cmin + 1 + adjv("spawnChampionMinAdj", w) if cch else cmin
        c1 = cmax + 1 + adjv("spawnChampionMaxAdj", w) if cch else cmax
    if roster_guard and rn == 0:
        nmin = nmax = 0.0
    return (nmin + nmax) / 2.0 + (cch / 100.0) * ((c0 + c1) / 2.0)

VARIANTS = {
    "V1 all-non-exempt (gamora default False)":      lambda p: False,
    "V2 AS-DECLARED (measured, this probe)":         lambda p: IGB[p],
    "V3 all BOSS pools exempt":                      lambda p: kind(p) == "BOSS",
    "V4 all spawnMax<2 exempt (P-E6 s8 guard)":      lambda p: num(REC[p].get("spawnMax")) < 2,
}
for guard in (False, True):
    print(f"\n  --- empty-regular-roster guard = {guard} ---")
    print(f"  {'variant':46s} {'151-170 p06ON':>14s} {'p06OFF':>10s} {'w160 ON':>9s} {'w160 OFF':>9s}")
    for vname, fn in VARIANTS.items():
        tot = tot6 = 0.0; w160on = w160off = 0.0
        for w in range(151, 171):
            wr_ = [r for r in rows if r["global_wave"] == str(w)]
            pts = collections.defaultdict(list)
            for r in wr_: pts[int(r["spawn_point"])].append(r)
            for pt in sorted(pts):
                opts = pts[pt]; wt = sum(float(o["pool_weight"]) for o in opts) or 1.0
                e = sum(float(o["pool_weight"]) * E(o["pool_record"], w, fn(o["pool_record"]), guard)
                        for o in opts) / wt
                tot += e
                if pt != 6: tot6 += e
                if w == 160:
                    w160on += e
                    if pt != 6: w160off += e
        print(f"  {vname:46s} {tot:14.2f} {tot6:10.2f} {w160on:9.2f} {w160off:9.2f}")

# ---------------------------------------------------------------- wave-160 body board
print("\n" + "=" * 110)
print("WAVE-160 BODY BOARD  with the empty-roster guard ON (the spec's '3+1+3' arithmetic)")
print("=" * 110)
for p in W160:
    r = REC[p]
    rn = sum(1 for j in range(1, 25) if r.get(f"name{j}"))
    cn = sum(1 for j in range(1, 25) if r.get(f"nameChampion{j}"))
    pt = [x["spawn_point"] for x in rows if x["global_wave"] == "160" and x["pool_record"] == p][0]
    for exempt in (True, False):
        e = E(p, 160, exempt, True)
        if exempt:
            lab = "EXEMPT"
        else:
            lab = "NONEXEM"
        print(f"  p{pt} {'*' if IGB[p]==exempt else ' '} {lab:8s} {p.replace('records/proxies/',''):56s} "
              f"roster={rn:2d} champroster={cn:2d}  bodies_E={e:.2f}")
print("\n  ('*' marks the branch the DB actually selects)")
