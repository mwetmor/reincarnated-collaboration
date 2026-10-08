#!/usr/bin/env python3
"""BV2F PT DEV-28 (R-C9-257 (c)) constructed test + guide runs. Read-only on the guides; writes fid/pt/dev28/.
  1. SYNTHETIC: a rock (own ID) on snow, a hard-edged shadow and a PCF-dithered shadow -> only the dither may change
  2. v1's guide + v1's ID render: changed px only in the dither zone, nothing outside it, no colour across objects
  3. our pilot guide (pinned 1c22764cb874) + LV's ID render (95b658fd0f7f): same checks + before/after crops at rock
     shadows (fid/pt/dev28/crops/)."""
import hashlib, json, os, sys
import numpy as np
from PIL import Image
from scipy import ndimage
Image.MAX_IMAGE_PIXELS = None
C9 = "/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9"
FID = C9 + "/barrow_v2/fid"
sys.path.insert(0, FID + "/v1tools")
import dev28  # noqa: E402
OUT = FID + "/pt/dev28"
os.makedirs(OUT + "/crops", exist_ok=True)
LIT = np.array([206, 198, 190], float)


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def checker(a):
    g = a.astype(np.float32).mean(-1)
    cb = np.abs(g[:-1, :-1] - g[1:, :-1] - g[:-1, 1:] + g[1:, 1:]) / 4.0
    e = np.zeros_like(g)
    e[:-1, :-1] = cb
    return e


def snow_masks(a):
    af = a.astype(float)
    s = (af * LIT).sum(-1) / (LIT * LIT).sum()
    resid = np.abs(af - s[..., None] * LIT).max(-1)
    snowish = (resid < 16) & (s > 0.4) & (s < 1.08)
    lit = ndimage.binary_erosion(snowish & (s >= 0.93), iterations=3)
    edge = ndimage.binary_dilation(snowish & (s < 0.9), iterations=3) & ndimage.binary_dilation(snowish & (s >= 0.93), iterations=3) & snowish
    shadow = snowish & (s < 0.9)
    return lit, edge, shadow


def run_guide(name, gpath, ipath):
    G = Image.open(gpath).convert("RGB")
    I = Image.open(ipath).convert("RGB")
    out, rep = dev28.smooth(G, I)
    a = np.asarray(G)
    b = np.asarray(out)
    ids = np.asarray(I)
    seg = (ids[..., 0].astype(np.int64) << 16) | (ids[..., 1].astype(np.int64) << 8) | ids[..., 2]
    _, _, zone = dev28.detect(a)
    zone = zone & ~((ndimage.maximum_filter(seg, size=3) != ndimage.minimum_filter(seg, size=3)) | (a.astype(float).mean(-1) < dev28.INK_GREY))
    changed = (a != b).any(-1)
    lit, edge, shadow = snow_masks(a)
    # per-object mean colour drift (objects >= 2000 px): colour can only move inside an object, never across
    lab = np.unique(seg, return_inverse=True)[1].reshape(seg.shape)
    cnt = np.bincount(lab.ravel())
    drift = 0.0
    for c in range(3):
        m0 = np.bincount(lab.ravel(), a[..., c].ravel().astype(float)) / cnt
        m1 = np.bincount(lab.ravel(), b[..., c].ravel().astype(float)) / cnt
        drift = max(drift, float(np.abs(m1 - m0)[cnt >= 2000].max()))
    boundary = ndimage.morphological_gradient(lab, size=3) > 0
    ce0, ce1 = checker(a), checker(b)
    r = {"guide": gpath.replace(C9 + "/", ""), "guide_sha12": sha(gpath)[:12], "ids": ipath.replace(C9 + "/", ""), "ids_sha12": sha(ipath)[:12],
         "dev28": rep,
         "changed_outside_zone_px": int((changed & ~zone).sum()),
         "changed_share_of_frame": float(changed.mean()),
         "object_mean_colour_drift_max_levels": round(drift, 3),
         "boundary_px_changed_share": float((changed & boundary).sum() / max(1, boundary.sum())),
         "zone_checker_energy": [round(float(ce0[zone].mean()), 3), round(float(ce1[zone].mean()), 3)],
         "ink_px_changed": int((changed & (a.astype(float).mean(-1) < dev28.INK_GREY)).sum()),
         "lit_snow_px_changed": int((changed & lit).sum()), "lit_snow_px": int(lit.sum()),
         "shadow_edge_checker_energy": [round(float(ce0[edge].mean()), 3), round(float(ce1[edge].mean()), 3)],
         "shadow_on_snow_checker_energy": [round(float(ce0[shadow].mean()), 3), round(float(ce1[shadow].mean()), 3)],
         "shadow_on_snow_mean_rgb": [np.round(a[shadow].mean(0), 2).tolist(), np.round(b[shadow].mean(0), 2).tolist()]}
    print(name, json.dumps(r))
    assert r["changed_outside_zone_px"] == 0, "pixels changed outside the dither zone"
    assert r["boundary_px_changed_share"] == 0.0 and r["ink_px_changed"] == 0, "a silhouette rim or ink pixel changed"
    return r, a, b


def synthetic():
    H = W = 160
    a = np.zeros((H, W, 3), np.uint8); a[:] = LIT
    ids = np.zeros((H, W, 3), np.uint8)
    a[30:70, 20:60] = (143, 141, 140); ids[30:70, 20:60] = (24, 8, 200)          # the rock, its own ID
    sh = np.rint(LIT * 0.72).astype(np.uint8)
    a[70:110, 20:60] = sh                                                      # hard-edged shadow below it
    yy, xx = np.mgrid[0:H, 0:W]
    bayer = np.array([[0, 2], [3, 1]])[yy % 2, xx % 2]
    cov = np.clip((xx - 90) / 20.0, 0, 1)                                      # PCF ramp x 90..110, dithered
    dith = (bayer / 4.0 + 0.125) < cov
    reg = (yy >= 40) & (yy < 120) & (xx >= 80)
    a[reg & dith] = sh
    b = np.asarray(dev28.smooth(Image.fromarray(a), Image.fromarray(ids))[0])
    ch = (a != b).any(-1)
    rock = (ids != 0).any(-1)
    hard = np.zeros((H, W), bool); hard[60:120, 10:70] = True
    ramp = reg & (xx >= 88) & (xx < 112)
    ce0, ce1 = checker(a), checker(b)
    r = {"rock_px_changed": int((ch & rock).sum()), "hard_shadow_region_px_changed": int((ch & hard).sum()),
         "flat_far_px_changed": int((ch & (xx > 130)).sum() + (ch & (xx < 75) & ~hard & ~rock).sum()),
         "dither_ramp_checker_energy": [round(float(ce0[ramp].mean()), 3), round(float(ce1[ramp].mean()), 3)],
         "dither_ramp_mean_grey": [round(float(a[ramp].mean()), 2), round(float(b[ramp].mean()), 2)]}
    print("synthetic", json.dumps(r))
    assert r["rock_px_changed"] == 0 and r["hard_shadow_region_px_changed"] == 0 and r["flat_far_px_changed"] == 0
    assert r["dither_ramp_checker_energy"][1] < 0.25 * r["dither_ramp_checker_energy"][0]
    return r


def crops(a, b, cls, n=4, size=256, win=(4096, 2560)):
    """crops centred on the strongest dither next to ROCK (class 5) over SNOW (class 1) shadows"""
    rock = ndimage.binary_dilation(cls == 5, iterations=10)
    snow = cls == 1
    e = checker(a) * (rock & snow)
    pts = []
    e2 = ndimage.uniform_filter(e, 41)
    e2[win[1] - size // 2:, :] = 0; e2[:, win[0] - size // 2:] = 0   # inside the pilot window
    for _ in range(n):
        y, x = np.unravel_index(np.argmax(e2), e2.shape)
        pts.append((int(x), int(y)))
        e2[max(0, y - size):y + size, max(0, x - size):x + size] = 0
    out = []
    for i, (x, y) in enumerate(pts):
        x0 = int(np.clip(x - size // 2, 0, a.shape[1] - size)); y0 = int(np.clip(y - size // 2, 0, a.shape[0] - size))
        A = Image.fromarray(a[y0:y0 + size, x0:x0 + size]).resize((size * 2, size * 2), Image.NEAREST)
        B = Image.fromarray(b[y0:y0 + size, x0:x0 + size]).resize((size * 2, size * 2), Image.NEAREST)
        sheet = Image.new("RGB", (size * 4 + 8, size * 2), (255, 255, 255))
        sheet.paste(A, (0, 0)); sheet.paste(B, (size * 2 + 8, 0))
        p = "%s/crops/rock_shadow_%d_x%d_y%d.png" % (OUT, i, x0, y0)
        sheet.save(p)
        out.append({"file": p.replace(FID + "/", ""), "px": [x0, y0, size, size], "layout": "left = before, right = DEV-28; 2x nearest"})
    return out


TARGETS = {"stone_circle": ["ring_stones", "ring_fallen"], "cliff_top_boulders": ["cliff_faces", "carved_rock", "ground_rock", "ledge_rocks"],
           "barrow_door_rocks": ["barrow_cutting", "door_post_L", "door_post_R", "door_lintel", "barrow_front"]}


def target_crops(a, b, ids, table, tag, win=(4096, 2560)):
    """per target: the centre of the guide's dither (DEV-28 zone, changed pixels) on the snow around those objects, inside the
    pilot window; two sheets each, before | after: DETAIL 320 x 320 at 1:1 and PLAY 960 x 540 at 1:1 (the guide is rendered at
    the play camera's own px/m, so 1 guide px = 1 play px at 1920 x 1080: PLAY is half a play frame at play zoom)"""
    gid = (ids[..., 0].astype(np.int64) << 16) | (ids[..., 1].astype(np.int64) << 8) | ids[..., 2]
    name2id = {v["id"]: int(k) for k, v in table.items()}
    snow = gid == name2id["ground_snow"]
    changed = (a != b).any(-1)
    out = {}
    for t, names in TARGETS.items():
        m = np.isin(gid, [name2id[n] for n in names if n in name2id])
        m[win[1]:, :] = False; m[:, win[0]:] = False
        near = ndimage.binary_dilation(m, iterations=60) & snow & changed
        near[win[1]:, :] = False; near[:, win[0]:] = False
        if not near.any():
            out[t] = {"none": "no DEV-28 change on snow near %s inside the pilot window" % names}
            continue
        dens = ndimage.uniform_filter(near.astype(np.float32), 121)
        y, x = np.unravel_index(np.argmax(dens), dens.shape)
        out[t] = {"objects": names, "centre_px": [int(x), int(y)], "changed_px_near": int(near.sum())}
        for nm, (w, h) in (("detail_1to1", (320, 320)), ("play_zoom", (960, 540))):
            x0 = int(np.clip(x - w // 2, 0, a.shape[1] - w)); y0 = int(np.clip(y - h // 2, 0, a.shape[0] - h))
            sheet = Image.new("RGB", (w * 2 + 8, h), (255, 255, 255))
            sheet.paste(Image.fromarray(a[y0:y0 + h, x0:x0 + w]), (0, 0))
            sheet.paste(Image.fromarray(b[y0:y0 + h, x0:x0 + w]), (w + 8, 0))
            p = "%s/crops_%s/%s_%s_x%d_y%d.png" % (OUT, tag, t, nm, x0, y0)
            os.makedirs(os.path.dirname(p), exist_ok=True)
            sheet.save(p)
            out[t][nm] = {"file": p.replace(FID + "/", ""), "px": [x0, y0, w, h], "layout": "left = guide as pinned, right = DEV-28; 1:1"}
    print("crops", json.dumps(out))
    return out


def flag_check():
    """the Tier-B block itself, executed in isolation on a small guide: unset -> the same GUIDE object (v1's guide,
    untouched); =1 -> smoothed; a wrong ID sha -> HALT (SystemExit)"""
    import pathlib, hashlib as hl
    src = open(FID + "/v1tools/tierB/conductor_scripts/guided_paint.py").read()
    blk = src[src.index("# BV2F-BEGIN DEV-28"):src.index("# BV2F-END", src.index("# BV2F-BEGIN DEV-28"))]
    a = np.zeros((64, 64, 3), np.uint8); a[:] = LIT
    yy, xx = np.mgrid[0:64, 0:64]; a[((yy + xx) % 2 == 0) & (xx > 20) & (xx < 40)] = np.rint(LIT * 0.75)
    ids = np.zeros_like(a); tmp = OUT + "/_flagcheck_ids.png"; Image.fromarray(ids).save(tmp)
    res = {}
    for name, env, want in (("unset", None, None), ("on", "1", None), ("on_wrong_sha", "1", "0" * 64)):
        g0 = Image.fromarray(a)
        ns = {"os": os, "sys": sys, "json": json, "pathlib": pathlib, "hashlib": hl, "Image": Image, "GUIDE": g0, "cmd": "stage",
              "cfg": {"dev28_ids": tmp, "dev28_ids_sha256": want or sha(tmp)}, "__file__": FID + "/v1tools/tierB/conductor_scripts/guided_paint.py"}
        if env is None:
            os.environ.pop("BV2F_DEV28", None)
        else:
            os.environ["BV2F_DEV28"] = env
        try:
            exec(blk, ns)
            res[name] = {"same_object": ns["GUIDE"] is g0, "bytes_equal": ns["GUIDE"].tobytes() == g0.tobytes()}
        except SystemExit as e:
            res[name] = {"halt": str(e)[:60]}
    os.environ.pop("BV2F_DEV28", None)
    os.replace(tmp, OUT + "/flagcheck_ids_black.png")
    print("flag", json.dumps(res))
    assert res["unset"]["same_object"] and not res["on"]["bytes_equal"] and "halt" in res["on_wrong_sha"]
    return res


if __name__ == "__main__":
    rec = {"_what": "DEV-28 constructed test (R-C9-257 (c)); dev28.py sha12 " + sha(FID + "/v1tools/dev28.py")[:12]}
    rec["synthetic"] = synthetic()
    rec["flag"] = flag_check()
    rec["v1_guide"], _, _ = run_guide("v1", C9 + "/barrow_full/paint/barrow_full_guide.png", C9 + "/barrow_full/take/ids/ids.png")
    # OUR guide: a guide + ID + class render of ONE pinned set (argv: guide ids class); without them it is skipped
    # (the pilot pin 1c22764cb874 kept no copy of its ID render, and LV's ids_art.png has since been re-rendered)
    if len(sys.argv) >= 4:
        g, i, c = sys.argv[1:4]
        rec["our_guide"], a, b = run_guide("ours", g, i)
        if len(sys.argv) >= 6:   # targeted crops: <manifest json> <tag>  (R-C9-260: stone circle, cliff-top boulders, door rocks)
            rec["crops"] = target_crops(a, b, np.asarray(Image.open(i).convert("RGB")), json.load(open(sys.argv[4]))["id_table"], sys.argv[5])
        else:
            rec["crops"] = crops(a, b, np.asarray(Image.open(c)))
    else:
        rec["our_guide"] = "SKIPPED: no pinned guide+ID+class set given (pilot pin kept no ID copy; LV re-rendering)"
    json.dump(rec, open(OUT + "/dev28_test.json", "w"), indent=1)
    print("OK")
