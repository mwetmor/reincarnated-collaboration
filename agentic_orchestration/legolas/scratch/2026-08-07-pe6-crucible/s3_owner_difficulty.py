#!/usr/bin/env python3
"""S3 — PE6: archive lineage per tier + the poolEpic/poolLegendary difficulty axis. READ-ONLY.
GD internal difficulty naming: (base)=Normal, Epic=Elite, Legendary=Ultimate.
Crucible difficulty labels: Aspirant / Challenger / Gladiator. The FIXTURE IS ON GLADIATOR.
"""
import sys, pathlib, collections, re, json
sys.path.insert(0, "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arz_adapter_2026_07_24 import ArzArchive

ROOT = pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-II-20260724")
ORDER = [("base", ROOT / "database/database.arz"), ("gdx1", ROOT / "gdx1/database/GDX1.arz"),
         ("gdx2", ROOT / "gdx2/database/GDX2.arz"), ("gdx3", ROOT / "gdx3/database/GDX3.arz"),
         ("sm_mod", ROOT / "mods/survivalmode/database/SurvivalMode.arz"),
         ("sm1", ROOT / "survivalmode1/database/SurvivalMode1.arz"),
         ("sm2", ROOT / "survivalmode2/database/SurvivalMode2.arz"),
         ("sm3", ROOT / "survivalmode3/database/SurvivalMode3.arz")]
M, ALL = {}, collections.defaultdict(list)
for k, p in ORDER:
    a = ArzArchive(p)
    for r in a.records:
        M[r] = (k, a); ALL[r].append(k)
def get(p):
    e = M.get(str(p)); return e[1].read_record(str(p)) if e else None

PAT = re.compile(r"^records/proxies/tier(\d+)waves/proxy_w(\d+)_p(\d+)a\.dbr$")
rows = []
for path in M:
    m = PAT.match(path)
    if not m: continue
    rows.append((int(m.group(1)), int(m.group(2)), int(m.group(3)), path))

print("=== per-tier archive provenance of wave spawn-point proxies ===")
print(f"{'tier':>4} {'waves':>5} {'pts':>4}  effective-owner counts        (all-archives-carrying counts)")
for t in range(1, 21):
    sub = [r for r in rows if r[0] == t]
    eff = collections.Counter(M[p][0] for *_x, p in sub)
    allc = collections.Counter()
    for *_x, p in sub:
        for k in ALL[p]: allc[k] += 1
    print(f"{t:4d} {len(set(r[1] for r in sub)):5d} {len(sub):4d}  {dict(eff)}   {dict(allc)}")

# ---------- difficulty pool axis
print("\n=== difficulty-scoped pool fields on wave proxies ===")
hits = []
for t, w, pt, path in rows:
    rec = get(path)
    hasE = any(f"poolEpic{i}" in rec for i in range(1, 9))
    hasL = any(f"poolLegendary{i}" in rec for i in range(1, 9))
    if hasE or hasL:
        hits.append((t, w, pt, path, hasE, hasL, rec))
print(f"wave proxies carrying poolEpic/poolLegendary: {len(hits)} of {len(rows)}")
byt = collections.Counter(h[0] for h in hits)
print("by tier:", dict(sorted(byt.items())))
byw = collections.Counter((h[0], h[1]) for h in hits)
print("by (tier,wave):", dict(sorted(byw.items())))

print("\n--- full listing ---")
for t, w, pt, path, hasE, hasL, rec in sorted(hits):
    base = [(str(rec[f"pool{i}"]), rec.get(f"weight{i}")) for i in range(1, 9) if rec.get(f"pool{i}")]
    ep = [(str(rec[f"poolEpic{i}"]), rec.get(f"weightEpic{i}")) for i in range(1, 9) if rec.get(f"poolEpic{i}")]
    lg = [(str(rec[f"poolLegendary{i}"]), rec.get(f"weightLegendary{i}")) for i in range(1, 9) if rec.get(f"poolLegendary{i}")]
    print(f"\n  tier{t:02d} w{w:02d} p{pt:02d}  (wave {(t-1)*10+w})  [{M[path][0]}]")
    for lbl, lst in (("NORMAL/Aspirant  ", base), ("EPIC/Challenger  ", ep), ("LEGEND/Gladiator ", lg)):
        for pp, ww in lst:
            pr = get(pp)
            print(f"     {lbl} w={ww:<5} {pp}  spawn {pr.get('spawnMin')}-{pr.get('spawnMax')} "
                  f"champ {pr.get('championChance')}% {pr.get('championMin')}-{pr.get('championMax')}")
json.dump([[h[0], h[1], h[2], h[3]] for h in hits], open("s3_difficulty_hits.json", "w"), indent=1)
