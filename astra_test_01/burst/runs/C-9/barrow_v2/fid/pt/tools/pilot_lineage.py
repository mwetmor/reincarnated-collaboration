#!/usr/bin/env python3
"""BV2F PT: write fid/pt/pilot/lineage.json (PH's p2_lineage.py --spec schema) from the CURRENT pilot records: every
static texture the painted pilot wears -> its producing record -> the pilot painting's sha. Re-run whenever the prep,
the bakes or their tools change (R-C9-194: the tool-sha links go stale otherwise).
    python3 fid/pt/tools/pilot_lineage.py"""
import hashlib, json, os
FID = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
C9 = os.path.dirname(os.path.dirname(FID))
D = C9 + "/barrow_full/godot/data/bv2f/pilot_rp/painted"   # R-C9-232: the repaint (the Phase 2' pilot data: bv2f/pilot/painted)
R = FID + "/pt/pilot/root"
paint = FID + "/pt/pilot/painting.png"
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
man = json.load(open(D + "/manifest.json"))
br = json.load(open(FID + "/pt/pilot/bake_report.json"))
pl = json.load(open(R + "/take/plates/plates.json"))["plates"]
prep = FID + "/pt/tools/bv2f_prep.py"
T = [{"id": "painting.bin", "path": D + "/painting.bin", "role": "ground + every primitive + the heather/snow albedo + the water's base (projection)",
      "links": [{"kind": "sha_record", "record": D + "/manifest.json", "field": "painting.sha256"}, {"kind": "bytes_equal", "input": paint}]},
     {"id": "lit", "path": D + "/" + man["lit"]["file"], "role": "painted direct-sun share (his shadow's mask)",
      "links": [{"kind": "sha_record", "record": D + "/manifest.json", "field": "lit.sha256"},
                {"kind": "producer", "tool": prep, "tool_sha": sha(prep),
                 "evidence": "fid/pt/pilot/painted_prep.json painting_sha256 = %s" % json.load(open(FID + "/pt/pilot/painted_prep.json"))["painting_sha256"][:12],
                 "input": paint}]}]
bake = FID + "/v1tools/tierA/barrow_full/tools/t5_06b_bake.py"
for k, v in br["pieces"].items():
    png = FID + "/" + v["texture"]
    p = pl[k]
    T.append({"id": "bake " + k, "path": D + "/" + man["bakes"][k]["file"], "role": "baked real model (%d px, DEV-19)" % v.get("texture_px", 1024),
              "links": [{"kind": "sha_record", "record": D + "/manifest.json", "field": "bakes.%s.sha256" % k}, {"kind": "bytes_equal", "input": png}]})
    T.append({"id": "work bake " + k, "path": png, "role": "bake output", "intermediate": True,
              "links": [{"kind": "producer", "tool": bake, "tool_sha": sha(bake),
                         "evidence": "fid/pt/tools/pt_bake.py (sha %s) runs the frozen t5_06b_bake.py --sheet <id>:fid/pt/pilot/painting.png; record fid/pt/pilot/bake_report.json pieces.%s.texture" % (sha(FID + "/pt/tools/pt_bake.py")[:12], k),
                         "input": R + "/take/plates/" + os.path.basename(p["file"])}]})
    T.append({"id": "plate " + k, "path": R + "/take/plates/" + os.path.basename(p["file"]), "role": "plate", "intermediate": True,
              "links": [{"kind": "crop_of", "input": paint, "rect": p["rect_px"], "alpha_min": 255}]})
spec = {"name": "bv2f pilot", "painting": {"path": paint, "sha": json.load(open(R + "/take/take_report.json"))["painting"]["sha256"]}, "textures": T,
        "_note": "no texels of their own (data, not painted texture): heather.json, snow_grid.bin, snow_ground_h.bin (heights), water_sdf.bin (the floes' distance field for the foam). The sprays, the snow, the floes and the water WEAR painting.bin (projected); the water's swell/foam are procedural motion over it (DEV-5)."}
json.dump(spec, open(FID + "/pt/pilot/lineage.json", "w"), indent=1)
print("lineage: %d nodes" % len(T))
