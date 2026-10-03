#!/usr/bin/env python3
"""barrow_v2 paint lane (BVP, drax): THE GREAT DOOR'S GABLED PORCH (conductor ruling, BVP brief).

    python3 tools/bvp_porch.py            print the porch feature + its clearances (no write)
    python3 tools/bvp_porch.py --apply    add/replace feature `hall_porch` in layout_v2.json, then the
                                          caller re-runs tools/validate_layout_v2.py (must stay all-PASS)

Why: at zero yaw the hall's floor-facing wall faces NW (312.99 deg), away from the camera, and the 6.5 m
hall hides the door. A camera at the south, 52.95 deg down, sees only south-facing faces and roofs. So the
door gets its own gabled porch projecting from the long west wall toward p04's patch: its ridge runs
OUT from the wall (perpendicular to it), so its roof reaches north of the hall's own silhouette and shows
above the hall's ridge line on screen; its double doors stand open at the porch mouth; smoke rolls out.

Geometry: the porch is centred a little NE of the door (the floor's p04 arc curves AWAY from the wall to
the NE, so the clearance grows that way) and still spans the door. It is a blocker, OUTSIDE the floor
with >= MIN_CLEAR_M clearance (R5 needs zero area inside; this keeps a visible strip of yard too).
"""
import json, math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
LAY = os.path.join(os.path.dirname(HERE), "layout_v2.json")
DEPTH_M, WIDTH_M, SHIFT_NE_M = 2.4, 3.6, 0.8
EAVE_Z, RIDGE_Z = 3.4, 5.0
MIN_CLEAR_M = 0.5


def dseg(p, a, b):
    dx, dy = b[0] - a[0], b[1] - a[1]
    t = max(0.0, min(1.0, ((p[0] - a[0]) * dx + (p[1] - a[1]) * dy) / (dx * dx + dy * dy)))
    return math.hypot(p[0] - a[0] - t * dx, p[1] - a[1] - t * dy)


def inside(p, poly):
    c = False
    for i in range(len(poly)):
        (x1, y1), (x2, y2) = poly[i], poly[(i + 1) % len(poly)]
        if (y1 > p[1]) != (y2 > p[1]) and p[0] < x1 + (p[1] - y1) * (x2 - x1) / (y2 - y1):
            c = not c
    return c


def porch(L):
    hall = next(f for f in L["features"] if f["id"] == "longhall")["footprint"]
    door = next(f for f in L["features"] if f["id"] == "hall_great_door")
    a, b = hall[0], hall[1]                                   # the long west wall, SW -> NE
    L_ = math.hypot(b[0] - a[0], b[1] - a[1])
    u = ((b[0] - a[0]) / L_, (b[1] - a[1]) / L_)              # along the wall, toward NE
    n = (u[1], -u[0])                                         # outward normal (NW, toward the floor)
    if n[0] > 0:
        n = (-n[0], -n[1])
    dc = [sum(p[0] for p in door["footprint"]) / 4, sum(p[1] for p in door["footprint"]) / 4]
    t0 = (dc[0] - a[0]) * u[0] + (dc[1] - a[1]) * u[1]       # the door's station on the wall line
    base = (a[0] + u[0] * t0, a[1] + u[1] * t0)
    c = (base[0] + u[0] * SHIFT_NE_M, base[1] + u[1] * SHIFT_NE_M)
    hw = WIDTH_M / 2
    fp = [[c[0] - u[0] * hw, c[1] - u[1] * hw],
          [c[0] + u[0] * hw, c[1] + u[1] * hw],
          [c[0] + u[0] * hw + n[0] * DEPTH_M, c[1] + u[1] * hw + n[1] * DEPTH_M],
          [c[0] - u[0] * hw + n[0] * DEPTH_M, c[1] - u[1] * hw + n[1] * DEPTH_M]]
    fp = [[round(x, 4), round(y, 4)] for x, y in fp]
    mouth = [round(c[0] + n[0] * DEPTH_M, 4), round(c[1] + n[1] * DEPTH_M, 4)]
    faces = (math.degrees(math.atan2(n[0], -n[1])) + 360) % 360
    return {
        "id": "hall_porch", "kind": "porch", "footprint": fp, "z_bottom_m": 0.0, "z_top_m": RIDGE_Z,
        "eave_z_m": EAVE_Z, "ridge_z_m": RIDGE_Z, "ridge": "perpendicular to the hall wall, running OUT toward p04",
        "mouth_centre": mouth, "faces_deg": round(faces, 2),
        "blocks_movement": True, "blocks_sight": True, "placement": "OUTSIDE the walkable edge",
        "note": ("the great door's gabled porch (conductor ruling, BVP): at zero yaw the hall's floor-facing wall "
                 "faces away from the camera and the hall hides the door, so the porch's own roof, projecting out "
                 "of the wall toward p04's patch, marks the entrance from above; the double doors stand open at its "
                 "mouth and smoke rolls out over its roof (p04: out of smoke)"),
    }


def main():
    L = json.load(open(LAY))
    F = [tuple(p) for p in L["floor"]["polygon"]]
    f = porch(L)
    clear = min(min(dseg(p, F[i], F[(i + 1) % len(F)]) for i in range(len(F))) for p in f["footprint"])
    # sample the porch's edges too (a convex floor can come closest mid-edge)
    fp = f["footprint"]
    for i in range(4):
        a, b = fp[i], fp[(i + 1) % 4]
        for k in range(21):
            q = (a[0] + (b[0] - a[0]) * k / 20, a[1] + (b[1] - a[1]) * k / 20)
            if inside(q, F):
                sys.exit(f"porch point {q} is INSIDE the floor")
            clear = min(clear, min(dseg(q, F[j], F[(j + 1) % len(F)]) for j in range(len(F))))
    f["clearance_to_floor_m"] = round(clear, 3)
    print(json.dumps(f, indent=1))
    if clear < MIN_CLEAR_M:
        sys.exit(f"clearance {clear:.3f} < {MIN_CLEAR_M}")
    if "--apply" in sys.argv:
        L["features"] = [g for g in L["features"] if g["id"] != "hall_porch"]
        i = next(k for k, g in enumerate(L["features"]) if g["id"] == "hall_great_door")
        L["features"].insert(i + 1, f)
        json.dump(L, open(LAY, "w"), indent=2, ensure_ascii=False)
        print("applied to", LAY)


if __name__ == "__main__":
    main()
