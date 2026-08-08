#!/usr/bin/env python3
"""eor_cohort.py — WAVE-START COHORT CENSUS for Grim Dawn Crucible footage.

galadriel / visual-perception seam. KC2-SIM fourth-extraction pass.

Why this module exists. The third-extraction chain located readouts
(`eor_hptext.scan`) and read them (`eor_hpocr.read_index`) in TWO decode passes
over the same window. At the I/O rates this footage delivers that is the
dominant cost, and a five-wave census multiplies it by five. This module fuses
locate+read into ONE streaming decode pass, and adds the per-frame simultaneity
bookkeeping a census needs (a `top-N of distinct values` answer is not a census;
`how many bodies were on camera at once` is).

It LOCATES and CLUSTERS only. Every value that reaches a note is eye-read from a
magnified exact-seek crop, exactly as in the three prior passes.

  census <video> <t0> <t1> <fps> <atlas.npz> <out.json>
  simul  <out.json>                       per-frame simultaneity + body bounds
"""
from __future__ import annotations

import json
import subprocess
import sys
from collections import defaultdict

import numpy as np

sys.path.insert(0, __file__.rsplit("/", 1)[0])

import eor_hptext as HT      # noqa: E402
import eor_hpocr as HO       # noqa: E402

W, H = 1920, 1080


# --------------------------------------------------------------- blob finding
#
# Two behaviours the third-extraction locator did not have to handle, both of
# which appear the moment the census moves off wave 160 and into the 151-158
# band, and both of which corrupt a count if left alone:
#
#   (a) VIEWPORT-EDGE CLIPPING. Monsters at the screen edge have their readout
#       cut by the frame. Left-clipping eats the numerator and LEAVES THE
#       DENOMINATOR INTACT ("...874/225,874)"), so the fingerprint survives and
#       must be recovered. Right-clipping eats the denominator ("(453,064"), so
#       the body is present but its fingerprint is UNAVAILABLE - which is a
#       different fact from "no body there" and is recorded as such.
#   (b) ROW FRAGMENTATION. A dim glyph can break the dilation chain and split
#       one string into two boxes. Merging same-row neighbours repairs it.

def _mask(frame, min_ch=HT.MIN_CH):
    return frame.min(axis=2) > min_ch


def blobs2(frame, min_w=30, max_w=340, min_h=5, max_h=16, gap=HT.GAP):
    """Text-run boxes. Same achromatic gate as eor_hptext, looser width floor so
    edge-clipped fragments survive, plus a same-row merge pass."""
    m = _mask(frame)
    if not m.any():
        return []
    d = m.copy()
    for k in range(1, gap + 1):
        d[:, k:] |= m[:, :-k]
        d[:, :-k] |= m[:, k:]
    d[1:, :] |= d[:-1, :]
    d[:-1, :] |= d[1:, :]

    seen = np.zeros(d.shape, dtype=bool)
    ys, xs = np.where(d)
    raw = []
    for y0, x0 in zip(ys, xs):
        if seen[y0, x0]:
            continue
        stack = [(y0, x0)]
        seen[y0, x0] = True
        minx = maxx = x0
        miny = maxy = y0
        while stack:
            y, x = stack.pop()
            if x < minx: minx = x
            if x > maxx: maxx = x
            if y < miny: miny = y
            if y > maxy: maxy = y
            for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                ny, nx = y + dy, x + dx
                if 0 <= ny < d.shape[0] and 0 <= nx < d.shape[1] \
                        and d[ny, nx] and not seen[ny, nx]:
                    seen[ny, nx] = True
                    stack.append((ny, nx))
        h = maxy - miny + 1
        if not (min_h <= h <= max_h):
            continue
        raw.append([int(minx), int(miny), int(maxx), int(maxy)])

    # same-row merge: vertical overlap >= 50% of the shorter box, x-gap <= 22
    raw.sort(key=lambda b: (b[1], b[0]))
    merged, used = [], [False] * len(raw)
    for i, b in enumerate(raw):
        if used[i]:
            continue
        cur = list(b)
        used[i] = True
        changed = True
        while changed:
            changed = False
            for j, c in enumerate(raw):
                if used[j]:
                    continue
                ov = min(cur[3], c[3]) - max(cur[1], c[1]) + 1
                sh = min(cur[3] - cur[1], c[3] - c[1]) + 1
                if ov < 0.5 * sh:
                    continue
                gapx = max(cur[0], c[0]) - min(cur[2], c[2]) - 1
                if gapx > 22:
                    continue
                cur = [min(cur[0], c[0]), min(cur[1], c[1]),
                       max(cur[2], c[2]), max(cur[3], c[3])]
                used[j] = True
                changed = True
        merged.append(cur)

    out = []
    for (x0, y0, x1, y1) in merged:
        w = x1 - x0 + 1
        if not (min_w <= w <= max_w):
            continue
        if HT.in_hud(x0, y0, x1, y1):
            continue
        dens = m[y0:y1 + 1, x0:x1 + 1].mean()
        if not (0.04 <= dens <= 0.55):
            continue
        out.append((x0, y0, x1, y1, round(float(dens), 3)))
    return out


def parse_ext(s):
    """Extended readout parse.

    Returns (kind, cur, max):
      'full'   -> "(cur/max)"        both recovered
      'lclip'  -> "...cur/max)"      denominator recovered, numerator partial
      'rclip'  -> "(cur..."          BODY PRESENT, denominator unavailable
      None     -> not a readout
    """
    pr = HO.parse(s)
    if pr:
        return ("full", pr[0], pr[1])

    def _num(x):
        if not x or not all(c in "0123456789," for c in x):
            return None
        segs = x.split(",")
        if len(segs) > 1 and (not (1 <= len(segs[0]) <= 3)
                              or any(len(q) != 3 for q in segs[1:])):
            return None
        try:
            v = int(x.replace(",", ""))
        except ValueError:
            return None
        return v if v > 0 else None

    # left-clipped: ends in ')', has a '/', denominator fully rendered
    if s.endswith(")") and "/" in s and not s.startswith("("):
        tail = s[:-1].rsplit("/", 1)[-1]
        v = _num(tail)
        if v is not None and len(tail.replace(",", "")) >= 4:
            return ("lclip", None, v)
    # right-clipped: opens the readout, never closes it
    if s.startswith("(") and ")" not in s:
        head = s[1:].split("/")[0]
        v = _num(head)
        if v is not None:
            return ("rclip", v, None)
    return None


def census(video, t0, t1, fps, atlaspath, outpath):
    """Single streaming decode pass: locate + OCR every readout in the window."""
    atlas = HO.load(atlaspath)
    dur = t1 - t0
    cmd = ["ffmpeg", "-v", "error", "-ss", f"{t0}", "-t", f"{dur}", "-i", video,
           "-vf", f"fps={fps}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=W * H * 3)
    nb = W * H * 3
    out, i = [], 0
    while True:
        buf = p.stdout.read(nb)
        if len(buf) < nb:
            break
        fr = np.frombuffer(buf, dtype=np.uint8).reshape(H, W, 3)
        t = round(t0 + i / fps, 4)
        bl = blobs2(fr)
        if bl:
            v_all = HO.white(fr)
            for (x0, y0, x1, y1, dens) in bl:
                s, sc, mg = HO.read_string(atlas, v_all[y0:y1 + 1, x0:x1 + 1])
                pe = parse_ext(s)
                out.append({"t": t, "box": [x0, y0, x1, y1], "raw": s,
                            "kind": pe[0] if pe else None,
                            "cur": pe[1] if pe else None,
                            "max": pe[2] if pe else None,
                            "edge": ("L" if x0 <= 1 else "") + ("R" if x1 >= W - 2 else ""),
                            "score": round(sc, 3), "margin": round(mg, 3)})
        i += 1
        if i % 100 == 0:
            print(f"  ... {i} frames, {len(out)} readouts", flush=True)
    p.stdout.close(); p.wait()
    json.dump({"video": video, "t0": t0, "t1": t1, "fps": fps,
               "frames": i, "rows": out}, open(outpath, "w"))
    nk = defaultdict(int)
    for r in out:
        nk[r["kind"]] += 1
    print(f"frames={i} readouts={len(out)} " + " ".join(
        f"{k}={v}" for k, v in sorted(nk.items(), key=lambda x: str(x[0]))))
    return out


# ------------------------------------------------------------ body resolution

def _cluster_frame(rs, xtol=40):
    """Group one frame's readouts into BODIES.

    One body renders one readout per frame, so two boxes that share a row band
    and sit within xtol of each other are the same readout split by the locator,
    not two monsters. Returns list of body dicts.
    """
    rs = sorted(rs, key=lambda r: (r["box"][1], r["box"][0]))
    used = [False] * len(rs)
    out = []
    for i, a in enumerate(rs):
        if used[i]:
            continue
        grp = [a]
        used[i] = True
        changed = True
        while changed:
            changed = False
            for j, b in enumerate(rs):
                if used[j]:
                    continue
                for g in grp:
                    ov = min(g["box"][3], b["box"][3]) - max(g["box"][1], b["box"][1]) + 1
                    sh = min(g["box"][3] - g["box"][1], b["box"][3] - b["box"][1]) + 1
                    gx = max(g["box"][0], b["box"][0]) - min(g["box"][2], b["box"][2]) - 1
                    if ov >= 0.5 * sh and gx <= xtol:
                        grp.append(b)
                        used[j] = True
                        changed = True
                        break
        # A cluster carrying two DIFFERENT fully-parsed maxes is two monsters
        # standing close enough to brush readouts, not one split string. Split
        # it back out - measured at 0.14% of clusters, but it understates a peak.
        fulls = {g["max"] for g in grp if g["kind"] == "full"}
        if len(fulls) > 1:
            for fm in sorted(fulls):
                sub = [g for g in grp if g["kind"] == "full" and g["max"] == fm]
                out.append({"max": fm, "cur": sub[0]["cur"],
                            "x": min(g["box"][0] for g in sub),
                            "y": min(g["box"][1] for g in sub),
                            "kinds": ["full"], "n": len(sub), "split": True})
            continue
        mx = next((g["max"] for g in grp if g["kind"] == "full"), None)
        if mx is None:
            mx = next((g["max"] for g in grp if g["kind"] == "lclip"), None)
        cur = next((g["cur"] for g in grp if g["kind"] == "full"), None)
        kinds = {g["kind"] for g in grp}
        out.append({"max": mx, "cur": cur,
                    "x": min(g["box"][0] for g in grp),
                    "y": min(g["box"][1] for g in grp),
                    "kinds": sorted(k for k in kinds if k),
                    "n": len(grp)})
    return out


def bodies(path, exclude_max=(), t_lo=None, t_hi=None, noise_max=()):
    """`exclude_max` DROPS a readout (used for the player globe, which is not a
    census body). `noise_max` keeps the readout as a BODY but nulls its
    fingerprint - the right treatment for an eye-confirmed OCR corruption, which
    is evidence of a body on camera and not evidence of a distinct monster."""
    return _bodies(path, exclude_max, t_lo, t_hi, set(noise_max))


def _bodies(path, exclude_max=(), t_lo=None, t_hi=None, noise_max=frozenset()):
    """Per-frame body resolution + per-fingerprint multiplicity.

    Returns (per_frame, per_max). A fingerprint's `simul_max` is the largest
    number of SIMULTANEOUS distinct bodies carrying it on one frame - the
    established lower bound on how many bodies share that max HP.
    """
    d = json.load(open(path))
    byframe = defaultdict(list)
    for r in d["rows"]:
        if r["kind"] is None:
            continue
        if t_lo is not None and r["t"] < t_lo:
            continue
        if t_hi is not None and r["t"] > t_hi:
            continue
        if r["max"] in exclude_max:
            continue
        if r["max"] in noise_max:
            r = dict(r, max=None, cur=None)
        byframe[r["t"]].append(r)

    per_frame = {}
    stat = defaultdict(lambda: {"n": 0, "simul_max": 0, "simul_t": None,
                                "t0": 9e9, "t1": -9e9})
    for t in sorted(byframe):
        bl = _cluster_frame(byframe[t])
        known = [b for b in bl if b["max"] is not None]
        unk = [b for b in bl if b["max"] is None]
        per_frame[t] = {"bodies": len(bl), "known": len(known),
                        "unknown_max": len(unk),
                        "maxes": sorted(b["max"] for b in known)}
        cnt = defaultdict(int)
        for b in known:
            cnt[b["max"]] += 1
        for mx, c in cnt.items():
            s = stat[mx]
            s["n"] += c
            s["t0"] = min(s["t0"], t)
            s["t1"] = max(s["t1"], t)
            if c > s["simul_max"]:
                s["simul_max"] = c
                s["simul_t"] = t
    per_max = {k: {"n": v["n"], "simul_max": v["simul_max"],
                   "simul_t": v["simul_t"],
                   "t0": round(v["t0"], 3), "t1": round(v["t1"], 3)}
               for k, v in stat.items()}
    return per_frame, per_max


# ---------------------------------------------------------------- simultaneity

def simul(path, player_max=None, min_n=1):
    """Per-frame and per-fingerprint simultaneity bookkeeping.

    Returns a dict with, for each parsed max-HP fingerprint:
      n           number of readouts carrying it
      simul_max   the largest number of SIMULTANEOUS readouts of that max with
                  DISTINCT current values on one frame  -> a lower bound on the
                  number of bodies sharing the fingerprint
      t0, t1      first and last frame carrying it
    and, per frame, the number of distinct readouts on camera.
    """
    d = json.load(open(path))
    rows = d["rows"]
    byframe = defaultdict(list)
    for r in rows:
        if r["max"]:
            byframe[r["t"]].append(r)

    stat = defaultdict(lambda: {"n": 0, "simul_max": 0, "t0": 9e9, "t1": -9e9,
                                "simul_t": None, "curs": set()})
    frame_counts = {}
    for t, rs in byframe.items():
        # distinct bodies on this frame: unique (max, cur) pairs, since one body
        # renders one readout per frame
        uniq = {(r["max"], r["cur"]) for r in rs}
        frame_counts[t] = len(uniq)
        per = defaultdict(set)
        for r in rs:
            per[r["max"]].add(r["cur"])
        for mx, curs in per.items():
            s = stat[mx]
            s["n"] += len([r for r in rs if r["max"] == mx])
            s["t0"] = min(s["t0"], t)
            s["t1"] = max(s["t1"], t)
            if len(curs) > s["simul_max"]:
                s["simul_max"] = len(curs)
                s["simul_t"] = t
    out = {}
    for mx, s in stat.items():
        if s["n"] < min_n:
            continue
        out[mx] = {"n": s["n"], "simul_max": s["simul_max"],
                   "simul_t": s["simul_t"],
                   "t0": round(s["t0"], 3), "t1": round(s["t1"], 3)}
    return {"per_max": out, "frame_counts": frame_counts,
            "frames_with_readouts": len(byframe), "frames": d["frames"]}


if __name__ == "__main__":
    if sys.argv[1] == "census":
        census(sys.argv[2], float(sys.argv[3]), float(sys.argv[4]),
               float(sys.argv[5]), sys.argv[6], sys.argv[7])
    elif sys.argv[1] == "simul":
        s = simul(sys.argv[2])
        fc = s["frame_counts"]
        print(f"frames={s['frames']} with_readouts={s['frames_with_readouts']}")
        if fc:
            mx = max(fc.values())
            print(f"max simultaneous distinct readouts = {mx} at "
                  f"{[t for t, v in fc.items() if v == mx][:6]}")
        for k in sorted(s["per_max"], reverse=True):
            v = s["per_max"][k]
            print(f"  {k:>12,}  n={v['n']:<5} simul={v['simul_max']} "
                  f"@{v['simul_t']}  {v['t0']} -> {v['t1']}")
