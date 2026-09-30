# HER GEAR STACKS, CHECKED (the conductor, 2026-09-30, for Matt's R-C9-69 test: GEAR steps her from the base body to the
# full costume A on the phone page). Reads the renders of film_rt/gear_stills.gd -- every stack of the scene package, at the
# play camera, 1x and 2x, beauty + ID + paint-class passes -- and answers the three questions asked of each stack:
#   PAINT       is anything UNPAINTED showing where a garment used to cover? The class pass colours every visible body
#               pixel by what its texel is: PAINTED by a projection camera (06b_bake's own mask, work/tex_AB_mask.png),
#               FILLED by the bake from its nearest painted texel, or BARE (no colour at all). Counted over the body,
#               and over the pixels each stack REVEALS against the full kit
#   SEE-THROUGH the body seen through a garment: scripts/s11_count.py, unchanged, per stack (a HOLE = body with garment on
#               6 of its 8 sides; an isolated PALE dot = the speckle you see; the robe's front split and slits are the
#               design's own openings and are reported apart)
#   STILLS      2x sheets per stack for the look: idle and walk, headings 25 and 205
#
#   python3 scripts/s19_gear_stacks.py <renders dir> <out stills dir>      -> work/s19_gear_stacks.json
import json, os, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
D, OUTD = sys.argv[1], sys.argv[2]
os.makedirs(OUTD, exist_ok=True)
rep_r = json.load(open(os.path.join(D, "gear_stills_report.json")))
STACKS = rep_r["stacks"]
SHOTS = [("idle", 25), ("idle", 205), ("walk", 25), ("walk", 205)]


def cls(p):
    I = np.asarray(Image.open(p).convert('RGB')).astype(int)
    return ((I[..., 0] > 200) & (I[..., 1] > 200) & (I[..., 2] > 200), (I[..., 0] > 200) & (I[..., 1] > 200) & (I[..., 2] < 60),
            (I[..., 0] > 200) & (I[..., 1] < 60) & (I[..., 2] > 200))


def dots(idp, bp, sc):
    # s11_count.py's rule, restated only to LOCATE the dots it counts (its totals are taken from s11 itself, below)
    I = np.asarray(Image.open(idp).convert('RGB')).astype(int); B = np.asarray(Image.open(bp).convert('RGB')).astype(int)
    body = (I[..., 0] > 200) & (I[..., 1] < 60) & (I[..., 2] < 60); garm = (I[..., 2] > 200) & (I[..., 0] < 60) & (I[..., 1] < 60)
    pale = B.min(-1) > 170; MAXC = 6 * sc * sc
    lab, n = ndimage.label(body, np.ones((3, 3))); iso = np.zeros_like(body)
    sizes = ndimage.sum(body, lab, range(1, n + 1)) if n else np.array([])
    for ci in (np.nonzero(sizes <= MAXC)[0] + 1 if n else []):
        cm = lab == ci; ring = ndimage.binary_dilation(cm, np.ones((3, 3))) & ~cm
        if ring.sum() and (garm & ring).sum() / ring.sum() >= 0.75: iso |= cm
    big = np.isin(lab, (np.nonzero(sizes > MAXC)[0] + 1)) if n else np.zeros_like(body)
    iso &= ~ndimage.binary_dilation(big, np.ones((3, 3)), iterations=2 * sc)
    chain, nch = ndimage.label(ndimage.binary_dilation(body & ~big, np.ones((3, 3)), iterations=sc), np.ones((3, 3)))
    if nch:
        csz = ndimage.sum(body & ~big, chain, range(1, nch + 1)); iso &= ~np.isin(chain, np.nonzero(csz > MAXC)[0] + 1)
    return iso & pale, iso


out = dict(what="her gear stacks checked at the play camera (film_rt/gear_stills.gd + scripts/s19_gear_stacks.py)", stacks=[])
# one crop for every sheet: the union of her silhouette over every stack and shot at 2x
box = None
for s in STACKS:
    for c, h in SHOTS:
        I = np.asarray(Image.open(os.path.join(D, "stack%d_%s_h%d_s2_id.png" % (s["index"], c, h))).convert('RGB')).astype(int)
        ys, xs = np.nonzero(I.sum(-1) > 90); b = (xs.min(), ys.min(), xs.max() + 1, ys.max() + 1)
        box = b if box is None else (min(box[0], b[0]), min(box[1], b[1]), max(box[2], b[2]), max(box[3], b[3]))
box = (int(box[0]) - 12, int(box[1]) - 12, int(box[2]) + 12, int(box[3]) + 12); W, H = box[2] - box[0], box[3] - box[1]
for s in STACKS:
    i = s["index"]
    subprocess.run([sys.executable, os.path.join(HERE, "s11_count.py"), D, "stack%d" % i], check=True, capture_output=True)
    cnt = json.load(open(os.path.join(D, "stack%d_counts.json" % i)))
    sp = {}
    for sc in (1, 2):
        rows = {k: v for k, v in cnt["per_still"].items() if k.endswith("s%d" % sc)}
        sp["%dx" % sc] = dict(isolated_pale_dots_px=sum(r["isolated_speckle_px"] for r in rows.values()),
                              isolated_holes_px=sum(r["isolated_hole_px"] for r in rows.values()),
                              opening_edge_pale_px=sum(r["opening_edge_fragments_pale_px"] for r in rows.values()),
                              slit_pale_px=sum(r["slit_fragments_pale_px"] for r in rows.values()))
    # paint classes: over the body, and over what this stack reveals against the full kit (the last stack)
    tot = dict(body_px=0, filled_px=0, bare_px=0, revealed_px=0, revealed_filled_px=0)
    for c, h in SHOTS:
        for sc in (1, 2):
            w, y, m = cls(os.path.join(D, "stack%d_%s_h%d_s%d_class.png" % (i, c, h, sc)))
            w4, y4, m4 = cls(os.path.join(D, "stack%d_%s_h%d_s%d_class.png" % (STACKS[-1]["index"], c, h, sc)))
            vis, vis4 = w | y | m, w4 | y4 | m4; rev = vis & ~vis4
            tot["body_px"] += int(vis.sum()); tot["filled_px"] += int(y.sum()); tot["bare_px"] += int(m.sum())
            tot["revealed_px"] += int(rev.sum()); tot["revealed_filled_px"] += int((y & rev).sum())
    tot["filled_pct"] = round(100.0 * tot["filled_px"] / max(tot["body_px"], 1), 2)
    tot["revealed_filled_pct"] = round(100.0 * tot["revealed_filled_px"] / max(tot["revealed_px"], 1), 2)
    # the 2x sheet, the pale dots circled
    sheet = Image.new('RGB', (W * len(SHOTS), H + 30), (255, 255, 255)); dr = ImageDraw.Draw(sheet)
    where = []
    for k, (c, h) in enumerate(SHOTS):
        bp = os.path.join(D, "stack%d_%s_h%d_s2_beauty.png" % (i, c, h))
        pal, iso = dots(os.path.join(D, "stack%d_%s_h%d_s2_id.png" % (i, c, h)), bp, 2)
        im = Image.open(bp).convert('RGB').crop(box); sheet.paste(im, (k * W, 30))
        lab, n = ndimage.label(pal, np.ones((3, 3)))
        for ci in range(1, n + 1):
            ys, xs = np.nonzero(lab == ci); cx, cy = int(xs.mean()) - box[0] + k * W, int(ys.mean()) - box[1] + 30
            dr.ellipse((cx - 9, cy - 9, cx + 9, cy + 9), outline=(0, 160, 255), width=2)
            where.append(dict(shot="%s h%d" % (c, h), x=int(xs.mean()), y=int(ys.mean()), px=int(len(xs))))
        dr.text((k * W + 6, 16), "%s  heading %d" % (c, h), fill=(0, 0, 0))
    dr.text((6, 2), "stack %d  %s  --  %s" % (i, s["name"], ", ".join(s["pieces"]) or "the base body"), fill=(0, 0, 0))
    sp_ = os.path.join(OUTD, "stack%d_2x.png" % i)
    sheet.save(sp_)
    out["stacks"].append(dict(index=i, name=s["name"], pieces=s["pieces"], armed=s["armed"], grip_R=s["grip_R"], carry_layer=s["carry_layer"],
                              see_through=sp, pale_dots_at_2x=where, paint=tot, sheet=os.path.relpath(sp_, ROOT)))
    print("  stack %d %-18s pale dots 1x %d / 2x %d (holes %d / %d) | body paint: filled %.2f%%, bare %d; revealed %d px, filled %.2f%% -> %s"
          % (i, s["name"], sp["1x"]["isolated_pale_dots_px"], sp["2x"]["isolated_pale_dots_px"], sp["1x"]["isolated_holes_px"],
             sp["2x"]["isolated_holes_px"], tot["filled_pct"], tot["bare_px"], tot["revealed_px"], tot["revealed_filled_pct"], os.path.basename(sp_)))
# one overview: every stack's sheet, stacked, at half size
ims = [Image.open(os.path.join(ROOT, s["sheet"])) for s in out["stacks"]]
ov = Image.new('RGB', (ims[0].width, sum(im.height for im in ims)), (255, 255, 255)); y = 0
for im in ims:
    ov.paste(im, (0, y)); y += im.height
ov.resize((ov.width // 2, ov.height // 2), Image.LANCZOS).save(os.path.join(OUTD, "all_stacks_overview_1x.png"))
out["overview"] = os.path.relpath(os.path.join(OUTD, "all_stacks_overview_1x.png"), ROOT)
out["method"] = dict(camera="the play camera: orthographic, pitch 52.9535 deg, yaw 47 deg, 100.617 px/m at 1x (201.2 at 2x)",
                     shots=[list(x) for x in SHOTS], poses="idle at 1.0 s, walk at 0.5 s; the carry layer only where the stack is armed",
                     see_through="scripts/s11_count.py per stack, unchanged", paint="the class pass against 06b_bake's painted mask",
                     reference="pass 2's shipped costume (full kit, 5 clips x 4 headings at 1.0 s): isolated pale 1 px at 1x, 7 at 2x (manifest speckles)")
json.dump(out, open(os.path.join(ROOT, "work", "s19_gear_stacks.json"), "w"), indent=1)
print("wrote work/s19_gear_stacks.json")
