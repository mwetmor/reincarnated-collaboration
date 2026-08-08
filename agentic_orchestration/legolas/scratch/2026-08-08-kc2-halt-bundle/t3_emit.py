#!/usr/bin/env python3
"""HALT-9 step 3: full 200-row x 3-difficulty emission over ALL non-zero fields. READ-ONLY."""
import sys, pathlib, csv, json
sys.path.insert(0, "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arz_adapter_2026_07_24 import ArzArchive

HERE = pathlib.Path(__file__).parent
ROOT = pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-II-20260724")
A = ArzArchive(ROOT / "mods/survivalmode/database/SurvivalMode.arz")
RECS = [("aspirant", "records/game/balancingadjustment_survivalmode_enemies01.dbr"),
        ("challenger", "records/game/balancingadjustment_survivalmode_enemies02.dbr"),
        ("gladiator", "records/game/balancingadjustment_survivalmode_enemies03.dbr")]
R = {d: A.read_record(p) for d, p in RECS}

NZ = json.load(open(HERE / "t2_nonzero_fields.json"))
ARR = [r["field"] for r in NZ if r["kind"] == "array"]
SCA = [r["field"] for r in NZ if r["kind"] == "scalar"]

# U-8 tier map: 200 waves / 20 tiers = 10 waves per tier (U-8 § tier map)
def tier(w):
    return (w - 1) // 10 + 1

# ---- main per-wave CSV ----
hdr = ["wave", "tier", "difficulty"] + ARR
out = HERE / "halt9_survival_wave_scaling_full.csv"
with open(out, "w", newline="") as fh:
    wr = csv.writer(fh)
    wr.writerow(hdr)
    for d, _ in RECS:
        for w in range(1, 201):
            i = w - 1
            row = [w, tier(w), d]
            for f in ARR:
                v = R[d].get(f)
                row.append(v[i] if isinstance(v, list) and i < len(v) else "")
            wr.writerow(row)
print(f"wrote {out}  ({len(ARR)} array fields x 200 waves x 3 difficulties)")

# ---- scalar sidecar ----
out2 = HERE / "halt9_survival_scalars.csv"
with open(out2, "w", newline="") as fh:
    wr = csv.writer(fh)
    wr.writerow(["difficulty", "field", "value"])
    for d, _ in RECS:
        for f in SCA:
            wr.writerow([d, f, R[d].get(f)])
print(f"wrote {out2}  ({len(SCA)} scalar fields x 3 difficulties)")

# ---- U-8 byte-match sanity ----
U8 = pathlib.Path("/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/scratch/2026-08-07-u8-tierwave/u8_survival_wave_scaling.csv")
u8rows = list(csv.DictReader(open(U8)))
u8cols = [c for c in u8rows[0] if c not in ("wave", "tier", "difficulty")]
print(f"\n== U-8 CROSS-CHECK: {len(u8rows)} rows, cols={u8cols} ==")
newrows = list(csv.DictReader(open(out)))
idx = {(r["wave"], r["difficulty"]): r for r in newrows}
mismatch = 0
tiermis = 0
for r in u8rows:
    k = (r["wave"], r["difficulty"])
    n = idx.get(k)
    if n is None:
        print(f"  MISSING {k}"); mismatch += 1; continue
    if n["tier"] != r["tier"]:
        tiermis += 1
    for c in u8cols:
        a, b = r[c], n.get(c, "")
        if abs(float(a) - float(b)) > 1e-9:
            print(f"  MISMATCH {k} {c}: u8={a} new={b}"); mismatch += 1
print(f"  value mismatches: {mismatch}   tier-column mismatches: {tiermis}")
print("  VERDICT:", "IDENTICAL on all 9 U-8 columns" if mismatch == 0 else "DIVERGENT")

# ---- key waves table ----
KEY = [1, 10, 50, 100, 130, 140, 150, 159, 160, 161, 170, 180, 190, 200]
print("\n== KEY-WAVE TABLE (the waves the spec binds at) ==")
for f in ARR:
    line = f"{f:38s}"
    for d, _ in RECS:
        v = R[d][f]
        line += " | " + " ".join(f"{v[w-1]:g}" for w in KEY)
    print(line)
print(f"\n  columns per difficulty: waves {KEY}")

# ---- retaliation deep-dive (source conflict F-4) ----
print("\n== retaliationTotalDamageModifier — full profile ==")
f = "retaliationTotalDamageModifier"
for d, _ in RECS:
    v = R[d][f]
    # find first wave where value hits certain marks
    marks = {}
    for target in (16, 22, 24, 53, 54, 74, 77, 110):
        hits = [w for w in range(1, 201) if abs(v[w - 1] - target) < 1e-9]
        if hits:
            marks[target] = (min(hits), max(hits))
    print(f"  {d:11s} w1={v[0]:g} w100={v[99]:g} w160={v[159]:g} w200={v[199]:g}  distinct={len(set(v))}")
    print(f"              value->wave-range: " + ", ".join(f"{t}@w{a}-{b}" for t, (a, b) in sorted(marks.items())))
# step profile for gladiator
v = R[f'gladiator'][f] if False else R["gladiator"][f]
steps = [(w, v[w - 1]) for w in range(1, 201) if w == 1 or v[w - 1] != v[w - 2]]
print(f"  gladiator step points (wave,value): {steps}")
