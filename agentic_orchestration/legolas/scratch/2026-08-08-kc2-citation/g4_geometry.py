#!/usr/bin/env python3
"""F-12a — arena geometry summary. The reference frame is the PatrolPoint_Attack centroid (the
convergence zone every non-ambush Crucible spawn is sent to by survivalevent.lua:553), NOT the
`playerspawnpoint` (which is the level ENTRY, tens of metres outside the arena). READ-ONLY."""
import csv, math, collections, re

PP = collections.defaultdict(list)
for r in csv.DictReader(open("kc2_crucible_patrolpoints.csv")):
    PP[(r["arena_archive"], r["arena_map"])].append((float(r["x"]), float(r["y"]), float(r["z"])))

PL = collections.defaultdict(list)
for r in csv.DictReader(open("kc2_crucible_arena_placements.csv")):
    PL[(r["arena_archive"], r["arena_map"])].append(r)

EM = re.compile(r"(spawnpoint0[2-6])\.dbr$|(tier\d\dspawnpoint01)\.dbr$")
out = []
print(f"{'arena':34s} {'tag':22s} {'emit sites':>10s} {'r_min':>7s} {'r_mean':>7s} {'r_max':>7s} "
      f"{'patrol r_max':>12s} {'p05 r':>7s}")
for k in sorted(PL):
    pts = PP.get(k)
    if not pts: continue
    cx = sum(p[0] for p in pts) / len(pts); cz = sum(p[2] for p in pts) / len(pts)
    prad = [math.hypot(p[0] - cx, p[2] - cz) for p in pts]
    sites, p05r = {}, None
    for r in PL[k]:
        m = EM.search(r["record"])
        if not m: continue
        nm = m.group(1) or m.group(2)
        x, z = float(r["x"]), float(r["z"])
        d = math.hypot(x - cx, z - cz)
        brg = (math.degrees(math.atan2(x - cx, z - cz)) + 360) % 360
        # p01 is placed PER TIER (spread up to 17 m across tiers) -> keyed per tier, never collapsed
        key = ("p01_tier" + nm[4:6]) if nm.startswith("tier") else "p" + nm[-2:]
        sites.setdefault(key, (x, z, d, brg))
        if key == "p05": p05r = d
    if not sites: continue
    ds = [v[2] for v in sites.values()]
    print(f"{k[0]+'/'+k[1]:34s} {'':22s} {len(sites):>10d} {min(ds):7.2f} "
          f"{sum(ds)/len(ds):7.2f} {max(ds):7.2f} {max(prad):12.2f} "
          f"{(f'{p05r:7.2f}' if p05r else '      -')}")
    for key in sorted(sites):
        x, z, d, brg = sites[key]
        oc = (brg / 30) % 12 or 12
        out.append(dict(arena_archive=k[0], arena_map=k[1], emitter=key,
                        x=round(x, 3), z=round(z, 3),
                        arena_centre_x=round(cx, 3), arena_centre_z=round(cz, 3),
                        arena_centre_basis="centroid of the PatrolPoint_Attack group",
                        radius_m=round(d, 3), bearing_deg=round(brg, 2), oclock=round(oc, 2),
                        patrol_r_min=round(min(prad), 3), patrol_r_mean=round(sum(prad)/len(prad), 3),
                        patrol_r_max=round(max(prad), 3), n_patrol_points=len(pts)))

with open("kc2_crucible_emitter_geometry.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(out[0])); w.writeheader(); w.writerows(out)
print(f"\n[wrote] kc2_crucible_emitter_geometry.csv  {len(out)} rows")

print("\n=== EMITTER RADII, all arenas pooled (the F-12a parameter) ===")
rr = [o["radius_m"] for o in out]
rr.sort()
print(f"  n={len(rr)}  min={rr[0]:.2f}  p25={rr[len(rr)//4]:.2f}  median={rr[len(rr)//2]:.2f}  "
      f"p75={rr[3*len(rr)//4]:.2f}  max={rr[-1]:.2f}  mean={sum(rr)/len(rr):.2f} m")
print(f"  build's UNCITED Arena.emitter_radius_m = 30.0  ->  percentile "
      f"{100*sum(1 for v in rr if v < 30.0)/len(rr):.1f} % of measured emitter radii are below it")

print("\n=== per-emitter-slot across arenas ===")
byslot = collections.defaultdict(list)
for o in out: byslot[o["emitter"]].append(o["radius_m"])
for s in sorted(byslot):
    v = sorted(byslot[s])
    print(f"  {s}  n={len(v):2d}  min={v[0]:7.2f}  median={v[len(v)//2]:7.2f}  max={v[-1]:7.2f} m")
