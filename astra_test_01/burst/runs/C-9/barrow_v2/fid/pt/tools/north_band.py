#!/usr/bin/env python3
"""BV2F PT, R-C9-384 (tranche BV2F-N1, cap 10): paint the NORTH BAND of the site plate (site_ph4) by the guided paint-over
method, with context strips taken from the FINISHED plate's top rows.

    python3 fid/pt/tools/north_band.py init                 # pin inputs -> fid/pt/north/cfg_bv2f_n1.json
    python3 fid/pt/tools/north_band.py stage <c> [SUF]      # canvas for band chunk c (0..4), registered for refs_guard
    python3 fid/pt/tools/north_band.py brief <c> [SUF]      # briefs/C-9/BV2F-N1-<c>_N<SUF>.task.json
    python3 fid/pt/tools/north_band.py compose              # band (6656 x 768) + ph4 plate (6656 x 4864) + identity proof
    python3 fid/pt/tools/north_band.py seamcheck            # the band | plate seam, measured + crops

WHY NOT THE FROZEN STAGER. v1's guided_paint stages context only from LEFT / TOP / TOP-RIGHT neighbours (v1 painted
top-left -> bottom-right). The band lies ABOVE a finished plate, so its context is BELOW it. This tool keeps v1's
canvas geometry (1536 x 1024 at the 1280 x 768 stride: the band row is grid row -1, so its 256 bottom rows ARE plate rows
0..255), v1's brief wording (geo, rules, refs, fill phrase, retry clause, image cap 2, from the PH3 cfg verbatim), v1's
wavefront (left to right: chunk c is ready when c-1 is painted) and v1's stitch ramps across the band's own vertical
joins. The frozen refs_guard and wave.sh fire every burst. Registered as DEV-30 (proposed) in the hand-back.

PINS. The bottom context is the FINAL ph3 painting (painting_ph3_r339_full.png, pixels 1e5f9dd90c0f), which already
carries every DEV-24 layer (1-25) and the DEV-29 context patch -- so the band inherits the repaired plate, never a raw
canvas. The guide is LV's band render (fid/lv/ph4/guide/band_guide.png, sha-pinned) with DEV-28 smoothing (band_ids.png).

IDENTITY. compose never writes a plate pixel: ph4[768:] == ph3 byte for byte (asserted, and proved in identity.json).
The seam is handled on the BAND side only (fixed()): a low-frequency tone step across the seam row, measured per column
on same-class columns, smoothed along x and removed with a taper fading up from the seam (DEV-27's idea, one-sided);
and on ice, the plate's rows reflected upward and faded out over 96 px. The next chunk's left context is the FIXED chunk."""
import hashlib
import json
import os
import subprocess
import sys

import numpy as np
from PIL import Image

Image.MAX_IMAGE_PIXELS = None
FID = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
B = "/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst"
A9 = B + "/runs/C-9/artifacts"
N = os.path.join(FID, "pt", "north")
CFG = os.path.join(N, "cfg_bv2f_n1.json")
PH3_CFG = os.path.join(FID, "pt/pilot/cfg_bv2a_ph3.json")
PLATE = os.path.join(FID, "pt/ph3/final/painting_ph3_r339_full.png")
PLATE_FILE_SHA = "4dc60d9c583613022705eec02bfa6f6c3af655d17edbf50d7291940412b365a6"
PLATE_PIX_PREFIX = "1e5f9dd90c0f"
LVG = os.path.join(FID, "lv/ph4/guide")
PREFIX = "BV2F-N1"
CW, CH, SX, SY, OV = 1536, 1024, 1280, 768, 256
COLS, BAND, W = 5, 768, 6656

BAND_NOTE = (
    "THIS PANEL IS ON THE NORTH EDGE OF THE SCENE, BEYOND everything painted so far: the painted strip along its BOTTOM is "
    "the top edge of the finished scene, and the new paint must grow UPWARD out of it, as if the scene had always "
    "continued there -- same light, same snow, same brushwork and ink, no line or change where it meets the strip. "
    "What lies up here, exactly where the render puts it: the barrow mound's snow-covered dome rising behind its "
    "carved door (the grey slab over the door is the door's own stone roof), heather clumps on its flanks and its line "
    "of standing kerb stones continuing round its right side; the frozen mere's far shore with its reed islands; the "
    "narrow dark river running away northward; a low snowy shingle shore at the far left; and, between them, open deep "
    "snowfield with clustered heather tufts and a few lone weathered stones. Nothing else: no building, ruin, tree, "
    "cliff, wall, fire, path or new landmark anywhere; the top edge simply continues the snowfield.")


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def pix_sha(a):
    return hashlib.sha256(np.ascontiguousarray(a).tobytes()).hexdigest()


def load_cfg():
    c = json.load(open(CFG))
    for f, s in ((c["plate"], c["plate_sha256"]), (c["guide"], c["guide_sha256"]), (c["ids"], c["ids_sha256"])):
        if sha(f) != s:
            sys.exit("N1 HALT: %s is not the pinned file" % f)
    return c


def key(c):
    return "%d_N" % c


def src(c):
    """the band chunk's delivered canvas: -r1 first (the frozen stager's convention), then the plain id"""
    for suf in ("-r1", ""):
        p = "%s/%s-%s%s/%s-%s.png" % (A9, PREFIX, key(c), suf, PREFIX, key(c))
        if os.path.exists(p):
            return p
    return None


def guide_dev28(c):
    """the pinned band guide with DEV-28 shadow smoothing (fid/v1tools/dev28.py, the same smoother the Tier-B stager runs)"""
    out = os.path.join(N, "band_guide_dev28.png")
    rj = os.path.join(N, "band_guide_dev28.json")
    if os.path.exists(out) and os.path.exists(rj):
        r_ = json.load(open(rj))
        if r_["src_sha256"] == c["guide_sha256"] and r_["dev28"].get("reed_posts", {}).get("v") == 3 and sha(out) == r_["out_sha256"]:
            return np.asarray(Image.open(out).convert("RGB"))
    sys.path.insert(0, os.path.join(FID, "v1tools"))
    import dev28
    from scipy import ndimage
    g, rep = dev28.smooth(Image.open(c["guide"]).convert("RGB"), Image.open(c["ids"]).convert("RGB"))
    # R-C9-263's class-tint rule for LV's reed_tufts, applied at staging: the tufts render as stiff vertical POSTS, which
    # the painter copied as cattail stalks (R-C9-264). A post pixel takes the REED tint on the reed bed's footprint
    # (ground_reed, grown 3 px) and the SNOW tint elsewhere -- the same rule local_repaint.py's class_tint fill uses.
    man = json.load(open(os.path.join(LVG, "band_manifest.json")))
    n2i = {v["id"]: int(k) for k, v in man["id_table"].items()}
    lvl = json.load(open(os.path.join(FID, "../../barrow_full/godot/data/bv2f/site_ph4/level/level.json")))
    tint = lambda n: np.rint(np.array(lvl["tints_srgb"][n]) * 255).astype(np.uint8)
    I = np.asarray(Image.open(c["ids"]).convert("RGB")).astype(np.int64)
    gid = (I[..., 0] << 16) | (I[..., 1] << 8) | I[..., 2]
    post = gid == n2i["reed_tufts"]
    a = np.asarray(g.convert("RGB")).copy()
    # the posts AND their pen outline (2 px) are removed: each pixel takes the nearest pixel outside them (the reed bed's
    # straw tint where the post stood on its bed, the snow beside it elsewhere) -- no ghost post shapes are left to copy
    hole = ndimage.binary_dilation(post, iterations=2)
    _, (iy, ix) = ndimage.distance_transform_edt(hole, return_indices=True)
    a[hole] = a[iy[hole], ix[hole]]
    # the pen's arc across the river where LV's old channel head met the extension (band x 400-600, y 425-475): an edge
    # of the old cap, not a feature -- removed the same way, so the painter does not paint a log or crack across it
    arc = np.zeros(hole.shape, bool)
    arc[425:475, 400:600] = np.asarray(a[425:475, 400:600], np.float64).mean(-1) < 40
    arc = ndimage.binary_dilation(arc, iterations=1)
    _, (iy, ix) = ndimage.distance_transform_edt(arc, return_indices=True)
    a[arc] = a[iy[arc], ix[arc]]
    rep["river_arc_px"] = int(arc.sum())
    rep["reed_posts"] = {"v": 3, "post_px": int(post.sum()), "filled_px_incl_outline": int(hole.sum()),
                         "rule": "R-C9-263/264: LV's reed_tufts posts (copied as cattails) removed from the guide; filled from the nearest non-post pixel (reed bed straw / snow)"}
    g = Image.fromarray(a)
    g.save(out)
    json.dump({"src_sha256": c["guide_sha256"], "ids_sha256": c["ids_sha256"], "out_sha256": sha(out), "dev28": rep},
              open(os.path.join(N, "band_guide_dev28.json"), "w"), indent=1)
    return a


def cmd_init():
    os.makedirs(N, exist_ok=True)
    p3 = json.load(open(PH3_CFG))
    assert sha(PLATE) == PLATE_FILE_SHA, "the final ph3 painting is not the pinned one"
    a = np.asarray(Image.open(PLATE).convert("RGB"))
    assert pix_sha(a).startswith(PLATE_PIX_PREFIX) and a.shape == (4096, W, 3)
    man = json.load(open(os.path.join(LVG, "band_manifest.json")))
    # pinned COPIES (standing practice): LV may re-render; the band paints from these
    gp, ip, cp = (os.path.join(N, n) for n in ("band_guide_pinned.png", "band_ids_pinned.png", "band_class_pinned.png"))
    for s_, d_ in ((os.path.join(LVG, "band_guide.png"), gp), (os.path.join(LVG, "band_ids.png"), ip), (os.path.join(LVG, "band_class.png"), cp)):
        open(d_, "wb").write(open(s_, "rb").read())
    assert sha(gp) == man["guide"]["sha256"] and sha(ip) == man["ids"]["sha256"]
    lvc = subprocess.check_output(["git", "-C", FID, "log", "-1", "--format=%h", "--", os.path.join(LVG, "band_manifest.json")]).decode().strip()
    cfg = {"_what": "R-C9-384 NORTH BAND paint cfg (fid/pt/tools/north_band.py): tranche BV2F-N1, cap 10",
           "prefix": PREFIX, "cols": COLS, "rows": 1, "band_px": BAND,
           "plate": PLATE, "plate_sha256": PLATE_FILE_SHA, "plate_pixels_sha256_prefix": PLATE_PIX_PREFIX,
           "guide": gp, "guide_sha256": sha(gp), "ids": ip, "ids_sha256": sha(ip), "class": cp, "class_sha256": sha(cp),
           "guide_source": "fid/lv/ph4/guide/band_guide.png (LV site_ph4 level, fid/lv/tools/ph4_level.py + ph4_band_stitch.py)",
           "guide_lv_commit": lvc or "uncommitted at init",
           "name": "barrow_v2 site_ph4 NORTH BAND, 5 x 1 over the finished ph3 plate (BV2F R-C9-384)",
           "experiment": p3["experiment"], "run_tag": "Run C-9 BV2F north extension (site_ph4)",
           "ruling": "Matt R-C9-364/365/381 (north extension go), R-C9-384 (dispatch)",
           "geo": p3["geo"], "_geo_file": p3["_geo_file"], "_geo_sha256": p3["_geo_sha256"],
           "rules": p3["rules"], "refs": p3["refs"], "fill_phrase": p3["fill_phrase"], "retry_extra": p3["retry_extra"],
           "unpainted_phrase": p3["unpainted_phrase"], "band_note": BAND_NOTE,
           "_from": "geo/rules/refs/fill/retry/unpainted = the PH3 cfg verbatim (fid/pt/pilot/cfg_bv2a_ph3.json); band_note = the one added text (DEV-10-style note)",
           "dev28": "ON: the band guide is DEV-28-smoothed with band_ids before any canvas is cut (fid/pt/north/band_guide_dev28.json)",
           "wavefront": "0_N -> 1_N -> 2_N -> 3_N -> 4_N (chunk c is ready when c-1 is painted)"}
    json.dump(cfg, open(CFG, "w"), indent=1, ensure_ascii=False)
    print("cfg ok", CFG)


ICE = ("ice", "ice_mid", "shore_ice", "tide_ice")
SEAM_K, SEAM_SIG, TAPER, MIRROR_K = 8, 48.0, 320, 96


def fixed(c, cf):
    """BAND-SIDE SEAM FIX of chunk c's raw canvas (rows < 768 only; rows >= 768 become the real plate):
    (1) TONE: the low-frequency step across the seam -- median of the band's rows 760..767 minus median of the plate's rows
        768..775, per column, on columns whose class is the same on both sides (LV's band class map) -- smoothed along x
        (sigma 48) and removed from the band with a smoothstep taper rising 320 px above the seam (DEV-27's idea, one-sided);
    (2) ICE TEXTURE: where the band AND the plate are ice classes at the seam, the plate's rows reflected upward are blended
        into the band, weight 1 at the seam fading to 0 over 96 px (C0-continuous at the seam row by construction).
    Cached in fid/pt/north/fixed/<bid>.png with its record (raw / plate / class shas)."""
    from scipy import ndimage
    s_ = src(c)
    bid = os.path.basename(os.path.dirname(s_))
    od = os.path.join(N, "fixed")
    os.makedirs(od, exist_ok=True)
    op, oj = os.path.join(od, bid + ".png"), os.path.join(od, bid + ".json")
    if os.path.exists(op) and os.path.exists(oj):
        r_ = json.load(open(oj))
        if r_.get("v") == 1 and r_["raw_sha256"] == sha(s_) and r_["out_sha256"] == sha(op):
            return np.asarray(Image.open(op).convert("RGB"))
    x0 = c * SX
    raw = np.asarray(Image.open(s_).convert("RGB")).astype(np.float64)
    P8 = np.asarray(Image.open(cf["plate"]).convert("RGB"))
    pl = P8[0:CH - BAND, x0:x0 + CW].astype(np.float64)
    lvl = json.load(open(os.path.join(FID, "../../barrow_full/godot/data/bv2f/site_ph4/level/level.json")))
    CL = np.asarray(Image.open(cf["class"]))[:, x0:x0 + CW]
    names = lvl["classes"]
    a = raw[:BAND].copy()
    # (1) tone
    up_ = a[BAND - SEAM_K:BAND]
    dn_ = pl[0:SEAM_K]
    ca, cb = CL[BAND - SEAM_K:BAND], CL[BAND:BAND + SEAM_K]
    same = np.all(ca == ca[-1:], 0) & np.all(cb == ca[-1:], 0)
    d = np.median(up_, 0) - np.median(dn_, 0)                       # (CW, 3)
    w_ = ndimage.gaussian_filter1d(same.astype(np.float64), SEAM_SIG, mode="nearest")
    D = np.stack([ndimage.gaussian_filter1d(d[:, k] * same, SEAM_SIG, mode="nearest") / np.maximum(w_, 1e-3) for k in range(3)], -1)
    D[w_ < 0.05] = 0.0
    D = np.clip(D, -30, 30)
    t = np.clip((np.arange(BAND) - (BAND - TAPER)) / TAPER, 0, 1)
    t = t * t * (3 - 2 * t)
    a -= t[:, None, None] * D[None]
    # (2) ice mirror
    ice_ids = [names.index(n) for n in ICE if n in names]
    k = np.arange(MIRROR_K)
    ys = BAND - 1 - k                                                # band rows 767 .. 672
    mir = pl[k]                                                      # plate rows 0 .. 95 reflected
    m = np.isin(CL[ys], ice_ids) & np.isin(CL[BAND + k], ice_ids)
    m = ndimage.gaussian_filter(m.astype(np.float64), 6)
    wk = (1 - k / MIRROR_K) ** 2
    W_ = m * wk[:, None]
    a[ys] = a[ys] * (1 - W_[..., None]) + mir * W_[..., None]
    out = raw.copy()
    out[:BAND] = a
    out[BAND:] = pl
    out8 = np.clip(out + 0.5, 0, 255).astype(np.uint8)
    Image.fromarray(out8).save(op)
    json.dump({"v": 1, "bid": bid, "raw": s_, "raw_sha256": sha(s_), "plate_sha256": cf["plate_sha256"], "class_sha256": cf["class_sha256"],
               "out_sha256": sha(op), "tone_step_cols_measured": int(same.sum()),
               "tone_step_median_abs_rgb": [round(float(np.median(np.abs(D[:, i]))), 2) for i in range(3)],
               "tone_step_max_abs": round(float(np.abs(D).max()), 2), "ice_mirror_px": int((W_ > 0.01).sum()),
               "params": {"seam_rows": SEAM_K, "sigma_x": SEAM_SIG, "taper_px": TAPER, "mirror_px": MIRROR_K, "ice_classes": ICE}},
              open(oj, "w"), indent=1)
    return out8


def canvas(c, cf):
    G = guide_dev28(cf)
    P8 = np.asarray(Image.open(cf["plate"]).convert("RGB"))
    x0 = c * SX
    can = G[:CH, x0:x0 + CW].copy()
    kept = []
    can[BAND:CH] = P8[0:CH - BAND, x0:x0 + CW]                         # the finished plate's top 256 rows
    kept.append("its BOTTOM 256 rows")
    if c > 0:
        s = src(c - 1)
        if s is None:
            sys.exit("N1 HALT: chunk %d is not ready (%s not painted)" % (c, key(c - 1)))
        L = fixed(c - 1, cf)                                             # the left neighbour, seam-fixed (DEV-29's principle:
        assert L.shape == (CH, CW, 3)                                    # context carries the repaired paint, not the raw)
        can[0:BAND, 0:OV] = L[0:BAND, SX:CW]                           # the left neighbour's right 256 columns
        kept.append("its LEFT 256 columns")
    return can, kept


def cmd_stage(c, suf):
    cf = load_cfg()
    can, kept = canvas(c, cf)
    bid = "%s-%s%s" % (PREFIX, key(c), suf)
    cp = "%s/CS9-guides/%s_canvas.png" % (A9, bid)
    Image.fromarray(can).save(cp)
    mp = A9 + "/CS9-guides/manifest.json"
    man = json.load(open(mp)) if os.path.exists(mp) else {}
    man[os.path.basename(cp)] = sha(cp)
    json.dump(man, open(mp, "w"), indent=1)
    os.makedirs(os.path.join(N, "stage"), exist_ok=True)
    json.dump({"bid": bid, "kept": kept, "canvas_sha256": sha(cp), "left_src": src(c - 1) if c else None,
               "left_src_sha256": sha(src(c - 1)) if c else None, "plate_sha256": cf["plate_sha256"], "guide_sha256": cf["guide_sha256"]},
              open(os.path.join(N, "stage", "%s.json" % bid), "w"), indent=1)
    print(bid, "staged", kept)


def cmd_brief(c, suf):
    cf = load_cfg()
    bid = "%s-%s%s" % (PREFIX, key(c), suf)
    st = json.load(open(os.path.join(N, "stage", "%s.json" % bid)))
    cp = "%s/CS9-guides/%s_canvas.png" % (A9, bid)
    assert sha(cp) == st["canvas_sha256"], "canvas changed since stage"
    k = key(c)
    head = f"GENERATE BURST {bid} — {cf['run_tag']}, {cf['name']} panel {k} over a conductor LAYOUT GUIDE ({cf['ruling']}). task_id \"{bid}\".\n\n"
    text = (head + "IMAGE 1 is the canvas to EDIT (1536x1024): " + "; ".join(st["kept"]) +
            " are ALREADY PAINTED (real pixels from the finished painting and its neighbouring panel); in the rest, " + cf["geo"] +
            "\nUse image_gen in EDIT mode on IMAGE 1: keep the painted strips as they are and " + cf["fill_phrase"] +
            " that CONTINUES them seamlessly (no visible join). " + cf["rules"] + "\n\n" + cf["band_note"] +
            (" " + cf["band_note_ice"] if c >= 1 and cf.get("band_note_ice") else ""))
    refs = [{"path": cp, "role": "IMAGE 1 — the canvas to EDIT (painted strips + layout guide)"}] + \
           [{"path": p, "role": f"IMAGE {i + 2} — {role}"} for i, (p, role) in enumerate(cf["refs"])]
    text += (f"\n\nOne image_gen EDIT call. ONE retry only if a painted strip was altered, a join remains, anything appears that the guide does not put there (an extra landmark, fire, river or any town), {cf['retry_extra']}or {cf['unpainted_phrase']} — name the reason. "
             f"Copy the output to out/{PREFIX}-{k}.png with sha256. No code. No other files. No web.\nRETURN: receipt task_id \"{bid}\"; images = the file with prompt, references and elapsed_s; calls_used = the TRUE number of image_gen calls; status; concerns. Never PASS/FAIL.")
    json.dump({"text": text, "references": refs, "image_cap": 2, "minutes_cap": 15, "tool_call_cap": 20,
               "outputs": [f"out/{PREFIX}-{k}.png"], "effort": "high", "add_dirs": [], "experiment": cf["experiment"]},
              open(B + "/briefs/C-9/%s.task.json" % bid, "w"), indent=1, ensure_ascii=False)
    print(bid, "brief ok", len(text), "chars")


# ------------------------------------------------------------------------------------------------------------ compose
def band_blend(rows):
    """v1's stitch ramps across the band's own vertical joins (partition of unity in x), on canvas rows `rows`"""
    up = np.linspace(0, 1, OV, endpoint=False) + 0.5 / OV
    h = rows.stop - rows.start
    acc = np.zeros((h, W, 3))
    ws = np.zeros((h, W))
    srcs = {}
    for c in range(COLS):
        p = src(c)
        if p is None:
            sys.exit("N1 HALT: chunk %s not painted" % key(c))
        srcs[key(c)] = {"file": p, "sha256": sha(p)}
        im = fixed(c, load_cfg()).astype(np.float64)[rows]
        wx = np.ones(CW)
        if c > 0:
            wx[:OV] *= up
        if c < COLS - 1:
            wx[CW - OV:] *= up[::-1]
        acc[:, c * SX:c * SX + CW] += im * wx[None, :, None]
        ws[:, c * SX:c * SX + CW] += wx[None, :]
    assert abs(ws.min() - 1) < 1e-9 and abs(ws.max() - 1) < 1e-9
    return acc / ws[..., None], srcs


def cmd_compose():
    cf = load_cfg()
    P8 = np.asarray(Image.open(cf["plate"]).convert("RGB"))
    band, srcs = band_blend(slice(0, BAND))                          # the FIXED chunks (fixed()), v1's ramps across their joins
    band8 = np.clip(band + 0.5, 0, 255).astype(np.uint8)
    ph4 = np.concatenate([band8, P8], 0)
    assert ph4.shape == (4096 + BAND, W, 3)
    assert np.array_equal(ph4[BAND:], P8), "a plate pixel changed"
    os.makedirs(os.path.join(N, "final"), exist_ok=True)
    out = os.path.join(N, "final", "painting_ph4_full.png")
    Image.fromarray(ph4).save(out)
    Image.fromarray(band8).save(os.path.join(N, "final", "band.png"))
    Image.fromarray(ph4).resize((W // 4, (4096 + BAND) // 4), Image.LANCZOS).save(os.path.join(N, "final", "painting_ph4_preview.jpg"), quality=86)
    # IDENTITY PROOF, re-read from disk
    R = np.asarray(Image.open(out).convert("RGB"))
    rec = {"_what": "R-C9-384 IDENTITY PROOF: every ph3 plate pixel is byte-identical in ph4 at (x, y + 768)",
           "ph3_painting": cf["plate"], "ph3_file_sha256": cf["plate_sha256"], "ph3_pixels_sha256": pix_sha(P8),
           "ph4_painting": out, "ph4_file_sha256": sha(out), "ph4_pixels_sha256": pix_sha(R),
           "ph4_rows_768_on_pixels_sha256": pix_sha(R[BAND:]),
           "identical": bool(np.array_equal(R[BAND:], P8)), "differing_px": int((R[BAND:] != P8).any(-1).sum()),
           "band_chunks": srcs,
           "seam_fix": {k_: json.load(open(os.path.join(N, "fixed", "%s.json" % os.path.basename(os.path.dirname(v_["file"])))))
                        for k_, v_ in srcs.items()}}
    # control: a one-pixel change in the plate region must be caught
    R2 = R.copy()
    R2[BAND + 2000, 3000, 0] ^= 1
    rec["control_one_px_change_caught"] = not np.array_equal(R2[BAND:], P8)
    json.dump(rec, open(os.path.join(N, "final", "identity.json"), "w"), indent=1)
    print(json.dumps({k: v for k, v in rec.items() if k != "band_chunks"}, indent=1))


def cmd_seamcheck():
    """the seam at ph4 row 768: per 128-px segment, the step across the seam vs the same statistic one band of rows away
    inside the plate (control) and inside the band (control); plus 1:1 and play-zoom crops along it"""
    from scipy import ndimage
    ph4 = np.asarray(Image.open(os.path.join(N, "final", "painting_ph4_full.png")).convert("RGB")).astype(np.float64)
    L = ph4.mean(-1)
    lo = ndimage.gaussian_filter(L, 3)

    def step(y):           # mean |row y-1..y-8 mean - row y..y+7 mean| per 128-px segment, low-pass (tone) and grain
        a, b = lo[y - 8:y].mean(0), lo[y:y + 8].mean(0)
        tone = np.abs(a - b)
        hf = np.abs(L - lo)
        ga, gb = hf[y - 24:y].mean(0), hf[y:y + 24].mean(0)
        g = np.maximum(ga, gb) / np.maximum(np.minimum(ga, gb), 1e-6)
        seg = lambda v: [round(float(v[i:i + 128].mean()), 2) for i in range(0, W, 128)]
        return seg(tone), seg(g)
    s_t, s_g = step(BAND)
    c1_t, c1_g = step(BAND + 96)      # inside the plate
    c2_t, c2_g = step(BAND - 96)      # inside the band
    rep = {"seam_row": BAND, "segments_128px": len(s_t),
           "tone_step": {"seam": s_t, "control_plate": c1_t, "control_band": c2_t,
                         "seam_median": round(float(np.median(s_t)), 2), "control_median": round(float(np.median(c1_t + c2_t)), 2),
                         "seam_max": max(s_t), "control_max": max(c1_t + c2_t)},
           "grain_ratio": {"seam": s_g, "control_plate": c1_g, "control_band": c2_g,
                           "seam_median": round(float(np.median(s_g)), 3), "control_median": round(float(np.median(c1_g + c2_g)), 3)}}
    os.makedirs(os.path.join(N, "seam"), exist_ok=True)
    json.dump(rep, open(os.path.join(N, "seam", "seamcheck.json"), "w"), indent=1)
    im = Image.fromarray(ph4.astype(np.uint8))
    for i, x in enumerate(range(0, W, 1280)):
        im.crop((x, BAND - 256, min(W, x + 1280), BAND + 256)).save(os.path.join(N, "seam", "seam_1to1_%d.png" % i))
    print(json.dumps({k: (v if not isinstance(v, dict) else {kk: vv for kk, vv in v.items() if "median" in kk or "max" in kk}) for k, v in rep.items()}, indent=1))


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "init":
        cmd_init()
    elif cmd == "stage":
        cmd_stage(int(sys.argv[2]), sys.argv[3] if len(sys.argv) > 3 else "")
    elif cmd == "brief":
        cmd_brief(int(sys.argv[2]), sys.argv[3] if len(sys.argv) > 3 else "")
    elif cmd == "fix":
        fixed(int(sys.argv[2]), load_cfg())
        print(json.dumps(json.load(open(os.path.join(N, "fixed", "%s-%s.json" % (PREFIX, key(int(sys.argv[2])))))) if os.path.exists(os.path.join(N, "fixed", "%s-%s.json" % (PREFIX, key(int(sys.argv[2]))))) else "fixed"))
    elif cmd == "compose":
        cmd_compose()
    elif cmd == "seamcheck":
        cmd_seamcheck()
    else:
        sys.exit("unknown command")
