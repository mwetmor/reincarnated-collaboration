#!/usr/bin/env python3
"""S4 — PE6 MASTER Crucible wave-composition extractor. READ-ONLY.

Resolution chain (3 hops):
  records/proxies/tier<NN>waves/proxy_w<WW>_p<PP>a.dbr   [Proxy | ProxyAmbush]
    -> pool{i} / poolEpic{i} / poolLegendary{i}          [difficulty-scoped, weighted ALTERNATIVES]
       -> proxypool record: spawnMin/Max, championChance/Min/Max,
          name{j}/weight{j}/limit{j}/minPlayerLevel{j}, nameChampion{j}/weightChampion{j}
          -> records/creatures/enemies/*.dbr  [Monster]  -> description tag -> Text_EN.arc display name

Global wave number := (tier-1)*10 + wave     [proved by checkpoint tags: tier05->50 ... tier18->180]
Difficulty:  base pools = ASPIRANT(Normal) | poolEpic = CHALLENGER(Elite) | poolLegendary = GLADIATOR(Ultimate)
             Gladiator view = poolLegendary if present on that spawn-point record else base pools.
"""
import sys, pathlib, collections, re, json
sys.path.insert(0, "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arz_adapter_2026_07_24 import ArzArchive
from gd_arc_reader_2026_07_26 import ArcArchive, parse_tag_file

ROOT = pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-II-20260724")
ORDER = [("base", ROOT / "database/database.arz"), ("gdx1", ROOT / "gdx1/database/GDX1.arz"),
         ("gdx2", ROOT / "gdx2/database/GDX2.arz"), ("gdx3", ROOT / "gdx3/database/GDX3.arz"),
         ("sm_mod", ROOT / "mods/survivalmode/database/SurvivalMode.arz"),
         ("sm1", ROOT / "survivalmode1/database/SurvivalMode1.arz"),
         ("sm2", ROOT / "survivalmode2/database/SurvivalMode2.arz"),
         ("sm3", ROOT / "survivalmode3/database/SurvivalMode3.arz")]

M = {}
for k, p in ORDER:
    a = ArzArchive(p)
    for r in a.records:
        M[r] = (k, a)

_cache = {}
def get(p):
    p = str(p)
    if p in _cache: return _cache[p]
    e = M.get(p)
    r = e[1].read_record(p) if e else None
    _cache[p] = r
    return r
def own(p):
    e = M.get(str(p)); return e[0] if e else None
def num(v, d=0.0):
    try: return float(v)
    except Exception: return d

# ---------------------------------------------------------------- display tags
TAGS = {}
for arc in sorted(ROOT.rglob("Text_EN.arc")):
    try:
        A = ArcArchive(arc)
    except Exception as ex:
        print(f"  [arc skip] {arc}: {ex}"); continue
    for name in A.names():
        if not name.lower().endswith(".txt"): continue
        try:
            d = parse_tag_file(A.read_file(name))
        except Exception:
            continue
        for k, v in d:
            TAGS.setdefault(k, v)
print(f"loaded {len(TAGS)} localization tags")

_mname = {}
def monster_name(rec_path):
    rp = str(rec_path)
    if rp in _mname: return _mname[rp]
    r = get(rp)
    if r is None:
        _mname[rp] = ("<MISSING RECORD>", None); return _mname[rp]
    tag = r.get("description") or r.get("Description")
    nm = TAGS.get(str(tag), None) if tag else None
    _mname[rp] = (nm or f"<untagged:{pathlib.Path(rp).stem}>", str(tag) if tag else None)
    return _mname[rp]

# ---------------------------------------------------------------- pool resolution
def pool_detail(pp):
    """Full roster + counts of one proxypool record."""
    pr = get(pp)
    if pr is None: return None
    d = dict(pool=str(pp), owner=own(pp),
             smin=num(pr.get("spawnMin")), smax=num(pr.get("spawnMax")),
             cch=num(pr.get("championChance")), cmin=num(pr.get("championMin")),
             cmax=num(pr.get("championMax")), roster=[], champroster=[])
    for j in range(1, 25):
        n = pr.get(f"name{j}")
        if not n: continue
        nm, tag = monster_name(n)
        d["roster"].append(dict(rec=str(n), name=nm, tag=tag,
                                w=num(pr.get(f"weight{j}")), limit=pr.get(f"limit{j}"),
                                minPL=pr.get(f"minPlayerLevel{j}"),
                                lv=str(pr.get(f"levelVarianceEquation{j}") or "")))
    for j in range(1, 25):
        n = pr.get(f"nameChampion{j}")
        if not n: continue
        nm, tag = monster_name(n)
        d["champroster"].append(dict(rec=str(n), name=nm, tag=tag,
                                     w=num(pr.get(f"weightChampion{j}")), limit=pr.get(f"limitChampion{j}"),
                                     minPL=pr.get(f"minPlayerLevelChampion{j}"),
                                     lv=str(pr.get(f"levelVarianceEquationChampion{j}") or "")))
    return d

DIFFS = [("aspirant", "pool", "weight"), ("challenger", "poolEpic", "weightEpic"),
         ("gladiator", "poolLegendary", "weightLegendary")]

PAT = re.compile(r"^records/proxies/tier(\d+)waves/proxy_w(\d+)_p(\d+)a\.dbr$")
points = collections.defaultdict(list)
for path in M:
    m = PAT.match(path)
    if not m: continue
    t, w, pt = int(m.group(1)), int(m.group(2)), int(m.group(3))
    rec = get(path)
    cls = M[path][1].record_type(path)
    entry = dict(tier=t, wave=w, gwave=(t - 1) * 10 + w, pt=pt, path=path,
                 owner=own(path), cls=cls, diffs={}, fallback={})
    if cls == "ProxyAmbush":
        entry["ambush"] = dict(minGroupSize=rec.get("minGroupSize"), maxGroupSize=rec.get("maxGroupSize"),
                               spawnThreshold=rec.get("spawnThreshold"),
                               minSpawnTime=rec.get("minSpawnTime"), maxSpawnTime=rec.get("maxSpawnTime"),
                               minDelayTime=rec.get("minDelayTime"), maxDelayTime=rec.get("maxDelayTime"),
                               alertArea=rec.get("alertArea"))
    for dname, pfx, wfx in DIFFS:
        opts = []
        for i in range(1, 13):
            pp = rec.get(f"{pfx}{i}")
            if not pp: continue
            pd = pool_detail(pp)
            if pd is None:
                opts.append(dict(pool=str(pp), UNRESOLVED=True)); continue
            pd["w"] = num(rec.get(f"{wfx}{i}"), 0.0)
            opts.append(pd)
        if opts:
            entry["diffs"][dname] = opts
            entry["fallback"][dname] = False
        else:
            entry["diffs"][dname] = entry["diffs"]["aspirant"]
            entry["fallback"][dname] = True
    points[(t, w)].append(entry)

print(f"resolved spawn points: {sum(len(v) for v in points.values())}  (tier,wave) pairs: {len(points)}")

def wave_stats(pts, diff):
    """min / max / E over the spawn points, for one difficulty view."""
    tmin = tmax = texp = 0.0
    for e in pts:
        opts = [o for o in e["diffs"][diff] if not o.get("UNRESOLVED")]
        if not opts: continue
        wt = sum(o["w"] for o in opts) or 1.0
        tmin += min(o["smin"] for o in opts)
        tmax += max(o["smax"] + o["cmax"] for o in opts)
        texp += sum(o["w"] * (((o["smin"] + o["smax"]) / 2.0)
                              + (o["cch"] / 100.0) * ((o["cmin"] + o["cmax"]) / 2.0)) for o in opts) / wt
    return tmin, tmax, texp

def kind_of(poolpath):
    p = str(poolpath)
    if "/poolsboss" in p: return "BOSS"
    if "/poolshero" in p: return "HERO"
    if "/poolsdevotion" in p: return "DEVOTION"
    if "/poolsbounty" in p: return "BOUNTY"
    return "trash"

waves = []
for (t, w), pts in sorted(points.items()):
    rec = dict(tier=t, wave=w, gwave=(t - 1) * 10 + w, npts=len(pts),
               owners=sorted(set(e["owner"] for e in pts)),
               classes=dict(collections.Counter(e["cls"] for e in pts)))
    for d in ("aspirant", "challenger", "gladiator"):
        mn, mx, ex = wave_stats(pts, d)
        rec[d] = dict(min=mn, max=mx, E=round(ex, 2))
        kinds = collections.Counter()
        fams, bosses, heroes = collections.Counter(), collections.Counter(), collections.Counter()
        for e in pts:
            for o in e["diffs"][d]:
                if o.get("UNRESOLVED"): continue
                k = kind_of(o["pool"]); kinds[k] += 1
                stem = pathlib.Path(o["pool"]).stem
                fams[stem] += 1
                for r in o["roster"]:
                    if k == "BOSS": bosses[r["name"]] += 1
                    elif k == "HERO": heroes[r["name"]] += 1
                for r in o["champroster"]:
                    heroes[r["name"]] += 1
        rec[d]["kinds"] = dict(kinds); rec[d]["pools"] = dict(fams)
        rec[d]["boss_names"] = sorted(bosses); rec[d]["hero_names"] = sorted(heroes)
    rec["points"] = pts
    waves.append(rec)

json.dump(waves, open("s4_waves_full.json", "w"), indent=1)
print("[wrote s4_waves_full.json]")

print("\n=== per-wave GLADIATOR summary, waves 1..200 ===")
print(f"{'gw':>4} {'t':>3} {'w':>3} {'pts':>4} {'min':>5} {'max':>5} {'E':>7}  kinds                    boss/hero present")
for r in sorted(waves, key=lambda x: x["gwave"]):
    g = r["gladiator"]
    bh = ""
    if g["boss_names"]: bh += "BOSS:" + ",".join(g["boss_names"][:4])
    if g["hero_names"]: bh += "  HERO:" + ",".join(g["hero_names"][:3])
    print(f"{r['gwave']:4d} {r['tier']:3d} {r['wave']:3d} {r['npts']:4d} {g['min']:5.0f} {g['max']:5.0f} "
          f"{g['E']:7.2f}  {str(g['kinds']):24s} {bh[:90]}")
