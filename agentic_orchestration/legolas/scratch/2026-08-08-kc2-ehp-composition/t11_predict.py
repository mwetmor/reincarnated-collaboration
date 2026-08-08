#!/usr/bin/env python3
"""
DEFINITIVE PREDICTION TABLE — full DB-cited chain, every wave-160 roster record,
under each candidate composition rule. Residual reported per fingerprint. NO FITTING.
READ-ONLY.
"""
import sys, json, pathlib, math, csv
sys.path.insert(0, str(pathlib.Path(__file__).parent))

OUT = pathlib.Path(__file__).parent
chain = json.load(open(OUT / "t3_chain.json"))
roster = json.load(open(OUT / "t1_roster.json"))

F = {"F1": 3722896.0, "F2": 2955796.0, "F3": 2295755.0}
APL = 100
ULT = 580.0                       # mp+difficulty_enemies01.characterLifeModifier[8]  (Ultimate,1P)
GLAD_159 = 324.0                  # survivalmode_enemies03.characterLifeModifier[159]
GLAD_158 = 322.0                  # ...[158]

LVBAND = {"records/proxies/lv8_boss+.dbr": (106, 106),
          "records/proxies/lv7_uber hero.dbr": (103, 105),
          "records/proxies/lv6_hero.dbr": (104, 105)}
PROXY_FOR = {p: [v for k, v in d["lvkeys"].items() if "levelVarianceEquation" in k][0]
             for p, d in roster.items()}

rows = []
for p, e in chain["chain"].items():
    lifeq = chain["bios"][e["bio"].lower()]["fields"]["characterLife"].replace("^", "**")
    lo, hi = LVBAND[PROXY_FOR[p]]
    own = e.get("characterLifeModifier") or 0.0
    for sl in sorted({lo, hi}):
        clr = eval(e["charLevel"], {}, {"charLevel": float(sl)})
        for tag, cl in (("float", clr), ("floor", float(math.floor(clr)))):
            base = eval(lifeq, {}, {"charLevel": cl})
            for gname, g in (("w160(i159)", GLAD_159), ("w159/i158", GLAD_158)):
                M = 1 + ULT / 100 + g / 100 + own / 100
                rows.append({"point": roster[p]["pools"][0].split(":")[0][:3],
                             "who": e["desc"] or p.split("/")[-1].replace(".dbr", ""),
                             "record": p, "bio": e["bio"].split("/")[-1].replace(".dbr", ""),
                             "life_eq": chain["bios"][e["bio"].lower()]["fields"]["characterLife"],
                             "charLevel_eq": e["charLevel"], "spawn": sl,
                             "cl_mode": tag, "charLevel": cl, "own_lifemod": own,
                             "glad_src": gname, "M": M, "base_life": base, "eHP": base * M})

with open(OUT / "t11_predicted_ehp.csv", "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0]))
    w.writeheader()
    w.writerows(rows)

print("=" * 122)
print("PREDICTED eHP — chain: characterLife(bio, charLevel) x (1 + 5.80[Ultimate] + G/100[Gladiator wave] + own/100)")
print("=" * 122)
sel = [r for r in rows if r["cl_mode"] == "float" and r["glad_src"] == "w160(i159)"]
sel.sort(key=lambda r: -r["eHP"])
print(f"{'pt':4s} {'who':38s} {'bio':30s} {'cl':>7s} {'M':>7s} {'base':>10s} {'eHP':>12s}  nearest F")
for r in sel:
    best = min(F.items(), key=lambda kv: abs(r["eHP"] / kv[1] - 1))
    err = r["eHP"] / best[1] - 1
    flag = f"{best[0]} {err*100:+7.3f}%" if abs(err) < 0.20 else ""
    print(f"{r['point']:4s} {r['who'][:36]:38s} {r['bio'][:28]:30s} {r['charLevel']:7.2f} {r['M']:7.2f} "
          f"{r['base_life']:>10,.0f} {r['eHP']:>12,.0f}  {flag}")

print("\n" + "=" * 122)
print("RESIDUAL TABLE — best DB-permitted realisation per fingerprint, all four rule variants")
print("=" * 122)
for glad in ("w160(i159)", "w159/i158"):
    for mode in ("float", "floor"):
        sub = [r for r in rows if r["cl_mode"] == mode and r["glad_src"] == glad]
        print(f"\n  -- Gladiator term {glad}   charLevel {mode}")
        for k, fv in F.items():
            b = min(sub, key=lambda r: abs(r["eHP"] / fv - 1))
            print(f"     {k} {fv:>10,.0f}  best = {b['who'][:34]:36s} ({b['point']}, cl={b['charLevel']:.2f}) "
                  f"pred {b['eHP']:>11,.0f}   err {(b['eHP']/fv-1)*100:+7.3f}%")

print("\n" + "=" * 122)
print("EXACT-M BACK-SOLVE — what multiplier each fingerprint demands at its DB-permitted level")
print("=" * 122)
for k, fv in F.items():
    print(f"\n  {k} = {fv:,.0f}")
    cands = sorted({(r["who"], r["point"], r["charLevel"], r["base_life"])
                    for r in rows if r["cl_mode"] == "float"}, key=lambda x: -x[3])
    for who, pt, cl, base in cands:
        M = fv / base
        if 8.0 < M < 14.0:
            print(f"     {who[:36]:38s} ({pt}, cl={cl:6.2f}) base={base:>10,.0f}  ->  M = {M:8.5f}"
                  f"   [1+5.80+G => G = {(M-1-5.80)*100:7.2f}]")

print("\nwrote t11_predicted_ehp.csv")
