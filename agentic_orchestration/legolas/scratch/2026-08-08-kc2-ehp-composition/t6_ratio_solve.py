#!/usr/bin/env python3
"""
DECISIVE TEST — ratios are multiplier-invariant.

If a single global multiplier M closes the chain, then for the three measured fingerprints
    F1=3,722,896  F2=2,955,796  F3=2,295,755
there must exist three roster records whose BASE life values sit in the same ratios.
This test cannot be fitted: M cancels.

READ-ONLY. No external fetch.
"""
import sys, json, pathlib, itertools, math
sys.path.insert(0, str(pathlib.Path(__file__).parent))

OUT = pathlib.Path(__file__).parent
chain = json.load(open(OUT / "t3_chain.json"))

APL = 100                                   # fixture player level (L100)

# levelVarianceEquation proxies, DB-CITED (t3 §A)
LVPROXY = {
    "records/proxies/lv8_boss+.dbr":     ("(apl+4)+(apl//50)", "(apl+4)+(apl//50)"),
    "records/proxies/lv7_uber hero.dbr": ("(apl+3)",           "(apl+3)+(apl//50)"),
    "records/proxies/lv6_hero.dbr":      ("(apl+2)+(apl//50)", "(apl+3)+(apl//50)"),
}


def lvl_band(proxy, apl=APL, intdiv=True):
    lo, hi = LVPROXY[proxy]
    d = apl // 50 if intdiv else apl / 50
    env = {"apl": apl}
    lo = eval(lo.replace("apl//50", str(d)).replace("apl/50", str(d)), {}, env)
    hi = eval(hi.replace("apl//50", str(d)).replace("apl/50", str(d)), {}, env)
    return lo, hi


def eval_charlevel(expr, spawn_level):
    return eval(expr, {}, {"charLevel": float(spawn_level)})


def eval_life(expr, cl):
    # equations use ^ for power
    e = expr.replace("^", "**")
    return eval(e, {}, {"charLevel": float(cl)})


# proxy assignment per record (from t1)
PROXY_FOR = {}
roster = json.load(open(OUT / "t1_roster.json"))
for p, v in roster.items():
    for k, vv in v["lvkeys"].items():
        if "levelVarianceEquation" in k:
            PROXY_FOR[p] = vv

bios = chain["bios"]
rows = []
for p, e in chain["chain"].items():
    proxy = PROXY_FOR.get(p)
    if not proxy:
        print(f"  !! no proxy for {p}")
        continue
    lifeq = bios[e["bio"].lower()]["fields"]["characterLife"]
    lo, hi = lvl_band(proxy)
    for trunc in (True, False):
        for sl in sorted({lo, hi}):
            cl_raw = eval_charlevel(e["charLevel"], sl)
            cl = math.floor(cl_raw) if trunc else cl_raw
            rows.append({
                "record": p, "desc": e["desc"], "cls": e["cls"], "pools": roster[p]["pools"],
                "proxy": proxy, "spawn_level": sl, "charLevel_eq": e["charLevel"],
                "charLevel": cl, "trunc": trunc, "life_eq": lifeq,
                "base_life": eval_life(lifeq, cl)})

print("=" * 118)
print(f"BASE LIFE TABLE — apl={APL}, all plausible level realisations")
print("=" * 118)
print(f"{'record':58s} {'proxy lvl':>9s} {'charLev':>9s} {'T':>2s} {'base_life':>14s}")
for r in sorted(rows, key=lambda x: -x["base_life"]):
    print(f"{r['record'].split('/')[-1][:56]:58s} {r['spawn_level']:>9} {r['charLevel']:>9.2f} "
          f"{'Y' if r['trunc'] else 'n':>2s} {r['base_life']:>14,.0f}")

# ---------------- ratio test ----------------
F = [3722896.0, 2955796.0, 2295755.0]
print("\n" + "=" * 118)
print("RATIO TEST — measured fingerprint ratios that any correct chain must reproduce")
print("=" * 118)
print(f"   F1/F2 = {F[0]/F[1]:.5f}    F2/F3 = {F[1]/F[2]:.5f}    F1/F3 = {F[0]/F[2]:.5f}")

# distinct base values
uniq = {}
for r in rows:
    uniq.setdefault(round(r["base_life"], 3), []).append(r)
vals = sorted(uniq)
print(f"\n   {len(vals)} distinct base-life values across {len(rows)} realisations")

print("\n== TRIPLES whose base-life ratios match all three measured ratios within tol ==")
best = []
for a, b, c in itertools.permutations(vals, 3):
    if not (a > b > c):
        continue
    e1 = abs((a / b) / (F[0] / F[1]) - 1)
    e2 = abs((b / c) / (F[1] / F[2]) - 1)
    e3 = abs((a / c) / (F[0] / F[2]) - 1)
    worst = max(e1, e2, e3)
    best.append((worst, a, b, c, e1, e2, e3))
best.sort()
for worst, a, b, c, e1, e2, e3 in best[:12]:
    print(f"\n   max-err {worst*100:6.3f}%   base=({a:,.0f} / {b:,.0f} / {c:,.0f})")
    print(f"       implied M: {F[0]/a:.4f} , {F[1]/b:.4f} , {F[2]/c:.4f}")
    for v, tag in ((a, "F1"), (b, "F2"), (c, "F3")):
        for r in uniq[round(v, 3)][:3]:
            print(f"       {tag}: {r['desc'] or r['record'].split('/')[-1]:44s} "
                  f"cl={r['charLevel']:.2f} T={'Y' if r['trunc'] else 'n'} pools={r['pools']}")

json.dump(rows, open(OUT / "t6_base_life.json", "w"), indent=1, default=str)
print("\nwrote t6_base_life.json")
