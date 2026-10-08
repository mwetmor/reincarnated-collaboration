#!/usr/bin/env python3
"""BV2F lane PT, DEV-22 (R-C9-216): THE STAIR'S TREAD SNOW -- the grids a second SnowFieldTerrain (DEV-18's terrain snow,
scripts/bv2f/snow_field_terrain.gd; v1's snow_field.gd untouched) needs to lay TRUE 3D snow on each tread top of the
sea-cave stair and nowhere else: bare stone fronts (sketch A's look), his footprints and puffs as he climbs.
    python3 fid/pt/tools/stair_snow_prep.py [--treads fid/lv/art/stair_treads.json] [--level <level.json>] [--out DIR]
SOURCE: LV's fid/lv/art/stair_treads.json (id, height, outline) when it exists; else the level's own tread prisms
(level.json sim.slabs.stair_treads: poly in sim x/y, top z1) -- stated in the output.
GRIDS (world xz, square cells CELL m, covering the field's AREA exactly -- the terrain snow's plane UV IS this layout):
  depth mul  1 on the tread top inset INSET_M from its edges, ramping to 0 over FEATHER_M toward the edge; 0 off the
             treads (the snow is cut there: the fronts stay bare);
  trodden    0;
  ground h   the tread top (world y) on each tread; off the treads the NEAREST tread's top (no sheet plunging between).
Sim -> world (bv2f_prep.py): u = x, v = -y; world x = u cos47 - v sin47, z = -u sin47 - v cos47; y = z (asserted in Godot
by the test tool against the Level node's own transform)."""
import hashlib, json, math, os, sys
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage

FID = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
GODOT = os.path.abspath(os.path.join(FID, "..", "..", "barrow_full", "godot"))
_a = sys.argv[1:]
arg = lambda k, d: _a[_a.index(k) + 1] if k in _a else d
TREADS = arg("--treads", os.path.join(FID, "lv", "art", "stair_treads.json"))
LEVEL = arg("--level", os.path.join(GODOT, "data", "bv2f", "art", "level.json"))
OUT = arg("--out", os.path.join(GODOT, "data", "bv2f", "stair_snow"))
CELL = 0.02
MARGIN = 1.5
INSET_M = 0.03
FEATHER_M = 0.05
FIELD_M_PER_PX = 0.01
C47, S47 = math.cos(math.radians(47.0)), math.sin(math.radians(47.0))
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()


def to_world(x, y):
    u, v = x, -y
    return u * C47 - v * S47, -u * S47 - v * C47


def main():
    treads, source = [], None
    if os.path.exists(TREADS):
        J = json.load(open(TREADS))
        items = J["treads"] if isinstance(J, dict) and "treads" in J else J
        for t in items:
            if "outline_uv" in t:   # LV's schema (R-C9-216): v1 (u, v) metres, z_m = the tread top; sim x = u, y = -v
                treads.append({"id": str(t["id"]), "top": float(t["z_m"]), "poly": [(float(p[0]), -float(p[1])) for p in t["outline_uv"]]})
            else:
                treads.append({"id": str(t["id"]), "top": float(t["height"]), "poly": [(float(p[0]), float(p[1])) for p in t["outline"]]})
        source = {"file": TREADS, "sha256": sha(TREADS), "_": "LV's stair_treads.json (outline_uv in v1 (u, v) m, z_m = top)"}
    else:
        L = json.load(open(LEVEL))
        for i, t in enumerate(L["sim"]["slabs"]["stair_treads"]["items"]):
            treads.append({"id": "tread_%03d" % i, "top": float(t["z1"]), "poly": [(float(p[0]), float(p[1])) for p in t["poly"]]})
        source = {"file": LEVEL, "sha256": sha(LEVEL), "_": "INTERIM: the level's own tread prisms (sim.slabs.stair_treads, top = z1) -- LV's stair_treads.json not yet exported"}
    W = [np.array([to_world(x, y) for x, y in t["poly"]]) for t in treads]
    allp = np.concatenate(W)
    x0, z0 = allp.min(0) - MARGIN
    x1, z1 = allp.max(0) + MARGIN
    side = max(x1 - x0, z1 - z0)
    n = int(math.ceil(side / CELL))
    side = n * CELL
    # rasterise each tread (world xz -> grid px), its id and top
    idm = Image.new("I", (n, n), 0)
    dr = ImageDraw.Draw(idm)
    for k, w in enumerate(W):
        dr.polygon([((p[0] - x0) / CELL, (p[1] - z0) / CELL) for p in w], fill=k + 1)
    ID = np.asarray(idm, np.int32)                 # row = z, col = x
    on = ID > 0
    tops = np.array([0.0] + [t["top"] for t in treads])
    # depth mul: distance inside the tread's edge (to the nearest pixel NOT of the same tread)
    mul = np.zeros((n, n), np.float32)
    for k in range(1, len(treads) + 1):
        m = ID == k
        if not m.any():
            continue
        ys, xs = np.nonzero(m)
        a0, a1, b0, b1 = max(ys.min() - 2, 0), min(ys.max() + 3, n), max(xs.min() - 2, 0), min(xs.max() + 3, n)
        d = ndimage.distance_transform_edt(m[a0:a1, b0:b1]) * CELL
        mul[a0:a1, b0:b1] = np.where(m[a0:a1, b0:b1], np.clip((d - INSET_M) / FEATHER_M, 0.0, 1.0), mul[a0:a1, b0:b1])
    # ground: the tread's top on it, the nearest tread's top off it
    _, (iy, ix) = ndimage.distance_transform_edt(~on, return_indices=True)
    gh = tops[ID[iy, ix]].astype(np.float32)
    os.makedirs(OUT, exist_ok=True)
    gp, hp = os.path.join(OUT, "grid.bin"), os.path.join(OUT, "ground_h.bin")
    np.concatenate([mul.ravel(), np.zeros(n * n, np.float32)]).astype("<f4").tofile(gp)
    gh.ravel().astype("<f4").tofile(hp)
    field_px = int(min(1024, 2 ** math.ceil(math.log2(side / FIELD_M_PER_PX))))
    man = {"_what": "DEV-22 (R-C9-216): the stair's tread snow -- grids for a SnowFieldTerrain (fid/pt/tools/stair_snow_prep.py)",
           "source": source, "treads": len(treads), "area_xz": [round(float(x0), 4), round(float(z0), 4), round(side, 4), round(side, 4)],
           "cell_m": CELL, "nx": n, "nz": n, "field_px": field_px, "grid_quad_m": 0.04,
           "grid": {"file": "grid.bin", "sha256": sha(gp), "_layout": "float32 LE: nx*nz depth multipliers (row = z), then nx*nz trodden"},
           "ground_h": {"file": "ground_h.bin", "sha256": sha(hp), "_": "float32 nx*nz world-y tread tops (m)"},
           "inset_m": INSET_M, "feather_m": FEATHER_M, "tread_top_y": [round(float(tops[1:].min()), 3), round(float(tops[1:].max()), 3)],
           "snow_px_share": round(float((mul > 0).mean()), 4)}
    json.dump(man, open(os.path.join(OUT, "stair_snow.json"), "w"), indent=1)
    prev = np.zeros((n, n, 3), np.uint8)
    prev[..., 0] = (np.clip((gh - gh.min()) / max(float(np.ptp(gh)), 1e-3), 0, 1) * 200).astype(np.uint8)
    prev[..., 1] = (mul * 255).astype(np.uint8)
    os.makedirs(os.path.join(FID, "pt", "dev22"), exist_ok=True)
    Image.fromarray(prev[::2, ::2]).save(os.path.join(FID, "pt", "dev22", "grids_preview.png"))
    print(json.dumps({k: v for k, v in man.items() if k not in ("grid", "ground_h")}))


if __name__ == "__main__":
    main()
