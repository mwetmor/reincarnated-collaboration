#!/usr/bin/env python3
"""Frame-accurate refinement of Crucible wave-badge transitions.

For each 1-Hz candidate transition second, extract a 60 fps window of the badge
ROI and locate the first frame whose badge signature matches the POST state
rather than the PRE state. Reports the transition time in video-clock seconds
with 1/60 s resolution.

usage: eor_refine.py <video> <outdir> <t1,t2,t3,...> [pre_pad] [post_pad]
"""
import sys, os, subprocess, glob, json
import numpy as np
from PIL import Image

X0, X1, Y0, Y1 = 36, 77, 8, 39
CROP = "crop=140:50:1550:125"


def red(path):
    im = np.array(Image.open(path).convert("RGB")).astype(np.int16)
    s = im[Y0:Y1, X0:X1]
    v = s[:, :, 0] - np.maximum(s[:, :, 1], s[:, :, 2])
    return np.clip(v, 0, 255).astype(np.float32)


def sg(v):
    w = v.copy(); w[w < 12] = 0; w = np.power(w, 0.5)
    n = np.linalg.norm(w)
    return (w / n) if n > 0 else w


def extract(video, t0, dur, outdir):
    os.makedirs(outdir, exist_ok=True)
    for f in glob.glob(os.path.join(outdir, "*.png")):
        os.remove(f)
    subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t0:.3f}", "-i", video,
                    "-t", f"{dur:.3f}", "-vf", CROP, "-vsync", "0",
                    os.path.join(outdir, "%05d.png"), "-y"], check=True)
    return sorted(glob.glob(os.path.join(outdir, "*.png")))


def refine(video, tc, workdir, pre=3.0, post=3.0, fps=60.0):
    t0 = tc - pre
    files = extract(video, t0, pre + post, os.path.join(workdir, "tmp"))
    sigs, ens = [], []
    for f in files:
        v = red(f); ens.append(float(v.sum())); sigs.append(sg(v))
    n = len(files)
    # PRE reference = median-ish of first 20% ; POST = last 20%
    a = [i for i in range(0, max(1, n // 5)) if ens[i] > 300]
    b = [i for i in range(n - max(1, n // 5), n) if ens[i] > 300]
    if not a or not b:
        return None
    ref_a = np.mean([sigs[i] for i in a], axis=0); ref_a /= np.linalg.norm(ref_a)
    ref_b = np.mean([sigs[i] for i in b], axis=0); ref_b /= np.linalg.norm(ref_b)
    sep = 1.0 - float((ref_a * ref_b).sum())
    scores = []
    for i in range(n):
        if ens[i] < 300:
            scores.append(None); continue
        da = 1.0 - float((ref_a * sigs[i]).sum())
        db = 1.0 - float((ref_b * sigs[i]).sum())
        scores.append(db - da)      # <0 => looks like POST, >0 => looks like PRE
    # first index from which the signal stays POST-like for >=15 valid frames
    k = None
    valid = [i for i, s in enumerate(scores) if s is not None]
    for i in valid:
        if scores[i] >= 0: continue
        fwd = [j for j in valid if j >= i][:20]
        if len(fwd) >= 10 and all(scores[j] < 0 for j in fwd):
            k = i; break
    if k is None:
        return {"t_candidate": tc, "sep": sep, "t_change": None, "n": n}
    return {"t_candidate": tc, "sep": sep, "t_change": round(t0 + k / fps, 3),
            "frame_idx": k, "n": n,
            "amb_frames": sum(1 for s in scores if s is not None and abs(s) < 0.02)}


if __name__ == "__main__":
    video, workdir = sys.argv[1], sys.argv[2]
    cands = [float(x) for x in sys.argv[3].split(",")]
    pre = float(sys.argv[4]) if len(sys.argv) > 4 else 3.0
    post = float(sys.argv[5]) if len(sys.argv) > 5 else 3.0
    os.makedirs(workdir, exist_ok=True)
    out = []
    for tc in cands:
        r = refine(video, tc, workdir, pre, post)
        out.append(r)
        print(r, flush=True)
    json.dump(out, open(os.path.join(workdir, "refined.json"), "w"), indent=1)
