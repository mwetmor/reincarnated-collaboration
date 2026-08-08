#!/usr/bin/env python3
"""Final sweep: EVERY corpus record that could contribute a characterLife* term. READ-ONLY."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from t0_lib import merged, index


def s(v):
    if isinstance(v, list):
        nz = [x for x in v if isinstance(x, (int, float)) and abs(x) > 1e-9]
        return f"array len{len(v)} nz={len(nz)} i159={v[159] if len(v) > 159 else '-'}"
    return str(v)


print("=" * 110)
print("A — every record using gameadjustment.tpl / attributepak.tpl with a non-zero life modifier")
print("=" * 110)
for p in sorted(index()):
    if not p.endswith(".dbr"):
        continue
    rec, prov, own = merged(p)
    tn = str(rec.get("templateName", ""))
    if "gameadjustment" not in tn and "attributepak" not in tn:
        continue
    lm, lmm = rec.get("characterLifeModifier"), rec.get("characterLifeMultModifier")

    def nz(v):
        if isinstance(v, list):
            return any(isinstance(x, (int, float)) and abs(x) > 1e-9 for x in v)
        return isinstance(v, (int, float)) and abs(v) > 1e-9

    if nz(lm) or nz(lmm):
        print(f"\n   {p}  [{own}]  tpl={tn.split('/')[-1]}")
        print(f"       characterLifeModifier     = {s(lm)}")
        print(f"       characterLifeMultModifier = {s(lmm)}")

print("\n" + "=" * 110)
print("B — corpus-wide: who REFERENCES any balancingadjustment record?")
print("=" * 110)
n = 0
for p in sorted(index()):
    if not p.endswith(".dbr"):
        continue
    rec, _, own = merged(p)
    for f, v in rec.items():
        if isinstance(v, str) and "balancingadjustment" in v.lower():
            print(f"      {p:62s} {f:24s} -> {v.split('/')[-1]}   [{own}]")
            n += 1
print(f"   ({n} references)")
