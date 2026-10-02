# THE PACK AGAINST THE GLB, for a kit WITHOUT layers (the GD EoR warlord; any kit whose states play their clip alone): every
# state, direction and frame, the renderer's own sockets (raw json, the port frame) against the glTF pose at the SAME time
# (the pack's t_s; the glTF rule: un-keyed = rest, rotations slerped), turned into that direction's port frame.
#
#   python3 scripts/validate_sockets.py <raw.json> <kit.json> <out.json>
#
# Port frame (render_cells.gd): the character turned theta = 90 - bearing about +Y, then x = X, y = Z, z = Y. A socket is
# its bone's world origin + along_bone_m x the bone's +Y (normalised), as render_cells.gd _sockets() computes it.
# REFUSES a kit with layers (layer_specs / layer_list / layers): that pose needs the mixer (nb_join/scripts/j_validate_pack.py).
import json, math, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); RUNS = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(RUNS, "so_d7", "scripts")); C = __import__('s17_loop_closure')
RAW, KIT, OUT = sys.argv[1:4]
raw = json.load(open(RAW)); kit = json.load(open(KIT))
if kit.get("layer_specs") or kit.get("layer_list") or kit.get("layers"):
    sys.exit("REFUSED: this kit has layers -- validate it with the mixer (nb_join/scripts/j_validate_pack.py)")
m = C.model(kit["source"]["body"]); nid = m["nid"]
BEAR = {"S": 90.0, "SW": 135.0, "W": 180.0, "NW": 225.0, "N": 270.0, "NE": 315.0, "E": 0.0, "SE": 45.0}


def port(p, bearing):
    th = math.radians(90 - bearing); x, y, z = p
    return np.array([x * math.cos(th) + z * math.sin(th), -x * math.sin(th) + z * math.cos(th), y])


out = dict(what="the renderer's sockets against the glTF pose at the pack's own t_s, every state, direction and frame, in the port frame",
           pack_raw=os.path.abspath(RAW), kit=os.path.abspath(KIT), states={}, samples=0)
worst = 0.0
for st, sd in kit["states"].items():
    ws = 0.0; n = 0
    for d, b in BEAR.items():
        cell = raw["cells"].get("%s/%s" % (st, d))
        if cell is None: continue
        for t, sk in zip(cell["t_s"], cell["sockets"]):
            G = C.globals_at(m, sd["clip"], float(t))
            for k, sdef in kit["sockets"].items():
                M = G[nid[sdef["bone"]]]; Y = M[:3, 1] / np.linalg.norm(M[:3, 1])
                want = M[:3, 3] + float(sdef.get("along_bone_m", 0.0)) * Y
                if "local_m" in sdef:                                  # an off-axis point (render_cells.gd's local_m)
                    Rn = M[:3, :3] / np.linalg.norm(M[:3, :3], axis=0); want = want + Rn @ np.array(sdef["local_m"], float)
                e = float(np.linalg.norm(port(want, b) - np.array(sk[k]))); ws = max(ws, e); n += 1
    out["states"][st] = dict(worst_m=round(ws, 5), samples=n); out["samples"] += n; worst = max(worst, ws)
    print("  %-15s worst %.5f m over %d socket samples" % (st, ws, n))
out["worst_m"] = round(worst, 5)
json.dump(out, open(OUT, "w"), indent=1)
print("wrote %s: worst %.5f m over %d samples" % (OUT, worst, out["samples"]))
