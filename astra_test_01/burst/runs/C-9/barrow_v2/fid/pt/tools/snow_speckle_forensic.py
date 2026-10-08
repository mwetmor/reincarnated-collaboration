#!/usr/bin/env python3
"""BV2F PT (R-C9-268 item 1; jack-ryan pilot-4 Gate-2 s4): SNOW-GRAIN FORENSIC, 0 images, no Godot.
Is the fine single-pixel speckle the P11 judge cited ("fine single-pixel speckle on the paper grain") in the PAINTING or
added by the RENDER (bakes / mips / filtering / the pen pass)?
  A. The confident-trial pilot crops (P11 v3 keys: trials 07 22 25 26 39 61 + 12 17 28 46 49 + wrong 21 41) located in the
     painting: plate px from the still's camera centre (1 still px = 1 plate px: the stills and the plate share the play
     camera's px/m), refined by a +-48 px NCC search; the same crop measured in the STILL and in the PAINTING.
  B. The same measures on v1 (its own stills vs its own painting, the same alignment) = the CONTROL: what v1's render does
     to v1's paint.
  C. Per paint chunk: snow support (px and 64-px windows at >= 70 % coverage, P4's own window rule) for pilot 4 and v1.
Measures, on L* (CIE), snow-class pixels only (the still's class mask; the painting's pinned class map), eroded 2 px:
  speck = mean |L - median3x3(L)|            (single-pixel speckle)
  hf1   = std(L - G(0.7))                    (1-px band)       hf2 = std(G(0.7) - G(1.6))   (2-3 px band)
  r12   = hf1 / hf2                          (> 1: energy concentrated at the single pixel)
    python3 fid/pt/tools/snow_speckle_forensic.py  -> fid/pt/r268/snow_speckle.json"""
import json, os
import numpy as np
from PIL import Image
from scipy import ndimage
Image.MAX_IMAGE_PIXELS = None
FID = "/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/barrow_v2/fid"
C9 = os.path.dirname(os.path.dirname(FID))
OUT = FID + "/pt/r268"
os.makedirs(OUT, exist_ok=True)
PPM, PPV = 100.617553710938, 80.3076
PILOT = {"u0": -33.5757, "v1": 22.3699, "painting": FID + "/pt/pilot/painting.png"}
V1 = {"u0": -28.715, "v1": 17.7203, "painting": C9 + "/barrow_full/paint/barrow_full_painted.png"}


def lab_L(a):
    x = a.astype(np.float64) / 255.0
    c = np.where(x <= 0.04045, x / 12.92, ((x + 0.055) / 1.055) ** 2.4)
    Y = c @ np.array([0.2126729, 0.7151522, 0.0721750])
    f = np.where(Y > 216 / 24389, np.cbrt(Y), (24389 / 27 * Y + 16) / 116)
    return 116 * f - 16


def measures(L, m):
    m = ndimage.binary_erosion(m, iterations=2)
    if m.sum() < 500:
        return None
    med = ndimage.median_filter(L, 3)
    g07, g16 = ndimage.gaussian_filter(L, 0.7), ndimage.gaussian_filter(L, 1.6)
    hf1, hf2 = (L - g07)[m].std(), (g07 - g16)[m].std()
    return {"px": int(m.sum()), "speck": round(float(np.abs(L - med)[m].mean()), 3), "hf1": round(float(hf1), 3),
            "hf2": round(float(hf2), 3), "r12": round(float(hf1 / max(hf2, 1e-6)), 3)}


def align(still_crop, P, x0, y0, r=48):
    """NCC of the still crop's L* against the painting around (x0, y0)"""
    s = lab_L(still_crop)
    s = (s - s.mean()) / (s.std() + 1e-6)
    h, w = s.shape
    best = (-2, x0, y0)
    for dy in range(-r, r + 1, 2):
        for dx in range(-r, r + 1, 2):
            x, y = x0 + dx, y0 + dy
            if x < 0 or y < 0 or x + w > P.shape[1] or y + h > P.shape[0]:
                continue
            p = lab_L(P[y:y + h, x:x + w])
            p = (p - p.mean()) / (p.std() + 1e-6)
            c = float((s * p).mean())
            if c > best[0]:
                best = (c, x, y)
    c, x, y = best
    for dy in (-1, 0, 1):   # 1-px refinement
        for dx in (-1, 0, 1):
            xx, yy = x + dx, y + dy
            if xx < 0 or yy < 0 or xx + w > P.shape[1] or yy + h > P.shape[0]:
                continue
            p = lab_L(P[yy:yy + h, xx:xx + w]); p = (p - p.mean()) / (p.std() + 1e-6)
            cc = float((s * p).mean())
            if cc > c:
                c, x, y = cc, xx, yy
    return c, x, y


def main():
    keys = json.load(open(FID + "/ph/p11/keys/abx3_pilot4_v1_vs_pilot.json"))["trials"]
    pv = {v["name"]: v for v in json.load(open(FID + "/pt/pilot/stills_views.json"))["views"]}
    v1v = json.load(open(FID + "/pc/v1_stills/views.json"))["views"]
    P = np.asarray(Image.open(PILOT["painting"]).convert("RGB"))
    V = np.asarray(Image.open(V1["painting"]).convert("RGB"))
    # snow masks in the paintings: pilot = pinned class map (snow); v1 = PH's v1 class masks (p4_texture.v1_classes)
    import subprocess, sys
    man = json.loads(subprocess.check_output(["git", "-C", FID, "show", "b5894d440:astra_test_01/burst/runs/C-9/barrow_v2/fid/lv/guide_art/guide_manifest.json"]))
    cls = np.asarray(Image.open(FID + "/pt/pilot/class_art_pinned_ps4.png"))[:P.shape[0], :P.shape[1]]
    psnow = cls == man["class"]["classes"].index("snow")
    sys.path.insert(0, FID + "/ph/harness")
    import p4_texture as T
    vmask = T.v1_classes()[0]["snow"]
    snow_id = None
    res = {"_what": __doc__.split("\n")[0], "pilot_crops": [], "v1_crops": [], "chunks": {}}
    trials = ["trial_07", "trial_22", "trial_25", "trial_26", "trial_39", "trial_61", "trial_12", "trial_17", "trial_28",
              "trial_46", "trial_49", "trial_21", "trial_41"]
    seen = set()
    for t in trials:
        d = keys[t]
        for side in "ABX":
            s = d[side]
            pil = "pilot_stills" in s["src"]
            if not pil and "/pc/v1_stills/" not in s["src"]:
                continue   # v1 crops from other still sets (no camera record here) are skipped
            name = os.path.basename(s["src"])[:-4]
            key = (name, tuple(s["rect"]))
            if key in seen:
                continue
            seen.add(key)
            x, y, w, h = s["rect"]
            st = np.asarray(Image.open(s["src"]).convert("RGB"))[y:y + h, x:x + w]
            if pil:
                cu, cv = pv[name]["camera_centre_ground_uv"]; F, Pimg, pm = PILOT, P, psnow
                cm = np.asarray(Image.open(s["src"].replace(".png", ".classes.png")))[y:y + h, x:x + w]
                mp = json.load(open(FID + "/pt/pilot_stills/classes_mapping.json"))
                sm = cm == int(mp["values"]["snow"])
            else:
                cu, cv = v1v[name]["camera"]["centre_ground_uv"]; F, Pimg, pm = V1, V, vmask
                sm = None
            x0 = int(round((cu - F["u0"]) * PPM + x - 960)); y0 = int(round((F["v1"] - cv) * PPV + y - 540))
            c, px, py = align(st, Pimg, x0, y0)
            pcrop = Pimg[py:py + h, px:px + w]
            msk_p = pm[py:py + h, px:px + w]
            msk_s = sm if sm is not None else msk_p     # v1: no still class mask -> the aligned painting's snow
            both = msk_p & msk_s
            row = {"trial": t, "side": side, "class": s["class"], "still_name": name, "rect": [x, y, w, h],
                   "plate_xy": [px, py], "ncc": round(c, 3), "snow_px": int(both.sum()),
                   "still": measures(lab_L(st), both), "painting": measures(lab_L(pcrop), both)}
            (res["pilot_crops"] if pil else res["v1_crops"]).append(row)
    # C. snow support per chunk (P4's 64-px windows at >= 70 % coverage, step 32)
    def support(mask, rects):
        out = {}
        for k, (x0, y0, x1, y1) in rects:
            m = mask[y0:y1, x0:x1]
            cov = ndimage.uniform_filter(m.astype(np.float32), 64)[32::32, 32::32]
            out[k] = {"snow_px": int(m.sum()), "windows_ge70": int((cov >= 0.7).sum())}
        return out
    res["chunks"]["pilot4"] = support(psnow, [("%d_%d" % (c, r), (1280 * c, 768 * r, 1280 * c + 1536, 768 * r + 1024)) for r in range(3) for c in range(3)])
    res["chunks"]["v1"] = support(vmask, T.v1_chunks())
    # summary: median over aligned crops (ncc >= 0.5), snow-class crops and all
    def summ(rows):
        ok = [r for r in rows if r["ncc"] >= 0.5 and r["still"] and r["painting"]]
        f = lambda k, w: round(float(np.median([r[w][k] for r in ok])), 3) if ok else None
        return {"n": len(ok), **{"%s_%s" % (w, k): f(k, w) for w in ("still", "painting") for k in ("speck", "hf1", "r12")}}
    res["summary"] = {"pilot": summ(res["pilot_crops"]), "v1": summ(res["v1_crops"])}
    json.dump(res, open(OUT + "/snow_speckle.json", "w"), indent=1)
    print(json.dumps(res["summary"], indent=1))
    for r in res["pilot_crops"] + res["v1_crops"]:
        print(r["trial"], r["side"], r["still_name"], r["class"], "ncc", r["ncc"], "snow", r["snow_px"],
              "still", r["still"] and (r["still"]["speck"], r["still"]["r12"]), "paint", r["painting"] and (r["painting"]["speck"], r["painting"]["r12"]))


if __name__ == "__main__":
    main()
