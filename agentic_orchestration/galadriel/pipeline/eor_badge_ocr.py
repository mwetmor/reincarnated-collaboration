#!/usr/bin/env python3
"""EoR Crucible wave-badge OCR + plateau timeline.

Pipeline
  1. redness map of the badge-ring interior (gamma-compressed, L2-normalised)
  2. frame-to-frame NCC distance -> candidate change points
  3. per-plateau medoid frame -> column-segment into digit glyphs
  4. glyph clustering -> tiny alphabet; clusters labelled by an external
     labels.json (written by a human/multimodal read of one exemplar each)
  5. OCR every plateau; emit wave timeline

Sub-commands:
  glyphs <framedir> <out_prefix>          extract + cluster glyphs, dump exemplars
  read   <framedir> <out_prefix> <labels> OCR using labelled clusters
"""
import sys, os, glob, json
import numpy as np
from PIL import Image, ImageDraw

X0, X1, Y0, Y1 = 36, 77, 8, 39
GAMMA, FLOOR = 0.5, 12
MIN_ENERGY = 300.0


def red(path):
    im = np.array(Image.open(path).convert("RGB")).astype(np.int16)
    s = im[Y0:Y1, X0:X1]
    v = s[:, :, 0] - np.maximum(s[:, :, 1], s[:, :, 2])
    return np.clip(v, 0, 255).astype(np.float32)


def sig(v):
    w = v.copy(); w[w < FLOOR] = 0
    w = np.power(w, GAMMA)
    n = np.linalg.norm(w)
    return (w / n) if n > 0 else w


def load_all(framedir):
    files = sorted(glob.glob(os.path.join(framedir, "*.png")))
    ts, sigs, en = [], [], []
    for f in files:
        t = int(os.path.basename(f).split(".")[0])
        v = red(f)
        ts.append(t); en.append(float(v.sum())); sigs.append(sig(v))
    return files, np.array(ts), sigs, np.array(en)


def plateaus(ts, sigs, en, thresh=0.035):
    """Return list of dicts: kind badge|nobadge, t0,t1, member indices."""
    out, cur = [], None
    for i in range(len(ts)):
        has = en[i] >= MIN_ENERGY
        if not has:
            if cur: out.append(cur); cur = None
            if out and out[-1]["kind"] == "nobadge" and out[-1]["i1"] == i - 1:
                out[-1]["t1"] = ts[i]; out[-1]["i1"] = i
            else:
                out.append({"kind": "nobadge", "t0": int(ts[i]), "t1": int(ts[i]),
                            "i0": i, "i1": i})
            continue
        if cur is None:
            cur = {"kind": "badge", "t0": int(ts[i]), "t1": int(ts[i]), "i0": i, "i1": i,
                   "idx": [i]}
            continue
        d = 1.0 - float((sigs[cur["idx"][-1]] * sigs[i]).sum())
        d2 = 1.0 - float((sigs[cur["idx"][0]] * sigs[i]).sum())
        if min(d, d2) <= thresh:
            cur["t1"] = int(ts[i]); cur["i1"] = i; cur["idx"].append(i)
        else:
            out.append(cur)
            cur = {"kind": "badge", "t0": int(ts[i]), "t1": int(ts[i]), "i0": i, "i1": i,
                   "idx": [i]}
    if cur: out.append(cur)
    return out


def medoid(p, sigs):
    idx = p["idx"]
    if len(idx) == 1: return idx[0]
    M = np.stack([sigs[i].ravel() for i in idx])
    G = M @ M.T
    return idx[int(np.argmax(G.sum(axis=1)))]


def segment_glyphs(v):
    """Column-segment the redness map into digit glyph bitmaps."""
    prof = v.sum(axis=0)
    on = prof > 18
    runs, s = [], None
    for x, o in enumerate(on):
        if o and s is None: s = x
        if not o and s is not None:
            runs.append((s, x - 1)); s = None
    if s is not None: runs.append((s, len(on) - 1))
    runs = [r for r in runs if r[1] - r[0] >= 2]
    # merge runs separated by a single dead column only if a piece is too thin
    glyphs = []
    for (a, b) in runs:
        sub = v[:, a:b + 1]
        rows = np.nonzero(sub.sum(axis=1) > 12)[0]
        if len(rows) < 6: continue
        y0, y1 = int(rows.min()), int(rows.max())
        g = sub[y0:y1 + 1]
        glyphs.append({"x0": a, "x1": b, "y0": y0, "y1": y1, "bmp": g})
    return glyphs


def glyph_canvas(g, H=18, W=14):
    c = np.zeros((H, W), dtype=np.float32)
    b = g["bmp"]
    h, w = b.shape
    h, w = min(h, H), min(w, W)
    c[:h, :w] = b[:h, :w]
    n = np.linalg.norm(c)
    return c / n if n > 0 else c


def cmd_glyphs(framedir, prefix):
    files, ts, sigs, en = load_all(framedir)
    ps = plateaus(ts, sigs, en)
    bad = [p for p in ps if p["kind"] == "badge"]
    print(f"frames={len(ts)} plateaus={len(ps)} badge-plateaus={len(bad)}")
    clusters = []
    recs = []
    for p in bad:
        mi = medoid(p, sigs)
        v = red(files[mi])
        gs = segment_glyphs(v)
        labels = []
        for gi, g in enumerate(gs):
            c = glyph_canvas(g)
            best, bd = -1, 9e9
            for k, cl in enumerate(clusters):
                d = 1.0 - float((c * cl["c"]).sum())
                if d < bd: bd, best = d, k
            if best >= 0 and bd <= 0.045:
                clusters[best]["n"] += 1
            else:
                clusters.append({"c": c, "n": 1, "ex_t": int(ts[mi]), "ex_i": gi,
                                 "w": g["x1"] - g["x0"] + 1, "h": g["y1"] - g["y0"] + 1})
                best = len(clusters) - 1
            labels.append(best)
        recs.append({"t0": p["t0"], "t1": p["t1"], "medoid_t": int(ts[mi]),
                     "glyph_clusters": labels, "nglyph": len(gs)})
    os.makedirs(prefix + "-glyphex", exist_ok=True)
    for k, cl in enumerate(clusters):
        img = cl["c"] / (cl["c"].max() or 1)
        im = Image.fromarray((255 - img * 255).astype(np.uint8)).resize((14 * 14, 18 * 14), Image.NEAREST)
        im.save(f"{prefix}-glyphex/g{k:02d}_n{cl['n']}_w{cl['w']}h{cl['h']}.png")
    json.dump({"plateaus": recs,
               "clusters": [{"k": k, "n": c["n"], "w": c["w"], "h": c["h"],
                             "ex_t": c["ex_t"], "ex_i": c["ex_i"]} for k, c in enumerate(clusters)]},
              open(prefix + "-glyphs.json", "w"), indent=1)
    print(f"glyph clusters={len(clusters)}")
    for k, c in enumerate(clusters):
        print(f"  g{k:02d} n={c['n']:4d} w={c['w']} h={c['h']} ex_t={c['ex_t']} pos={c['ex_i']}")


def cmd_read(framedir, prefix, labelfile):
    lab = json.load(open(labelfile))          # {"0": "1", "1": "5", ...}
    G = json.load(open(prefix + "-glyphs.json"))
    rows = []
    for p in G["plateaus"]:
        digs = [lab.get(str(k), "?") for k in p["glyph_clusters"]]
        s = "".join(digs)
        rows.append({"t0": p["t0"], "t1": p["t1"], "medoid_t": p["medoid_t"],
                     "raw": s, "wave": int(s) if s.isdigit() else None})
    json.dump(rows, open(prefix + "-waves.json", "w"), indent=1)
    for r in rows:
        print(f"[{r['t0']:5d}..{r['t1']:5d}] {r['raw']:>5s}")


if __name__ == "__main__":
    if sys.argv[1] == "glyphs":
        cmd_glyphs(sys.argv[2], sys.argv[3])
    else:
        cmd_read(sys.argv[2], sys.argv[3], sys.argv[4])
