#!/usr/bin/env python3
"""Group located HP-readout blobs into per-body tracks and render eye-read sheets.

Rationale: a single monster's readout is re-detected on every frame it is engaged,
so a 10 Hz scan of a 26 s window yields ~1,100 blobs for a board of a handful of
bodies. Reading 1,100 crops by eye is not a census, it is a lottery. Grouping them
into spatiotemporal tracks first reduces the eye-read set to one representative per
body-appearance, which IS readable exhaustively -- so the census can be closed rather
than sampled.

Each rendered tile carries the readout text AND the health bar beneath it, because
the bar's frame furniture (double skull = nemesis/boss, single skull, plain) and its
colour (red = hostile, green = player-side summon) are the class discriminators.

  track  <index.json> <ocr.json> <out.json>
  sheets <track.json> <video> <outdir> [tiles_per_sheet]
"""
import sys, os, json, subprocess, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H = 1920, 1080
FONT = "/System/Library/Fonts/Supplemental/Andale Mono.ttf"

# vertical span below the text baseline that contains the health bar
BAR_BELOW = 18
PAD_X, PAD_TOP = 6, 5


def cen(b):
    x0, y0, x1, y1 = b
    return (0.5 * (x0 + x1), 0.5 * (y0 + y1))


def track(indexpath, ocrpath, outpath, dt_tol=0.25, d_tol=55.0, w_tol=28):
    idx = json.load(open(indexpath))
    ocr = {(round(r["t"], 4), tuple(r["box"])): r for r in json.load(open(ocrpath))}
    blobs = sorted(idx["blobs"], key=lambda b: (b["t"], b["box"][0]))
    tracks = []
    for b in blobs:
        c = cen(b["box"]); w = b["w"]
        best, bd = None, 9e9
        for tr in tracks:
            last = tr["items"][-1]
            if b["t"] - last["t"] > dt_tol or b["t"] <= last["t"] - 1e-6:
                continue
            lc = cen(last["box"])
            d = math.hypot(c[0] - lc[0], c[1] - lc[1])
            if d <= d_tol and abs(w - last["w"]) <= w_tol and d < bd:
                bd, best = d, tr
        r = ocr.get((round(b["t"], 4), tuple(b["box"])), {})
        item = {"t": b["t"], "box": b["box"], "w": b["w"],
                "raw": r.get("raw"), "cur": r.get("cur"), "max": r.get("max")}
        if best is None:
            tracks.append({"items": [item]})
        else:
            best["items"].append(item)
    out = []
    for i, tr in enumerate(tracks):
        it = tr["items"]
        maxes = [x["max"] for x in it if x["max"]]
        vals = {}
        for m in maxes:
            vals[m] = vals.get(m, 0) + 1
        mode = max(vals.items(), key=lambda kv: kv[1])[0] if vals else None
        # representative = the frame whose OCR agrees with the track mode and whose
        # blob is widest (most ink, least occlusion)
        cand = [x for x in it if x["max"] == mode] or it
        rep = max(cand, key=lambda x: x["w"])
        out.append({"id": i, "n": len(it), "t0": it[0]["t"], "t1": it[-1]["t"],
                    "mode_max": mode, "n_parsed": len(maxes),
                    "vals": vals, "rep": rep})
    out.sort(key=lambda r: r["t0"])
    for i, r in enumerate(out):
        r["id"] = i
    json.dump(out, open(outpath, "w"), indent=1)
    print(f"blobs={len(blobs)} tracks={len(out)}")
    for r in out:
        print(f"  #{r['id']:>3} t {r['t0']:.1f}-{r['t1']:.1f} n={r['n']:>3} "
              f"max={r['mode_max']} vals={r['vals']}")


def sheets(trackpath, video, outdir, per=8):
    os.makedirs(outdir, exist_ok=True)
    trs = json.load(open(trackpath))
    # one exact-seek frame grab per representative
    tiles = []
    try:
        font = ImageFont.truetype(FONT, 22)
    except Exception:
        font = ImageFont.load_default()
    for r in trs:
        t = r["rep"]["t"]; x0, y0, x1, y1 = r["rep"]["box"]
        tmp = os.path.join(outdir, f"_f{r['id']:03d}.png")
        subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t}", "-i", video,
                        "-frames:v", "1", "-y", tmp], check=True)
        im = Image.open(tmp).convert("RGB")
        cx0 = max(0, x0 - PAD_X); cy0 = max(0, y0 - PAD_TOP)
        cx1 = min(W, x1 + PAD_X + 1); cy1 = min(H, y1 + BAR_BELOW + 1)
        c = im.crop((cx0, cy0, cx1, cy1))
        c = c.resize((c.width * 4, c.height * 4), Image.LANCZOS)
        lab = Image.new("RGB", (c.width, c.height + 28), (0, 0, 0))
        lab.paste(c, (0, 28))
        d = ImageDraw.Draw(lab)
        d.text((4, 3), f"#{r['id']} t={t:.2f} n={r['n']} @({x0},{y0})",
               fill=(255, 235, 120), font=font)
        tiles.append(lab)
        os.remove(tmp)
    for s in range(0, len(tiles), per):
        grp = tiles[s:s + per]
        Wm = max(t.width for t in grp); Ht = sum(t.height + 8 for t in grp)
        sh = Image.new("RGB", (Wm, Ht), (18, 18, 18)); y = 0
        for t in grp:
            sh.paste(t, (0, y)); y += t.height + 8
        p = os.path.join(outdir, f"sheet-{s//per:02d}.png")
        sh.save(p); print("wrote", p, sh.size)


if __name__ == "__main__":
    if sys.argv[1] == "track":
        track(sys.argv[2], sys.argv[3], sys.argv[4])
    else:
        sheets(sys.argv[2], sys.argv[3], sys.argv[4],
               int(sys.argv[5]) if len(sys.argv) > 5 else 8)
