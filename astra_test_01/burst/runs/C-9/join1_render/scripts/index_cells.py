# JOIN-1 sprite-cell INDEXER + LINT (C-9): the rendered cells -> matrix_index.json, schema
# join1-sprite-cells/1 (reincarnated-godot/docs/join1-sprite-cell-contract-2026-09-29.md, d95e1df, 3.2).
#
#   python3 scripts/index_cells.py <kit.json> <pack_kit_dir> <raw.json> <closure_dir> [--sheet out.png]
#
# Everything the stage checks is computed here from the FILES, so the index cannot drift from them
# (the contract's lesson from C-8's stale matrix_index): sha256 per frame, cell_sha256 = sha256 of the
# frame digests in order joined by "\n", the alpha union box (PIL getbbox of the alpha channel, the
# convention stage_art.py crops with: [x0, y0, x1, y1), x1/y1 exclusive), the 1 px edge lint, frame
# counts against t_s, the release sample (t_s[release_index] == release_s == the manifest's), the
# facing lint (+-0.5 deg against the direction table), sockets present in every frame, the anchor
# (measured per frame by the renderer, within 0.01 px of (384, 448)). A cell that fails any of these
# is FAILED_LINT with the reason in `flags`. `mirror_of` is never written.
# A pack re-rendered IN PART (J1_ONLY, then scripts/merge_raw.py) carries each cell's `render_pass` and the
# passes' provenance (`render_passes`: body / kit-config / tool sha per render) -- the files are still what is hashed.
import hashlib, json, math, os, sys, time
import numpy as np
from PIL import Image, ImageDraw
a = sys.argv[1:]
KIT, PACK, RAW, CLO = a[0], a[1], a[2], a[3]
SHEET = a[a.index('--sheet') + 1] if '--sheet' in a else None
HERE = os.path.dirname(os.path.abspath(__file__))
kit = json.load(open(KIT)); raw = json.load(open(RAW))
man_path = kit["source"]["clip_manifest"]; man = json.load(open(man_path))
sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()
DIRS = ["S", "SW", "W", "NW", "N", "NE", "E", "SE"]
BEAR = {"S": 90, "SW": 135, "W": 180, "NW": 225, "N": 270, "NE": 315, "E": 0, "SE": 45}
PPM = 151.33680669505316
ALPHA = 52.9535411256029
ANCHOR = [384, 448]


def mget(path):
    v = man
    for k in path.split("."):
        v = v[k]
    return v


states, cells, complete = {}, {}, 0
for st, sd in kit["states"].items():
    n = int(sd["frames"])
    T = float(raw["durations_s"][st])
    t_s = [round(float(t), 6) for t in raw["cells"]["%s/S" % st]["t_s"]]
    rec = dict(kind=sd["kind"], role=sd["role"], clip=dict(animation=sd["clip"], duration_s=round(T, 6), manifest_entry=sd.get("manifest_entry")),
               frames=n, t_s=t_s, root_motion="stripped", stride_m_per_cycle=None, release_index=None, release_s=None,
               hold_last=bool(sd.get("hold_last", False)), closure_mad=None)
    if sd.get("skill"):
        rec["skill"] = sd["skill"]
    if sd.get("variant_of"):
        # a VARIANT for a look (not a contract state): it plays another state's clip under its own layers
        rec["variant_of"] = sd["variant_of"]; rec["variant_note"] = sd.get("variant_note")
    if sd.get("notes_from"):
        # facts about the clip AS SHIPPED that a reader would otherwise re-find (the kit names manifest paths)
        rec["notes"] = [mget(p_) for p_ in sd["notes_from"]]
    if sd.get("stride_from"):
        loco = mget(sd["stride_from"])
        rec["stride_m_per_cycle"] = round(float(loco["speed_m_s"]) * T, 4)
        rec["stride_method"] = ("the clip is in place at source; stride = the manifest's FOOT-LOCK speed (%.3f m/s, the speed that holds the "
                                "planted foot still) x the clip length (%.4f s)" % (float(loco["speed_m_s"]), T))
    if sd["sampling"] == "release":
        rs = float(mget(sd["release_from"]))
        r = min(max(int(round((n - 1) * rs / T)), 1), n - 2)
        rec.update(release_index=r, release_s=round(rs, 6), release_socket=sd.get("release_socket"))
    states[st] = rec
    mads = []
    for d in DIRS:
        key = "%s/%s" % (st, d)
        rc = raw["cells"].get(key)
        cdir = os.path.join(PACK, "cells", st, d)
        flags, files = [], []
        if rc is None:
            cells[key] = dict(status="PENDING", flags=["not rendered"], frames=0, files=[]); continue
        names = ["%s_%s_%02d.png" % (st, d, i) for i in range(n)]
        box = None; edge = False
        for nm in names:
            p = os.path.join(cdir, nm)
            if not os.path.exists(p):
                flags.append("missing " + nm); continue
            files.append(dict(name=nm, sha256=sha(p)))
            im = Image.open(p)
            if im.mode != "RGBA":
                flags.append("%s mode %s" % (nm, im.mode))
            al = np.asarray(im.getchannel("A"))
            b = im.getchannel("A").getbbox()
            if b:
                box = list(b) if box is None else [min(box[0], b[0]), min(box[1], b[1]), max(box[2], b[2]), max(box[3], b[3])]
            if al[0, :].any() or al[-1, :].any() or al[:, 0].any() or al[:, -1].any():
                edge = True
            if im.size != (768, 768):
                flags.append("%s size %s" % (nm, im.size))
        if edge:
            flags.append("EDGE_TOUCH: alpha on the 1 px border")
        if len(files) != n or len(t_s) != n:
            flags.append("frame count %d files, %d t_s, want %d" % (len(files), len(t_s), n))
        fm = float(rc["facing"]["root_deg"])
        dev = (fm - BEAR[d] + 180) % 360 - 180
        if abs(dev) > 0.5:
            flags.append("FACING %.3f deg against %d" % (fm, BEAR[d]))
        worst_anchor = max(max(abs(p[0] - ANCHOR[0]), abs(p[1] - ANCHOR[1])) for p in rc["anchor_px"])
        if worst_anchor > 0.01:
            flags.append("ANCHOR off by %.3f px" % worst_anchor)
        req = [k for k in kit["sockets"] if not k.startswith("_")]
        for i, s in enumerate(rc["sockets"]):
            miss = [k for k in req if k not in s or s[k] is None]
            if miss:
                flags.append("frame %d sockets missing %s" % (i, miss))
        if rec["release_index"] is not None and abs(t_s[rec["release_index"]] - rec["release_s"]) > 1e-4:
            flags.append("release sample %.6f != release_s %.6f" % (t_s[rec["release_index"]], rec["release_s"]))
        # the loop's closure: render(T) against render(0), mean |dRGBA| over the canvas, 0-255
        if sd["kind"] == "loop":
            pT = os.path.join(CLO, "%s_%s_T.png" % (st, d))
            if os.path.exists(pT) and files:
                A0 = np.asarray(Image.open(os.path.join(cdir, names[0])).convert("RGBA")).astype(np.int16)
                AT = np.asarray(Image.open(pT).convert("RGBA")).astype(np.int16)
                # over the FIGURE (either frame opaque), not the canvas: a canvas mean is mostly transparent
                # zeros, and it reported the run's open seam as 0.98 while 73% of her pixels moved
                fig = (A0[..., 3] > 0) | (AT[..., 3] > 0)
                mads.append(float(np.abs(A0 - AT)[fig].mean()))
        digests = [f["sha256"] for f in files]
        status = "COMPLETE" if not [f for f in flags if not f.startswith("note")] else "FAILED_LINT"
        complete += status == "COMPLETE"
        sock = {k: [s[k] for s in rc["sockets"]] for k in req}
        cells[key] = dict(status=status, flags=flags, frames=len(files), files=files, render_pass=rc.get("render_pass"),
                          cell_sha256=hashlib.sha256("\n".join(digests).encode()).hexdigest(),
                          alpha_union_bbox=box or [0, 0, 0, 0], edge_touch=edge,
                          facing_measured_deg=round(fm, 4), facing_hips_frame0_deg=round(float(rc["facing"]["hips_deg"]), 3),
                          anchor_measured_max_dev_px=round(worst_anchor, 4), sockets_m=sock)
    if mads:
        rec["closure_mad"] = round(max(mads), 4)
        if rec["closure_mad"] > 5.0:
            # the contract expects ~0 and does not make it a stage lint; an open seam is REPORTED on the state and
            # as a note on each of its cells (a note does not fail a cell), never hidden
            rec["closure_flag"] = ("OPEN LOOP SEAM: the clip's last key is not its first (render(T) differs from render(0) by %.1f "
                                   "in-figure); the wrap from frame N-1 to frame 0 pops. A clip-hygiene fix at the source, not a render one."
                                   % rec["closure_mad"])
            for d in DIRS:
                c_ = cells.get("%s/%s" % (st, d))
                if c_ and c_.get("status") == "COMPLETE":
                    c_["flags"].append("note: " + rec["closure_flag"])
        rec["closure_mad_note"] = ("max over the 8 directions of mean |RGBA(T) - RGBA(0)| over the FIGURE's pixels (either frame opaque), "
                                   "0-255; render(T) is rendered for this and is not in the pack")

tool = os.path.join(HERE, "render_cells.gd")
sup = None
if kit.get("supersedes"):
    # a later version of a DECLARED pack: the pack it supersedes is named by its index's sha256, read from the file and
    # checked against the kit's pin -- if the declared index ever changed, this refuses rather than pointing at the wrong one
    sp = kit["supersedes"]
    got = sha(sp["index"])
    if sp.get("index_sha256") and got != sp["index_sha256"]:
        sys.exit("REFUSED -- the superseded index %s is %s, the kit pins %s" % (sp["index"], got[:12], sp["index_sha256"][:12]))
    sup = dict(sp, index_sha256=got)
    if sp.get("body_glb"):
        sup["body_sha256_checked"] = sha(sp["body_glb"]) == sp.get("body_sha256")
idx = {
    "schema": "join1-sprite-cells/1",
    "kit": kit["kit"],
    "pack_version": kit.get("pack_version", 1),
    "supersedes": sup,
    "status": "DRAFT -- rendered and linted by C-9; NOT declared COMPLETE as a pack (the conductor declares after Matt's look and moves it to join1_pack/)",
    "producer": {"run": "C-9", "tool": tool, "tool_sha256": sha(tool), "indexer": os.path.abspath(__file__), "indexer_sha256": sha(os.path.abspath(__file__)),
                 "kit_config": os.path.abspath(KIT), "kit_config_sha256": sha(KIT), "ts": time.strftime("%Y-%m-%dT%H:%M:%S%z")},
    "source": {"glb": kit["source"]["body"], "glb_sha256": sha(kit["source"]["body"]),
               "pieces": [{"glb": p, "sha256": sha(p)} for p in kit["source"].get("pieces", [])],
               "h_model_m": raw["h_model"]["h_m"], "h_model_method": kit["h_model"]["method"] + ((" (crown = %s at rest %.4f; sole = the ground 0)" % (raw["h_model"]["crown_bone"], raw["h_model"]["crown_m"])) if "crown_bone" in raw["h_model"] else (" (every 7th vertex; sole %.4f, crown %.4f)" % (raw["h_model"]["sole_m"], raw["h_model"]["crown_m"]))),
               "loadout": kit["source"]["loadout"]},
    "clip_manifest": {"path": man_path, "sha256": sha(man_path)},
    "camera": {"projection": "orthographic", "pitch_deg": ALPHA, "ppm_render": PPM, "ppm_multiple_of_gd": 2,
               "canvas_px": [768, 768], "anchor_px": ANCHOR, "ortho_size_m": round(768 / PPM, 5),
               "frame": "port model: x screen-right, y toward camera, z up; origin = character ground origin",
               "yaw_deg": 0.0, "character_heading": "theta = 90 - bearing about +Y (the model faces +Z); frame-0 root forward measured per cell"},
    "image": {"format": "png", "mode": "RGBA", "alpha": "straight", "colorspace": "sRGB", "plate": None, "baked_shadow": False,
              "baked_vfx": False, "lights": "camera-parented",
              "lights_detail": "the Barrow's winter sun (paint_stack.gd: 55 deg, screen azimuth 305, (1.0, 0.955, 0.885), energy 0.90, shadow blur 1.7) as a child of the camera, ambient 0.30 white; self-shadowing only (no ground)",
              "antialias": "none: every alpha is 0 or 255"},
    "directions": {"order": DIRS, "facing_ground_bearing_deg": BEAR},
    "states": states,
    "sockets_def": {k: v.get("_what") for k, v in kit["sockets"].items() if not k.startswith("_")},
    "alpha_union_bbox_convention": "[x0, y0, x1, y1), x1/y1 exclusive -- PIL getchannel('A').getbbox(), as stage_art.py crops",
    "layers": kit.get("layers") if kit.get("layers") is not None else {
        "layer_specs": [{"path": p_, "sha256": sha(p_)} for p_ in kit.get("layer_specs", [])],
        "layer_list": kit.get("layer_list"), "layer_list_from": kit.get("layer_list_from")},
    "morphs": kit.get("morphs"),
    # the runtime glTF path re-samples (GLTFState.bake_fps): what that does to THIS pack's clips, measured
    "runtime_resampling": json.load(open(kit["runtime_resample"])) if kit.get("runtime_resample") else None,
    # a pack re-rendered in part (merge_raw.py) says which render made each cell, and from what
    "render_passes": raw.get("render_passes"),
    "cells": cells,
    "expected": len(kit["states"]) * 8, "complete": complete,
}
json.dump(idx, open(os.path.join(PACK, "matrix_index.json"), "w"), indent=1)
bad = {k: v["flags"] for k, v in cells.items() if v["status"] != "COMPLETE"}
print("matrix_index.json: %d of %d cells COMPLETE%s" % (complete, idx["expected"], "" if not bad else "; FAILED: %s" % json.dumps(bad)[:600]))
for st, r in states.items():
    print("  %-14s N=%2d T=%.4f s  %s%s" % (st, r["frames"], r["clip"]["duration_s"],
          ("release r=%d at %.4f s" % (r["release_index"], r["release_s"])) if r["release_index"] is not None else "",
          ("closure MAD %.3f" % r["closure_mad"]) if r["closure_mad"] is not None else ""))

if SHEET:
    # FOR MATT: each state's RELEASE frame (casts) or MID frame across all 8 directions, 1x ppm_render (no scaling),
    # each tile the state's union box over the 8 directions, on a light grey so the silhouette reads
    rows = []
    for st, r in states.items():
        i = r["release_index"] if r["release_index"] is not None else r["frames"] // 2
        bx = None
        for d in DIRS:
            b = cells["%s/%s" % (st, d)].get("alpha_union_bbox")
            if b and b != [0, 0, 0, 0]:
                bx = list(b) if bx is None else [min(bx[0], b[0]), min(bx[1], b[1]), max(bx[2], b[2]), max(bx[3], b[3])]
        rows.append((st, i, bx))
    tw = max(b[2] - b[0] for _, _, b in rows) + 8
    lab = 18
    H = sum(b[3] - b[1] + 8 + lab for _, _, b in rows)
    sheet = Image.new("RGBA", (tw * 8 + 150, H), (214, 216, 218, 255))
    dr = ImageDraw.Draw(sheet)
    y = 0
    for st, i, b in rows:
        h = b[3] - b[1] + 8
        dr.text((6, y + lab + h // 2 - 8), "%s\nframe %d%s" % (st, i, " (release)" if states[st]["release_index"] is not None else " (mid)"), fill=(20, 20, 20, 255))
        for k, d in enumerate(DIRS):
            im = Image.open(os.path.join(PACK, "cells", st, d, "%s_%s_%02d.png" % (st, d, i))).convert("RGBA")
            crop = im.crop((b[0], b[1], b[2], b[3]))
            x = 150 + k * tw + (tw - crop.size[0]) // 2
            sheet.alpha_composite(crop, (x, y + lab + 4))
            if y == 0:
                pass
            dr.text((150 + k * tw + 4, y + 2), "%s (%d deg)" % (d, BEAR[d]), fill=(60, 60, 60, 255))
        y += h + lab
    sheet.convert("RGB").save(SHEET)
    print("contact sheet: %s (%dx%d, 1x ppm_render)" % (SHEET, sheet.size[0], sheet.size[1]))
