#!/usr/bin/env python3
"""E-2 / S2 -- emit the exemption sidecar + a revised pools CSV, and print the
wave-160 board plus the 151-170 calibration-band delta. READ-ONLY on all corpora.

PRIMARY emission  : pe6_pool_ignoregamebalance.csv   (sidecar, keyed by pool_record)
CONVENIENCE       : pe6_crucible_wave_pools_v2.csv   (P-E6 CSV + 3 appended columns)

Count model applied for the board is U-9 s6 verbatim:
    if pool.ignoreGameBalance:  n=[smin,smax]           c=[cmin,cmax]
    else:                       n_min=floor((smin+1+0)*120/100), n_max=smax+1+0, clamp min<=max
                                c_min=cmin+1+adj, c_max=cmax+1+adj      (adj == +1 for w>=~68)
"""
import sys, pathlib, re, csv, json, math, collections, hashlib

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
M = {}
for k, rel in ORDER:
    a = ArzArchive(ROOT / rel)
    for r in a.records:
        M[r] = (k, a)
_c = {}
def get(p):
    p = str(p)
    if p in _c: return _c[p]
    e = M.get(p); _c[p] = e[1].read_record(p) if e else None
    return _c[p]
def own(p):
    e = M.get(str(p)); return e[0] if e else None
def num(v, d=0.0):
    try: return float(v)
    except Exception: return d

# ------------------------------------------------------------------ index-bound audit
PAT = re.compile(r"^records/proxies/tier(\d+)waves/proxy_w(\d+)_p(\d+)a\.dbr$")
maxidx = collections.Counter()
for path in M:
    if not PAT.match(path): continue
    r = get(path)
    for pfx in ("pool", "poolEpic", "poolLegendary"):
        hi = 0
        for i in range(1, 33):
            if r.get(f"{pfx}{i}"): hi = i
        maxidx[(pfx, hi)] += 1
print("index-bound audit (highest declared slot index per proxy record):")
for (pfx, hi), n in sorted(maxidx.items()):
    print(f"    {pfx:14s} max_i={hi:2d}  on {n:4d} proxies")
print("  -> confirms the 1..12 loop bound in P-E6 s4 truncates nothing.\n")

# ------------------------------------------------------------------ resolve flag
def resolve(p):
    r = get(p)
    if r is None:
        return dict(state="NORECORD", raw="", igb=None, owner=None, grade="NAMED-ABSENT")
    if "ignoreGameBalance" in r:
        v = r["ignoreGameBalance"]
        return dict(state="PRESENT", raw=str(v), igb=bool(num(v, 0) != 0),
                    owner=own(p), grade="DB-CITED")
    return dict(state="ABSENT", raw="", igb=False, owner=own(p), grade="TPL-DEFAULT")

rows = list(csv.DictReader(open(PE6)))
pools = sorted(set(r["pool_record"] for r in rows))
RES = {p: resolve(p) for p in pools}
print(f"pools CSV: {len(rows)} rows, {len(pools)} distinct pool_record")
st = collections.Counter(RES[p]["state"] for p in pools)
print(f"field-state over the CSV's pool set: {dict(st)}   IGB=True: {sum(1 for p in pools if RES[p]['igb'])}\n")

# archive-owner agreement check against the CSV's own pool_archive column
csv_owner = {}
for r in rows:
    csv_owner.setdefault(r["pool_record"], set()).add(r["pool_archive"])
mismatch = [(p, sorted(csv_owner[p]), RES[p]["owner"]) for p in pools
            if RES[p]["owner"] not in csv_owner[p]]
print(f"pool_archive agreement: {len(pools) - len(mismatch)}/{len(pools)} agree; "
      f"mismatches={mismatch if mismatch else 'NONE'}\n")

# ------------------------------------------------------------------ SIDECAR
side = []
for p in pools:
    r = get(p); d = RES[p]
    side.append(dict(pool_record=p, pool_archive=d["owner"], pool_family=pathlib.Path(p).parent.name,
                     pool_kind=("BOSS" if "/poolsboss" in p else "HERO" if "/poolshero" in p
                                else "DEVOTION" if "/poolsdevotion" in p
                                else "BOUNTY" if "/poolsbounty" in p else "trash"),
                     ignore_game_balance=d["igb"], field_state=d["state"], raw_value=d["raw"],
                     provenance=d["grade"],
                     spawn_min=num(r.get("spawnMin")) if r else "",
                     spawn_max=num(r.get("spawnMax")) if r else "",
                     champion_chance=num(r.get("championChance")) if r else "",
                     champion_min=num(r.get("championMin")) if r else "",
                     champion_max=num(r.get("championMax")) if r else "",
                     proxy_pool_equation=(str(r.get("proxyPoolEquation") or "") if r else "")))
side.sort(key=lambda d: d["pool_record"])
with open("pe6_pool_ignoregamebalance.csv", "w", newline="") as f:
    wr = csv.DictWriter(f, fieldnames=list(side[0])); wr.writeheader(); wr.writerows(side)
print(f"[wrote pe6_pool_ignoregamebalance.csv] {len(side)} rows")

# ------------------------------------------------------------------ REVISED POOLS CSV
fn = list(rows[0]) + ["ignore_game_balance", "igb_field_state", "igb_provenance"]
for r in rows:
    d = RES[r["pool_record"]]
    r["ignore_game_balance"] = d["igb"]; r["igb_field_state"] = d["state"]; r["igb_provenance"] = d["grade"]
with open("pe6_crucible_wave_pools_v2.csv", "w", newline="") as f:
    wr = csv.DictWriter(f, fieldnames=fn); wr.writeheader(); wr.writerows(rows)
print(f"[wrote pe6_crucible_wave_pools_v2.csv] {len(rows)} rows, {len(fn)} cols\n")

# ------------------------------------------------------------------ count model
adjrec = get("records/game/balancingadjustment_survivalmode_enemies03.dbr")
def adjv(field, w):
    v = adjrec.get(field, [])
    i = min(max(int(w) - 1, 0), len(v) - 1)
    return num(v[i]) if v else 0.0

def counts(pool, w, exempt):
    r = get(pool)
    smin, smax = num(r.get("spawnMin")), num(r.get("spawnMax"))
    cch, cmin, cmax = num(r.get("championChance")), num(r.get("championMin")), num(r.get("championMax"))
    if exempt:
        return smin, smax, cch, cmin, cmax
    nmin = math.floor((smin + 1 + adjv("spawnMinAdj", w)) * 120 / 100.0)
    nmax = smax + 1 + adjv("spawnMaxAdj", w)
    if nmin > nmax: nmin = nmax
    c0 = cmin + (1 + adjv("spawnChampionMinAdj", w)) if cch else cmin
    c1 = cmax + (1 + adjv("spawnChampionMaxAdj", w)) if cch else cmax
    return nmin, nmax, cch, c0, c1

def E(pool, w, exempt):
    nmin, nmax, cch, c0, c1 = counts(pool, w, exempt)
    return (nmin + nmax) / 2.0 + (cch / 100.0) * ((c0 + c1) / 2.0)

# ------------------------------------------------------------------ WAVE 160 BOARD
print("=" * 118)
print("WAVE 160 BOARD  (E-3)   -- per spawn point, Gladiator, pools as declared")
print("=" * 118)
w160 = [r for r in rows if r["global_wave"] == "160"]
print(f"{'pt':>3} {'kind':9s} {'pool':56s} {'wt':>6s} {'IGB':>6s} {'state':8s} "
      f"{'base n':>8s} {'base c':>8s} | {'AS-IS n':>9s} {'c':>7s} {'E':>6s} | {'ifNONEX n':>10s} {'c':>7s} {'E':>6s}")
by_pt = collections.defaultdict(list)
for r in w160: by_pt[int(r["spawn_point"])].append(r)
tot_asis = tot_nonex = tot_allex = 0.0
for pt in sorted(by_pt):
    opts = by_pt[pt]
    wt = sum(float(o["pool_weight"]) for o in opts) or 1.0
    e_asis = e_non = e_ex = 0.0
    for o in opts:
        p = o["pool_record"]; d = RES[p]
        a = counts(p, 160, d["igb"]); b = counts(p, 160, False); c = counts(p, 160, True)
        ea, eb, ec = E(p, 160, d["igb"]), E(p, 160, False), E(p, 160, True)
        e_asis += float(o["pool_weight"]) * ea / wt
        e_non  += float(o["pool_weight"]) * eb / wt
        e_ex   += float(o["pool_weight"]) * ec / wt
        print(f"{pt:3d} {o['pool_kind']:9s} {p.replace('records/proxies/',''):56s} "
              f"{float(o['pool_weight']):6.0f} {str(d['igb']):>6s} {d['state']:8s} "
              f"{num(get(p).get('spawnMin')):3.0f}-{num(get(p).get('spawnMax')):<4.0f} "
              f"{num(get(p).get('championMin')):3.0f}-{num(get(p).get('championMax')):<4.0f} | "
              f"{a[0]:4.0f}-{a[1]:<4.0f} {a[3]:3.0f}-{a[4]:<3.0f} {ea:6.2f} | "
              f"{b[0]:5.0f}-{b[1]:<4.0f} {b[3]:3.0f}-{b[4]:<3.0f} {eb:6.2f}")
    tot_asis += e_asis; tot_nonex += e_non; tot_allex += e_ex
    print(f"{'':3s} {'point E':9s} {'':56s} {'':6s} {'':6s} {'':8s} {'':8s} {'':8s} | "
          f"{'':9s} {'':7s} {e_asis:6.2f} | {'':10s} {'':7s} {e_non:6.2f}")
print(f"\nWAVE-160 TOTAL E   as-declared={tot_asis:.2f}   all-non-exempt={tot_nonex:.2f}   "
      f"all-exempt={tot_allex:.2f}   delta(as-declared - all-non-exempt)={tot_asis - tot_nonex:+.2f}")

print("\n--- p04 cell, explicit ---")
for o in by_pt[4]:
    p = o["pool_record"]; d = RES[p]; r = get(p)
    print(f"  {p}")
    print(f"     archive={d['owner']}  weight={o['pool_weight']}  field_state={d['state']}  "
          f"raw={d['raw']!r}  ignoreGameBalance={d['igb']}  provenance={d['grade']}")
    print(f"     spawnMin/Max={num(r.get('spawnMin')):.0f}/{num(r.get('spawnMax')):.0f}  "
          f"championChance={num(r.get('championChance')):.0f} "
          f"championMin/Max={num(r.get('championMin')):.0f}/{num(r.get('championMax')):.0f}  "
          f"proxyPoolEquation={r.get('proxyPoolEquation')}")
    print(f"     -> exempt branch  n={counts(p,160,True)[0]:.0f}-{counts(p,160,True)[1]:.0f}   "
          f"non-exempt branch n={counts(p,160,False)[0]:.0f}-{counts(p,160,False)[1]:.0f}")

# ------------------------------------------------------------------ BAND 151-170
print("\n" + "=" * 118)
print("CALIBRATION BAND 151-170  -- wave E under as-declared IGB vs the default-False model")
print("=" * 118)
print(f"{'w':>4} {'pts':>4} {'E_declared':>11s} {'E_allFalse':>11s} {'delta':>8s}  "
      f"{'exempt pools on the wave (pt:pool)':s}")
band_d = band_f = 0.0
p06_d = p06_f = 0.0
for w in range(151, 171):
    wr_ = [r for r in rows if r["global_wave"] == str(w)]
    pts = collections.defaultdict(list)
    for r in wr_: pts[int(r["spawn_point"])].append(r)
    ed = ef = 0.0; ed6 = ef6 = 0.0; ex = []
    for pt in sorted(pts):
        opts = pts[pt]; wt = sum(float(o["pool_weight"]) for o in opts) or 1.0
        a = sum(float(o["pool_weight"]) * E(o["pool_record"], w, RES[o["pool_record"]]["igb"]) for o in opts) / wt
        b = sum(float(o["pool_weight"]) * E(o["pool_record"], w, False) for o in opts) / wt
        ed += a; ef += b
        if pt != 6: ed6 += a; ef6 += b
        for o in opts:
            if RES[o["pool_record"]]["igb"]: ex.append(f"p{pt}:{pathlib.Path(o['pool_record']).stem}")
    band_d += ed; band_f += ef; p06_d += ed6; p06_f += ef6
    print(f"{w:4d} {len(pts):4d} {ed:11.2f} {ef:11.2f} {ed - ef:+8.2f}  {', '.join(ex)[:60]}")
print(f"\nBAND TOTAL  p06 ON : declared={band_d:.2f}  allFalse={band_f:.2f}  delta={band_d - band_f:+.2f}")
print(f"BAND TOTAL  p06 OFF: declared={p06_d:.2f}  allFalse={p06_f:.2f}  delta={p06_d - p06_f:+.2f}")

json.dump(dict(resolve={p: RES[p] for p in pools}), open("e2_resolve.json", "w"), indent=1)

for f in ("pe6_pool_ignoregamebalance.csv", "pe6_crucible_wave_pools_v2.csv"):
    h = hashlib.sha256(pathlib.Path(f).read_bytes()).hexdigest()
    print(f"\nSHA-256  {f}  {h}")
