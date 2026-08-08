#!/usr/bin/env python3
"""
EXHAUSTIVE M-CONSISTENCY ENUMERATION.

The wave-160 board is exactly one body per spawn point: {p01 nemesis, p02 nemesis, p03 nemesis,
p04 superboss, p06 hero}. The three measured fingerprints must be three of those five, each with
its OWN DB-permitted charLevel, all sharing ONE global multiplier M.

Enumerate every (record x permitted level) realisation, one per spawn point, choose 3, and score
the spread of the three implied M values. NO fitting: M is not a free parameter per fingerprint,
it is required to be common, and the spread is the falsifier.
READ-ONLY.
"""
import sys, json, pathlib, itertools, math
sys.path.insert(0, str(pathlib.Path(__file__).parent))

OUT = pathlib.Path(__file__).parent
chain = json.load(open(OUT / "t3_chain.json"))
roster = json.load(open(OUT / "t1_roster.json"))

F = [3722896.0, 2955796.0, 2295755.0]
APL = 100

LVPROXY = {                                 # (min, max) at apl=100, integer division
    "records/proxies/lv8_boss+.dbr":     (106, 106),
    "records/proxies/lv7_uber hero.dbr": (103, 105),
    "records/proxies/lv6_hero.dbr":      (104, 105),
}

PROXY_FOR = {}
for p, v in roster.items():
    for k, vv in v["lvkeys"].items():
        if "levelVarianceEquation" in k:
            PROXY_FOR[p] = vv


def point_of(p):
    return roster[p]["pools"][0].split(":")[0]


bios = chain["bios"]
cands = []                                   # (point, label, base_life, meta)
for p, e in chain["chain"].items():
    proxy = PROXY_FOR[p]
    lifeq = bios[e["bio"].lower()]["fields"]["characterLife"].replace("^", "**")
    lo, hi = LVPROXY[proxy]
    own_mod = e.get("characterLifeModifier") or 0.0
    for pool in roster[p]["pools"]:
        pt = pool.split(":")[0][:3]
        for sl in sorted({lo, hi}):
            for trunc in (True, False):
                clr = eval(e["charLevel"], {}, {"charLevel": float(sl)})
                cl = math.floor(clr) if trunc else clr
                base = eval(lifeq, {}, {"charLevel": float(cl)})
                cands.append({"point": pt, "record": p, "desc": e["desc"] or p.split("/")[-1],
                              "bio": e["bio"].split("/")[-1], "spawn": sl, "cl": cl,
                              "trunc": trunc, "base": base, "own_life_mod": own_mod})

print(f"{len(cands)} candidate realisations across points "
      f"{sorted({c['point'] for c in cands})}")

# group by spawn point
BY = {}
for c in cands:
    BY.setdefault(c["point"], []).append(c)
for k in sorted(BY):
    print(f"   {k}: {len(BY[k])} realisations, base range "
          f"{min(x['base'] for x in BY[k]):,.0f} .. {max(x['base'] for x in BY[k]):,.0f}")

print("\n" + "=" * 112)
print("ENUMERATION — pick 3 distinct spawn points, assign F1>F2>F3, require ONE common M")
print("=" * 112)

results = []
pts = sorted(BY)
for tri in itertools.combinations(pts, 3):
    for perm in itertools.permutations(tri):
        for a in BY[perm[0]]:
            for b in BY[perm[1]]:
                for c in BY[perm[2]]:
                    m = [F[0] / a["base"], F[1] / b["base"], F[2] / c["base"]]
                    spread = max(m) / min(m) - 1
                    results.append((spread, sum(m) / 3, a, b, c))
results.sort(key=lambda x: x[0])

seen = set()
shown = 0
for spread, mbar, a, b, c in results:
    key = (a["record"], b["record"], c["record"])
    if key in seen:
        continue
    seen.add(key)
    print(f"\n  spread {spread*100:6.3f}%   M_mean = {mbar:.4f}")
    for tag, x, fv in (("F1", a, F[0]), ("F2", b, F[1]), ("F3", c, F[2])):
        print(f"    {tag} {fv:>10,.0f}  {x['point']}  {x['desc'][:38]:40s} {x['bio'][:34]:36s} "
              f"spawn={x['spawn']} cl={x['cl']:g} base={x['base']:>10,.0f} M={fv/x['base']:.4f}")
    shown += 1
    if shown >= 8:
        break

json.dump([{"spread": r[0], "M": r[1],
            "F1": r[2]["desc"], "F2": r[3]["desc"], "F3": r[4]["desc"],
            "cl": [r[2]["cl"], r[3]["cl"], r[4]["cl"]]} for r in results[:400]],
          open(OUT / "t8_top.json", "w"), indent=1, default=str)
print("\nwrote t8_top.json")
