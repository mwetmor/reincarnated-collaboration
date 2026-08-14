#!/usr/bin/env python3
"""RUN KC2-PM4 · LAP Q · I-Q2 — FCT glyph-stroke colour census (the heal-FCT existence question).

Reads the Apple-Vision OCR TSV produced by `ocr.swift` (byte-identical to Lap N's) over
  (a) a 1.0 s-cadence census of the combat span t in [683.0, 864.0]  -> 181 frames
  (b) 60 fps full frames across the top-5 pre-registered HP recovery windows -> 498 frames
and classifies every OCR box by the colour of its GLYPH STROKES, per PREREGISTRATION.md § 4 (I-Q2).

Glyph-stroke statistic (Lap N's convention, retained for comparability):
    glyph pixels := box pixels at or above the 88th luminance percentile of the box
    colour       := mean RGB of those pixels

Colour classes (pre-registered, § 4 I-Q2):
    red_taken       R/G >= 1.6
    cream_dealt     1.02 <= R/G < 1.6
    green_candidate G - max(R,B) >= 20  AND  G >= 80          [LOOSE: high recall, low precision]
    blue_candidate  B - max(R,G) >= 20  AND  B >= 80
    neutral         otherwise

READ-ONLY on every source.  Emits pm4q_fct_colour.csv + the green-candidate crops for I-Q3.
"""
import re, csv, sys, json, hashlib, collections
import numpy as np
from PIL import Image

OUT = ("/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/"
       "notes/2026-08-14-kc2-pm4-lap-q-heal-discriminator")
OCR_TSV = "/tmp/pm4q/full_ocr.tsv"

# window start timestamps as extracted (pre-registered windows padded by 0.25 s each side)
WIN_T0 = {1: 843.133, 2: 861.917, 3: 841.233, 4: 832.817, 5: 821.833}
CENSUS_T0 = 683.0

PAIR = re.compile(r'^\(?[\d,]+\s*/\s*[\d,]+\)?$')
CRIT = re.compile(r'^(\d[\d,]{0,9})\s*\(x(\d\.\d{2})\)$')
BARE = re.compile(r'^\d[\d,]{0,9}$')
SIGNED = re.compile(r'^[+-]\d[\d,]{0,9}$')

# HUD boxes: fixed screen furniture, excluded from FCT classes (Lap N's list + this lap's own additions)
HUD = [(0.715, 0.885), (0.822, 0.846), (0.486, 0.053), (0.297, 0.050),
       (0.645, 0.046), (0.700, 0.960), (0.302, 0.062), (0.648, 0.062)]


def frame_time(path):
    m = re.search(r'/census/C(\d{4})\.png$', path)
    if m:
        return CENSUS_T0 + int(m.group(1)), "census", None
    m = re.search(r'/win/w(\d)/W(\d{4})\.png$', path)
    if m:
        k = int(m.group(1))
        return WIN_T0[k] + int(m.group(2)) / 60.0, "window", k
    raise ValueError(path)


_cache = {}


def glyph_colour(path, bx, by, bw, bh):
    """Mean RGB of the box pixels at/above the 88th luminance percentile."""
    if path not in _cache:
        _cache.clear()
        _cache[path] = np.asarray(Image.open(path).convert("RGB")).astype(float)
    im = _cache[path]
    H, W, _ = im.shape
    x0, x1 = int(bx * W), int((bx + bw) * W)
    y1, y0 = int((1 - by) * H), int((1 - by - bh) * H)
    x0, x1 = max(0, x0), min(W, x1)
    y0, y1 = max(0, y0), min(H, y1)
    if x1 <= x0 or y1 <= y0:
        return None, None
    p = im[y0:y1, x0:x1].reshape(-1, 3)
    lum = 0.299 * p[:, 0] + 0.587 * p[:, 1] + 0.114 * p[:, 2]
    sel = p[lum >= np.percentile(lum, 88)]
    return sel.mean(0), (x0, y0, x1, y1)


def text_class(t):
    if PAIR.match(t):
        return "pair"
    if CRIT.match(t):
        return "crit"
    if BARE.match(t):
        return "bare"
    if SIGNED.match(t):
        return "signed"
    return "other"


def colour_class(r, g, b):
    mxrb, mxrg = max(r, b), max(r, g)
    if g - mxrb >= 20 and g >= 80:
        return "green_candidate"
    if b - mxrg >= 20 and b >= 80:
        return "blue_candidate"
    rg = r / max(g, 1.0)
    if rg >= 1.6:
        return "red_taken"
    if rg >= 1.02:
        return "cream_dealt"
    return "neutral"


def main():
    rows = []
    raw = []
    for ln in open(OCR_TSV):
        f = ln.rstrip("\n").split("\t")
        if len(f) >= 7:
            raw.append(f)
    # group by path so the image cache is hit once per frame
    raw.sort(key=lambda f: f[0])
    for path, text, conf, bx, by, bw, bh in raw:
        bx, by, bw, bh = map(float, (bx, by, bw, bh))
        t, src, wk = frame_time(path)
        c, px = glyph_colour(path, bx, by, bw, bh)
        if c is None:
            continue
        r, g, b = c
        is_hud = any(abs(bx - hx) < 0.02 and abs(by - hy) < 0.02 for hx, hy in HUD)
        rows.append(dict(
            source=src, window=wk if wk else "", frame_path=path.split("/")[-1],
            t_sec=round(t, 4), text=text, ocr_conf=float(conf),
            text_class=text_class(text.strip()), is_hud=int(is_hud),
            colour_class=colour_class(r, g, b),
            rgb_r=round(r, 1), rgb_g=round(g, 1), rgb_b=round(b, 1),
            r_over_g=round(r / max(g, 1.0), 3),
            g_minus_maxrb=round(g - max(r, b), 1),
            bbox_x=round(bx, 5), bbox_y=round(by, 5), bbox_w=round(bw, 5), bbox_h=round(bh, 5),
            px_x0=px[0], px_y0=px[1], px_x1=px[2], px_y1=px[3],
        ))
    rows.sort(key=lambda z: (z["source"], z["t_sec"], -z["ocr_conf"]))
    with open(f"{OUT}/pm4q_fct_colour.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    NUM = ("bare", "crit", "signed")
    fct = [r for r in rows if not r["is_hud"] and r["text_class"] in NUM]
    print(f"OCR observations                 : {len(rows)}")
    print(f"non-HUD numeric FCT boxes        : {len(fct)}")
    print("colour census (non-HUD numeric)  :",
          dict(collections.Counter(r["colour_class"] for r in fct)))
    print("colour census (ALL boxes)        :",
          dict(collections.Counter(r["colour_class"] for r in rows)))

    pc1 = sum(1 for r in fct if r["colour_class"] == "cream_dealt")
    pc2 = sum(1 for r in fct if r["colour_class"] == "red_taken")
    print(f"\nPC-1 cream numeric FCT >= 100 : {pc1}  -> {'PASS' if pc1 >= 100 else 'FAIL'}")
    print(f"PC-2 red   numeric FCT >=   5 : {pc2}  -> {'PASS' if pc2 >= 5 else 'FAIL'}")

    cand = [r for r in fct if r["colour_class"] == "green_candidate"]
    print(f"\ngreen_candidate numeric FCT boxes : {len(cand)}  (ALL hand-adjudicated, I-Q3)")
    for r in cand:
        print(f"   t={r['t_sec']:9.3f} conf={r['ocr_conf']:.2f} "
              f"RGB=({r['rgb_r']},{r['rgb_g']},{r['rgb_b']}) "
              f"g-max(r,b)={r['g_minus_maxrb']:6.1f} {r['text']!r}")

    # also report green candidates of ANY text class, so nothing green is silently dropped
    gall = [r for r in rows if r["colour_class"] == "green_candidate"]
    print(f"\ngreen_candidate boxes of ANY class: {len(gall)}")
    print("   by text_class:", dict(collections.Counter(r["text_class"] for r in gall)))

    json.dump(dict(
        n_obs=len(rows), n_numeric_fct=len(fct),
        pc1_cream=pc1, pc2_red=pc2,
        pc1_pass=pc1 >= 100, pc2_pass=pc2 >= 5,
        n_green_numeric=len(cand), n_green_any=len(gall),
    ), open("/tmp/pm4q/iq2_summary.json", "w"), indent=2)

    h = hashlib.sha256(open(f"{OUT}/pm4q_fct_colour.csv", "rb").read()).hexdigest()
    print(f"\npm4q_fct_colour.csv rows={len(rows)} sha256={h}")


if __name__ == "__main__":
    main()
