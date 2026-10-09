#!/usr/bin/env python3
"""§ 52 (R-C9-331; jack-ryan painting Gate-2 H-1, #76): DERIVE the § 51 substitution domain for the FULL-SITE a1 table
from geometry x staging chronology -- never a named list. Reads NO a1 value (no tone, no MAD): only
  (1) the pinned 25 canvases (sha-checked against fid/pt/ph3/final/canvases.json),
  (2) the pinned DEV-29 inputs (context_patch painting + support mask, sha-checked against cfg_bv2a_ph3.json),
  (3) each NEWER chunk's STAGED canvas (artifacts/CS9-guides/<task>_canvas.png: the exact IMAGE 1 the painter got),
and records, per join, the plate rect of the context strip, its mask px, and WHETHER the stager substituted there:
  DEV29_ON  iff inside (strip & mask) the staged canvas equals the context_patch painting on >= 99 % of px
  DEV29_OFF iff it equals the RAW older canvas there on >= 99 % of px      (anything else: UNRESOLVED -> STOP)
Joins: '|' (c,r)|(c+1,r), '/' (c,r)/(c,r+1), '\\' (c,r)\\(c+1,r+1), 'x/' (c+1,r)/(c,r+1) (anti-diagonal). The ready rule
(cfg _wavefront: left, top, top-right painted first) makes the right / lower chunk the NEWER side of every pair.
  site_domain.py -> results/site/s52_domain.json"""
import json
import os
import pathlib
import sys

import numpy as np
from PIL import Image

sys.path.insert(0, os.path.dirname(__file__))
from common import *  # noqa
import p5v2 as V

ART = C9 / "artifacts"
GUIDES = ART / "CS9-guides"
CANV = jload(FID / "pt/ph3/final/canvases.json")
CFG = jload(FID / "pt/pilot/cfg_bv2a_ph3.json")
W, H = 6656, 4096
CW, CH, SX, SY, OV = 1536, 1024, 1280, 768, 256


def task_of(k):
    """the kept canvas's task id (its artifacts dir); a byte COPY points at the task that painted it"""
    d = pathlib.Path(CANV[k]["canvas"]).parent.name
    cp = ART / d / "COPY.json"
    if cp.exists():
        src = jload(cp)["copy_of"]
        return pathlib.Path(src).parts[0] if "/" in src else src
    return d


def strip_rect(kind, c, r):
    """plate rect [x0, y0, x1, y1) of the context strip the NEWER chunk received from the OLDER one"""
    if kind == "|":
        return (SX * (c + 1), SY * r, SX * (c + 1) + OV, SY * r + CH)
    if kind == "/":
        return (SX * c, SY * (r + 1), SX * c + CW, SY * (r + 1) + OV)
    return (SX * (c + 1), SY * (r + 1), SX * (c + 1) + OV, SY * (r + 1) + OV)      # both diagonals: the corner square


def main():
    cp = CFG["context_patch"]
    assert V.sha(cp["painting"]) == cp["painting_sha256"], "context_patch painting sha mismatch -> STOP"
    assert V.sha(cp["mask"]) == cp["mask_sha256"], "context_patch mask sha mismatch -> STOP"
    pp = V.load(cp["painting"])
    mk = np.asarray(Image.open(cp["mask"])) > 127
    patched = np.zeros((H, W, 3), np.float32)
    patched[:pp.shape[0], :pp.shape[1]] = pp
    mask = np.zeros((H, W), bool)
    mask[:mk.shape[0], :mk.shape[1]] = mk
    bad = [k for k, v in CANV.items() if V.sha(ART / v["canvas"]) != v["sha256"]]
    assert not bad, "pinned canvas sha mismatch -> STOP: %s" % bad
    raw = {k: V.load(ART / v["canvas"]) for k, v in CANV.items()}
    staged = {}
    joins = []
    for r in range(5):
        for c in range(5):
            cand = []
            if c < 4:
                cand.append(("|", "%d_%d" % (c, r), "%d_%d" % (c + 1, r)))
            if r < 4:
                cand.append(("/", "%d_%d" % (c, r), "%d_%d" % (c, r + 1)))
            if c < 4 and r < 4:
                cand.append(("\\", "%d_%d" % (c, r), "%d_%d" % (c + 1, r + 1)))
                cand.append(("x/", "%d_%d" % (c + 1, r), "%d_%d" % (c, r + 1)))
            for kind, a, b in cand:
                ca, ra = map(int, a.split("_"))
                rect = strip_rect(kind, c, r)
                x0, y0, x1, y1 = rect
                m = mask[y0:y1, x0:x1]
                row = {"join": a + {"|": "|", "/": "/", "\\": "\\", "x/": " x/ "}[kind] + b, "kind": kind, "older": a, "newer": b,
                       "pilot_pair": bool(CANV[a]["pilot"] and CANV[b]["pilot"]), "strip_rect_xyxy": list(rect),
                       "strip_px": int(m.size), "mask_px": int(m.sum()), "mask_share": round(float(m.mean()), 4),
                       "newer_task": task_of(b)}
                if m.sum() == 0:
                    row["dev29"] = "n/a (strip clear of the mask: substitution is the identity)"
                    row["substitute_older"] = False
                elif row["pilot_pair"]:
                    row["dev29"] = "OFF (pilot-4 staging, before DEV-29 existed)"
                    row["substitute_older"] = False
                else:
                    t = row["newer_task"]
                    if t not in staged:
                        staged[t] = V.load(GUIDES / ("%s_canvas.png" % t))
                    S = staged[t]
                    cb, rb = map(int, b.split("_"))
                    bx, by = SX * cb, SY * rb                       # the newer canvas's plate origin
                    sl = (slice(y0 - by, y1 - by), slice(x0 - bx, x1 - bx))
                    s = S[sl][m]
                    p = patched[y0:y1, x0:x1][m]
                    o = raw[a][(slice(y0 - SY * ra, y1 - SY * ra), slice(x0 - SX * ca, x1 - SX * ca))][m]
                    eq_p = float(np.all(np.abs(s - p) <= 1, -1).mean())
                    eq_o = float(np.all(np.abs(s - o) <= 1, -1).mean())
                    row.update(staged_eq_patched=round(eq_p, 4), staged_eq_raw_older=round(eq_o, 4),
                               staged_canvas="artifacts/CS9-guides/%s_canvas.png" % t, staged_sha256=V.sha(GUIDES / ("%s_canvas.png" % t)))
                    if eq_p >= 0.99 and eq_p > eq_o:
                        row["dev29"], row["substitute_older"] = "ON (staged == context_patch painting in strip & mask)", True
                    elif eq_o >= 0.99:
                        row["dev29"], row["substitute_older"] = "OFF (staged == raw older canvas in strip & mask)", False
                    else:
                        row["dev29"], row["substitute_older"] = "UNRESOLVED -> STOP", None
                joins.append(row)
    out = {"_what": "§ 52 derived § 51 domain (R-C9-331 / Gate-2 H-1): geometry x staging chronology; NO a1 value read",
           "context_patch": {"painting_sha256": cp["painting_sha256"], "mask_sha256": cp["mask_sha256"]},
           "canvases_sha_ok": True, "dev25c_chunks": CFG["dev25c_chunks"],
           "domain_substituted": [j["join"] for j in joins if j["substitute_older"]],
           "strip_meets_mask": [j["join"] for j in joins if j["mask_px"] > 0],
           "unresolved": [j["join"] for j in joins if j["substitute_older"] is None],
           "joins": joins}
    od = PH / "results/site"
    od.mkdir(parents=True, exist_ok=True)
    dump(out, str(od / "s52_domain.json"))
    for j in joins:
        if j["mask_px"]:
            print("%-14s mask %6d (%.3f)  %s  %s" % (j["join"], j["mask_px"], j["mask_share"], j["dev29"],
                                                    {k: j[k] for k in ("staged_eq_patched", "staged_eq_raw_older") if k in j}))
    print("substituted:", out["domain_substituted"], "unresolved:", out["unresolved"])


if __name__ == "__main__":
    main()
