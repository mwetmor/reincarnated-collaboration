#!/usr/bin/env python3
"""§ 52 (a): the FULL-SITE P5 table (R-C9-331 / Gate-2 H-1), exactly as pre-registered at commit 7d47a498d.
  a1 (§ 44, full 256, bar 9.569) on the 40 neighbour joins; § 51 substitution on the DERIVED domain (s52_domain.json);
  W-1 add-only guard for joins new to the domain; '\\' corners vs 4.809 (only 2_2\\3_3 binds); anti-diagonal corners
  report-only beside v1's own 9; P5(b) seam_vis 5 x 5 on the r328 painting (<= 0.799); raw MAD + c reported;
  1:1 crops (jpg + sha) for every join over its bar or raw MAD > 13.09.
  site_p5.py -> results/site/p5.json, results/site/p5_crops/"""
import hashlib
import json
import os
import sys

import numpy as np
from PIL import Image
from scipy import ndimage

sys.path.insert(0, os.path.dirname(__file__))
from common import *  # noqa
import p5v2 as V
import p5_seams as S5
import site_domain as SD

OUT = PH / os.environ.get("PH_PILOT_OUT", "results/site")          # s57: results/site_r332
PAINT = FID / os.environ.get("PH_SITE_PAINT", "pt/ph3/final/painting_ph3_r328_full.png")
PAINT_SHA = os.environ.get("PH_SITE_PAINT_SHA", "3fc04a7d0f63180b9a6117d90e29bfc4d9ca4833c9c2ff0acb49ceeb65e44638")
BAR, BAR_CORNER = 9.569, 4.809
S51_NAMED = {"0_2/0_3", "1_2/1_3", "2_2/2_3", "2_2\\3_3"}
SX, SY, CW, CH, OV, TRIM = 1280, 768, 1536, 1024, 256, 12


def corner_a1(sa, sb):
    ga = np.stack([ndimage.gaussian_filter(sa[..., k], 6) for k in range(3)], -1)
    gb = np.stack([ndimage.gaussian_filter(sb[..., k], 6) for k in range(3)], -1)
    d = np.abs(ga - gb).mean(-1)
    segs = []
    for y in range(0, OV, 128):
        for x in range(0, OV, 128):
            blk = d[max(y, TRIM):min(y + 128, OV - TRIM), max(x, TRIM):min(x + 128, OV - TRIM)]
            segs.append(float(blk.mean()))
    return segs, round(float(np.abs(sa - sb).mean()), 2)


def anti_corner(A, B):
    """A = (c+1, r) (upper-right, OLDER), B = (c, r+1) (lower-left, newer): the shared corner square is A's bottom-left
    256 x 256 and B's top-right 256 x 256"""
    return corner_a1(A[SY:CH, :OV], B[:OV, SX:CW])


def v1_anti():
    """v1's own 9 anti-diagonal corners (T10BF raw canvases; context only, never a bar)"""
    vp = V.v1_paths()
    out = {}
    for r in range(3):
        for c in range(3):
            a, b = "%d_%d" % (c + 1, r), "%d_%d" % (c, r + 1)
            if a in vp and b in vp:
                s, _ = anti_corner(V.load(vp[a]), V.load(vp[b]))
                out[a + " x/ " + b] = round(max(s), 3)
    return out


def crop(P, j, segs, name):
    od = OUT / "p5_crops"
    od.mkdir(parents=True, exist_ok=True)
    x0, y0, x1, y1 = j["strip_rect_xyxy"]
    seg = int(np.argmax(segs))
    Hh, Ww = P.shape[:2]
    if j["kind"] == "|":
        cy = y0 + seg * 128 + 64
        box = (x0 + 128 - 256, max(0, min(cy - 256, Hh - 512)))
        box = (box[0], box[1], box[0] + 512, box[1] + 512)
    elif j["kind"] == "/":
        cx = x0 + seg * 128 + 64
        bx = max(0, min(cx - 512, Ww - 1024))
        box = (bx, y0 + 128 - 256, bx + 1024, y0 + 128 + 256)
    else:
        box = (x0 - 128, y0 - 128, x0 + 384, y0 + 384)
    fn = od / ("%s_seg%d_%s_x%d_y%d_1to1.jpg" % (j["join"].replace("|", "I").replace("/", "S").replace("\\", "D").replace(" x", "X").replace(" ", ""),
                                                 seg + 1, name, box[0], box[1]))
    Image.fromarray(np.clip(P[box[1]:box[3], box[0]:box[2]], 0, 255).astype(np.uint8)).save(fn, quality=92)
    return {"crop": str(fn.relative_to(FID)), "box_xyxy": list(box), "sha256": hashlib.sha256(fn.read_bytes()).hexdigest()}


def main():
    dom = jload(PH / "results/site/s52_domain.json")
    cfg = SD.CFG["context_patch"]
    assert V.sha(cfg["painting"]) == cfg["painting_sha256"] and V.sha(cfg["mask"]) == cfg["mask_sha256"], "DEV-29 inputs sha -> STOP"
    assert V.sha(PAINT) == PAINT_SHA, "painting sha -> STOP"
    bad = [k for k, v in SD.CANV.items() if V.sha(SD.ART / v["canvas"]) != v["sha256"]]
    assert not bad, "canvas sha -> STOP %s" % bad
    raw = {k: V.load(SD.ART / v["canvas"]) for k, v in SD.CANV.items()}
    pp = V.load(cfg["painting"])
    mk = np.asarray(Image.open(cfg["mask"])) > 127
    patched = np.zeros((SD.H, SD.W, 3), np.float32)
    patched[:pp.shape[0], :pp.shape[1]] = pp
    mask = np.zeros((SD.H, SD.W), bool)
    mask[:mk.shape[0], :mk.shape[1]] = mk
    # § 51 per-run real-mask self-test on every substituted OLDER canvas
    olders = sorted({j["older"] for j in dom["joins"] if j["substitute_older"]})
    selftest = {}
    sub = {}
    for k in olders:
        A2 = V.context_patch(raw[k], k, patched, mask)
        c, r = map(int, k.split("_"))
        m_c = mask[SY * r:SY * r + CH, SX * c:SX * c + CW]
        ch = np.any(A2 != raw[k], -1)
        ok = bool((ch & ~m_c).sum() == 0 and np.array_equal(A2[m_c], patched[SY * r:SY * r + CH, SX * c:SX * c + CW][m_c]))
        selftest[k] = {"mask_px_in_canvas": int(m_c.sum()), "changed_px": int(ch.sum()), "changed_outside_mask": int((ch & ~m_c).sum()),
                       "inside_equals_patched": ok, "pass": ok}
        assert ok, "DEV-29 self-test FAIL on %s -> STOP" % k
        sub[k] = A2
    P = load_rgb(PAINT)
    rows, corners, anti = [], [], []
    for j in dom["joins"]:
        a, b = j["older"], j["newer"]
        A, B = raw[a], raw[b]
        As = sub[a] if j["substitute_older"] else A
        if j["kind"] in ("|", "/"):
            horiz = j["kind"] == "|"
            rr = V.a_pair(A, B, horiz)
            rs = V.a_pair(As, B, horiz) if j["substitute_older"] else rr
            raw_max, sub_max = max(rr["a1"]), max(rs["a1"])
            new_dom = j["substitute_older"] and j["join"] not in S51_NAMED
            if j["substitute_older"] and not new_dom:
                binding, rule = sub_max, "s51 named: substituted"
            elif new_dom:
                binding, rule = max(raw_max, sub_max), "s52 new to domain: W-1 add-only (max of raw, substituted)"
            else:
                binding, rule = raw_max, "raw (substitution = identity or DEV-29 OFF)"
            row = {"join": j["join"], "kind": j["kind"], "dev29": j["dev29"], "rule": rule,
                   "a1_binding": round(binding, 3), "a1_raw": round(raw_max, 3),
                   "a1_substituted": round(sub_max, 3) if j["substitute_older"] else None,
                   "a1_segments_raw": [round(x, 3) for x in rr["a1"]],
                   "a1_segments_substituted": [round(x, 3) for x in rs["a1"]] if j["substitute_older"] else None,
                   "raw_mad": rr["raw_mad"], "pass": binding <= BAR, "pilot_pair": j["pilot_pair"]}
            segs = rs["a1"] if (j["substitute_older"] and sub_max >= raw_max) else rr["a1"]
            if not row["pass"] or rr["raw_mad"] > 13.09:
                row.update(crop(P, j, segs, "a1_%.3f" % binding))
            rows.append(row)
        elif j["kind"] == "\\":
            sr, mr = corner_a1(A[SY:CH, SX:CW], B[:OV, :OV])
            ss, _ = corner_a1(As[SY:CH, SX:CW], B[:OV, :OV]) if j["substitute_older"] else (sr, mr)
            binding = j["join"] == "2_2\\3_3"
            val = max(ss) if binding else max(max(sr), max(ss))
            row = {"join": j["join"], "dev29": j["dev29"], "binding": binding, "a1_corner": round(val, 3), "a1_raw": round(max(sr), 3),
                   "a1_substituted": round(max(ss), 3) if j["substitute_older"] else None, "raw_mad": mr,
                   "over_corner_bar_4.809": val > BAR_CORNER}
            if val > BAR_CORNER:
                row.update(crop(P, j, ss if max(ss) >= max(sr) else sr, "corner_%.3f" % val))
            corners.append(row)
        else:
            sr, mr = anti_corner(A, B)
            ss, _ = anti_corner(As, B) if j["substitute_older"] else (sr, mr)
            anti.append({"join": j["join"], "dev29": j["dev29"], "a1_raw": round(max(sr), 3),
                         "a1_substituted": round(max(ss), 3) if j["substitute_older"] else None, "raw_mad": mr, "report_only": True})
    b = S5.seam_vis(P, 5, 5)
    cal = jload(PH / "results/p5v2_calibration.json")
    c_on = V.c_measure(P, list(SD.CANV))
    fa = [r["join"] for r in rows if not r["pass"]]
    fb = [x["seam"] for x in b if x["score"] > 0.799]
    out = {"_what": "s52 (a) full-site P5, as pre-registered at 7d47a498d (R-C9-331)", "painting_sha256": PAINT_SHA,
           "bar_a1": BAR, "bar_corner": BAR_CORNER, "dev29_selftest": selftest,
           "a1_rows": rows, "a1_fail": fa, "a1_fail_n": len(fa), "a1_n": len(rows),
           "a1_fail_pilot_internal": [r["join"] for r in rows if not r["pass"] and r["pilot_pair"]],
           "corners": corners, "corner_binding_2_2_3_3": [c for c in corners if c["binding"]],
           "corners_over_bar_report_only": [(c["join"], c["a1_corner"]) for c in corners if c["over_corner_bar_4.809"] and not c["binding"]],
           "anti_corners_report_only": anti, "v1_anti_corners_context": v1_anti(),
           "b": b, "b_max": max(x["score"] for x in b), "b_over": fb,
           "reported_c_on": {"tone_max": V.c_max(c_on, "tone"), "grain_max": V.c_max(c_on, "grain"),
                             "tone_over_v1_bar": [(x["boundary"], x["chunk"], x["tone_max"]) for x in c_on
                                                  if x["tone_max"] is not None and x["tone_max"] > cal["bars_v1"]["c_tone"]]},
           "pass": not fa and not fb and all(not c["over_corner_bar_4.809"] for c in corners if c["binding"])}
    dump(out, str(OUT / "p5.json"))
    print("a1 FAIL %d/%d:" % (len(fa), len(rows)), [(r["join"], r["a1_binding"]) for r in rows if not r["pass"]])
    print("corner 2_2\\3_3:", out["corner_binding_2_2_3_3"][0]["a1_corner"], " corners over bar (report):", out["corners_over_bar_report_only"])
    print("b_max", out["b_max"], "b_over", fb, " v1 anti ctx", out["v1_anti_corners_context"])
    print("anti:", [(x["join"], x["a1_raw"], x["a1_substituted"]) for x in anti])


if __name__ == "__main__":
    main()
