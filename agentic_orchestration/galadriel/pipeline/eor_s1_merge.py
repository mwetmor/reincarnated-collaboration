#!/usr/bin/env python3
"""Sitting-1 badge plateau build + adjacent-plateau merge + read montages.

Over-segmentation source: the badge glyph has a slow glow pulse and transient
occlusion (floating combat text, screen flashes) that breaks a constant-value
run into several plateaus. Merging temporally adjacent plateaus whose MEDOID
signatures agree recovers the true value runs without bridging real transitions.
"""
import sys, os, glob, json
import numpy as np
from PIL import Image, ImageDraw

X0, X1, Y0, Y1 = 36, 77, 8, 39
MIN_E = 300.0


def red(path):
    im = np.array(Image.open(path).convert("RGB")).astype(np.int16)
    s = im[Y0:Y1, X0:X1]
    return np.clip(s[:, :, 0] - np.maximum(s[:, :, 1], s[:, :, 2]), 0, 255).astype(np.float32)


def sg(v):
    w = v.copy(); w[w < 12] = 0; w = np.power(w, 0.5)
    n = np.linalg.norm(w)
    return (w / n) if n > 0 else w


def medoid(members, sig):
    if len(members) == 1: return members[0]
    M = np.stack([sig[t].ravel() for t in members])
    return int(members[int(np.argmax((M @ M.T).sum(axis=1)))])


def build(indir, split=0.045, merge=0.09):
    files = {int(os.path.basename(f).split(".")[0]): f
             for f in glob.glob(os.path.join(indir, "*.png"))}
    ts = sorted(files)
    sig, en = {}, {}
    for t in ts:
        v = red(files[t]); en[t] = float(v.sum()); sig[t] = sg(v)
    tmin, tmax = ts[0], ts[-1]
    missing = [t for t in range(tmin, tmax + 1) if t not in sig]

    ps, cur = [], None
    for t in range(tmin, tmax + 1):
        ok = t in sig and en[t] >= MIN_E
        if not ok:
            if cur: ps.append(cur); cur = None
            continue
        if cur is None:
            cur = [t]; continue
        d = min(1 - float((sig[cur[-1]] * sig[t]).sum()),
                1 - float((sig[cur[0]] * sig[t]).sum()))
        if d <= split:
            cur.append(t)
        else:
            ps.append(cur); cur = [t]
    if cur: ps.append(cur)

    # merge pass: repeat until stable
    changed = True
    while changed:
        changed = False
        out = [ps[0]]
        for p in ps[1:]:
            a, b = medoid(out[-1], sig), medoid(p, sig)
            gap = p[0] - out[-1][-1]
            d = 1 - float((sig[a] * sig[b]).sum())
            if d <= merge and gap <= 6:
                out[-1] = out[-1] + p; changed = True
            else:
                out.append(p)
        ps = out
    recs = [{"t0": p[0], "t1": p[-1], "n": len(p), "medoid": medoid(p, sig)} for p in ps]
    return recs, missing


def montages(indir, recs, prefix, cols=4, per=16, scale=4):
    med = [r["medoid"] for r in recs]
    outs = []
    for k in range(0, len(med), per):
        chunk = med[k:k + per]
        rows = (len(chunk) + cols - 1) // cols
        W, H = 54 * scale, 44 * scale + 14
        S = Image.new("RGB", (cols * W, rows * H), (15, 15, 15))
        d = ImageDraw.Draw(S)
        for i, t in enumerate(chunk):
            f = os.path.join(indir, f"{t:05d}.png")
            im = Image.open(f).convert("RGB").crop((30, 2, 84, 46)).resize((W, 44 * scale), Image.LANCZOS)
            r, c = divmod(i, cols)
            S.paste(im, (c * W, r * H + 14))
            d.text((c * W + 3, r * H + 2), f"{t}", fill=(120, 255, 120))
        p = f"{prefix}-{k//per:02d}.png"
        S.save(p); outs.append(p)
    return outs


if __name__ == "__main__":
    indir, prefix = sys.argv[1], sys.argv[2]
    recs, missing = build(indir,
                          float(sys.argv[3]) if len(sys.argv) > 3 else 0.045,
                          float(sys.argv[4]) if len(sys.argv) > 4 else 0.09)
    json.dump({"plateaus": recs, "missing": missing}, open(prefix + "-merged.json", "w"), indent=1)
    print(f"plateaus={len(recs)} missing_frames={len(missing)}")
    for r in recs:
        print(f"  [{r['t0']:5d}..{r['t1']:5d}] n={r['n']:4d} med={r['medoid']}")
    outs = montages(indir, recs, prefix + "-read")
    print("montages:", outs)
