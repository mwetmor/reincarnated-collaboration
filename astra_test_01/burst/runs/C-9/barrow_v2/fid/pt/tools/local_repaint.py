#!/usr/bin/env python3
"""BV2F PT DEV-24 PROTOTYPE (R-C9-243): a MASKED LOCAL REPAINT -- one region of a finished pilot painting repainted with
its PAINTED surroundings as the context, pasted back class-masked with a low-frequency tone match (DEV-23's idea, on a
ring round the region). No wavefront, no neighbour cascade. OFF the build: reads the build's painting, writes only under
fid/pt/dev24/<name>/ and the burst's own brief/artifacts. (The Tier-B form is specified in fid/pt/dev24/DEV24_SPEC.md.)
    python3 fid/pt/tools/local_repaint.py <spec.json> stage|brief|paste [attempt]
spec: {name, prefix, painting, rect_xy [x0, y0] (the 1536x1024 canvas in plate px), region: {classes [..], seed
"dark_lines", dilate_px}, paste_classes [..], fill_rgb, note, cfg (the pilot cfg: geo/rules/refs/run_tag/experiment)}"""
import hashlib, json, os, sys
import numpy as np
from PIL import Image
from scipy import ndimage
FID = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
B = "/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst"
A9 = B + "/runs/C-9/artifacts"
S = json.load(open(sys.argv[1]))
CMD = sys.argv[2]
ATT = sys.argv[3] if len(sys.argv) > 3 else "1"
OUT = os.path.join(FID, "pt", "dev24", S["name"])
os.makedirs(OUT, exist_ok=True)
CW, CH = 1536, 1024
x0, y0 = S["rect_xy"]
P8 = np.asarray(Image.open(S["painting"]).convert("RGB"))
# R-C9-262 (revival): the class map is the PINNED one named by the spec (class_png + the LV commit whose manifest names its
# classes), never LV's live working file; unset = the R-C9-243 behaviour (LV's guide_art files)
if "class_png" in S:
    import subprocess
    cm = json.loads(subprocess.check_output(["git", "-C", FID, "show", "%s:astra_test_01/burst/runs/C-9/barrow_v2/fid/lv/guide_art/guide_manifest.json" % S["class_commit"]]))["class"]
    assert hashlib.sha256(open(S["class_png"], "rb").read()).hexdigest() == S["class_sha256"], "class map is not the pinned one"
    CL = np.asarray(Image.open(S["class_png"]))
else:
    cm = json.load(open(FID + "/lv/guide_art/guide_manifest.json"))["class"]
    CL = np.asarray(Image.open(FID + "/lv/guide_art/class_art.png"))
CL = (CL[..., 0] if CL.ndim == 3 else CL)[:P8.shape[0], :P8.shape[1]]
cls_in = lambda names: np.isin(CL, [cm["classes"].index(n) for n in names if n in cm["classes"]])
crop = lambda a: a[y0:y0 + CH, x0:x0 + CW]
bid = "%s-%s-%s" % (S["prefix"], S["name"], ATT)


def region():
    """the pixels to repaint, canvas-local: the seed (thin dark lines on bright ground) dilated, inside the region classes"""
    L = P8.astype(np.float64).mean(-1)
    loc = ndimage.gaussian_filter(L, 8)
    th, lmin = S["region"].get("seed_dark", 45), S["region"].get("seed_loc_min", 170)   # R-C9-262: the blue mere is darker than rp3's
    seed = crop((L < loc - th) & (loc > lmin) & cls_in(S["region"].get("seed_classes", S["region"]["classes"])))
    if "seed_box" in S["region"]:     # canvas-local [x0, y0, x1, y1]: the target only
        bx = S["region"]["seed_box"]; keep = np.zeros_like(seed); keep[bx[1]:bx[3], bx[0]:bx[2]] = True; seed &= keep
    R = ndimage.binary_dilation(seed, iterations=int(S["region"]["dilate_px"])) & crop(cls_in(S["region"]["classes"]))
    R = ndimage.binary_closing(R, iterations=6) & crop(cls_in(S["region"]["classes"]))
    return R


if CMD == "stage":
    R = region()
    can = crop(P8).copy()
    can[R] = np.array(S["fill_rgb"], np.uint8)          # a flat greybox patch: the painter paints it, as it paints a guide
    Image.fromarray(can).save(os.path.join(OUT, "canvas.png"))
    # registered as the frozen guided_paint stages its canvases (CS9-guides/manifest.json: refs_guard's (b)-class rule)
    cp = A9 + "/CS9-guides/%s_canvas.png" % bid
    Image.fromarray(can).save(cp)
    mp = A9 + "/CS9-guides/manifest.json"
    man = json.load(open(mp)) if os.path.exists(mp) else {}
    man[os.path.basename(cp)] = hashlib.sha256(open(cp, "rb").read()).hexdigest()
    json.dump(man, open(mp, "w"), indent=1)
    Image.fromarray((R * 255).astype(np.uint8)).save(os.path.join(OUT, "region.png"))
    json.dump({"rect_xy": [x0, y0], "region_px": int(R.sum()), "painting_sha256": hashlib.sha256(open(S["painting"], "rb").read()).hexdigest()},
              open(os.path.join(OUT, "stage.json"), "w"), indent=1)
    print("staged", int(R.sum()), "px")
elif CMD == "brief":
    cfg = json.load(open(S["cfg"]))
    text = ("GENERATE BURST %s — %s, a LOCAL REPAINT of one small region of the finished BV2F pilot painting (%s). task_id \"%s\".\n\n"
            "IMAGE 1 is the canvas to EDIT (1536x1024): it is ALREADY PAINTED everywhere EXCEPT one flat pale blue-grey "
            "patch (a greybox area). Paint ONLY that patch, so that it CONTINUES the painting round it seamlessly -- same "
            "brushwork, grain, tone and light; no visible edge where the patch ends. Everything outside the patch must stay "
            "exactly as it is. What the patch is: %s\n%s\n\n"
            "One image_gen EDIT call. ONE retry only if anything outside the patch changed, an edge or join of the patch "
            "remains visible, or the patch is still flat -- name the reason. Copy the output to out/%s.png with sha256. "
            "No code. No other files. No web.\nRETURN: receipt task_id \"%s\"; images = the file with prompt, references and "
            "elapsed_s; calls_used = the TRUE number of image_gen calls; status; concerns. Never PASS/FAIL."
            ) % (bid, cfg.get("run_tag", ""), S.get("ruling", "R-C9-243"), bid, S["note"], cfg["rules"], bid, bid)
    refs = [{"path": A9 + "/CS9-guides/%s_canvas.png" % bid, "role": "IMAGE 1 — the canvas to EDIT (the finished painting + ONE greybox patch to paint)"}] + \
           [{"path": p, "role": "IMAGE %d — %s" % (i + 2, role)} for i, (p, role) in enumerate(cfg["refs"])]
    json.dump({"text": text, "references": refs, "image_cap": 2, "minutes_cap": 15, "tool_call_cap": 20,
               "outputs": ["out/%s.png" % bid], "effort": "high", "add_dirs": [], "experiment": cfg["experiment"]},
              open(B + "/briefs/C-9/%s.task.json" % bid, "w"), indent=1, ensure_ascii=False)
    print(bid, "brief ok")
elif CMD == "paste":
    R = np.asarray(Image.open(os.path.join(OUT, "region.png"))) > 127
    new = np.asarray(Image.open("%s/%s/%s.png" % (A9, bid, bid)).convert("RGB")).astype(np.float64)
    old = crop(P8).astype(np.float64)
    pc = crop(cls_in(S["paste_classes"]))
    # the paste: the region grown 12 px, within the paste classes, feathered 6 px
    M = ndimage.binary_dilation(R, iterations=12) & pc
    w = ndimage.gaussian_filter(M.astype(np.float64), 6) * pc
    # tone match: on a ring of paste-class pixels just OUTSIDE the paste, the low-frequency difference old - new,
    # spread by normalised convolution (sigma 48) over the paste
    ring = ndimage.binary_dilation(M, iterations=40) & ~ndimage.binary_dilation(M, iterations=8) & pc
    num = np.stack([ndimage.gaussian_filter((old - new)[..., i] * ring, 48) for i in range(3)], -1)
    den = ndimage.gaussian_filter(ring.astype(np.float64), 48)[..., None]
    corr = num / np.maximum(den, 1e-6) * (den > 0.02)
    newc = new + corr
    out = old * (1 - w[..., None]) + newc * w[..., None]
    full = P8.copy()
    full[y0:y0 + CH, x0:x0 + CW] = np.clip(out + 0.5, 0, 255).astype(np.uint8)
    Image.fromarray(full).save(os.path.join(OUT, "painting_patched_%s.png" % ATT))
    # outside the paste mask nothing may change
    ch = np.abs(full.astype(int) - P8.astype(int)).max(-1)
    outside = np.ones(P8.shape[:2], bool); outside[y0:y0 + CH, x0:x0 + CW] = ~(w > 0)
    rep = {"bid": bid, "paste_px": int(M.sum()), "changed_px_outside_paste": int((ch[outside] > 0).sum()),
           "tone_corr_mean_abs": round(float(np.abs(corr[M]).mean()), 2) if M.any() else None,
           "dark_line_px_before": int(((old.mean(-1) < ndimage.gaussian_filter(old.mean(-1), 8) - S["region"].get("seed_dark", 45)) & M).sum()),
           "dark_line_px_after": int(((out.mean(-1) < ndimage.gaussian_filter(out.mean(-1), 8) - S["region"].get("seed_dark", 45)) & M).sum())}
    json.dump(rep, open(os.path.join(OUT, "paste_%s.json" % ATT), "w"), indent=1)
    print(rep)
