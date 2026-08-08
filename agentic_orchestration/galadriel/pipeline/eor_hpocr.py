#!/usr/bin/env python3
"""Read Grim Dawn in-world monster HP readouts `(current/max)` from located blobs.

Companion to eor_hptext.py, which LOCATES the strings. This module CLUSTERS them so
that a human eye only has to verify one representative per distinct value instead of
one per frame. It is a deduper, not an oracle: every value that reaches the note is
re-read by eye from a magnified crop of its own frame.

Font behaviour that makes this tractable: the readout is drawn at a uniform ~9.5 px
character pitch with a full blank column between glyphs, so column-gap segmentation
returns exactly one run per character (verified 21/21 on two independent strings).

  build <frame.png> <spec.json> <atlas.npz>   spec: {"x0,y0,x1,y1": "(3,722,896/3,722,896)"}
  read  <index.json> <video> <atlas.npz> <out.json>
"""
import sys, os, json, subprocess
import numpy as np
from PIL import Image

W, H = 1920, 1080
MIN_CH = 135
CH_H, CH_W = 16, 12          # atlas canvas


def white(fr):
    """Achromatic-brightness field: high for white text, low for saturated VFX."""
    return np.clip(fr.astype(np.int16).min(axis=2) - MIN_CH, 0, 255).astype(np.float32)


def segment(v):
    """v: whiteness patch for one string. Returns list of (c0, c1) char columns."""
    cols = (v > 0).sum(axis=0)
    runs, inr, s = [], False, 0
    for i, c in enumerate(cols):
        if c > 0 and not inr:
            s, inr = i, True
        elif c == 0 and inr:
            runs.append((s, i - 1)); inr = False
    if inr:
        runs.append((s, len(cols) - 1))
    return [r for r in runs if r[1] - r[0] >= 0]


def patch(v, c0, c1):
    g = v[:, c0:c1 + 1]
    rows = np.nonzero(g.sum(axis=1) > 0)[0]
    if len(rows) == 0:
        return None
    g = g[rows.min():rows.max() + 1]
    canvas = np.zeros((CH_H, CH_W), dtype=np.float32)
    h, w = min(g.shape[0], CH_H), min(g.shape[1], CH_W)
    # top-align on the glyph's own ink, but keep the row offset as a feature by
    # storing it separately (commas/periods sit low, digits sit high)
    canvas[:h, :w] = g[:h, :w]
    return canvas, int(rows.min())


def norm(a):
    n = np.linalg.norm(a)
    return a / n if n > 0 else a


def build(framepath, specpath, outpath):
    fr = np.array(Image.open(framepath).convert("RGB"))
    v_all = white(fr)
    spec = json.load(open(specpath))
    bank = {}
    for box, truth in spec.items():
        x0, y0, x1, y1 = [int(q) for q in box.split(",")]
        v = v_all[y0:y1 + 1, x0:x1 + 1]
        segs = segment(v)
        if len(segs) != len(truth):
            print(f"  SKIP {box}: {len(segs)} runs vs {len(truth)} chars -> {truth}")
            continue
        for ch, (c0, c1) in zip(truth, segs):
            r = patch(v, c0, c1)
            if r:
                bank.setdefault(ch, []).append((r[0], r[1]))
        print(f"  ok  {box}  {len(segs)} chars  {truth}")
    atlas = {}
    for ch, lst in bank.items():
        atlas[ch] = {"bmp": np.median(np.stack([g for g, _ in lst]), axis=0),
                     "top": float(np.median([t for _, t in lst])),
                     "n": len(lst)}
    np.savez(outpath,
             **{f"bmp_{ord(k)}": v["bmp"] for k, v in atlas.items()},
             **{f"top_{ord(k)}": np.array([v["top"]]) for k, v in atlas.items()})
    print("alphabet:", "".join(sorted(atlas)),
          {k: atlas[k]["n"] for k in sorted(atlas)})


def load(path):
    z = np.load(path)
    ks = [int(k[4:]) for k in z.files if k.startswith("bmp_")]
    return {chr(k): {"bmp": norm(z[f"bmp_{k}"]), "top": float(z[f"top_{k}"][0])} for k in ks}


def classify(atlas, canvas, top):
    q = norm(canvas)
    best, bs, second = None, -9e9, -9e9
    for ch, a in atlas.items():
        s = float((q * a["bmp"]).sum()) - 0.06 * abs(top - a["top"])
        if s > bs:
            second, bs, best = bs, s, ch
        elif s > second:
            second = s
    return best, bs, bs - second


def read_string(atlas, v):
    segs = segment(v)
    chars, scores, margins = [], [], []
    for c0, c1 in segs:
        r = patch(v, c0, c1)
        if r is None:
            chars.append("?"); scores.append(0.0); margins.append(0.0); continue
        ch, s, m = classify(atlas, r[0], r[1])
        chars.append(ch); scores.append(s); margins.append(m)
    return "".join(chars), (min(scores) if scores else 0.0), (min(margins) if margins else 0.0)


def parse(s):
    """`(cur/max)` -> (cur, max) ints, or None."""
    if not (s.startswith("(") and s.endswith(")") and s.count("/") == 1):
        return None
    body = s[1:-1]
    a, b = body.split("/")
    try:
        ai = int(a.replace(",", "")); bi = int(b.replace(",", ""))
    except ValueError:
        return None
    # comma-grouping sanity: thousands separators every 3 from the right
    for part in (a, b):
        segsx = part.split(",")
        if len(segsx) > 1:
            if not (1 <= len(segsx[0]) <= 3) or any(len(x) != 3 for x in segsx[1:]):
                return None
    if bi <= 0 or ai < 0 or ai > bi * 1.02:
        return None
    return ai, bi


def read_index(indexpath, video, atlaspath, outpath):
    atlas = load(atlaspath)
    idx = json.load(open(indexpath))
    fps = idx["fps"]; t0 = idx["t0"]; t1 = idx["t1"]
    byframe = {}
    for b in idx["blobs"]:
        byframe.setdefault(round(b["t"], 4), []).append(b)
    cmd = ["ffmpeg", "-v", "error", "-ss", f"{t0}", "-t", f"{t1-t0}", "-i", video,
           "-vf", f"fps={fps}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=W * H * 3)
    nb = W * H * 3
    out, i = [], 0
    while True:
        buf = p.stdout.read(nb)
        if len(buf) < nb:
            break
        t = round(t0 + i / fps, 4)
        bl = byframe.get(t, [])
        if bl:
            fr = np.frombuffer(buf, dtype=np.uint8).reshape(H, W, 3)
            v_all = white(fr)
            for b in bl:
                x0, y0, x1, y1 = b["box"]
                s, sc, mg = read_string(atlas, v_all[y0:y1 + 1, x0:x1 + 1])
                pr = parse(s)
                out.append({"t": t, "box": b["box"], "raw": s,
                            "cur": pr[0] if pr else None, "max": pr[1] if pr else None,
                            "score": round(sc, 3), "margin": round(mg, 3)})
        i += 1
    p.stdout.close(); p.wait()
    json.dump(out, open(outpath, "w"), indent=1)
    good = [r for r in out if r["max"]]
    print(f"blobs={len(out)} parsed={len(good)} ({100*len(good)/max(1,len(out)):.0f}%)")


if __name__ == "__main__":
    if sys.argv[1] == "build":
        build(sys.argv[2], sys.argv[3], sys.argv[4])
    else:
        read_index(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
