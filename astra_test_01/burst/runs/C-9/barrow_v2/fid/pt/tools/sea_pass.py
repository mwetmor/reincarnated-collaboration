#!/usr/bin/env python3
"""BV2F PT SEA PASS (R-C9-321; plan fid/pt/ph3/sea_pass_plan.json): DEV-24 patches on the FINAL full-site painting
(pt/ph3/final/painting_ph3_full.png, 8e169e6331bb), one patch per layer, each staged on the previous patch's result.
  D   = every plate px where LV bac035332's guide / class / ids differ from the 023686e3c pins (both pinned COPIES)
  PC  = the PASTE mask: water/ice classes of the NEW class map  |  water/ice of the OLD map where D (ice that became
        rock/snow/shingle: the W2 ledge, the waterline)  |  the accepted pilot rects where D (grown 8 px: the spar and its
        shadow, W1, rubble, beach_reveal, waterline);  inside the pilot window ALSO inside the R-C9-321 allowlist
        (fid/pt/ph3/allow_321.png). Land px that are land in both maps are never pasted (Matt: land done).
  R   = the REPAINT region: D grown 16 px, inside PC, its small enclosed holes (< HOLE px) filled   |  P1: the W1 rect
        (the turbulent water by the stern)  |  P3: open water (class sea) in the crack-net boxes;  all inside PC.
  Patches claim R inside their canvas inset by IN px (not at the plate's own border), in order; every R px is claimed.
    python3 fid/pt/tools/sea_pass.py plan              -> fid/pt/ph3/sea/plan.json + <name>/{region,paste}.png + specs
    python3 fid/pt/tools/sea_pass.py spec <name>       -> (re)writes the spec with painting = the current base
    python3 fid/pt/tools/sea_pass.py accept <name> <att>   -> pins the pasted patch, the base moves on
    python3 fid/pt/tools/sea_pass.py cfg               -> appends the accepted patches as dev24 layers 6.. to the PH3 cfg"""
import hashlib, json, os, sys
import numpy as np
from PIL import Image
from scipy import ndimage
Image.MAX_IMAGE_PIXELS = None
FID = "/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/barrow_v2/fid"
A9 = "/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/artifacts"
P = FID + "/pt/ph3/"
OUT = P + "sea/"
CFG = FID + "/pt/pilot/cfg_bv2a_ph3.json"
FINAL = P + "final/painting_ph3_full.png"
NEW, OLD = "bac035332", "023686e3c"
CW, CH, IN, HOLE = 1536, 1024, 64, 60000
WI = ("sea", "lead", "shore_ice", "tide_ice", "ice", "ice_mid")
P3_BOXES = [[1700, 2800, 4400, 4096], [0, 3072, 1700, 4096]]
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
NOTE_SEA = ("SEA ICE AND OPEN WATER of a frozen northern shore, painted as the painting round them paints them (same snow, "
            "same ice, same blue water, same watercolour hand and warm light): every floe and every shore-fast ice sheet keeps "
            "EXACTLY its rendered outline, size and THICKNESS (its pale side face exactly as tall as the render shows); floes "
            "flat and natural with worn, slightly rounded edges and snow on top -- NO raised rims, NO zig-zag snow edges; the "
            "OPEN WATER between them is calm, deep, dark blue water like the painted water round the patch, with NO crack "
            "lines, white veins, nets or honeycomb pattern on it; tiny floes stay tiny; rocks and cliffs at the edges continue "
            "exactly as painted.")
LAYOUT = [  # name, canvas rect_xy, what (P1-P4 of the plan), the patch's own note before NOTE_SEA
    ("sea_TL", [0, 0], "P4 (rubble rect: the mere's raised block)",
     "the top-left corner of the frozen MERE: large flat ice plates over dark water; the one small raised block that stood "
     "there is GONE -- dark open water in its place, exactly as the render shows. "),
    ("sea_A1", [0, 1370], "P1 (pole + W1) + P4 (the pilot sea)",
     "the shore and sea below the wrecked ship. The long FALLEN POLE that lay across the snow and the ice is GONE: snow, "
     "shore ice and water continue under where it lay, with no trace of it or its shadow (the ship's ribs and timbers and "
     "its one standing mast stub stay exactly as painted). The water by the stern is calm, deep, dark water -- no foam, no "
     "turbulence; the flat shore ice there ends in a clean ice edge with a face down to the water. "),
    ("sea_A2", [1200, 1350], "P4 (the accepted waterline)",
     "the WATERLINE at the foot of the shingle beach: shingle and snow meet the sea along a smooth, worn, natural curve -- "
     "no steps or stair-like edge. "),
    ("sea_B1", [0, 2240], "P4 (the pilot sea + Phase 3' ice)", ""),
    ("sea_B2", [1300, 2240], "P4 (the pilot sea + Phase 3' ice)", ""),
    ("sea_W2", [2560, 2560], "P2 (the W2 ledge) + P3 + P4",
     "the SEA CAVE mouth at the cliff foot: the flat ledge at the mouth is WET DARK ROCK with a thin white rime edge (no ice "
     "sheet, no snow cover on it; it stays a flat walkable ledge, its outline exactly as rendered); the sea at the cliff "
     "foot is DEEP and DARK, the same tone as the rest of the open water -- no lighter shallow water. "),
    ("sea_C1", [0, 3072], "P3 + P4 (Phase 3' ice)", ""),
    ("sea_C2", [1300, 3072], "P3 + P4 (Phase 3' ice)", ""),
    ("sea_C3", [2600, 3072], "P3 + P4 (Phase 3' ice)", ""),
    ("sea_R1", [4000, 3072], "P4 (Phase 3' ice)", ""),
]


def load_state():
    p = OUT + "state.json"
    return json.load(open(p)) if os.path.exists(p) else {"base": FINAL, "base_sha256": sha(FINAL), "accepted": []}


def plan():
    os.makedirs(OUT, exist_ok=True)
    m = json.loads(__import__("subprocess").check_output(["git", "-C", FID, "show", "%s:astra_test_01/burst/runs/C-9/barrow_v2/fid/lv/guide_art/guide_manifest.json" % NEW]))
    cls = m["class"]["classes"]
    pins = json.load(open(P + "pins_ph3.json")); assert pins["lv_commit"] == NEW
    for k in ("guide", "ids", "class"):
        assert sha(P + "%s_art_pinned_%s.png" % (k, NEW)) == pins[k]["sha256"]
    Cn = np.asarray(Image.open(P + "class_art_pinned_%s.png" % NEW)); Co = np.asarray(Image.open(P + "class_art_pinned_%s.png" % OLD))
    D = np.zeros(Cn.shape, bool)
    for k in ("guide", "class", "ids"):
        a = np.asarray(Image.open(P + "%s_art_pinned_%s.png" % (k, NEW))); b = np.asarray(Image.open(P + "%s_art_pinned_%s.png" % (k, OLD)))
        d = a != b; D |= d.any(2) if d.ndim == 3 else d
    wi = [cls.index(n) for n in WI]
    wn, wo = np.isin(Cn, wi), np.isin(Co, wi)
    al = json.load(open(P + "allow_321.json")); assert al["PASS"] and sha(P + "allow_321.png") == al["allow_png_sha256"]
    allow = np.zeros(Cn.shape, bool); allow[:2560, :4096] = np.asarray(Image.open(P + "allow_321.png")) > 0
    pilot = np.zeros(Cn.shape, bool); pilot[:2560, :4096] = True
    rect = np.zeros(Cn.shape, bool)
    for rl in al["rects"].values():
        for x0, y0, x1, y1 in rl:
            rect[max(0, y0):max(0, y1), max(0, x0):max(0, x1)] = True
    PC = wn | (wo & D) | (rect & ndimage.binary_dilation(D, iterations=8))
    PC &= ~pilot | allow
    R = ndimage.binary_dilation(D, iterations=16) & PC
    holes = ndimage.binary_fill_holes(R) & ~R
    lab, n = ndimage.label(holes)
    sz = ndimage.sum(holes, lab, range(1, n + 1))
    small = np.isin(lab, 1 + np.nonzero(sz < HOLE)[0]) & PC
    R |= small
    w1 = np.zeros_like(R); x0, y0, x1, y1 = al["rects"]["W1"][0]; w1[y0:y1, x0:x1] = True
    R |= w1 & PC
    p3 = np.zeros_like(R)
    for x0, y0, x1, y1 in P3_BOXES:
        p3[y0:y1, x0:x1] = True
    R |= p3 & (Cn == cls.index("sea")) & PC
    R &= PC
    H, W = R.shape
    claimed = np.zeros_like(R)
    rows = []
    for name, (x, y), what, note in LAYOUT:
        z = np.zeros_like(R)
        z[y + (IN if y > 0 else 0):y + CH - (IN if y + CH < H else 0), x + (IN if x > 0 else 0):x + CW - (IN if x + CW < W else 0)] = True
        c = R & z & ~claimed; claimed |= c
        d = OUT + name + "/"; os.makedirs(d, exist_ok=True)
        Image.fromarray((c[y:y + CH, x:x + CW] * 255).astype(np.uint8)).save(d + "region.png")
        Image.fromarray((PC[y:y + CH, x:x + CW] * 255).astype(np.uint8)).save(d + "paste.png")
        rows.append({"name": name, "rect_xy": [x, y], "what": what, "region_px": int(c.sum()),
                     "region_sha256": sha(d + "region.png"), "paste_sha256": sha(d + "paste.png"), "note": note + NOTE_SEA})
    left = R & ~claimed
    rec = {"_what": "BV2F PT sea pass plan (R-C9-321): DEV-24 patches on the final painting, one per layer, in order",
           "new": NEW, "old": OLD, "D_px": int(D.sum()), "PC_px": int(PC.sum()), "R_px": int(R.sum()),
           "R_small_holes_filled_px": int(small.sum()), "R_W1_px": int((w1 & PC).sum()), "R_P3_open_sea_px": int((p3 & (Cn == cls.index("sea")) & PC).sum()),
           "pilot_PC_outside_allow_px": int((PC & pilot & ~allow).sum()), "unclaimed_px": int(left.sum()),
           "params": {"canvas": [CW, CH], "inset": IN, "hole_fill_lt": HOLE, "grow_D": 16, "rect_grow": 8, "water_ice": WI, "p3_boxes": P3_BOXES},
           "patches": rows}
    json.dump(rec, open(OUT + "plan.json", "w"), indent=1)
    Image.fromarray((R * 255).astype(np.uint8)).save(OUT + "R_full.png")
    Image.fromarray((PC * 255).astype(np.uint8)).save(OUT + "PC_full.png")
    print(json.dumps({k: v for k, v in rec.items() if k != "patches"}))
    for r in rows:
        print(r["name"], r["rect_xy"], r["region_px"])
    assert not left.any(), "unclaimed region px"


def spec(name, att="1", cap=1):
    pl = json.load(open(OUT + "plan.json"))
    row = [r for r in pl["patches"] if r["name"] == name][0]
    st = load_state()
    assert sha(st["base"]) == st["base_sha256"]
    d = OUT + name + "/"
    S = {"prefix": "BV2F-LR4", "name": name, "painting": st["base"], "rect_xy": row["rect_xy"], "layer": 6 + len(st["accepted"]),
         "class_png": P + "class_art_pinned_%s.png" % NEW, "class_sha256": sha(P + "class_art_pinned_%s.png" % NEW), "class_commit": NEW,
         "guide_png": P + "guide_art_pinned_%s.png" % NEW, "guide_sha256": sha(P + "guide_art_pinned_%s.png" % NEW),
         "region": {"mode": "png", "png": d + "region.png", "sha256": row["region_sha256"]},
         "paste_mask_png": d + "paste.png", "paste_mask_sha256": row["paste_sha256"],
         "fill": "guide", "brief_v": 2, "image_cap": cap, "cfg": CFG, "note": row["note"],
         "ruling": "R-C9-321 sea pass %s: %s" % (name, row["what"])}
    json.dump(S, open(FID + "/pt/dev24/spec_%s.json" % name, "w"), indent=1)
    print("spec", name, "base", os.path.basename(st["base"]), "layer", S["layer"])


CORR_LO, CORR_HI = 0.02, 0.15


def stale_mask(name):
    """plate px a LATER patch of the plan repaints: their paint is stale, so the tone ring must not sample it"""
    pl = json.load(open(OUT + "plan.json"))
    names = [r["name"] for r in pl["patches"]]
    st = np.zeros((4096, 6656), bool)
    for r in pl["patches"][names.index(name) + 1:]:
        x, y = r["rect_xy"]
        st[y:y + CH, x:x + CW] |= np.asarray(Image.open(OUT + r["name"] + "/region.png")) > 127
    return st


def soft_corr(old, new, R, pc, stale):
    """R-C9-321: DEV-24's tone correction, PINNED per patch (corr_npz), with two changes for large sea patches: the ring
    skips stale px (repainted later), and the field FADES OUT (smoothstep of the ring density, CORR_LO..CORR_HI) instead
    of v1-DEV-24's hard cut at density 0.02 -- the hard cut drew a visible tone line inside large regions (measured
    |corr| at the cut up to 24 levels in A1/B1/W2)"""
    sys.path.insert(0, FID + "/v1tools"); import dev24
    M, w = dev24.weights(R, pc)
    ring = ndimage.binary_dilation(M, iterations=dev24.RING_OUT) & ~ndimage.binary_dilation(M, iterations=dev24.RING_IN) & pc & ~stale
    num = np.stack([ndimage.gaussian_filter((old - new)[..., i] * ring, dev24.CORR_SIGMA) for i in range(3)], -1)
    den = ndimage.gaussian_filter(ring.astype(np.float64), dev24.CORR_SIGMA)[..., None]
    t = np.clip((den - CORR_LO) / (CORR_HI - CORR_LO), 0, 1)
    return num / np.maximum(den, 1e-6) * (t * t * (3 - 2 * t))


def accept(name, att):
    sys.path.insert(0, FID + "/v1tools"); import dev24
    st = load_state()
    pin = json.load(open(FID + "/pt/dev24/%s/pin_%s.json" % (name, att)))
    base = np.asarray(Image.open(st["base"]).convert("RGB"))
    x0, y0 = pin["rect_xy"]
    R = np.asarray(Image.open(pin["region_png"])) > 127; pc = np.asarray(Image.open(pin["paste_png"])) > 127
    new = np.asarray(Image.open(pin["new_png"]).convert("RGB")).astype(np.float64)
    corr = soft_corr(base[y0:y0 + CH, x0:x0 + CW].astype(np.float64), new, R, pc, stale_mask(name)[y0:y0 + CH, x0:x0 + CW])
    cp = FID + "/pt/dev24/%s-%s_corr.npz" % (name, att)
    np.savez_compressed(cp, corr=corr.astype(np.float32))
    pin["corr_npz"], pin["corr_sha256"] = cp, sha(cp)
    pin["read_sha256"] = dev24.read_sha(base, pin)
    out, rep = dev24.apply_layer(base, {"patches": [pin]})
    res = FID + "/pt/dev24/%s/painting_sea_%s.png" % (name, att)
    Image.fromarray(out).save(res)
    assert (np.asarray(Image.open(res).convert("RGB")) == out).all()
    st["accepted"].append({"layer": 6 + len(st["accepted"]), "pin": pin, "base": st["base"], "base_pixels_sha256": dev24.pixels_sha(base),
                           "result": res, "result_sha256": sha(res), "report": rep})
    st["base"], st["base_sha256"] = res, sha(res)
    json.dump(st, open(OUT + "state.json", "w"), indent=1)
    print("accepted", name, att, "layer", st["accepted"][-1]["layer"], rep)


def rebuild():
    """re-accept every accepted patch in order from the final painting (no image calls): after a paste-rule change"""
    st = load_state()
    done = [(a["pin"]["name"].rsplit("-", 1)[0], a["pin"]["name"].rsplit("-", 1)[1]) for a in st["accepted"]]
    json.dump({"base": FINAL, "base_sha256": sha(FINAL), "accepted": [], "_prev": st}, open(OUT + "state.json", "w"), indent=1)
    for n, a in done:
        accept(n, a)


def cfg():
    st = load_state()
    c = json.load(open(CFG))
    n0 = len(c["dev24"]["layers"])
    assert n0 == 5, "the PH3 cfg already carries sea layers (%d layers)" % n0
    for a in st["accepted"]:
        c["dev24"]["layers"].append({"base_pixels_sha256": a["base_pixels_sha256"], "patches": [a["pin"]],
                                     "_r_c9_321": "sea pass layer %d (%s)" % (a["layer"], a["pin"]["name"])})
    c["_dev24_sea"] = ("R-C9-321 SEA PASS: layers 6-%d = one DEV-24 patch each, staged in order on the final painting "
                       "(fid/pt/ph3/sea/plan.json, state.json); each pinned by its read region" % (5 + len(st["accepted"])))
    json.dump(c, open(CFG, "w"), indent=1, ensure_ascii=False)
    print("cfg layers", len(c["dev24"]["layers"]))


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "plan":
        plan()
    elif cmd == "spec":
        spec(sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else "1", int(sys.argv[4]) if len(sys.argv) > 4 else 1)
    elif cmd == "accept":
        accept(sys.argv[2], sys.argv[3])
    elif cmd == "rebuild":
        rebuild()
    elif cmd == "cfg":
        cfg()
