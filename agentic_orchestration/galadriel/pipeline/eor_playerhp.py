#!/usr/bin/env python3
"""Read the Grim Dawn HUD player-health numerals `cur/max` at frame rate.

Instrument for threat-grammar extraction: the player's own health readout is the
only damage-application clock in the substrate that is exact. Every downward step
of `cur` is an incoming hit (or the frame-sum of simultaneous hits); every upward
step is regeneration / leech / potion. Positions are FIXED in the HUD, so the box
never has to be located per frame -- unlike the in-world readouts.

The glyph atlas is built by segmenting hand-read frames; every value the note
quotes is re-checked by eye against a magnified crop of its own frame.

  atlas  <video> <spec.json> <atlas.npz>   spec: [{"t":690.0,"s":"19670/20005"}, ...]
  trace  <video> <t0> <t1> <atlas.npz> <out.json>

Box (1920x1080 GD HUD, 100% UI scale): x 572..702, y 1004..1028.
"""
import sys, os, json, subprocess
import numpy as np
from PIL import Image

BOX = (572, 1004, 118, 24)      # x, y, w, h  (118 clips a 1px HUD specular at x=694)
THRESH = 140                    # min-channel; calibrated -- see note 2026-08-08 threat-grammar A.1
CH_H, CH_W = 18, 12             # atlas canvas
FPS = 60.0


def mask_of(rgb):
    """Achromatic-bright field. HUD numerals are cream/white; the orb is saturated red."""
    a = rgb.astype(np.int16)
    return (a.min(axis=2) > THRESH)


def segment(m):
    """Column-gap segmentation -> list of (c0, c1) inclusive glyph column runs."""
    col = m.any(axis=0)
    runs, i, n = [], 0, len(col)
    while i < n:
        if col[i]:
            j = i
            while j + 1 < n and col[j + 1]:
                j += 1
            if j - i + 1 >= 2:          # kill 1px specular noise
                runs.append((i, j))
            i = j + 1
        else:
            i += 1
    return runs


def norm(m, c0, c1):
    """Crop a glyph run, tight-trim rows, paste centred into a CH_H x CH_W canvas."""
    g = m[:, c0:c1 + 1]
    rs = np.where(g.any(axis=1))[0]
    if len(rs) == 0:
        return None
    g = g[rs.min():rs.max() + 1, :]
    canvas = np.zeros((CH_H, CH_W), bool)
    h, w = g.shape
    if h > CH_H or w > CH_W:
        g = np.array(Image.fromarray(g).resize((min(w, CH_W), min(h, CH_H))))
        h, w = g.shape
    r0 = (CH_H - h) // 2
    c0p = (CH_W - w) // 2
    canvas[r0:r0 + h, c0p:c0p + w] = g
    return canvas


def grab(video, t):
    tmp = f"/tmp/_php_{os.getpid()}.png"
    subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.6f}", "-i", video,
                    "-frames:v", "1", "-vf",
                    f"crop={BOX[2]}:{BOX[3]}:{BOX[0]}:{BOX[1]}", "-y", tmp], check=True)
    a = np.array(Image.open(tmp).convert("RGB"))
    os.remove(tmp)
    return a


def build_atlas(video, spec, out):
    protos = {}
    for job in spec:
        m = mask_of(grab(video, job["t"]))
        runs = segment(m)
        s = job["s"]
        if len(runs) != len(s):
            print(f"  SKIP t={job['t']}: {len(runs)} runs vs {len(s)} chars", file=sys.stderr)
            continue
        for (c0, c1), ch in zip(runs, s):
            g = norm(m, c0, c1)
            if g is None:
                continue
            protos.setdefault(ch, []).append(g)
    keys = sorted(protos)
    arr = np.stack([np.mean(np.stack(protos[k]).astype(np.float32), axis=0) for k in keys])
    np.savez(out, keys=np.array(keys), protos=arr,
             counts=np.array([len(protos[k]) for k in keys]))
    print("atlas:", {k: len(protos[k]) for k in keys})


def classify(g, keys, protos):
    d = ((protos - g.astype(np.float32)[None]) ** 2).sum(axis=(1, 2))
    i = int(np.argmin(d))
    srt = np.sort(d)
    marg = float(srt[1] - srt[0]) if len(srt) > 1 else 1e9
    return keys[i], float(srt[0]), marg


def read_mask(m, keys, protos):
    runs = segment(m)
    if not runs:
        return None, 0.0
    out, worst = [], 1e9
    for c0, c1 in runs:
        g = norm(m, c0, c1)
        if g is None:
            return None, 0.0
        ch, d, marg = classify(g, keys, protos)
        out.append(ch)
        worst = min(worst, marg)
    return "".join(out), worst


def trace(video, t0, t1, atlas, out):
    z = np.load(atlas, allow_pickle=True)
    keys = list(z["keys"]); protos = z["protos"]
    n = int(round((t1 - t0) * FPS))
    w, h = BOX[2], BOX[3]
    cmd = ["ffmpeg", "-v", "error", "-ss", f"{t0:.6f}", "-i", video,
           "-frames:v", str(n), "-vf", f"crop={w}:{h}:{BOX[0]}:{BOX[1]}",
           "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=10 ** 8)
    rows = []
    fsz = w * h * 3
    k = 0
    while True:
        buf = p.stdout.read(fsz)
        if len(buf) < fsz:
            break
        fr = np.frombuffer(buf, np.uint8).reshape(h, w, 3)
        s, marg = read_mask(mask_of(fr), keys, protos)
        cur = mx = None
        if s and "/" in s:
            a, _, b = s.partition("/")
            if a.isdigit() and b.isdigit():
                cur, mx = int(a), int(b)
        rows.append({"f": k, "t": round(t0 + k / FPS, 5), "raw": s,
                     "cur": cur, "max": mx, "margin": round(marg, 1)})
        k += 1
    p.stdout.close(); p.wait()
    json.dump({"video": video, "t0": t0, "t1": t1, "n": len(rows), "rows": rows},
              open(out, "w"))
    ok = sum(1 for r in rows if r["cur"] is not None)
    print(f"trace {t0}-{t1}: {len(rows)} frames, {ok} parsed ({100*ok/max(1,len(rows)):.2f}%)")


if __name__ == "__main__":
    c = sys.argv[1]
    if c == "atlas":
        build_atlas(sys.argv[2], json.load(open(sys.argv[3])), sys.argv[4])
    elif c == "trace":
        trace(sys.argv[2], float(sys.argv[3]), float(sys.argv[4]), sys.argv[5], sys.argv[6])
