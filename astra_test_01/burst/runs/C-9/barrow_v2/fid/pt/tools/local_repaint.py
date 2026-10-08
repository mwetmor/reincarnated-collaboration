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
    """the pixels to repaint, canvas-local. mode "dark_lines" (default): thin dark lines on bright ground, dilated, inside
    the region classes; "classes" (R-C9-263): the seed classes inside seed_box, dilated, inside the region classes;
    "box": the seed_box itself, inside the region classes"""
    mode = S["region"].get("mode", "dark_lines")
    if mode in ("classes", "box"):
        bx = S["region"]["seed_box"]
        keep = np.zeros((CH, CW), bool); keep[bx[1]:bx[3], bx[0]:bx[2]] = True
        rc = crop(cls_in(S["region"]["classes"]))
        if mode == "box":
            return keep & rc
        seed = crop(cls_in(S["region"]["seed_classes"])) & keep
        R = ndimage.binary_dilation(seed, iterations=int(S["region"]["dilate_px"]))
        up = int(S["region"].get("extend_up_px", 0))   # painted stalks stand UP the screen from their ground footprint
        if up:
            col = R.copy()
            for k in range(1, up + 1):
                col[:-k] |= R[k:]
            R = col
        R &= rc
        return ndimage.binary_closing(R, iterations=4) & rc
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
    if S.get("fill") == "class_tint":
        # R-C9-263: the guide's flat CLASS TINTS (no rendered geometry): LV's reed_tufts are stiff vertical posts in the
        # render, which is what the painter copied as cattail stalks -- a post pixel takes the reed tint only on the reed
        # bed's footprint (ground_reed, grown 3 px), the snow tint elsewhere
        import subprocess
        mf = json.loads(subprocess.check_output(["git", "-C", FID, "show", "%s:astra_test_01/burst/runs/C-9/barrow_v2/fid/lv/guide_art/guide_manifest.json" % S["class_commit"]]))
        assert hashlib.sha256(open(S["ids_png"], "rb").read()).hexdigest() == S["ids_sha256"], "ids are not the pinned ones"
        I = np.asarray(Image.open(S["ids_png"]).convert("RGB")).astype(np.int64)
        gid = crop((I[..., 0] << 16) | (I[..., 1] << 8) | I[..., 2])
        n2i = {v["id"]: int(k) for k, v in mf["id_table"].items()}
        tint = {i: np.rint(np.array(mf["tints_srgb"].get(n, [0.5, 0.5, 0.5])) * 255).astype(np.uint8) for i, n in enumerate(cm["classes"])}
        C = crop(CL)
        fillimg = np.zeros((CH, CW, 3), np.uint8)
        for i, t in tint.items():
            fillimg[C == i] = t
        post = gid == n2i["reed_tufts"]
        bed = ndimage.binary_dilation(gid == n2i["ground_reed"], iterations=3)
        fillimg[post & bed] = tint[cm["classes"].index("reed")]
        fillimg[post & ~bed] = tint[cm["classes"].index("snow")]
        can[R] = fillimg[R]
    elif S.get("fill") == "guide":   # R-C9-263: the pinned GUIDE's own pixels in the patch (shape and class layout to paint)
        assert hashlib.sha256(open(S["guide_png"], "rb").read()).hexdigest() == S["guide_sha256"], "guide is not the pinned one"
        can[R] = crop(np.asarray(Image.open(S["guide_png"]).convert("RGB")))[R]
    else:
        can[R] = np.array(S["fill_rgb"], np.uint8)          # a flat greybox patch: the painter paints it, as it paints a guide
    Image.fromarray((crop(cls_in(S["paste_classes"])) * 255).astype(np.uint8)).save(os.path.join(OUT, "paste_classes.png"))
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
elif CMD == "pin":
    # R-C9-263: the cfg dev24 entry for this patch (attempt ATT), every file sha-pinned
    sh = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
    np_ = "%s/%s/%s.png" % (A9, bid, bid)
    ent = {"name": "%s-%s" % (S["name"], ATT), "rect_xy": [x0, y0],
           "region_png": os.path.join(OUT, "region.png"), "region_sha256": sh(os.path.join(OUT, "region.png")),
           "paste_png": os.path.join(OUT, "paste_classes.png"), "paste_sha256": sh(os.path.join(OUT, "paste_classes.png")),
           "new_png": np_, "new_sha256": sh(np_)}
    json.dump(ent, open(os.path.join(OUT, "pin_%s.json" % ATT), "w"), indent=1)
    print(json.dumps(ent))
elif CMD == "paste":
    R = np.asarray(Image.open(os.path.join(OUT, "region.png"))) > 127
    new = np.asarray(Image.open("%s/%s/%s.png" % (A9, bid, bid)).convert("RGB")).astype(np.float64)
    old = crop(P8).astype(np.float64)
    pc = crop(cls_in(S["paste_classes"]))
    sys.path.insert(0, os.path.join(FID, "v1tools")); import dev24   # R-C9-263: the ONE paste the Tier-B stitch also runs
    out, w, corr, M = dev24.paste_local(old, new, R, pc)
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
