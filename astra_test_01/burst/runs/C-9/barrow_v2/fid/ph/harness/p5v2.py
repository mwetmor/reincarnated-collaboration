#!/usr/bin/env python3
"""P5 v2 -- re-instrumented per jack-ryan's pre-ruling (agentic_orchestration/qa/findings/2026-10-08-bv2f-p5-dense-texture-
preruling.md, 309c4c41b; adopted R-C9-251 subject to this calibration). Parameters are the finding's, frozen there.

  a1  overlap TONE disagreement, RAW canvases: each canvas's rendition of the shared 256-px strip, Gaussian sigma 6 px per
      sRGB channel (0-255), mean over channels of |G(a) - G(b)|, trimmed 12 px on every strip edge, split along the
      overlap's length into 128-px segments (8 vertical, 12 horizontal); score = per-segment mean; row = max segment.
  a2  overlap GRAIN disagreement, RAW canvases: H = luma - G_sigma3(luma); same segments; |log2((std H_b + .5)/(std H_a + .5))|.
  b   stitched seam visibility at the band centre: p5_seams.seam_vis, unchanged (<= 0.799).
  c   context-boundary STEP on the STITCHED painting: x = 1280c + 256 (c >= 1, over chunk (c, r)'s row span) and
      y = 768r + 256 (r >= 1, over its column span), per 64-px segment, on Lab (D65) blurred sigma 4 px; ALL classes.
        T(p) = || mean Lab[p-10, p-4) - mean Lab[p+4, p+10) ||
        G(p) = | log2((std H[p, p+24) + .05) / (std H[p-24, p) + .05)) |,  H = L* - G_sigma3(L*) (L* unblurred)
        excess = X(0) - median X(+-o), o in {32, 40, ..., 96}
      a segment counts only inside a run of >= 2 consecutive segments on one boundary; run score = min of the two;
      a segment whose +-110 px window touches unpainted px is excluded.
  Bars: v1's own maximum on the same measure (T10BF raw canvases; barrow_full_painted.png, flag-off).
  Raw overlap MAD: reported, not binding.
"""
import hashlib
import json
import math
import os
import pathlib
import subprocess
import sys

import numpy as np
from PIL import Image
from scipy import ndimage

sys.path.insert(0, os.path.dirname(__file__))
from common import *  # noqa
import p5_seams as S5

CW, CH, SX, SY = 1536, 1024, 1280, 768
OV = 256
TRIM, SEG_A, SEG_C = 12, 128, 64
OFFS = list(range(32, 97, 8))
STITCH = FID / "v1tools/tierB/conductor_scripts/guided_stitch.py"
SCR = pathlib.Path(os.environ.get("PH_P5_SCRATCH", "/private/tmp/claude-501/-Users-admin-Games-reincarnated-collaboration/"
                                  "df21e264-6571-4d04-96ee-b8e2bd6d97fa/scratchpad/p5v2"))


def load(p):
    return np.asarray(Image.open(p).convert("RGB"), np.float32)


def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


# --------------------------------------------------------------------------------------------------- a1 / a2
def _strips(A, B, horiz):
    """horiz: B is A's right neighbour (shared columns); else B is A's lower neighbour (shared rows)"""
    if horiz:
        return A[:, SX:CW], B[:, :OV]          # 1024 x 256
    return A[SY:CH, :], B[:OV, :]              # 256 x 1536


def _luma(x):
    return 0.2126 * x[..., 0] + 0.7152 * x[..., 1] + 0.0722 * x[..., 2]


def a_pair(A, B, horiz):
    sa, sb = _strips(A, B, horiz)
    ga = np.stack([ndimage.gaussian_filter(sa[..., k], 6) for k in range(3)], -1)
    gb = np.stack([ndimage.gaussian_filter(sb[..., k], 6) for k in range(3)], -1)
    d = np.abs(ga - gb).mean(-1)
    la, lb = _luma(sa), _luma(sb)
    ha, hb = la - ndimage.gaussian_filter(la, 3), lb - ndimage.gaussian_filter(lb, 3)
    if not horiz:                              # put the overlap's LENGTH on axis 0 for both orientations
        d, ha, hb = d.T, ha.T, hb.T
    L = d.shape[0]
    d, ha, hb = d[TRIM:L - TRIM, TRIM:OV - TRIM], ha[TRIM:L - TRIM, TRIM:OV - TRIM], hb[TRIM:L - TRIM, TRIM:OV - TRIM]
    a1, a2 = [], []
    for s0 in range(0, L, SEG_A):
        lo, hi = max(s0 - TRIM, 0), min(s0 + SEG_A - TRIM, L - 2 * TRIM)
        if hi <= lo:
            continue
        a1.append(float(d[lo:hi].mean()))
        a2.append(abs(math.log2((hb[lo:hi].std() + 0.5) / (ha[lo:hi].std() + 0.5))))
    raw = float(np.abs(sa - sb).mean())
    return {"a1": a1, "a2": a2, "raw_mad": round(raw, 2)}


def a_set(paths, mod=None):
    """paths: key 'c_r' -> canvas png. mod(key, img) -> img lets a constructed fail alter one canvas."""
    cache = {}

    def get(k):
        if k not in cache:
            im = load(paths[k])
            cache[k] = mod(k, im) if mod else im
        return cache[k]
    rows = []
    for k in sorted(paths):
        c, r = map(int, k.split("_"))
        for dc, dr, horiz, sep in ((1, 0, True, "|"), (0, 1, False, "/")):
            n = "%d_%d" % (c + dc, r + dr)
            if n not in paths:
                continue
            res = a_pair(get(k), get(n), horiz)
            rows.append({"join": k + sep + n, "a1_max": round(max(res["a1"]), 3), "a2_max": round(max(res["a2"]), 3),
                         "a1_segments": [round(x, 3) for x in res["a1"]], "a2_segments": [round(x, 3) for x in res["a2"]],
                         "raw_mad": res["raw_mad"]})
    return rows


# --------------------------------------------------------------------------------------------------- c
def rgb2lab(img):
    return rgb_to_lab(img)


def c_measure(img, keys, cols=None, rows=None):
    """img: stitched painting (RGB float); keys: the painted chunk keys 'c_r' (coverage = union of their rects)"""
    Hh, Ww = img.shape[:2]
    cov = np.zeros((Hh, Ww), bool)
    for k in keys:
        c, r = map(int, k.split("_"))
        cov[SY * r:SY * r + CH, SX * c:SX * c + CW] = True
    unp = ~cov
    lab = rgb2lab(img)
    labb = np.stack([ndimage.gaussian_filter(lab[..., k], 4) for k in range(3)], -1)
    L = lab[..., 0]
    Hf = L - ndimage.gaussian_filter(L, 3)
    out = []
    ks = set(keys)
    for k in sorted(keys):
        c, r = map(int, k.split("_"))
        for vert, nb in ((True, "%d_%d" % (c - 1, r)), (False, "%d_%d" % (c, r - 1))):
            if nb not in ks:
                continue
            if vert:
                p = SX * c + OV
                span = (SY * r, min(SY * r + CH, Hh))
            else:
                p = SY * r + OV
                span = (SX * c, min(SX * c + CW, Ww))
            segs = []
            for s0 in range(span[0], span[1] - SEG_C + 1, SEG_C):
                s1 = s0 + SEG_C
                if vert:
                    win = unp[max(s0 - 110, 0):s1 + 110, max(p - 110, 0):p + 110]
                    T = lambda q: float(np.linalg.norm(labb[s0:s1, q - 10:q - 4].reshape(-1, 3).mean(0) - labb[s0:s1, q + 4:q + 10].reshape(-1, 3).mean(0)))
                    G = lambda q: abs(math.log2((Hf[s0:s1, q:q + 24].std() + 0.05) / (Hf[s0:s1, q - 24:q].std() + 0.05)))
                else:
                    win = unp[max(p - 110, 0):p + 110, max(s0 - 110, 0):s1 + 110]
                    T = lambda q: float(np.linalg.norm(labb[q - 10:q - 4, s0:s1].reshape(-1, 3).mean(0) - labb[q + 4:q + 10, s0:s1].reshape(-1, 3).mean(0)))
                    G = lambda q: abs(math.log2((Hf[q:q + 24, s0:s1].std() + 0.05) / (Hf[q - 24:q, s0:s1].std() + 0.05)))
                lim = Ww if vert else Hh
                if win.any() or p - 96 - 24 < 0 or p + 96 + 24 > lim:
                    segs.append(None)
                    continue
                tx = T(p) - float(np.median([T(p + s * o) for o in OFFS for s in (-1, 1)]))
                gx = G(p) - float(np.median([G(p + s * o) for o in OFFS for s in (-1, 1)]))
                segs.append((s0, tx, gx))
            runs = []
            for a, b in zip(segs, segs[1:]):
                if a is None or b is None:
                    continue
                runs.append({"at": a[0], "tone": round(min(a[1], b[1]), 3), "grain": round(min(a[2], b[2]), 3)})
            out.append({"boundary": ("x=%d" if vert else "y=%d") % p, "chunk": k, "span": list(span), "runs": runs,
                        "tone_max": max([x["tone"] for x in runs], default=None), "grain_max": max([x["grain"] for x in runs], default=None)})
    return out


def c_max(rows, what):
    v = [r[what + "_max"] for r in rows if r[what + "_max"] is not None]
    return max(v) if v else None


# --------------------------------------------------------------------------------------------------- stitching
def stitch(prefix, cols, rows, out, flags):
    """PT's Tier-B guided_stitch.py (read-only, run as-is) with env flags {'BV2F_DEV23': '0'/'1', ...}"""
    SCR.mkdir(parents=True, exist_ok=True)
    cfg = SCR / ("cfg_%s.json" % prefix)
    cfg.write_text(json.dumps({"prefix": prefix, "cols": cols, "rows": rows}))
    env = dict(os.environ, **flags)
    r = subprocess.run([sys.executable, str(STITCH), str(cfg), str(out)], env=env, capture_output=True, text=True)
    if r.returncode:
        raise SystemExit("stitch failed: " + r.stderr[-800:])
    return r.stdout.strip()


OFF = {"BV2F_DEV23": "0", "BV2F_DEV25": "0", "BV2F_DEV26": "0", "BV2F_DEV27": "0"}
ON2325 = {"BV2F_DEV23": "1", "BV2F_DEV25": "1", "BV2F_DEV26": "0", "BV2F_DEV27": "0"}
ALLON = {"BV2F_DEV23": "1", "BV2F_DEV25": "1", "BV2F_DEV26": "1", "BV2F_DEV27": "1"}


# --------------------------------------------------------------------------------------------------- canvas sets
def v1_paths():
    return S5.canvases("T10BF")


def manifest_pilot3():
    """C5: the build's canvases, pinned explicitly (never canvases(): it prefers -r1 = PS3b for BV2F-PS3)"""
    m = {}
    for c in range(3):
        for r in range(3):
            k = "%d_%d" % (c, r)
            d = "BV2F-PS3A-%s-r1" % k if k == "2_2" else "BV2F-PS3A-%s" % k
            p = ART / d / ("BV2F-PS3A-%s.png" % k)
            m[k] = {"path": str(p), "sha256": sha(p), "dir": d}
    return m


def verdict_row(a, b, c, bars, a2_alive=True):
    fa1 = [r["join"] for r in a if r["a1_max"] > bars["a1"]]
    fa2 = [r["join"] for r in a if r["a2_max"] > bars["a2"]] if a2_alive else []
    fb = [s["seam"] for s in b if s["score"] > 0.799]
    fct = [(x["boundary"], x["chunk"]) for x in c if x["tone_max"] is not None and x["tone_max"] > bars["c_tone"]]
    fcg = [(x["boundary"], x["chunk"]) for x in c if x["grain_max"] is not None and x["grain_max"] > bars["c_grain"]]
    return {"a1_over": fa1, "a2_over": fa2, "b_over": fb, "c_tone_over": fct, "c_grain_over": fcg,
            "pass": not (fa1 or fa2 or fb or fct or fcg)}
