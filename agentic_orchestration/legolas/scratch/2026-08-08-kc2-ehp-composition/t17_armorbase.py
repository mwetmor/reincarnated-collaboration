#!/usr/bin/env python3
"""The armorbase passive layer: which record, which rank, what characterLifeModifier. READ-ONLY."""
import sys, pathlib, json
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from t0_lib import merged, index

OUT = pathlib.Path(__file__).parent
chain = json.load(open(OUT / "t3_chain.json"))["chain"]

print("=" * 110)
print("A — armorbase* passives: characterLifeModifier by array index")
print("=" * 110)
AB = sorted(p for p in index() if "nonplayerskills/passive/armorbase" in p)
arrs = {}
print(f"{'record':16s} {'FileDescription':34s} " + " ".join(f"i{i:<5d}" for i in (100, 103, 105, 106, 108, 110, 111, 118, 119)))
for p in AB:
    rec, prov, own = merged(p)
    v = rec.get("characterLifeModifier")
    arrs[p.split('/')[-1].replace('.dbr', '')] = v
    if isinstance(v, list):
        print(f"{p.split('/')[-1]:16s} {str(rec.get('FileDescription'))[:32]:34s} "
              + " ".join(f"{v[i]:<6.0f}" for i in (100, 103, 105, 106, 108, 110, 111, 118, 119)))

print("\n" + "=" * 110)
print("B — which armorbase passive, at which skillLevel equation, per wave-160 roster record")
print("=" * 110)
rows = {}
for p, e in sorted(chain.items(), key=lambda kv: kv[1]["desc"] or kv[0]):
    rec, prov, own = merged(p)
    who = e["desc"] or p.split("/")[-1].replace(".dbr", "")
    for i in range(1, 30):
        sn = rec.get(f"skillName{i}")
        if isinstance(sn, str) and "armorbase" in sn.lower():
            lvl = rec.get(f"skillLevel{i}")
            rows[p] = (who, sn.split('/')[-1].replace('.dbr', ''), f"skillLevel{i}", lvl)
            print(f"   {who[:42]:44s} {sn.split('/')[-1]:16s} skillLevel{i} = {lvl!r}")
            break
    else:
        print(f"   {who[:42]:44s} -- no armorbase skill --")

json.dump({"arrays": {k: v for k, v in arrs.items()},
           "assign": {k: list(v) for k, v in rows.items()}},
          open(OUT / "t17_armorbase.json", "w"), indent=1, default=str)

print("\n" + "=" * 110)
print("C — full chain WITH the armorbase term, evaluated")
print("=" * 110)
F = {"F1": 3722896.0, "F2": 2955796.0, "F3": 2295755.0}
ULT, GLAD = 580.0, 324.0
LVBAND = {"records/proxies/lv8_boss+.dbr": (106, 106),
          "records/proxies/lv7_uber hero.dbr": (103, 105),
          "records/proxies/lv6_hero.dbr": (104, 105)}
roster = json.load(open(OUT / "t1_roster.json"))
PROXY_FOR = {p: [v for k, v in d["lvkeys"].items() if "levelVarianceEquation" in k][0]
             for p, d in roster.items()}

out = []
for p, e in chain.items():
    if p not in rows:
        continue
    who, abrec, slkey, sleq = rows[p]
    lifeq = json.load(open(OUT / "t3_chain.json"))["bios"][e["bio"].lower()]["fields"]["characterLife"].replace("^", "**")
    lo, hi = LVBAND[PROXY_FOR[p]]
    for sl in sorted({lo, hi}):
        cl = eval(e["charLevel"], {}, {"charLevel": float(sl)})
        base = eval(lifeq, {}, {"charLevel": cl})
        rank = eval(str(sleq), {}, {"charLevel": cl}) if isinstance(sleq, str) else float(sleq or 0)
        idx = max(0, min(199, int(rank) - 1))          # rank r -> array index r-1
        idx0 = max(0, min(199, int(rank)))             # rank r -> array index r
        ab = arrs[abrec]
        own = e.get("characterLifeModifier") or 0.0
        for lbl, ix in (("rank-1", idx), ("rank", idx0)):
            M = 1 + ULT / 100 + GLAD / 100 + own / 100 + ab[ix] / 100
            ehp = base * M
            best = min(F.items(), key=lambda kv: abs(ehp / kv[1] - 1))
            out.append((who, sl, cl, abrec, rank, lbl, ab[ix], M, base, ehp,
                        best[0], ehp / best[1] - 1))

out.sort(key=lambda r: -r[9])
print(f"{'who':34s} {'cl':>7s} {'ab':>12s} {'rank':>7s} {'idxmode':8s} {'abVal':>6s} {'M':>7s} {'eHP':>13s}  near")
for r in out:
    if r[5] != "rank-1":
        continue
    print(f"{r[0][:32]:34s} {r[2]:7.2f} {r[3]:>12s} {r[4]:7.1f} {r[5]:8s} {r[6]:6.0f} {r[7]:7.2f} "
          f"{r[9]:>13,.0f}  {r[10]} {r[11]*100:+7.2f}%")
