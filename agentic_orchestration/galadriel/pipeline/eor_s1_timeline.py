#!/usr/bin/env python3
"""Sitting-1 wave-badge timeline: change-point detection over 1 Hz badge crops.

Emits candidate transition seconds (1 Hz resolution) plus per-plateau medoid
frames for anchor reading. Gap-aware: missing 1 Hz frames are marked and never
silently bridged.
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


def main(indir, out_prefix, thresh=0.045):
    files = {int(os.path.basename(f).split(".")[0]): f
             for f in glob.glob(os.path.join(indir, "*.png"))}
    ts = sorted(files)
    sig, en = {}, {}
    for t in ts:
        v = red(files[t]); en[t] = float(v.sum()); sig[t] = sg(v)

    tmin, tmax = ts[0], ts[-1]
    missing = [t for t in range(tmin, tmax + 1) if t not in sig]

    # plateau build over badge-present frames, gap-aware
    plateaus, cur = [], None
    for t in range(tmin, tmax + 1):
        if t not in sig or en[t] < MIN_E:
            if cur: plateaus.append(cur); cur = None
            continue
        if cur is None:
            cur = {"t0": t, "t1": t, "members": [t]}
            continue
        if t != cur["t1"] + 1:                    # frame gap -> break plateau
            plateaus.append(cur); cur = {"t0": t, "t1": t, "members": [t]}
            continue
        d1 = 1.0 - float((sig[cur["members"][-1]] * sig[t]).sum())
        d0 = 1.0 - float((sig[cur["members"][0]] * sig[t]).sum())
        if min(d0, d1) <= thresh:
            cur["t1"] = t; cur["members"].append(t)
        else:
            plateaus.append(cur); cur = {"t0": t, "t1": t, "members": [t]}
    if cur: plateaus.append(cur)

    # medoid per plateau
    for p in plateaus:
        m = p["members"]
        if len(m) == 1:
            p["medoid"] = m[0]
        else:
            M = np.stack([sig[t].ravel() for t in m])
            p["medoid"] = int(m[int(np.argmax((M @ M.T).sum(axis=1)))])

    json.dump({"plateaus": [{k: v for k, v in p.items() if k != "members"} | {"n": len(p["members"])}
                            for p in plateaus],
               "missing_frames": missing},
              open(out_prefix + "-plateaus.json", "w"), indent=1)
    print(f"frames={len(ts)} missing={len(missing)} plateaus={len(plateaus)}")
    for p in plateaus:
        print(f"  [{p['t0']:5d}..{p['t1']:5d}] n={len(p['members']):4d} medoid={p['medoid']}")


def montage(indir, prefix, times, cols=6, scale=4):
    W, H = 54 * scale, 44 * scale + 13
    rows = (len(times) + cols - 1) // cols
    S = Image.new("RGB", (cols * W, rows * H), (15, 15, 15))
    d = ImageDraw.Draw(S)
    for i, t in enumerate(times):
        f = os.path.join(indir, f"{t:05d}.png")
        if not os.path.exists(f): continue
        im = Image.open(f).convert("RGB").crop((30, 2, 84, 46)).resize((W, 44 * scale), Image.LANCZOS)
        r, c = divmod(i, cols)
        S.paste(im, (c * W, r * H + 13))
        d.text((c * W + 3, r * H + 1), f"{t}", fill=(120, 255, 120))
    S.save(prefix)
    return S.size


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], float(sys.argv[3]) if len(sys.argv) > 3 else 0.045)
