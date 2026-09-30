# THE PACK AGAINST THE MEASURE: do the renderer's pixels come from the pose this lane measured? For every move state
# (the four moves and the shout's variant), every direction and every frame, the renderer's own sockets (raw json,
# the port frame) against scripts/j_measure.py's glTF composite at the SAME times (the pack's t_s), turned into that
# direction's port frame. One rule in both is the claim; this is the check -- the weight curves included.
#
#   python3 scripts/j_validate_pack.py <raw.json> <kit.json>      -> work/j_validate_pack.json
#
# Port frame (render_cells.gd): the character turned theta = 90 - bearing about +Y, then x = X, y = Z, z = Y.
import json, math, os, subprocess, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE); RUNS = os.path.dirname(ROOT)
RAW, KIT = sys.argv[1], sys.argv[2]
raw = json.load(open(RAW)); kit = json.load(open(KIT))
BEAR = {"S": 90, "SW": 135, "W": 180, "NW": 225, "N": 270, "NE": 315, "E": 0, "SE": 45}
STATES = [s for s in ("whirlwind", "shout", "shout_raised", "hit", "death") if s in kit["states"]]
times = {s: raw["cells"]["%s/S" % s]["t_s"] for s in STATES}
tj = os.path.join(ROOT, "work", "_pack_times.json"); json.dump(times, open(tj, "w"))
mj = os.path.join(ROOT, "work", "jm_packtimes.json")
clips = ",".join(s if kit["states"][s]["clip"] == s else "%s:%s" % (s, kit["states"][s]["clip"]) for s in STATES)
pieces = kit["source"]["pieces"]; sword = next(p for p in pieces if p.endswith("sword.glb")); axe = next(p for p in pieces if p.endswith("axe_l.glb"))
subprocess.run(["blender", "-b", "-noaudio", "--python", os.path.join(HERE, "j_measure.py"), "--", kit["source"]["body"], mj, "--clips", clips,
                "--sword", sword, "--axe", axe, "--morphs", ",".join("%s=%s" % (k, v) for k, v in kit["morphs"].items() if not k.startswith("_")),
                "--layers-json", kit["layer_list_from"], "--times-json", tj, "--no-pen"], check=True, capture_output=True)
jm = json.load(open(mj))
L_ = {"main": 0.7768, "off": 0.8089}


def port(p, bearing):
    th = math.radians(90 - bearing); x, y, z = p
    X = x * math.cos(th) + z * math.sin(th); Z = -x * math.sin(th) + z * math.cos(th)
    return np.array([X, Z, y])


out = dict(what="the renderer's sockets (main_grip, main_tip, off_grip, off_tip, chest) against j_measure.py's composite at the pack's own "
                "t_s, every direction and frame of the move states, in the port frame; the tips as grip + L x the weapon's +Y",
           pack_raw=os.path.abspath(RAW), measure=os.path.relpath(mj, ROOT), body_sha256=jm.get("body_sha256"), states={}, samples=0)
worst = 0.0
for s in STATES:
    rows = jm["clips"][s]["rows"]; ws = 0.0; n = 0
    for d, b in BEAR.items():
        cell = raw["cells"]["%s/%s" % (s, d)]
        for i, sk in enumerate(cell["sockets"]):
            r = rows[i]; W_ = r["weapons"]
            want = {"main_grip": W_["r"]["grip"], "off_grip": W_["l"]["grip"],
                    "main_tip": list(np.array(W_["r"]["grip"]) + L_["main"] * np.array(W_["r"]["Y"])),
                    "off_tip": list(np.array(W_["l"]["grip"]) + L_["off"] * np.array(W_["l"]["Y"])),
                    "chest": r["joints"]["Spine02"]}
            for k, v in want.items():
                e = float(np.linalg.norm(port(v, b) - np.array(sk[k]))); ws = max(ws, e); n += 1
    out["states"][s] = dict(worst_m=round(ws, 5), samples=n); out["samples"] += n; worst = max(worst, ws)
    print("  %-13s worst %.5f m over %d socket samples" % (s, ws, n))
out["worst_m"] = round(worst, 5)
json.dump(out, open(os.path.join(ROOT, "work", "j_validate_pack.json"), "w"), indent=1)
print("wrote work/j_validate_pack.json: worst %.5f m over %d samples" % (worst, out["samples"]))
